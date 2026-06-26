#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调用 DramaAIStudio（灵伴 iDrama）OpenAPI，仅拉取各资产「候选图终稿」信息（§6.7）：

- `GET /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/candidates/final-candidates`

将快照写入「数据总目录 / 项目ID / asset_final_candidates.json」；
与上次快照对比后输出 `initial` / `changed` / `unchanged`（与 sync_project_assets_snapshot.py 一致）。

6.7 的 `items[].url` 为短时签名，不参与前后对比；比对使用不含 `url` 的稳定字段。
若终稿集合或稳定字段有变更，在 diff 的对应条目中附带 `before`/`after` 的签名 URL 映射便于直接打开。

依赖：Python 3.9+，仅标准库。
认证：环境变量 IDRAMA_TOKEN，或命令行 --token。
基地址：环境变量 IDRAMA_BASE_URL，默认 https://idrama.lingban.cn
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def _final_items_stable(items: Any) -> List[Dict[str, Any]]:
    """
    将 §6.7 的 items 转为可比对结构：去掉短时签名 `url`，仅保留稳定字段。
    兼容旧快照：历史上 `url` 可能嵌在 `final_items` 元素内。
    """
    if not isinstance(items, list):
        return []
    out: List[Dict[str, Any]] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        row = {k: v for k, v in it.items() if k != "url"}
        out.append(row)
    return out


def _final_signed_url_map_from_items(items: Any) -> Dict[str, str]:
    """从原始 items 提取 candidate_id -> 签名 url（若有）。"""
    if not isinstance(items, list):
        return {}
    m: Dict[str, str] = {}
    for it in items:
        if not isinstance(it, dict):
            continue
        cid = it.get("candidate_id")
        u = it.get("url")
        if cid is None or u is None:
            continue
        m[str(cid)] = str(u)
    return m


def _final_urls_map_from_asset(row: Dict[str, Any]) -> Dict[str, str]:
    """读取资产行上的 `final_urls`（candidate_id -> 可打开地址）。"""
    u = row.get("final_urls")
    return dict(u) if isinstance(u, dict) else {}


def _utc_iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _request_json(
    base_url: str,
    token: str,
    method: str,
    path: str,
    *,
    timeout: float = 120.0,
) -> Tuple[int, Dict[str, Any]]:
    url = urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    req = urllib.request.Request(
        url,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            status = getattr(resp, "status", 200) or 200
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        status = e.code
    try:
        body = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        body = {"_raw": raw, "_parse_error": True}
    return status, body if isinstance(body, dict) else {"_raw": body}


def _unwrap_api(body: Dict[str, Any]) -> Tuple[int, Any, str]:
    code = body.get("code", 0)
    try:
        code_int = int(code)
    except (TypeError, ValueError):
        code_int = 0
    return code_int, body.get("data"), str(body.get("msg") or "")


def fetch_asset_list(base_url: str, token: str, play_id: str, *, include_deleted: bool) -> List[Dict[str, Any]]:
    q = {"include_deleted": "true"} if include_deleted else {}
    qs = urllib.parse.urlencode(q) if q else ""
    path = f"/openapi/drama/{play_id}/assets/list" + (f"?{qs}" if qs else "")
    status, body = _request_json(base_url, token, "GET", path)
    code, data, msg = _unwrap_api(body)
    if status >= 400 or code != 1:
        raise RuntimeError(f"资产列表失败 HTTP {status} code={code} msg={msg}")
    if not isinstance(data, list):
        raise RuntimeError(f"资产列表 data 类型异常: {type(data)}")
    return [x for x in data if isinstance(x, dict)]


def fetch_final_candidates(
    base_url: str, token: str, play_id: str, asset_type: Any, asset_id: str
) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, str], Optional[str]]:
    """
    §6.7 终稿列表。
    返回 (不含 url 的稳定 items、candidate_id 有序列表、签名 url 映射、若失败则为 error 否则 None)。
    """
    try:
        at = int(asset_type)
    except (TypeError, ValueError):
        return [], [], {}, "invalid asset_type"
    path = (
        f"/openapi/drama/{play_id}/assets/{at}/"
        f"{urllib.parse.quote(str(asset_id), safe='')}/general/candidates/final-candidates"
    )
    status, body = _request_json(base_url, token, "GET", path)
    code, data, msg = _unwrap_api(body)
    if status >= 400 or code != 1:
        return [], [], {}, f"HTTP {status} code={code} msg={msg}"
    if not isinstance(data, dict):
        return [], [], {}, "data not object"
    items = data.get("items") or []
    if not isinstance(items, list):
        return [], [], {}, "items not list"
    raw_items: List[Dict[str, Any]] = [x for x in items if isinstance(x, dict)]
    finals: List[str] = []
    for it in raw_items:
        cid = it.get("candidate_id")
        if cid is not None:
            finals.append(str(cid))
    stable = _final_items_stable(raw_items)
    url_map = _final_signed_url_map_from_items(raw_items)
    return stable, finals, url_map, None


