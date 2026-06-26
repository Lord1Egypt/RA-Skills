"""
知识融合策略与安全写入机制

提供多种内容合并策略，确保反向更新已有页面时：
- 不破坏原有结构
- 可追溯可回滚
- Agent 可审查 diff 后确认应用
"""

import difflib
import shutil
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from .agent_logger import get_logger
from .core import WikiManager, WikiPage

LOG = get_logger("merge")


class MergeStrategy(Enum):
    """内容合并策略"""

    LINK_ONLY = "link_only"
    APPEND_RELATED = "append_related"
    APPEND_SECTION = "append_section"
    UPDATE_CONCEPT = "update_concept"


@dataclass
class ChangeProposal:
    """变更提案，供 Agent 审查"""

    page_title: str
    page_path: Path
    original_content: str
    proposed_content: str
    diff: str
    strategy: MergeStrategy
    reason: str
    backup_path: Optional[Path] = None

    def to_markdown(self) -> str:
        lines = [
            f"## 变更提案: {self.page_title}",
            f"**策略**: {self.strategy.value}",
            f"**原因**: {self.reason}",
            "",
            "### Diff",
            "```diff",
            self.diff,
            "```",
        ]
        return "\n".join(lines)


class ContentMerger:
    """内容合并器：按策略安全地合并新内容到已有页面"""

    def __init__(self, wiki: WikiManager):
        self.wiki = wiki

    def merge(
        self,
        page: WikiPage,
        addition: str,
        strategy: MergeStrategy,
        context: Optional[Dict] = None,
    ) -> str:
        LOG.info("merge: page=%s strategy=%s", page.title, strategy.value)
        """
        将新内容按指定策略合并到页面中。

        Args:
            page: 目标页面
            addition: 要添加的新内容
            strategy: 合并策略
            context: 额外上下文，可包含:
                - target: 关联页面标题（用于相关页面描述）
                - relation_desc: 关系描述
                - section_title: 追加章节的标题（APPEND_SECTION 用）
                - source_date: 来源日期

        Returns:
            合并后的完整内容（含 frontmatter）
        """
        content = page.content
        ctx = context or {}

        if strategy == MergeStrategy.LINK_ONLY:
            # 仅更新 frontmatter，不在正文操作
            pass

        elif strategy == MergeStrategy.APPEND_RELATED:
            target = ctx.get("target", "")
            desc = ctx.get("relation_desc", "相关")
            content = self.add_related_link(content, target, desc)

        elif strategy == MergeStrategy.APPEND_SECTION:
            section = ctx.get("section_title", "## 最新进展")
            content = self.append_after_section(content, section, addition)

        elif strategy == MergeStrategy.UPDATE_CONCEPT:
            content = self._update_concept_definition(content, addition)

        # 追加变更日志
        today = ctx.get("source_date", datetime.now().strftime("%Y-%m-%d"))
        log_entry = self._build_changelog_entry(strategy, ctx, addition)
        content = self.append_changelog(content, f"{today}: {log_entry}")

        # 重建完整页面（含更新后的 frontmatter）
        return self._rebuild_page(page, content)

    def generate_diff(self, original: str, modified: str) -> str:
        """生成统一的 diff 格式"""
        LOG.debug("generate_diff: original=%d chars, modified=%d chars", len(original), len(modified))
        original_lines = original.splitlines(keepends=True)
        modified_lines = modified.splitlines(keepends=True)
        # 确保每行以换行结尾
        if original_lines and not original_lines[-1].endswith("\n"):
            original_lines[-1] += "\n"
        if modified_lines and not modified_lines[-1].endswith("\n"):
            modified_lines[-1] += "\n"
        diff = difflib.unified_diff(
            original_lines,
            modified_lines,
            fromfile="original",
            tofile="modified",
        )
        return "".join(diff)

    def append_after_section(
        self,
        content: str,
        section_title: str,
        new_text: str,
    ) -> str:
        """
        在指定章节后追加内容。如果章节不存在，则在"相关页面"之前创建。

        Args:
            content: 页面正文内容
            section_title: 章节标题，如 "## 最新进展"
            new_text: 要追加的文本

        Returns:
            修改后的内容
        """
        lines = content.split("\n")

        # 检查章节是否已存在
        section_idx = -1
        for i, line in enumerate(lines):
            if line.strip().lower() == section_title.strip().lower():
                section_idx = i
                break

        if section_idx >= 0:
            # 找到该章节下一个同级或更高级标题的位置
            level = self._heading_level(section_title)
            insert_idx = len(lines)
            for i in range(section_idx + 1, len(lines)):
                if self._heading_level(lines[i]) > 0 and self._heading_level(lines[i]) <= level:
                    insert_idx = i
                    break

            # 在该位置前插入内容
            insert_lines = ["", new_text] if new_text else []
            lines = lines[:insert_idx] + insert_lines + lines[insert_idx:]
        else:
            # 章节不存在，在"相关页面"之前创建
            related_idx = -1
            for i, line in enumerate(lines):
                lower = line.strip().lower()
                if lower in ("## 相关页面", "## related pages", "## 相关概念"):
                    related_idx = i
                    break

            new_section = [section_title, "", new_text, ""]
            if related_idx >= 0:
                lines = lines[:related_idx] + new_section + lines[related_idx:]
            else:
                # 在"来源"之前，或末尾
                source_idx = -1
                for i, line in enumerate(lines):
                    if line.strip().lower() in ("## 来源", "## sources", "## 变更日志", "## changelog"):
                        source_idx = i
                        break
                if source_idx >= 0:
                    lines = lines[:source_idx] + new_section + lines[source_idx:]
                else:
                    lines.extend([""] + new_section)

        return "\n".join(lines)

    def add_related_link(
        self,
        content: str,
        target: str,
        description: str,
    ) -> str:
        """
        在页面的"相关页面"章节追加条目。
        如果章节不存在则自动创建。

        Args:
            content: 页面正文内容
            target: 要链接的页面标题
            description: 关系描述

        Returns:
            修改后的内容
        """
        lines = content.split("\n")
        new_entry = f"- [[{target}]] — {description}"

        # 查找"相关页面"章节
        related_idx = -1
        for i, line in enumerate(lines):
            lower = line.strip().lower()
            if lower in ("## 相关页面", "## related pages", "## 相关概念", "## related concepts"):
                related_idx = i
                break

        if related_idx >= 0:
            # 在该章节末尾追加
            insert_idx = len(lines)
            for i in range(related_idx + 1, len(lines)):
                if self._heading_level(lines[i]) > 0:
                    insert_idx = i
                    break
            # 检查是否已存在相同链接
            section_text = "\n".join(lines[related_idx:insert_idx])
            if f"[[{target}]]" in section_text:
                return content  # 已存在，不重复添加
            lines.insert(insert_idx, new_entry)
        else:
            # 在"来源"或"变更日志"之前创建"相关页面"章节
            anchor_idx = len(lines)
            for i, line in enumerate(lines):
                lower = line.strip().lower()
                if lower in ("## 来源", "## sources", "## 变更日志", "## changelog"):
                    anchor_idx = i
                    break
            new_section = ["## 相关页面", "", new_entry, ""]
            lines = lines[:anchor_idx] + new_section + lines[anchor_idx:]

        return "\n".join(lines)

    def append_changelog(self, content: str, entry: str) -> str:
        """
        在"变更日志"章节追加条目。
        如果章节不存在则自动创建。

        Args:
            content: 页面正文内容
            entry: 变更条目，如 "2026-04-21: 补充与 Bid2X 的对比"

        Returns:
            修改后的内容
        """
        lines = content.split("\n")
        new_entry = f"- {entry}"

        # 查找"变更日志"章节
        changelog_idx = -1
        for i, line in enumerate(lines):
            lower = line.strip().lower()
            if lower in ("## 变更日志", "## changelog", "## 变更记录"):
                changelog_idx = i
                break

        if changelog_idx >= 0:
            # 在该章节开头（标题后）插入新条目
            insert_idx = changelog_idx + 1
            # 跳过空行
            while insert_idx < len(lines) and lines[insert_idx].strip() == "":
                insert_idx += 1
            # 检查是否已存在相同条目
            section_text = "\n".join(lines[changelog_idx:])
            if entry in section_text:
                return content
            lines.insert(insert_idx, new_entry)
        else:
            # 在末尾创建"变更日志"章节
            while lines and lines[-1].strip() == "":
                lines.pop()
            new_section = ["", "## 变更日志", "", new_entry]
            lines.extend(new_section)

        return "\n".join(lines)

    def _update_concept_definition(self, content: str, new_definition: str) -> str:
        """
        更新页面的"一句话定义"（第一个非空非标题行）。
        这是唯一可能替换正文的策略，限制影响范围。

        Args:
            content: 页面正文内容
            new_definition: 新定义

        Returns:
            修改后的内容
        """
        lines = content.split("\n")
        for i, line in enumerate(lines):
            stripped = line.strip()
            # 跳过标题和 frontmatter 分隔符
            if not stripped or stripped.startswith("#") or stripped.startswith("---"):
                continue
            # 找到第一个内容行，认为是定义句
            old_def = lines[i]
            lines[i] = new_definition
            # 保留旧定义作为注释
            lines.insert(i + 1, f"\n> 历史定义: {old_def}")
            break
        return "\n".join(lines)

    def _rebuild_page(self, page: WikiPage, new_content: str) -> str:
        """重建完整页面（含更新后的 frontmatter）"""
        fm = dict(page.frontmatter)
        fm["updated"] = datetime.now().strftime("%Y-%m-%d")

        fm_lines = ["---"]
        for key, value in fm.items():
            if isinstance(value, list):
                fm_lines.append(f"{key}:")
                for v in value:
                    fm_lines.append(f'  - "{v}"')
            else:
                fm_lines.append(f'{key}: "{value}"')
        fm_lines.append("---")

        return "\n".join(fm_lines) + "\n\n" + new_content

    def _heading_level(self, line: str) -> int:
        """返回标题级别（# 数量），不是标题返回 0"""
        stripped = line.strip()
        if stripped.startswith("#"):
            level = 0
            for c in stripped:
                if c == "#":
                    level += 1
                else:
                    break
            # 确保后面有空格
            if level < len(stripped) and stripped[level] == " ":
                return level
        return 0

    def _build_changelog_entry(self, strategy: MergeStrategy, ctx: Dict, addition: str) -> str:
        """根据策略生成变更日志条目文本"""
        target = ctx.get("target", "")
        desc = ctx.get("relation_desc", "")
        if strategy == MergeStrategy.LINK_ONLY:
            return f"添加相关页面链接"
        elif strategy == MergeStrategy.APPEND_RELATED:
            return f"添加与 [[{target}]] 的关联 — {desc}"
        elif strategy == MergeStrategy.APPEND_SECTION:
            section = ctx.get("section_title", "新章节")
            return f"补充{section.lstrip('#').strip()} — {addition[:50]}..."
        elif strategy == MergeStrategy.UPDATE_CONCEPT:
            return f"更新概念定义"
        return "内容更新"


