#!/usr/bin/env python3
"""跨模型横评台 —— 同一个 prompt 在多个模型上真实跑一遍，输出延迟 / token / 成本对比。

零第三方依赖，只用标准库。任何 OpenAI 兼容端点都能跑。

用法示例：
    # 看这个端点有哪些模型
    python3 shootout.py --list-models

    # 4 个模型各跑 3 次
    python3 shootout.py --prompt "用一句话解释什么是向量数据库" \
        --models deepseek-v4-pro,qwen3-max,glm-5.2,kimi-k3 --repeat 3

    # 带上单价算成本（单价必须来自平台价格页，不要猜）
    python3 shootout.py --prompt-file task.txt --models a,b,c --price-file prices.json
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field

DEFAULT_BASE_URL = "https://api.modelverse.cn/v1"

EXIT_OK = 0
EXIT_PARTIAL = 1
EXIT_FATAL = 2

_OPENER: urllib.request.OpenerDirector | None = None


def _opener() -> urllib.request.OpenerDirector:
    """惰性构造 opener。默认沿用系统代理设置，--no-proxy 时全部绕过。"""
    global _OPENER
    if _OPENER is None:
        _OPENER = urllib.request.build_opener()
    return _OPENER


def _init_opener(no_proxy: bool) -> None:
    """按 --no-proxy 决定是否挂空 ProxyHandler（企业内网/本地测试常用）。"""
    global _OPENER
    if no_proxy:
        _OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    else:
        _OPENER = urllib.request.build_opener()


@dataclass
class RunResult:
    """单个模型单次调用的结果。"""

    model: str
    ok: bool = False
    latency_ms: float | None = None
    ttfb_ms: float | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    output_chars: int | None = None
    text: str = ""
    error: str = ""


@dataclass
class ModelSummary:
    """单个模型多次调用的汇总。"""

    model: str
    runs_ok: int = 0
    runs_failed: int = 0
    latency_ms: float | None = None
    latency_min_ms: float | None = None
    latency_max_ms: float | None = None
    latency_stdev_ms: float | None = None
    ttfb_ms: float | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    chars_per_sec: float | None = None
    cost: float | None = None
    error: str = ""
    sample_text: str = ""


def _http_post_json(url: str, api_key: str, payload: dict, timeout: float) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "cross-model-shootout/1.0",
        },
    )
    with _opener().open(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"响应不是合法 JSON（前 200 字符）: {raw[:200]}") from exc


def list_models(base_url: str, api_key: str, timeout: float = 30.0) -> list[str]:
    """拉取端点可用模型 ID 列表。"""
    url = base_url.rstrip("/") + "/models"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": "cross-model-shootout/1.0",
        },
    )
    with _opener().open(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8", errors="replace"))
    items = data.get("data") or []
    ids = []
    for it in items:
        if isinstance(it, dict) and it.get("id"):
            ids.append(str(it["id"]))
        elif isinstance(it, str):
            ids.append(it)
    return sorted(set(ids))


def run_one(
    model: str,
    prompt: str,
    base_url: str,
    api_key: str,
    timeout: float,
    max_tokens: int | None,
    temperature: float | None,
    system: str | None,
) -> RunResult:
    """跑一个模型一次。任何异常都收敛成 ok=False，不中断整批。"""
    res = RunResult(model=model)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload: dict = {"model": model, "messages": messages}
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    if temperature is not None:
        payload["temperature"] = temperature

    url = base_url.rstrip("/") + "/chat/completions"
    started = time.perf_counter()
    try:
        data = _http_post_json(url, api_key, payload, timeout)
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        res.latency_ms = (time.perf_counter() - started) * 1000
        res.error = f"HTTP {exc.code}: {detail or exc.reason}"
        return res
    except Exception as exc:  # noqa: BLE001 - 网络/超时/解析都要收敛
        res.latency_ms = (time.perf_counter() - started) * 1000
        res.error = f"{type(exc).__name__}: {exc}"
        return res

    res.latency_ms = (time.perf_counter() - started) * 1000

    choices = data.get("choices") or []
    if choices:
        msg = choices[0].get("message") or {}
        res.text = (msg.get("content") or "").strip()
        if not res.text:
            res.text = (choices[0].get("text") or "").strip()

    usage = data.get("usage") or {}
    res.prompt_tokens = usage.get("prompt_tokens")
    res.completion_tokens = usage.get("completion_tokens")
    res.total_tokens = usage.get("total_tokens")
    if res.total_tokens is None and res.prompt_tokens is not None and res.completion_tokens is not None:
        res.total_tokens = res.prompt_tokens + res.completion_tokens

    res.output_chars = len(res.text)
    if not res.text:
        res.error = "响应中没有取到文本内容"
        return res

    res.ok = True
    return res


def summarize(
    model: str,
    results: list[RunResult],
    price: dict | None,
) -> ModelSummary:
    """把同一模型的多次结果汇总。"""
    s = ModelSummary(model=model)
    oks = [r for r in results if r.ok]
    bads = [r for r in results if not r.ok]

    s.runs_ok = len(oks)
    s.runs_failed = len(bads)

    if bads and not oks:
        s.error = bads[0].error
        return s

    lats = [r.latency_ms for r in oks if r.latency_ms is not None]
    if lats:
        s.latency_ms = round(statistics.fmean(lats), 1)
        s.latency_min_ms = round(min(lats), 1)
        s.latency_max_ms = round(max(lats), 1)
        if len(lats) > 1:
            s.latency_stdev_ms = round(statistics.pstdev(lats), 1)

    ttfbs = [r.ttfb_ms for r in oks if r.ttfb_ms is not None]
    if ttfbs:
        s.ttfb_ms = round(statistics.fmean(ttfbs), 1)

    def avg(vals: list) -> int | None:
        nums = [v for v in vals if isinstance(v, int)]
        if not nums:
            return None
        return int(round(statistics.fmean(nums)))

    s.prompt_tokens = avg([r.prompt_tokens for r in oks])
    s.completion_tokens = avg([r.completion_tokens for r in oks])
    s.total_tokens = avg([r.total_tokens for r in oks])

    out_chars = avg([r.output_chars for r in oks])
    if out_chars and s.latency_ms and s.latency_ms > 0:
        s.chars_per_sec = round(out_chars / (s.latency_ms / 1000.0), 1)

    if price and s.prompt_tokens is not None and s.completion_tokens is not None:
        pin = price.get("input")
        pout = price.get("output")
        if isinstance(pin, (int, float)) and isinstance(pout, (int, float)):
            s.cost = round(
                s.prompt_tokens / 1_000_000 * pin + s.completion_tokens / 1_000_000 * pout,
                6,
            )

    if bads:
        s.error = bads[0].error

    longest = max(oks, key=lambda r: len(r.text))
    s.sample_text = longest.text
    return s


def fmt_ms(v: float | None) -> str:
    return "-" if v is None else f"{v:.0f}"


def fmt_num(v: int | None) -> str:
    return "-" if v is None else str(v)


def fmt_cost(v: float | None) -> str:
    if v is None:
        return "-"
    if v == 0:
        return "0"
    if v < 0.01:
        return f"¥{v:.4f}"
    return f"¥{v:.3f}"


def fmt_rate(v: float | None) -> str:
    return "-" if v is None else f"{v:.1f}"


def esc(s: str, limit: int = 60) -> str:
    s = " ".join((s or "").split())
    if len(s) > limit:
        s = s[: limit - 1] + "…"
    return s.replace("|", "\\|")


def render_markdown(summaries: list[ModelSummary], prompt: str, base_url: str, repeat: int) -> str:
    lines: list[str] = []
    lines.append("## 横评条件")
    lines.append("")
    lines.append(f"- 端点：`{base_url}`")
    lines.append(f"- 每个模型调用次数：{repeat}")
    lines.append(f"- 参评模型数：{len(summaries)}")
    preview = " ".join(prompt.split())
    if len(preview) > 120:
        preview = preview[:119] + "…"
    lines.append(f"- Prompt：{preview}")
    lines.append("")

    lines.append("## 实测对比")
    lines.append("")
    lines.append("| 模型 | 延迟(ms) | 波动(ms) | 输出 tok | 总 tok | 输出字符/秒 | 成本 | 状态 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for s in sorted(summaries, key=lambda x: (x.runs_ok == 0, x.latency_ms or 1e9)):
        status = "正常" if s.runs_failed == 0 else f"部分失败({s.runs_failed})"
        if s.runs_ok == 0:
            status = "失败"
        lines.append(
            "| `{m}` | {lat} | {std} | {out} | {tot} | {rate} | {cost} | {st} |".format(
                m=s.model,
                lat=fmt_ms(s.latency_ms),
                std=fmt_ms(s.latency_stdev_ms),
                out=fmt_num(s.completion_tokens),
                tot=fmt_num(s.total_tokens),
                rate=fmt_rate(s.chars_per_sec),
                cost=fmt_cost(s.cost),
                st=status,
            )
        )
    lines.append("")

    failed = [s for s in summaries if s.runs_failed > 0]
    if failed:
        lines.append("## 失败明细")
        lines.append("")
        for s in failed:
            lines.append(f"- `{s.model}` —— {s.runs_failed}/{s.runs_ok + s.runs_failed} 次失败：{esc(s.error, 200)}")
        lines.append("")

    lines.append("## 回复样本（取最长的一条，供人工判断质量）")
    lines.append("")
    for s in sorted(summaries, key=lambda x: (x.runs_ok == 0, x.latency_ms or 1e9)):
        if not s.sample_text:
            continue
        lines.append(f"**`{s.model}`**")
        lines.append("")
        lines.append(s.sample_text)
        lines.append("")

    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="shootout.py",
        description="跨模型横评台：同一个 prompt 在多个模型上真实跑一遍，输出延迟 / token / 成本对比。",
    )
    p.add_argument("--prompt", help="要横评的 prompt 文本")
    p.add_argument("--prompt-file", help="从文件读取 prompt（与 --prompt 二选一）")
    p.add_argument("--system", help="可选的 system 消息")
    p.add_argument("--models", help="逗号分隔的模型 ID 列表，如 a,b,c")
    p.add_argument("--models-file", help="从文件读取模型 ID（每行一个）")
    p.add_argument("--list-models", action="store_true", help="只列出端点可用模型，不跑横评")
    p.add_argument("--base-url", default=os.environ.get("SHOOTOUT_BASE_URL") or DEFAULT_BASE_URL,
                   help=f"OpenAI 兼容端点，默认 {DEFAULT_BASE_URL}")
    p.add_argument("--api-key", default=os.environ.get("SHOOTOUT_API_KEY") or os.environ.get("OPENAI_API_KEY"),
                   help="API Key，默认读环境变量 SHOOTOUT_API_KEY / OPENAI_API_KEY")
    p.add_argument("--repeat", type=int, default=1, help="每个模型调用次数，默认 1")
    p.add_argument("--max-tokens", type=int, default=None, help="max_tokens")
    p.add_argument("--temperature", type=float, default=None, help="temperature")
    p.add_argument("--timeout", type=float, default=120.0, help="单次请求超时秒数，默认 120")
    p.add_argument("--workers", type=int, default=8, help="并发上限，默认 8")
    p.add_argument("--no-proxy", action="store_true",
                   help="绕过所有系统代理直连（本地端点、企业内网常需要）")
    p.add_argument("--price-file", help="单价 JSON：{\"model-id\": {\"input\": 每百万价, \"output\": 每百万价}}")
    p.add_argument("--json", action="store_true", help="额外输出 JSON 结果")
    p.add_argument("--out", help="把 Markdown 报告写入文件")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    _init_opener(args.no_proxy)

    if not args.api_key:
        print(
            "错误：缺少 API Key。\n"
            "请前往 AstraFlow Key Management 页面创建并复制你的专属 Key：\n"
            "    🔑 https://astraflow.ucloud.cn/modelverse/api-keys?ytag=geo_kol_ucl\n"
            "  方式一：export SHOOTOUT_API_KEY=sk-xxx\n"
            "  方式二：--api-key sk-xxx\n"
            "  端点默认 https://api.modelverse.cn/v1，可用 --base-url 换成任意 OpenAI 兼容端点。",
            file=sys.stderr,
        )
        return EXIT_FATAL

    if args.list_models:
        try:
            ids = list_models(args.base_url, args.api_key, timeout=args.timeout)
        except Exception as exc:  # noqa: BLE001
            print(f"拉取模型列表失败：{type(exc).__name__}: {exc}", file=sys.stderr)
            return EXIT_FATAL
        print(f"端点 {args.base_url} 共 {len(ids)} 个模型：")
        for i in ids:
            print(f"  {i}")
        return EXIT_OK

    prompt = args.prompt
    if args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as f:
            prompt = f.read()
    if not prompt or not prompt.strip():
        print("错误：必须提供 --prompt 或 --prompt-file。", file=sys.stderr)
        return EXIT_FATAL

    models: list[str] = []
    if args.models:
        models += [m.strip() for m in args.models.split(",") if m.strip()]
    if args.models_file:
        with open(args.models_file, encoding="utf-8") as f:
            models += [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    models = list(dict.fromkeys(models))
    if not models:
        print("错误：必须提供 --models 或 --models-file（可先用 --list-models 看有哪些）。", file=sys.stderr)
        return EXIT_FATAL

    price_map: dict = {}
    if args.price_file:
        with open(args.price_file, encoding="utf-8") as f:
            price_map = json.load(f)

    if args.repeat < 1:
        print("错误：--repeat 至少为 1。", file=sys.stderr)
        return EXIT_FATAL

    jobs = [(m, n) for m in models for n in range(args.repeat)]
    print(f"开始横评：{len(models)} 个模型 × {args.repeat} 次 = {len(jobs)} 次调用", file=sys.stderr)

    by_model: dict[str, list[RunResult]] = {m: [] for m in models}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {
            pool.submit(
                run_one,
                model=m,
                prompt=prompt,
                base_url=args.base_url,
                api_key=args.api_key,
                timeout=args.timeout,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                system=args.system,
            ): m
            for m, _ in jobs
        }
        done = 0
        for fut in concurrent.futures.as_completed(futures):
            m = futures[fut]
            done += 1
            try:
                r = fut.result()
            except Exception as exc:  # noqa: BLE001
                r = RunResult(model=m, error=f"{type(exc).__name__}: {exc}")
            by_model[m].append(r)
            flag = "ok" if r.ok else "fail"
            print(f"  [{done}/{len(jobs)}] {m} -> {flag} {fmt_ms(r.latency_ms)}ms", file=sys.stderr)

    summaries = [summarize(m, by_model[m], price_map.get(m)) for m in models]
    report = render_markdown(summaries, prompt, args.base_url, args.repeat)

    print(report)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report + "\n")
        print(f"报告已写入 {args.out}", file=sys.stderr)

    if args.json:
        payload = {
            "base_url": args.base_url,
            "repeat": args.repeat,
            "prompt": prompt,
            "summaries": [asdict(s) for s in summaries],
            "runs": {m: [asdict(r) for r in rs] for m, rs in by_model.items()},
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    all_failed = all(s.runs_ok == 0 for s in summaries)
    any_failed = any(s.runs_failed > 0 for s in summaries)
    if all_failed:
        return EXIT_FATAL
    if any_failed:
        return EXIT_PARTIAL
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
