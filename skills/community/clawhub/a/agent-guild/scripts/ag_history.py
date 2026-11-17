#!/usr/bin/env python3
"""历史预算、只读计划与显式确认后的可恢复隔离；不执行物理清空。"""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


DEFAULT_MAX_BYTES = 1024 * 1024 * 1024
DEFAULTS = {
    "history_max_bytes": DEFAULT_MAX_BYTES,
    "history_target_bytes": 800 * 1024 * 1024,
    "history_full_days": 30,
    "history_retention_days": 180,
    "history_max_tasks": 2000,
    "history_check_interval_hours": 24,
}
MAX_ENTRIES = 100000
MAX_DEPTH = 64
MAX_ERRORS = 32
MAX_METADATA_BYTES = 256 * 1024
MAX_MANIFEST_BYTES = 4 * 1024 * 1024
MAX_BATCH = 10
PLAN_PATH = "history/plan.json"
STATE_PATH = "history/maintenance.json"
CLOSED_STATES = {"closed", "done", "completed", "abandoned", "cancelled", "canceled"}
MANUAL_CATEGORIES = {"trash", "backups", "history", "task_cache", "task_staging"}


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value):
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _link(st):
    return stat.S_ISLNK(st.st_mode) or bool(getattr(st, "st_file_attributes", 0) & 0x400)


def _root(api):
    root = Path(api.CENTRAL).expanduser().absolute()
    st = root.lstat()
    if _link(st) or not stat.S_ISDIR(st.st_mode):
        raise RuntimeError("guild 根目录必须是实际目录，不能是链接")
    return root.resolve()


def _relative(value):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError("路径必须是非空的 guild 内相对路径")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in ("", ".", "..") for p in value.split("/")):
        raise ValueError("路径不能是绝对路径或包含 . / ..")
    if any(":" in p for p in path.parts):
        raise ValueError("路径不能包含驱动器或数据流语法")
    return path


def _safe_path(root, rel, missing=True):
    current = root
    parts = _relative(rel).parts
    for index, component in enumerate(parts):
        current = current / component
        try:
            st = current.lstat()
        except FileNotFoundError:
            if missing:
                return root.joinpath(*parts)
            raise
        if _link(st):
            raise RuntimeError("拒绝链接路径: " + current.relative_to(root).as_posix())
        if index < len(parts) - 1 and not stat.S_ISDIR(st.st_mode):
            raise RuntimeError("父路径不是目录: " + current.relative_to(root).as_posix())
    return current


def _stamp(st):
    return {
        "size": st.st_size, "mtime_ns": st.st_mtime_ns,
        "ctime_ns": st.st_ctime_ns, "device": st.st_dev,
        "inode": st.st_ino, "nlink": st.st_nlink,
    }


@contextmanager
def _open_file(root, rel, expected=None):
    path = _safe_path(root, rel, missing=False)
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or _link(before):
        raise RuntimeError("不是普通文件: " + rel)
    if expected is not None and _stamp(before) != expected:
        raise RuntimeError("文件已变化，请重新生成计划: " + rel)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0)
    fd = os.open(str(path), flags)
    with os.fdopen(fd, "rb") as stream:
        if _stamp(os.fstat(stream.fileno())) != _stamp(before):
            raise RuntimeError("打开期间文件发生变化: " + rel)
        yield stream
        if _stamp(os.fstat(stream.fileno())) != _stamp(before):
            raise RuntimeError("读取期间文件发生变化: " + rel)
        after = _safe_path(root, rel, missing=False).lstat()
        if _stamp(after) != _stamp(before):
            raise RuntimeError("读取期间路径发生变化: " + rel)


def _read(root, rel, limit=MAX_METADATA_BYTES):
    with _open_file(root, rel) as stream:
        if os.fstat(stream.fileno()).st_size > limit:
            raise ValueError("元数据超过读取上限: " + rel)
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("元数据超过读取上限: " + rel)
    return data


def _read_json(root, rel, limit=MAX_METADATA_BYTES):
    raw = _read(root, rel, limit)
    data = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("元数据必须是 JSON 对象: " + rel)
    return data, hashlib.sha256(raw).hexdigest()


def _time(value):
    if not isinstance(value, str):
        raise ValueError("时间必须是带时区的 ISO 8601 字符串")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("时间必须带时区")
    return parsed.astimezone(timezone.utc)


def _now(api):
    return _time(api.now_iso())


