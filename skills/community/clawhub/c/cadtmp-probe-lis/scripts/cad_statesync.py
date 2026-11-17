#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad-file-reader -> lis-skill-bus 可选接线（不侵入解析核心）。

作用：
  push  : 把 cad_scan / cad_measure 等产生的 cad-file-reader/v0 契约包装成
          cad-contract/v1 并发到 lis-skill-bus（优先 skillbus_client.py，
          bus 未安装时直接写本机默认状态文件，互相同构，不报错）。
  pull  : 从 bus 拉取最近一次 cad 契约（供五件套后续技能复用，免重复解图）。

用法：
  python3 cad_statesync.py push --entry-file 输出.json --project 项目 \
          [--building 楼栋] [--floor 楼层] [--source-file 图纸.dxf] \
          [--specialty 土建] [--skill cad-file-reader]
  python3 cad_statesync.py push --detail-json 详情.json --project 项目 ...
  python3 cad_statesync.py pull --project 项目 [--building 楼栋] [--floor 楼层] \
          [--out 内容.json] [--entry-id xxx]

兼容名：--state-push / --resume 分别是 push / pull 的别名。
纯 stdlib、不联网、不读云；公司数据只落本机 SKILLBUS_STATE_DIR。
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import cad_contract as _cc  # noqa: E402
from cad_scan_cache import file_digest  # noqa: E402

DEFAULT_STATE_FILE = Path(os.environ.get(
    "SKILLBUS_STATE_DIR",
    Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills" / ".skillbus",
)) / "state.json"


def log_err(msg: str) -> None:
    print(f"[cad_statesync] {msg}", file=sys.stderr)


_BUS_HINT_BENEFITS = (
    "lis-skill-bus 未安装：本次已自动降级到本机状态文件，功能不受影响，不装也能用。好处：同一张 CAD 图只解析一次，5 个算量技能共享同一份项目状态与识图契约；完全本地、不联网、不上云。"
)
_BUS_HINT_INSTALL = (
    "一行安装（macOS/Linux）：bash install_skillbus.sh --apply；"
    "Windows：install_skillbus.cmd --apply；只复制不注册 MCP：SKIP_MCP_REG=1 bash install_skillbus.sh --apply"
)


def bus_install_hint(op: str = "") -> None:
    print(f"[cad_statesync] {_BUS_HINT_BENEFITS}（操作：{op or '自动降级'}）", file=sys.stderr)
    print(f"[cad_statesync] 安装命令：\n  {_BUS_HINT_INSTALL}", file=sys.stderr)



# --------------------------------------------------------------------------- bus 定位
def _candidate_paths() -> list[Path]:
    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    out: list[Path] = []
    for var in ("SKILLBUS_HOME", "SKILLBUS_CLIENT"):
        raw = os.environ.get(var)
        if not raw:
            continue
        p = Path(raw) if var.endswith("CLIENT") else Path(raw) / "skillbus_client.py"
        out.append(p)
    out.append(codex_home / "mcp_servers" / "lis-skill-bus" / "skillbus_client.py")
    out.append(codex_home / "skills" / "lis-skill-bus" / "skillbus_client.py")
    out.append(codex_home / "skills" / ".skillbus" / "skillbus_client.py")
    # 常见本机开发/落地副本（不断言唯一，命中第一个即可）
    patterns = (
        str(home / ".codex" / "*" / "lis-skill-bus" / "skillbus_client.py"),
    )
    for pat in patterns:
        out.extend(Path(x) for x in glob.glob(pat))
    seen: set[str] = set()
    uniq: list[Path] = []
    for p in out:
        r = str(p.resolve())
        if r not in seen:
            seen.add(r)
            uniq.append(p)
    return uniq


def _is_dev_copy(p: Path) -> bool:
    s = str(p.resolve()).replace("\\", "/")
    markers = (
        "/lis-skill-bus-step",
        "/work/lis-skill-bus",
        "/codex-dev",
        "/tmp/lis-skill-bus",
    )
    return any(m in s for m in markers)


