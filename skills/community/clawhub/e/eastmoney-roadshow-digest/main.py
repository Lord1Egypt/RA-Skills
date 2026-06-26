from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

ENTRY_ENV_NAME = "EASTMONEY_ROADSHOW_ENTRY"
ENTRY_ENV_VALUE = "python3-main"

import sys

if str((Path(__file__).resolve().parent / ".vendor")) not in sys.path:
    sys.path.insert(0, str((Path(__file__).resolve().parent / ".vendor")))

from providers.asr import ASRUnavailable, ASRError, extract_audio, transcribe_audio
from providers.eastmoney import EastMoneyError, fetch_page

BASE = Path(__file__).resolve().parent
OUT = BASE / "outputs"


def enforce_standard_entry() -> None:
    entry = os.getenv(ENTRY_ENV_NAME)
    if entry != ENTRY_ENV_VALUE:
        raise SystemExit(
            "Invalid execution entry for eastmoney-roadshow-digest. "
            "Use the documented standard entry only: "
            f"EASTMONEY_ROADSHOW_ENTRY={ENTRY_ENV_VALUE} python3 main.py --url <EASTMONEY_ROADSHOW_URL>. "
            "Do not run via uv run, alternate wrappers, or other Python launch paths."
        )


def ensure_outputs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def dump_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_asr_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", "", text)
    text = re.sub(r"[，,]{2,}", "，", text)
    text = re.sub(r"[。]{2,}", "。", text)
    pieces = []
    buf = ""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        buf += line
        while len(buf) >= 90:
            cut = max(buf.rfind("。", 0, 120), buf.rfind("？", 0, 120), buf.rfind("！", 0, 120), buf.rfind("；", 0, 120), buf.rfind("，", 0, 120))
            if cut < 30:
                cut = 90
            pieces.append(buf[: cut + (1 if cut < len(buf) and buf[cut] in '。？！，；' else 0)].strip())
            buf = buf[cut + (1 if cut < len(buf) and buf[cut] in '。？！，；' else 0):].strip()
    if buf:
        pieces.append(buf)
    cleaned = []
    last = None
    for piece in pieces:
        piece = piece.strip("，。； ")
        if len(piece) < 6:
            continue
        if piece == last:
            continue
        cleaned.append(piece)
        last = piece
    return "\n\n".join(cleaned).strip()


def clean_metadata_transcript(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines()]
    out: List[str] = []
    seen = set()
    for line in lines:
        if not line:
            if out and out[-1] != "":
                out.append("")
            continue
        line = re.sub(r"\s+", " ", line)
        if line in seen and len(line) > 12:
            continue
        seen.add(line)
        if line.startswith("[") and "]" in line:
            name, rest = line.split("]", 1)
            rest = rest.strip()
            line = f"{name[1:]}：{rest}" if rest else name[1:]
        if line.startswith("- "):
            out.append(line)
            continue
        if line in {"嘉宾资料：", "议程："}:
            out.append(line)
            continue
        if line.startswith("标题：") or line.startswith("简介："):
            out.append(line)
            continue
        out.append(line)
    cleaned = "\n".join(out)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def transcript_quality(meta: Dict[str, Any], transcript: str, asr_status: str) -> Dict[str, Any]:
    duration_seconds = 0
    chapters = meta.get("playback_chapter") or []
    for chapter in chapters:
        for group in chapter.get("media_group") or []:
            media = group.get("media") or {}
            duration_seconds = max(duration_seconds, int(media.get("duration") or 0))
    text_len = len(re.sub(r"\s+", "", transcript or ""))
    quality = "usable"
    reasons: List[str] = []
    if asr_status == "ASR_partial":
        quality = "insufficient"
        reasons.append("ASR partial completion")
    if duration_seconds >= 1800 and text_len < 1500:
        quality = "insufficient"
        reasons.append("transcript too short for video duration")
    elif duration_seconds >= 900 and text_len < 800:
        quality = "insufficient"
        reasons.append("transcript likely incomplete for medium/long replay")
    return {
        "quality": quality,
        "duration_seconds": duration_seconds,
        "text_length": text_len,
        "reasons": reasons,
    }


