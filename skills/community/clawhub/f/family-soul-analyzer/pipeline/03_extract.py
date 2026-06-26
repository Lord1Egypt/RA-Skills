"""
阶段3：LLM 批量提取行为模式
============================
输入：data/denoised/chunks.jsonl
输出：data/observations/observations.jsonl

使用 Anthropic Batches API 并行处理所有对话块。
费用约为直接调用的 50%。

断点续传说明：
- 原始 API 响应缓存在 data/observations/raw_cache.jsonl
- 重跑时：已缓存的 chunk 不再调 API，只重新解析
- 已成功解析的 chunk 跳过
"""

import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
import anthropic
from config import (
    ANTHROPIC_API_KEY, BATCH_SIZE, DATA_DIR, EXTRACT_MODEL, PROMPTS_DIR,
)
from utils import iter_chunks, load_jsonl, print_step, save_jsonl


# ── 路径 ──────────────────────────────────────────────────────────────────────
OBS_DIR      = DATA_DIR / "observations"
OBS_PATH     = OBS_DIR / "observations.jsonl"
RAW_CACHE    = OBS_DIR / "raw_cache.jsonl"   # {chunk_id, raw_text} 永久缓存


# ── 请求构建 ──────────────────────────────────────────────────────────────────
def build_request(chunk: dict, prompt_template: str) -> dict:
    text = chunk["text"]
    chunk_id = chunk["chunk_id"]
    time_range = f"{chunk['start_time']} ~ {chunk['end_time']}"

    prompt = (
        prompt_template
        .replace("{{CHAT_TEXT}}", text)
        .replace("{{CHUNK_ID}}", str(chunk_id))
        .replace("{{TIME_RANGE}}", time_range)
    )
    return {
        "custom_id": f"chunk-{chunk_id}",
        "params": {
            "model": EXTRACT_MODEL,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        },
    }


# ── JSON 解析（多层回退）──────────────────────────────────────────────────────
def parse_observation(result_text: str, chunk_id: int, silent: bool = False) -> Optional[dict]:
    """从 LLM 输出中解析 JSON，多层回退策略"""
    import re

    _NO_SIGNAL = object()  # 哨兵：解析成功但 has_signal=false

    def try_parse(s: str):
        """返回 dict（成功有信号）、_NO_SIGNAL（无信号）、None（解析失败）"""
        try:
            obj = json.loads(s.strip())
            if not obj.get("has_signal", True):
                return _NO_SIGNAL
            return obj
        except json.JSONDecodeError:
            return None

    def check(r) -> Optional[dict]:
        """把 try_parse 结果转成 (should_return, value)"""
        return r  # caller handles _NO_SIGNAL and None

    def repair_truncated(s: str) -> str:
        """补全截断的 JSON：根据未闭合的 { 和 [ 补齐"""
        stack = []
        in_string = False
        escape_next = False
        for ch in s:
            if escape_next:
                escape_next = False
                continue
            if ch == "\\" and in_string:
                escape_next = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch in "{[":
                stack.append(ch)
            elif ch == "}":
                if stack and stack[-1] == "{":
                    stack.pop()
            elif ch == "]":
                if stack and stack[-1] == "[":
                    stack.pop()

        # 补全未闭合的括号（倒序）
        closing = {"[": "]", "{": "}"}
        suffix = "".join(closing[c] for c in reversed(stack))
        return s + suffix

    def fix_inner_quotes(s: str) -> str:
        """修复 JSON 字符串值内的未转义双引号（LLM 常在描述里用 "原文" 引用聊天内容）"""
        result_chars = []
        in_string = False
        i = 0
        while i < len(s):
            c = s[i]
            if c == '\\' and in_string:
                result_chars.append(c)
                i += 1
                if i < len(s):
                    result_chars.append(s[i])
                i += 1
                continue
            if c == '"':
                if not in_string:
                    in_string = True
                    result_chars.append(c)
                else:
                    j = i + 1
                    while j < len(s) and s[j] in ' \t\r\n':
                        j += 1
                    next_ch = s[j] if j < len(s) else ''
                    if next_ch in ':,}]' or j >= len(s):
                        in_string = False
                        result_chars.append(c)
                    else:
                        result_chars.append('\\')
                        result_chars.append(c)
            else:
                result_chars.append(c)
            i += 1
        return ''.join(result_chars)

    def attempt(*candidates) -> Optional[dict]:
        """对候选字符串列表依次尝试解析（含截断修复和引号修复），遇到有效结果或 _NO_SIGNAL 立即返回"""
        for s in candidates:
            if not s:
                continue
            for variant in [s, repair_truncated(s), fix_inner_quotes(s), repair_truncated(fix_inner_quotes(s))]:
                r = try_parse(variant)
                if r is _NO_SIGNAL:
                    return None   # 无信号，正常跳过，不打警告
                if r is not None:
                    return r
        return None  # 所有尝试都失败

    text = result_text.strip()
    start = text.find("{")

    # 候选1：```json ... ``` 块
    c1 = None
    m = re.search(r"```json\s*(.*?)```", text, re.DOTALL)
    if m:
        c1 = m.group(1)

    # 候选2：``` ... ``` 块（无语言标注）
    c2 = None
    m2 = re.search(r"```\s*(.*?)```", text, re.DOTALL)
    if m2:
        c2 = m2.group(1)

    # 候选3：最外层 { ... }
    c3 = None
    if start != -1:
        end = text.rfind("}")
        if end > start:
            c3 = text[start:end + 1]

    # 候选4：从 { 到文本末尾（截断场景）
    c4 = text[start:] if start != -1 else None

    # 候选5：```json 到文本末尾（截断场景）
    c5 = None
    m5 = re.search(r"```json\s*(.*)", text, re.DOTALL)
    if m5:
        c5 = m5.group(1)

    # 候选6：整段文本
    c6 = text

    result = attempt(c1, c2, c3, c4, c5, c6)
    if result is not None:
        return result

    if not silent:
        print(f"  ⚠ chunk-{chunk_id} JSON 解析失败，跳过（前50字：{text[:50]!r}）")
    return None


