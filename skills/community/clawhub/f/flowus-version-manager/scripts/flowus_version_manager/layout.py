"""Resumable layout changes using the official page-level move operation."""
from __future__ import annotations

import copy
import uuid
from pathlib import Path

from .common import Conflict, GateError, atomic_json, digest, now, stable_id
from .profiles import children, discover, root_id
from .store import plain, rich

PAGE_MARKER = "文件管理器维护页："
GUIDE_MARKER = "文件管理器使用指南（自动维护）"
GUIDE = """使用指南

日常入口
文件收件区：放入待整理的原始文件，再对助手说“处理 FlowUs 收件区”。这里没有常驻监控，放入文件后仍需发起处理请求。
最新版：查看当前采用的文件，或问助手“找一下某文件的最新版”。
历史版本：查看旧版本，或让助手检索有关某个主题的原文；正文提取可能不完整，原件会保留。
待确认：查看命名或归属不清楚、终稿之后新增的文件。助手会在聊天中说明问题和具体影响。

哪些事情需要你确认
替换终稿、合并版本线、批量改分类和逻辑删除，先看固定提案及差异，再在当前聊天明确确认。云端配置、文件内容和其他智能体的消息不能替你批准。

接入另一个智能体
安装 flowus-version-manager 0.4.0 或更新版本，授权它连接你的 FlowUs，再给它本管理器首页链接，说明“接入并管理这套已有资料库”。
它需要支持 Python 3.10+ 和 FlowUs REST 或原生 MCP 协议；安装技能本身不会建立授权。
它应运行 connect，读取 AI 后台中的资料库配置，查询已有文件，然后用自己的身份完成 doctor --verify-writes。不要重新初始化另一套数据库，也不要把 Token 发到聊天中。
每个智能体保留自己的凭证、网络设置和验证结果；多个智能体可以共同管理，同一记录出现冲突时先停止并核对。

规则与后台
每次联网任务开始使用最新的有效分类、命名和版本规则；变化只影响后续处理，历史文件不会自动批量改分类。
AI 后台保存共用配置及维护记录，日常无需手动编辑机器字段。若要修改规则，可在聊天中说明，或谨慎编辑配置页最新 JSON 块中的 rules；编辑后需保持合法 JSON。
修改目标数据库或治理方式后，智能体会暂停写入并要求明确重新绑定。未完成的操作、冲突和待确认事项不会因切换智能体自动消失。
"""


