#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调用 DramaAIStudio（灵伴 iDrama）OpenAPI，拉取指定剧目下所有分镜的「选中视频」详情。

流程：
1) 通过 §5.1 获取剧本集列表（episodes）；
2) 逐集调用「GET /openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/selected-videos」；
3) 将本次结果写入「数据总目录 / 项目ID / storyboard_selected_videos.json」；
4) 与上次快照对比并输出变更摘要（initial / changed / unchanged）。

8.4 响应中 `video.result_video_url` 为短时签名，不参与前后对比；落盘的 `video` 仅含稳定字段，
该短时地址单独存放在每镜的 `result_video_url`（与接口字段同名，位于 shot 顶层）。若选用视频有变更，在 diff 中附带前后链接便于直接打开。

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
    """
    发起已鉴权的 JSON 请求，返回 (http_status, body_dict)。
    body 若不是合法 JSON 则包装为 {"_raw": text}。
    """
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
    """统一响应：返回 (code, data, msg)。"""
    code = body.get("code", 0)
    try:
        code_int = int(code)
    except (TypeError, ValueError):
        code_int = 0
    return code_int, body.get("data"), str(body.get("msg") or "")


def fetch_episodes(base_url: str, token: str, play_id: str) -> List[int]:
    """第 1 步：拉取剧本集列表，得到 episode_no 列表。"""
    path = f"/openapi/drama/{play_id}/scripts"
    status, body = _request_json(base_url, token, "GET", path)
    code, data, msg = _unwrap_api(body)
    if status >= 400 or code != 1:
        raise RuntimeError(f"获取剧本集失败 HTTP {status} code={code} msg={msg}")
    if not isinstance(data, dict):
        raise RuntimeError(f"剧本集 data 类型异常: {type(data)}")
    episodes = data.get("episodes") or []
    if not isinstance(episodes, list):
        raise RuntimeError("剧本集 episodes 字段不是数组")

    out: List[int] = []
    for ep in episodes:
        if not isinstance(ep, dict):
            continue
        try:
            no = int(ep.get("episode_no"))
        except (TypeError, ValueError):
            continue
        out.append(no)
    return sorted(set(out))


def _video_dict_for_compare(video: Any) -> Optional[Dict[str, Any]]:
    """比对用 video 字典：剔除短时签名字段，兼容历史快照误存 `result_video_url` 的情况。"""
    if video is None:
        return None
    if not isinstance(video, dict):
        return None
    return {k: v for k, v in video.items() if k != "result_video_url"}