# ── 原始响应缓存 ───────────────────────────────────────────────────────────────
def load_raw_cache() -> dict:
    """返回 {chunk_id: raw_text}"""
    if not RAW_CACHE.exists():
        return {}
    cache = {}
    for entry in load_jsonl(RAW_CACHE):
        cache[entry["chunk_id"]] = entry["raw_text"]
    return cache


def append_raw_cache(results: dict) -> None:
    """把新的原始响应追加写入缓存。results = {custom_id: raw_text}"""
    with RAW_CACHE.open("a", encoding="utf-8") as f:
        for custom_id, raw_text in results.items():
            chunk_id = int(custom_id.replace("chunk-", ""))
            f.write(json.dumps({"chunk_id": chunk_id, "raw_text": raw_text}, ensure_ascii=False) + "\n")


# ── Batch API ─────────────────────────────────────────────────────────────────
def submit_batch(client: anthropic.Anthropic, requests: list) -> str:
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    batch_requests = [
        Request(
            custom_id=r["custom_id"],
            params=MessageCreateParamsNonStreaming(**r["params"]),
        )
        for r in requests
    ]
    batch = client.messages.batches.create(requests=batch_requests)
    print(f"  提交 batch {batch.id}，共 {len(batch_requests)} 个请求")
    return batch.id


def wait_for_batch(client: anthropic.Anthropic, batch_id: str) -> None:
    print(f"  等待 batch 完成（每 30 秒轮询一次）…")
    while True:
        batch = client.messages.batches.retrieve(batch_id)
        counts = batch.request_counts
        print(
            f"    处理中 {counts.processing} / 成功 {counts.succeeded} "
            f"/ 失败 {counts.errored} / 总计 {counts.processing + counts.succeeded + counts.errored}"
        )
        if batch.processing_status == "ended":
            break
        time.sleep(30)


def collect_results(client: anthropic.Anthropic, batch_id: str) -> dict:
    """返回 {custom_id: result_text}"""
    results = {}
    for result in client.messages.batches.results(batch_id):
        if result.result.type == "succeeded":
            msg = result.result.message
            text = next((b.text for b in msg.content if b.type == "text"), "")
            results[result.custom_id] = text
        else:
            print(f"  ⚠ {result.custom_id} API 失败：{result.result}")
    return results


