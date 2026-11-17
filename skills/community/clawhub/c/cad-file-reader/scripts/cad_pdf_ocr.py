#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad_pdf_ocr.py — PDF 图纸识图候选（本机 PDF 分流 + 本地 OCR）。

输入边界：PDF（矢量 / 扫描 / 混合）。
能力边界：只输出识图**文字候选**；扫描件 OCR 无矢量几何、无图层，全部进
review_candidates 并标 missing_layer/missing_unit/non_measurement。输出
图签栏元数据候选（title_block，仅作跨格式元数据锚点，需人工核对）。不输出
工程量、材料量、造价或结算量（final_quantity=false）。

做法：
  1. 用 pdf-inspector 的 pdf_route.py --no-ocr 分类（text/scanned/mixed）。
  2. 文本页：取 pdf-inspector 原生文字当候选（bbox=null）。
  3. 扫描/混合页：pdftoppm 渲染后调用本机 image-ocr --json，取行级文字与像素框。
  4. 记录 source_format（pdf_vector/pdf_raster/pdf_hybrid）与候选 page_index/page_bbox。
  5. 图签栏规则版：关键词匹配出字段候选，写入 pdf_meta.title_block。
  6. 两级缓存：文件级缓存 pdf 元数据，页面级缓存 OCR 行结果，避免整图重解析。
  7. 扫描页用线程池并行渲染+OCR（默认≤3 并发），逐页隔离 workdir。
  8. 全部候选按 cad-file-reader/v0 契约写出，可用 scripts/cad_validate.sh 校验。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from platform_paths import find_tool, normalize_platform

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent

_home_default = Path.home() / ".codex"


def _default_pdf_venv_python() -> str:
    """pdf-inspector 技能 venv Python 的跨平台默认路径。"""
    base = _home_default / "skills" / "pdf-inspector" / ".venv"
    if normalize_platform() == "win":
        return str(base / "Scripts" / "python.exe")
    return str(base / "bin" / "python")


PDF_INSPECTOR_VENV = Path(
    os.environ.get("PDF_INSPECTOR_VENV")
    or find_tool("pdf-inspector-python")
    or _default_pdf_venv_python()
)
_pdf_inspector_dir = PDF_INSPECTOR_VENV.parent.parent.parent
PDF_ROUTE = Path(
    os.environ.get("PDF_INSPECTOR_ROUTE")
    or str(_pdf_inspector_dir / "scripts" / "pdf_route.py")
)
PDETOPPM = find_tool("pdftoppm") or str(
    _home_default / ".." / ".cache" / "codex-runtimes"
    / "codex-primary-runtime" / "dependencies" / "bin" / "override" / "pdftoppm"
)
OCR_IMAGE = Path(
    os.environ.get("OCR_IMAGE")
    or find_tool("ocr_image")
    or str(_home_default / "bin" / "ocr_image")
)
# 工程图纸以中文图签/图名为主，本地 OCR 必须锁定中文语言包，禁止 auto-lang
# 自动切换到 eng（蓝图稀疏中文会被误判为英文导致召回坍缩，实测 degraded）。
OCR_LANG = os.environ.get("CAD_OCR_LANG", "chi_sim").strip() or "chi_sim"
OCR_FORCE_LANG = os.environ.get("CAD_OCR_FORCE_LANG", "1") not in ("0", "false", "no")
PDF_VEC_SCRIPT = Path(__file__).resolve().parent / "cad_pdf_vec.py"

SOURCE_SCHEMA = "cad-file-reader/v0"
REVIEW_REASONS = [
    "missing_scale", "missing_unit", "missing_layer", "missing_block_definition",
    "ambiguous_text_binding", "geometry_conflict", "duplicate_candidate",
    "outside_viewport", "incomplete_geometry", "low_confidence_inference",
]
MAX_REVIEW_PAGES_PER_PDF = 20          # 每份 PDF 最多写多少张复核截图，避免刷屏
LOW_CONF_LINE = 0.40                  # 单行 OCR 低置信阈值
LOW_CONF_PAGE_AVG = 0.60              # 整页 OCR 平均置信阈值
SOURCE_FORMAT_MAP = {
    "text_based": "pdf_vector",
    "scanned": "pdf_raster",
    "image_based": "pdf_raster",
    "mixed": "pdf_hybrid",
}

# 图签栏字段关键词（规则版，中文为主，兼顾英文缩写）

