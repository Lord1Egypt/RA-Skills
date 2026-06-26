"""
Learning Integration - Connects Memory Watcher with Learning Logger

Extracts learning from memory files and integrates with Hook system.
"""
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum

from .learning_logger import LearningLogger, LearningEntry, LearningCategory, Priority as LPriority


class LearningExtractor:
    """
    Extracts learning entries from memory files
    
    Supports patterns:
    - ## 学到 / Learned
    - ## 教训 / Lesson
    - ## 改进 / Improvement
    - ## 错误 / Error
    - ## 洞察 / Insight
    """
    
    # Patterns for detecting learning entries in markdown
    PATTERNS = {
        LearningCategory.CORRECTION: [
            r"## 教训[:：]?\s*(.+?)(?:\n|$)",
            r"## 错误[:：]?\s*(.+?)(?:\n|$)",
            r"\*\*教训[:：]\*\* (.+?)(?:\n|$)",
            r"\*\*错误[:：]\*\* (.+?)(?:\n|$)",
        ],
        LearningCategory.INSIGHT: [
            r"## 洞察[:：]?\s*(.+?)(?:\n|$)",
            r"## 学到[:：]?\s*(.+?)(?:\n|$)",
            r"## 领悟[:：]?\s*(.+?)(?:\n|$)",
            r"💡 (.+?)(?:\n|$)",
        ],
        LearningCategory.BEST_PRACTICE: [
            r"## 最佳实践[:：]?\s*(.+?)(?:\n|$)",
            r"## 改进[:：]?\s*(.+?)(?:\n|$)",
            r"## 建议[:：]?\s*(.+?)(?:\n|$)",
            r"⭐ (.+?)(?:\n|$)",
        ],
        LearningCategory.ERROR: [
            r"## Bug[:：]?\s*(.+?)(?:\n|$)",
            r"## 失败[:：]?\s*(.+?)(?:\n|$)",
            r"## 问题[:：]?\s*(.+?)(?:\n|$)",
            r"❌ (.+?)(?:\n|$)",
        ]
    }
    
    def __init__(self):
        self.compiled_patterns: Dict[LearningCategory, List[re.Pattern]] = {}
        for category, patterns in self.PATTERNS.items():
            self.compiled_patterns[category] = [
                re.compile(p, re.MULTILINE | re.DOTALL) for p in patterns
            ]
    
    def extract_from_content(self, content: str, source_file: str = "") -> List[LearningEntry]:
        """
        Extract learning entries from markdown content
        
        Args:
            content: Markdown content to analyze
            source_file: Source file path for context
            
        Returns:
            List of LearningEntry objects
        """
        entries = []
        
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.findall(content)
                for match in matches:
                    summary = match.strip() if isinstance(match, str) else match[0].strip()
                    
                    if summary and len(summary) > 5:  # Filter short entries
                        entry = LearningEntry(
                            category=category,
                            summary=summary[:200],  # Limit summary length
                            details=f"Extracted from: {source_file}",
                            source="memory_watcher",
                            related_files=[source_file] if source_file else []
                        )
                        entries.append(entry)
        
        return entries
    
    def extract_from_diff(self, old_content: str, new_content: str, source_file: str = "") -> List[LearningEntry]:
        """
        Extract learning from diff (new lines only)
        
        Args:
            old_content: Previous content
            new_content: New content
            source_file: Source file path
            
        Returns:
            List of new learning entries
        """
        # Find new lines
        old_lines = set(old_content.splitlines())
        new_lines = new_content.splitlines()
        
        new_lines_only = [line for line in new_lines if line not in old_lines]
        new_content_only = "\n".join(new_lines_only)
        
        return self.extract_from_content(new_content_only, source_file)