# ── 主流程 ────────────────────────────────────────────────────────────────────
def main():
    print_step(3, "LLM 批量提取行为模式")

    if not ANTHROPIC_API_KEY:
        print("✗ 请设置 ANTHROPIC_API_KEY 环境变量")
        sys.exit(1)

    import httpx
    client = anthropic.Anthropic(
        api_key=ANTHROPIC_API_KEY,
        http_client=httpx.Client(proxy=None),
    )
    prompt_template = (PROMPTS_DIR / "extract_patterns.md").read_text(encoding="utf-8")
    chunks = load_jsonl(DATA_DIR / "denoised" / "chunks.jsonl")
    print(f"  读入 {len(chunks):,} 个对话块")

    OBS_DIR.mkdir(parents=True, exist_ok=True)

    # 加载已完成的观察（chunk_id 集合）
    existing: list = []
    done_ids: set = set()
    if OBS_PATH.exists():
        existing = load_jsonl(OBS_PATH)
        done_ids = {o["chunk_id"] for o in existing}
        print(f"  已有解析结果：{len(done_ids)} 个")

    # 加载原始响应缓存（已调过 API 但可能解析失败的）
    raw_cache = load_raw_cache()
    cached_ids = set(raw_cache.keys())
    print(f"  原始响应缓存：{len(cached_ids)} 个")

    # 需要调 API 的 chunk（既没解析结果，也没缓存）
    need_api = [c for c in chunks if c["chunk_id"] not in done_ids and c["chunk_id"] not in cached_ids]
    # 有缓存但没解析结果的（上次解析失败，这次免费重试）
    need_parse = [c for c in chunks if c["chunk_id"] not in done_ids and c["chunk_id"] in cached_ids]

    print(f"  需要调 API：{len(need_api)} 个")
    print(f"  有缓存待重新解析：{len(need_parse)} 个")

    all_observations = list(existing)

    # ── 阶段 A：调 API 获取新结果 ─────────────────────────────────────────────
    if need_api:
        for batch_num, batch_chunks in enumerate(iter_chunks(need_api, BATCH_SIZE)):
            print(f"\n  [API] 批次 {batch_num + 1}（{len(batch_chunks)} 个块）")
            requests = [build_request(c, prompt_template) for c in batch_chunks]

            batch_id = submit_batch(client, requests)
            wait_for_batch(client, batch_id)
            raw_results = collect_results(client, batch_id)

            # 写入原始缓存（先存，再解析）
            append_raw_cache(raw_results)
            for custom_id, raw_text in raw_results.items():
                chunk_id = int(custom_id.replace("chunk-", ""))
                raw_cache[chunk_id] = raw_text

            # 解析本批次
            batch_obs = []
            for chunk in batch_chunks:
                raw = raw_cache.get(chunk["chunk_id"], "")
                obs = parse_observation(raw, chunk["chunk_id"])
                if obs:
                    batch_obs.append(obs)

            all_observations.extend(batch_obs)
            print(f"  本批次提取出 {len(batch_obs)} 条有效观察")
            save_jsonl(all_observations, OBS_PATH)

    # ── 阶段 B：重新解析已缓存但失败的 chunk（免费）─────────────────────────
    if need_parse:
        print(f"\n  [重解析] 尝试修复 {len(need_parse)} 个缓存 chunk…")
        recovered = 0
        for chunk in need_parse:
            raw = raw_cache.get(chunk["chunk_id"], "")
            obs = parse_observation(raw, chunk["chunk_id"])
            if obs:
                all_observations.append(obs)
                recovered += 1
        if recovered:
            save_jsonl(all_observations, OBS_PATH)
            print(f"  恢复了 {recovered} 个之前失败的 chunk")

    # ── 统计 ──────────────────────────────────────────────────────────────────
    obs = load_jsonl(OBS_PATH)
    all_tags: list = []
    for o in obs:
        all_tags.extend(o.get("context_tags", []))

    tag_counts = Counter(all_tags)
    print(f"\n  最常见的对话情景：")
    for tag, count in tag_counts.most_common(10):
        print(f"    {tag:15s}  {count} 次")

    print(f"\n  共 {len(obs)} 条有效观察记录")
    total = len(chunks)
    failed = total - len(obs)
    print(f"  覆盖率：{len(obs)}/{total}（{len(obs)/total*100:.1f}%），跳过 {failed} 个")


if __name__ == "__main__":
    main()