# 专业视角关键词（PDF 文本候选 -> discipline_view_tags，仅作下游筛选提示）
DISCIPLINE_KEYWORDS = {
    "electrical": ["电气", "照明", "动力", "配电", "插座", "开关", "电缆", "桥架", "弱电", "智能化", "防雷"],
    "fire_protection": ["消防", "火警", "喷淋", "消火栓", "防火"],
    "hvac_plumbing": ["给排水", "给水", "排水", "雨水", "空调", "通风", "暖通", "喷淋"],
    "structural": ["结构", "混凝土", "梁", "柱", "板", "钢筋", "基础", "楼梯"],
    "architectural": ["建筑", "门窗", "楼地面", "墙面", "吊顶", "幕墙"],
    "site": ["总图", "场地", "道路", "标高", "坐标"],
}


def _infer_discipline_tags(text: str) -> list[str]:
    """从文本关键词推断专业视角标签；无命中返回空列表，仅供下游筛选提示。"""
    text = str(text or "")
    hits: list[str] = []
    for discipline, keywords in DISCIPLINE_KEYWORDS.items():
        if any(k in text for k in keywords):
            hits.append(discipline)
    return hits


TITLE_BLOCK_KEYS = [
    (r"项目(?:名称)?", "project"),
    (r"工程(?:名称)?", "project"),
    (r"图名", "drawing_name"),
    (r"图号", "drawing_no"),
    (r"图别|专业", "discipline"),
    (r"比例", "scale"),
    (r"日期", "date"),
    (r"设计", "designer"),
    (r"审核", "reviewer"),
    (r"制图|绘图", "draftsperson"),
    (r"校对", "proofreader"),
    (r"备注", "remark"),
    (r"SCALE", "scale"),
    (r"DRAWING\s*NO", "drawing_no"),
    (r"DESIGN", "designer"),
    (r"APPROVED", "reviewer"),
    (r"REV", "revision"),
]


def _sysrun(args: list[str], timeout: int = 300) -> tuple[int, str, str]:
    proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


def _file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(pdf: Path, out_dir: Path, cache_dir: Path, force: bool) -> dict:
    digest = _file_hash(pdf)
    entry_file = cache_dir / f"{digest}.meta.json"
    if not force and entry_file.exists():
        try:
            return json.loads(entry_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    rc, out, err = _sysrun([
        sys.executable, str(PDF_ROUTE), str(pdf),
        "--output-dir", str(out_dir), "--no-ocr",
    ])
    if rc != 0:
        raise RuntimeError(f"pdf_route 分类失败: {err.strip() or out.strip()}")
    try:
        report = json.loads(out)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"pdf_route 输出不是 JSON: {exc}") from exc
    files = report.get("files") or []
    entry = files[0] if files else {"error": "no file entry"}
    if entry.get("error"):
        raise RuntimeError(entry["error"])
    entry["_source_hash"] = digest
    cache_dir.mkdir(parents=True, exist_ok=True)
    entry_file.write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
    return entry


def render_pdf_page(pdf: Path, page: int, workdir: Path) -> Path:
    prefix = workdir / f"page-{page}"
    rc, out, err = _sysrun(
        [PDETOPPM, "-png", "-r", "200", "-f", str(page), "-l", str(page), str(pdf), str(prefix)],
        timeout=180,
    )
    if rc != 0:
        raise RuntimeError(f"pdftoppm 渲染第 {page} 页失败: {err.strip() or out.strip()}")
    images = sorted(workdir.glob(f"page-{page}-*.png"))
    if not images:
        raise RuntimeError(f"第 {page} 页渲染无 PNG")
    return images[0]


def ocr_lines(image: Path) -> list[dict]:
    ocr_args = [str(OCR_IMAGE), "--json"]
    if OCR_FORCE_LANG:
        ocr_args += ["--lang", OCR_LANG, "--no-auto-lang"]
    ocr_args.append(str(image))
    rc, out, err = _sysrun(ocr_args, timeout=240)
    if rc != 0:
        raise RuntimeError(f"image-ocr 失败: {err.strip() or out.strip()}")
    try:
        data = json.loads(out)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"image-ocr 输出不是 JSON: {exc}") from exc
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("lines"), list):
        return data["lines"]
    if isinstance(data, dict) and isinstance(data.get("pages"), list):
        out_lines: list[dict] = []
        for page in data["pages"]:
            out_lines.extend(page.get("lines") or [])
        return out_lines
    raise RuntimeError("image-ocr 输出结构无法识别")


