#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad_scan 的低内存证据缓存与局部读取。

缓存按“单个源文件 + 影响原始证据的参数档”保存文字、图层、图框、块和几何证据。
缓存不保存工程量，也不参与扣减、损耗或造价计算。
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sqlite3
import tempfile
import time
from pathlib import Path
from typing import Any

# v3：图层名解码失败时改用 "#句柄" 作为图层身份（旧版会把整张图层表解成空串并落空图层）。
# 不升版本会让旧缓存把「空图层」结果原样复用，修复等于白做。
# v4：vendor 里的 ezdwg 由 0.12.6 升到 0.17.2——旧版对部分 DWG 会把图层名整表解成空串
# （实测 J-1结构 106 个图层名全空），新版能全部解出真实名（DIM/COLU_HATCH/WALL…）。
# 图层名从「#句柄降级」变成「真名」，证据内容整体变了，必须重新缓存。
CACHE_VERSION = 4
_TIMEOUT_MARKERS = (
    "解码超",
    "解码失败",
    "解码异常",
    "解析失败",
    "几何解码不可用",
    "几何解码失败",
    "达上限",
)

ROI = tuple[float, float, float, float]


def profile_for(args: Any, want: set[str]) -> dict:
    """生成影响原始证据内容的参数档；查询过滤和输出格式不进入该档。"""
    return {
        "cache_version": CACHE_VERSION,
        "kind": "cad_scan_raw",
        "want": sorted(want),
        "with_insert": bool(getattr(args, "with_insert", False)),
        "with_blocks": bool(getattr(args, "with_blocks", False)),
        "with_geom": bool(getattr(args, "with_geom", False)),
        "with_geom_layer": bool(getattr(args, "with_geom_layer", False)),
        "with_block_geom": bool(getattr(args, "with_block_geom", False)),
        "budget": float(getattr(args, "budget", 45.0)),
        "max_rows": int(getattr(args, "max_rows", 200000)),
        "geom_budget": float(getattr(args, "geom_budget", 0.0)),
        "geom_max_rows": int(getattr(args, "geom_max_rows", 0)),
        "no_sheet": bool(getattr(args, "no_sheet", False)),
        "sheets": str(getattr(args, "sheets", "auto")),
        "sheet_min": int(getattr(args, "sheet_min", 60)),
        "sheet_bin": float(getattr(args, "sheet_bin", 10000.0)),
    }


