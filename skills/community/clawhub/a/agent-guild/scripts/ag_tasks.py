#!/usr/bin/env python3
"""显式选择、会话所有权和不可变上下文快照组成的本地任务包引擎。"""

import argparse
import copy
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
import sys
import tempfile
import unicodedata
from datetime import datetime
from pathlib import Path


SCHEMA = 1
TASK_ID = re.compile(r"[0-9]{8}-[0-9a-f]{12}\Z")
SNAPSHOT = re.compile(r"r([0-9]{8,16})-[0-9a-f]{12}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
LIST_ID = re.compile(r"[0-9a-f]{32}\Z")
RESERVED = {"CON", "PRN", "AUX", "NUL", *["COM" + str(i) for i in range(1, 10)],
            *["LPT" + str(i) for i in range(1, 10)]}
STATUSES = ("active", "blocked", "waiting", "closed")
META_KEYS = {
    "schema_version", "id", "directory", "title", "project", "summary",
    "status", "revision", "created_at", "updated_at", "snapshot",
    "snapshot_revision", "owners", "sessions", "closure", "references", "pin", "hold",
}
USAGE = [
    "task create --title TITLE --project PROJECT --session SID --agent NAME [--summary TEXT] < context.md",
    "task list --session SID --agent NAME [--project PROJECT] [--archive]",
    "task resume --session SID --agent NAME (--list LIST_ID --number N | --id TASK_ID) [--handover | --collaborate]",
    "task checkpoint --id TASK_ID --session SID --agent NAME --expected-revision N [--status active|blocked|waiting] [--title TITLE] [--project PROJECT] [--summary TEXT] [--ref TASK_ID ...] [--clear-refs] [--pin | --unpin] [--hold | --unhold] < context.md",
    "task attach --id TASK_ID --session SID --agent NAME --expected-revision N --file ABS [--name SAFE]",
    "task release --id TASK_ID --session SID --agent NAME --expected-revision N",
    "task close --id TASK_ID --session SID --agent NAME --expected-revision N --evidence TEXT",
    "task reopen --id TASK_ID --session SID --agent NAME --expected-revision N",
]


class TaskError(Exception):
    def __init__(self, code, message, exit_code=1, **details):
        super().__init__(message)
        self.code = code
        self.exit_code = exit_code
        self.details = details


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise TaskError("usage", "参数错误：" + message, 2)


def _require(condition, message, code="invalid_data"):
    if not condition:
        raise TaskError(code, message)


def _case_key(value):
    return unicodedata.normalize("NFC", value).casefold()


def _keys(value, keys, label):
    _require(type(value) is dict and set(value) == set(keys), label + " 字段不合法")


def _integer(value, label, minimum=1):
    _require(type(value) is int and minimum <= value < 10 ** 16, label + " 必须是合法整数")
    return value


def _text(value, label, limit, empty=False, multiline=False):
    _require(type(value) is str and len(value) <= limit, label + " 类型或长度不合法")
    _require(empty or bool(value.strip()), label + " 不能为空")
    _require(not any(unicodedata.category(c).startswith("C") and
                     not (multiline and c in "\n\r\t") for c in value), label + " 含控制字符")
    return value


def _identifier(value, label):
    _require(type(value) is str and 1 <= len(value) <= 128 and
             value == unicodedata.normalize("NFC", value) and value[0].isalnum() and
             all(c.isalnum() or c in "_-" for c in value), label + " 必须是安全且非空的标识符")
    _require(len(value.encode("utf-8")) <= 200, label + " 的 UTF-8 文件名过长")
    _require(value.upper() not in RESERVED, label + " 是系统保留名称")
    return value


def _task_id(value):
    _require(type(value) is str and TASK_ID.fullmatch(value), "任务 ID 不合法")
    try:
        datetime.strptime(value[:8], "%Y%m%d")
    except ValueError:
        raise TaskError("invalid_data", "任务 ID 日期不合法")
    return value


def _timestamp(value):
    _require(type(value) is str, "时间戳类型不合法")
    try:
        stamp = datetime.fromisoformat(value)
    except ValueError:
        raise TaskError("invalid_data", "时间戳不合法")
    _require(stamp.tzinfo is not None, "时间戳必须包含时区")


def _identity(value):
    _keys(value, ("host", "session", "agent"), "会话身份")
    for key in ("host", "session", "agent"):
        _identifier(value[key], key)
    _require(_case_key(value["session"]) != _case_key(value["agent"]), "session 必须独立于 agent 名称")
    return value


def _slug(title):
    text = unicodedata.normalize("NFC", title)
    return "".join(c if c.isalnum() or c in "_-" else "-" for c in text).strip("-_")[:20] or "task"


def _directory(value, task_id):
    _require(type(value) is str and value.startswith(task_id + "-"), "任务目录与 ID 不匹配")
    slug = value[len(task_id) + 1:]
    _require(1 <= len(slug) <= 20 and all(c.isalnum() or c in "_-" for c in slug), "任务目录名不合法")


def _filename(value):
    _require(type(value) is str and 1 <= len(value) <= 96 and value[0].isalnum() and
             value == unicodedata.normalize("NFC", value) and ".." not in value and
             not value.endswith(".") and all(c.isalnum() or c in "_.-" for c in value),
             "附件名必须是安全的单层文件名")
    _require(len(value.encode("utf-8")) <= 180, "附件名的 UTF-8 文件名过长")
    _require(value.split(".", 1)[0].upper() not in RESERVED, "附件名是系统保留名称")
    return value


def _node(path, kind=None, missing=False):
    """只检查实际节点；不使用会跟随符号链接的 exists/is_file。"""
    try:
        info = path.lstat()
    except FileNotFoundError:
        if missing:
            return None
        raise TaskError("missing_data", "任务数据缺失：" + str(path))
    _require(not stat.S_ISLNK(info.st_mode) and
             not (getattr(info, "st_file_attributes", 0) & 0x400),
             "拒绝符号链接或重解析点：" + str(path), "unsafe_path")
    _require(stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode),
             "拒绝非普通文件节点：" + str(path), "unsafe_path")
    if stat.S_ISREG(info.st_mode):
        _require(info.st_nlink == 1, "拒绝硬链接：" + str(path), "unsafe_path")
    if kind == "file":
        _require(stat.S_ISREG(info.st_mode), "需要普通文件：" + str(path), "unsafe_path")
    if kind == "dir":
        _require(stat.S_ISDIR(info.st_mode), "需要目录：" + str(path), "unsafe_path")
    return info


