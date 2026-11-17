"""
BiliYouTik2Brain — 同步适配器注册表 (v4.0)

桥接 sync_config.py 与各同步目标的实际适配器实现。
支持: GitHub / Obsidian / Notion / 本地文件系统 (NAS)
"""

import os
from typing import Dict, List, Optional


# ═══════════════════════════════════════════════════════════
#  适配器基类
# ═══════════════════════════════════════════════════════════

class BaseSyncAdapter:
    """同步适配器基类"""

    name: str = "base"

    def is_configured(self) -> bool:
        """检查是否已配置"""
        return False

    def sync(self, files: List[Dict], config: Dict) -> Dict:
        """
        执行同步

        Args:
            files: [{path, content}] — 要同步的文件列表
            config: 目标配置

        Returns:
            {synced: int, failed: int, details: [...]}
        """
        raise NotImplementedError


# ═══════════════════════════════════════════════════════════
#  文件系统适配器（NAS / 本地目录）
# ═══════════════════════════════════════════════════════════

class FileSystemSync(BaseSyncAdapter):
    name = "filesystem"

    def __init__(self):
        self._target_dir = ""

    def is_configured(self) -> bool:
        return bool(self._target_dir) or bool(os.environ.get("B2T_SYNC_DIR"))

    def sync(self, files: List[Dict], config: Dict) -> Dict:
        target = config.get("path") or os.environ.get("B2T_SYNC_DIR")
        if not target:
            return {"synced": 0, "failed": len(files), "error": "目标路径未配置"}

        synced, failed, details = 0, 0, []
        os.makedirs(target, exist_ok=True)

        for f in files:
            try:
                dest = os.path.join(target, os.path.basename(f["path"]))
                with open(dest, "w", encoding="utf-8") as fh:
                    fh.write(f.get("content", ""))
                synced += 1
                details.append({"path": dest, "status": "ok"})
            except OSError as e:
                failed += 1
                details.append({"path": f["path"], "status": "error", "error": str(e)})

        return {"synced": synced, "failed": failed, "details": details}


# ═══════════════════════════════════════════════════════════
#  GitHub 适配器
# ═══════════════════════════════════════════════════════════

class GitHubSync(BaseSyncAdapter):
    name = "github"

    def __init__(self):
        self._repo = None
        self._token = None

    def is_configured(self) -> bool:
        return bool(os.environ.get("GITHUB_TOKEN") and os.environ.get("B2T_GITHUB_REPO"))

    def sync(self, files: List[Dict], config: Dict) -> Dict:
        repo = config.get("repo") or os.environ.get("B2T_GITHUB_REPO")
        token = config.get("token") or os.environ.get("GITHUB_TOKEN")
        branch = config.get("branch", "main")
        base_path = config.get("base_path", "transcripts/")

        if not repo or not token:
            return {"synced": 0, "failed": len(files), "error": "GitHub repo 或 token 未配置"}

        synced, failed, details = 0, 0, []

        try:
            import requests, base64

            session = requests.Session()
            session.headers.update({
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            })
            api_base = "https://api.github.com"

            for f in files:
                try:
                    file_path = base_path + os.path.basename(f["path"])
                    content_b64 = base64.b64encode(f["content"].encode("utf-8")).decode()

                    # 检查文件是否已存在（获取 sha）
                    sha = None
                    get_url = f"{api_base}/repos/{repo}/contents/{file_path}?ref={branch}"
                    r = session.get(get_url)
                    if r.status_code == 200:
                        sha = r.json().get("sha")

                    payload = {
                        "message": f"[biliyoutik2brain] {os.path.basename(f['path'])}",
                        "content": content_b64,
                        "branch": branch,
                    }
                    if sha:
                        payload["sha"] = sha

                    r = session.put(get_url, json=payload)
                    if r.status_code in (200, 201):
                        synced += 1
                        details.append({
                            "path": f"https://github.com/{repo}/blob/{branch}/{file_path}",
                            "status": "ok",
                        })
                    else:
                        failed += 1
                        details.append({
                            "path": file_path,
                            "status": "error",
                            "error": f"HTTP {r.status_code}: {r.json().get('message', '')}",
                        })
                except Exception as e:
                    failed += 1
                    details.append({"path": f["path"], "status": "error", "error": str(e)})

        except ImportError:
            return {"synced": 0, "failed": len(files), "error": "requests 库未安装"}

        return {"synced": synced, "failed": failed, "details": details}