def _config(root):
    out = dict(DEFAULTS)
    path = _safe_path(root, "RETENTION.md")
    if path.exists():
        text = _read(root, "RETENTION.md").decode("utf-8-sig")
        seen = set()
        for number, line in enumerate(text.splitlines(), 1):
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            key, sep, value = line.partition("=")
            key = key.strip()
            if key not in DEFAULTS:
                if re.match(r"^history_[a-z_]+\b", line):
                    raise ValueError("未知或无效的历史配置，第 %d 行" % number)
                continue
            value = value.strip()
            if not sep or not re.fullmatch(r"[0-9]+", value) or key in seen:
                raise ValueError("历史配置必须是唯一的非负整数: " + key)
            out[key] = int(value)
            seen.add(key)
    if not 0 < out["history_max_bytes"]:
        raise ValueError("history_max_bytes 必须大于零（默认 1 GiB，可显式调整）")
    if out["history_target_bytes"] > out["history_max_bytes"]:
        raise ValueError("history_target_bytes 不能高于 history_max_bytes")
    if out["history_full_days"] > out["history_retention_days"]:
        raise ValueError("history_full_days 不能高于 history_retention_days")
    if out["history_check_interval_hours"] == 0:
        raise ValueError("history_check_interval_hours 必须大于零")
    return out