def _path(path, kind=None, missing=False):
    _require(path.is_absolute() and ".." not in path.parts, "需要无路径穿越的绝对路径", "unsafe_path")
    current = Path(path.anchor)
    for part in path.parts[1:-1]:
        current = current / part
        _node(current, "dir")
    return _node(path, kind, missing)


def _mkdir(path):
    if _path(path, "dir", missing=True) is None:
        path.mkdir(mode=0o700, exist_ok=True)
        _path(path, "dir")


def _read_bytes(path, limit=None):
    before = _path(path, "file")
    _require(bool(before.st_mode & 0o444), "文件没有读取权限：" + str(path), "permission_denied")
    if limit is not None:
        _require(before.st_size <= limit, "数据文件过大：" + str(path))
    descriptor = os.open(str(path), os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(descriptor, "rb") as stream:
        opened = os.fstat(stream.fileno())
        _require((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino) and
                 stat.S_ISREG(opened.st_mode) and opened.st_nlink == 1,
                 "文件读取期间发生变化", "unsafe_path")
        data = stream.read() if limit is None else stream.read(limit + 1)
        after = os.fstat(stream.fileno())
    _require((opened.st_size, opened.st_mtime_ns) == (after.st_size, after.st_mtime_ns) and
             len(data) == after.st_size, "文件读取期间发生变化", "data_changed")
    if limit is not None:
        _require(len(data) <= limit, "数据文件过大")
    return data


def _json_pairs(pairs):
    value = {}
    for key, item in pairs:
        _require(key not in value, "JSON 含重复字段")
        value[key] = item
    return value


def _read_json(path, limit=1024 * 1024):
    try:
        return json.loads(_read_bytes(path, limit).decode("utf-8"), object_pairs_hook=_json_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (ValueError, UnicodeError):
        raise TaskError("invalid_data", "JSON 损坏：" + str(path))


def _json_size(value):
    return len((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def _sync_dir(path):
    if os.name != "nt":
        descriptor = os.open(str(path), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def _write_bytes(path, data):
    _path(path, "file", missing=True)
    descriptor = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    _sync_dir(path.parent)


def _write_json(api, path, value):
    _path(path, "file", missing=True)
    api.atomic_write_json(path, value)
    descriptor = os.open(str(path), os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    _sync_dir(path.parent)


def _meta(value, directory, location=None):
    _keys(value, META_KEYS, "任务元数据")
    _require(type(value["schema_version"]) is int and value["schema_version"] == SCHEMA,
             "不支持的任务元数据版本")
    _task_id(value["id"])
    _directory(value["directory"], value["id"])
    _require(value["directory"] == directory, "任务元数据目录不匹配")
    for key in ("title", "project"):
        _text(value[key], key, 200)
    _text(value["summary"], "summary", 240, empty=True)
    _require(type(value["status"]) is str and value["status"] in STATUSES, "任务状态不合法")
    _integer(value["revision"], "revision")
    _integer(value["snapshot_revision"], "snapshot_revision")
    _require(value["snapshot_revision"] <= value["revision"], "快照版本超过任务版本")
    _require(type(value["snapshot"]) is str and SNAPSHOT.fullmatch(value["snapshot"]), "快照指针不合法")
    _require(int(SNAPSHOT.fullmatch(value["snapshot"]).group(1)) == value["snapshot_revision"],
             "快照指针与版本不匹配")
    for key in ("created_at", "updated_at"):
        _timestamp(value[key])
    for key in ("owners", "sessions"):
        _require(type(value[key]) is list, key + " 必须是列表")
        seen = set()
        for item in value[key]:
            _identity(item)
            identity = (_case_key(item["host"]), _case_key(item["session"]))
            _require(identity not in seen, key + " 存在重复会话")
            seen.add(identity)
    _require(bool(value["sessions"]), "任务必须记录创建会话")
    _require(all(owner in value["sessions"] for owner in value["owners"]), "主人不在会话记录中")
    for key in ("pin", "hold"):
        _require(type(value[key]) is bool, key + " 必须是布尔值")
    _require(type(value["references"]) is list, "references 必须是任务 ID 列表")
    references = set()
    for reference in value["references"]:
        _task_id(reference)
        _require(reference != value["id"] and reference not in references, "任务引用不能重复或引用自身")
        references.add(reference)
    if value["closure"] is not None:
        _keys(value["closure"], ("evidence", "closed_at", "by"), "完成证据")
        _text(value["closure"]["evidence"], "evidence", 10000, multiline=True)
        _timestamp(value["closure"]["closed_at"])
        _identity(value["closure"]["by"])
        _require(value["closure"]["by"] in value["sessions"], "完成会话不在会话记录中")
    if value["status"] == "closed":
        _require(not value["owners"] and value["closure"] is not None, "已关闭任务状态不一致")
    if location is not None:
        _require((location == "archive") == (value["status"] == "closed"),
                 "任务状态与 active/archive 位置不一致")
    _require(_json_size(value) <= 1024 * 1024, "任务元数据过大")
    return value


def _public(meta, location):
    return {"task_id": meta["id"], **{key: copy.deepcopy(meta[key]) for key in
            ("title", "project", "summary", "status", "revision", "created_at", "updated_at", "owners", "sessions", "references", "pin", "hold")},
            "location": location}


def _descriptor(value):
    _keys(value, ("sha256", "size"), "内容摘要")
    _require(type(value["sha256"]) is str and DIGEST.fullmatch(value["sha256"]), "内容哈希不合法")
    _integer(value["size"], "size", 0)


def _manifest(value, meta):
    _keys(value, ("schema_version", "task_id", "revision", "context", "artifacts"), "快照清单")
    _require(type(value["schema_version"]) is int and value["schema_version"] == SCHEMA, "不支持的快照版本")
    _require(type(value["task_id"]) is str and value["task_id"] == meta["id"], "快照任务 ID 不匹配")
    _integer(value["revision"], "快照 revision")
    _require(value["revision"] == meta["snapshot_revision"], "快照版本不匹配")
    _descriptor(value["context"])
    _require(type(value["artifacts"]) is list, "附件清单必须是列表")
    names = set()
    for entry in value["artifacts"]:
        _keys(entry, ("name", "path", "sha256", "size"), "附件清单项")
        _filename(entry["name"])
        _descriptor({"sha256": entry["sha256"], "size": entry["size"]})
        _require(entry["name"].casefold() not in names, "附件名称重复")
        names.add(entry["name"].casefold())
        _require(type(entry["path"]) is str and
                 entry["path"] == "artifacts/" + entry["sha256"] + "-" + entry["name"],
                 "附件路径不合法", "unsafe_path")
    _require(_json_size(value) <= 4 * 1024 * 1024, "快照清单过大")
    return value


def _hash(data):
    return {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


def _check_tree(package):
    def fail(error):
        raise error
    size = 0
    for parent, directories, files in os.walk(str(package), followlinks=False, onerror=fail):
        _path(Path(parent), "dir")
        for name in directories:
            _node(Path(parent) / name, "dir")
        for name in files:
            size += _node(Path(parent) / name, "file").st_size
    return size


class Store:
    def __init__(self, api):
        self.api = api
        central = api.CENTRAL.expanduser()
        _require(".." not in central.parts, "公会根路径不能包含路径穿越", "unsafe_path")
        self.root = Path(os.path.abspath(str(central)))
        self.host = _identifier(api.host_id(), "host")
        _mkdir(self.root)
        self.handoff = self.root / "handoff"
        _mkdir(self.handoff)
        for name in ("active", "archive"):
            _mkdir(self.handoff / name)
        self.lock = self.handoff
        _path(self.lock.with_name(".handoff.ag-lock"), "file", missing=True)
        self.recovered = []

    def catalog(self):
        """全局锁内恢复移动日志；列举只读取元数据，绝不读取正文和附件。"""
        result = {}
        for location in ("active", "archive"):
            root = self.handoff / location
            for package in sorted(root.iterdir()):
                info = _node(package)
                if stat.S_ISREG(info.st_mode):
                    continue  # 兼容旧版本的单文件归档，但不把它们当任务包。
                _require(TASK_ID.fullmatch(package.name[:21]), "未知任务包目录：" + package.name)
                data = _meta(_read_json(package / "meta.json"), package.name)
                journal = package / ".transition.json"
                if _path(journal, "file", missing=True) is not None:
                    package, data, actual_location = self.recover(package, location, data)
                else:
                    actual_location = location
                _meta(data, package.name, actual_location)
                previous = result.get(data["id"])
                if previous is not None:
                    _require(previous[0] == package, "active/archive 存在重复任务 ID")
                result[data["id"]] = (package, data, actual_location)
        return result

    def recover(self, package, location, current):
        journal = _read_json(package / ".transition.json", 3 * 1024 * 1024)
        _keys(journal, ("schema_version", "source", "destination", "before", "after"), "移动事务")
        _require(type(journal["schema_version"]) is int and journal["schema_version"] == SCHEMA,
                 "不支持的移动事务版本")
        _require(type(journal["source"]) is str and type(journal["destination"]) is str and
                 {journal["source"], journal["destination"]} == {"active", "archive"}, "移动事务方向不合法")
        before = _meta(journal["before"], package.name, journal["source"])
        after = _meta(journal["after"], package.name, journal["destination"])
        _require(after["revision"] == before["revision"] + 1, "移动事务版本不连续")
        for key in ("id", "directory", "title", "project", "summary", "created_at", "snapshot", "snapshot_revision", "references", "pin", "hold"):
            _require(before[key] == after[key], "移动事务修改了非状态数据")
        if journal["destination"] == "archive":
            _require(after["sessions"] == before["sessions"] and after["closure"] is not None and
                     after["closure"]["by"] in before["owners"], "关闭事务的会话或权限不一致")
        else:
            _require(after["status"] == "active" and len(after["owners"]) == 1 and
                     after["closure"] == before["closure"], "重开事务状态不合法")
            expected_sessions = copy.deepcopy(before["sessions"])
            if after["owners"][0] not in expected_sessions:
                expected_sessions.append(after["owners"][0])
            _require(after["sessions"] == expected_sessions, "重开事务的会话不一致")
        _require(current == before or current == after, "移动事务与现有元数据不一致")
        size = _check_tree(package)
        reserve = _json_size(after) if current != after else 0
        if location == "active" and journal["destination"] == "archive":
            reserve += size
        if reserve:
            self.capacity(reserve)
        source = self.handoff / journal["source"] / package.name
        destination = self.handoff / journal["destination"] / package.name
        if location == journal["source"]:
            _require(_path(destination, "dir", missing=True) is None, "移动目标已存在")
            os.rename(str(package), str(destination))
            _sync_dir(source.parent)
            _sync_dir(destination.parent)
            package = destination
        else:
            _require(_path(source, "dir", missing=True) is None, "移动源与目标同时存在")
        if current != after:
            _write_json(self.api, package / "meta.json", after)
        (package / ".transition.json").unlink()
        _sync_dir(package)
        self.recovered.append(after["id"])
        return package, after, journal["destination"]

    def session(self, session, agent):
        identity = _identity({"host": self.host, "session": session, "agent": agent})
        parent = self.root
        for part in ("hosts", self.host, "task-sessions"):
            parent = parent / part
            _mkdir(parent)
        path = parent / (session + ".json")
        if _path(path, "file", missing=True) is None:
            return path, {"schema_version": SCHEMA, **identity,
                          "updated_at": self.api.now_iso(), "list": None}, True
        value = _read_json(path, 8 * 1024 * 1024)
        _keys(value, ("schema_version", "host", "session", "agent", "updated_at", "list"), "会话状态")
        _require(type(value["schema_version"]) is int and value["schema_version"] == SCHEMA,
                 "不支持的会话状态版本")
        _identity({key: value[key] for key in ("host", "session", "agent")})
        _require(all(value[key] == identity[key] for key in identity), "session 已属于其他 agent 或 host", "session_conflict")
        _timestamp(value["updated_at"])
        listing = value["list"]
        if listing is not None:
            _keys(listing, ("list_id", "issued_at", "items"), "列表快照")
            _require(type(listing["list_id"]) is str and LIST_ID.fullmatch(listing["list_id"]), "列表 ID 不合法")
            _timestamp(listing["issued_at"])
            _require(type(listing["items"]) is list, "列表快照 items 类型不合法")
            seen = set()
            for number, entry in enumerate(listing["items"], 1):
                _keys(entry, ("number", "task_id", "revision", "location"), "列表快照项")
                _integer(entry["number"], "number")
                _require(entry["number"] == number, "列表快照序号不连续")
                _task_id(entry["task_id"])
                _integer(entry["revision"], "revision")
                _require(type(entry["location"]) is str and entry["location"] in ("active", "archive"), "列表任务位置不合法")
                _require(entry["task_id"] not in seen, "列表快照任务重复")
                seen.add(entry["task_id"])
        return path, value, False

    def ensure_session(self, session):
        path, value, new = session
        if new:
            _write_json(self.api, path, value)

    def session_size(self, session):
        return _json_size(session[1]) if session[2] else 0

    def budget_lock(self):
        try:
            import ag_history
        except ImportError:
            raise TaskError("capacity_unavailable", "历史容量模块不可用，拒绝写入任务数据")
        _require(callable(getattr(ag_history, "budget_lock", None)),
                 "历史容量模块缺少 budget_lock，拒绝无锁写入", "capacity_unavailable")
        return ag_history.budget_lock(self.api)

    def capacity(self, size):
        try:
            import ag_history
        except ImportError:
            raise TaskError("capacity_unavailable", "历史容量模块不可用，拒绝写入任务数据")
        try:
            ag_history.ensure_capacity(self.api, additional_bytes=size)
        except (ValueError, RuntimeError) as error:
            raise TaskError("capacity_exceeded", "历史容量检查未通过：" + str(error))

    def load_content(self, package, meta):
        _check_tree(package)
        snapshot = package / "snapshots" / meta["snapshot"]
        manifest = _manifest(_read_json(snapshot / "manifest.json", 4 * 1024 * 1024), meta)
        context = _read_bytes(snapshot / "context.md")
        _require(_hash(context) == manifest["context"], "上下文内容与清单不一致", "integrity_error")
        try:
            text = context.decode("utf-8")
        except UnicodeError:
            raise TaskError("integrity_error", "上下文不是 UTF-8 文本")
        for entry in manifest["artifacts"]:
            data = _read_bytes(package / entry["path"])
            _require(_hash(data) == {key: entry[key] for key in ("sha256", "size")},
                     "附件内容与清单不一致", "integrity_error")
        return text, manifest

    def snapshot(self, package, meta, context, artifacts):
        name = "r{:08d}-{}".format(meta["revision"], secrets.token_hex(6))
        meta["snapshot"] = name
        meta["snapshot_revision"] = meta["revision"]
        snapshot = package / "snapshots" / name
        _require(_path(snapshot, "dir", missing=True) is None, "快照 ID 冲突")
        snapshot.mkdir(mode=0o700)
        manifest = {"schema_version": SCHEMA, "task_id": meta["id"], "revision": meta["revision"],
                    "context": _hash(context.encode("utf-8")), "artifacts": artifacts}
        _manifest(manifest, meta)
        _write_bytes(snapshot / "context.md", context.encode("utf-8"))
        _write_json(self.api, snapshot / "manifest.json", manifest)
        _sync_dir(snapshot.parent)
        self.publish(package, meta)
        return manifest

    def publish(self, package, meta):
        _meta(meta, package.name if not package.name.startswith(".task-new-") else meta["directory"])
        _write_json(self.api, package / "meta.json", meta)

    def transition(self, package, before, after, source, destination):
        target = self.handoff / destination / package.name
        _require(_path(target, "dir", missing=True) is None, "移动目标已存在")
        _meta(after, package.name, destination)
        journal = {"schema_version": SCHEMA, "source": source, "destination": destination,
                   "before": before, "after": after}
        _write_json(self.api, package / ".transition.json", journal)
        # 日志发布即表示提交意图；失败后下一次任务命令在全局锁内继续向前恢复。
        try:
            os.rename(str(package), str(target))
            _sync_dir(package.parent)
            _sync_dir(target.parent)
            self.publish(target, after)
            (target / ".transition.json").unlink()
            _sync_dir(target)
        except OSError:
            raise TaskError("transaction_pending", "任务移动尚未完成；下次 task 命令将恢复，请先重新 list", task_id=before["id"])
        return target


def _parser():
    parser = Parser(prog="ag task", add_help=False, allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("create", "list", "resume", "checkpoint", "attach", "release", "close", "reopen"):
        command = commands.add_parser(name, add_help=False, allow_abbrev=False)
        command.add_argument("--session", required=True)
        command.add_argument("--agent", required=True)
        if name == "create":
            command.add_argument("--title", required=True)
            command.add_argument("--project", required=True)
            command.add_argument("--summary", default="")
        elif name == "list":
            command.add_argument("--project")
            command.add_argument("--archive", action="store_true")
        elif name == "resume":
            choice = command.add_mutually_exclusive_group(required=True)
            choice.add_argument("--id")
            choice.add_argument("--list")
            command.add_argument("--number", type=int)
            takeover = command.add_mutually_exclusive_group()
            takeover.add_argument("--handover", action="store_true")
            takeover.add_argument("--collaborate", action="store_true")
        else:
            command.add_argument("--id", required=True)
            command.add_argument("--expected-revision", type=int, required=True)
            if name == "checkpoint":
                command.add_argument("--status", choices=STATUSES[:-1])
                command.add_argument("--title")
                command.add_argument("--project")
                command.add_argument("--summary")
                command.add_argument("--ref", action="append", default=[])
                command.add_argument("--clear-refs", action="store_true")
                pin = command.add_mutually_exclusive_group()
                pin.add_argument("--pin", dest="pin", action="store_true")
                pin.add_argument("--unpin", dest="pin", action="store_false")
                hold = command.add_mutually_exclusive_group()
                hold.add_argument("--hold", dest="hold", action="store_true")
                hold.add_argument("--unhold", dest="hold", action="store_false")
                command.set_defaults(pin=None, hold=None)
            elif name == "attach":
                command.add_argument("--file", required=True)
                command.add_argument("--name")
            elif name == "close":
                command.add_argument("--evidence", required=True)
    return parser


def _result(command, package, meta, location, **extra):
    return {"ok": True, "command": command, "task": _public(meta, location),
            "package": str(package), **extra}


def _join(meta, owner):
    for item in meta["sessions"]:
        _require((_case_key(item["host"]), _case_key(item["session"])) !=
                 (_case_key(owner["host"]), _case_key(owner["session"])) or item == owner,
                 "任务中的 session 属于其他 agent 或大小写不同的同名会话", "session_conflict")
    if owner not in meta["sessions"]:
        meta["sessions"].append(copy.deepcopy(owner))


def _bump(meta, api):
    result = copy.deepcopy(meta)
    result["revision"] += 1
    result["updated_at"] = api.now_iso()
    return result


def _dispatch(store, args, context, session, catalog):
    api = store.api
    owner = {"host": store.host, "session": args.session, "agent": args.agent}
    if args.command == "create":
        title = _text(args.title, "title", 200)
        project = _text(args.project, "project", 200)
        summary = _text(args.summary, "summary", 240, empty=True)
        for _ in range(10):
            task_id = datetime.now().strftime("%Y%m%d") + "-" + secrets.token_hex(6)
            directory = task_id + "-" + _slug(title)
            if task_id not in catalog and all(_path(store.handoff / loc / directory, "dir", missing=True) is None
                                             for loc in ("active", "archive")):
                break
        else:
            raise TaskError("id_collision", "无法生成唯一任务 ID，请重试")
        stamp = api.now_iso()
        meta = {"schema_version": SCHEMA, "id": task_id, "directory": directory, "title": title,
                "project": project, "summary": summary, "status": "active", "revision": 1,
                "created_at": stamp, "updated_at": stamp, "snapshot": "r00000001-" + "0" * 12,
                "snapshot_revision": 1, "owners": [owner], "sessions": [owner], "closure": None,
                "references": [], "pin": False, "hold": False}
        store.capacity(len(context.encode("utf-8")) + _json_size(meta) + store.session_size(session) + 4096)
        store.ensure_session(session)
        temporary = Path(tempfile.mkdtemp(prefix=".task-new-", dir=str(store.handoff)))
        try:
            (temporary / "snapshots").mkdir(mode=0o700)
            (temporary / "artifacts").mkdir(mode=0o700)
            store.snapshot(temporary, meta, context, [])
            package = store.handoff / "active" / directory
            _require(_path(package, "dir", missing=True) is None, "任务目录冲突")
            os.rename(str(temporary), str(package))
            _sync_dir(package.parent)
        finally:
            if temporary.exists():
                shutil.rmtree(str(temporary))
        return _result("create", package, meta, "active")

    if args.command == "list":
        location = "archive" if args.archive else "active"
        if args.project is not None:
            _text(args.project, "project", 200)
        rows = [meta for _, meta, loc in catalog.values()
                if loc == location and (args.project is None or args.project == meta["project"])]
        rows.sort(key=lambda item: (item["updated_at"], item["id"]), reverse=True)
        items = [{"number": number, **_public(meta, location)} for number, meta in enumerate(rows, 1)]
        listing = {"list_id": secrets.token_hex(16), "issued_at": api.now_iso(),
                   "items": [{key: entry[key] for key in ("number", "task_id", "revision", "location")} for entry in items]}
        value = copy.deepcopy(session[1])
        value["list"] = listing
        value["updated_at"] = listing["issued_at"]
        _require(_json_size(value) <= 8 * 1024 * 1024, "列表快照过大，请按 project 缩小范围")
        store.capacity(_json_size(value))
        _write_json(api, session[0], value)
        return {"ok": True, "command": "list", "list_id": listing["list_id"],
                "session": args.session, "agent": args.agent, "items": items}

    chosen = None
    if args.command == "resume" and args.list is not None:
        _require(LIST_ID.fullmatch(args.list), "列表 ID 不合法")
        _integer(args.number, "number")
        listing = session[1]["list"]
        _require(listing is not None and listing["list_id"] == args.list,
                 "列表快照已过期或不属于该会话，请重新 list", "stale_list")
        _require(args.number <= len(listing["items"]), "序号不在列表中", "invalid_selection")
        chosen = listing["items"][args.number - 1]
        task_id = chosen["task_id"]
    else:
        task_id = _task_id(args.id)
        if args.command == "resume":
            _require(args.number is None, "--number 只能与 --list 一起使用", "usage")
    entry = catalog.get(task_id)
    _require(entry is not None, "所选任务不存在，请重新 list", "stale_list" if chosen else "not_found")
    package, before, location = entry
    public = _public(before, location)
    if chosen is not None and (chosen["revision"] != before["revision"] or chosen["location"] != location):
        raise TaskError("stale_list", "所选任务自列单后发生变化，请重新 list", task=public)
    if args.command != "resume":
        _integer(args.expected_revision, "expected-revision")
        if args.expected_revision != before["revision"]:
            raise TaskError("revision_conflict", "任务版本已变化，请重新 list/resume", task=public)
    _join(copy.deepcopy(before), owner)

    if args.command == "resume":
        if location != "active":
            raise TaskError("archived", "任务已归档；请显式 reopen 后再 resume", task=public)
        owners = copy.deepcopy(before["owners"])
        if args.handover:
            owners = [owner]
        elif owner not in owners:
            if owners and not args.collaborate:
                raise TaskError("busy", "任务仍由其他会话持有；需要显式 --handover 或 --collaborate", task=public)
            owners.append(owner)
        text, manifest = store.load_content(package, before)
        meta = before
        if owners != before["owners"]:
            meta = _bump(before, api)
            meta["owners"] = owners
            _join(meta, owner)
        additional = store.session_size(session) + (_json_size(meta) if meta is not before else 0)
        if additional:
            store.capacity(additional)
        store.ensure_session(session)
        if meta is not before:
            store.publish(package, meta)
        return _result("resume", package, meta, location, context=text, artifacts=manifest["artifacts"],
                       context_path=str(package / "snapshots" / meta["snapshot"] / "context.md"))

    if args.command == "reopen":
        if location != "archive":
            raise TaskError("not_archived", "只能重新打开已归档任务", task=public)
    else:
        if location != "active":
            raise TaskError("archived", "任务已归档，不能直接写入", task=public)
        if owner not in before["owners"]:
            raise TaskError("not_owner", "当前会话没有写权，请先显式 resume", task=public)
    if args.command == "reopen" and _path(package / "pack.json", "file", missing=True) is not None:
        import ag_retention
        package = ag_retention.restore_for_reopen(api, package, before)
    text, manifest = store.load_content(package, before)
    meta = _bump(before, api)

    if args.command == "checkpoint":
        for key in ("title", "project", "summary"):
            value = getattr(args, key)
            if value is not None:
                meta[key] = _text(value, key, 240 if key == "summary" else 200, empty=key == "summary")
        if args.status is not None:
            meta["status"] = args.status
        if args.clear_refs:
            meta["references"] = []
        for reference in args.ref:
            _task_id(reference)
            _require(reference != task_id, "任务不能引用自身")
            _require(reference in catalog, "引用任务不存在：" + reference, "not_found")
            if reference not in meta["references"]:
                meta["references"].append(reference)
        for key in ("pin", "hold"):
            if getattr(args, key) is not None:
                meta[key] = getattr(args, key)
        _meta(meta, package.name, location)
        store.capacity(len(text.encode("utf-8")) + len(context.encode("utf-8")) +
                       2 * _json_size(manifest) + _json_size(meta) + store.session_size(session))
        store.ensure_session(session)
        store.snapshot(package, meta, context, manifest["artifacts"])
    elif args.command == "attach":
        source = Path(args.file)
        _require(source.is_absolute(), "--file 必须是绝对路径", "unsafe_path")
        name = _filename(args.name if args.name is not None else source.name)
        _require(all(item["name"].casefold() != name.casefold() for item in manifest["artifacts"]),
                 "附件名称已存在，请使用新的 --name", "attachment_exists")
        data = _read_bytes(source)
        digest = _hash(data)
        artifact = {"name": name, "path": "artifacts/" + digest["sha256"] + "-" + name, **digest}
        artifacts = manifest["artifacts"] + [artifact]
        store.capacity(len(data) + 2 * len(text.encode("utf-8")) +
                       2 * _json_size(manifest) + _json_size(meta) + _json_size(artifact) + store.session_size(session))
        store.ensure_session(session)
        destination = package / artifact["path"]
        if _path(destination, "file", missing=True) is None:
            _write_bytes(destination, data)
        else:
            _require(_read_bytes(destination) == data, "现有附件对象损坏", "integrity_error")
        store.snapshot(package, meta, text, artifacts)
    elif args.command == "release":
        meta["owners"] = [item for item in meta["owners"] if item != owner]
        store.capacity(_json_size(meta) + store.session_size(session))
        store.ensure_session(session)
        store.publish(package, meta)
    elif args.command == "close":
        evidence = _text(args.evidence, "evidence", 10000, multiline=True)
        meta["status"] = "closed"
        meta["owners"] = []
        meta["closure"] = {"evidence": evidence, "closed_at": api.now_iso(), "by": owner}
        store.capacity(len(text.encode("utf-8")) + _json_size(manifest) + 3 * _json_size(meta) +
                       sum(item["size"] for item in manifest["artifacts"]) + store.session_size(session) + 4096)
        store.ensure_session(session)
        package = store.transition(package, before, meta, "active", "archive")
        location = "archive"
    elif args.command == "reopen":
        meta["status"] = "active"
        meta["owners"] = [owner]
        _join(meta, owner)
        store.capacity(_json_size(before) + 2 * _json_size(meta) + store.session_size(session) + 4096)
        store.ensure_session(session)
        package = store.transition(package, before, meta, "archive", "active")
        location = "active"
    return _result(args.command, package, meta, location)


def run(args, api):
    """由 ag.py 调用；所有正常/错误输出均是一条 JSON，诊断同时写 stderr。"""
    try:
        if "--help" in args or "-h" in args:
            print(json.dumps({"ok": True, "usage": USAGE}, ensure_ascii=False))
            return 0
        parsed = _parser().parse_args(args)
        _identifier(parsed.session, "session")
        _identifier(parsed.agent, "agent")
        _require(_case_key(parsed.session) != _case_key(parsed.agent), "session 必须是独立会话 ID，不能使用 agent 名称")
        context = None
        if parsed.command in ("create", "checkpoint"):
            _require(not sys.stdin.isatty(), "请通过 stdin 提供完整上下文", "missing_context")
            context = sys.stdin.read()
            _require(bool(context.strip()), "完整上下文不能为空", "missing_context")
            context.encode("utf-8")
        store = Store(api)
        with api._append_lock(store.lock):
            with store.budget_lock():
                session = store.session(parsed.session, parsed.agent)
                catalog = store.catalog()
                result = _dispatch(store, parsed, context, session, catalog)
                if store.recovered:
                    result["recovered"] = sorted(set(store.recovered))
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except TaskError as error:
        result = {"ok": False, "error": error.code, "message": str(error), **error.details}
        print(json.dumps(result, ensure_ascii=False))
        print("ag task: " + str(error), file=sys.stderr)
        return error.exit_code
    except (OSError, UnicodeError, ValueError, RuntimeError) as error:
        message = "任务数据不可访问或无效：" + str(error)
        print(json.dumps({"ok": False, "error": "storage_error", "message": message}, ensure_ascii=False))
        print("ag task: " + message, file=sys.stderr)
        return 1