def ocr_page_cached(pdf: Path, page: int, cache_dir: Path, force: bool, digest: str) -> tuple[list[dict], dict | None]:
    page_cache = cache_dir / f"{digest}-page-{page}.ocr.json"
    if not force and page_cache.exists():
        try:
            data = json.loads(page_cache.read_text(encoding="utf-8"))
            if data.get("page") == page:
                return data.get("lines") or [], {"cache_hit": True}
        except (json.JSONDecodeError, OSError):
            pass
    with tempfile.TemporaryDirectory(prefix="cad-pdf-page-") as tmp:
        image = render_pdf_page(pdf, page, Path(tmp))
        lines = ocr_lines(image)
    payload = {"page": page, "lines": lines}
    cache_dir.mkdir(parents=True, exist_ok=True)
    page_cache.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return lines, {"cache_hit": False}


def _review_image_name(pdf: Path, page: int) -> str:
    stem = re.sub(r"[^A-Za-z0-9_\u4e00-\u9fff-]+", "_", pdf.stem).strip("_. ") or pdf.name
    return f"{stem}-p{page}.png"


def page_review_image(pdf: Path, page: int, review_dir: Path) -> Path | None:
    """把指定页渲染成 PNG 并保留到 review_dir；失败返回 None（不阻断主流程）。"""
    try:
        review_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="cad-pdf-review-") as tmp:
            img = render_pdf_page(pdf, page, Path(tmp))
            dest = review_dir / _review_image_name(pdf, page)
            shutil.copy2(img, dest)
            return dest
    except Exception:  # noqa: BLE001
        return None


def _mark_up_to(record: dict, cands: list[dict]) -> None:
    """给一批同页候选批量挂上 review_image，提示去 _review 看原图。"""
    img = record.get("image") if record else None
    if not img:
        return
    for cand in cands:
        cand["review_image"] = img


def stable_id(source: str, kind: str, page: int, text: str, idx: int) -> str:
    payload = f"{source}|{kind}|{page}|{text}|{idx}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def make_candidate(
    kind: str,
    text: str,
    evidence: list[dict],
    method: str,
    source: str,
    page: int,
    bbox: list[float] | None,
    confidence: float,
    idx: int,
    review_reasons: list[str],
    review_notes: str,
    source_format: str,
) -> dict:
    tags = _infer_discipline_tags(text)
    discipline_refs: list[dict] = [{"discipline": "all", "note": "PDF 识图/文字候选，需人工核对后可作提示输入"}]
    if tags:
        discipline_refs.extend({"discipline": t, "note": "PDF 文本关键词推断的专业视角"} for t in tags)
    cand = {
        "id": stable_id(source, kind, page, text, idx),
        "kind": kind,
        "value": None,
        "unit": None,
        "layer": None,
        "block_name": None,
        "text": text[:240],
        "bbox": bbox,
        "page_index": page,
        "page_bbox": bbox,
        "evidence": evidence,
        "source_format": source_format,
        "method": method,
        "confidence": round(max(0.0, min(1.0, confidence)), 4),
        "confidence_tier": "review_required",
        "review_reasons": review_reasons,
        "review_notes": review_notes,
        "source_schema": SOURCE_SCHEMA,
        "source_id": source,
        "final_quantity": False,
        "rotation": None,
        "discipline_refs": discipline_refs,
        "discipline_view_tags": tags,
        "confidence_scores": {"ocr_confidence": round(max(0.0, min(1.0, confidence)), 4)},
    }
    return cand


def _append_best_candidate(target: dict, key: str, value: str, page: int, bbox: list[float] | None, confidence: float) -> None:
    """图签栏字段候选：同一 key 只保留置信度最高的一条，不重复堆积。"""
    if not value:
        return
    current = target.get(key)
    if current is None or float(current.get("confidence", 0.0)) < confidence:
        target[key] = {
            "key": key,
            "value": value[:240],
            "page_index": page,
            "page_bbox": bbox,
            "confidence": round(max(0.0, min(1.0, confidence)), 4),
            "method": "rule",
        }