def _video_stable_and_signed(raw: Any) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    从接口原始 video 对象拆出：可比对稳定字段（不含 result_video_url）与短时签名播放地址。
    """
    if not isinstance(raw, dict):
        return None, None
    signed = raw.get("result_video_url")
    stable: Dict[str, Any] = {
        "id": str(raw.get("id")) if raw.get("id") is not None else None,
        "mode": raw.get("mode"),
        "status": raw.get("status"),
        "result_video_path": raw.get("result_video_path"),
        "selected": raw.get("selected"),
        "created_at": raw.get("created_at"),
        "duration_sec": raw.get("duration_sec"),
        "duration": raw.get("duration"),
        "name": raw.get("name"),
        "order": raw.get("order"),
    }
    su = str(signed) if signed is not None else None
    return stable, su


def fetch_episode_selected_videos(
    base_url: str,
    token: str,
    play_id: str,
    episode_no: int,
) -> Dict[str, Any]:
    """第 2 步：拉取单集所有分镜的选中视频。"""
    path = f"/openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/selected-videos"
    status, body = _request_json(base_url, token, "GET", path)
    code, data, msg = _unwrap_api(body)
    if status >= 400 or code != 1:
        raise RuntimeError(f"获取选中视频失败 episode={episode_no} HTTP {status} code={code} msg={msg}")
    if not isinstance(data, dict):
        raise RuntimeError(f"选中视频 data 类型异常 episode={episode_no}: {type(data)}")

    shots = data.get("shots") or []
    if not isinstance(shots, list):
        shots = []

    out_shots: List[Dict[str, Any]] = []
    for s in shots:
        if not isinstance(s, dict):
            continue
        sid = s.get("shot_id")
        if sid is None:
            continue
        st_v, sig_u = _video_stable_and_signed(s.get("video"))
        out_shots.append(
            {
                "shot_id": str(sid),
                "order": s.get("order"),
                "video": st_v,
                "result_video_url": sig_u,
            }
        )

    out_shots.sort(key=lambda x: (x.get("order") is None, x.get("order"), x.get("shot_id")))
    selected_count = sum(1 for x in out_shots if isinstance(x.get("video"), dict))
    return {
        "episode_no": episode_no,
        "shot_count": len(out_shots),
        "selected_video_count": selected_count,
        "shots": out_shots,
    }


def build_snapshot(base_url: str, token: str, play_id: str) -> Dict[str, Any]:
    """聚合全剧各集分镜选中视频，形成可落盘快照。"""
    episodes = fetch_episodes(base_url, token, play_id)
    items: List[Dict[str, Any]] = []
    for ep in episodes:
        items.append(fetch_episode_selected_videos(base_url, token, play_id, ep))
    return {
        "schema_version": 2,
        "play_id": str(play_id),
        "fetched_at": _utc_iso_now(),
        "episode_count": len(items),
        "episodes": items,
    }


def _episode_map(snapshot: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    episodes = snapshot.get("episodes") or []
    out: Dict[str, Dict[str, Any]] = {}
    if isinstance(episodes, list):
        for ep in episodes:
            if isinstance(ep, dict) and ep.get("episode_no") is not None:
                out[str(ep["episode_no"])] = ep
    return out


def _shot_map(ep: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    shots = ep.get("shots") or []
    out: Dict[str, Dict[str, Any]] = {}
    if isinstance(shots, list):
        for s in shots:
            if isinstance(s, dict) and s.get("shot_id") is not None:
                out[str(s["shot_id"])] = s
    return out


def diff_snapshots(old: Optional[Dict[str, Any]], new: Dict[str, Any]) -> Dict[str, Any]:
    """
    对比两次快照，产出结构化变更说明。
    当 old 为 None（首次）时，返回 {"initial": True, ...}。
    """
    if old is None:
        return {
            "initial": True,
            "play_id": new.get("play_id"),
            "episode_count": new.get("episode_count", 0),
        }

    old_eps = _episode_map(old)
    new_eps = _episode_map(new)
    old_ids = set(old_eps.keys())
    new_ids = set(new_eps.keys())

    changes: Dict[str, Any] = {
        "initial": False,
        "play_id": new.get("play_id"),
        "episodes_added": sorted(new_ids - old_ids, key=lambda x: int(x)),
        "episodes_removed": sorted(old_ids - new_ids, key=lambda x: int(x)),
        "episodes_modified": [],
    }

    for ep_id in sorted(old_ids & new_ids, key=lambda x: int(x)):
        o_ep = old_eps[ep_id]
        n_ep = new_eps[ep_id]
        ep_changes: Dict[str, Any] = {}

        if o_ep.get("shot_count") != n_ep.get("shot_count"):
            ep_changes["shot_count"] = {"before": o_ep.get("shot_count"), "after": n_ep.get("shot_count")}
        if o_ep.get("selected_video_count") != n_ep.get("selected_video_count"):
            ep_changes["selected_video_count"] = {
                "before": o_ep.get("selected_video_count"),
                "after": n_ep.get("selected_video_count"),
            }

        o_shots = _shot_map(o_ep)
        n_shots = _shot_map(n_ep)
        o_sids = set(o_shots.keys())
        n_sids = set(n_shots.keys())

        shot_added = sorted(n_sids - o_sids)
        shot_removed = sorted(o_sids - n_sids)
        if shot_added:
            ep_changes["shots_added"] = shot_added
            add_media: List[Dict[str, Any]] = []
            for sid in shot_added:
                sh = n_shots.get(sid) or {}
                vid = sh.get("video") if isinstance(sh.get("video"), dict) else None
                add_media.append(
                    {
                        "shot_id": sid,
                        "after_video_id": vid.get("id") if vid else None,
                        "after_result_video_url": sh.get("result_video_url"),
                    }
                )
            ep_changes["shots_added_media"] = add_media
        if shot_removed:
            ep_changes["shots_removed"] = shot_removed
            rem_media: List[Dict[str, Any]] = []
            for sid in shot_removed:
                sh = o_shots.get(sid) or {}
                vid = sh.get("video") if isinstance(sh.get("video"), dict) else None
                rem_media.append(
                    {
                        "shot_id": sid,
                        "before_video_id": vid.get("id") if vid else None,
                        "before_result_video_url": sh.get("result_video_url"),
                    }
                )
            ep_changes["shots_removed_media"] = rem_media

        shot_changed: List[Dict[str, Any]] = []
        for sid in sorted(o_sids & n_sids):
            o_s = o_shots[sid]
            n_s = n_shots[sid]
            one: Dict[str, Any] = {}
            if o_s.get("order") != n_s.get("order"):
                one["order"] = {"before": o_s.get("order"), "after": n_s.get("order")}
            if _video_dict_for_compare(o_s.get("video")) != _video_dict_for_compare(n_s.get("video")):
                ov = o_s.get("video") if isinstance(o_s.get("video"), dict) else None
                nv = n_s.get("video") if isinstance(n_s.get("video"), dict) else None
                one["video_changed"] = {
                    "before_id": ov.get("id") if ov else None,
                    "after_id": nv.get("id") if nv else None,
                    "before_result_video_path": ov.get("result_video_path") if ov else None,
                    "after_result_video_path": nv.get("result_video_path") if nv else None,
                    "before_status": ov.get("status") if ov else None,
                    "after_status": nv.get("status") if nv else None,
                    "before_result_video_url": o_s.get("result_video_url"),
                    "after_result_video_url": n_s.get("result_video_url"),
                }
            if one:
                shot_changed.append({"shot_id": sid, "changes": one})

        if shot_changed:
            ep_changes["shots_modified"] = shot_changed

        if ep_changes:
            changes["episodes_modified"].append({"episode_no": int(ep_id), "changes": ep_changes})

    return changes


def has_meaningful_change(diff: Dict[str, Any]) -> bool:
    if diff.get("initial"):
        return False
    if diff.get("episodes_added") or diff.get("episodes_removed"):
        return True
    if diff.get("episodes_modified"):
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
        description="拉取全剧分镜选中视频快照，写入本地并对比上次结果",
    )
    parser.add_argument("play_id", help="剧目（项目）ID")
    parser.add_argument(
        "--data-dir",
        default=os.environ.get("IDRAMA_DATA_DIR", "./project_data"),
        help="数据总目录，其下每个剧目一个子目录（默认 ./project_data 或环境变量 IDRAMA_DATA_DIR）",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("IDRAMA_BASE_URL", "https://idrama.lingban.cn"),
        help="API 基地址（不含路径前缀，默认读 IDRAMA_BASE_URL）",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("IDRAMA_TOKEN", ""),
        help="Bearer Token（默认读环境变量 IDRAMA_TOKEN）",
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
    snapshot_path = os.path.join(project_dir, "storyboard_selected_videos.json")

    try:
        new_snap = build_snapshot(args.base_url, token, play_id)
    except Exception:
        logger.exception("拉取分镜选中视频快照失败 play_id=%s", play_id)
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
