#!/usr/bin/env python3
"""有界、显式批准的无损压缩、整包退役和受管恢复副本清空。"""

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import sys
import zipfile
from contextlib import contextmanager
from pathlib import Path, PurePosixPath

import ag_history as H
import ag_tasks as T


MAINTENANCE_RESERVE_BYTES = 64 * 1024 * 1024
MAX_CONTROL_BYTES = 8 * 1024 * 1024
MAX_FILES = 10000
MAX_EXPANDED_BYTES = 8 * 1024 * 1024 * 1024
MAX_MEMBER_BYTES = 2 * 1024 * 1024 * 1024
MAX_CONTEXT_BYTES = 16 * 1024 * 1024
SUMMARY_BYTES = 64 * 1024  # 逐字摘要总预算：文首前缀与文末后缀各占一半，避免收据副本放大
CHUNK = 1024 * 1024
MAX_BATCH = 10
PLAN_PATH = "history/retention-plan.json"
CYCLE_PATH = "history/cycle.json"
PACK = "pack.json"
SUMMARY = "summary.json"
PAYLOAD = "payload.zip"
RESTORE_TMP = ".retention-restore.tmp"
SIDECARS = {PACK, SUMMARY, PAYLOAD}
TERMINAL_RECEIPT_STATES = ("purged", "restored")
HEX = re.compile(r"[0-9a-f]{64}\Z")


class NoProgress(RuntimeError):
    pass


def _require(condition, message):
    if not condition:
        raise RuntimeError(message)


def _json(value):
    return H._json(value) + "\n"


def _bytes(value):
    return _json(value).encode("utf-8")


def _safe(root, rel, missing=False):
    path = H._safe_path(root, rel, missing=missing)
    if path.exists():
        info = path.lstat()
        _require(stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode), "拒绝特殊文件: " + rel)
        if stat.S_ISREG(info.st_mode):
            _require(info.st_nlink == 1, "拒绝硬链接: " + rel)
    return path


def _read(root, rel, limit=MAX_CONTROL_BYTES):
    path = _safe(root, rel)
    _require(bool(path.lstat().st_mode & 0o444), "文件无读取权限: " + rel)
    return H._read(root, rel, limit)


def _read_json(root, rel, limit=MAX_CONTROL_BYTES):
    raw = _read(root, rel, limit)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=T._json_pairs,
                           parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (ValueError, UnicodeError, T.TaskError) as exc:
        raise ValueError("JSON 无效: " + rel) from exc
    _require(isinstance(value, dict), "JSON 必须是对象: " + rel)
    return value


def _file_hash(root, rel, expected=None):
    path = _safe(root, rel)
    info = path.lstat()
    _require(stat.S_ISREG(info.st_mode) and bool(info.st_mode & 0o444), "文件不可读: " + rel)
    digest = hashlib.sha256()
    with H._open_file(root, rel, expected) as stream:
        for data in iter(lambda: stream.read(CHUNK), b""):
            digest.update(data)
    return digest.hexdigest()


def _tree(root, rel, hashes=True):
    """只遍历显式选中的包；不跟随链接，限制深度、文件数和展开大小。"""
    base = _safe(root, rel)
    _require(stat.S_ISDIR(base.lstat().st_mode), "受管包不是目录: " + rel)
    files, directories = [], []
    total = 0

    def visit(folder, depth):
        nonlocal total
        _require(depth <= H.MAX_DEPTH, "受管包目录过深")
        path = _safe(root, folder)
        before = path.lstat()
        _require(bool(before.st_mode & 0o500), "目录不可访问: " + folder)
        with os.scandir(path) as iterator:
            names = sorted(entry.name for entry in iterator)
        for name in names:
            child = folder + "/" + name
            item = _safe(root, child)
            info = item.lstat()
            local = item.relative_to(base).as_posix()
            H._relative(local)
            if stat.S_ISDIR(info.st_mode):
                directories.append(local)
                _require(len(directories) <= MAX_FILES, "目录数量超过上限")
                visit(child, depth + 1)
            else:
                total += info.st_size
                _require(info.st_size <= MAX_MEMBER_BYTES and total <= MAX_EXPANDED_BYTES,
                         "包大小超过安全展开上限")
                row = {"path": local, "size": info.st_size, "stat": H._stamp(info)}
                if hashes:
                    row["sha256"] = _file_hash(root, child, row["stat"])
                files.append(row)
                _require(len(files) <= MAX_FILES, "包文件数量超过上限")
        after = _safe(root, folder).lstat()
        _require((before.st_dev, before.st_ino, before.st_mtime_ns) ==
                 (after.st_dev, after.st_ino, after.st_mtime_ns), "目录在扫描期间变化: " + folder)

    visit(rel, 0)
    return sorted(files, key=lambda row: row["path"]), sorted(directories)


def _rows(rows):
    _require(isinstance(rows, list) and 1 <= len(rows) <= MAX_FILES, "文件清单数量无效")
    seen, total = set(), 0
    for row in rows:
        _require(isinstance(row, dict), "文件清单条目无效")
        name = H._relative(row.get("path")).as_posix()
        _require(name not in seen and not any(name.startswith(p + "/") or p.startswith(name + "/")
                                             for p in seen), "文件清单路径重复或冲突")
        seen.add(name)
        size = row.get("size")
        _require(type(size) is int and 0 <= size <= MAX_MEMBER_BYTES, "文件清单大小无效")
        total += size
        _require(isinstance(row.get("sha256"), str) and HEX.fullmatch(row["sha256"]), "文件清单哈希无效")
    _require(total <= MAX_EXPANDED_BYTES, "展开总量超过安全上限")
    return rows


def _metadata(root, rel):
    text = _read(root, rel + "/meta.json", 1024 * 1024).decode("utf-8")
    meta = json.loads(text, object_pairs_hook=T._json_pairs)
    T._meta(meta, meta["directory"], "archive")
    _require(Path(rel).name == meta["directory"], "归档目录与元数据不一致")
    return meta, text