# ═══════════════════════════════════════════════════════════
#  Obsidian 适配器
# ═══════════════════════════════════════════════════════════

class ObsidianSync(BaseSyncAdapter):
    name = "obsidian"

    def is_configured(self) -> bool:
        return bool(os.environ.get("B2T_OBSIDIAN_VAULT"))

    def sync(self, files: List[Dict], config: Dict) -> Dict:
        vault = config.get("vault_path") or os.environ.get("B2T_OBSIDIAN_VAULT")
        if not vault or not os.path.isdir(vault):
            return {"synced": 0, "failed": len(files), "error": "Obsidian vault 路径不存在"}

        subdir = config.get("subdir", "biliyoutik2brain")
        target = os.path.join(vault, subdir)
        os.makedirs(target, exist_ok=True)

        synced, failed, details = 0, 0, []
        for f in files:
            try:
                dest = os.path.join(target, os.path.basename(f["path"]))
                with open(dest, "w", encoding="utf-8") as fh:
                    fh.write(f.get("content", ""))
                synced += 1
                details.append({"path": dest, "status": "ok"})
            except OSError as e:
                failed += 1
                details.append({"path": f["path"], "status": "error", "error": str(e)})

        return {"synced": synced, "failed": failed, "details": details}


# ═══════════════════════════════════════════════════════════
#  Notion 适配器
# ═══════════════════════════════════════════════════════════

class NotionSync(BaseSyncAdapter):
    name = "notion"

    def is_configured(self) -> bool:
        return bool(os.environ.get("NOTION_API_KEY") and os.environ.get("B2T_NOTION_DB_ID"))

    def sync(self, files: List[Dict], config: Dict) -> Dict:
        token = config.get("token") or os.environ.get("NOTION_API_KEY")
        db_id = config.get("database_id") or os.environ.get("B2T_NOTION_DB_ID")

        if not token or not db_id:
            return {"synced": 0, "failed": len(files), "error": "Notion API Key 或 Database ID 未配置"}

        synced, failed, details = 0, 0, []

        try:
            import requests
            from datetime import datetime

            session = requests.Session()
            session.headers.update({
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            })

            for f in files:
                try:
                    title = os.path.splitext(os.path.basename(f["path"]))[0]
                    content = f.get("content", "")[:2000]

                    payload = {
                        "parent": {"database_id": db_id},
                        "properties": {
                            "Name": {"title": [{"text": {"content": title}}]},
                            "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
                            "Content": {
                                "rich_text": [{"text": {"content": content[:1000]}}]
                            },
                        },
                    }

                    r = session.post(
                        "https://api.notion.com/v1/pages",
                        json=payload,
                    )

                    if r.status_code in (200, 201):
                        synced += 1
                        details.append({
                            "path": r.json().get("url", title),
                            "status": "ok",
                        })
                    else:
                        failed += 1
                        details.append({
                            "path": title,
                            "status": "error",
                            "error": f"HTTP {r.status_code}: {r.json().get('message', '')}",
                        })
                except Exception as e:
                    failed += 1
                    details.append({"path": f["path"], "status": "error", "error": str(e)})

        except ImportError:
            return {"synced": 0, "failed": len(files), "error": "requests 库未安装"}

        return {"synced": synced, "failed": failed, "details": details}


# ═══════════════════════════════════════════════════════════
#  适配器注册
# ═══════════════════════════════════════════════════════════

_ADAPTERS: Dict[str, BaseSyncAdapter] = {}


def _init_adapters():
    """延迟初始化所有适配器"""
    if _ADAPTERS:
        return
    for cls in [FileSystemSync, GitHubSync, ObsidianSync, NotionSync]:
        adapter = cls()
        _ADAPTERS[adapter.name] = adapter


def get_adapter(name: str) -> Optional[BaseSyncAdapter]:
    """获取同步适配器实例"""
    _init_adapters()
    return _ADAPTERS.get(name)


def list_adapters() -> Dict[str, bool]:
    """列出所有适配器及其配置状态"""
    _init_adapters()
    return {name: adapter.is_configured() for name, adapter in _ADAPTERS.items()}
