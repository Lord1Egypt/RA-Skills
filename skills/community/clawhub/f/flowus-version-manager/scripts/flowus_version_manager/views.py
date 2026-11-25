"""Human-readable generated catalogs; directory records remain authoritative."""
from __future__ import annotations

from .common import Conflict, GateError, ManagerError, atomic_json, digest, now, stable_id
from .store import plain, rich

VIEWS = {"latest": "最新版", "history": "历史版本", "review": "待确认"}
MARKER = "文件管理器自动生成的目录。"


def provision_views(config, path, writer):
    pages = config.setdefault("view_pages", {})
    for key, title in VIEWS.items():
        if key in pages:
            continue
        body = {"parent": {"page_id": config["business_parent_id"]},
                "properties": {"title": {"type": "title", "title": rich(title)}},
                "children": [{"object": "block", "type": "paragraph",
                              "paragraph": {"rich_text": rich(MARKER + "\n尚无已完成校验的文件。")}}]}
        page, _ = writer.request("POST", "/pages", body,
                                 idempotency=stable_id(config["vault_id"], "catalog", key))
        pages[key] = page["id"]
        atomic_json(path, config)


def refresh(manager, *, dry_run=False):
    pages = manager.config.get("view_pages", {})
    if set(pages) != set(VIEWS):
        return {"status": "not_configured", "next": "Run init --provision to create catalog pages"}
    documents = manager.store.list("documents")
    versions = manager.store.list("versions")
    signature = digest([(r.id, r.data) for r in documents + versions])
    version_map = {r.key: r for r in versions if r.data.get("upload_state") == "verified" and r.data.get("kind") != "probe"}
    latest = []
    for document in documents:
        key = document.data.get("latest")
        if document.data.get("status") != "active" or not key:
            continue
        version = version_map.get(key)
        if not version or version.data.get("document_key") != document.key:
            raise Conflict("Catalog cannot publish a missing or unverified latest version")
        latest.append(version)
    rows = {"latest": latest, "history": sorted(version_map.values(), key=lambda r: r.data.get("version_sort", 0), reverse=True),
            "review": [r for r in version_map.values() if r.data.get("status") == "needs_review"]}
    if dry_run:
        return {"dry_run": True, "counts": {key: len(value) for key, value in rows.items()}}
    manager.guard()
    for key, items in rows.items():
        blocks = manager.store.children(pages[key])
        owned = [block for block in blocks if block.get("type") == "paragraph"
                 and plain(block.get("paragraph", {}).get("rich_text")).startswith(MARKER)]
        if len(owned) != 1:
            raise GateError("Generated catalog marker was changed or duplicated; preserving the page for review")
        text = rich(f"{MARKER}\n更新于 {now()}\n共 {len(items)} 条；完整记录见下方数据库。\n")
        for item in items[:30]:
            label = item.data.get("original_name") or item.data.get("title") or item.key
            text.append({"type": "text", "text": {"content": label, "link": {"url": item.url}}})
            text.extend(rich(" · " + str(item.data.get("version_label", "")) +
                             (" · " + str(item.data.get("reason", "待确认")) if key == "review" else "") + "\n"))
        database = manager.config['databases']['documents' if key == 'latest' else 'versions']
        text.append({"type": "text", "text": {"content": "打开完整记录", "link": {"url": "https://flowus.cn/" + database}}})
        manager.store.writer.request("PATCH", "/blocks/" + owned[0]["id"],
                                      {"type": "paragraph", "paragraph": {"rich_text": text}})
    after = manager.store.list("documents") + manager.store.list("versions")
    changed = digest([(r.id, r.data) for r in after]) != signature
    return {"status": "refreshed", "counts": {key: len(value) for key, value in rows.items()},
            "changed_during_refresh": changed,
            "urls": {key: "https://flowus.cn/" + value for key, value in pages.items()}}


def after_write(manager, result):
    if not manager.config.get("view_pages"):
        return result
    try:
        result['catalogs'] = refresh(manager)
    except ManagerError as error:
        # A derived catalog failure must not disguise an already committed file operation.
        result['catalogs'] = {'status': 'needs_refresh', 'error': error.code, 'message': str(error)}
    return result