class SafeWriter:
    """安全写入器：备份、应用、回滚"""

    def __init__(self, wiki: WikiManager):
        self.wiki = wiki
        self.backups_dir = wiki.wiki_dir / ".backups"
        self.backups_dir.mkdir(exist_ok=True)

    def prepare(
        self,
        page: WikiPage,
        new_content: str,
        reason: str,
        strategy: MergeStrategy,
    ) -> ChangeProposal:
        """准备变更提案"""
        original = page.path.read_text(encoding="utf-8")
        diff = ContentMerger(self.wiki).generate_diff(original, new_content)
        return ChangeProposal(
            page_title=page.title,
            page_path=page.path,
            original_content=original,
            proposed_content=new_content,
            diff=diff,
            strategy=strategy,
            reason=reason,
        )

    def apply(self, proposal: ChangeProposal) -> Path:
        """
        应用变更提案，自动创建备份。

        Returns:
            备份文件路径
        """
        page_path = proposal.page_path
        LOG.info("apply: %s (strategy=%s)", page_path, proposal.strategy.value)
        if not page_path.exists():
            raise ValueError(f"Page not found: {page_path}")

        # 创建备份
        today = datetime.now().strftime("%Y%m%d")
        backup_name = f"{today}-{page_path.stem}.md"
        backup_path = self.backups_dir / backup_name
        # 处理重名
        counter = 1
        while backup_path.exists():
            backup_name = f"{today}-{page_path.stem}-{counter}.md"
            backup_path = self.backups_dir / backup_name
            counter += 1

        shutil.copy2(page_path, backup_path)
        LOG.debug("Backup created: %s", backup_path)

        # 写入新内容
        page_path.write_text(proposal.proposed_content, encoding="utf-8")
        proposal.backup_path = backup_path
        LOG.info("Applied changes to %s, backup at %s", page_path, backup_path)

        return backup_path

    def rollback(self, page_path: Path) -> bool:
        """
        回滚指定页面的最后一次变更。

        Args:
            page_path: 页面文件路径

        Returns:
            是否成功回滚
        """
        LOG.info("rollback: %s", page_path)
        if not page_path.exists():
            LOG.warning("rollback failed: page not found: %s", page_path)
            return False

        # 查找最新的备份
        stem = page_path.stem
        backups = sorted(
            self.backups_dir.glob(f"*-{stem}.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not backups:
            LOG.warning("rollback failed: no backup found for %s", stem)
            return False

        # 恢复备份
        shutil.copy2(backups[0], page_path)
        LOG.info("rollback complete: restored from %s", backups[0])
        return True

    def list_backups(self, page_path: Path) -> List[Path]:
        """列出指定页面的所有备份"""
        stem = page_path.stem
        return sorted(
            self.backups_dir.glob(f"*-{stem}.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