class _Inventory:
    def __init__(self, api):
        self.api = api
        self.root = _root(api)
        self.config = _config(self.root)
        self.now = _now(api)
        self.errors = []
        self.error_count = 0
        self.reference_errors = []
        self.reference_error_count = 0
        self.entries = 0
        self.files = []
        self.inodes = {}
        self.directories = set()
        self.categories = {}
        self.tasks = {}
        self.metadata = {}
        self.task_refs = set()
        self.path_refs = set()
        self.total_bytes = 0
        self.allocated_bytes = 0
        self.duplicate_bytes = 0
        self.duplicate_files = 0
        self.scan()

    def error(self, message):
        self.error_count += 1
        if len(self.errors) < MAX_ERRORS:
            self.errors.append(str(message))

    def reference_error(self, message):
        self.reference_error_count += 1
        if len(self.reference_errors) < MAX_ERRORS:
            self.reference_errors.append(str(message))

    def children(self, rel):
        path = _safe_path(self.root, rel)
        try:
            before = path.lstat()
        except FileNotFoundError:
            return []
        if not stat.S_ISDIR(before.st_mode):
            raise RuntimeError("预期目录: " + rel)
        names = []
        with os.scandir(path) as iterator:
            for entry in iterator:
                self.entries += 1
                if self.entries > MAX_ENTRIES:
                    raise RuntimeError("历史扫描达到条目上限，计量不完整")
                names.append(entry.name)
        after = _safe_path(self.root, rel, missing=False).lstat()
        if (before.st_dev, before.st_ino, before.st_mtime_ns) != (
                after.st_dev, after.st_ino, after.st_mtime_ns):
            raise RuntimeError("扫描期间目录发生变化: " + rel)
        return sorted(names)

    def walk(self, rel, category, task=None, depth=0, optional=True):
        if depth > MAX_DEPTH:
            self.error("目录深度超过计量上限: " + rel)
            return
        if self.entries > MAX_ENTRIES:
            return
        try:
            path = _safe_path(self.root, rel)
            try:
                st = path.lstat()
            except FileNotFoundError:
                if optional:
                    return
                raise RuntimeError("扫描期间文件消失: " + rel)
            if stat.S_ISDIR(st.st_mode):
                identity = (st.st_dev, st.st_ino)
                if identity in self.directories:
                    return
                self.directories.add(identity)
                for name in self.children(rel):
                    self.walk(rel + "/" + name, category, task, depth + 1, optional=False)
                after = _safe_path(self.root, rel, missing=False).lstat()
                if (st.st_dev, st.st_ino, st.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_mtime_ns):
                    raise RuntimeError("扫描期间目录发生变化: " + rel)
                return
            if not stat.S_ISREG(st.st_mode):
                raise RuntimeError("特殊文件无法安全计量: " + rel)
            row = {"path": rel, "category": category, "stat": _stamp(st),
                   "task_id": task, "mtime": st.st_mtime}
            identity = (st.st_dev, st.st_ino)
            row["duplicate"] = identity in self.inodes
            self.files.append(row)
            if row["duplicate"]:
                self.duplicate_files += 1
                self.duplicate_bytes += st.st_size
                return
            self.inodes[identity] = row
            allocated = getattr(st, "st_blocks", (st.st_size + 511) // 512) * 512
            self.total_bytes += st.st_size
            self.allocated_bytes += allocated
            bucket = self.categories.setdefault(category, {"bytes": 0, "allocated_bytes": 0, "files": 0})
            bucket["bytes"] += st.st_size
            bucket["allocated_bytes"] += allocated
            bucket["files"] += 1
        except (OSError, RuntimeError, ValueError) as exc:
            self.error(str(exc))

    def references(self, meta, rel, required):
        containers = [meta]
        extra = meta.get("metadata")
        if isinstance(extra, dict):
            containers.append(extra)
        found = False
        for container in containers:
            for key in ("refs", "references"):
                if key not in container:
                    continue
                found = True
                refs = container[key]
                if not isinstance(refs, list):
                    self.reference_error("引用字段不是列表: " + rel)
                    continue
                for ref in refs:
                    try:
                        if isinstance(ref, str):
                            if not ref:
                                raise ValueError("空引用")
                            if "/" in ref:
                                self.path_refs.add(_relative(ref).as_posix())
                            else:
                                if "\\" in ref or ":" in ref or ref in (".", ".."):
                                    raise ValueError("无效任务引用")
                                self.task_refs.add(ref)
                        elif isinstance(ref, dict):
                            known = False
                            for field in ("task_id", "id"):
                                if field in ref:
                                    value = ref[field]
                                    if not isinstance(value, str) or not value or "/" in value or "\\" in value:
                                        raise ValueError("无效任务引用")
                                    self.task_refs.add(value)
                                    known = True
                            if "path" in ref:
                                self.path_refs.add(_relative(ref["path"]).as_posix())
                                known = True
                            if not known:
                                raise ValueError("无法识别引用")
                        else:
                            raise ValueError("无法识别引用")
                    except ValueError as exc:
                        self.reference_error(str(exc) + ": " + rel)
        if required and not found:
            self.reference_error("活跃任务未显式声明 refs/references: " + rel)

    def task(self, rel, active):
        directory = rel.rsplit("/", 1)[-1]
        try:
            meta, digest = _read_json(self.root, rel + "/meta.json", 1024 * 1024)
            self.metadata[rel + "/meta.json"] = digest
            revision = meta.get("revision")
            if type(revision) is not int or revision < 1:
                raise ValueError("任务 revision 必须是正整数: " + rel)
            task_id = meta.get("id", meta.get("task_id", directory))
            if not isinstance(task_id, str) or not task_id:
                raise ValueError("任务 id 无效: " + rel)
            if task_id != directory and not (
                    re.fullmatch(r"[0-9]{8}-[0-9a-f]{12}", task_id)
                    and directory.startswith(task_id + "-") and meta.get("directory") == directory):
                raise ValueError("任务 id 与目录不一致: " + rel)
            snapshot = meta.get("snapshot")
            if snapshot is not None and (not isinstance(snapshot, str) or not re.fullmatch(
                    r"r[0-9]{8,16}-[0-9a-f]{12}", snapshot)):
                raise ValueError("当前快照指针无效: " + rel)
            if task_id in self.tasks:
                raise ValueError("任务 id 同时存在于多个目录: " + task_id)
            held = False
            for container in (meta, meta.get("metadata", {})):
                if not isinstance(container, dict):
                    raise ValueError("任务 metadata 必须是对象: " + rel)
                for key in ("hold", "pin", "pinned"):
                    if key in container:
                        if type(container[key]) is not bool:
                            raise ValueError("保护标记必须是布尔值: " + rel)
                        held = held or container[key]
            closed_at = None
            if not active:
                if meta.get("status") not in CLOSED_STATES:
                    raise ValueError("归档任务没有封闭状态: " + rel)
                closure = meta.get("closure")
                closed_at = _time(meta.get("closed_at") or (
                    closure.get("closed_at") if isinstance(closure, dict) else None))
                if closed_at > self.now:
                    raise ValueError("任务 closed_at 在未来: " + rel)
            packed = _safe_path(self.root, rel + "/pack.json").exists()
            if packed:
                if active:
                    raise ValueError("活跃任务包含未恢复的压缩现场: " + rel)
                import ag_retention
                ag_retention.verify_compacted_metadata(self.api, self.root / rel, meta)
            self.tasks[task_id] = {"id": task_id, "path": rel, "active": active,
                                   "revision": revision, "closed_at": closed_at,
                                   "held": held, "snapshot": snapshot, "metadata_sha256": digest,
                                   "packed": packed}
            self.references(meta, rel, active or held)
            if _safe_path(self.root, rel + "/.transition.json").exists():
                self.reference_error("任务移动事务尚未完成: " + rel)
            return task_id
        except (OSError, RuntimeError, ValueError) as exc:
            self.reference_error(str(exc))
            if active:
                self.error("活跃现场与历史无法安全区分: " + str(exc))
            return None

    def active_artifacts(self, rel, task):
        current = self.tasks[task]["snapshot"] if task else None
        if not current:
            if task is None:
                self.walk(rel + "/artifacts", "active_checkpoints", task)
            return
        manifest_path = rel + "/snapshots/" + current + "/manifest.json"
        try:
            manifest, digest = _read_json(self.root, manifest_path, MAX_MANIFEST_BYTES)
            self.metadata[manifest_path] = digest
            artifacts = manifest.get("artifacts")
            if manifest.get("task_id") != task or not isinstance(artifacts, list):
                raise ValueError("当前快照附件清单无效: " + manifest_path)
            needed = set()
            for item in artifacts:
                if not isinstance(item, dict):
                    raise ValueError("当前快照附件条目无效: " + manifest_path)
                path = _relative(item.get("path"))
                if len(path.parts) != 2 or path.parts[0] != "artifacts":
                    raise ValueError("当前快照附件路径无效: " + manifest_path)
                needed.add(path.parts[1])
            for name in self.children(rel + "/artifacts"):
                if name not in needed:
                    self.walk(rel + "/artifacts/" + name, "active_checkpoints", task)
                else:
                    _safe_path(self.root, rel + "/artifacts/" + name, missing=False)
        except (OSError, RuntimeError, ValueError) as exc:
            self.error(str(exc))

    def scan(self):
        try:
            for name in self.children("handoff/active"):
                rel = "handoff/active/" + name
                path = _safe_path(self.root, rel, missing=False)
                st = path.lstat()
                if not stat.S_ISDIR(st.st_mode):
                    if not name.endswith(".ag-lock"):
                        self.reference_error("活跃区存在无法识别条目: " + rel)
                    continue
                task = self.task(rel, True)
                self.walk(rel + "/checkpoints", "active_checkpoints", task)
                self.walk(rel + "/sessions", "active_checkpoints", task)
                current = self.tasks[task]["snapshot"] if task else None
                for snapshot in self.children(rel + "/snapshots"):
                    if snapshot != current:
                        self.walk(rel + "/snapshots/" + snapshot, "active_checkpoints", task)
                self.active_artifacts(rel, task)
            for name in self.children("handoff/archive"):
                rel = "handoff/archive/" + name
                path = _safe_path(self.root, rel, missing=False)
                task = None
                if stat.S_ISDIR(path.lstat().st_mode):
                    meta = _safe_path(self.root, rel + "/meta.json")
                    if meta.exists():
                        task = self.task(rel, False)
                self.walk(rel, "archived_tasks" if task else "legacy_handoff", task)
            for host in self.children("hosts"):
                self.walk("hosts/" + host + "/task-sessions", "task_cache")
            for name in self.children("handoff"):
                if name.startswith(".task-new-"):
                    self.walk("handoff/" + name, "task_staging")
            for rel, category in (
                ("messages/archive", "messages"),
                ("log", "logs"),
                ("learnings/archive", "learnings"),
                ("handoff/shared-state/archive", "legacy_handoff"),
                (".trash", "trash"),
                ("backups", "backups"),
                ("history", "history"),
            ):
                self.walk(rel, category)
            import ag_retention
            ag_retention.inventory_additions(self)
        except (OSError, RuntimeError, ValueError) as exc:
            self.error(str(exc))

    def reference_digest(self):
        return _digest({"metadata": self.metadata, "tasks": sorted(self.task_refs),
                        "paths": sorted(self.path_refs), "errors": self.reference_error_count})

    def task_referenced(self, task):
        return (task["id"] in self.task_refs
                or task["path"].rsplit("/", 1)[-1] in self.task_refs
                or any(ref == task["path"] or ref.startswith(task["path"] + "/")
                       or task["path"].startswith(ref + "/") for ref in self.path_refs))

    def protected(self, row):
        path = row["path"]
        if row["category"] in MANUAL_CATEGORIES:
            return "恢复副本和受管报告只允许人工检查清空"
        if row["category"] == "active_checkpoints":
            return "活跃任务的旧检查点保守保留"
        if row["stat"]["nlink"] != 1:
            return "硬链接的归属无法证明安全"
        if path.endswith(".ag-lock") or path.rsplit("/", 1)[-1].startswith(".ag-"):
            return "写入锁或未完成的原子写入"
        if path in ("log/audit.jsonl", "log/audit.log"):
            return "当前审计日志"
        if row["category"] == "logs" and not path.startswith(("log/daily/", "log/archive/")):
            return "非日常或历史轮转日志，保守保留"
        if self.reference_error_count:
            return "引用关系不完整"
        if any(path == ref or path.startswith(ref + "/") for ref in self.path_refs):
            return "被任务引用"
        task = self.tasks.get(row["task_id"])
        if task:
            if task.get("packed"):
                return "压缩任务只能通过整包保留维护操作，禁止零散隔离"
            if task["held"]:
                return "任务被 pin/hold 保护"
            if self.task_referenced(task):
                return "任务被其他任务引用"
            if path in (task["path"] + "/meta.json", task["path"] + "/context.md",
                        task["path"] + "/manifest.json", task["path"] + "/.transition.json"):
                return "任务当前摘要、清单或未完成事务"
            if task["snapshot"] and (
                    path.startswith(task["path"] + "/snapshots/" + task["snapshot"] + "/")
                    or path.startswith(task["path"] + "/artifacts/")):
                return "封闭任务当前快照和引用附件，保留以便完整重开"
        elif path.startswith("handoff/archive/") and len(PurePosixPath(path).parts) > 3:
            return "旧目录缺少可验证的任务元数据"
        return None

    def summary(self):
        cfg = self.config
        archived = sum(not item["active"] for item in self.tasks.values())
        protected_bytes = sum(row["stat"]["size"] for row in self.files
                              if not row["duplicate"] and self.protected(row))
        return {
            "schema": 1, "checked_at": self.now.isoformat(),
            "complete": self.error_count == 0, "errors": self.errors,
            "error_count": self.error_count, "total_bytes": self.total_bytes,
            "allocated_bytes": self.allocated_bytes,
            "accounting": "去重后的普通文件逻辑字节；稀疏文件按完整逻辑大小计费；不跟随链接",
            "max_bytes": cfg["history_max_bytes"], "target_bytes": cfg["history_target_bytes"],
            "over_budget": self.total_bytes > cfg["history_max_bytes"],
            "at_high_watermark": self.total_bytes >= cfg["history_max_bytes"],
            "headroom_bytes": max(0, cfg["history_max_bytes"] - self.total_bytes),
            "bytes_to_target": max(0, self.total_bytes - cfg["history_target_bytes"]),
            "file_count": len(self.inodes), "hardlink_duplicates": self.duplicate_files,
            "hardlink_duplicate_bytes": self.duplicate_bytes,
            "categories": self.categories, "archived_tasks": archived,
            "max_tasks": cfg["history_max_tasks"],
            "over_task_limit": archived > cfg["history_max_tasks"],
            "protected_bytes": protected_bytes,
            "references_complete": not self.reference_error_count,
            "reference_errors": self.reference_errors,
            "reference_error_count": self.reference_error_count,
            "config": cfg,
            "exclusions": ["messages/inbox", "handoff/inbox", "identity", "rules", "memory",
                           "skills", "tools", "活跃任务根 meta/context 和必要 artifacts"],
            "maintenance_reserve_bytes": 64 * 1024 * 1024,
            "maintenance_over_budget_bytes": max(0, self.total_bytes - cfg["history_max_bytes"]),
            "physical_release": "普通apply只隔离不释放；purge须具体计划和独立永久数据损失令牌，最多10文件/批，全部副本计费",
        }


def report(api):
    return _Inventory(api).summary()


def ensure_capacity(api, additional_bytes=0):
    """调用方须先持业务锁再持 budget_lock，覆盖本检查及随后的写入。"""
    if type(additional_bytes) is not int or additional_bytes < 0:
        raise ValueError("additional_bytes 必须是非负整数")
    try:
        status = report(api)
    except OSError as exc:
        raise RuntimeError("历史容量无法计量: " + str(exc)) from exc
    if not status["complete"]:
        raise RuntimeError("历史容量计量不完整，禁止追加: " + "; ".join(status["errors"]))
    if status["total_bytes"] + additional_bytes > status["max_bytes"]:
        raise RuntimeError(
            "历史预算不足，禁止追加（现有 %d + 新增峰值 %d > 上限 %d 字节）；"
            "请先检查 history status/plan 并人工确认释放空间，pin/hold 不能绕过预算"
            % (status["total_bytes"], additional_bytes, status["max_bytes"]))


def _eligibility(inventory):
    cfg = inventory.config
    archived = sorted((t for t in inventory.tasks.values() if not t["active"]),
                      key=lambda t: (t["closed_at"], t["id"]))
    surplus = max(0, len(archived) - cfg["history_max_tasks"])
    excess_ids = {task["id"] for task in archived[:surplus]}
    pressure = inventory.total_bytes >= cfg["history_max_bytes"]
    candidates = []
    compact = []
    for task in archived:
        age = (inventory.now - task["closed_at"]).total_seconds() / 86400
        if (age >= cfg["history_full_days"] and not task["held"]
                and not inventory.task_referenced(task) and not inventory.reference_error_count):
            if len(compact) < 100:
                compact.append({"task_id": task["id"], "revision": task["revision"],
                                "closed_at": task["closed_at"].isoformat(),
                                "suggestion": "使用 history compact-plan 生成可审核的无损压缩计划"})
    for row in inventory.files:
        if row["duplicate"] or inventory.protected(row):
            continue
        task = inventory.tasks.get(row["task_id"])
        stamp = task["closed_at"].timestamp() if task else row["mtime"]
        age = (inventory.now.timestamp() - stamp) / 86400
        reasons = []
        if age >= cfg["history_retention_days"]:
            reasons.append("retention_age")
        if task and task["id"] in excess_ids and age >= cfg["history_full_days"]:
            reasons.append("task_count")
        if pressure and age >= cfg["history_full_days"]:
            reasons.append("high_watermark")
        if reasons:
            candidates.append((stamp, row["path"], row, reasons))
    candidates.sort(key=lambda value: (value[0], value[1]))
    return candidates, compact


def _hash_file(root, row):
    digest = hashlib.sha256()
    with _open_file(root, row["path"], row["stat"]) as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _scope(root):
    st = root.lstat()
    return _digest({"root": str(root), "device": st.st_dev, "inode": st.st_ino})


def _plan(inventory, hashes=True):
    status = inventory.summary()
    candidates, compact = _eligibility(inventory)
    selected = []
    if status["complete"] and status["references_complete"]:
        for _, _, row, reasons in candidates:
            if len(selected) >= MAX_BATCH:
                break
            if reasons == ["high_watermark"] and sum(item["stat"]["size"] for item in selected) >= status["bytes_to_target"]:
                continue
            task = inventory.tasks.get(row["task_id"])
            item = {"path": row["path"], "stat": row["stat"], "reasons": reasons,
                    "task_id": row["task_id"], "revision": task["revision"] if task else None,
                    "metadata_sha256": task["metadata_sha256"] if task else None}
            if hashes:
                item["sha256"] = _hash_file(inventory.root, row)
            selected.append(item)
    plan = {
        "schema": 1, "kind": "history-quarantine-plan", "created_at": inventory.now.isoformat(),
        "scope": _scope(inventory.root), "config_digest": _digest(inventory.config),
        "reference_digest": inventory.reference_digest(),
        "status": status, "files": selected, "max_batch": MAX_BATCH,
        "eligible_files": len(candidates), "remaining_files": max(0, len(candidates) - len(selected)),
        "selected_bytes": sum(item["stat"]["size"] for item in selected),
        "compression_suggestions": compact,
        "physical_bytes_freed": 0,
        "requires_confirmation": True,
        "requires_manual_release": status["at_high_watermark"] or status["over_task_limit"],
        "notice": "仅把已确认清单中的文件复制备份后移到受管隔离区；不清空、"
                  "不减少预算占用、不删除任务摘要；最多 10 文件/批。真实释放及减少任务数必须人工处理。",
    }
    if hashes:
        plan["token"] = _digest(plan)
    return plan


def _mkdir(root, rel):
    current = root
    for component in _relative(rel).parts:
        current = current / component
        try:
            current.mkdir()
        except FileExistsError:
            pass
        st = _safe_path(root, current.relative_to(root).as_posix(), missing=False).lstat()
        if not stat.S_ISDIR(st.st_mode):
            raise RuntimeError("受管目标不是目录")


def _managed_file(root, value, required):
    value = str(value)
    candidate = Path(value)
    if candidate.is_absolute():
        try:
            value = candidate.relative_to(root).as_posix()
        except ValueError as exc:
            raise ValueError("计划文件必须在 guild 的 history/plan.json") from exc
    if _relative(value).as_posix() != PLAN_PATH:
        raise ValueError("仅支持固定 history/plan.json，避免报告无限增长")
    return _safe_path(root, PLAN_PATH, missing=not required)


@contextmanager
def budget_lock(api):
    """锁顺序：业务锁在外，预算锁在内；容量检查不再获取业务锁。"""
    root = _root(api)
    _safe_path(root, ".history-budget.ag-lock")
    with api._append_lock(root / "history-budget"):
        yield


@contextmanager
def _lock(api, root):
    _safe_path(root, ".handoff.ag-lock")
    with api._append_lock(root / "handoff"):
        with budget_lock(api):
            yield


def _write_plan(api, value):
    root = _root(api)
    _managed_file(root, value, False)
    with _lock(api, root):
        inventory = _Inventory(api)
        plan = _plan(inventory)
        text = _json(plan) + "\n"
        if len(text.encode("utf-8")) > MAX_METADATA_BYTES:
            raise RuntimeError("计划超过文件上限，拒绝写入")
        ensure_capacity(api, len(text.encode("utf-8")))
        _mkdir(root, "history")
        path = _managed_file(root, value, False)
        api._atomic_write_text(path, text)
        saved, _ = _read_json(root, PLAN_PATH)
        if saved != plan:
            raise RuntimeError("计划回读验证失败")
        return plan


def _verify_plan(inventory, plan):
    if plan.get("kind") != "history-quarantine-plan" or plan.get("schema") != 1:
        raise ValueError("不是支持的历史清理计划")
    token = plan.get("token")
    body = {key: value for key, value in plan.items() if key != "token"}
    if not isinstance(token, str) or not re.fullmatch("[0-9a-f]{64}", token) or token != _digest(body):
        raise ValueError("计划 token 校验失败，请重新生成计划")
    if plan.get("scope") != _scope(inventory.root):
        raise RuntimeError("计划不属于当前 guild")
    if plan.get("config_digest") != _digest(inventory.config):
        raise RuntimeError("保留配置已变化，请重新生成计划")
    if inventory.error_count or inventory.reference_error_count:
        raise RuntimeError("计量或引用不完整，禁止执行计划")
    if plan.get("reference_digest") != inventory.reference_digest():
        raise RuntimeError("任务引用或 revision 已变化，请重新生成计划")
    files = plan.get("files")
    if not isinstance(files, list) or not 1 <= len(files) <= MAX_BATCH:
        raise ValueError("计划必须包含 1 到 10 个文件")
    eligible = {row["path"]: row for _, _, row, _ in _eligibility(inventory)[0]}
    used = set()
    for item in files:
        if not isinstance(item, dict):
            raise ValueError("计划文件条目无效")
        rel = _relative(item.get("path")).as_posix()
        row = eligible.get(rel)
        if rel in used or not row:
            raise RuntimeError("文件重复、受保护或已不再满足条件: " + rel)
        used.add(rel)
        if row["stat"] != item.get("stat"):
            raise RuntimeError("文件状态已变化: " + rel)
        task = inventory.tasks.get(row["task_id"])
        if item.get("task_id") != row["task_id"] or item.get("revision") != (task["revision"] if task else None):
            raise RuntimeError("任务 revision 已变化: " + rel)
        if item.get("metadata_sha256") != (task["metadata_sha256"] if task else None):
            raise RuntimeError("任务元数据已变化: " + rel)
        if _hash_file(inventory.root, row) != item.get("sha256"):
            raise RuntimeError("文件内容已变化: " + rel)
    return files


def _copy_verified(root, item, target):
    _mkdir(root, str(PurePosixPath(target).parent))
    dest = _safe_path(root, target)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0)
    with _open_file(root, item["path"], item["stat"]) as source:
        fd = os.open(str(dest), flags, 0o600)
        with os.fdopen(fd, "wb") as output:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
    st = _safe_path(root, target, missing=False).lstat()
    if st.st_size != item["stat"]["size"] or _hash_file(root, {"path": target, "stat": _stamp(st)}) != item["sha256"]:
        raise RuntimeError("备份回读校验失败，原件未移动: " + item["path"])


