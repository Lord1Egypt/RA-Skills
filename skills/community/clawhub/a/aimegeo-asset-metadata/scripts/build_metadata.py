#!/usr/bin/env python3
"""Validate agent-authored media notes and assemble a local metadata handoff.

Standard library only. Never opens media, fetches URLs, renames originals, or
invents descriptive prose. Public functions are also used by the self-test.
"""

import argparse
import json
import math
import re
import sys
import unicodedata
from datetime import date, datetime
from decimal import Decimal, localcontext
from pathlib import Path
from urllib.parse import urlsplit


EXTENSIONS = {
    "image": {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif",
              ".heic", ".heif", ".tif", ".tiff", ".bmp", ".ico"},
    "video": {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi", ".mpeg",
              ".mpg", ".3gp", ".m2ts", ".ts", ".ogv"},
    "audio": {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".oga",
              ".opus", ".aiff", ".aif", ".wma", ".m4b"},
}
COMMON = {"id", "type", "original_filename", "filename_stem", "title",
          "caption", "evidence", "content_url", "page_url"}
TIMED = {"description", "duration_seconds", "upload_date", "chapters"}
FIELDS = {
    "image": COMMON | {"decorative", "alt"},
    "video": COMMON | TIMED | {"thumbnail_url", "subtitles"},
    "audio": COMMON | TIMED | {"transcript"},
}
GAP_LABELS = {
    "evidence": "素材查看结果或用户说明", "title": "标题",
    "content_url": "媒体公开地址", "caption": "图注或简短说明",
    "alt": "信息图片的替代文本", "description": "视频或音频简介",
    "duration_seconds": "已确认时长", "upload_date": "实际上传日期",
    "thumbnail_url": "已确认的封面地址", "subtitles": "字幕文件或不适用说明",
    "chapters": "带时间点的章节", "transcript": "文字稿或不适用说明",
}


class InputError(ValueError):
    """An actionable input error, safe to display without a traceback."""


def check(condition, message):
    if not condition:
        raise InputError(message)


def fields(value, allowed, where):
    check(isinstance(value, dict), f"{where}: expected an object")
    extra = value.keys() - allowed
    check(not extra, f"{where}: unsupported fields: {', '.join(sorted(extra))}")


def string(value, where, required=False):
    if value is None:
        check(not required, f"{where}: required non-empty string")
        return None
    check(isinstance(value, str), f"{where}: expected string or null")
    check(not any(unicodedata.category(c) == "Cc" and c not in "\n\t" for c in value),
          f"{where}: control characters are not allowed")
    value = value.strip()
    check(not required or bool(value), f"{where}: required non-empty string")
    return value or None


def number(value, where, positive=False):
    try:
        finite = isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
    except OverflowError:
        finite = False
    check(finite, f"{where}: expected finite number")
    check(value > 0 if positive else value >= 0,
          f"{where}: must be {'positive' if positive else 'non-negative'}")
    return value


def public_url(value, where):
    value = string(value, where)
    if value is None:
        return None
    try:
        parts = urlsplit(value)
        hostname = parts.hostname
        # urlsplit defers port validation until this property is read.
        # A malformed/out-of-range port is not a usable HTTP(S) address.
        _ = parts.port
    except ValueError as exc:
        raise InputError(f"{where}: invalid URL") from exc
    check(parts.scheme in {"http", "https"} and bool(hostname)
          and parts.username is None and parts.password is None
          and not any(c.isspace() for c in value),
          f"{where}: expected HTTP(S) URL without embedded credentials")
    return value


def upload_date(value, where):
    value = string(value, where)
    if value is None:
        return None
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            date.fromisoformat(value)
        else:
            match = re.fullmatch(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?"
                r"(?:Z|[+-](?P<offset_hours>\d{2}):(?P<offset_minutes>\d{2}))", value)
            check(match is not None, f"{where}: expected ISO date or timezone-qualified datetime")
            if match["offset_hours"] is not None:
                # fromisoformat() normalizes overflowing offset minutes.
                check(int(match["offset_hours"]) < 24 and int(match["offset_minutes"]) < 60,
                      f"{where}: timezone offset hours must be 00-23 and minutes 00-59")
            datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        if isinstance(exc, InputError):
            raise
        raise InputError(f"{where}: invalid calendar date or time") from exc
    return value