def _profile_text(profile: dict) -> str:
    return json.dumps(profile, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def cache_path(cache_dir: Path, digest: str, profile: dict) -> Path:
    ident = hashlib.sha256(_profile_text(profile).encode("utf-8")).hexdigest()[:12]
    return cache_dir / f"cad-scan-v{CACHE_VERSION}-{digest[:20]}-{ident}.sqlite"


def _safe_db_path(path: Path) -> str:
    return "file:" + str(path).replace("?", "%3f").replace("#", "%23") + "?mode=ro"


def _metadata_value(conn: sqlite3.Connection, key: str, default: Any = None) -> Any:
    row = conn.execute("SELECT value FROM metadata WHERE key=?", (key,)).fetchone()
    return row[0] if row else default


def _open_ro(path: Path, digest: str, profile_text: str):
    if not path.is_file():
        return None
    try:
        conn = sqlite3.connect(_safe_db_path(path), uri=True)
        version = int(_metadata_value(conn, "cache_version", -1))
        if version != CACHE_VERSION:
            conn.close()
            return None
        if _metadata_value(conn, "source_sha256") != digest:
            conn.close()
            return None
        if _metadata_value(conn, "profile") != profile_text:
            conn.close()
            return None
        return conn
    except (sqlite3.Error, OSError):
        return None


def _finite(v: Any) -> float | None:
    try:
        x = float(v)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def _bbox(bbox: Any) -> ROI | None:
    if not isinstance(bbox, (list, tuple)) or len(bbox) < 4:
        return None
    vals = [_finite(v) for v in bbox[:4]]
    if any(v is None for v in vals):
        return None
    return (
        min(vals[0], vals[2]), min(vals[1], vals[3]),
        max(vals[0], vals[2]), max(vals[1], vals[3]),
    )


def _intersects_bbox(bbox: Any, roi: ROI) -> bool:
    box = _bbox(bbox)
    if box is None:
        return False
    x1, y1, x2, y2 = roi
    return box[0] <= x2 and box[2] >= x1 and box[1] <= y2 and box[3] >= y1


def records_in_roi(recs: list[dict], roi: ROI) -> list[dict]:
    x1, y1, x2, y2 = roi
    out = []
    for r in recs:
        x, y = _finite(r.get("x")), _finite(r.get("y"))
        if x is not None and y is not None and x1 <= x <= x2 and y1 <= y <= y2:
            out.append(r)
    return out


def segments_in_roi(segs: list, roi: ROI, seg_layers: list[str] | None = None):
    x1, y1, x2, y2 = roi
    out = []
    out_layers: list[str] | None = [] if seg_layers is not None else None
    for i, seg in enumerate(segs):
        if not isinstance(seg, (list, tuple)) or len(seg) < 4:
            continue
        ax, ay, bx, by = (_finite(seg[0]), _finite(seg[1]),
                          _finite(seg[2]), _finite(seg[3]))
        if None in (ax, ay, bx, by):
            continue
        if not (min(ax, bx) <= x2 and max(ax, bx) >= x1 and
                min(ay, by) <= y2 and max(ay, by) >= y1):
            continue
        out.append((ax, ay, bx, by))
        if out_layers is not None:
            out_layers.append(seg_layers[i] if seg_layers and i < len(seg_layers) else "")
    return out, out_layers


def sheets_in_roi(sheets: list[dict], roi: ROI) -> list[dict]:
    return [s for s in sheets if _intersects_bbox(s.get("bbox"), roi)]


def sheet_id(r: dict) -> int | None:
    try:
        value = r.get("sheet")
        return None if value is None else int(value)
    except (TypeError, ValueError):
        return None


def sheet_bbox(sheets: list[dict], sheet: int) -> ROI | None:
    for row in sheets:
        try:
            if int(row.get("id")) == int(sheet):
                return _bbox(row.get("bbox"))
        except (TypeError, ValueError):
            continue
    return None


def _segment_row(seg: Any, layer: str | None = None) -> tuple:
    """归一化几何外接框；缓存局部查询用 xmin/ymin/xmax/ymax 索引。"""
    if not isinstance(seg, (list, tuple)) or len(seg) < 4:
        raise ValueError("geometry segment requires four coordinates")
    x1, y1, x2, y2 = (_finite(v) for v in seg[:4])
    if None in (x1, y1, x2, y2):
        raise ValueError("geometry segment has non-finite coordinates")
    return (
        x1, y1, x2, y2,
        min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2),
        layer,
    )


def _roi_where(roi: ROI, table: str = "records") -> tuple[str, list]:
    x1, y1, x2, y2 = roi
    return (
        f"{table}.x IS NOT NULL AND {table}.y IS NOT NULL "
        "AND x >= ? AND x <= ? AND y >= ? AND y <= ?",
        [x1, x2, y1, y2],
    )


def _geom_where(roi: ROI) -> tuple[str, list]:
    x1, y1, x2, y2 = roi
    return (
        "xmin <= ? AND xmax >= ? AND ymin <= ? AND ymax >= ?",
        [x2, x1, y2, y1],
    )