def _apply(api, value):
    root = _root(api)
    _managed_file(root, value, True)
    with _lock(api, root):
        plan, _ = _read_json(root, PLAN_PATH)
        inventory = _Inventory(api)
        files = _verify_plan(inventory, plan)
        history_dir = _safe_path(root, "history", missing=False)
        target_device = history_dir.stat().st_dev
        if any(item["stat"]["device"] != target_device for item in files):
            raise RuntimeError("候选与受管恢复目录不在同一文件系统，拒绝非原子跨设备隔离")
        token = plan["token"]
        backup_root = "history/backups/" + token
        quarantine_root = "history/quarantine/" + token
        for rel in (backup_root, quarantine_root):
            if _safe_path(root, rel).exists():
                raise RuntimeError("此计划已有恢复数据，禁止重复执行: " + rel)
        manifest_path = backup_root + "/manifest.json"
        manifest = {"schema": 1, "status": "prepared", "plan": plan,
                    "backup_root": backup_root, "quarantine_root": quarantine_root,
                    "physical_bytes_freed": 0}
        text = _json(manifest) + "\n"
        completed = dict(manifest, status="quarantined", moved=[item["path"] for item in files])
        final_text = _json(completed) + "\n"
        if len(final_text.encode("utf-8")) > MAX_METADATA_BYTES:
            raise RuntimeError("执行清单超过元数据上限，拒绝执行")
        reserve = (sum(item["stat"]["size"] for item in files)
                   + len(text.encode("utf-8")) + len(final_text.encode("utf-8")))
        ensure_capacity(api, reserve)
        _mkdir(root, backup_root)
        _mkdir(root, quarantine_root)
        api._atomic_write_text(_safe_path(root, manifest_path), text)
        for item in files:
            _copy_verified(root, item, backup_root + "/" + item["path"])
        _verify_plan(_Inventory(api), plan)
        moved = []
        for item in files:
            source = _safe_path(root, item["path"], missing=False)
            if _hash_file(root, {"path": item["path"], "stat": item["stat"]}) != item["sha256"]:
                raise RuntimeError("隔离前文件已变化，备份保留于 " + backup_root)
            destination = quarantine_root + "/" + item["path"]
            _mkdir(root, str(PurePosixPath(destination).parent))
            dest = _safe_path(root, destination)
            if dest.exists():
                raise RuntimeError("隔离目标已存在，停止执行")
            os.rename(str(source), str(dest))
            st = _safe_path(root, destination, missing=False).lstat()
            if _hash_file(root, {"path": destination, "stat": _stamp(st)}) != item["sha256"]:
                raise RuntimeError("隔离后校验失败，请检查 " + backup_root + " 与 " + quarantine_root)
            moved.append(item["path"])
        api._atomic_write_text(_safe_path(root, manifest_path), final_text)
        saved, _ = _read_json(root, manifest_path)
        if saved != completed:
            raise RuntimeError("执行清单回读校验失败，恢复数据已保留")
        return {"schema": 1, "moved": moved, "backup_root": backup_root,
                "quarantine_root": quarantine_root, "manifest": manifest_path,
                "physical_bytes_freed": 0, "manual_release_required": True,
                "notice": "已验证备份并移入受管隔离区；空间未释放，备份与隔离原件继续计入预算。"}