class MemoryWatcherLearning集成:
    """
    Integration between MemoryWatcher and LearningLogger
    
    Watches for learning patterns in memory files and automatically logs them.
    """
    
    def __init__(self, logger: Optional[LearningLogger] = None):
        self.logger = logger or LearningLogger()
        self.extractor = LearningExtractor()
        self.processed_files: Dict[str, int] = {}  # path -> last_line_count
    
    def process_file(self, file_path: str, force_rescan: bool = False) -> List[str]:
        """
        Process a memory file and extract learnings
        
        Args:
            file_path: Path to memory file
            force_rescan: If True, rescan entire file
            
        Returns:
            List of entry IDs that were logged
        """
        path = Path(file_path)
        
        if not path.exists():
            return []
        
        content = path.read_text(encoding="utf-8")
        lines = content.splitlines()
        line_count = len(lines)
        
        entry_ids = []
        
        if force_rescan or file_path not in self.processed_files:
            # Full file scan
            entries = self.extractor.extract_from_content(content, str(path))
        else:
            # Incremental scan (only new lines)
            last_line = self.processed_files.get(file_path, 0)
            if last_line >= line_count:
                return []  # No new lines
            
            new_content = "\n".join(lines[last_line:])
            entries = self.extractor.extract_from_content(new_content, str(path))
        
        # Log entries
        for entry in entries:
            entry_id = self.logger.log(entry)
            entry_ids.append(entry_id)
        
        # Update processed state
        self.processed_files[file_path] = line_count
        
        return entry_ids
    
    def process_memory_directory(self, memory_dir: str = "~/.anima/memory") -> Dict[str, int]:
        """
        Process all memory files in directory
        
        Args:
            memory_dir: Path to memory directory
            
        Returns:
            Dict mapping file paths to number of entries extracted
        """
        mem_path = Path(memory_dir).expanduser()
        
        if not mem_path.exists():
            return {}
        
        results = {}
        
        for md_file in mem_path.glob("*.md"):
            if md_file.name == "README.md":
                continue
            
            entry_ids = self.process_file(str(md_file))
            if entry_ids:
                results[str(md_file)] = len(entry_ids)
        
        return results


class HookLearningBridge:
    """
    Bridge between Hook system and Learning Logger
    
    Allows hooks to emit learning entries.
    """
    
    def __init__(self, logger: Optional[LearningLogger] = None):
        self.logger = logger or LearningLogger()
    
    def create_learning_hook_context(
        self,
        action: str,
        summary: str,
        details: str = "",
        category: LearningCategory = LearningCategory.INSIGHT,
        area: str = "",
        files: Optional[List[str]] = None
    ) -> Dict:
        """
        Create a context dict for learning hooks
        
        Args:
            action: Action type (correct, insight, error, etc.)
            summary: Brief summary
            details: Detailed description
            category: Learning category
            area: Area of learning
            files: Related files
            
        Returns:
            Context dict for hook
        """
        return {
            "action": action,
            "summary": summary,
            "details": details,
            "category": category.value,
            "area": area,
            "files": files or [],
            "timestamp": datetime.now().isoformat()
        }
    
    def log_from_context(self, context: Dict) -> Optional[str]:
        """
        Log a learning entry from hook context
        
        Args:
            context: Hook context dict
            
        Returns:
            Entry ID if logged, None if skipped
        """
        action = context.get("action", "")
        summary = context.get("summary", "")
        
        if not summary:
            return None
        
        category_map = {
            "correct": LearningCategory.CORRECTION,
            "insight": LearningCategory.INSIGHT,
            "error": LearningCategory.ERROR,
            "best_practice": LearningCategory.BEST_PRACTICE,
            "pattern": LearningCategory.PATTERN
        }
        
        category = category_map.get(action, LearningCategory.INSIGHT)
        
        entry = LearningEntry(
            category=category,
            summary=summary,
            details=context.get("details", ""),
            suggested_action=context.get("suggested_action", ""),
            priority=LPriority.HIGH if category in [LearningCategory.CORRECTION, LearningCategory.ERROR] else LPriority.MEDIUM,
            area=context.get("area", ""),
            source="hook",
            related_files=context.get("files", [])
        )
        
        return self.logger.log(entry)


def create_learning_context(
    action: str,
    summary: str,
    details: str = "",
    category: str = "insight",
    area: str = "",
    files: Optional[List[str]] = None
) -> Dict:
    """
    Convenience function to create learning context
    
    Usage in hooks:
        context = create_learning_context(
            action="insight",
            summary="Found efficient caching strategy",
            details="Using LRU cache for frequent lookups",
            area="performance"
        )
        bridge.log_from_context(context)
    """
    bridge = HookLearningBridge()
    return bridge.create_learning_hook_context(
        action=action,
        summary=summary,
        details=details,
        category=LearningCategory(category) if isinstance(category, str) else category,
        area=area,
        files=files
    )