def load_cached_scan(
    source: Path,
    cache_dir: Path,
    digest: str,
    profile: dict,
    roi: ROI | None = None,
    sheet: int | None = None,
):
    """读取缓存；局部查询时只取命中行，避免重建全图记录。

    返回 None 表示缓存未命中；--sheet 未命中时返回空结果并保留 cache hit 统计。
    """
    profile_text = _profile_text(profile)
    path = cache_path(cache_dir, digest, profile)
    conn = _open_ro(path, digest, profile_text)
    if conn is None:
        return None
    try:
        rec_where = "1=1"
        rec_params: list = []
        geom_where = "1=1"
        geom_params: list = []
        partial = roi is not None or sheet is not None

        data_rows = dict(conn.execute("SELECT key, value FROM data"))
        try:
            meta = {key: json.loads(value) for key, value in data_rows.items()}
        except Exception:
            return None
        # 旧结构没有 sheets 键；拒绝复用并让主流程重建规范缓存。
        if not isinstance(meta.get("sheets"), list):
            return None
        sheets = meta.get("sheets") or []

        if roi is not None:
            rec_where, rec_params = _roi_where(roi)
            geom_where, geom_params = _geom_where(roi)
            meta["sheets"] = sheets_in_roi(sheets, roi)
        if sheet is not None:
            bbox = sheet_bbox(sheets, sheet)
            meta["sheets"] = [
                s for s in sheets
                if str(s.get("id")) == str(sheet) and _bbox(s.get("bbox")) is not None
            ]
            if bbox is None:
                rec_where = "1=0"
                geom_where = "1=0"
                geom_params = []
            else:
                rec_where = "sheet = ?"
                rec_params = [int(sheet)]
                geom_where, geom_params = _geom_where(bbox)

        recs = [
            {"kind": kind, "text": text, "x": x, "y": y,
             "layer": layer or None, "sheet": sheet_id_value}
            for kind, text, x, y, layer, sheet_id_value
            in conn.execute(
                f"SELECT kind, text, x, y, layer, sheet FROM records WHERE {rec_where} ORDER BY id",
                rec_params,
            )
        ]

        if partial:
            layers = sorted({
                str(row[0]) for row in conn.execute(
                    f"SELECT DISTINCT layer FROM records WHERE {rec_where}", rec_params
                ) if row[0]
            })
            meta.pop("block_refs", None)
            meta.pop("insert_count", None)
            meta.pop("block_defs", None)
        else:
            layers = sorted({
                str(row[0]) for row in conn.execute("SELECT name FROM layers") if row[0]
            })

        segs: list[tuple] = []
        seg_layers: list[str] | None = None
        if bool(profile.get("with_geom_layer")):
            seg_layers = []
            for x1, y1, x2, y2, layer in conn.execute(
                f"SELECT x1, y1, x2, y2, layer FROM geometry WHERE {geom_where} ORDER BY id",
                geom_params,
            ):
                segs.append((x1, y1, x2, y2))
                seg_layers.append(layer or "")
        else:
            for x1, y1, x2, y2 in conn.execute(
                f"SELECT x1, y1, x2, y2 FROM geometry WHERE {geom_where} ORDER BY id",
                geom_params,
            ):
                segs.append((x1, y1, x2, y2))

        try:
            notes = json.loads(_metadata_value(conn, "scan_notes", "[]"))
        except Exception:
            notes = []

        return {
            "recs": recs,
            "layers": layers,
            "meta": meta,
            "segs": segs,
            "seg_layers": seg_layers,
            "notes": notes,
            "cache_file": str(path),
            "partial": partial,
            "sheet_count": len(sheets),
        }
    finally:
        try:
            conn.close()
        except Exception:
            pass


def _should_cache(notes: list[str]) -> bool:
    return not any(
        any(marker in str(note) for marker in _TIMEOUT_MARKERS)
        for note in (notes or [])
    )


