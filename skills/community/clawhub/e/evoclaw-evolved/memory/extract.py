# Auto Memory Extraction — 自动记忆抽取
# 参考: claude-code src/core/memory.ts / DreamTask memory extraction
#
# 设计:
#   心跳时自动检查新经验 → 提炼洞察 → 写入记忆文件
#   分类: user / feedback / project / reference
#   去重: 检查现有标题, 避免重复写入
#   状态追踪: extract_state.json 记录 last_extract_ts

from __future__ import annotations
import os
import re
import json
import time
import hashlib
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/openclaw/.openclaw/workspace"))
MEMORY_DIR = WORKSPACE / "memory"
EXTRACT_STATE_FILE = WORKSPACE / "evoclaw" / "memory" / "extract_state.json"
EXTRACT_DIR = WORKSPACE / "evoclaw" / "memory"
EXTRACT_DIR.mkdir(parents=True, exist_ok=True)


# ─── 抽取类别 ───────────────────────────────────────────────────

MEMORY_CATEGORIES = ["user", "feedback", "project", "reference"]


@dataclass
class ExtractionResult:
    """单次抽取结果"""
    category: str
    title: str
    content: str
    source: str                    # 来源文件/事件
    extracted_at: float = field(default_factory=time.time)
    tags: list[str] = field(default_factory=list)
    confidence: float = 0.8        # 置信度 0-1

    def to_frontmatter(self) -> str:
        lines = [
            "---",
            f"category: {self.category}",
            f"title: {self.title}",
            f"extracted_at: {datetime.fromtimestamp(self.extracted_at).isoformat()}",
            f"source: {self.source}",
            f"confidence: {self.confidence}",
            f"tags: [{', '.join(self.tags)}]" if self.tags else "tags: []",
            "---",
            "",
            self.content,
        ]
        return "\n".join(lines)


# ─── 经验解析 ───────────────────────────────────────────────────

@dataclass
class ExperienceEntry:
    """经验条目"""
    timestamp: float
    category: str          # user / feedback / project / reference
    content: str
    source: str
    tags: list[str] = field(default_factory=list)


def parse_experiences(experiences_file: Path) -> list[ExperienceEntry]:
    """
    解析 experiences JSONL 文件, 提取待抽取的经验.
    """
    entries = []
    if not experiences_file.exists():
        return entries

    try:
        lines = experiences_file.read_text(encoding="utf-8").strip().split("\n")
        for line in lines:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                if obj.get("type") in ("notable", "pivotal", "experience"):
                    entries.append(ExperienceEntry(
                        timestamp=obj.get("timestamp", time.time()),
                        category=obj.get("category", "reference"),
                        content=obj.get("content", ""),
                        source=obj.get("source", str(experiences_file)),
                        tags=obj.get("tags", []),
                    ))
            except json.JSONDecodeError:
                continue
    except Exception:
        pass

    return entries


# ─── 抽取器 ─────────────────────────────────────────────────────

