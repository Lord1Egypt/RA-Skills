#!/usr/bin/env python3
"""回填历史周报的中文翻译（外科手术式：只改 HTML 内的 NEWS_DATA）。

背景
----
英文报道的中文总结依赖**本地 Ollama**（best-effort）。生成那一刻若服务没起、
CPU 忙超时、或缓存未命中，翻译会**静默跳过**，报告照常产出但保留英文。
历史期次一旦漏翻就永久是英文——RSS 仅保留约 1 周，原始 news.json 通常已
无法回抓重建。

本脚本直接从**已发布的 HTML** 提取 ``NEWS_DATA``，补译后原样写回，
因此不需要任何原始输入文件。

用法
----
    # 只核查，不改动
    python scripts/backfill_translations.py --check AI_News_2026-08-31.html

    # 回填（缓存命中优先，未命中的调本地 Ollama）
    python scripts/backfill_translations.py AI_News_2026-08-31.html AI_News_2026-08-24.html

    # 只走缓存，不调用 Ollama（离线可用，能补多少算多少）
    python scripts/backfill_translations.py --no-ollama AI_News_*.html

    # 回填同时产出可发布的译文源
    python scripts/backfill_translations.py --emit-source translations.json AI_News_*.html
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from aiweekly.translate import (  # noqa: E402
    Translator, _detect_lang, _TranslateCache, _title_key,
)
from html import escape as html_escape  # noqa: E402  避免与局部变量 html 同名

NEWS_DATA_RE = re.compile(r"const\s+NEWS_DATA\s*=\s*(\[.*?\]);", re.S)
CJK = re.compile(r"[一-鿿]")

TRANSLATIONS_SCHEMA = "ai-weekly-translations/v1"


def load_news_data(html: str) -> tuple[list[dict], re.Match] | tuple[None, None]:
    """提取 HTML 内的 NEWS_DATA；失败返回 (None, None)。"""
    m = NEWS_DATA_RE.search(html)
    if not m:
        return None, None
    try:
        return json.loads(m.group(1)), m
    except json.JSONDecodeError:
        return None, None


def write_news_data(html: str, data: list[dict], m: re.Match) -> str:
    """把 NEWS_DATA 原样写回（序列化格式与生成器保持一致）。"""
    blob = json.dumps(data, ensure_ascii=False)
    return html[:m.start(1)] + blob + html[m.end(1):]


def coverage(data: list[dict]) -> dict:
    """统计该期英文条目的中文覆盖情况。"""
    en = [x for x in data
          if (x.get("lang") or _detect_lang(x.get("title", ""),
                                            x.get("summary", ""))) == "en"]
    return {
        "total": len(data),
        "en": len(en),
        "cn_summary": sum(1 for x in en if x.get("cn_summary")),
        "cn_title": sum(1 for x in en if x.get("cn_title")),
    }


def check_only(paths: list[Path]) -> int:
    print(f"{'文件':26s}{'总条':>6s}{'英条':>6s}{'摘要':>7s}{'标题':>7s}  判定")
    print("-" * 72)
    need = []
    for p in paths:
        html = p.read_text(encoding="utf-8")
        data, m = load_news_data(html)
        if data is None:
            print(f"{p.name:26s}  ⚠️ 未找到 NEWS_DATA，跳过")
            continue
        c = coverage(data)
        miss_sum = c["en"] - c["cn_summary"]
        miss_tit = c["en"] - c["cn_title"]
        if miss_sum or miss_tit:
            verdict = f"缺摘要 {miss_sum} / 缺标题 {miss_tit}"
            need.append(p)
        else:
            verdict = "完整"
        print(f"{p.name:26s}{c['total']:6d}{c['en']:6d}"
              f"{c['cn_summary']:7d}{c['cn_title']:7d}  {verdict}")
    print("-" * 72)
    print(f"需回填 {len(need)}/{len(paths)} 期")
    return 0


def backfill(paths: list[Path], tr: Translator, dry_run: bool) -> dict:
    """逐期回填，返回汇总统计。"""
    stats = {"files": 0, "cache_hit": 0, "translated": 0, "failed": 0,
             "title_only": 0}
    for p in paths:
        html = p.read_text(encoding="utf-8")
        data, m = load_news_data(html)
        if data is None:
            print(f"⚠️ {p.name}: 未找到 NEWS_DATA，跳过")
            continue

        before = coverage(data)
        en = [x for x in data
              if (x.get("lang") or _detect_lang(x.get("title", ""),
                                                x.get("summary", ""))) == "en"]
        todo = [x for x in en if not x.get("cn_summary")]
        # 有摘要但缺标题的，单独补标题（translate_items 会跳过这批）
        title_only = [x for x in en if x.get("cn_summary") and not x.get("cn_title")]

        print(f"\n📄 {p.name}: {before['total']} 条 / 英文 {before['en']} "
              f"| 已有摘要 {before['cn_summary']} 标题 {before['cn_title']}")
        if not todo and not title_only:
            # 不 continue：即使译文已完整，市场信号卡仍可能缺中文注解（见下）
            print("   ✅ 译文已完整")

        hit, done, fail = 0, 0, 0
        if todo:
            before_hit = tr.stats["cache_hit"]
            tr.translate_items(data)          # 就地补 cn_summary / cn_title
            hit = tr.stats["cache_hit"] - before_hit
            done = tr.stats["translated"]
            e2 = coverage(data)
            fail = e2["en"] - e2["cn_summary"]
            print(f"   🌐 摘要：缓存命中 {hit} / 新译 {done} / 仍缺 {fail}")

        if title_only and tr.enabled and tr.available():
            n = 0
            for x in title_only:
                t = (x.get("title") or "").strip()
                if not t:
                    continue
                try:
                    from aiweekly.translate import _TITLE_PROMPT, MIN_CJK_TITLE
                    cn = tr.translate(t, prompt=_TITLE_PROMPT, min_cjk=MIN_CJK_TITLE)
                except Exception:  # noqa: BLE001  单条失败不影响其余
                    cn = None
                if cn:
                    x["cn_title"] = cn
                    n += 1
            print(f"   🔤 补中文标题 {n}/{len(title_only)}")
            stats["title_only"] += n

        after = coverage(data)
        gained = (after["cn_summary"] != before["cn_summary"]
                  or after["cn_title"] != before["cn_title"])

        # 市场信号卡是静态 HTML，新闻回填后仍需单独补中文注解
        new_html, n_cards = patch_signal_cards(
            write_news_data(html, data, m), data)
        if n_cards:
            print(f"   🏷️ 市场信号卡补中文注解 {n_cards} 张")

        if not gained and not n_cards:
            print("   ⏭️ 无新增译文，不写回")
            continue

        if dry_run:
            print(f"   🏃 dry-run：将写入 {after['cn_summary']} 摘要 / "
                  f"{after['cn_title']} 标题 / {n_cards} 张卡片注解（未落盘）")
        else:
            p.write_text(new_html, encoding="utf-8")
            print(f"   ✅ 已写回：摘要 {before['cn_summary']}→{after['cn_summary']}，"
                  f"标题 {before['cn_title']}→{after['cn_title']}")

        stats["files"] += 1
        stats["cache_hit"] += hit
        stats["translated"] += done
        stats["failed"] += fail
    return stats


def patch_signal_cards(html: str, data: list[dict]) -> tuple[str, int]:
    """给「本周市场信号」卡补 `.ms-cn` 中文注解。

    必要性：市场信号卡是**渲染时**生成的静态 HTML。该期生成时没有译文，
    卡片自然没有中文注解；只回填 NEWS_DATA 会让新闻列表有中文、卡片仍全英文，
    `validate_report.py` 的 `signals_cn` 检查因此失败。

    做法与渲染层 `aiweekly/market.py` 保持一致：在 `ms-title` 的 `</a>` 之后、
    `ms-meta` 之前插入同一结构的注解块。
    """
    cn_by_url = {x["url"]: x["cn_summary"] for x in data
                 if x.get("lang") == "en" and x.get("cn_summary") and x.get("url")}
    if not cn_by_url:
        return html, 0
    parts = html.split('<div class="ms-card">')
    if len(parts) < 2:
        return html, 0
    n = 0
    out = [parts[0]]
    for seg in parts[1:]:
        head = seg[:2000]
        if 'class="ms-cn"' in head:
            out.append(seg)
            continue
        hm = re.search(r'<a class="ms-title" href="([^"]*)"[^>]*>.*?</a>', head, re.S)
        if hm and hm.group(1) in cn_by_url:
            cn = html_escape(cn_by_url[hm.group(1)])
            ins = (f'<div class="ms-cn"><span class="cn-badge">中文</span> {cn}</div>')
            seg = seg[:hm.end()] + ins + seg[hm.end():]
            n += 1
        out.append(seg)
    return '<div class="ms-card">'.join(out), n


def emit_source(paths: list[Path], out: Path) -> int:
    """把各期已回填的译文汇总成可发布的译文源（按 URL 索引）。"""
    from aiweekly.translate import _TranslateCache
    entries: dict[str, dict] = {}
    for p in paths:
        html = p.read_text(encoding="utf-8")
        data, _ = load_news_data(html)
        if not data:
            continue
        for x in data:
            if not (x.get("cn_summary") or x.get("cn_title")):
                continue
            url = (x.get("url") or "").strip()
            if not url:
                continue
            src = (x.get("summary") or x.get("title") or "").strip()
            entries[url] = {
                "src_hash": _TranslateCache._src_hash(src),
                "title_key": _title_key(x.get("title")),
                "cn_title": x.get("cn_title") or "",
                "cn_summary": x.get("cn_summary") or "",
            }
    payload = {
        "schema": TRANSLATIONS_SCHEMA,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "count": len(entries),
        "note": "AI 周报英文报道中文译文源。按原文 URL 索引；title_key 为标题归一化指纹，"
                "用于校验是否同一条报道。无本地翻译模型的用户可用 --translations-url 拉取。",
        "entries": entries,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print(f"\n📦 译文源已写出：{out}（{len(entries)} 条）")
    return len(entries)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="回填历史周报的中文翻译（直接改 HTML 内的 NEWS_DATA）")
    ap.add_argument("files", nargs="+", help="要处理的 HTML 文件（支持 glob）")
    ap.add_argument("--check", action="store_true", help="只核查覆盖情况，不改动文件")
    ap.add_argument("--dry-run", action="store_true", help="执行翻译但不写回文件")
    ap.add_argument("--no-ollama", action="store_true",
                    help="只用本地缓存，不调用 Ollama（离线可用）")
    ap.add_argument("--cache", default=None, help="译文缓存路径")
    ap.add_argument("--model", default="qwen2.5:7b", help="本地 Ollama 模型")
    ap.add_argument("--timeout", type=int, default=60, help="单条翻译超时秒数")
    ap.add_argument("--workers", type=int, default=3, help="并发线程数")
    ap.add_argument("--retries", type=int, default=1, help="单条失败重试次数")
    ap.add_argument("--emit-source", default=None,
                    help="额外把各期译文汇总写出为译文源 JSON")
    args = ap.parse_args()

    paths: list[Path] = []
    for pat in args.files:
        hits = sorted(Path().glob(pat)) if any(c in pat for c in "*?[") else [Path(pat)]
        for p in hits:
            if p.is_file() and p not in paths:
                paths.append(p)
    if not paths:
        print("❌ 未找到任何匹配文件")
        return 1

    if args.check:
        return check_only(paths)

    cache_path = args.cache or str(Path(paths[0]).parent / ".translate_cache.json")
    tr = Translator(
        enabled=not args.no_ollama, model=args.model, timeout=args.timeout,
        max_workers=args.workers, retries=args.retries,
        translate_title=True, cache_path=cache_path)

    if not args.no_ollama:
        ok, detail = None, ""
        try:
            from aiweekly.translate import ollama_health
            ok, detail = ollama_health(timeout=5.0, model=args.model)
        except Exception:  # noqa: BLE001
            ok = False
        print(f"🩺 本地 Ollama：{detail}")
        if not ok:
            print("   ↳ 不可用，将只复用本地缓存译文；未命中的保留英文原文")

    t0 = time.time()
    stats = backfill(paths, tr, dry_run=args.dry_run)
    print(f"\n{'=' * 60}")
    print(f"📊 回填汇总：处理 {stats['files']} 期 | 缓存命中 {stats['cache_hit']} | "
          f"新译 {stats['translated']} | 补标题 {stats['title_only']} | "
          f"仍缺 {stats['failed']} | 耗时 {time.time() - t0:.0f}s")
    print(f"   Translator 统计：{tr.stats}")

    if args.emit_source:
        emit_source(paths, Path(args.emit_source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