def iso_duration(seconds):
    total = Decimal(str(seconds))
    # Decimal's default precision can reject a finite duration's large integer
    # quotient. Size local precision to its digits instead of limiting duration.
    with localcontext() as context:
        context.prec = max(context.prec, len(total.as_tuple().digits), total.adjusted() + 1)
        hours, rest = divmod(total, Decimal(3600))
        minutes, secs = divmod(rest, Decimal(60))
    result = "PT"
    if hours:
        result += f"{int(hours)}H"
    if minutes:
        result += f"{int(minutes)}M"
    if secs or result == "PT":
        seconds_text = format(secs, "f")
        if "." in seconds_text:
            seconds_text = seconds_text.rstrip("0").rstrip(".")
        result += seconds_text + "S"
    return result


def safe_stem(value):
    value = unicodedata.normalize("NFC", value)
    chars = [c if unicodedata.category(c)[0] in {"L", "N", "M"}
             or c in "-_" else "-" for c in value]
    stem = re.sub(r"-+", "-", "".join(chars)).strip("-_")
    check(any(unicodedata.category(c)[0] in {"L", "N"} for c in stem),
          "filename_stem: needs at least one letter or number")
    # 120 UTF-8 bytes leaves room for collision suffixes and the original suffix.
    stem = stem.encode("utf-8")[:120].decode("utf-8", errors="ignore").rstrip("-_")
    if re.fullmatch(r"(?i:con|prn|aux|nul|com[1-9]|lpt[1-9])", stem):
        stem = "asset-" + stem
    return stem


def attachment(value, where):
    if value is None:
        return {"status": "missing", "reference": None, "reason": None}
    fields(value, {"status", "reference", "reason"}, where)
    status = value.get("status")
    check(isinstance(status, str) and status in {"provided", "missing", "not_applicable"},
          f"{where}.status: expected provided, missing or not_applicable")
    reference = string(value.get("reference"), where + ".reference")
    reason = string(value.get("reason"), where + ".reason")
    check(status != "provided" or bool(reference), f"{where}: provided needs reference")
    check(status == "provided" or reference is None,
          f"{where}: reference allowed only with provided status")
    check(status != "not_applicable" or bool(reason),
          f"{where}: not_applicable needs reason")
    return {"status": status, "reference": reference, "reason": reason}


def evidence_record(value, where):
    fields(value, {"kind", "scope", "reference", "details"}, where)
    kind, scope = value.get("kind"), value.get("scope")
    check(isinstance(kind, str) and kind in {"reviewed", "user_description", "unavailable"},
          f"{where}.kind: expected reviewed, user_description or unavailable")
    check(isinstance(scope, str) and scope in {"full", "excerpt", "none"},
          f"{where}.scope: expected full, excerpt or none")
    reference = string(value.get("reference"), where + ".reference", required=True)
    details = string(value.get("details"), where + ".details")
    if kind == "unavailable":
        check(scope == "none" and details is None,
              f"{where}: unavailable needs scope none and no content details")
    else:
        check(scope != "none" and bool(details),
              f"{where}: available evidence needs scope full/excerpt and details")
    return {"kind": kind, "scope": scope, "reference": reference, "details": details}


def schema_for(asset):
    kind = asset["type"]
    if kind == "image" and asset["decorative"]:
        return {"status": "not_applicable", "jsonld": None, "missing_fields": []}
    node = {"@context": "https://schema.org", "@type": {
        "image": "ImageObject", "video": "VideoObject", "audio": "AudioObject"}[kind]}
    mapping = {"name": asset["title"], "contentUrl": asset["content_url"]}
    mapping["description"] = (asset["caption"] or asset["alt"]) if kind == "image" else asset["description"]
    expected = ["name", "description", "contentUrl"]
    if kind != "image":
        mapping["uploadDate"] = asset["upload_date"]
        mapping["duration"] = asset["duration_iso8601"]
        expected += ["uploadDate", "duration"]
        if kind == "video":
            mapping["thumbnailUrl"] = asset["thumbnail_url"]
            expected.append("thumbnailUrl")
    node.update({key: value for key, value in mapping.items() if value is not None})
    if asset["page_url"]:
        node["isPartOf"] = {"@id": asset["page_url"]}
    if kind != "image" and asset["chapters"]:
        node["hasPart"] = [{"@type": "Clip", "name": c["title"],
                            "startOffset": c["start_seconds"]} for c in asset["chapters"]]
    missing = [key for key in expected if key not in node]
    return {"status": "partial" if missing else "fields_present",
            "jsonld": node, "missing_fields": missing}