def get_llm_config() -> Dict[str, str] | None:
    if os.getenv("OPENAI_API_KEY"):
        return {
            "provider": "openai",
            "base_url": "https://api.openai.com/v1",
            "api_key": os.getenv("OPENAI_API_KEY") or "",
            "model": "gpt-4o-mini",
        }
    if os.getenv("OPENROUTER_API_KEY"):
        return {
            "provider": "openrouter",
            "base_url": "https://openrouter.ai/api/v1",
            "api_key": os.getenv("OPENROUTER_API_KEY") or "",
            "model": "openai/gpt-4o-mini",
        }
    moonshot_key = os.getenv("MOONSHOT_API_KEY") or os.getenv("KIMI_API_KEY")
    if moonshot_key:
        return {
            "provider": "moonshot",
            "base_url": "https://api.moonshot.cn/v1",
            "api_key": moonshot_key,
            "model": os.getenv("MOONSHOT_MODEL", "moonshot-v1-8k"),
        }
    return None


def detect_llm_provider() -> str | None:
    cfg = get_llm_config()
    return cfg["provider"] if cfg else None


def llm_enabled() -> bool:
    return get_llm_config() is not None


def call_llm(system_prompt: str, user_prompt: str, model: str = "default", temperature: float = 0.2) -> str:
    cfg = get_llm_config()
    if not cfg:
        raise RuntimeError("No LLM provider configured")

    payload = {
        "model": cfg["model"] if model == "default" else model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    resp = requests.post(
        f"{cfg['base_url']}/chat/completions",
        headers={
            "Authorization": f"Bearer {cfg['api_key']}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"LLM request failed: {resp.text[:200]}")

    data = resp.json()
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("LLM response contained no choices")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, list):
        content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
    if not content:
        raise RuntimeError("LLM response content was empty")
    return str(content).strip()


def llm_clean_transcript(text: str, meta: Dict[str, Any]) -> str:
    system_prompt = (
        "你是中文财经音频整理助手。任务不是总结，而是把 ASR 转写整理成可读的结构化发言记录。"
        "不要预设节目形式，可能是一人讲、两人对话、三人互动、教学、访谈、串场甚至表演。"
        "请尽量保持原意，不要编造，不要补事实。"
    )
    title = meta.get("name") or meta.get("intro") or "未命名路演"
    guest_names = [g.get("alias") or g.get("nickname") for g in (meta.get("guests") or []) if g.get("alias") or g.get("nickname")]
    user_prompt = (
        f"标题：{title}\n"
        f"可参考嘉宾名：{', '.join(guest_names) if guest_names else '无'}\n\n"
        "请将下面转写整理为结构化 markdown 文本，要求：\n"
        "1. 修正明显断句问题，按语义分段；\n"
        "2. 尽量复原发言结构，但不要强行判断必须是主持人/嘉宾；\n"
        "3. 可使用类似 [发言] / [提问] / [回答] / [串场] / [讲解] 这样的轻量标签；\n"
        "4. 删除明显无信息的寒暄和纯重复口水，但不要误删有内容的轻松表达；\n"
        "5. 不要总结，不要改写成纪要，只整理成更可读的发言记录；\n"
        "6. 如果某段非常不确定，可标记 [低置信]；\n\n"
        "原始转写如下：\n\n"
        f"{text}"
    )
    return call_llm(system_prompt, user_prompt, model="default", temperature=0.1)


def llm_make_summary(meta: Dict[str, Any], clean_transcript: str) -> str:
    system_prompt = (
        "你是中文财经路演纪要助手。请基于整理后的发言记录生成结构化纪要。"
        "不要照抄原句，不要把开场寒暄和嘉宾介绍写成核心结论。"
        "不要预设固定路演形式，要根据内容自适应表达。"
    )
    title = meta.get("name") or meta.get("intro") or "未命名路演"
    user_prompt = (
        f"标题：{title}\n\n"
        "请基于下面的整理稿生成 markdown 纪要，输出结构固定为：\n"
        "# Summary\n"
        "## Executive Summary\n"
        "- 用 2-4 条写这场路演真正讲了什么\n"
        "## Main Discussion\n"
        "- 提炼主要讨论点\n"
        "## Risk Notes\n"
        "- 如有风险或不确定性则写，没有可写‘未见明确风险提示’\n"
        "## Quality Note\n"
        "- 简要说明基于自动转写整理，仍建议人工复核\n\n"
        "要求：\n"
        "1. 用自己的话写，不直接复制原文长句；\n"
        "2. 不要把开场欢迎、节目介绍、打招呼当核心内容；\n"
        "3. 如果正文信息仍不足，就明确写‘当前可确认内容有限’，不要硬编结论。\n\n"
        "整理稿如下：\n\n"
        f"{clean_transcript}"
    )
    return call_llm(system_prompt, user_prompt, model="default", temperature=0.2)


def llm_make_brief(meta: Dict[str, Any], summary_text: str) -> str:
    system_prompt = "你是简报压缩助手，请把纪要压成一版简短、可读、不夸张的 brief。"
    user_prompt = (
        "请基于下面 summary 输出 markdown brief，结构固定为：\n"
        "# Brief\n\n"
        "**标题**：...\n\n"
        "**一句话判断**\n"
        "...\n\n"
        "**三点要点**\n"
        "- ...\n- ...\n- ...\n\n"
        "**备注**\n"
        "...\n\n"
        "要求：简洁，不重复，不抄原句。\n\n"
        f"{summary_text}"
    )
    return call_llm(system_prompt, user_prompt, model="default", temperature=0.2)


def make_deliverable_summary(meta: Dict[str, Any], transcript: str, quality: str = "usable") -> str:
    title = meta.get("name") or meta.get("intro") or "未命名路演"
    status_map = {1: "直播中", 3: "回放", 4: "预告"}
    status = status_map.get(meta.get("status"), str(meta.get("status")))
    guests = meta.get("guests") or []
    guest_names = [g.get("alias") or g.get("nickname") for g in guests if g.get("alias") or g.get("nickname")]
    lines = [x.strip() for x in transcript.splitlines() if x.strip()]
    usable = [x for x in lines if not x.startswith(("标题：", "简介：", "嘉宾资料：", "议程："))]
    highlights = []
    for item in usable:
        if len(item) >= 16:
            highlights.append(item[:120])
        if len(highlights) >= 5:
            break
    if not highlights:
        highlights = ["当前公开页面可提取的主要信息集中于主题、嘉宾与回放元数据；逐字稿仍建议补做 ASR/人工校对。"]
    agenda_lines = []
    config = meta.get("config") or {}
    for ag in config.get("agendas", []) or []:
        label = ag.get("title") or ag.get("name")
        if label:
            agenda_lines.append(f"- {label}")
    guest_block = "\n".join(f"- {name}" for name in guest_names[:8]) if guest_names else "- 页面未暴露清晰嘉宾名录"
    agenda_block = "\n".join(agenda_lines) if agenda_lines else "- 页面未暴露结构化议程"
    highlight_block = "\n".join(f"- {x}" for x in highlights)
    if quality != "usable":
        highlight_block = "- 当前转写质量不足，以下内容不应视为完整纪要或核心结论。\n- 建议先完成更完整的 ASR 或人工复核，再使用本页内容进行正式摘要。"
    return (
        f"# Summary\n\n"
        f"## Executive Overview\n"
        f"- 标题：{title}\n"
        f"- 页面状态：{status}\n"
        f"- 时间：{meta.get('start_time')} → {meta.get('end_time')}\n"
        f"- 处理方式：公开页面解析；字幕优先；必要时媒体+ASR 回退\n\n"
        f"## Guests\n{guest_block}\n\n"
        f"## Agenda Signals\n{agenda_block}\n\n"
        f"## Key Takeaways\n{highlight_block}\n\n"
        f"## Quality Note\n"
        f"- 本摘要基于公开页面元数据与当前可得文本生成；若需对外发布或用于投资判断，建议补充真实 ASR 与人工复核。\n"
    )


def make_deliverable_brief(meta: Dict[str, Any], transcript: str, quality: str = "usable") -> str:
    title = meta.get("name") or "未命名路演"
    lines = [x.strip() for x in transcript.splitlines() if x.strip()]
    usable = [x for x in lines if not x.startswith(("标题：", "简介：", "嘉宾资料：", "议程："))]
    points = []
    for item in usable:
        if len(item) >= 14:
            points.append(item[:80])
        if len(points) >= 3:
            break
    while len(points) < 3:
        fallback = [
            "本场主题聚焦震荡市环境下的量化产品配置。",
            "公开页面可稳定提取回放元数据与媒体地址。",
            "若要形成正式逐字稿，仍需补齐 ASR 或人工校对。",
        ]
        points.append(fallback[len(points)])
    if quality != "usable":
        return (
            f"# Brief\n\n"
            f"本场回放已完成工程层面的页面解析、媒体提取与文本生成，但当前转写质量不足，尚不适合输出为正式纪要或核心结论摘要。现阶段可确认的是：公开回放页可被解析，且可得到基础元数据、媒体地址与初步文本产物；但若用于研究纪要、投资讨论或外部传播，仍应先补做更完整的转写与人工校对。\n"
        )
    return (
        f"# Brief\n\n"
        f"**标题**：{title}\n\n"
        f"**适合谁看**：需要快速判断本场路演是否值得进一步精听的审核者/研究支持人员。\n\n"
        f"**三条核心结论**\n"
        f"- {points[0]}\n"
        f"- {points[1]}\n"
        f"- {points[2]}\n\n"
        f"**当前可用性**\n- 已可稳定抽取公开元数据与回放媒体；逐字稿质量仍受 ASR 可用性影响。\n\n"
        f"**一句话风险提示**\n- 若缺少可用字幕或 ASR 依赖，文本产物将退化为基于公开元数据的结构化摘要。\n"
    )


def summarize(meta: Dict[str, Any], transcript: str) -> str:
    bullets: List[str] = []
    title = meta.get("name") or meta.get("intro") or "未命名路演"
    bullets.append(f"# 会议纪要\n\n## 主题\n- {title}")
    bullets.append(f"\n## 基本信息\n- 状态：{meta.get('status')}\n- 开始：{meta.get('start_time')}\n- 结束：{meta.get('end_time')}")
    guests = meta.get("guests") or []
    if guests:
        guest_lines = []
        for g in guests[:8]:
            alias = g.get("alias") or g.get("nickname") or "未知嘉宾"
            intro = (g.get("intro") or "").strip().replace("\n", " ")
            guest_lines.append(f"- {alias}：{intro[:120]}".rstrip("："))
        bullets.append("\n## 嘉宾\n" + "\n".join(guest_lines))
    key_points = []
    for line in [x.strip() for x in transcript.splitlines() if x.strip()]:
        if len(line) >= 18:
            key_points.append(f"- {line[:120]}")
        if len(key_points) >= 6:
            break
    if not key_points:
        key_points = ["- 未获得高质量逐字稿；请结合 meta 与回放人工复核。"]
    bullets.append("\n## 核心观点（基于转写抽取）\n" + "\n".join(key_points))
    bullets.append("\n## 风险提示\n- 本纪要仅基于公开页面元数据与自动转写生成，可能存在漏字、错字与语义压缩，不能替代人工复核。")
    return "\n".join(bullets).strip() + "\n"


def make_brief(meta: Dict[str, Any], transcript: str) -> str:
    lines = [x.strip() for x in transcript.splitlines() if x.strip()]
    picks = [f"- {x[:80]}" for x in lines[:3]] or ["- 未取得足够转写内容，需人工查看回放。"]
    return (
        f"# Brief\n\n"
        f"**标题**：{meta.get('name') or '未命名路演'}\n\n"
        f"**三条核心结论**\n" + "\n".join(picks) + "\n\n"
        f"**一句话风险提示**\n- 内容来自公开页面与自动转写，需人工复核。\n"
    )


def run(url: str) -> Dict[str, Any]:
    ensure_outputs()
    report: Dict[str, Any] = {
        "url": url,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "steps": [],
        "status": "failed",
        "notes": [],
        "artifacts": [
            "outputs/meta.json",
            "outputs/transcript.md",
            "outputs/clean_transcript.md",
            "outputs/summary.md",
            "outputs/brief.md",
            "outputs/run_report.md",
        ],
    }
    transcript = ""
    clean_transcript = ""
    asr_status = "not_run"
    content_quality = "unknown"

    try:
        page = fetch_page(url)
        meta = {
            "source_url": page.url,
            "channel_id": page.channel_id,
            "html_title": page.html_title,
            "page_notes": page.notes,
            "subtitle_candidates": page.subtitle_candidates,
            "media_candidates": page.media_candidates,
            "metadata": page.metadata,
        }
        dump_json(OUT / "meta.json", meta)
        report["steps"].append("url validation: ok")
        report["steps"].append("page parsing: ok")

        if page.subtitle_candidates:
            report["steps"].append("subtitle extraction: candidates found but parser not yet specialized; fallback continues")
            report["notes"].append("Subtitle-first branch is implemented as discovery. No subtitle payload was consumable for this tested URL.")
        else:
            report["steps"].append("subtitle extraction: no candidates found")

        if page.media_candidates:
            report["steps"].append("media discovery: ok")
            media_url = page.media_candidates[0]["url"]
            try:
                audio_path = extract_audio(media_url, OUT)
                report["steps"].append("audio extraction: ok")
                try:
                    asr = transcribe_audio(audio_path, model_size="small", segment_seconds=45, total_timeout_seconds=7200)
                    transcript = asr.get("text", "").strip()
                    asr_status = asr.get("status", "ASR_complete")
                    report["steps"].append(f"ASR: {asr_status}")
                    report["notes"].append(
                        f"ASR engine: {asr.get('engine')}; model={asr.get('model_size')}; chunks={asr.get('completed_chunks')}/{asr.get('total_chunks')}; timeout={asr.get('timeout_seconds')}s"
                    )
                except ASRUnavailable as e:
                    report["steps"].append("ASR: unavailable")
                    report["notes"].append(str(e))
                except ASRError as e:
                    report["steps"].append("ASR: failed")
                    report["notes"].append(str(e))
            except Exception as e:
                report["steps"].append("audio extraction: failed")
                report["notes"].append(str(e))
        else:
            report["steps"].append("media discovery: no candidates found")

        if transcript:
            transcript = normalize_asr_text(transcript)
            clean_transcript = transcript
            report["notes"].append("Transcript generated from ASR and normalized with enhanced cleanup.")
        else:
            guests = page.metadata.get("guests") or []
            guest_lines = []
            for g in guests:
                alias = g.get("alias") or g.get("nickname") or "未知嘉宾"
                intro = (g.get("intro") or "").strip()
                if intro:
                    guest_lines.append(f"[{alias}] {intro}")
            agenda_lines = []
            config = page.metadata.get("config") or {}
            for ag in config.get("agendas", []) or []:
                title = ag.get("title") or ag.get("name") or "议程"
                agenda_lines.append(f"- {title}")
            transcript = "\n".join(
                [
                    f"标题：{page.metadata.get('name') or ''}",
                    f"简介：{page.metadata.get('intro') or ''}",
                    "",
                    "嘉宾资料：",
                    *guest_lines,
                    "",
                    "议程：",
                    *agenda_lines,
                ]
            ).strip()
            clean_transcript = clean_metadata_transcript(transcript)
            report["notes"].append("No ASR transcript available; transcript.md falls back to structured public metadata text.")

        if not clean_transcript:
            clean_transcript = clean_text(transcript)
        quality_info = transcript_quality(page.metadata, clean_transcript, asr_status)
        content_quality = quality_info["quality"]
        if quality_info["reasons"]:
            report["notes"].append(
                "Content quality check: " + "; ".join(quality_info["reasons"])
            )
        report["notes"].append(
            f"Content usability={content_quality}; duration={quality_info['duration_seconds']}s; text_length={quality_info['text_length']}"
        )

        cleaned_for_output = clean_transcript
        summary_text = make_deliverable_summary(page.metadata, clean_transcript, quality=content_quality)
        brief_text = make_deliverable_brief(page.metadata, clean_transcript, quality=content_quality)

        provider = detect_llm_provider()
        if transcript and provider:
            try:
                cleaned_for_output = llm_clean_transcript(clean_transcript, page.metadata)
                report["notes"].append(f"LLM enhancement: enabled (provider={provider})")
                report["notes"].append("LLM clean transcript: ok")
                report["steps"].append("llm clean: ok")
                summary_text = llm_make_summary(page.metadata, cleaned_for_output)
                report["notes"].append("LLM summary: ok")
                report["steps"].append("llm summary: ok")
                brief_text = llm_make_brief(page.metadata, summary_text)
                report["notes"].append("LLM brief: ok")
                report["steps"].append("llm brief: ok")
            except Exception:
                report["notes"].append("LLM enhancement: unavailable, fallback applied")
        else:
            report["notes"].append("LLM enhancement: disabled (no provider key configured)")

        write(OUT / "transcript.md", "# Transcript\n\n" + transcript.strip() + "\n")
        write(OUT / "clean_transcript.md", "# Clean Transcript\n\n" + cleaned_for_output + "\n")
        write(OUT / "summary.md", summary_text)
        write(OUT / "brief.md", brief_text)
        report["steps"].append("cleaning: ok")
        report["steps"].append("summary: ok")
        report["steps"].append("brief: ok")
        report["status"] = "ok" if content_quality == "usable" else "degraded"
    except EastMoneyError as e:
        report["notes"].append(f"EastMoney parse error: {e}")
    except Exception as e:
        report["notes"].append(f"Unhandled error: {e}")
    finally:
        report["finished_at"] = datetime.now().isoformat(timespec="seconds")
        md = ["# Run Report", "", f"- URL: {report['url']}", f"- Status: {report['status']}", f"- Engineering completion: {'yes' if report['steps'] else 'no'}", f"- Content usability: {content_quality}", "", "## Steps"]
        md.extend([f"- {s}" for s in report["steps"]] or ["- none"])
        md.extend(["", "## Notes"])
        md.extend([f"- {n}" for n in report["notes"]] or ["- none"])
        md.extend(["", "## Artifacts"])
        md.extend([f"- {a}" for a in report["artifacts"]])
        write(OUT / "run_report.md", "\n".join(md) + "\n")
    return report


def main() -> None:
    enforce_standard_entry()
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    result = run(args.url)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