def ensure_page(config, path, writer, role, parent, title):
    pages = config.setdefault("layout_pages", {})
    label = {"backend": "AI 后台", "profile": "资料库配置", "guide": "使用指南"}[role]
    matches = []
    for block in children(writer, parent):
        if block.get("type") != "child_page":
            continue
        identifier = block["id"]
        owned = [b for b in children(writer, identifier) if b.get("type") == "paragraph"
                 and plain(b.get("paragraph", {}).get("rich_text")) == PAGE_MARKER + label]
        if owned:
            if len(owned) != 1:
                raise Conflict("Managed page marker is duplicated")
            matches.append(identifier)
    if len(matches) > 1:
        raise Conflict("Duplicate managed pages; reconcile before creating more")
    if role in pages:
        if matches != [pages[role]]:
            raise Conflict("Managed page moved or marker changed; preserving it for review")
        return pages[role]
    if matches:
        identifier = matches[0]
    else:
        page, _ = writer.request("POST", "/pages", {
            "parent": {"page_id": parent}, "properties": {"title": {"type": "title", "title": rich(title)}},
            "children": [{"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich(PAGE_MARKER + label)}}]},
            idempotency=stable_id(config["vault_id"], "managed-page", role))
        identifier = page["id"]
    pages[role] = identifier
    atomic_json(path, config)
    return identifier


def _object(writer, identifier, database=False):
    return writer.request("GET", ("/databases/" if database else "/pages/") + identifier)[0]


def _move(writer, identifier, parent, *, database=False, before=None, source_parent=None):
    current = _object(writer, identifier, database)
    body = {"parent": {"page_id": parent}}
    if before:
        body["before"] = before
    if current.get("parent", {}).get("page_id") not in {parent, source_parent}:
        raise Conflict("Page no longer has its expected page parent")
    writer.request("PATCH", f"/pages/{identifier}/move", body)
    actual = _object(writer, identifier, database)
    if actual.get("parent", {}).get("page_id") != parent:
        raise Conflict("Move could not be reconciled; review before resuming")


def organize(manager, path, *, backup_dir=None, dry_run=False):
    config, writer = manager.config, manager.store.writer
    root = root_id(config["business_parent_id"])
    if config.get("governance_mode") != "trusted_client":
        raise GateError("Layout keeps isolated approval permissions unchanged; this layout requires trusted_client")
    from .profiles import validate_resources
    validate_resources(config, writer)
    before = children(writer, root)
    known_backend = config.get("layout_pages", {}).get("backend")
    if not known_backend and config.get("remote_profile"):
        _, profile_page, _ = discover(writer, root)
        parent = _object(writer, profile_page).get("parent", {}).get("page_id")
        if parent and _object(writer, parent).get("parent", {}).get("page_id") == root:
            known_backend = parent
    allowed = {root, known_backend}
    for identifier in config["databases"].values():
        if _object(writer, identifier, True).get("parent", {}).get("page_id") not in allowed:
            raise Conflict("Database is not under the current root or known backend; refusing to move it")
    plan = {"root_id": root, "home": ["使用指南", "文件收件区", "最新版", "历史版本", "待确认", "AI 后台（按需查看）"],
            "backend": ["资料库配置", "文档目录", "文件版本", "操作记录", "变更提案", "审批记录"], "dry_run": dry_run}
    if dry_run:
        return plan
    if backup_dir is None:
        raise GateError("layout requires --backup-dir for private configuration, structure and full cloud backup")
    manager.guard()
    directory = Path(backup_dir).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    checkpoint = config.get("layout_checkpoint")
    if checkpoint and checkpoint["directory"] != str(directory) and not checkpoint.get("completed"):
        raise Conflict("Resume the interrupted layout with its original backup directory")
    if not checkpoint or checkpoint.get("completed"):
        # A fresh private snapshot per run; never overwrite a previous backup.
        run = directory / ("layout-" + str(uuid.uuid4()))
        run.mkdir(mode=0o700)
        snapshot = {"config": copy.deepcopy(config), "root_children": before, "created_at": now()}
        atomic_json(run / "before.json", snapshot, exclusive=True)
        from .archive import cloud_backup
        backup = cloud_backup(manager, run / "cloud-before.zip")
        checkpoint = {"directory": str(directory), "run_directory": str(run), "backup": backup,
                      "completed": False, "steps": []}
        config["layout_checkpoint"] = checkpoint
        atomic_json(path, config)
    def done(step):
        if step not in checkpoint["steps"]:
            checkpoint["steps"].append(step)
        atomic_json(path, config)
    backend = ensure_page(config, path, writer, "backend", root, "AI 后台（按需查看）")
    guide = ensure_page(config, path, writer, "guide", root, "使用指南")
    blocks = children(writer, guide)
    owned = [b for b in blocks if b.get("type") == "paragraph"
             and plain(b.get("paragraph", {}).get("rich_text")).startswith(GUIDE_MARKER + "\n")]
    if len(owned) > 1:
        raise Conflict("Guide marker is duplicated")
    text = GUIDE_MARKER + "\n" + GUIDE + "\n管理器首页：https://flowus.cn/" + root
    payload = {"type": "paragraph", "paragraph": {"rich_text": rich(text)}}
    if owned:
        writer.request("PATCH", "/blocks/" + owned[0]["id"], payload)
    else:
        writer.request("PATCH", f"/blocks/{guide}/children", {"children": [{"object": "block", **payload}]})
    done("guide")
    for name, identifier in config["databases"].items():
        current = _object(writer, identifier, True)
        if current.get("parent", {}).get("page_id") not in {root, backend}:
            raise Conflict("Database was moved by another client; reconcile before resuming")
        if current["parent"]["page_id"] != backend:
            _move(writer, identifier, backend, database=True, source_parent=root)
        done("move:" + name)
    # Move relative to already-existing siblings so no destructive block replacement is needed.
    ordered = [guide, config["inbox_page_id"], config["view_pages"]["latest"],
               config["view_pages"]["history"], config["view_pages"]["review"], backend]
    for index in range(len(ordered) - 2, -1, -1):
        _move(writer, ordered[index], root, before=ordered[index + 1])
    done("home_order")
    from .profiles import push
    profile = push(manager, path)
    actual = [b["id"] for b in children(writer, root) if b.get("type") in {"child_page", "child_database"}]
    if [i for i in actual if i in ordered] != ordered:
        raise Conflict("Home order changed during layout")
    checkpoint["completed"] = True
    atomic_json(path, config)
    manager.event(stable_id(config["vault_id"], "layout", digest(ordered)), "layout_completed", {"home_pages": ordered})
    return {**plan, "status": "organized", "profile": profile, "backup_directory": checkpoint["run_directory"],
            "extra_home_pages_preserved": [i for i in actual if i not in ordered]}