def save_cached_scan(
    source: Path,
    cache_dir: Path,
    digest: str,
    profile: dict,
    recs: list[dict],
    layers: list[str],
    meta: dict,
    segs: list,
    seg_layers: list[str] | None,
    scan_notes: list[str],
) -> str | None:
    """原子写入单个源图的证据缓存。解码失败、超预算或截断时不写入。"""
    if not _should_cache(scan_notes):
        return None
    cache_meta = dict(meta or {})
    cache_meta.setdefault("sheets", [])
    if not isinstance(cache_meta["sheets"], list):
        return None
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        target = cache_path(cache_dir, digest, profile)
        fd, tmp_name = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp", dir=cache_dir)
        os.close(fd)
        tmp = Path(tmp_name)
        conn = sqlite3.connect(str(tmp))
        try:
            conn.execute("PRAGMA journal_mode=OFF")
            conn.execute("PRAGMA synchronous=OFF")
            # 临时库先批量写入，索引延后创建，降低大图缓存写入耗时。
            conn.executescript("""
                CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE data (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kind TEXT NOT NULL,
                    text TEXT NOT NULL,
                    x REAL,
                    y REAL,
                    layer TEXT,
                    sheet INTEGER
                );
                CREATE TABLE layers (name TEXT PRIMARY KEY);
                CREATE TABLE geometry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    x1 REAL NOT NULL, y1 REAL NOT NULL,
                    x2 REAL NOT NULL, y2 REAL NOT NULL,
                    xmin REAL NOT NULL, ymin REAL NOT NULL,
                    xmax REAL NOT NULL, ymax REAL NOT NULL,
                    layer TEXT
                );
            """)
            source_stat = source.stat()
            metadata = {
                "cache_version": str(CACHE_VERSION),
                "source_sha256": digest,
                "source_name": source.name,
                "source_size": str(source_stat.st_size),
                "source_mtime_ns": str(source_stat.st_mtime_ns),
                "profile": _profile_text(profile),
                "created_at": str(time.time()),
                "record_count": str(len(recs)),
                "geometry_count": str(len(segs)),
                "scan_notes": json.dumps(scan_notes or [], ensure_ascii=False),
            }
            conn.executemany(
                "INSERT INTO metadata(key,value) VALUES(?,?)", metadata.items())
            conn.executemany(
                "INSERT INTO data(key,value) VALUES(?,?)",
                [(key, json.dumps(value, ensure_ascii=False, separators=(",", ":")))
                 for key, value in cache_meta.items() if key != "segs"])
            def record_rows():
                for r in recs:
                    sid = sheet_id(r)
                    yield (
                        str(r.get("kind") or ""), str(r.get("text") or ""),
                        _finite(r.get("x")), _finite(r.get("y")),
                        str(r.get("layer") or "") or None,
                        sid,
                    )

            def geometry_rows():
                for i, seg in enumerate(segs):
                    layer = (seg_layers[i] if seg_layers and i < len(seg_layers) else "") or None
                    yield _segment_row(seg, layer)

            conn.executemany(
                "INSERT INTO records(kind,text,x,y,layer,sheet) VALUES(?,?,?,?,?,?)",
                record_rows())
            conn.executemany(
                "INSERT INTO layers(name) VALUES(?)",
                ((str(x),) for x in sorted(set(layers)) if x))
            if profile.get("with_geom_layer"):
                conn.executemany(
                    "INSERT INTO geometry(x1,y1,x2,y2,xmin,ymin,xmax,ymax,layer) "
                    "VALUES(?,?,?,?,?,?,?,?,?)",
                    geometry_rows())
            else:
                conn.executemany(
                    "INSERT INTO geometry(x1,y1,x2,y2,xmin,ymin,xmax,ymax,layer) "
                    "VALUES(?,?,?,?,?,?,?,?,?)",
                    (_segment_row(seg, None) for seg in segs))
            conn.executescript("""
                CREATE INDEX records_xy ON records(x, y);
                CREATE INDEX records_sheet ON records(sheet);
                CREATE INDEX geometry_bbox ON geometry(xmin, ymin, xmax, ymax);
            """)
            conn.commit()
        finally:
            conn.close()
        os.replace(tmp, target)
        return str(target)
    except (OSError, sqlite3.Error, ValueError, TypeError):
        try:
            if "tmp" in locals() and tmp.exists():
                tmp.unlink()
        except OSError:
            pass
        return None