def find_bus_client() -> Path | None:
    if os.environ.get("SKILLBUS_DISABLE") == "1":
        bus_install_hint("SKILLBUS_DISABLE=1")
        return None
    for p in _candidate_paths():
        if p.is_file():
            if _is_dev_copy(p):
                print(f"[cad_statesync] bus 命中来源：{p}（临时副本/dev，非正式安装）", file=sys.stderr)
            else:
                print(f"[cad_statesync] bus 命中来源：{p}（正式安装）", file=sys.stderr)
            return p
    bus_install_hint()
    return None


# --------------------------------------------------------------------------- 降级直写（与 bus state.json 同构）
def _project_key(project: str, building: str, floor: str) -> str:
    parts = [x for x in (project, building, floor) if x]
    return "__slash__".join(parts) if parts else "__project__"


def read_local_state() -> dict:
    if not DEFAULT_STATE_FILE.exists():
        return {"state_version": 1, "projects": {}}
    try:
        return json.loads(DEFAULT_STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"state_version": 1, "projects": {}, "_corrupted": str(DEFAULT_STATE_FILE)}


def write_local_state(state: dict) -> None:
    DEFAULT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = DEFAULT_STATE_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, DEFAULT_STATE_FILE)


def _merge_provenance(entry: dict, skill: str) -> dict:
    entry = dict(entry or {})
    prov = dict(entry.get("_provenance") or {})
    prov.update({
        "source_skill": skill,
        "schema": entry.get("schema") or "cad-contract/v1",
        "pushed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    })
    entry["_provenance"] = prov
    return entry


def push_fallback(project: str, building: str, floor: str, entry: dict, skill: str) -> dict:
    state = read_local_state()
    key = _project_key(project, building, floor)
    bucket = state.setdefault("projects", {}).setdefault(key, {})
    entry = _merge_provenance(entry, skill)
    eid = entry.get("_id")
    if eid:
        old = bucket.get(eid)
        bucket[eid] = entry if old is None else {**(old or {}), **entry}
    else:
        bucket["_last"] = {**(bucket.get("_last") or {}), **entry}
    write_local_state(state)
    return {"project_key": key, "saved": True, "degraded": True,
            "entry_id": eid or "_last", "count": len(bucket)}


def pull_fallback(project: str, building: str, floor: str) -> dict:
    state = read_local_state()
    key = _project_key(project, building, floor)
    bucket = state.get("projects", {}).get(key, {})
    picked = bucket.get("_last") or next(iter(bucket.values()), None)
    return {"project_key": key, "hit": picked is not None, "entry": picked}


# --------------------------------------------------------------------------- 包装 cad-contract/v1
def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _file_sha256(path: str | None) -> tuple[str, bool]:
    if not path:
        return "", False
    p = Path(path)
    if not p.is_file():
        return "", False
    try:
        return file_digest(p), True
    except Exception:  # noqa: BLE001
        h = hashlib.sha256()
        with p.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest(), True


def _load_v0(payload: dict) -> dict:
    """归一化到带 contract.candidates 的 cad-file-reader/v0 payload。"""
    if not isinstance(payload, dict):
        raise ValueError("契约必须是 JSON 对象")
    if payload.get("schema") == "cad-file-reader/v0" and isinstance(payload.get("contract"), dict):
        return payload
    if isinstance(payload.get("contract"), dict) and payload["contract"].get("schema") == "cad-file-reader/v0":
        wrap = dict(payload)
        wrap.setdefault("schema", "cad-file-reader/v0")
        return wrap
    # cad_scan detail JSON：追加 text_records 契约
    if payload.get("schema", "cad-scan-detail") in ("cad-scan-detail", None, "") and isinstance(payload.get("text_records"), list):
        _cc.contractize_payload(payload, concise=False)
        payload.setdefault("schema", "cad-scan-detail")
        return payload
    raise ValueError("无法识别 cad-file-reader/v0 契约（缺 contract.candidates / text_records）")


def wrap_v1(v0: dict, project: str, building: str, floor: str, zone: str, room: str,
            specialty: str, tag_source: str, source_file: str | None, skill: str,
            review_required: bool) -> dict:
    v0 = _load_v0(v0)
    errs = _cc.validate_contract_payload(v0)
    if errs:
        raise ValueError("cad-file-reader/v0 契约校验失败：" + "; ".join(errs[:5]))
    contract = v0.get("contract") or {}
    cands = contract.get("candidates") or []
    review = contract.get("review_candidates") or []
    has_review = any(r.get("confidence_tier") == "review_required" for r in review) or any(
        r.get("confidence_tier") == "review_required" for r in cands if "review_required" in str(r.get("confidence_tier")))
    if review_required or has_review:
        tier = "review_required"
    elif any(r.get("confidence_tier") == "inferred_candidate" for r in cands):
        tier = "inferred_candidate"
    else:
        tier = "confirmed_evidence"

    sha, sha_ok = _file_sha256(source_file)
    src_name = source_file or tag_source or v0.get("source_file") or ""
    if not src_name:
        mid = contract.get("source") or ""
        src_name = str(mid) if isinstance(mid, (str, Path)) else ""
    if isinstance(src_name, Path):
        src_name = str(src_name)
    if not sha_ok and v0.get("input_sha256"):
        sha = str(v0["input_sha256"])

    summary = contract.get("summary") or {}
    reason = []
    if tier == "review_required":
        reason.append("含低置信或需人工复核的候选，下游引用前需核对")
    if not src_name:
        reason.append("未提供图纸来源文件名")
    eid = f"cad:{project}:{building}:{floor}:{sha[:10] if sha else 'noloc'}"

    return {
        "_id": eid,
        "schema": "cad-contract/v1",
        "spec": "cad-file-reader/v0",
        "version": "1",
        "project_key": {
            "project": project,
            "building": building,
            "floor": floor,
            "zone": zone,
            "room": room,
            "specialty": specialty,
            "source": tag_source,
            "review_required": bool(review_required or tier == "review_required"),
            "source_evidence": {"summary": summary},
        },
        "producer": {
            "skill": skill,
            "schema": "cad-file-reader/v0",
            "produced_at": _now(),
            "final_quantity": False,
        },
        "source": {
            "file": src_name,
            "sha256": sha,
            "page": None,
            "evidence": [
                f"candidate_total={summary.get('total', 0)}",
                f"review_required={summary.get('review_required', 0)}",
                "source_schema=cad-file-reader/v0",
            ],
        },
        "contract": v0,
        "review": {"review_required": tier == "review_required", "tier": tier, "reason": reason},
    }


# --------------------------------------------------------------------------- 子命令
def _run(cmd: list[str]) -> int:
    import subprocess
    return subprocess.call(cmd)


def cmd_push(args: argparse.Namespace) -> int:
    v0: dict
    if args.entry_file:
        try:
            v0 = json.loads(Path(args.entry_file).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            log_err(f"--entry-file 读取失败：{exc}")
            return 2
    elif args.detail_json:
        try:
            detail = json.loads(Path(args.detail_json).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            log_err(f"--detail-json 读取失败：{exc}")
            return 2
        _cc.contractize_payload(detail, concise=False)
        v0 = detail
        if args.source_file:
            v0["source_file"] = args.source_file
    else:
        log_err("push 需要 --entry-file 或 --detail-json")
        return 2

    if isinstance(v0, dict) and v0.get("schema") == "cad-contract/v1":
        entry = dict(v0)
        for field, val in (("project", args.project), ("building", args.building),
                           ("floor", args.floor), ("zone", args.zone), ("room", args.room)):
            if val is not None and val != "":
                entry.setdefault("project_key", {})[field] = val
        if args.specialty:
            entry.setdefault("project_key", {})["specialty"] = args.specialty
    else:
        entry = wrap_v1(
            v0, project=args.project, building=args.building or "", floor=args.floor or "",
            zone=args.zone or "", room=args.room or "", specialty=args.specialty or "土建",
            tag_source=args.source or "file", source_file=args.source_file,
            skill=args.skill or "cad-file-reader", review_required=bool(args.review_required),
        )

    client = find_bus_client()
    tmp = SCRIPT_DIR / f".cad_statesync_push_{os.getpid()}.json"
    try:
        tmp.write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
        if client is not None:
            r = _run([sys.executable, str(client), "push",
                      "--project", args.project, "--building", args.building or "",
                      "--floor", args.floor or "", "--skill", args.skill or "cad-file-reader",
                      "--entry-file", str(tmp)])
            if r != 0:
                raise RuntimeError(f"bus 客户端退出码 {r}，已降级直写本机状态文件")
            print(f"[cad_statesync] 已推送 bus：{client}")
            return 0
        result = push_fallback(args.project, args.building or "", args.floor or "",
                               entry, args.skill or "cad-file-reader")
        print(f"[cad_statesync] bus 未安装，降级直写 {DEFAULT_STATE_FILE}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:  # noqa: BLE001
        log_err(f"推送异常，降级直写本机状态文件：{exc}")
        try:
            result = push_fallback(args.project, args.building or "", args.floor or "",
                                   entry, args.skill or "cad-file-reader")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        except Exception as exc2:  # noqa: BLE001
            log_err(f"降级也失败：{exc2}")
            return 2
    finally:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass


def cmd_pull(args: argparse.Namespace) -> int:
    client = find_bus_client()
    if client is None:
        result = pull_fallback(args.project, args.building or "", args.floor or "")
        entry = result.get("entry")
        if entry is not None and args.out:
            Path(args.out).write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
        if entry is None:
            print(json.dumps({"project_key": result["project_key"], "hit": False,
                              "reason": "无共享状态（降级：本机正常解析）"}, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"project_key": result["project_key"], "hit": True, "entry": entry},
                             ensure_ascii=False, indent=2))
        return 0

    cmd = [sys.executable, str(client), "pull", "--project", args.project,
           "--building", args.building or "", "--floor", args.floor or ""]
    if args.entry_id:
        cmd += ["--entry-id", args.entry_id]
    if args.out:
        cmd += ["--out", args.out]
    return _run(cmd)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["--state-push"]:
        argv[:1] = ["push"]
    elif argv[:1] == ["--resume"]:
        argv[:1] = ["pull"]
    ap = argparse.ArgumentParser(description="cad-file-reader 与 lis-skill-bus 的可选接线")
    ap.add_argument("command", choices=["push", "pull", "state-push", "resume"],
                    help="push/state-push 发布契约；pull/resume 拉取")
    ap.add_argument("--project", default="", help="项目标识")
    ap.add_argument("--building", default="", help="楼栋（可选）")
    ap.add_argument("--floor", default="", help="楼层（可选）")
    ap.add_argument("--zone", default="", help="分区（可选）")
    ap.add_argument("--room", default="", help="房间（可选）")
    ap.add_argument("--specialty", default="土建", help="专业（默认 土建）")
    ap.add_argument("--source", default="file", choices=["explicit", "auto", "file"],
                    help="project_key.source，默认 file")
    ap.add_argument("--skill", default="cad-file-reader", help="producer.skill 名称")
    ap.add_argument("--entry-file", default="", help="已生成的 cad-file-reader/v0 协议 JSON")
    ap.add_argument("--detail-json", default="", help="cad_scan 的 --detail-json 详情文件")
    ap.add_argument("--source-file", default="", help="原始图纸路径（用于 source.sha256）")
    ap.add_argument("--review-required", action="store_true", help="强制下游需人工复核")
    ap.add_argument("--out", default="", help="pull 输出到文件（可选）")
    ap.add_argument("--entry-id", default="", help="pull 指定 entry_id（默认 _last）")
    args = ap.parse_args(argv)

    if args.command in ("push", "state-push"):
        # 兼容 --resume 语义（拉取）不留；这里 state-push 就是 push
        return cmd_push(args)
    return cmd_pull(args)


if __name__ == "__main__":
    raise SystemExit(main())