def _pair_label_value(result: dict[str, dict], texts: list[dict]) -> None:
    """二段对齐：字段名行只有标签（如“图名”后无值）时，取同页同列、y 紧邻下方的一行作为值候选。

    仅用于图签栏元数据候选，最终仍需人工核对。
    """
    labels = [(key, val) for key, val in result.items() if key.endswith("_label")]
    if not labels:
        return
    by_page: dict[int, list[list[float]]] = {}
    for item in texts:
        page = int(item.get("page_index") or item.get("page") or 0)
        bbox = item.get("bbox")
        if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            by_page.setdefault(page, []).append(bbox)
    used_values: set[str] = set()
    for label_key, label_val in labels:
        bb = label_val.get("page_bbox")
        page = int(label_val.get("page_index") or 0)
        if not isinstance(bb, (list, tuple)) or len(bb) < 4:
            continue
        lx = float(bb[0]); lx1 = float(bb[2]); ly_c = (float(bb[1]) + float(bb[3])) / 2.0
        best = None; best_dist = float("inf")
        for candidate_bbox in by_page.get(page, []):
            if all(abs(float(candidate_bbox[i]) - float(bb[i])) < 0.01 for i in range(4)):
                continue  # 排除标签自身
            bx = ",".join(f"{float(v):.4f}" for v in candidate_bbox[:4])
            if bx in used_values:
                continue  # 一个值行只配对一个标签
            cx0, cy0, cx1, cy1 = (float(v) for v in candidate_bbox[:4])
            # 同列（x 重叠）
            if not (max(lx, cx0) < min(lx1, cx1) + 0.01):
                continue
            cy_c = (cy0 + cy1) / 2.0
            # 值须在标签下方（PDF 坐标 y 向下增大），避免配到上方/其他行
            if cy_c <= ly_c + 1.0:
                continue
            gap = cy_c - ly_c
            if gap > 12.0:  # 容忍相邻约两行（PDF 点）
                continue
            dist = abs((cx0 + cx1) / 2.0 - (lx + lx1) / 2.0) + gap
            if dist < best_dist:
                best_dist = dist; best = candidate_bbox
        if best is None:
            continue
        used_values.add(",".join(f"{float(v):.4f}" for v in best[:4]))
        # 按该 bbox 找对应文本
        for item in texts:
            b = item.get("bbox")
            if isinstance(b, list) and len(b) >= 4 and all(abs(float(b[i]) - best[i]) < 0.01 for i in range(4)):
                value = str(item.get("text") or "").strip()
                if not value or value == str(label_val.get("value") or ""):
                    continue
                key = label_key[:-len("_label")]
                conf = float(label_val.get("confidence") or 0.75)
                _append_best_candidate(result, key, value, page, b, conf)
                break



def _match_title_text(target: dict[str, dict], item: dict) -> bool:
    """对单行做图签栏关键词匹配；命中返回 True。"""
    text = str(item.get("text") or item.get("line") or "").strip()
    if not text:
        return False
    page = int(item.get("page_index") or item.get("page") or 0)
    bbox = item.get("bbox")
    confidence = float(item.get("confidence") or item.get("ocr_confidence") or 0.75)
    matched = False
    for pattern, key in TITLE_BLOCK_KEYS:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if not m:
            continue
        matched = True
        tail = text[m.end():].strip(" :：—=_")
        if tail:
            _append_best_candidate(target, key, tail, page, bbox, confidence)
        else:
            _append_best_candidate(target, key + "_label", text, page, bbox, confidence)
    return matched


def extract_title_block(texts: list[dict]) -> dict:
    """关键词版图签栏语义候选（全量兜底）。"""
    result: dict[str, dict] = {}
    for item in texts:
        _match_title_text(result, item)
    _pair_label_value(result, texts)
    return result


def extract_title_block_layout(texts: list[dict]) -> dict:
    """版式优先图签栏提取：先扫右下角图签栏区域命中字段，未命中的字段再回退全量关键词。"""
    result: dict[str, dict] = {}
    by_page: dict[int, list[dict]] = {}
    max_x: dict[int, float] = {}
    max_y: dict[int, float] = {}
    for item in texts:
        page = int(item.get("page_index") or item.get("page") or 0)
        by_page.setdefault(page, []).append(item)
        bbox = item.get("bbox")
        if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            max_x[page] = max(max_x.get(page, 0.0), float(bbox[0]), float(bbox[2]))
            max_y[page] = max(max_y.get(page, 0.0), float(bbox[1]), float(bbox[3]))
    # 先按右下区域（宽>45%、高<55%）优先
    priority: list[dict] = []
    rest: list[dict] = []
    for page, items in by_page.items():
        pw = max_x.get(page)
        ph = max_y.get(page)
        for item in items:
            bbox = item.get("bbox")
            in_region = False
            if isinstance(bbox, (list, tuple)) and len(bbox) >= 4 and pw and ph:
                x0, y0, x1, y1 = (float(v) for v in bbox[:4])
                cx = (min(x0, x1) + max(x0, x1)) / 2.0
                cy = (min(y0, y1) + max(y0, y1)) / 2.0
                in_region = cx > 0.45 * pw and cy < 0.55 * ph
            (priority if in_region else rest).append(item)
    for item in priority:
        _match_title_text(result, item)
    for item in rest:
        _match_title_text(result, item)
    _pair_label_value(result, priority + rest)
    return result


