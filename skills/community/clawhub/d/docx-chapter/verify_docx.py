#!/usr/bin/env python3
"""
docx-chapter 脚注验证脚本
检查 DOCX 内部 XML，发现重复 URL、遗漏 footnoteRef、字体污染等问题。
规避坑 #4, #5, #6, #7。
"""

import re
import sys
import json
import zipfile
from pathlib import Path
from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

# 含中文标点的正确 URL 正则（坑 #5）
URL_RE = re.compile(r'https?://[^\s<>"」。，；：！？\!\?」』（）、《》【】…—～０-９\[()]+')  # L-5.1

# 不应出现的字体（坑 #7）
# 注：SimSun 不在黑名单中——它是 Pandoc/Word 默认中文脚注基础字体，
# 几乎所有 DOCX 脚注的 ns0:rFonts 都会引用它，误杀率 100%。
# 黑名单只包含"非默认脚注应出现"的字体（仿宋、黑体、楷体等）。
BANNED_FONTS = {"仿宋", "仿宋_GB2312", "黑体", "楷体",
                "FangSong", "FangSong_GB2312", "SimHei", "KaiTi",
                "微软雅黑"}

# 显式字号的豁免 halftone 值——Pandoc 默认给所有 run 设 sz=21（≈10.5pt，五号）
# 这是 Pandoc 的正常输出，不算污染（红队 #5 FP-1）
_DEFAULT_SZ_HALF_PTS = {"21", "18", "20", "22", "24"}
BANNED_FONT_ATTRS = [
    f'{{{NS["w"]}}}ascii',
    f'{{{NS["w"]}}}hAnsi',
    f'{{{NS["w"]}}}eastAsia',
    f'{{{NS["w"]}}}cs',
]


def extract_footnotes(zip_path: str) -> list[dict]:
    """Extract all footnotes from DOCX XML."""
    results = []
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Build relationship ID -> URL map
        rel_url_map = {}
        if 'word/_rels/footnotes.xml.rels' in zf.namelist():
            rels_tree = etree.parse(zf.open('word/_rels/footnotes.xml.rels'))
            rels_root = rels_tree.getroot()
            for rel_elem in rels_root.findall(f'{{{NS["rel"]}}}Relationship'):
                rel_id = rel_elem.get('Id')
                rel_target = rel_elem.get('Target')
                if rel_id and rel_target:
                    rel_url_map[rel_id] = rel_target

        if 'word/footnotes.xml' not in zf.namelist():
            return results

        with zf.open('word/footnotes.xml') as f:
            tree = etree.parse(f)
            root = tree.getroot()
            for fn_elem in root.findall('.//w:footnote', NS):
                fn_id = fn_elem.get(f'{{{NS["w"]}}}id')
                fn_type = fn_elem.get(f'{{{NS["w"]}}}type', '')
                if fn_id in ('0', '-1') or fn_type in ('separator', 'continuationSeparator', 'continuationNotice'):
                    continue  # structural footnotes, not content

                result = {
                    "id": fn_id,
                    "urls_in_body": [],
                    "urls_in_hyperlink": [],
                    "has_footnoteRef": False,
                    "font_issues": [],
                    "raw_text": "",
                    "hyperlinks_no_style": [],
                }

                # Check for footnoteRef (坑 #6)
                ref_elems = fn_elem.findall('.//w:footnoteRef', NS)
                result["has_footnoteRef"] = len(ref_elems) > 0

                # Extract text from <w:t> elements
                texts = []
                for t_elem in fn_elem.iter(f'{{{NS["w"]}}}t'):
                    if t_elem.text:
                        texts.append(t_elem.text)
                result["raw_text"] = "".join(texts)

                # Extract URLs from body text (坑 #4) — exclude <w:t> inside <w:hyperlink>
                for t_elem in fn_elem.iter(f'{{{NS["w"]}}}t'):
                    if t_elem.text:
                        # Check if this <w:t> is inside a <w:hyperlink>
                        parent_r = t_elem.getparent()
                        is_inside_hl = (parent_r is not None
                                        and parent_r.tag == f'{{{NS["w"]}}}r'
                                        and parent_r.getparent() is not None
                                        and parent_r.getparent().tag == f'{{{NS["w"]}}}hyperlink')
                        if is_inside_hl:
                            continue
                        result["urls_in_body"].extend(URL_RE.findall(t_elem.text))

                # Extract URLs from hyperlink targets (r:id → relationship target only;
                # w:history is a boolean flag, not a URL — see 坑 C-2.2 / M-5.2)
                for hl_elem in fn_elem.iter(f'{{{NS["w"]}}}hyperlink'):
                    # w:history is a boolean flag — skip entirely
                    if hl_elem.get(f'{{{NS["w"]}}}history') is not None:
                        continue
                    rid_attr = hl_elem.get(f'{{{NS["r"]}}}id')
                    if rid_attr and rid_attr in rel_url_map:
                        result["urls_in_hyperlink"].append(rel_url_map[rid_attr])
                    elif not rid_attr:
                        print(f"Warning: hyperlink without r:id in footnote {fn_id}", file=sys.stderr)

                    # Check if inner <w:r> has <w:rStyle w:val="Hyperlink"/> for blue underline
                    hl_runs = hl_elem.findall(f'w:r', NS)
                    for hl_run in hl_runs:
                        hl_rPr = hl_run.find(f'w:rPr', NS)
                        hl_has_style = False
                        if hl_rPr is not None:
                            for style_elem in hl_rPr.findall(f'w:rStyle', NS):
                                if style_elem.get(f'{{{NS["w"]}}}val') == 'Hyperlink':
                                    hl_has_style = True
                        if not hl_has_style:
                            result["hyperlinks_no_style"].append(rid_attr if rid_attr else "(no r:id)")

                # Check fonts in <w:rFonts> (坑 #7)
                for rFonts_elem in fn_elem.iter(f'{{{NS["w"]}}}rFonts'):
                    for attr_key in BANNED_FONT_ATTRS:
                        val = rFonts_elem.get(attr_key)
                        if val and val.strip() in BANNED_FONTS:
                            result["font_issues"].append(f"Banned font '{val}' in {attr_key.split('}')[1]}")

                for sz_elem in fn_elem.iter(f'{{{NS["w"]}}}sz'):
                    sz_val = sz_elem.get(f'{{{NS["w"]}}}val')
                    if sz_val and sz_val not in _DEFAULT_SZ_HALF_PTS:
                        result["font_issues"].append(
                            f"Non-default font size sz={sz_val} (half-pts) — Pandoc default 21=五号 tolerated"
                        )

                results.append(result)

    return results


