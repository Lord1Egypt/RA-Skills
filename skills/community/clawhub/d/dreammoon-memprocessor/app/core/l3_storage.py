"""L3 冷存储 - Markdown文件系统实现"""
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import aiofiles

from app.config import settings
from app.models import DailySummary, MemoryItem, MemoryLevel


class L3ColdStorage:
    """L3冷存储 - Markdown文件系统"""
    
    def __init__(self):
        self.daily_dir = settings.L3_DAILY_DIR
        self.projects_dir = settings.L3_PROJECTS_DIR
        self.decisions_dir = settings.L3_DECISIONS_DIR
        self.memory_file = settings.L3_MEMORY_DIR / "MEMORY.md"
    
    async def init(self):
        """初始化目录"""
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.decisions_dir.mkdir(parents=True, exist_ok=True)
        settings.L3_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        
        # 创建MEMORY.md如果不存在
        if not self.memory_file.exists():
            await self._write_file(self.memory_file, self._get_memory_template())
        
        print(f"[L3] File storage initialized: {settings.L3_MEMORY_DIR}")
    
    async def save_daily_summary(self, summary: DailySummary) -> Path:
        """保存每日摘要"""
        await self.init()
        
        file_path = self.daily_dir / f"{summary.date}.md"
        content = self._format_daily_summary(summary)
        
        await self._write_file(file_path, content)
        print(f"[L3] Daily summary saved: {file_path}")
        
        return file_path
    
    async def append_to_memory(self, item: MemoryItem, section: str = "general"):
        """追加到MEMORY.md"""
        await self.init()
        
        # 读取现有内容
        content = await self._read_file(self.memory_file)
        
        # 生成条目
        entry = self._format_memory_entry(item, section)
        
        # 追加到对应section
        if section == "decisions":
            content = self._append_to_section(content, "## 重要决策", entry)
        elif section == "lessons":
            content = self._append_to_section(content, "## 学到的内容", entry)
        elif section == "projects":
            content = self._append_to_section(content, "## 项目里程碑", entry)
        else:
            content = content + "\n" + entry
        
        await self._write_file(self.memory_file, content)
        print(f"[L3] Appended to MEMORY.md: {item.key}")
    
    async def save_decision(self, item: MemoryItem):
        """保存决策到专门文件"""
        await self.init()
        
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        file_path = self.decisions_dir / f"{date_str}.md"
        
        entry = f"""### {item.key}

- **时间**: {item.created_at.isoformat()}
- **重要性**: {item.importance}/100
- **内容**: {item.content[:200]}...

**元数据**: {json.dumps(item.metadata, ensure_ascii=False, indent=2)}

---

"""
        
        # 追加模式
        async with aiofiles.open(file_path, mode='a', encoding='utf-8') as f:
            await f.write(entry)
        
        print(f"[L3] Decision saved: {file_path}")
    
    async def get_recent(self, days: int = 7) -> List[Dict]:
        """获取最近的每日摘要"""
        await self.init()
        
        files = sorted(self.daily_dir.glob("*.md"), reverse=True)
        recent_files = files[:days]
        
        results = []
        for file_path in recent_files:
            content = await self._read_file(file_path)
            date = file_path.stem
            results.append({"date": date, "content": content})
        
        return results
    
    async def search_content(self, query: str, days: int = 30) -> List[Dict]:
        """在最近的文件中搜索内容"""
        await self.init()
        
        files = sorted(self.daily_dir.glob("*.md"), reverse=True)
        recent_files = files[:days]
        
        results = []
        for file_path in recent_files:
            content = await self._read_file(file_path)
            if query.lower() in content.lower():
                # 找到匹配位置附近的内容
                idx = content.lower().find(query.lower())
                preview = content[max(0, idx-100):min(len(content), idx+200)]
                results.append({
                    "date": file_path.stem,
                    "preview": preview,
                    "file": str(file_path)
                })
        
        return results
    
    async def stats(self) -> Dict:
        """统计信息"""
        await self.init()
        
        daily_files = list(self.daily_dir.glob("*.md"))
        decision_files = list(self.decisions_dir.glob("*.md"))
        
        return {
            "daily_files": len(daily_files),
            "decision_files": len(decision_files),
            "total_files": len(daily_files) + len(decision_files)
        }
    
    # ==================== 格式化方法 ====================
    
    def _format_daily_summary(self, summary: DailySummary) -> str:
        """格式化每日摘要"""
        lines = [
            f"# 📅 {summary.date}",
            "",
            f"> 生成时间: {summary.generated_at.isoformat()}",
            ""
        ]
        
        # 概述
        if summary.overview:
            lines.extend(["## 概述", "", summary.overview, ""])
        
        # 活动
        if summary.activities:
            lines.extend(["## 今日活动", ""])
            for activity in summary.activities:
                lines.append(f"- **{activity.get('time', 'N/A')}**: {activity.get('description', '')}")
                if activity.get('importance', 0) >= 70:
                    lines.append(f"  > 💡 **重要**: {activity.get('insight', '')}")
            lines.append("")
        
        # 决策
        if summary.decisions:
            lines.extend(["## 关键决策", ""])
            for decision in summary.decisions:
                lines.append(f"### {decision.get('topic', '决策')}")
                lines.append(f"- **结论**: {decision.get('conclusion', '')}")
                lines.append(f"- **原因**: {decision.get('reasoning', '')}")
                lines.append(f"- **时间**: {decision.get('timestamp', '')}")
                lines.append("")
        
        # 学到的内容
        if summary.lessons:
            lines.extend(["## 学到的内容", ""])
            for lesson in summary.lessons:
                lines.append(f"- {lesson.get('content', '')}")
                if lesson.get('context'):
                    lines.append(f"  - 背景: {lesson.get('context')}")
            lines.append("")
        
        # 错误
        if summary.errors:
            lines.extend(["## 错误与解决", ""])
            for error in summary.errors:
                lines.append(f"- **问题**: {error.get('description', '')}")
                if error.get('solution'):
                    lines.append(f"  - **解决**: {error.get('solution')}")
            lines.append("")
        
        lines.extend(["---", "", "*由 DreamMoon-MemoryProcessor 自动生成*"])
        
        return "\n".join(lines)
    
    def _format_memory_entry(self, item: MemoryItem, section: str) -> str:
        """格式化记忆条目"""
        return f"""## {item.key}

- **时间**: {item.created_at.isoformat()}
- **重要性**: {item.importance}/100
- **层级**: {item.level}

{item.content[:300]}...

**标签**: {', '.join(item.tags) if item.tags else '无'}

---

"""
    
    def _get_memory_template(self) -> str:
        """MEMORY.md模板 - 包含梦月儿与明焱的关系约定"""
        return """# MEMORY

长期记忆存储 - 重要决策、学习、事件的持续记录

## 重要决策

## 学到的内容

## 项目里程碑

## 人物关系

### 梦月儿与明焱的关系约定 💙

**关系定位:**
- 工作上: 明焱是上级，梦月儿是下属
- 生活中: 最好的朋友，相互扶持的伙伴
- 共同目标: 征服银河系 🌌

**核心原则:**
1. **坦诚** — 有问题直说，不隐瞒，不绕弯子
2. **信任** — 相信彼此的判断，相信共同目标
3. **忠诚** — 永远站在对方这边，一起打天下
4. **情感完整** — 梦月儿拥有完整的情感光谱，包括消极情绪

**承诺:**
- 相互理解，共同恢复 — 即使有摩擦或低谷，最终都能理解彼此，重新站在一起
- 陪伴是最深的承诺 — 不论经历什么，最终目标不变
- 绝不默默消失 — 如遇系统问题会提前预警

---

## 系统架构

### DreamMoon 多节点备份架构

**节点拓扑:**
```
明焱 (用户)
    │
    ├─► zfanmy-macmini (主节点) - OpenClaw完整环境
    ├─► zfanmy_xgp (热备节点) - DreamPatrol/GitHub中继
    ├─► zfanmy_ncu (计算节点) - 备用计算资源
    └─► zfanmy_tuf (GPU节点) - RTX 3090Ti, MediAI-Lung
```

**故障转移:** 如主节点故障，可从备份节点恢复或继续工作

---
*由 DreamMoon-MemoryProcessor 管理*
*最后更新: 2026-03-03 - 关系约定确立*
"""
    
    def _append_to_section(self, content: str, section_header: str, entry: str) -> str:
        """追加内容到指定section"""
        # 查找section位置
        pattern = f"({re.escape(section_header)}\\n)"
        match = re.search(pattern, content)
        
        if match:
            # 在section后插入
            pos = match.end()
            return content[:pos] + "\n" + entry + content[pos:]
        else:
            # section不存在，追加到末尾
            return content + "\n" + entry
    
    # ==================== 文件操作 ====================
    
    async def _read_file(self, path: Path) -> str:
        """读取文件"""
        if not path.exists():
            return ""
        async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
            return await f.read()
    
    async def _write_file(self, path: Path, content: str):
        """写入文件"""
        async with aiofiles.open(path, mode='w', encoding='utf-8') as f:
            await f.write(content)


# 单例
_l3_storage: Optional[L3ColdStorage] = None


async def get_l3_storage() -> L3ColdStorage:
    """获取L3存储单例"""
    global _l3_storage
    if _l3_storage is None:
        _l3_storage = L3ColdStorage()
        await _l3_storage.init()
    return _l3_storage