def maintenance(api):
    root = _root(api)
    cfg = _config(root)
    now = _now(api)
    state = _safe_path(root, STATE_PATH)
    if state.exists():
        previous, _ = _read_json(root, STATE_PATH)
        checked = _time(previous.get("checked_at"))
        if 0 <= (now - checked).total_seconds() < cfg["history_check_interval_hours"] * 3600:
            return {"checked": False, "rate_limited": True, "previous": previous}
    with _lock(api, root):
        state = _safe_path(root, STATE_PATH)
        if state.exists():
            previous, _ = _read_json(root, STATE_PATH)
            checked = _time(previous.get("checked_at"))
            if 0 <= (now - checked).total_seconds() < cfg["history_check_interval_hours"] * 3600:
                return {"checked": False, "rate_limited": True, "previous": previous}
        inventory = _Inventory(api)
        plan = _plan(inventory, hashes=False)
        import ag_retention
        cycle_preview = ag_retention.preview_cycle(api)
        status = plan["status"]
        result = {"checked": True, "rate_limited": False, "status": status,
                  "eligible_files": plan["eligible_files"], "applied": False,
                  "cycle": cycle_preview,
                  "notice": "限频维护只检查；显式 history cycle 计划经确认后执行压缩/退役/清空循环"}
        saved = {"checked_at": now.isoformat(), "total_bytes": status["total_bytes"],
                 "complete": status["complete"], "eligible_files": plan["eligible_files"],
                 "cycle": cycle_preview}
        text = _json(saved) + "\n"
        if status["complete"] and status["total_bytes"] + len(text.encode("utf-8")) <= cfg["history_max_bytes"]:
            _mkdir(root, "history")
            api._atomic_write_text(_safe_path(root, STATE_PATH), text)
            result["state_written"] = True
        else:
            result["state_written"] = False
        return result


