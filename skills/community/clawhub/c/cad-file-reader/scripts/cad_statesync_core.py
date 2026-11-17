#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad_statesync_core —— 五份 statesync 复制粘贴的共享实现（§2.4 抽共享）。

历史：cad-file-reader / zhuangshi / anzhuang / yuanlin / tujian 各有一份
~424 行近同构实现（差异只有 SKILL 名、专业名、目标 section 清单）。
本模块把公共逻辑收成一处，各技能保留薄壳（thin wrapper）传参调用。

行为不变承诺：与原 anzhuang_statesync.py 逐函数等价（2026-10-30 归一比对，
zhuangshi/anzhuang/yuanlin 三份归一化后仅 section 清单与文案不同）。

用法（薄壳侧）：
    from cad_statesync_core import run_cli
    run_cli(skill="anzhuang-suanliang", specialty="安装",
            sections=["route_segments", ...], core_sections=["circuits", ...])

纯 stdlib、不联网、不读云；公司数据只落本机 SKILLBUS_STATE_DIR / 技能状态文件。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def make_state_file() -> Path:
    return Path(os.environ.get(
        "SKILLBUS_STATE_DIR",
        Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills" / ".skillbus",
    )) / "state.json"


class Core:
    """参数化的 statesync 公共实现。"""

    def __init__(self, skill: str, specialty: str,
                 sections: list[str], core_sections: list[str]):
        self.SKILL = skill
        self.DEFAULT_SPECIALTY = specialty
        self.DEFAULT_SECTIONS = list(sections)
        self.DEFAULT_CORE_SECTIONS = list(core_sections)
        self.DEFAULT_STATE_FILE = make_state_file()
        self.SCRIPT_DIR = None  # 薄壳可注入，用于 push 临时文件
        self.log_prefix = f"[{skill} statesync]"

    def log_err(self, msg: str) -> None:
        print(f"{self.log_prefix} {msg}", file=sys.stderr)

    # ---------------------------------------------------------------- bus 定位
    def _candidate_paths(self) -> list[Path]:
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
        patterns = (
            str(home / "Documents" / "Codex" / "*" / "tan" / "work" / "lis-skill-bus" / "skillbus_client.py"),
            str(home / "Documents" / "Codex" / "*" / "*" / "lis-skill-bus" / "skillbus_client.py"),
            str(home / "Documents" / "*" / "lis-skill-bus" / "skillbus_client.py"),
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

    def _is_dev_copy(self, p: Path) -> bool:
        s = str(p.resolve()).replace("\\", "/")
        markers = ("/tan/work/", "/work/lis-skill-bus", "/lis-skill-bus-step",
                   "/Documents/Codex/")
        return any(m in s for m in markers)

    def find_bus_client(self) -> Path | None:
        if os.environ.get("SKILLBUS_DISABLE") == "1":
            return None
        for p in self._candidate_paths():
            if p.is_file():
                if self._is_dev_copy(p):
                    print(f"{self.log_prefix} bus 命中来源：{p}（临时副本/dev，非正式安装）",
                          file=sys.stderr)
                else:
                    print(f"{self.log_prefix} bus 命中来源：{p}（正式安装）", file=sys.stderr)
                return p
        return None

    # ------------------------------------------------- 降级直写（与 bus 同构）
    @staticmethod
    def _key(project: str, building: str, floor: str) -> str:
        parts = [x for x in (project, building, floor) if x]
        return "__slash__".join(parts) if parts else "__project__"

    def read_local_state(self) -> dict:
        if not self.DEFAULT_STATE_FILE.exists():
            return {"state_version": 1, "projects": {}}
        try:
            return json.loads(self.DEFAULT_STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {"state_version": 1, "projects": {},
                    "_corrupted": str(self.DEFAULT_STATE_FILE)}

    def write_local_state(self, state: dict) -> None:
        self.DEFAULT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.DEFAULT_STATE_FILE.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, self.DEFAULT_STATE_FILE)

    def wrap_entry(self, entry: dict, project: str, building: str, floor: str,
                   specialty: str, skill: str) -> dict:
        entry = dict(entry or {})
        if entry.get("schema") == "cad-contract/v1":
            pk = dict(entry.get("project_key") or {})
            for field, val in (("project", project), ("building", building),
                               ("floor", floor), ("zone", ""), ("room", "")):
                if val:
                    pk[field] = val
            if specialty:
                pk["specialty"] = specialty
            entry["project_key"] = pk
            return entry
        pk = {
            "project": project, "building": building, "floor": floor,
            "zone": "", "room": "", "specialty": specialty or self.DEFAULT_SPECIALTY,
            "source": "file", "review_required": False,
        }
        src = entry.get("source") or {}
        if isinstance(src, dict) and "file" in src:
            file_name = str(src.get("file", ""))
            sha = str(src.get("sha256", ""))
        else:
            file_name = str(entry.get("source_file") or "")
            sha = str(entry.get("input_sha256") or "")
        contract = dict(entry)
        if "qto_spec" not in contract and isinstance(entry.get("contract"), dict) \
                and entry["contract"].get("schema") == "qto-project/v1":
            contract = entry["contract"]
        wrapped = {
            "_id": f"{skill}:{project}:{building}:{floor}:{int(time.time() * 1000)}",
            "schema": "cad-contract/v1",
            "spec": "qto-project/v1",
            "version": "1",
            "project_key": pk,
            "producer": {
                "skill": skill,
                "schema": "qto-project/v1",
                "produced_at": _now(),
                "final_quantity": False,
            },
            "source": {"file": file_name, "sha256": sha, "page": None,
                       "evidence": [f"producer={skill}"]},
            "contract": contract,
            "review": {"review_required": False, "tier": "confirmed_evidence", "reason": []},
        }
        # 顶层同步 contract_id/provenance/单位：下游 guard 与 site/算量只读顶层，
        # 不能要求每个技能再解一层 contract 外壳。
        inner = contract if isinstance(contract, dict) else {}
        nested = inner.get("contract") if isinstance(inner.get("contract"), dict) else {}
        for key in ("contract_id", "provenance", "coordinate_unit", "unit_scale"):
            val = inner.get(key)
            if val is None:
                val = nested.get(key)
            if val is None:
                val = entry.get(key)
            if val is not None:
                wrapped[key] = val
        return wrapped

    def push_fallback(self, project: str, building: str, floor: str,
                      entry: dict, skill: str) -> dict:
        state = self.read_local_state()
        key = self._key(project, building, floor)
        bucket = state.setdefault("projects", {}).setdefault(key, {})
        entry = dict(entry or {})
        prov = dict(entry.get("_provenance") or {})
        prov.update({"source_skill": skill, "pushed_at": _now()})
        entry["_provenance"] = prov
        eid = entry.get("_id")
        if eid:
            old = bucket.get(eid)
            bucket[eid] = entry if old is None else {**(old or {}), **entry}
        else:
            entry = {**(bucket.get("_last") or {}), **entry}
            bucket["_last"] = entry
        self.write_local_state(state)
        return {"project_key": key, "saved": True, "degraded": True,
                "entry_id": eid or "_last", "count": len(bucket)}

    def pull_fallback(self, project: str, building: str, floor: str) -> dict:
        state = self.read_local_state()
        key = self._key(project, building, floor)
        bucket = state.get("projects", {}).get(key, {})
        picked = bucket.get("_last") or next(iter(bucket.values()), None)
        return {"project_key": key, "hit": picked is not None, "entry": picked}

    # ------------------------------------------------------------- 命中判定
    @staticmethod
    def _section_items(contract: dict, section: str):
        if not isinstance(contract, dict):
            return None
        direct = contract.get(section)
        if isinstance(direct, list):
            return direct
        nested = contract.get("sections")
        if isinstance(nested, dict):
            val = nested.get(section)
            if isinstance(val, list):
                return val
        return None

    def match_sections(self, entry: dict, targets: list[str]) -> dict:
        c = (entry or {}).get("contract") or {}
        matched, missing, empty, review_flagged = [], [], [], []
        for s in targets:
            items = self._section_items(c, s)
            if items is None:
                missing.append(s)
            elif len(items) == 0:
                empty.append(s)
            else:
                matched.append(s)
                if any(not isinstance(it, dict) for it in items):
                    continue
                if any(str(it.get("confidence_tier")) == "review_required"
                       or "review_required" in str(it.get("review", ""))
                       or bool(it.get("review_required"))
                       for it in items if isinstance(it, dict)):
                    review_flagged.append(s)
        return {"matched": matched, "missing": missing, "empty": empty,
                "review_flagged": review_flagged,
                "candidate_only": True, "usable": bool(matched)}

    @staticmethod
    def _unique(items):
        seen = set()
        out = []
        for x in items:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    def apply_core_rule(self, entry, mm, core_targets):
        core = self.match_sections(entry, core_targets)
        missing_core = [s for s in core_targets
                        if s in core["missing"] or s in core["empty"]]
        core_matched = core["matched"]
        if not core_matched:
            return False, core_matched, missing_core, \
                self._unique(mm["review_flagged"] + missing_core)
        return True, core_matched, missing_core, list(mm["review_flagged"])

    # --------------------------------------------------------------- 子命令
    def cmd_push(self, args: argparse.Namespace) -> int:
        if not args.entry_file:
            self.log_err("push 需要 --entry-file")
            return 2
        try:
            payload = json.loads(Path(args.entry_file).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.log_err(f"--entry-file 读取失败：{exc}")
            return 2
        entry = self.wrap_entry(payload, args.project, args.building, args.floor,
                                args.specialty, args.skill)
        client = self.find_bus_client()
        script_dir = self.SCRIPT_DIR or Path(args.entry_file).resolve().parent
        tmp = script_dir / f".{self.SKILL}_push_{os.getpid()}.json"
        try:
            tmp.write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
            if client is not None:
                r = subprocess.run([sys.executable, str(client), "push",
                                    "--project", args.project, "--building", args.building,
                                    "--floor", args.floor, "--skill", args.skill,
                                    "--entry-file", str(tmp)],
                                   capture_output=True, text=True)
                if r.returncode != 0:
                    raise RuntimeError(
                        f"bus 客户端退出码 {r.returncode}：{r.stderr.strip()[:200]}")
                print(f"{self.log_prefix} 已推送 bus：{client}")
                try:
                    print(r.stdout.strip())
                except Exception:
                    pass
                return 0
            result = self.push_fallback(args.project, args.building, args.floor,
                                        entry, args.skill)
            print(f"{self.log_prefix} bus 未安装，降级直写 {self.DEFAULT_STATE_FILE}")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        except Exception as exc:  # noqa: BLE001
            self.log_err(f"推送异常，降级直写本机状态文件：{exc}")
            try:
                result = self.push_fallback(args.project, args.building, args.floor,
                                            entry, args.skill)
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return 0
            except Exception as exc2:  # noqa: BLE001
                self.log_err(f"降级也失败：{exc2}")
                return 2
        finally:
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass

    def cmd_pull(self, args: argparse.Namespace) -> int:
        client = self.find_bus_client()
        if client is None:
            result = self.pull_fallback(args.project, args.building, args.floor)
        else:
            cmd = [sys.executable, str(client), "pull", "--project", args.project,
                   "--building", args.building, "--floor", args.floor]
            if args.entry_id:
                cmd += ["--entry-id", args.entry_id]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                print(json.dumps({"hit": False,
                                  "reason": f"bus pull 失败 rc={r.returncode}",
                                  "stderr": r.stderr[-300:]},
                                 ensure_ascii=False, indent=2))
                return 0
            try:
                result = json.loads(r.stdout)
            except json.JSONDecodeError:
                print(json.dumps({"hit": False, "reason": "bus pull 输出无法解析"},
                                 ensure_ascii=False, indent=2))
                return 0
        entry = result.get("entry")
        if not result.get("hit") or entry is None:
            print(json.dumps({"hit": False,
                              "reason": result.get("reason", "无共享状态（未命中）"),
                              "project_key": result.get("project_key", "")},
                             ensure_ascii=False, indent=2))
            return 0
        schema = entry.get("schema")
        if schema != "cad-contract/v1":
            print(json.dumps({"hit": True, "usable": False,
                              "reason": f"schema={schema!r} 不是 cad-contract/v1"},
                             ensure_ascii=False, indent=2))
            return 0
        mm = self.match_sections(entry, args.target_sections)
        usable = mm["usable"]
        review_flagged = list(mm["review_flagged"])
        core_matched, core_missing = [], []
        if args.require_all and mm["missing"]:
            usable = False
        if args.require_core:
            core_ok, core_matched, core_missing, review_flagged = \
                self.apply_core_rule(entry, mm, args.core_sections)
            if not core_ok:
                usable = False
        core_fields = {}
        if args.require_core:
            core_fields = {"core_sections": args.core_sections,
                           "core_matched": core_matched,
                           "core_missing_core": core_missing}
        if not usable:
            reason = "缺必选核心 section" if core_missing else "目标 section 字段未命中"
            print(json.dumps({"hit": True, "usable": False, "reason": reason,
                              "target_sections": args.target_sections,
                              "matched": mm["matched"], "missing": mm["missing"],
                              "empty": mm["empty"],
                              "review_flagged": review_flagged,
                              "candidate_only": True, **core_fields},
                             ensure_ascii=False, indent=2))
            return 0
        if args.out:
            Path(args.out).write_text(
                json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
        if args.out_dir:
            od = Path(args.out_dir)
            od.mkdir(parents=True, exist_ok=True)
            (od / "cad-contract.json").write_text(
                json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
            (od / "bus-pull-status.json").write_text(json.dumps({
                "hit": True, "usable": True, "schema": schema,
                "matched": mm["matched"], "missing": mm["missing"],
                "review_flagged": review_flagged, "candidate_only": True, **core_fields,
                "project_key": entry.get("project_key", {})},
                ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"hit": True, "usable": True, "schema": schema,
                          "matched": mm["matched"], "missing": mm["missing"],
                          "empty": mm["empty"], "review_flagged": review_flagged,
                          "candidate_only": True, **core_fields,
                          "project_key": entry.get("project_key", {})},
                         ensure_ascii=False, indent=2))
        return 0

    # ---------------------------------------------------------------- CLI
    def build_parser(self) -> argparse.ArgumentParser:
        ap = argparse.ArgumentParser(
            description=f"{self.SKILL} 与 lis-skill-bus 契约接线")
        ap.add_argument("command", choices=["push", "pull"])
        ap.add_argument("--project", required=True, help="项目标识")
        ap.add_argument("--building", default="", help="楼栋（可选）")
        ap.add_argument("--floor", default="", help="楼层（可选）")
        ap.add_argument("--specialty", default=self.DEFAULT_SPECIALTY,
                        help=f"专业（默认 {self.DEFAULT_SPECIALTY}）")
        ap.add_argument("--skill", default=self.SKILL, help="producer.skill 名称")
        ap.add_argument("--entry-file", default="", help="push 用的本技能输出 JSON")
        ap.add_argument("--target-sections", default=",".join(self.DEFAULT_SECTIONS),
                        help="命中判定的 cad contract section 字段（逗号分隔）")
        ap.add_argument("--out", default="", help="pull 命中时写入的从契约文件")
        ap.add_argument("--out-dir", default="",
                        help="pull 命中时写入 cad-contract.json + bus-pull-status.json 的目录")
        ap.add_argument("--entry-id", default="", help="pull 指定 entry_id（默认最近一条）")
        ap.add_argument("--require-all", action="store_true",
                        help="所有 target sections 都命中才算 usable")
        ap.add_argument("--require-core", action="store_true",
                        help="必选核心 section 至少一命中且非空才算 usable（默认关闭，保持宽松）")
        ap.add_argument("--core-sections", default=",".join(self.DEFAULT_CORE_SECTIONS),
                        help="必选核心 section（逗号分隔，默认："
                             + ",".join(self.DEFAULT_CORE_SECTIONS) + "）")
        return ap

    def run_cli(self, argv: list[str] | None = None) -> int:
        args = self.build_parser().parse_args(argv)
        args.target_sections = [s.strip() for s in (args.target_sections or "").split(",")
                                if s.strip()]
        args.core_sections = [s.strip() for s in (args.core_sections or "").split(",")
                              if s.strip()]
        if args.command == "push":
            return self.cmd_push(args)
        return self.cmd_pull(args)


def run_cli(skill: str, specialty: str, sections: list[str],
            core_sections: list[str], argv: list[str] | None = None,
            script_dir: Path | None = None) -> int:
    """薄壳入口：构造 Core 并跑 CLI。"""
    core = Core(skill, specialty, sections, core_sections)
    core.SCRIPT_DIR = script_dir
    return core.run_cli(argv)