def normalize_asset(raw, index, used_names):
    where = f"assets[{index}]"
    check(isinstance(raw, dict), f"{where}: expected object")
    kind = raw.get("type")
    check(isinstance(kind, str) and kind in FIELDS, f"{where}.type: expected image, video or audio")
    fields(raw, FIELDS[kind], where)
    asset_id = string(raw.get("id"), where + ".id", required=True)
    original = string(raw.get("original_filename"), where + ".original_filename", required=True)
    check(not any(c in original for c in "/\\\n\t") and original == raw["original_filename"],
          f"{where}.original_filename: expected basename, not path or padded name")
    suffix = Path(original).suffix
    check(suffix.lower() in EXTENSIONS[kind],
          f"{where}.original_filename: extension does not match {kind} or is unsupported")
    stem_input = string(raw.get("filename_stem"), where + ".filename_stem") or original[:-len(suffix)]
    stem = safe_stem(stem_input)
    filename, counter = stem + suffix, 2
    while unicodedata.normalize("NFC", filename).casefold() in used_names:
        filename = f"{stem}-{counter}{suffix}"
        counter += 1
    used_names.add(unicodedata.normalize("NFC", filename).casefold())
    evidence = evidence_record(raw.get("evidence"), where + ".evidence")
    title = string(raw.get("title"), where + ".title")
    caption = string(raw.get("caption"), where + ".caption")
    description = string(raw.get("description"), where + ".description") if kind != "image" else None
    decorative = raw.get("decorative", False)
    check(isinstance(decorative, bool), f"{where}.decorative: expected boolean")
    alt = string(raw.get("alt"), where + ".alt") if kind == "image" else None
    if kind == "image":
        if decorative:
            check(alt is None, f"{where}.alt: decorative image requires empty alt")
            alt = ""
        elif raw.get("alt") is not None:
            check(bool(alt), f"{where}.alt: empty alt requires decorative true")
    if evidence["kind"] == "unavailable":
        check(not caption and not description and not alt,
              f"{where}: unavailable evidence cannot support alt, caption or description")
    asset = {"id": asset_id, "type": kind, "original_filename": original,
             "suggested_filename": filename, "title": title, "evidence": evidence,
             "caption": caption, "content_url": public_url(raw.get("content_url"), where + ".content_url"),
             "page_url": public_url(raw.get("page_url"), where + ".page_url")}
    gaps = [key for key in ("title", "content_url", "caption") if asset[key] is None]
    if evidence["kind"] == "unavailable":
        gaps.insert(0, "evidence")
    if kind == "image":
        asset.update({"decorative": decorative, "alt": alt})
        if decorative:
            gaps = [key for key in gaps if key not in {"title", "content_url", "caption", "evidence"}]
        elif alt is None:
            gaps.append("alt")
    else:
        duration = raw.get("duration_seconds")
        if duration is not None:
            number(duration, where + ".duration_seconds", positive=True)
        chapters = raw.get("chapters")
        check(chapters is None or isinstance(chapters, list), f"{where}.chapters: expected array or null")
        normalized_chapters, previous = [], -1
        for ci, chapter in enumerate(chapters or []):
            cw = f"{where}.chapters[{ci}]"
            fields(chapter, {"start_seconds", "title"}, cw)
            start = number(chapter.get("start_seconds"), cw + ".start_seconds")
            check(start > previous, f"{cw}: starts must be strictly increasing")
            check(duration is None or start < duration, f"{cw}: start must be before duration")
            normalized_chapters.append({"start_seconds": start,
                                        "title": string(chapter.get("title"), cw + ".title", required=True)})
            previous = start
        asset.update({"description": description, "duration_seconds": duration,
                      "duration_iso8601": iso_duration(duration) if duration is not None else None,
                      "upload_date": upload_date(raw.get("upload_date"), where + ".upload_date"),
                      "chapters": normalized_chapters or None})
        gaps += [key for key in ("description", "duration_seconds", "upload_date") if asset[key] is None]
        att_key = "subtitles" if kind == "video" else "transcript"
        asset[att_key] = attachment(raw.get(att_key), where + "." + att_key)
        if asset[att_key]["status"] == "missing":
            gaps.append(att_key)
        if kind == "video":
            asset["thumbnail_url"] = public_url(raw.get("thumbnail_url"), where + ".thumbnail_url")
            if asset["thumbnail_url"] is None:
                gaps.append("thumbnail_url")
            if asset["chapters"] is None:
                gaps.append("chapters")
    asset["gaps"] = gaps
    asset["status"] = "needs_information" if gaps else "ready_for_review"
    asset["schema"] = schema_for(asset)
    return asset