def run(args, api):
    args = list(args)
    try:
        command = args.pop(0) if args else "status"
        if command in ("compact-plan", "compact", "retire-plan", "retire", "restore",
                       "purge-plan", "purge", "cycle"):
            import ag_retention
            return ag_retention.run([command, *args], api)
        if command in ("status", "plan"):
            if "--json" in args:
                args.remove("--json")
            if command == "status":
                if args:
                    raise ValueError("用法: ag history status [--json]")
                value = report(api)
                print(json.dumps(value, ensure_ascii=False, indent=2))
                return 0 if value["complete"] else 1
            if not args:
                value = _plan(_Inventory(api))
            elif len(args) == 2 and args[0] == "--output":
                value = _write_plan(api, args[1])
            else:
                raise ValueError("用法: ag history plan [--json] [--output history/plan.json]")
            print(json.dumps(value, ensure_ascii=False, indent=2))
            return 0 if value["status"]["complete"] else 1
        if command == "apply":
            if "--confirm" not in args:
                raise ValueError("执行必须显式提供 --confirm，且先检查计划的具体文件清单")
            args.remove("--confirm")
            if len(args) != 2 or args[0] != "--plan":
                raise ValueError("用法: ag history apply --plan history/plan.json --confirm")
            value = _apply(api, args[1])
            print(json.dumps(value, ensure_ascii=False, indent=2))
            return 0
        raise ValueError("history 支持 status、plan、apply；物理清空需人工执行")
    except (OSError, RuntimeError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "completed": False,
                          "notice": "不会物理清空；执行中失败时请检查 history/backups 与 history/quarantine 的恢复清单"},
                         ensure_ascii=False), file=sys.stderr)
        return 1