def _summary(root, rel, meta, meta_text):
    context_path = "snapshots/" + meta["snapshot"] + "/context.md"
    if _safe(root, rel + "/" + PACK, missing=True).exists():
        pack = _pack(root, rel, meta)
        value = _read_json(root, rel + "/" + SUMMARY)
        _require(H._digest(value) == pack["summary_sha256"], "摘要校验失败")
        return value
    descriptor = None
    manifest_rel = rel + "/snapshots/" + meta["snapshot"] + "/manifest.json"
    manifest = T._manifest(_read_json(root, manifest_rel, 4 * 1024 * 1024), meta)
    descriptor = manifest["context"]
    _require(_file_hash(root, rel + "/" + context_path) == descriptor["sha256"], "当前上下文哈希不符")
    with H._open_file(root, rel + "/" + context_path) as stream:
        sample = stream.read(SUMMARY_BYTES // 2)
    truncated = descriptor["size"] > len(sample)
    text = sample.decode("utf-8", errors="ignore" if truncated else "strict")
    value = {"schema": 1, "kind": "literal-task-summary", "task_id": meta["id"],
             "title": meta["title"], "project": meta["project"], "summary": meta["summary"],
             "closure": meta["closure"], "references": meta["references"],
             "source": {"meta_sha256": hashlib.sha256(meta_text.encode("utf-8")).hexdigest(),
                        "context_path": context_path, "context_sha256": descriptor["sha256"],
                        "context_size": descriptor["size"], "snapshot": meta["snapshot"]},
             "verbatim_context_prefix": text, "truncated": truncated,
             "notice": "只保留逐字摘录，不推断语义；截断时另附文末逐字后缀（出处 suffix_offset、"
                       "缺口 truncated_bytes）确保文末决定可见。永久清空的双重令牌同时确认已审阅此摘要，"
                       "仍有效的事实已另存于长期记忆并登记引用。"}
    if truncated:
        offset = max(0, descriptor["size"] - SUMMARY_BYTES // 2)
        with H._open_file(root, rel + "/" + context_path) as stream:
            stream.seek(offset)
            tail = stream.read(SUMMARY_BYTES // 2)
        value["verbatim_context_suffix"] = tail.decode("utf-8", errors="ignore")
        value["suffix_offset"] = offset
        value["truncated_bytes"] = max(0, descriptor["size"] - len(sample) - len(tail))
    return value


def _receipt_meta(receipt):
    text = receipt.get("meta_text")
    _require(isinstance(text, str) and len(text.encode("utf-8")) <= 1024 * 1024, "退役元数据备份无效")
    meta = json.loads(text, object_pairs_hook=T._json_pairs)
    T._meta(meta, meta["directory"], "archive")
    _require(hashlib.sha256(text.encode("utf-8")).hexdigest() == receipt.get("meta_sha256"), "退役元数据备份哈希错误")
    _require(receipt.get("source") == "handoff/archive/" + meta["directory"], "退役源路径无效")
    ticket = _ticket(receipt.get("ticket"))
    _require(receipt.get("destination") == "history/retired/" + ticket + "/" + meta["directory"],
             "退役恢复路径越界")
    plan = receipt.get("plan")
    _verify_seal(plan)
    _require(plan.get("kind") == "retire-plan" and plan.get("token") == ticket and
             plan.get("source") == receipt["source"] and plan.get("meta_text") == text and
             plan.get("meta_sha256") == receipt["meta_sha256"] and plan.get("summary") == receipt.get("summary"),
             "退役收据与已批准计划不符")
    return meta


def inventory_additions(inventory):
    """history/ 已计字节；把恢复区及永久保留收据中的引用加入全局保护图。"""
    if getattr(inventory, "_retention_added", False):
        return
    inventory._retention_added = True
    try:
        for ticket in inventory.children("history/retired"):
            _require(HEX.fullmatch(ticket), "受管退役票据名称无效")
            rel = "history/retired/" + ticket + "/receipt.json"
            receipt = _read_json(inventory.root, rel)
            _require(receipt.get("kind") == "retirement-receipt" and receipt.get("ticket") == ticket,
                     "退役收据无效")
            meta = _receipt_meta(receipt)
            state = receipt.get("state")
            _require(state in ("verifying", "retired", "restored", "purging", "purged"), "退役状态无效")
            if state == "restored":
                continue
            source_meta = receipt["source"] + "/meta.json"
            if source_meta not in inventory.metadata:
                inventory.metadata[source_meta] = receipt["meta_sha256"]
                inventory.references(meta, source_meta, True)
            elif inventory.metadata[source_meta] != receipt["meta_sha256"]:
                raise RuntimeError("退役事务期间任务元数据发生变化")
    except (OSError, RuntimeError, ValueError, T.TaskError) as exc:
        inventory.reference_error(str(exc))


def _inventory(api):
    inventory = H._Inventory(api)
    inventory_additions(inventory)
    _require(not inventory.error_count, "历史计量不完整: " + "; ".join(inventory.errors))
    _require(not inventory.reference_error_count, "引用关系不完整: " + "; ".join(inventory.reference_errors))
    return inventory


def _capacity(api, additional):
    inventory = _inventory(api)
    limit = inventory.config["history_max_bytes"] + MAINTENANCE_RESERVE_BYTES
    _require(inventory.total_bytes + additional <= limit,
             "维护峰值超过历史上限加固定 64 MiB reserve；停止且保留恢复材料")
    return max(0, limit - inventory.total_bytes)


def _writable(root, rel):
    path = _safe(root, rel)
    _require(stat.S_ISDIR(path.lstat().st_mode) and bool(path.lstat().st_mode & 0o222),
             "目录没有写权限: " + rel)
    return path


def _write(api, rel, value):
    root = H._root(api)
    data = _bytes(value)
    _require(len(data) <= MAX_CONTROL_BYTES, "控制文件超过大小上限")
    _capacity(api, len(data))
    parent = str(PurePosixPath(rel).parent)
    H._mkdir(root, parent)
    _writable(root, parent)
    path = _safe(root, rel, missing=True)
    api._atomic_write_text(path, data.decode("utf-8"))
    _require(_read_json(root, rel) == value, "事务回读验证失败: " + rel)
    T._sync_dir(path.parent)


def _seal(value):
    value = copy.deepcopy(value)
    value.pop("token", None)
    value.pop("data_loss_token", None)
    value["token"] = H._digest(value)
    if value.get("irreversible"):
        value["data_loss_token"] = H._digest({"permanently_discard_last_copy": value["token"],
                                             "scope": value["scope"]})
    return value


def _verify_seal(plan):
    _require(isinstance(plan, dict) and plan.get("schema") == 1, "计划格式无效")
    _require(_seal(plan) == plan, "计划或确认令牌被修改")


def _base(inventory, kind):
    return {"schema": 1, "kind": kind, "created_at": inventory.now.isoformat(),
            "scope": H._scope(inventory.root), "config_digest": H._digest(inventory.config),
            "reference_digest": inventory.reference_digest(), "max_batch": MAX_BATCH,
            "maintenance_reserve_bytes": MAINTENANCE_RESERVE_BYTES}


def _guard(api, plan):
    _verify_seal(plan)
    inventory = _inventory(api)
    _require(plan.get("scope") == H._scope(inventory.root), "计划不属于当前 guild")
    _require(plan.get("config_digest") == H._digest(inventory.config), "保留配置已变化，必须重新计划")
    _require(plan.get("reference_digest") == inventory.reference_digest(), "任务元数据、版本或引用已变化，必须重新计划")
    _require(plan.get("max_batch") == MAX_BATCH, "批次上限无效")
    return inventory


def _eligible(inventory, task):
    _require(task is not None and not task["active"], "只能维护显式选择的已封闭归档任务")
    _require(not task["held"] and not inventory.task_referenced(task), "任务被 pin/hold 或引用保护")
    return task


def _task_plan(api, task_id, kind):
    inventory = _inventory(api)
    task = _eligible(inventory, inventory.tasks.get(task_id))
    root, rel = inventory.root, task["path"]
    meta, meta_text = _metadata(root, rel)
    files, directories = _tree(root, rel)
    _require(not any(row["path"].startswith(".ag-") or row["path"] == ".transition.json" for row in files),
             "任务存在未完成事务")
    compacted = _safe(root, rel + "/" + PACK, missing=True).exists()
    if compacted:
        pack = _pack(root, rel, meta)
        _require(pack["state"] == "compact", "压缩事务未完成，请先续进同一计划")
        with _verified_zip(root, rel, pack):
            pass
    if kind == "compact-plan":
        _require(not compacted and not any(row["path"] in SIDECARS for row in files), "任务已压缩或存在冲突的保留文件")
    result = _base(inventory, kind)
    result.update(task_id=task_id, source=rel, revision=meta["revision"],
                  meta_text=meta_text, meta_sha256=task["metadata_sha256"],
                  summary=_summary(root, rel, meta, meta_text), files=files, directories=directories,
                  physical_bytes_freed=0, irreversible=False,
                  notice="计划只读取所选任务；压缩保留可验证完整 ZIP。退役只原子移动整包，不声称释放磁盘。")
    return _seal(result)


def _check_tree(root, rel, expected, missing=(), extras=(), compare_stat=True):
    current, directories = _tree(root, rel, hashes=False)
    actual = {row["path"]: row for row in current}
    wanted = {row["path"]: row for row in _rows(expected)}
    _require(set(actual) - set(extras) == set(wanted) - set(missing), "包文件集合已变化，拒绝读取或处置新增文件")
    for name in set(wanted) - set(missing):
        _require(actual[name]["size"] == wanted[name]["size"], "文件大小变化: " + name)
        if compare_stat:
            _require(actual[name]["stat"] == wanted[name]["stat"], "文件状态变化: " + name)
    return actual, directories


def _validate_pack(pack):
    _require(pack.get("kind") == "task-lossless-pack" and pack.get("schema") == 1, "压缩 sidecar 格式无效")
    _require(pack.get("state") in ("building", "compacting", "compact", "restoring", "restored", "aborting"), "压缩状态无效")
    _require(isinstance(pack.get("source_token"), str) and HEX.fullmatch(pack["source_token"]), "压缩来源令牌无效")
    rows = _rows(pack.get("files"))
    _require("meta.json" in {row["path"] for row in rows} and
             not any(row["path"] in SIDECARS for row in rows), "压缩清单包含保留字段或缺少元数据")
    dirs = pack.get("directories")
    _require(isinstance(dirs, list) and len(dirs) <= MAX_FILES and len(dirs) == len(set(dirs)), "压缩目录清单无效")
    for name in dirs:
        H._relative(name)
    return pack


def _pack(root, rel, meta):
    pack = _validate_pack(_read_json(root, rel + "/" + PACK))
    _require(pack.get("task_id") == meta["id"], "压缩包任务 ID 不符")
    _require(_file_hash(root, rel + "/meta.json") == pack.get("meta_sha256"), "压缩后元数据已变化")
    _require(next(row for row in pack["files"] if row["path"] == "meta.json")["sha256"] == pack["meta_sha256"],
             "压缩元数据哈希不一致")
    return pack


def verify_compacted_metadata(api, package, meta):
    """目录列举仅校验 sidecar/元数据，绝不打开 ZIP、正文或附件。"""
    root = H._root(api)
    rel = Path(package).relative_to(root).as_posix()
    return _pack(root, rel, meta)


class _LimitedWriter:
    def __init__(self, stream, limit):
        self.stream, self.limit = stream, limit

    def write(self, data):
        _require(self.stream.tell() + len(data) <= self.limit, "ZIP 工作盘达到固定维护峰值上限")
        return self.stream.write(data)

    def __getattr__(self, name):
        return getattr(self.stream, name)


def _zip_build(api, source, files, target, owner, journal_rel, journal):
    """原件全部保留至 ZIP 流式回读验证完成；已登记 inode 的未成品可安全续建。"""
    root = H._root(api)
    available = _capacity(api, 2 * len(_bytes(journal)) + 65536)
    limit = available - 2 * len(_bytes(journal)) - 65536
    _require(limit > 0, "没有足够的有界压缩工作盘")
    path = _safe(root, target, missing=True)
    H._mkdir(root, str(PurePosixPath(target).parent))
    _writable(root, str(PurePosixPath(target).parent))
    saved = journal.get(owner)
    if path.exists():
        info = path.lstat()
        _require(isinstance(saved, dict) and saved.get("inode") == info.st_ino and saved.get("device") == info.st_dev,
                 "未成品 ZIP 不属于当前事务，拒绝覆盖")
        limit += info.st_size
        flags = os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
    else:
        _require(saved is None, "已登记的 ZIP 工作文件丢失")
        flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(str(path), flags, 0o600)
    with os.fdopen(descriptor, "w+b") as output:
        info = os.fstat(output.fileno())
        _require(info.st_nlink == 1 and stat.S_ISREG(info.st_mode), "ZIP 工作文件不安全")
        if saved is None:
            journal[owner] = {"inode": info.st_ino, "device": info.st_dev}
            _write(api, journal_rel, journal)
        output.truncate(0)
        output.seek(0)
        limited = _LimitedWriter(output, limit)
        with zipfile.ZipFile(limited, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
            for row in files:
                info = zipfile.ZipInfo(row["path"], date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (stat.S_IFREG | 0o600) << 16
                digest, count = hashlib.sha256(), 0
                with H._open_file(root, source + "/" + row["path"], row.get("stat")) as original:
                    _require(os.fstat(original.fileno()).st_nlink == 1, "拒绝硬链接")
                    with archive.open(info, "w", force_zip64=True) as member:
                        for data in iter(lambda: original.read(CHUNK), b""):
                            digest.update(data)
                            count += len(data)
                            member.write(data)
                _require(digest.hexdigest() == row["sha256"] and count == row["size"], "压缩输入变化")
        output.flush()
        os.fsync(output.fileno())
    info = _safe(root, target).lstat()
    return {"path": Path(target).name, "size": info.st_size, "sha256": _file_hash(root, target)}


@contextmanager
def _verified_zip(root, rel, pack, selected=None):
    rows = _rows(pack["files"])
    descriptor = pack.get("zip")
    _require(isinstance(descriptor, dict) and descriptor.get("path") in (PAYLOAD, "recovery.zip"), "ZIP 描述无效")
    path = rel + "/" + descriptor["path"]
    info = _safe(root, path).lstat()
    _require(info.st_size == descriptor.get("size") and _file_hash(root, path) == descriptor.get("sha256"), "ZIP 哈希不符")
    expected = {row["path"]: row for row in rows}
    with H._open_file(root, path, H._stamp(info)) as stream:
        with zipfile.ZipFile(stream, "r") as archive:
            members = archive.infolist()
            _require(len(members) == len(rows), "ZIP 条目数不符")
            seen = set()
            for member in members:
                name = H._relative(member.filename).as_posix()
                _require(name not in seen and name in expected and not member.is_dir(), "ZIP 含重复、穿越或未知条目")
                seen.add(name)
                mode = member.external_attr >> 16
                _require(not mode or stat.S_IFMT(mode) in (0, stat.S_IFREG), "ZIP 含符号链接或特殊条目")
                _require(not member.flag_bits & 1 and member.compress_type in (zipfile.ZIP_DEFLATED, zipfile.ZIP_STORED),
                         "ZIP 加密或压缩格式不受支持")
                _require(member.file_size == expected[name]["size"] and
                         member.file_size <= MAX_MEMBER_BYTES and
                         member.file_size <= max(1, member.compress_size) * 10000, "ZIP 展开大小或压缩比不安全")
            for name, row in expected.items():
                if selected is not None and name not in selected:
                    continue
                digest, count = hashlib.sha256(), 0
                with archive.open(name) as member:
                    for data in iter(lambda: member.read(CHUNK), b""):
                        count += len(data)
                        _require(count <= row["size"], "ZIP 解压超过已确认长度")
                        digest.update(data)
                _require(count == row["size"] and digest.hexdigest() == row["sha256"], "ZIP CRC/内容回读失败")
            yield archive


def load_content(api, package, meta):
    """调用方已选中此任务；只读 ZIP，不加锁、不落盘、不修改元数据。"""
    root = H._root(api)
    rel = Path(package).relative_to(root).as_posix()
    pack = _pack(root, rel, meta)
    if pack["state"] == "restored":
        return _raw_content(root, rel, meta)
    _require(pack["state"] in ("compacting", "compact", "restoring"), "ZIP 尚未验证完成，原文仍保留，请续进压缩计划")
    prefix = "snapshots/" + meta["snapshot"] + "/"
    context_name, manifest_name = prefix + "context.md", prefix + "manifest.json"
    sizes = {row["path"]: row["size"] for row in pack["files"]}
    _require(sizes.get(context_name, MAX_CONTEXT_BYTES + 1) <= MAX_CONTEXT_BYTES and
             sizes.get(manifest_name, 4 * 1024 * 1024 + 1) <= 4 * 1024 * 1024, "当前上下文/清单超过安全读取上限")
    with _verified_zip(root, rel, pack, {context_name, manifest_name}) as archive:
        manifest = T._manifest(json.loads(archive.read(manifest_name).decode("utf-8"),
                                         object_pairs_hook=T._json_pairs), meta)
        context = archive.read(context_name)
        _require(T._hash(context) == manifest["context"], "压缩当前上下文与清单不符")
    artifact_paths = {entry["path"] for entry in manifest["artifacts"]}
    by_path = {row["path"]: row for row in pack["files"]}
    for entry in manifest["artifacts"]:
        _require(entry["path"] in by_path and all(by_path[entry["path"]][key] == entry[key] for key in ("size", "sha256")),
                 "压缩附件与当前清单不符")
    with _verified_zip(root, rel, pack, artifact_paths):
        pass
    return context.decode("utf-8"), manifest


def _raw_content(root, rel, meta):
    prefix = rel + "/snapshots/" + meta["snapshot"] + "/"
    manifest = T._manifest(_read_json(root, prefix + "manifest.json", 4 * 1024 * 1024), meta)
    context = _read(root, prefix + "context.md", MAX_CONTEXT_BYTES)
    _require(T._hash(context) == manifest["context"], "当前上下文与清单不符")
    for entry in manifest["artifacts"]:
        path = rel + "/" + entry["path"]
        _require(_safe(root, path).lstat().st_size == entry["size"] and _file_hash(root, path) == entry["sha256"], "附件内容不符")
    return context.decode("utf-8"), manifest


def _unlink(root, rel, digest=None):
    path = _safe(root, rel)
    _writable(root, str(PurePosixPath(rel).parent))
    if digest is not None:
        _require(_file_hash(root, rel) == digest, "清空前文件哈希变化: " + rel)
    path.unlink()
    T._sync_dir(path.parent)


def _remove_empty(root, base, directories):
    for name in sorted(directories, key=lambda value: (value.count("/"), value), reverse=True):
        path = _safe(root, base + "/" + name, missing=True)
        if path.exists():
            _require(stat.S_ISDIR(path.lstat().st_mode), "期望空目录")
            with os.scandir(path) as entries:
                empty = next(entries, None) is None
            if empty:
                path.rmdir()


def _compact(api, plan):
    inventory = _guard(api, plan)
    _require(plan["kind"] == "compact-plan", "需要压缩计划")
    task = _eligible(inventory, inventory.tasks.get(plan["task_id"]))
    root, rel = inventory.root, task["path"]
    _require(rel == plan["source"] and task["metadata_sha256"] == plan["meta_sha256"], "压缩源已变化")
    sidecar = rel + "/" + PACK
    if not _safe(root, sidecar, missing=True).exists():
        _check_tree(root, rel, plan["files"])
        pack = {"schema": 1, "kind": "task-lossless-pack", "state": "building", "task_id": plan["task_id"],
                "meta_sha256": plan["meta_sha256"], "source_token": plan["token"],
                "summary_sha256": H._digest(plan["summary"]), "files": plan["files"],
                "directories": plan["directories"], "deleted": [], "pending_delete": None, "zip": None}
        _write(api, sidecar, pack)
    else:
        meta = json.loads(plan["meta_text"])
        pack = _pack(root, rel, meta)
        _require(pack["source_token"] == plan["token"] and pack["files"] == plan["files"], "已有压缩事务不属于此计划")
    if pack["state"] == "aborting":
        _check_tree(root, rel, plan["files"], extras=SIDECARS)
        for row in plan["files"]:
            _require(_file_hash(root, rel + "/" + row["path"], row["stat"]) == row["sha256"], "撤销前原件校验失败")
        if _safe(root, rel + "/" + PAYLOAD, missing=True).exists():
            _unlink(root, rel + "/" + PAYLOAD, pack["zip"]["sha256"])
        _unlink(root, sidecar)
        raise NoProgress("无损压缩没有净收益；受管临时副本已撤销，原件完整")
    if pack["state"] == "building":
        _check_tree(root, rel, plan["files"], extras=SIDECARS)
        pack["zip"] = _zip_build(api, rel, plan["files"], rel + "/" + PAYLOAD,
                                  "zip_owner", sidecar, pack)
        with _verified_zip(root, rel, pack):
            pass
        savings = sum(row["size"] for row in plan["files"] if row["path"] != "meta.json") - (
            pack["zip"]["size"] + len(_bytes(pack)) + len(_bytes(plan["summary"])))
        if savings <= 0:
            pack["state"] = "aborting"
            _write(api, sidecar, pack)
            _unlink(root, rel + "/" + PAYLOAD, pack["zip"]["sha256"])
            _unlink(root, sidecar)
            raise NoProgress("无损压缩没有净收益；已撤销受管临时副本，原件保持完整，可明确退役")
        _write(api, rel + "/" + SUMMARY, plan["summary"])
        pack["state"] = "compacting"
        _write(api, sidecar, pack)
    _require(pack["state"] in ("compacting", "compact"), "压缩状态不允许继续删除原文")
    with _verified_zip(root, rel, pack):
        pass
    deleted = set(pack["deleted"])
    pending = pack.get("pending_delete")
    expected = {row["path"]: row for row in plan["files"]}
    _require(deleted <= set(expected) - {"meta.json"} and (pending is None or pending in expected and pending != "meta.json"),
             "压缩删除日志无效")
    if pending and not _safe(root, rel + "/" + pending, missing=True).exists():
        deleted.add(pending)
        pack["deleted"] = sorted(deleted)
        pack["pending_delete"] = None
        _write(api, sidecar, pack)
    _check_tree(root, rel, plan["files"], missing=deleted, extras=SIDECARS)
    remaining = [row for row in plan["files"] if row["path"] != "meta.json" and row["path"] not in deleted]
    count = 0
    for row in remaining[:MAX_BATCH]:
        _guard(api, plan)
        pack["pending_delete"] = row["path"]
        _write(api, sidecar, pack)
        _unlink(root, rel + "/" + row["path"], row["sha256"])
        count += 1
        deleted.add(row["path"])
        pack["deleted"] = sorted(deleted)
        pack["pending_delete"] = None
        _write(api, sidecar, pack)
    done = len(remaining) <= MAX_BATCH
    if done:
        _remove_empty(root, rel, plan["directories"])
        pack["state"] = "compact"
        _write(api, sidecar, pack)
    status = _inventory(api)
    return {"state": "complete" if done else "in_progress", "operation": "compact", "unlinked_files": count,
            "remaining_files": max(0, len(remaining) - count), "task_id": plan["task_id"],
            "total_bytes": status.total_bytes, "zip": rel + "/" + PAYLOAD,
            "notice": "ZIP 已完成 CRC/哈希回读；可用同一已批准计划继续，每批最多 10 个原文件。"}


def restore_for_reopen(api, package, meta):
    """调用方持 handoff→budget 锁；失败保留 ZIP 与事务，元数据从不改变。"""
    root = H._root(api)
    rel = Path(package).relative_to(root).as_posix()
    if not _safe(root, rel + "/" + PACK, missing=True).exists():
        return Path(package)
    pack = _pack(root, rel, meta)
    _require(pack["state"] in ("compacting", "compact", "restoring", "restored"), "压缩未完成备份验证，先续进压缩命令")
    if pack["state"] != "restored":
        rows = pack["files"]
        current, _ = _tree(root, rel, hashes=False)
        original = {row["path"] for row in rows}
        _require({row["path"] for row in current} <= original | SIDECARS | {RESTORE_TMP}, "恢复包含未知文件")
        temporary = _safe(root, rel + "/" + RESTORE_TMP, missing=True)
        if temporary.exists():
            ownership = pack.get("restore_temp")
            info = temporary.lstat()
            _require(isinstance(ownership, dict) and ownership.get("inode") == info.st_ino and
                     ownership.get("device") == info.st_dev and ownership.get("path") in original,
                     "恢复临时文件归属无法验证")
        missing = []
        for row in rows:
            path = _safe(root, rel + "/" + row["path"], missing=True)
            if path.exists():
                _require(path.lstat().st_size == row["size"] and _file_hash(root, rel + "/" + row["path"]) == row["sha256"],
                         "恢复遇到不同内容，禁止覆盖")
            else:
                missing.append(row)
        _capacity(api, sum(row["size"] for row in missing) + 2 * len(_bytes(pack)))
        with _verified_zip(root, rel, pack) as archive:
            pack["state"] = "restoring"
            _write(api, rel + "/" + PACK, pack)
            for row in missing:
                target = rel + "/" + row["path"]
                H._mkdir(root, str(PurePosixPath(target).parent))
                destination = _safe(root, target, missing=True)
                _require(not destination.exists(), "恢复目标已出现，拒绝覆盖")
                if temporary.exists():
                    saved = pack.get("restore_temp", {})
                    info = temporary.lstat()
                    _require(saved.get("inode") == info.st_ino and saved.get("device") == info.st_dev,
                             "恢复临时文件已变化")
                    flags = os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
                else:
                    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
                descriptor = os.open(str(temporary), flags, 0o600)
                with os.fdopen(descriptor, "wb") as output, archive.open(row["path"]) as source:
                    info = os.fstat(output.fileno())
                    _require(info.st_nlink == 1, "恢复工作盘拒绝硬链接")
                    pack["restore_temp"] = {"path": row["path"], "inode": info.st_ino, "device": info.st_dev}
                    _write(api, rel + "/" + PACK, pack)
                    output.truncate(0)
                    count = 0
                    for data in iter(lambda: source.read(CHUNK), b""):
                        count += len(data)
                        _require(count <= row["size"], "恢复超过确认长度")
                        output.write(data)
                    output.flush()
                    os.fsync(output.fileno())
                _require(_file_hash(root, rel + "/" + RESTORE_TMP) == row["sha256"], "恢复文件回读失败")
                _require(not _safe(root, target, missing=True).exists(), "恢复目标冲突，禁止覆盖")
                os.rename(str(temporary), str(destination))
                T._sync_dir(destination.parent)
                pack["restore_temp"] = None
                _write(api, rel + "/" + PACK, pack)
        for name in pack["directories"]:
            H._mkdir(root, rel + "/" + name)
        _raw_content(root, rel, meta)
        pack["state"] = "restored"
        _write(api, rel + "/" + PACK, pack)
    for row in pack["files"]:
        _require(_file_hash(root, rel + "/" + row["path"]) == row["sha256"], "恢复原件不完整，保留 ZIP")
    for name in (PAYLOAD, SUMMARY):
        if _safe(root, rel + "/" + name, missing=True).exists():
            expected = pack["zip"]["sha256"] if name == PAYLOAD else hashlib.sha256(_bytes(_read_json(root, rel + "/" + SUMMARY))).hexdigest()
            if name == SUMMARY:
                _require(H._digest(_read_json(root, rel + "/" + SUMMARY)) == pack["summary_sha256"], "摘要变化")
                expected = _file_hash(root, rel + "/" + SUMMARY)
            _unlink(root, rel + "/" + name, expected)
    _unlink(root, rel + "/" + PACK)
    return Path(package)


def _ticket(value):
    _require(isinstance(value, str) and HEX.fullmatch(value), "ticket 必须是具体的 64 位十六进制令牌")
    return value


def _retire(api, plan):
    inventory = _guard(api, plan)
    _require(plan["kind"] == "retire-plan", "需要整包退役计划")
    root, source, ticket = inventory.root, plan["source"], _ticket(plan["token"])
    base = "history/retired/" + ticket
    receipt_path = base + "/receipt.json"
    meta = json.loads(plan["meta_text"], object_pairs_hook=T._json_pairs)
    T._meta(meta, meta["directory"], "archive")
    _require(source == "handoff/archive/" + meta["directory"] and meta["id"] == plan["task_id"] and
             hashlib.sha256(plan["meta_text"].encode("utf-8")).hexdigest() == plan["meta_sha256"],
             "退役计划任务/源路径/元数据不一致")
    task = inventory.tasks.get(plan["task_id"])
    if task is not None:
        _require(task["path"] == source and task["metadata_sha256"] == plan["meta_sha256"], "退役源不是所选任务")
    destination = base + "/" + meta["directory"]
    if _safe(root, receipt_path, missing=True).exists():
        receipt = _read_json(root, receipt_path)
        _receipt_meta(receipt)
        _require(receipt.get("plan") == plan, "退役票据不属于此计划")
    else:
        _eligible(inventory, inventory.tasks.get(plan["task_id"]))
        _check_tree(root, source, plan["files"])
        receipt = {"schema": 1, "kind": "retirement-receipt", "ticket": ticket, "state": "verifying",
                   "source": source, "destination": destination, "meta_text": plan["meta_text"],
                   "meta_sha256": plan["meta_sha256"], "summary": plan["summary"], "plan": plan,
                   "verified": [], "retired_at": inventory.now.isoformat()}
        _write(api, receipt_path, receipt)
    source_exists = _safe(root, source, missing=True).exists()
    destination_exists = _safe(root, destination, missing=True).exists()
    _require(source_exists != destination_exists, "退役源与目标同时存在或同时缺失")
    if destination_exists:
        _require(receipt["state"] in ("verifying", "retired"), "任务已进入其他维护状态")
        _check_tree(root, destination, plan["files"])
        receipt["state"] = "retired"
        _write(api, receipt_path, receipt)
        return {"state": "complete", "operation": "retire", "ticket": ticket, "physical_bytes_freed": 0,
                "verified_files": 0, "unlinked_files": 0}
    _eligible(inventory, inventory.tasks.get(plan["task_id"]))
    _check_tree(root, source, plan["files"])
    verified = set(receipt["verified"])
    _require(verified <= {row["path"] for row in plan["files"]}, "退役校验日志无效")
    remaining = [row for row in plan["files"] if row["path"] not in verified]
    for row in remaining[:MAX_BATCH]:
        _require(_file_hash(root, source + "/" + row["path"], row["stat"]) == row["sha256"], "退役输入哈希变化")
        verified.add(row["path"])
    receipt["verified"] = sorted(verified)
    _write(api, receipt_path, receipt)
    done = len(remaining) <= MAX_BATCH
    if done:
        _guard(api, plan)
        _check_tree(root, source, plan["files"])
        target = _safe(root, destination, missing=True)
        _require(not target.exists(), "退役目标冲突")
        _writable(root, str(PurePosixPath(source).parent))
        _writable(root, base)
        _require(_safe(root, source).lstat().st_dev == _safe(root, base).lstat().st_dev, "禁止跨设备退役")
        os.rename(str(_safe(root, source)), str(target))
        T._sync_dir(target.parent)
        T._sync_dir(root / "handoff/archive")
        receipt["state"] = "retired"
        _write(api, receipt_path, receipt)
    return {"state": "complete" if done else "in_progress", "operation": "retire", "ticket": ticket,
            "verified_files": min(MAX_BATCH, len(remaining)), "unlinked_files": 0,
            "remaining_files": max(0, len(remaining) - MAX_BATCH), "physical_bytes_freed": 0,
            "notice": "整包从 archive 原子移入受管恢复区；仍计入预算，未释放磁盘。"}


def _restore(api, ticket=None, task_id=None):
    inventory = _inventory(api)
    root = inventory.root
    if task_id is not None:
        matches = []
        for name in inventory.children("history/retired"):
            receipt = _read_json(root, "history/retired/" + _ticket(name) + "/receipt.json")
            if _receipt_meta(receipt)["id"] == task_id and receipt["state"] in ("verifying", "retired"):
                matches.append(name)
        _require(len(matches) == 1, "任务没有唯一可恢复票据，请显式选择 --ticket")
        ticket = matches[0]
    ticket = _ticket(ticket)
    receipt_path = "history/retired/" + ticket + "/receipt.json"
    receipt = _read_json(root, receipt_path)
    meta = _receipt_meta(receipt)
    _require(receipt["state"] in ("verifying", "retired"), "此票据不可恢复，或已永久清空/部分清空")
    source, destination = receipt["destination"], receipt["source"]
    if receipt.get("restore_pending") and not _safe(root, source, missing=True).exists():
        task = inventory.tasks.get(meta["id"])
        _require(task is not None and task["path"] == destination and task["metadata_sha256"] == receipt["meta_sha256"],
                 "恢复事务目标与原件不一致")
        _check_tree(root, destination, receipt["plan"]["files"])
        for row in receipt["plan"]["files"]:
            _require(_file_hash(root, destination + "/" + row["path"], row["stat"]) == row["sha256"], "恢复事务数据变化")
        receipt["state"] = "restored"
        receipt["restore_pending"] = False
        _write(api, receipt_path, receipt)
        return {"state": "complete", "operation": "restore", "ticket": ticket, "task_id": meta["id"],
                "package": str(root / destination), "physical_bytes_freed": 0}
    _require(meta["id"] not in inventory.tasks, "相同任务 ID 已存在，禁止覆盖")
    _require(not _safe(root, destination, missing=True).exists(), "恢复目标已存在，禁止覆盖")
    _check_tree(root, source, receipt["plan"]["files"])
    for row in receipt["plan"]["files"]:
        _require(_file_hash(root, source + "/" + row["path"], row["stat"]) == row["sha256"], "退役数据哈希不符")
    _writable(root, str(PurePosixPath(source).parent))
    H._mkdir(root, "handoff/archive")
    _writable(root, "handoff/archive")
    receipt["restore_pending"] = True
    _write(api, receipt_path, receipt)
    os.rename(str(_safe(root, source)), str(_safe(root, destination, missing=True)))
    T._sync_dir(root / "handoff/archive")
    receipt["state"] = "restored"
    receipt["restore_pending"] = False
    _write(api, receipt_path, receipt)
    return {"state": "complete", "operation": "restore", "ticket": ticket, "task_id": meta["id"],
            "package": str(root / destination), "physical_bytes_freed": 0}


def _receipt_cleanup_plan(api, ticket):
    """终态（purged/restored）收据的有界清理计划；批准即永久丢弃最后一份摘要/决策存档。"""
    inventory = _inventory(api)
    ticket = _ticket(ticket)
    root = inventory.root
    base = "history/retired/" + ticket
    receipt_path = base + "/receipt.json"
    receipt = _read_json(root, receipt_path)
    meta = _receipt_meta(receipt)
    _require(receipt.get("state") in TERMINAL_RECEIPT_STATES, "仅终态（purged/restored）收据可清理")
    files, directories = _tree(root, base)
    _require([row["path"] for row in files] == ["receipt.json"] and not directories,
             "终态票据目录含未登记文件，拒绝生成清理计划")
    plan = _base(inventory, "receipt-cleanup-plan")
    plan.update(ticket=ticket, state=receipt["state"], task_id=meta["id"],
                receipt_path=receipt_path, retired_at=receipt.get("retired_at"),
                receipt_size=files[0]["size"], receipt_sha256=files[0]["sha256"],
                summary_sha256=H._digest(receipt.get("summary")),
                physical_bytes_freed=0, irreversible=True,
                notice="删除终态收据即永久丢弃其摘要/决策记录的最后一份存档；"
                       "须另给此计划的具体 data_loss_token 双重确认；不会触碰任何现存任务。")
    return _seal(plan)


def _receipt_cleanup(api, plan):
    """删除终态收据会收缩引用图，故不复核整体引用摘要，只钉死收据自身内容后原子删除。"""
    _verify_seal(plan)
    _require(plan.get("kind") == "receipt-cleanup-plan" and plan.get("irreversible") is True,
             "需要终态收据清理计划")
    inventory = _inventory(api)
    _require(plan.get("scope") == H._scope(inventory.root), "计划不属于当前 guild")
    _require(plan.get("config_digest") == H._digest(inventory.config), "保留配置已变化，必须重新计划")
    _require(plan.get("max_batch") == MAX_BATCH, "批次上限无效")
    root, before = inventory.root, inventory.total_bytes
    ticket = _ticket(plan.get("ticket"))
    base = "history/retired/" + ticket
    _require(plan.get("receipt_path") == base + "/receipt.json", "收据清理路径越界")
    _require(plan.get("state") in TERMINAL_RECEIPT_STATES, "收据清理状态无效")
    directory = _safe(root, base, missing=True)
    if not directory.exists():
        return {"state": "complete", "operation": "receipt-cleanup", "ticket": ticket,
                "unlinked_files": 0, "removed_logical_bytes": 0, "net_history_bytes_freed": 0,
                "total_bytes": before,
                "notice": "终态收据已不在受管恢复区；同一已批准计划幂等完成。"}
    receipt_file = _safe(root, base + "/receipt.json", missing=True)
    unlinked, released = 0, 0
    if receipt_file.exists():
        receipt = _read_json(root, base + "/receipt.json")
        meta = _receipt_meta(receipt)
        _require(receipt.get("state") == plan["state"], "收据状态与已批准计划不符")
        _require(receipt.get("retired_at") == plan.get("retired_at") and meta["id"] == plan.get("task_id"),
                 "收据归属与已批准计划不符")
        _require(_file_hash(root, base + "/receipt.json") == plan.get("receipt_sha256"),
                 "收据内容已变化，必须重新计划")
        files, directories = _tree(root, base)
        _require([row["path"] for row in files] == ["receipt.json"] and not directories,
                 "终态票据目录含未登记文件，拒绝清理")
        _unlink(root, base + "/receipt.json", plan["receipt_sha256"])
        unlinked, released = 1, plan.get("receipt_size", 0)
    with os.scandir(directory) as entries:
        _require(next(entries, None) is None, "票据目录仍有未知文件，拒绝移除")
    directory.rmdir()
    T._sync_dir(directory.parent)
    after = _inventory(api)
    return {"state": "complete", "operation": "receipt-cleanup", "ticket": ticket,
            "unlinked_files": unlinked, "removed_logical_bytes": released,
            "net_history_bytes_freed": before - after.total_bytes, "total_bytes": after.total_bytes,
            "notice": "终态收据已逐文件物理 unlink，票据目录已移除；其中的摘要/决策记录随之永久丢弃"
                      "（已双重确认）。不保证操作系统立即回收物理块。"}


def _referenced_path(inventory, path):
    return any(path == ref or path.startswith(ref + "/") or ref.startswith(path + "/") for ref in inventory.path_refs)


def _recovery_plan(api, ticket):
    inventory = _inventory(api)
    ticket = _ticket(ticket)
    root = inventory.root
    retired_path = "history/retired/" + ticket + "/receipt.json"
    plan = _base(inventory, "purge-plan")
    if _safe(root, retired_path, missing=True).exists():
        receipt = _read_json(root, retired_path)
        meta = _receipt_meta(receipt)
        _require(receipt["state"] == "retired", "仅完整退役包可生成清空计划")
        _require(not meta["pin"] and not meta["hold"] and meta["id"] not in inventory.task_refs and
                 meta["directory"] not in inventory.task_refs and not _referenced_path(inventory, receipt["source"]),
                 "退役任务被引用或保护")
        source = receipt["destination"]
        _require(not _referenced_path(inventory, source), "恢复包被引用")
        files, directories = _tree(root, source)
        _check_tree(root, source, receipt["plan"]["files"])
        _require(files == receipt["plan"]["files"], "退役包与原计划不符")
        plan.update(ticket=ticket, source=source, files=files, directories=directories,
                    receipt_path=retired_path, recovery_type="retired", summary=receipt["summary"],
                    task_id=meta["id"], original_source=receipt["source"],
                    backup_path="history/retired/" + ticket + "/recovery.zip",
                    preserved_receipt=retired_path)
    else:
        base = "history/backups/" + ticket
        manifest_path = base + "/manifest.json"
        manifest = _read_json(root, manifest_path)
        original = manifest.get("plan")
        _require(isinstance(original, dict) and original.get("kind") == "history-quarantine-plan" and
                 original.get("token") == ticket, "未识别的旧受管恢复清单")
        body = {key: value for key, value in original.items() if key != "token"}
        _require(H._digest(body) == ticket and original.get("scope") == H._scope(root), "旧恢复清单被修改或不属于本 guild")
        _require(manifest.get("backup_root") == base and
                 manifest.get("quarantine_root") == "history/quarantine/" + ticket and
                 manifest.get("status") in ("prepared", "quarantined"), "旧恢复目录边界不合法")
        originals = original.get("files")
        _require(isinstance(originals, list) and 1 <= len(originals) <= MAX_BATCH, "旧恢复清单条数无效")
        roots = [base, "history/quarantine/" + ticket]
        files, directories = [], []
        allowed = {"backups/" + ticket + "/manifest.json"}
        for entry in originals:
            origin = H._relative(entry["path"]).as_posix()
            _require(not _referenced_path(inventory, origin), "旧恢复原件路径被引用")
            task = inventory.tasks.get(entry.get("task_id"))
            if task:
                _eligible(inventory, task)
                _require(not H._Inventory.protected(inventory, {"path": origin, "task_id": task["id"],
                           "category": "archived_tasks", "stat": entry["stat"]}), "旧恢复文件现在是受保护现场")
            for directory in roots:
                path = directory + "/" + origin
                exists = _safe(root, path, missing=True).exists()
                _require(exists or directory != base, "旧备份不完整，禁止清空")
                if exists:
                    _require(_safe(root, path).lstat().st_size == entry["stat"]["size"] and
                             _file_hash(root, path) == entry["sha256"], "旧备份/隔离原件校验失败")
                    allowed.add(path[len("history/"):])
        for directory in roots:
            if _safe(root, directory, missing=True).exists():
                selected, dirs = _tree(root, directory)
                prefix = directory[len("history/"):] + "/"
                files.extend(dict(row, path=prefix + row["path"]) for row in selected)
                directories.extend(prefix.rstrip("/") + "/" + name for name in dirs)
                directories.append(prefix.rstrip("/"))
        _require({row["path"] for row in files} == allowed, "旧恢复区含未登记文件，禁止清空")
        _require(not any(_referenced_path(inventory, "history/" + row["path"]) for row in files), "恢复副本被引用")
        plan.update(ticket=ticket, source="history", files=sorted(files, key=lambda row: row["path"]),
                    directories=sorted(set(directories)), recovery_type="legacy", task_id=None,
                    original_sources=[row["path"] for row in originals],
                    summary={"kind": "legacy-recovery-summary", "original_files": originals,
                             "notice": "旧版本已验证备份和隔离副本；批准永久清空前必须审阅原清单并另存有效事实。"},
                    receipt_path="history/receipts/" + ticket + ".json",
                    backup_path="history/receipts/" + ticket + ".recovery.zip",
                    preserved_receipt="history/receipts/" + ticket + ".json")
    plan.update(irreversible=True, verified_backup_required=True,
                notice="将先创建并逐字节校验有限 ZIP 备份；最多 10 普通文件/批，"
                       "最后一份备份也会永久删除。两个具体令牌确认同时表示已审阅摘要、"
                       "已把仍有效事实另存并登记引用。收据/摘要/决策来源保留至终态；"
                       "终态收据随后经双确认纳入有界清理，不再永久计费。")
    return _seal(plan)


def _purge_protection(inventory, plan):
    if plan["recovery_type"] == "retired":
        _require(plan["task_id"] not in inventory.tasks and plan["task_id"] not in inventory.task_refs and
                 not _referenced_path(inventory, plan["original_source"]), "退役任务被新引用或重新创建")
    else:
        for path in plan["original_sources"]:
            _require(not _referenced_path(inventory, path), "旧原件被引用")
    for row in plan["files"]:
        _require(not _referenced_path(inventory, plan["source"] + "/" + row["path"]), "待清空文件被引用")


def _purge_files(root, plan, deleted, pending=None):
    expected = {row["path"]: row for row in plan["files"]}
    _require(deleted <= set(expected) | {"@backup"}, "清空日志包含未知路径")
    _require(pending is None or pending in expected or pending == "@backup", "清空待处理路径无效")
    for name, row in expected.items():
        path = plan["source"] + "/" + name
        exists = _safe(root, path, missing=True).exists()
        if name in deleted:
            _require(not exists, "已删除文件重新出现，禁止自动处置")
        elif not exists:
            _require(name == pending, "未登记的文件缺失，停止清空")
        else:
            _require(_safe(root, path).lstat().st_size == row["size"] and
                     _file_hash(root, path, row["stat"]) == row["sha256"], "待清空数据变化")
    bases = [plan["source"]] if plan["recovery_type"] == "retired" else [
        "history/backups/" + plan["ticket"], "history/quarantine/" + plan["ticket"]]
    actual = set()
    for base in bases:
        if _safe(root, base, missing=True).exists():
            rows, _ = _tree(root, base, hashes=False)
            for row in rows:
                full = base + "/" + row["path"]
                actual.add(full[len(plan["source"]) + 1:])
    _require(actual == set(expected) - deleted - ({pending} if pending and pending not in actual else set()),
             "受管恢复区新增文件，拒绝清空")


def _purge(api, plan):
    inventory = _guard(api, plan)
    _require(plan["kind"] == "purge-plan" and plan.get("irreversible") is True, "需要永久清空计划")
    ticket = _ticket(plan.get("ticket"))
    _rows(plan.get("files"))
    if plan.get("recovery_type") == "retired":
        expected_receipt = "history/retired/" + ticket + "/receipt.json"
        _require(plan.get("receipt_path") == expected_receipt and
                 plan.get("backup_path") == "history/retired/" + ticket + "/recovery.zip", "清空恢复路径越界")
        registered = _read_json(inventory.root, expected_receipt)
        meta = _receipt_meta(registered)
        _require(plan.get("source") == registered["destination"] and plan.get("original_source") == registered["source"] and
                 plan.get("files") == registered["plan"]["files"] and plan.get("directories") == registered["plan"]["directories"] and
                 plan.get("task_id") == meta["id"] and plan.get("summary") == registered["summary"], "清空计划超出已登记退役包")
        _require(registered["state"] in ("retired", "purging", "purged"), "退役票据状态不允许清空")
    else:
        _require(plan.get("recovery_type") == "legacy" and plan.get("source") == "history" and
                 plan.get("receipt_path") == "history/receipts/" + ticket + ".json" and
                 plan.get("backup_path") == "history/receipts/" + ticket + ".recovery.zip", "旧受管恢复路径越界")
        allowed = ("backups/" + ticket + "/", "quarantine/" + ticket + "/")
        _require(all(row["path"].startswith(allowed) for row in plan["files"]), "旧恢复计划试图清空非受管文件")
        if not _safe(inventory.root, plan["receipt_path"], missing=True).exists():
            recreated = _recovery_plan(api, ticket)
            for key in ("source", "files", "directories", "original_sources", "summary"):
                _require(plan.get(key) == recreated.get(key), "旧恢复计划与受管清单不符")
    _purge_protection(inventory, plan)
    root, receipt_path = inventory.root, plan["receipt_path"]
    if _safe(root, receipt_path, missing=True).exists():
        receipt = _read_json(root, receipt_path)
    else:
        _require(plan["recovery_type"] == "legacy", "缺失退役收据")
        receipt = {"schema": 1, "kind": "purge-receipt", "ticket": plan["ticket"], "summary": plan["summary"]}
    if "purge" not in receipt:
        _purge_files(root, plan, set())
        for row in plan["files"]:
            _writable(root, str(PurePosixPath(plan["source"] + "/" + row["path"]).parent))
        receipt["purge"] = {"plan": plan, "state": "building", "deleted": [], "pending_delete": None,
                            "backup": None, "approved_at": inventory.now.isoformat()}
        _write(api, receipt_path, receipt)
    journal = receipt["purge"]
    _require(journal.get("plan") == plan, "已有清空事务不属于此计划")
    if journal["state"] == "complete":
        return {"state": "complete", "operation": "purge", "unlinked_files": 0, "ticket": plan["ticket"]}
    if journal["state"] == "building":
        _purge_files(root, plan, set())
        backup = _zip_build(api, plan["source"], plan["files"], plan["backup_path"],
                            "backup_owner", receipt_path, receipt)
        journal["backup"] = backup
        _verify_backup(root, plan, journal)
        journal["state"] = "deleting"
        if receipt.get("kind") == "retirement-receipt":
            receipt["state"] = "purging"
        _write(api, receipt_path, receipt)
    _require(journal["state"] == "deleting", "清空事务状态无效")
    deleted = set(journal["deleted"])
    pending = journal["pending_delete"]
    _purge_files(root, plan, deleted, pending)
    if pending:
        path = plan["backup_path"] if pending == "@backup" else plan["source"] + "/" + pending
        if not _safe(root, path, missing=True).exists():
            deleted.add(pending)
            journal["deleted"] = sorted(deleted)
            journal["pending_delete"] = None
            _write(api, receipt_path, receipt)
    if "@backup" not in deleted:
        _verify_backup(root, plan, journal)
    remaining = [row for row in plan["files"] if row["path"] not in deleted]
    selected = remaining[:MAX_BATCH]
    count, released = 0, 0
    for row in selected:
        _purge_protection(_guard(api, plan), plan)
        journal["pending_delete"] = row["path"]
        _write(api, receipt_path, receipt)
        _unlink(root, plan["source"] + "/" + row["path"], row["sha256"])
        count += 1
        released += row["size"]
        deleted.add(row["path"])
        journal["deleted"] = sorted(deleted)
        journal["pending_delete"] = None
        _write(api, receipt_path, receipt)
    if len(remaining) <= count and "@backup" not in deleted and count < MAX_BATCH:
        _purge_protection(_guard(api, plan), plan)
        _verify_backup(root, plan, journal)
        journal["pending_delete"] = "@backup"
        _write(api, receipt_path, receipt)
        _unlink(root, plan["backup_path"], journal["backup"]["sha256"])
        released += journal["backup"]["size"]
        count += 1
        deleted.add("@backup")
        journal["deleted"] = sorted(deleted)
        journal["pending_delete"] = None
        _write(api, receipt_path, receipt)
    done = len(remaining) <= len(selected) and "@backup" in deleted
    if done:
        _remove_empty(root, plan["source"], plan["directories"])
        if plan["recovery_type"] == "retired":
            path = _safe(root, plan["source"])
            with os.scandir(path) as entries:
                _require(next(entries, None) is None, "恢复区仍有未知文件")
            path.rmdir()
            receipt["state"] = "purged"
        journal["state"] = "complete"
        _write(api, receipt_path, receipt)
    after = _inventory(api)
    return {"state": "complete" if done else "in_progress", "operation": "purge", "ticket": plan["ticket"],
            "unlinked_files": count, "removed_logical_bytes": released,
            "net_history_bytes_freed": inventory.total_bytes - after.total_bytes,
            "total_bytes": after.total_bytes, "preserved_receipt": receipt_path,
            "notice": "已逐文件物理 unlink；不保证操作系统快照/文件系统立即回收物理块。未使用回收站伪报释放。"}


def _verify_backup(root, plan, journal):
    descriptor = journal.get("backup")
    _require(isinstance(descriptor, dict), "缺少已验证备份")
    path = plan["backup_path"]
    _require(_safe(root, path).lstat().st_size == descriptor["size"] and _file_hash(root, path) == descriptor["sha256"],
             "清空前备份校验失败")
    expected = {row["path"]: row for row in _rows(plan["files"])}
    with H._open_file(root, path) as stream, zipfile.ZipFile(stream) as archive:
        members = archive.infolist()
        _require(len(members) == len(expected) and len({item.filename for item in members}) == len(members), "备份条目集合错误")
        for member in members:
            name = H._relative(member.filename).as_posix()
            _require(name in expected and not member.is_dir() and member.file_size == expected[name]["size"] and
                     stat.S_IFMT(member.external_attr >> 16) in (0, stat.S_IFREG) and not member.flag_bits & 1 and
                     member.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED) and
                     member.file_size <= max(1, member.compress_size) * 10000, "备份成员无效或不安全")
            digest, count = hashlib.sha256(), 0
            with archive.open(member) as source:
                for data in iter(lambda: source.read(CHUNK), b""):
                    count += len(data)
                    _require(count <= expected[name]["size"], "备份展开越界")
                    digest.update(data)
            _require(count == expected[name]["size"] and digest.hexdigest() == expected[name]["sha256"], "备份回读错误")


def _needs(inventory):
    archives = [task for task in inventory.tasks.values() if not task["active"]]
    expired = [task["id"] for task in archives if (inventory.now - task["closed_at"]).total_seconds() >=
               inventory.config["history_retention_days"] * 86400]
    full = [task["id"] for task in archives if (inventory.now - task["closed_at"]).total_seconds() >=
            inventory.config["history_full_days"] * 86400 and
            not _safe(inventory.root, task["path"] + "/" + PACK, missing=True).exists()]
    return {"bytes_to_target": max(0, inventory.total_bytes - inventory.config["history_target_bytes"]),
            "excess_tasks": max(0, len(archives) - inventory.config["history_max_tasks"]),
            "expired_tasks": expired, "full_detail_tasks": full}


def _cycle_plan(api):
    inventory = _inventory(api)
    result = _base(inventory, "cycle-plan")
    tasks = sorted((task for task in inventory.tasks.values() if not task["active"]),
                   key=lambda task: (task["closed_at"], task["id"]))
    surplus = max(0, len(tasks) - inventory.config["history_max_tasks"])
    excess = {task["id"] for task in tasks[:surplus]}
    actions, blockers = [], []
    for task in tasks:
        age = (inventory.now - task["closed_at"]).total_seconds() / 86400
        pressure = inventory.total_bytes > inventory.config["history_target_bytes"]
        compacted = _safe(inventory.root, task["path"] + "/" + PACK, missing=True).exists()
        retire = age >= inventory.config["history_retention_days"] or task["id"] in excess or pressure
        compact = age >= inventory.config["history_full_days"] and not compacted
        if age < inventory.config["history_full_days"] or not (compact or retire):
            continue
        if task["held"] or inventory.task_referenced(task):
            blockers.append({"task_id": task["id"], "reason": "pin/hold/引用保护"})
            continue
        selected = _task_plan(api, task["id"], "compact-plan" if compact else "retire-plan")
        actions.append({"kind": "task", "plan": selected, "compact": compact, "retire": retire,
                        "mandatory_retire": age >= inventory.config["history_retention_days"] or task["id"] in excess,
                        "derived_files": ["meta.json", PACK, SUMMARY, PAYLOAD] if compact else [],
                        "notice": "只允许本清单及其经验证压缩产物；退休后如仍需回收，将清空确切的受管恢复包。"})
    recovery = []
    for ticket in inventory.children("history/retired"):
        receipt = _read_json(inventory.root, "history/retired/" + ticket + "/receipt.json")
        if receipt["state"] == "retired":
            recovery.append((receipt["retired_at"], ticket))
    for ticket in inventory.children("history/backups"):
        if HEX.fullmatch(ticket):
            manifest = _read_json(inventory.root, "history/backups/" + ticket + "/manifest.json")
            recovery.append((manifest.get("plan", {}).get("created_at", ""), ticket))
    for _, ticket in sorted(recovery):
        try:
            selected = _recovery_plan(api, ticket)
            actions.append({"kind": "purge", "plan": selected})
        except (OSError, RuntimeError, ValueError, T.TaskError) as exc:
            blockers.append({"ticket": ticket, "reason": str(exc)})
    for ticket in inventory.children("history/retired"):
        try:
            receipt = _read_json(inventory.root, "history/retired/" + ticket + "/receipt.json")
            if receipt.get("state") not in TERMINAL_RECEIPT_STATES:
                continue
            selected = _receipt_cleanup_plan(api, ticket)
            actions.append({"kind": "receipt-cleanup", "plan": selected})
        except (OSError, RuntimeError, ValueError, T.TaskError) as exc:
            blockers.append({"ticket": ticket, "reason": str(exc)})
    bounded, size = [], 0
    for action in actions:
        item_size = len(_bytes(action))
        if size + item_size > MAX_CONTROL_BYTES // 3:
            blockers.append({"reason": "本轮具体清单已达到控制文件安全上限；剩余对象须重新计划批准"})
            break
        size += item_size
        bounded.append(action)
    actions = bounded
    result.update(actions=actions, blockers=blockers[:H.MAX_ERRORS], needs=_needs(inventory),
                  irreversible=any(action["kind"] in ("purge", "receipt-cleanup") or action.get("retire")
                                   for action in actions),
                  notice="默认只计划。批准后每次执行至多一个 10 文件批次；每轮重新计量。"
                         "永久清空必须另给此计划的具体 data_loss_token；未列出的新文件永不纳入。"
                         "先无损压缩，仍超低水位/年龄/数量时才退役及清空；摘要和收据保留至终态，"
                         "终态收据经双确认有界清理，不再永久计费。")
    return _seal(result)


def _cycle(api, plan, data_loss):
    inventory = _guard(api, plan)
    _require(plan["kind"] == "cycle-plan" and isinstance(plan.get("actions"), list), "需要循环计划")
    root = inventory.root
    existing = _safe(root, CYCLE_PATH, missing=True)
    if existing.exists():
        previous = _read_json(root, CYCLE_PATH)
        if previous.get("plan", {}).get("token") == plan["token"]:
            state = previous
        else:
            _require(previous.get("state") in ("complete", "blocked", "needs_confirmation"), "另一个已批准循环尚未结束")
            state = None
    else:
        state = None
    if state is None:
        state = {"schema": 1, "kind": "retention-cycle", "plan": plan, "index": 0, "phase": None,
                 "current_plan": None, "state": "in_progress", "rounds": 0}
        _write(api, CYCLE_PATH, state)
    _require(state.get("plan") == plan and type(state.get("index")) is int and
             0 <= state["index"] <= len(plan["actions"]), "循环事务与计划不符")
    actions = plan["actions"]
    result = None
    while state["index"] < len(actions):
        action = actions[state["index"]]
        selected = action["plan"]
        if state["phase"] is None:
            state["phase"] = {"purge": "purge", "receipt-cleanup": "receipt"}.get(
                action["kind"]) or ("compact" if action["compact"] else "retire")
            state["current_plan"] = selected
        phase = state["phase"]
        # 终态收据清理会收缩引用图；此后循环不再复核整体引用摘要，只重新计量
        if state.get("digest_released") or action["kind"] == "receipt-cleanup":
            inventory = _inventory(api)
        else:
            inventory = _guard(api, plan)
        if phase == "purge":
            if action["kind"] == "purge" and not _needs(inventory)["bytes_to_target"]:
                state["index"] += 1
                state["phase"] = state["current_plan"] = None
                continue
            if not data_loss:
                state["state"] = "needs_confirmation"
                _write(api, CYCLE_PATH, state)
                return {"state": "needs_confirmation", "data_loss_token": plan.get("data_loss_token"),
                        "needs": _needs(inventory), "notice": "未提供具体永久数据损失令牌；未删除恢复原件。"}
            result = _purge(api, state["current_plan"])
        elif phase == "receipt":
            if not data_loss:
                state["state"] = "needs_confirmation"
                _write(api, CYCLE_PATH, state)
                return {"state": "needs_confirmation", "data_loss_token": plan.get("data_loss_token"),
                        "needs": _needs(inventory), "notice": "未提供具体永久数据损失令牌；终态收据未删除。"}
            result = _receipt_cleanup(api, state["current_plan"])
        elif phase == "compact":
            try:
                result = _compact(api, state["current_plan"])
            except NoProgress as exc:
                if action.get("retire"):
                    state["current_plan"] = _task_plan(api, selected["task_id"], "retire-plan")
                    state["phase"] = "retire"
                    state["rounds"] += 1
                    _write(api, CYCLE_PATH, state)
                    return {"state": "in_progress", "operation": "cycle", "rounds": state["rounds"],
                            "batch": {"unlinked_files": 2, "notice": str(exc)}, "needs": _needs(_inventory(api))}
                state["index"] += 1
                state["phase"] = state["current_plan"] = None
                state.setdefault("blocked_items", []).append({"task_id": selected["task_id"], "reason": str(exc)})
                _write(api, CYCLE_PATH, state)
                return {"state": "in_progress", "operation": "cycle", "rounds": state["rounds"],
                        "batch": {"unlinked_files": 2, "notice": str(exc)}, "needs": _needs(_inventory(api))}
        elif phase == "retire":
            mandatory = action.get("mandatory_retire") or _needs(inventory)["excess_tasks"] > 0
            if not mandatory and not _needs(inventory)["bytes_to_target"]:
                state["index"] += 1
                state["phase"] = state["current_plan"] = None
                continue
            result = _retire(api, state["current_plan"])
        else:
            raise RuntimeError("循环阶段无效")
        state["rounds"] += 1
        if action["kind"] == "receipt-cleanup" and result["state"] == "complete":
            state["digest_released"] = True
        after = _inventory(api) if state.get("digest_released") else _guard(api, plan)
        if result["state"] == "complete":
            if phase == "compact" and action.get("retire") and (
                    action.get("mandatory_retire") or _needs(after)["bytes_to_target"] or _needs(after)["excess_tasks"]):
                task = after.tasks.get(selected["task_id"])
                _require(task is not None, "压缩后的任务丢失")
                rows, _ = _tree(root, task["path"], hashes=False)
                _require({row["path"] for row in rows} == set(action["derived_files"]), "压缩后出现未授权文件")
                packed = _pack(root, task["path"], json.loads(selected["meta_text"]))
                _require(packed["source_token"] == selected["token"] and packed["files"] == selected["files"], "压缩产物来源变化")
                state["current_plan"] = _task_plan(api, selected["task_id"], "retire-plan")
                state["phase"] = "retire"
            elif phase == "retire":
                state["current_plan"] = _recovery_plan(api, result["ticket"])
                state["phase"] = "purge"
            else:
                state["index"] += 1
                state["phase"] = state["current_plan"] = None
        state["state"] = "in_progress"
        _write(api, CYCLE_PATH, state)
        break
    final = _inventory(api)
    needs = _needs(final)
    satisfied = not any(needs.values())
    if state["index"] == len(actions):
        state["state"] = "complete" if satisfied else ("blocked" if plan.get("blockers") or state.get("blocked_items") or not actions else "needs_confirmation")
        _write(api, CYCLE_PATH, state)
        final = _inventory(api)
        needs = _needs(final)
    return {"state": state["state"], "operation": "cycle", "rounds": state["rounds"],
            "action_index": state["index"], "total_actions": len(actions), "batch": result,
            "needs": needs, "total_bytes": final.total_bytes, "target_bytes": final.config["history_target_bytes"],
            "blockers": plan.get("blockers", []), "notice": "重复同一已批准命令续进；计划有限，未见新对象不会获得默认授权。"}


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def _parser():
    parser = _Parser(prog="ag history", add_help=False, allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("compact-plan", "retire-plan", "purge-plan", "compact", "retire", "purge", "restore", "cycle"):
        command = commands.add_parser(name, add_help=False, allow_abbrev=False)
        command.add_argument("--json", action="store_true")
        if name in ("compact-plan", "retire-plan"):
            command.add_argument("--id", required=True)
        elif name == "purge-plan":
            command.add_argument("--ticket", required=True)
        elif name == "restore":
            choice = command.add_mutually_exclusive_group(required=True)
            choice.add_argument("--ticket")
            choice.add_argument("--id")
        else:
            command.add_argument("--plan", required=name != "cycle")
            command.add_argument("--confirm", required=name != "cycle")
            if name in ("purge", "cycle"):
                command.add_argument("--confirm-data-loss")
        if name.endswith("-plan") or name == "cycle":
            command.add_argument("--output")
    return parser


def _external(root, value):
    path = Path(value)
    if not path.is_absolute():
        _require(value == PLAN_PATH, "相对计划路径只能为 " + PLAN_PATH)
        return _safe(root, PLAN_PATH, missing=True), True
    _require(".." not in path.parts, "计划路径不能包含穿越")
    try:
        relative = path.relative_to(root).as_posix()
    except ValueError:
        T._path(path.parent, "dir")
        T._path(path, "file", missing=True)
        return path, False
    _require(relative == PLAN_PATH, "guild 内只允许固定维护计划，避免报告无限增长")
    return _safe(root, PLAN_PATH, missing=True), True


def _load_plan(root, value):
    if value == "-":
        raw = sys.stdin.buffer.read(MAX_CONTROL_BYTES + 1) if hasattr(sys.stdin, "buffer") else sys.stdin.read(MAX_CONTROL_BYTES + 1).encode("utf-8")
    else:
        path, managed = _external(root, value)
        raw = _read(root, PLAN_PATH) if managed else T._read_bytes(path, MAX_CONTROL_BYTES)
    _require(len(raw) <= MAX_CONTROL_BYTES, "计划超过读取上限")
    plan = json.loads(raw.decode("utf-8"), object_pairs_hook=T._json_pairs)
    _verify_seal(plan)
    return plan


def _output(api, plan, value):
    if value is None or value == "-":
        return
    root = H._root(api)
    path, managed = _external(root, value)
    if managed:
        _write(api, PLAN_PATH, plan)
    else:
        _require(not path.exists(), "外部计划文件已存在，拒绝覆盖")
        data = _bytes(plan)
        _require(len(data) <= MAX_CONTROL_BYTES, "计划超过大小上限")
        T._write_bytes(path, data)


def run(args, api):
    try:
        parsed = _parser().parse_args(list(args))
        root = H._root(api)
        with H._lock(api, root):
            command = parsed.command
            if command in ("compact-plan", "retire-plan"):
                value = _task_plan(api, parsed.id, command)
                _output(api, value, parsed.output)
            elif command == "purge-plan":
                value = _recovery_plan(api, parsed.ticket)
                _output(api, value, parsed.output)
            elif command == "restore":
                value = _restore(api, parsed.ticket, parsed.id)
            elif command == "cycle" and parsed.plan is None:
                _require(parsed.confirm is None and parsed.confirm_data_loss is None, "确认令牌必须与具体 --plan 同时使用")
                value = _cycle_plan(api)
                _output(api, value, parsed.output)
            else:
                _require(not getattr(parsed, "output", None), "执行模式不接受 --output")
                value = _load_plan(root, parsed.plan)
                _require(parsed.confirm == value["token"], "--confirm 必须精确匹配已审阅计划 token")
                data_loss = getattr(parsed, "confirm_data_loss", None)
                if command == "purge":
                    _require(data_loss == value.get("data_loss_token") and data_loss is not None,
                             "永久清空必须另给精确 --confirm-data-loss 令牌")
                elif data_loss is not None:
                    _require(data_loss == value.get("data_loss_token"), "永久数据损失令牌不匹配")
                if command == "cycle":
                    value = _cycle(api, value, data_loss is not None)
                else:
                    value = {"compact": _compact, "retire": _retire, "purge": _purge}[command](api, value)
        print(json.dumps(value, ensure_ascii=False, indent=2))
        return 0 if value.get("state") not in ("blocked", "needs_confirmation") else 2
    except (OSError, RuntimeError, ValueError, UnicodeError, KeyError, TypeError, T.TaskError, zipfile.BadZipFile) as exc:
        print(json.dumps({"error": str(exc), "completed": False,
                          "notice": "已中止；原件、ZIP 或受管事务仍保留。只允许重试同一明确批准计划，不会处理新增文件。"},
                         ensure_ascii=False), file=sys.stderr)
        return 1


def preview_cycle(api):
    """唯一的启动/结束预览：纯元信息、只计数；needs 不携带任务 ID 或上下文进入默认启动缓存。"""
    inventory = _inventory(api)
    counts = {"compact": 0, "retire": 0, "purge": 0, "receipt_cleanup": 0, "protected": 0}
    tasks = sorted((task for task in inventory.tasks.values() if not task["active"]),
                   key=lambda task: (task["closed_at"], task["id"]))
    surplus = max(0, len(tasks) - inventory.config["history_max_tasks"])
    pressure = inventory.total_bytes > inventory.config["history_target_bytes"]
    for index, task in enumerate(tasks):
        age = (inventory.now - task["closed_at"]).total_seconds() / 86400
        compact = age >= inventory.config["history_full_days"] and not task["packed"]
        retire = age >= inventory.config["history_retention_days"] or index < surplus or pressure
        if age < inventory.config["history_full_days"] or not (compact or retire):
            continue
        if task["held"] or inventory.task_referenced(task):
            counts["protected"] += 1
            continue
        if compact:
            counts["compact"] += 1
        if retire:
            counts["retire"] += 1
    for ticket in inventory.children("history/retired"):
        receipt = _read_json(inventory.root, "history/retired/" + ticket + "/receipt.json")
        if receipt.get("state") == "retired":
            counts["purge"] += 1
        elif receipt.get("state") in TERMINAL_RECEIPT_STATES:
            counts["receipt_cleanup"] += 1
    for ticket in inventory.children("history/backups"):
        if HEX.fullmatch(ticket):
            counts["purge"] += 1
    needs = _needs(inventory)
    return {"counts": counts,
            "needs": {"bytes_to_target": needs["bytes_to_target"], "excess_tasks": needs["excess_tasks"],
                      "expired_tasks": len(needs["expired_tasks"]),
                      "full_detail_tasks": len(needs["full_detail_tasks"])},
            "needs_confirmation": bool(sum(counts[key] for key in
                                           ("compact", "retire", "purge", "receipt_cleanup"))),
            "over_budget": inventory.total_bytes > inventory.config["history_max_bytes"],
            "maintenance_reserve_bytes": MAINTENANCE_RESERVE_BYTES,
            "applied": False}