class MemoryExtractor:
    """
    自动记忆抽取器.
    
    流程:
      1. 扫描 experiences/ 目录, 找到自上次抽取以来的新条目
      2. 对每条经验进行分类和提炼
      3. 去重检查 (标题相似度)
      4. 写入对应的记忆文件
    """

    def __init__(self):
        self.state = self._load_state()
        self._memory_files: dict[str, Path] = {}

    # ─── 状态管理 ───────────────────────────────────────────────

    def _load_state(self) -> dict:
        if EXTRACT_STATE_FILE.exists():
            try:
                return json.loads(EXTRACT_STATE_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"last_extract_ts": 0.0, "extracted_count": 0}

    def _save_state(self) -> None:
        EXTRACT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        EXTRACT_STATE_FILE.write_text(json.dumps(self.state, indent=2))

    # ─── 核心抽取 ──────────────────────────────────────────────

    def extract(self, experiences_dir: Optional[Path] = None) -> list[ExtractionResult]:
        """
        执行一次抽取.
        返回: 新抽取的记忆列表
        """
        experiences_dir = experiences_dir or (MEMORY_DIR / "experiences")
        last_ts = self.state.get("last_extract_ts", 0.0)
        results = []

        if not experiences_dir.exists():
            return results

        # 扫描所有日期文件
        for exp_file in sorted(experiences_dir.glob("*.jsonl")):
            entries = parse_experiences(exp_file)
            for entry in entries:
                if entry.timestamp <= last_ts:
                    continue

                # 分类
                category = self._categorize(entry)
                if not category:
                    continue

                # 提炼
                extracted = self._refine(entry, category)
                if not extracted:
                    continue

                # 去重
                if self._is_duplicate(extracted):
                    continue

                # 写入记忆文件
                self._write_memory(extracted)
                results.append(extracted)

        # 更新状态
        self.state["last_extract_ts"] = time.time()
        self.state["extracted_count"] = self.state.get("extracted_count", 0) + len(results)
        self._save_state()

        return results

    def _categorize(self, entry: ExperienceEntry) -> Optional[str]:
        """
        分类经验条目.
        参考: claude-code memory taxonomy
          user      — Boss 的偏好/背景
          feedback  — Boss 的指导/纠正
          project   — 技术决策/项目进度
          reference — 学到的知识/技能
        """
        content_lower = entry.content.lower()
        tags_lower = [t.lower() for t in entry.tags]

        # feedback 关键词
        if any(k in content_lower for k in ["纠正", "不对", "应该", "要这样", "feedback", "不对", "错误"]):
            return "feedback"
        if any(k in tags_lower for k in ["feedback", "correction", "纠正"]):
            return "feedback"

        # project 关键词
        if any(k in content_lower for k in ["实现", "项目", "部署", "决定", "技术选型"]):
            return "project"
        if any(k in tags_lower for k in ["project", "技术决策"]):
            return "project"

        # user 关键词
        if any(k in content_lower for k in ["喜欢", "讨厌", "偏好", "希望", "想要", "不喜欢"]):
            return "user"
        if any(k in tags_lower for k in ["user", "preference", "偏好"]):
            return "user"

        # reference: 默认
        if len(entry.content) > 20:
            return "reference"

        return None

    def _refine(self, entry: ExperienceEntry, category: str) -> Optional[ExtractionResult]:
        """
        提炼经验为结构化记忆.
        这里用规则提取, 后续可升级为 LLM.
        """
        content = entry.content.strip()
        if len(content) < 10:
            return None

        # 生成标题
        title = self._generate_title(content, category)

        # 置信度
        confidence = 0.5
        if len(content) > 50:
            confidence = 0.7
        if entry.tags:
            confidence = 0.85

        return ExtractionResult(
            category=category,
            title=title,
            content=content,
            source=entry.source,
            tags=entry.tags,
            confidence=confidence,
        )

    def _generate_title(self, content: str, category: str) -> str:
        """生成记忆标题"""
        # 取前30字符作为标题
        preview = content[:30].strip()
        # 去掉特殊字符
        preview = re.sub(r'[^\w\u4e00-\u9fff\s]', '', preview)
        category_prefix = {"user": "用户偏好", "feedback": "经验反馈", "project": "项目决策", "reference": "知识记录"}[category]
        return f"{category_prefix}: {preview}..."

    def _is_duplicate(self, extracted: ExtractionResult, threshold: float = 0.8) -> bool:
        """
        简单去重: 检查现有文件中是否有相似标题.
        后续可升级为 embedding 相似度.
        """
        extracted_dir = EXTRACT_DIR / extracted.category
        if not extracted_dir.exists():
            return False

        # 简单检查: 标题前40字符完全相同视为重复
        title_prefix = extracted.title[:40].lower()
        for f in extracted_dir.glob("*.md"):
            try:
                lines = f.read_text(encoding="utf-8").split("\n")
                for line in lines:
                    if line.startswith("title:"):
                        existing_title = line[6:].strip().lower()
                        if existing_title[:40] == title_prefix:
                            return True
            except Exception:
                continue

        return False

    def _write_memory(self, extracted: ExtractionResult) -> None:
        """写入记忆文件"""
        category_dir = EXTRACT_DIR / extracted.category
        category_dir.mkdir(parents=True, exist_ok=True)

        # 文件名: 时间戳 + 标题hash
        ts = int(extracted.extracted_at)
        title_hash = hashlib.md5(extracted.title.encode()).hexdigest()[:6]
        filename = f"{ts}_{title_hash}.md"
        filepath = category_dir / filename

        filepath.write_text(extracted.to_frontmatter(), encoding="utf-8")


# ─── 便捷函数 ───────────────────────────────────────────────────

def auto_extract() -> list[ExtractionResult]:
    """一键执行自动抽取"""
    extractor = MemoryExtractor()
    return extractor.extract()


if __name__ == "__main__":
    results = auto_extract()
    print(f"Extracted: {len(results)} memories")
    for r in results:
        print(f"  [{r.category}] {r.title[:40]}")
    print("✅ Memory extraction complete")