def check_url_duplication(footnotes: list[dict]) -> list[dict]:
    """Check for duplicate URLs in body text vs hyperlink (坑 #4)."""
    issues = []
    for fn in footnotes:
        body_set = {u.rstrip('/') for u in fn["urls_in_body"]}
        hl_set = {u.rstrip('/') for u in fn["urls_in_hyperlink"]}
        duplicates = body_set & hl_set
        if duplicates:
            issues.append({
                "type": "url_duplication",
                "footnote": fn["id"],
                "severity": "error",
                "urls": list(duplicates),
                "detail": "Same URL in <w:t> and <w:hyperlink> — 应删掉其中一个",
            })
    return issues


def check_url_no_hyperlink(footnotes: list[dict]) -> list[dict]:
    """Check for URLs in footnote body that are NOT hyperlinked (补漏)."""
    issues = []
    for fn in footnotes:
        body_set = {u.rstrip('/') for u in fn["urls_in_body"]}
        hl_set = {u.rstrip('/') for u in fn["urls_in_hyperlink"]}
        missing = body_set - hl_set
        if missing:
            issues.append({
                "type": "url_no_hyperlink",
                "footnote": fn["id"],
                "severity": "error",
                "urls": list(missing),
                "detail": "URLs in body but not wrapped in <w:hyperlink> — 在 Word 中不可点击",
            })
    return issues


def check_missing_footnoteRef(footnotes: list[dict]) -> list[dict]:
    """Check for missing footnoteRef (坑 #6)."""
    issues = []
    for fn in footnotes:
        if not fn["has_footnoteRef"]:
            issues.append({
                "type": "missing_footnoteRef",
                "footnote": fn["id"],
                "severity": "error",
                "detail": "Missing <w:footnoteRef /> — page number won't display",
            })
    return issues