def _norm_bbox(bbox_raw: list) -> list[float] | None:
    try:
        x0, y0, x1, y1 = (float(v) for v in bbox_raw[:4])
    except (TypeError, ValueError):
        return None
    low = [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
    return low if low[0] <= low[2] and low[1] <= low[3] else None


def _px_to_pdf_bbox(bbox_px: list[float] | None, dpi: int = 200) -> list[float] | None:
    """OCR 像素框换算为 PDF 点（1in=72pt，dpi 默认渲染 200）。"""
    if not bbox_px or len(bbox_px) < 4:
        return None
    scale = 72.0 / float(dpi)
    return [round(float(v) * scale, 3) for v in bbox_px[:4]]


def _resolve_selected_pages(pages_arg: str | None, page_count: int) -> tuple[set[int] | None, list[int]]:
    """把 --pages 1,3-5 解析为 1-based 页码集合；返回 (选中集合或 None, 越界页列表)。

    None 表示不筛选（处理全部页）；越界页只记录并跳过，不阻断主流程。
    """
    if not pages_arg or page_count < 1:
        return None, []
    wanted: set[int] = set()
    for part in str(pages_arg).split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, _, b = part.partition("-")
            try:
                lo, hi = int(a), int(b)
            except ValueError:
                continue
            wanted.update(range(lo, min(hi, page_count) + 1))
        else:
            try:
                wanted.add(int(part))
            except ValueError:
                continue
    invalid = sorted({p for p in wanted if p < 1 or p > page_count})
    selected = {p for p in wanted if 1 <= p <= page_count}
    return (selected if selected else None), invalid



def text_based_candidates(entry: dict, out_dir: Path, source: str, source_format: str, vec_items: list[dict] | None = None, selected_pages: set[int] | None = None) -> tuple[list[dict], list[dict]]:
    """文本页候选；返回 (候选列表, 用于图签栏分析的文本行)。

        有矢量原生坐标（vec_items）时，把与该行同页同文的坐标转成 bbox 回填，
    供图签栏版式优先使用；无坐标时 bbox=null（PDF 原生文字没有像素框）。
        pdf-inspector 的 markdown 用 ``` 代码块按页分隔，页序号从 1 递增；
    selected_pages 非空时只输出指定页的候选。
    """
    vec_index: dict[tuple[int, str], list[float]] = {}
    for item in (vec_items or []):
        key = (int(item.get("page") or 1), str(item.get("text") or "").strip())
        if key not in vec_index:
            x = float(item.get("x") or 0); y = float(item.get("y") or 0)
            w = float(item.get("width") or 0); h = float(item.get("height") or 0)
            vec_index[key] = [round(x, 3), round(y - h, 3), round(x + w, 3), round(y, 3)]
    md_file = Path(entry.get("markdown_file") or out_dir / f"{Path(source).stem}.md")
    candidates: list[dict] = []
    title_input: list[dict] = []
    idx = 0
    if not md_file.exists():
        return [], []
    text = md_file.read_text(encoding="utf-8")
    page = 1
    in_fence = False
    fence_count = 0
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            if not in_fence:
                fence_count += 1
                page = fence_count
            in_fence = not in_fence
            continue
        clean = stripped.strip("`").strip()
        if not clean:
            continue
        if clean.startswith("## "):
            continue
        if clean.lower().startswith(("#", "|", "-", "*")) and len(clean) < 4:
            continue
        if selected_pages is not None and page not in selected_pages:
            continue
        bbox = vec_index.get((page, clean))
        evidence = [{"source": "pdf-inspector", "file": source, "page": page, "method": "native-text", "bbox": bbox}]
        candidates.append(make_candidate(
            "text", clean, evidence, "pdf-inspector-native", source, page, bbox, 0.85, idx,
            ["missing_layer", "missing_unit", "missing_scale"],
            "PDF 原生文本候选，带原生文字坐标（PDF 点单位，不参与测量）；仅作识图提示，需人工核对。",
            source_format,
        ))
        title_input.append({"text": clean, "page_index": page, "bbox": bbox, "confidence": 0.85})
        idx += 1
    return candidates, title_input


def scanned_candidates(pdf: Path, entry: dict, source: str, cache_dir: Path, source_format: str, max_workers: int, force: bool, digest: str, selected_pages: set[int] | None = None, review_dir: Path | None = None) -> tuple[list[dict], list[dict], dict]:
    """扫描页候选：逐页渲染+OCR（线程池并行），带页面级缓存；selected_pages 非空时只处理指定页。

    review_dir 非空时，OCR 失败页、无有效文字页、整页低置信页会把原图 PNG 保留到
    review_dir（同时写入同页候选的 review_image），供人眼或多模态复核。
    """
    pages = [p for p in (entry.get("ocr_pages") or []) if selected_pages is None or int(p) in selected_pages]
    candidates: list[dict] = []
    title_input: list[dict] = []
    idx = 0
    cache_stats = {"cache_hits": 0, "page_total": len(pages), "selected_pages": sorted(pages)}
    review_pages: dict[int, dict] = {}
    page_screenshots = 0

    def save_review(page: int, reason: str) -> str | None:
        nonlocal page_screenshots
        if review_dir is None or page_screenshots >= MAX_REVIEW_PAGES_PER_PDF:
            return None
        img = page_review_image(pdf, page, review_dir)
        if img is None:
            return None
        page_screenshots += 1
        rel = f"_review/{img.name}"
        review_pages[int(page)] = {"page": int(page), "image": rel, "reason": reason, "source": str(pdf)}
        return rel

    def work(page: int):
        try:
            lines, meta = ocr_page_cached(pdf, page, cache_dir, force, digest)
            return page, lines, meta
        except RuntimeError as exc:
            return page, exc, None

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_iter = pool.map(work, pages, chunksize=1)
        for page, lines, meta in future_iter:
            page = int(page)
            if meta and meta.get("cache_hit"):
                cache_stats["cache_hits"] += 1
            if isinstance(lines, Exception):
                rel = save_review(page, "OCR 失败")
                cand = make_candidate(
                    "text", f"[OCR 失败 page {page}]",
                    [{"source": "local-ocr", "file": str(pdf), "page": page, "error": str(lines)}],
                    "local-ocr", source, page, None, 0.0, idx,
                    ["low_confidence_inference", "missing_layer", "missing_unit", "missing_scale"],
                    "扫描页 OCR 失败，需人工查阅原图（_review 内附复核截图）。",
                    source_format,
                )
                if rel:
                    cand["review_image"] = rel
                candidates.append(cand)
                idx += 1
                continue
            page_conf_sum = 0.0
            page_text_lines = 0
            low_lines = 0
            page_cands: list[dict] = []
            page_title: list[dict] = []
            for line in lines:
                text = str(line.get("text") or "").strip()
                if not text:
                    continue
                try:
                    conf = float(line.get("conf") or line.get("confidence") or 0.0)
                except (TypeError, ValueError):
                    conf = 0.0
                if conf > 1.0:
                    conf = conf / 100.0
                page_conf_sum += max(0.0, min(1.0, conf))
                page_text_lines += 1
                if conf < LOW_CONF_LINE:
                    low_lines += 1
                bbox_px = _norm_bbox([line.get(k, 0.0) for k in ("x0", "y0", "x1", "y1")])
                bbox = _px_to_pdf_bbox(bbox_px, dpi=200)
                evidence = [{"source": "local-ocr", "file": str(pdf), "page": page, "method": "local-ocr", "dpi": 200, "source_bbox_px": bbox_px, "page_bbox": bbox}]
                cand = make_candidate(
                    "text", text, evidence, "local-ocr-pixel", source, page, bbox, conf, idx,
                    ["missing_layer", "missing_unit", "missing_scale"],
                    "扫描件 OCR 像素级文字候选，bbox 已换算为 PDF 点（dpi200，1in=72pt），无矢量几何/图层/比例，不参与测量，需人工核对。",
                    source_format,
                )
                cand["source_bbox_px"] = bbox_px
                if conf < LOW_CONF_LINE:
                    cand.setdefault("review_reasons", [])
                    if "low_confidence_inference" not in cand["review_reasons"]:
                        cand["review_reasons"].append("low_confidence_inference")
                page_cands.append(cand)
                page_title.append({"text": text, "page_index": page, "bbox": bbox, "confidence": conf})
                idx += 1
            if not page_text_lines:
                rel = save_review(page, "扫描页 OCR 无有效文字")
            else:
                avg = page_conf_sum / page_text_lines
                if avg < LOW_CONF_PAGE_AVG or low_lines > 0:
                    parts = []
                    if low_lines:
                        parts.append(f"整页含 {low_lines} 条低置信(<{int(LOW_CONF_LINE*100)}%)文字")
                    if avg < LOW_CONF_PAGE_AVG:
                        parts.append(f"整页平均置信 {avg*100:.0f}% 低于 {int(LOW_CONF_PAGE_AVG*100)}%")
                    rel = save_review(page, "低置信区块，" + "；".join(parts))
                else:
                    rel = None
            if rel:
                _mark_up_to(review_pages.get(int(page)), page_cands)
            candidates.extend(page_cands)
            title_input.extend(page_title)
    cache_stats["review_pages"] = review_pages
    return candidates, title_input, cache_stats


def vec_coords(pdf: Path) -> dict:
    """读取矢量 PDF 原生文字坐标；失败/非矢量返回空结构，不阻断主流程。"""
    tmp = tempfile.NamedTemporaryFile(prefix="cad-pdf-vec-", suffix=".json", delete=False, mode="w", encoding="utf-8")
    tmp_path = Path(tmp.name); tmp.close()
    try:
        proc = subprocess.run(
            [str(PDF_INSPECTOR_VENV), str(PDF_VEC_SCRIPT), str(pdf), "--json", str(tmp_path)],
            capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0:
            return {"count": 0, "items": [], "error": proc.stderr.strip()[-200:]}
        if not tmp_path.exists():
            return {"count": 0, "items": [], "error": "无输出"}
        data = json.loads(tmp_path.read_text(encoding="utf-8"))
        return {"count": data.get("count", 0), "items": data.get("items", []), "error": None}
    except Exception as exc:  # noqa: BLE001
        return {"count": 0, "items": [], "error": str(exc)[-200:]}
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass


def build_contract(candidates: list[dict], entry: dict, source: str, out_dir: Path, only_classify: bool, source_format: str, title_block: dict, cache_stats: dict) -> dict:
    main = [c for c in candidates if c["confidence_tier"] != "review_required"]
    review = [c for c in candidates if c["confidence_tier"] == "review_required"]
    contract = {
        "schema": SOURCE_SCHEMA,
        "source": source,
        "origin_schema": "cad-file-reader/pdf-ocr-v2",
        "summary": {
            "total": len(main) + len(review),
            "candidate_count": len(main),
            "review_required": len(review),
            "confirmed_evidence": sum(1 for c in main if c["confidence_tier"] == "confirmed_evidence"),
            "inferred_candidate": sum(1 for c in main if c["confidence_tier"] == "inferred_candidate"),
        },
        "review_reasons": REVIEW_REASONS,
        "candidates": main,
        "review_candidates": review,
        "boundary": "PDF 识图只输出文字候选与证据，不输出最终工程量、材料量、造价或结算量（final_quantity=false）；扫描件 OCR 无矢量几何，不得用于测量。图签栏字段仅作元数据锚点，需人工核对。",
    }
    payload = {
        "source_file": source,
        "source_format": source_format,
        "pdf_meta": {
            "has_vector_geometry": source_format == "pdf_vector",
            "vector_text_items": cache_stats.get("vector_text_items", []),
            "vector_text_count": int(cache_stats.get("vector_text_count", 0)),
            "pdf_type": entry.get("pdf_type"),
            "page_count": entry.get("page_count"),
            "confidence": entry.get("confidence"),
            "direct_pages": entry.get("direct_pages"),
            "ocr_pages": entry.get("ocr_pages"),
            "source_format": source_format,
            "classify_only": only_classify,
            "cache": cache_stats,
            "title_block": title_block,
        },
        "contract": contract,
    }
    return payload


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="PDF 图纸识图候选（本机分流 + 本地 OCR）")
    parser.add_argument("inputs", nargs="+", help="PDF 文件或目录")
    parser.add_argument("--out-dir", default="pdf识图", help="输出目录")
    parser.add_argument("--cache-dir", default=None, help="两级缓存目录（默认 <out-dir>/_pdf_cache）")
    parser.add_argument("--workers", type=int, default=3, help="扫描页并行数（默认3，建议≤CPU核心数）")
    parser.add_argument("--classify-only", action="store_true", help="只分类不 OCR")
    parser.add_argument("--no-text", action="store_true", help="跳过文本页候选")
    parser.add_argument("--pages", default=None, metavar="1,3-5", help="只处理指定 1-based 页码（逗号/连字符）；默认全部页")
    parser.add_argument("--force", action="store_true", help="忽略两级缓存，重新解析/渲染")
    parser.add_argument("--review-out", default=None, metavar="DIR",
                        help="复核截图输出目录（默认 <out-dir>/_review）")
    parser.add_argument("--no-review", action="store_true", help="不输出 _review 复核截图")
    args = parser.parse_args()

    pdfs: list[Path] = []
    for raw in args.inputs:
        path = Path(raw)
        if path.is_dir():
            pdfs.extend(sorted(p for p in path.rglob("*") if p.suffix.lower() == ".pdf"))
        elif path.is_file():
            pdfs.append(path)
    if not pdfs:
        print(json.dumps({"error": "no PDF found"}, ensure_ascii=False, indent=2))
        return 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = Path(args.cache_dir) if args.cache_dir else out_dir / "_pdf_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    review_dir = None
    if not args.no_review:
        review_dir = Path(args.review_out) if args.review_out else out_dir / "_review"
        review_dir.mkdir(parents=True, exist_ok=True)
    all_review: list[dict] = []
    results = []
    for pdf_file in pdfs:
        pdf_file = pdf_file.resolve()
        source = str(pdf_file)
        pdf_hash = _file_hash(pdf_file)
        try:
            entry = classify(pdf_file, out_dir, cache_dir, args.force)
        except RuntimeError as exc:
            results.append({"file": source, "error": str(exc)})
            continue
        source_format = SOURCE_FORMAT_MAP.get(entry.get("pdf_type") or "mixed", "pdf_hybrid")
        selected_pages, invalid_pages = _resolve_selected_pages(args.pages, int(entry.get("page_count") or 1))
        if args.classify_only:
            results.append({"file": source, "pdf_meta": entry, "candidates": 0, "source_format": source_format, "action": "classify-only"})
            continue
        candidates: list[dict] = []
        title_input: list[dict] = []
        cache_stats: dict = {"file_meta_cached": True, "selected_pages": (sorted(selected_pages) if selected_pages else None), "invalid_pages": invalid_pages}
        if source_format == "pdf_vector" and not args.classify_only:
            vec = vec_coords(pdf_file)
            cache_stats["vector_text_count"] = vec.get("count", 0)
            cache_stats["vector_text_items"] = vec.get("items", [])
            cache_stats["vector_text_error"] = vec.get("error")
        if not args.no_text:
            text_cands, text_title = text_based_candidates(entry, out_dir, source, source_format, cache_stats.get("vector_text_items"), selected_pages)
            candidates.extend(text_cands)
            title_input.extend(text_title)
        if entry.get("ocr_pages"):
            try:
                scan_cands, scan_title, scan_cache = scanned_candidates(
                    pdf_file, entry, source, cache_dir, source_format, max(args.workers, 1), args.force, pdf_hash,
                    selected_pages, review_dir
                )
                candidates.extend(scan_cands)
                title_input.extend(scan_title)
                cache_stats.update(scan_cache)
            except RuntimeError as exc:
                results.append({"file": source, "error": str(exc), "partial_candidates": len(candidates)})
                continue
        # 全文件元数据缓存命中标记
        meta_file = cache_dir / f"{pdf_hash}.meta.json"
        cache_stats["file_meta_cached"] = meta_file.exists() and not args.force
        title_block = extract_title_block_layout(title_input)
        payload = build_contract(candidates, entry, source, out_dir, args.classify_only, source_format, title_block, cache_stats)
        out_json = out_dir / f"{pdf_file.stem}.pdf识图.json"
        out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        markdown = []
        markdown.append(f"# PDF 识图候选：{pdf_file.name}")
        markdown.append(f"- PDF 类型：{entry.get('pdf_type')}；source_format：{source_format}；页数：{entry.get('page_count')}")
        if selected_pages is not None:
            markdown.append(f"- 指定页：{','.join(str(p) for p in sorted(selected_pages))}（跳过未指定页）")
        markdown.append(f"- 候选总数：{len(candidates)}；全部为文字候选（final_quantity=false）")
        if title_block:
            markdown.append("")
            markdown.append("## 图签栏候选（元数据锚点，需人工核对）")
            for key, item in sorted(title_block.items()):
                markdown.append(f"- {item.get('key')} = {item.get('value')} (page {item.get('page_index')}, conf={item.get('confidence')})")
        markdown.append("")
        markdown.append("## review_candidates")
        for c in payload["contract"]["review_candidates"]:
            markdown.append(f"- [page {c.get('page_index','')}] {c.get('text')} (conf={c.get('confidence')})")
            markdown.append(f"  - {c.get('review_notes')}")
        (out_dir / f"{pdf_file.stem}.pdf识图.md").write_text("\n".join(markdown), encoding="utf-8")
        for rec in (cache_stats.get("review_pages") or {}).values():
            rec.setdefault("file", source)
            all_review.append(rec)
        results.append({"file": source, "pdf_type": entry.get("pdf_type"),
                        "source_format": source_format, "candidates": len(candidates),
                        "output": str(out_json), "cache": cache_stats, "error": None})

    if review_dir is not None and all_review:
        index = {
            "schema": "cad-file-reader/pdf-ocr/_review/v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "out_dir": str(out_dir),
            "images": all_review,
        }
        (review_dir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    report = {
        "tool": "cad-file-reader-pdf-ocr",
        "version": "v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "out_dir": str(out_dir),
        "cache_dir": str(cache_dir),
        "review_images_count": len(all_review),
        "review_dir": str(review_dir) if review_dir else None,
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