def build(document):
    fields(document, {"assets"}, "input")
    raw_assets = document.get("assets")
    check(isinstance(raw_assets, list) and bool(raw_assets), "input.assets: expected non-empty array")
    assets, used_names, ids = [], set(), set()
    for i, raw in enumerate(raw_assets):
        asset = normalize_asset(raw, i, used_names)
        check(asset["id"] not in ids, f"assets[{i}].id: duplicate id")
        ids.add(asset["id"])
        assets.append(asset)
    return {
        "schema_version": "1.0",
        "provenance_note": "文本由调用方撰写；证据类型照录。时长、日期、地址及附件均为输入值，脚本未探测媒体或验证附件。",
        "schema_note": "JSON-LD仅含已提供字段；fields_present只表示本工具列出的交接字段齐全，不表示搜索资格、收录或引用。",
        "summary": {"total": len(assets),
                    "by_type": {kind: sum(a["type"] == kind for a in assets) for kind in EXTENSIONS},
                    "needs_information": sum(bool(a["gaps"]) for a in assets),
                    "by_evidence": {kind: sum(a["evidence"]["kind"] == kind for a in assets)
                                    for kind in ("reviewed", "user_description", "unavailable")}},
        "assets": assets,
    }


def handoff(result):
    # Render existing notes and concrete gaps, without authoring media descriptions.
    def literal(value):
        return json.dumps(value, ensure_ascii=False)

    lines = ["# 图注与字幕交接清单", "", result["provenance_note"], "", result["schema_note"], ""]
    for asset in result["assets"]:
        lines += [f"## {literal(asset['id'])}", "",
                  f"- 类型：{asset['type']}",
                  f"- 原文件：{literal(asset['original_filename'])}",
                  f"- 文件名建议：{literal(asset['suggested_filename'])}（仅建议，未重命名）",
                  f"- 标题：{literal(asset['title'])}",
                  f"- 内容依据：{literal(asset['evidence'])}",
                  f"- 图注或简短说明：{literal(asset['caption'])}"]
        if asset["type"] == "image":
            lines += [f"- alt：{literal(asset['alt'])}；装饰图：{literal(asset['decorative'])}"]
        else:
            key = "subtitles" if asset["type"] == "video" else "transcript"
            lines += [f"- 简介：{literal(asset['description'])}",
                      f"- 时长：{literal(asset['duration_seconds'])} 秒；ISO 8601：{literal(asset['duration_iso8601'])}",
                      f"- 上传日期：{literal(asset['upload_date'])}",
                      f"- {'字幕' if key == 'subtitles' else '文字稿'}：{literal(asset[key])}",
                      f"- 章节：{literal(asset['chapters'])}"]
            if asset["type"] == "video":
                lines.append(f"- 封面：{literal(asset['thumbnail_url'])}")
        lines += [f"- 结构化资料：{asset['schema']['status']}；待补字段：{literal(asset['schema']['missing_fields'])}",
                  "- 待补：" + ("、".join(GAP_LABELS[key] for key in asset["gaps"]) or "无；交付前复核内容与附件"), ""]
    lines += ["null 表示未提供或未确认；空 alt 仅供装饰图。附件 provided 表示已提供引用，未验证文件内容。", ""]
    return "\n".join(lines)


def read_document(path):
    def reject_constant(value):
        raise InputError(f"JSON: non-finite constant {value} is not allowed")

    def unique_object(pairs):
        obj = {}
        for key, value in pairs:
            check(key not in obj, f"JSON: duplicate key {key}")
            obj[key] = value
        return obj

    return json.loads(Path(path).read_text(encoding="utf-8"),
                      parse_constant=reject_constant, object_pairs_hook=unique_object)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 JSON with agent-authored notes")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for the two handoff files")
    args = parser.parse_args(argv)
    try:
        result = build(read_document(args.input))
        rendered = handoff(result)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "媒体元信息.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        (args.output_dir / "图注与字幕交接清单.md").write_text(rendered, encoding="utf-8")
    except (InputError, OSError, ValueError, OverflowError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