def check_font_issues(footnotes: list[dict]) -> list[dict]:
    """Check for banned fonts/sizes (坑 #7)."""
    issues = []
    for fn in footnotes:
        for fi in fn["font_issues"]:
            issues.append({
                "type": "font_issue",
                "footnote": fn["id"],
                "severity": "warning",
                "detail": fi,
            })
    return issues


def check_hyperlink_style(footnotes: list[dict]) -> list[dict]:
    """Check hyperlinks have w:rStyle="Hyperlink" for blue underline visual."""
    issues = []
    for fn in footnotes:
        for rid in fn.get("hyperlinks_no_style", []):
            issues.append({
                "type": "hyperlink_no_style",
                "footnote": fn["id"],
                "severity": "warning",
                "detail": f"Hyperlink {rid} missing rStyle='Hyperlink' — URL 可点击但无蓝色下划线",
            })
    return issues


def check_footnote_continuity(footnotes: list[dict]) -> list[dict]:
    """Check for gaps in footnote numbering (H-7.1)."""
    issues = []
    ids = []
    for fn in footnotes:
        try:
            ids.append(int(fn["id"]))
        except (ValueError, TypeError):
            pass
    if len(ids) < 2:
        return issues
    ids.sort()
    for i in range(len(ids) - 1):
        gap = ids[i+1] - ids[i]
        if gap > 1:
            missing = list(range(ids[i]+1, ids[i+1]))
            issues.append({
                "type": "footnote_gap",
                "footnote": str(ids[i]),
                "severity": "warning",
                "detail": f"Footnote IDs jump from {ids[i]} to {ids[i+1]} (missing: {missing})",
            })
    return issues


def load_url_status(docx_dir: str):
    """Load url_status.json from DOCX directory if exists (array of curl output strings)."""
    status_path = Path(docx_dir) / "url_status.json"
    if not status_path.exists():
        return None
    with open(status_path) as f:
        return json.load(f)


def parse_http_status(curl_output: str):
    """Parse HTTP status code from curl output like 'HTTP/2 200' or 'HTTP/1.1 404 Not Found'."""
    match = re.search(r'HTTP/[\d.]+\s+(\d+)', curl_output)
    if match:
        return match.group(1)
    return None


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: verify_docx.py <path/to/file.docx>"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    docx_path = sys.argv[1]
    if not Path(docx_path).exists():
        print(json.dumps({"error": f"File not found: {docx_path}"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    footnotes = extract_footnotes(docx_path)
    issues = []
    issues.extend(check_url_duplication(footnotes))
    issues.extend(check_url_no_hyperlink(footnotes))
    issues.extend(check_missing_footnoteRef(footnotes))
    issues.extend(check_font_issues(footnotes))
    issues.extend(check_hyperlink_style(footnotes))
    issues.extend(check_footnote_continuity(footnotes))

    # URL reachability markers (merge url_status.json if exists)
    url_status_data = load_url_status(str(Path(docx_path).parent))
    url_status_map: dict[str, str] = {}
    if url_status_data is not None:
        for i, fn in enumerate(footnotes):
            if i < len(url_status_data):
                raw = url_status_data[i]
                if isinstance(raw, str) and raw.strip():
                    code = parse_http_status(raw)
                    if code:
                        url_status_map[fn["id"]] = code

    # Annotate URL-related issues with reachability info
    for issue in issues:
        if issue["type"] in ("url_no_hyperlink", "url_duplication") and issue["footnote"] in url_status_map:
            issue["reachability"] = url_status_map[issue["footnote"]]

    result = {
        "file": docx_path,
        "total_footnotes": len(footnotes),
        "structured_issues": sorted(issues, key=lambda x: (x["severity"], int(x["footnote"]))),
        "footnote_details": [
            {
                "id": fn["id"],
                "has_footnoteRef": fn["has_footnoteRef"],
                "urls_in_body": fn["urls_in_body"],
                "urls_in_hyperlink": fn["urls_in_hyperlink"],
                "font_issues": fn["font_issues"],
                "hyperlinks_no_style": fn["hyperlinks_no_style"],
                "reachability": url_status_map.get(fn["id"]),
            }
            for fn in footnotes
        ],
    }

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