def build_snapshot(
    base_url: str,
    token: str,
    play_id: str,
    *,
    include_deleted: bool,
) -> Dict[str, Any]:
    rows = fetch_asset_list(base_url, token, play_id, include_deleted=include_deleted)
    assets_out: List[Dict[str, Any]] = []
    for summary in sorted(rows, key=lambda x: str(x.get("id", ""))):
        aid = str(summary.get("id", ""))
        if not aid:
            continue
        at = summary.get("type")
        final_items, final_ids, signed_map, final_err = fetch_final_candidates(base_url, token, play_id, at, aid)
        assets_out.append(
            {
                "id": aid,
                "type": at,
                "name": summary.get("name"),
                "deleted": bool(summary.get("deleted", False)),
                "operation_time": summary.get("operation_time"),
                "has_final_image": summary.get("has_final_image"),
                "final_candidate_ids": final_ids,
                "final_items": final_items,
                "final_urls": signed_map,
                "final_fetch_error": final_err,
            }
        )
    return {
        "schema_version": 2,
        "play_id": str(play_id),
        "fetched_at": _utc_iso_now(),
        "include_deleted": include_deleted,
        "focus": "asset_final_candidates_only",
        "assets": assets_out,
    }


def _asset_key_map(snapshot: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    assets = snapshot.get("assets") or []
    out: Dict[str, Dict[str, Any]] = {}
    if isinstance(assets, list):
        for a in assets:
            if isinstance(a, dict) and a.get("id") is not None:
                out[str(a["id"])] = a
    return out


def diff_snapshots(old: Optional[Dict[str, Any]], new: Dict[str, Any]) -> Dict[str, Any]:
    if old is None:
        return {
            "initial": True,
            "play_id": new.get("play_id"),
            "asset_count": len(new.get("assets") or []),
        }

    # 第 1 步：逐项对比稳定字段；签名 URL 仅用于 diff 展示，不参与是否变更判定。
    old_m = _asset_key_map(old)
    new_m = _asset_key_map(new)
    old_ids = set(old_m.keys())
    new_ids = set(new_m.keys())

    changes: Dict[str, Any] = {
        "initial": False,
        "play_id": new.get("play_id"),
        "assets_added": sorted(new_ids - old_ids),
        "assets_removed": sorted(old_ids - new_ids),
        "assets_modified": [],
    }

    for aid in sorted(old_ids & new_ids):
        o = old_m[aid]
        n = new_m[aid]
        mods: Dict[str, Any] = {}
        for field in ("name", "type", "deleted", "operation_time", "has_final_image"):
            if o.get(field) != n.get(field):
                mods[field] = {"before": o.get(field), "after": n.get(field)}
        if o.get("final_candidate_ids") != n.get("final_candidate_ids"):
            mods["final_candidate_ids"] = {
                "before": o.get("final_candidate_ids"),
                "after": n.get("final_candidate_ids"),
            }
        o_stable = _final_items_stable(o.get("final_items"))
        n_stable = _final_items_stable(n.get("final_items"))
        if o_stable != n_stable:
            mods["final_items"] = {"before": o_stable, "after": n_stable}
        fe_o = o.get("final_fetch_error")
        fe_n = n.get("final_fetch_error")
        if fe_o != fe_n:
            mods["final_fetch_error"] = {"before": fe_o, "after": fe_n}
        if mods.get("final_candidate_ids") is not None or mods.get("final_items") is not None:
            old_urls = _final_urls_map_from_asset(o)
            new_urls = _final_urls_map_from_asset(n)
            mods["final_urls"] = {"before": old_urls, "after": new_urls}
        if mods:
            changes["assets_modified"].append({"asset_id": aid, "name": n.get("name"), "changes": mods})

    added_ids = changes.get("assets_added") or []
    if added_ids:
        previews: List[Dict[str, Any]] = []
        for xid in added_ids:
            row = new_m.get(str(xid)) or {}
            previews.append(
                {
                    "asset_id": str(xid),
                    "name": row.get("name"),
                    "final_urls": _final_urls_map_from_asset(row),
                }
            )
        changes["assets_added_media"] = previews

    removed_ids = changes.get("assets_removed") or []
    if removed_ids:
        rprev: List[Dict[str, Any]] = []
        for xid in removed_ids:
            row = old_m.get(str(xid)) or {}
            rprev.append(
                {
                    "asset_id": str(xid),
                    "name": row.get("name"),
                    "final_urls": _final_urls_map_from_asset(row),
                }
            )
        changes["assets_removed_media"] = rprev

    return changes


def has_meaningful_change(diff: Dict[str, Any]) -> bool:
    if diff.get("initial"):
        return False
    if diff.get("assets_added") or diff.get("assets_removed"):
        return True
    if diff.get("assets_modified"):
        return True
    return False


def load_json_file(path: str) -> Optional[Dict[str, Any]]:
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(path: str, data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="拉取资产候选图终稿快照（§6.7），写入本地并对比上次结果",
    )
    parser.add_argument("play_id", help="剧目（项目）ID")
    parser.add_argument(
        "--data-dir",
        default=os.environ.get("IDRAMA_DATA_DIR", "./project_data"),
        help="数据总目录（默认 ./project_data 或环境变量 IDRAMA_DATA_DIR）",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("IDRAMA_BASE_URL", "https://idrama.lingban.cn"),
        help="API 基地址（默认读 IDRAMA_BASE_URL）",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("IDRAMA_TOKEN", ""),
        help="Bearer Token（默认读环境变量 IDRAMA_TOKEN）",
    )
    parser.add_argument(
        "--include-deleted",
        action="store_true",
        help="资产列表包含已软删除项（§6.1 include_deleted=true）",
    )
    parser.add_argument(
        "--print-full-snapshot",
        action="store_true",
        help="无论是否变化，将完整快照 JSON 打印到 stdout",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="仅输出变更或错误；正常情况不打印进度",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.WARNING if args.quiet else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    token = (args.token or "").strip()
    if not token:
        logger.error("缺少 Token：请设置环境变量 IDRAMA_TOKEN 或使用 --token")
        return 2

    play_id = str(args.play_id).strip()
    project_dir = os.path.join(args.data_dir, play_id)
    snapshot_path = os.path.join(project_dir, "asset_final_candidates.json")

    try:
        new_snap = build_snapshot(
            args.base_url,
            token,
            play_id,
            include_deleted=args.include_deleted,
        )
    except Exception:
        logger.exception("拉取候选终稿快照失败 play_id=%s", play_id)
        return 1

    previous = load_json_file(snapshot_path)
    diff = diff_snapshots(previous, new_snap)

    if diff.get("initial"):
        save_json_file(snapshot_path, new_snap)
        if not args.quiet:
            print(json.dumps({"status": "initial", "path": snapshot_path, "detail": diff}, ensure_ascii=False, indent=2))
        elif args.print_full_snapshot:
            print(json.dumps(new_snap, ensure_ascii=False, indent=2))
        return 0

    if has_meaningful_change(diff):
        print(json.dumps({"status": "changed", "diff": diff}, ensure_ascii=False, indent=2))
        save_json_file(snapshot_path, new_snap)
        if args.print_full_snapshot:
            print(json.dumps({"status": "full_snapshot", "snapshot": new_snap}, ensure_ascii=False, indent=2))
        return 0

    save_json_file(snapshot_path, new_snap)
    if not args.quiet:
        print(json.dumps({"status": "unchanged", "play_id": play_id, "path": snapshot_path}, ensure_ascii=False, indent=2))
    if args.print_full_snapshot:
        print(json.dumps(new_snap, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
