"""
BiliYouTik2Brain — 集成中心 (v4.0)

统一外部集成入口。所有集成默认关闭，通过配置逐项开启。
支持: 记忆系统 / Obsidian / Notion
"""

import os
from typing import Dict, List, Optional, Any

from .integration_config import (
    load_integration_config, save_integration_config,
    is_integration_enabled, get_enabled_integrations,
    enable_integration, disable_integration,
    SUPPORTED_INTEGRATIONS,
)


# ═══════════════════════════════════════════════════════════
#  集成基类
# ═══════════════════════════════════════════════════════════

class BaseIntegration:
    """集成基类"""

    name: str = "base"

    def is_available(self) -> bool:
        """检查是否可用（依赖 + 配置）"""
        return False

    def push(self, data: Dict) -> Dict:
        """
        推送数据

        Args:
            data: {bvid, video_title, uploader, transcript, summary, keywords, ...}

        Returns:
            {success: bool, message: str, ...}
        """
        raise NotImplementedError

    def pull(self, query: Dict = None) -> Any:
        """拉取数据（可选）"""
        raise NotImplementedError


# ═══════════════════════════════════════════════════════════
#  记忆系统集成
# ═══════════════════════════════════════════════════════════

class MemorySystemIntegration(BaseIntegration):
    name = "memory_system"

    def is_available(self) -> bool:
        # 检查 MEMORY.md 和 memory/ 目录
        mem = os.path.expanduser("~/openclaw/workspace/MEMORY.md")
        return os.path.exists(mem)

    def push(self, data: Dict) -> Dict:
        """将转录知识推送到记忆系统"""
        if not self.is_available():
            return {"success": False, "message": "记忆系统不可用"}

        try:
            video_title = data.get("video_title", "")
            bvid = data.get("bvid", "")
            summary = data.get("summary", "")
            keywords = data.get("keywords", [])
            domain = data.get("domain", "")

            # 写入当天日记
            from datetime import datetime
            date_str = datetime.now().strftime("%Y-%m-%d")
            daily_path = os.path.expanduser(f"~/openclaw/workspace/memory/{date_str}.md")
            os.makedirs(os.path.dirname(daily_path), exist_ok=True)

            entry = f"""
### 📹 {video_title}
- **平台**: bilibili | **BV**: {bvid}
- **领域**: {domain or '未分类'}
- **摘要**: {summary[:200] if summary else '无'}
- **关键词**: {', '.join(keywords[:5]) if keywords else '无'}
"""
            with open(daily_path, "a", encoding="utf-8") as f:
                f.write(entry)

            return {
                "success": True,
                "message": f"已写入 {daily_path}",
                "path": daily_path,
            }
        except Exception as e:
            return {"success": False, "message": str(e)}


# ═══════════════════════════════════════════════════════════
#  Obsidian 集成
# ═══════════════════════════════════════════════════════════

class ObsidianIntegration(BaseIntegration):
    name = "obsidian"

    def is_available(self) -> bool:
        vault = os.environ.get("B2T_OBSIDIAN_VAULT")
        return bool(vault and os.path.isdir(vault))

    def push(self, data: Dict) -> Dict:
        """推送笔记到 Obsidian vault"""
        vault = os.environ.get("B2T_OBSIDIAN_VAULT")
        if not vault or not os.path.isdir(vault):
            return {"success": False, "message": "Obsidian vault 未配置"}

        try:
            subdir = os.path.join(vault, "biliyoutik2brain")
            os.makedirs(subdir, exist_ok=True)

            video_title = data.get("video_title", "unknown")
            bvid = data.get("bvid", "")
            # 安全文件名
            safe = video_title.replace("/", "_").replace(":", "_")[:60]
            filename = f"{safe}_{bvid}.md"
            filepath = os.path.join(subdir, filename)

            content = f"""# {video_title}

> 来源: bilibili | BV: {bvid}
> UP主: {data.get('uploader', '')}

## 摘要
{data.get('summary', '')}

## 关键词
{', '.join(data.get('keywords', []))}

## 转录
{data.get('transcript', '')[:5000]}
"""
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            return {
                "success": True,
                "message": f"已保存到 {filepath}",
                "path": filepath,
            }
        except Exception as e:
            return {"success": False, "message": str(e)}


# ═══════════════════════════════════════════════════════════
#  Notion 集成
# ═══════════════════════════════════════════════════════════

class NotionIntegration(BaseIntegration):
    name = "notion"

    def is_available(self) -> bool:
        return bool(os.environ.get("NOTION_API_KEY") and os.environ.get("B2T_NOTION_DB_ID"))

    def push(self, data: Dict) -> Dict:
        """推送页面到 Notion 数据库"""
        token = os.environ.get("NOTION_API_KEY")
        db_id = os.environ.get("B2T_NOTION_DB_ID")

        if not token or not db_id:
            return {"success": False, "message": "Notion API 未配置"}

        try:
            import requests
            from datetime import datetime

            session = requests.Session()
            session.headers.update({
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            })

            video_title = data.get("video_title", "")
            payload = {
                "parent": {"database_id": db_id},
                "properties": {
                    "Name": {"title": [{"text": {"content": video_title[:100]}}]},
                    "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
                    "Tags": {
                        "multi_select": [
                            {"name": kw[:20]} for kw in data.get("keywords", [])[:5]
                        ]
                    },
                    "BV": {"rich_text": [{"text": {"content": data.get("bvid", "")}}]},
                },
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": data.get("summary", "")[:500]}}]
                        },
                    },
                ],
            }

            r = session.post("https://api.notion.com/v1/pages", json=payload)
            if r.status_code in (200, 201):
                return {
                    "success": True,
                    "message": f"已创建 Notion 页面",
                    "url": r.json().get("url", ""),
                }
            else:
                return {
                    "success": False,
                    "message": f"Notion API: HTTP {r.status_code}",
                }

        except ImportError:
            return {"success": False, "message": "requests 库未安装"}
        except Exception as e:
            return {"success": False, "message": str(e)}


# ═══════════════════════════════════════════════════════════
#  集成注册
# ═══════════════════════════════════════════════════════════

_INTEGRATIONS: Dict[str, BaseIntegration] = {}


def _init():
    if _INTEGRATIONS:
        return
    for cls in [MemorySystemIntegration, ObsidianIntegration, NotionIntegration]:
        inst = cls()
        _INTEGRATIONS[inst.name] = inst


def push_to_all(data: Dict) -> Dict[str, Dict]:
    """
    向所有已启用的集成推送数据。

    这是管线的主入口: 转录完成后调用此函数。
    """
    _init()
    enabled = get_enabled_integrations()
    results = {}

    for item in enabled:
        name = item["name"]
        integration = _INTEGRATIONS.get(name)
        if not integration:
            results[name] = {"success": False, "message": "集成未找到"}
            continue

        results[name] = integration.push(data)

    return results


def push_to(name: str, data: Dict) -> Dict:
    """向指定集成推送数据"""
    _init()
    if not is_integration_enabled(name):
        return {"success": False, "message": f"{name} 未启用"}

    integration = _INTEGRATIONS.get(name)
    if not integration:
        return {"success": False, "message": f"{name} 未实现"}

    return integration.push(data)


def check_all_available() -> Dict[str, bool]:
    """检查所有集成的可用性"""
    _init()
    return {name: inst.is_available() for name, inst in _INTEGRATIONS.items()}
