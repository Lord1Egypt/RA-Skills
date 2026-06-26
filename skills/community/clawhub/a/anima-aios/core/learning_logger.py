"""
Learning Logger - Standardized learning behavior logging
Compatible with self-improving-agent's .learnings/ directory
"""
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
from enum import Enum
from dataclasses import dataclass, field


class LearningCategory(Enum):
    """Learning entry categories"""
    CORRECTION = "correction"          # 纠正
    INSIGHT = "insight"               # 洞察
    KNOWLEDGE_GAP = "knowledge_gap"   # 知识缺口
    BEST_PRACTICE = "best_practice"   # 最佳实践
    ERROR = "error"                   # 错误
    PATTERN = "pattern"               # 模式


class Priority(Enum):
    """Learning entry priority"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Status(Enum):
    """Learning entry status"""
    PENDING = "pending"
    APPLIED = "applied"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


@dataclass
class LearningEntry:
    """Learning entry data structure"""
    category: LearningCategory
    summary: str
    details: str = ""
    suggested_action: str = ""
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    area: str = ""
    source: str = "hook"  # "hook", "user", "system"
    pattern_key: Optional[str] = None
    recurrence_count: int = 1
    related_files: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Update timestamps"""
        self.last_seen = self.created_at


@dataclass
class LearningEntryDisplay:
    """Learning entry for display (with formatted strings)"""
    id: str
    category: str
    priority: str
    status: str
    area: str
    summary: str
    details: str
    suggested_action: str
    source: str
    pattern_key: Optional[str]
    recurrence_count: int
    first_seen: str
    last_seen: str
    related_files: List[str]
    created_at: str
    emoji: str


class LearningLogger:
    """Learning Logger - records learning behaviors to LEARNINGS.md and .learnings/"""
    
    # Category emoji mapping
    CATEGORY_EMOJI = {
        LearningCategory.CORRECTION: "🔧",
        LearningCategory.INSIGHT: "💡",
        LearningCategory.KNOWLEDGE_GAP: "📚",
        LearningCategory.BEST_PRACTICE: "⭐",
        LearningCategory.ERROR: "❌",
        LearningCategory.PATTERN: "🔄"
    }
    
    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize Learning Logger
        
        Args:
            base_path: Base path for learnings directory (default: ~/.anima/learnings)
        """
        self.base_path = Path(base_path or "~/.anima/learnings").expanduser()
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Main learnings file
        self.learnings_file = self.base_path / "LEARNINGS.md"
        self._ensure_learnings_file()
        
        # .learnings/ directory (compatible with self-improving-agent)
        self.learnings_compat_dir = Path("~/.anima/.learnings").expanduser()
        self.learnings_compat_dir.mkdir(parents=True, exist_ok=True)
        
        # Index file
        self.index_file = self.base_path / "INDEX.md"
        self._ensure_index_file()
    
    def _ensure_learnings_file(self) -> None:
        """Ensure main LEARNINGS.md file exists with proper header"""
        if not self.learnings_file.exists():
            self.learnings_file.write_text(
                "# Learning Log\n\n"
                "> 自动记录的学习条目\n\n"
                "## 统计\n\n"
                f"- 总数：0\n"
                f"- 纠正：0\n"
                f"- 洞察：0\n"
                f"- 知识缺口：0\n"
                f"- 最佳实践：0\n"
                f"- 错误：0\n\n"
                "---\n",
                encoding="utf-8"
            )
    
    def _ensure_index_file(self) -> None:
        """Ensure index file exists"""
        if not self.index_file.exists():
            self.index_file.write_text(
                "# Learning Index\n\n"
                "> 按类别和优先级组织的学习条目索引\n\n"
                "---\n",
                encoding="utf-8"
            )
    
    def log(self, entry: LearningEntry) -> str:
        """
        Log a learning entry
        
        Args:
            entry: LearningEntry to log
            
        Returns:
            The entry ID
        """
        # Update timestamps
        entry.updated_at = datetime.now()
        entry.last_seen = datetime.now()
        
        # Format and save to main file
        md_content = self._format_entry(entry)
        self._append_to_learnings(md_content)
        
        # Sync to .learnings/ directory (compatible with self-improving-agent)
        self._sync_to_learnings_dir(entry)
        
        # Update index
        self._update_index(entry)
        
        return entry.id
    
    def log_correction(
        self,
        summary: str,
        details: str = "",
        suggested_action: str = "",
        area: str = "",
        related_files: Optional[List[str]] = None,
        source: str = "hook"
    ) -> str:
        """Log a correction entry"""
        entry = LearningEntry(
            category=LearningCategory.CORRECTION,
            summary=summary,
            details=details,
            suggested_action=suggested_action,
            priority=Priority.HIGH,
            area=area,
            source=source,
            related_files=related_files or []
        )
        return self.log(entry)
    
    def log_insight(
        self,
        summary: str,
        details: str = "",
        suggested_action: str = "",
        area: str = "",
        related_files: Optional[List[str]] = None,
        source: str = "hook"
    ) -> str:
        """Log an insight entry"""
        entry = LearningEntry(
            category=LearningCategory.INSIGHT,
            summary=summary,
            details=details,
            suggested_action=suggested_action,
            priority=Priority.MEDIUM,
            area=area,
            source=source,
            related_files=related_files or []
        )
        return self.log(entry)
    
    def log_error(
        self,
        summary: str,
        details: str = "",
        suggested_action: str = "",
        area: str = "",
        related_files: Optional[List[str]] = None,
        source: str = "hook"
    ) -> str:
        """Log an error entry"""
        entry = LearningEntry(
            category=LearningCategory.ERROR,
            summary=summary,
            details=details,
            suggested_action=suggested_action,
            priority=Priority.HIGH,
            area=area,
            source=source,
            related_files=related_files or []
        )
        return self.log(entry)
    
    def _format_entry(self, entry: LearningEntry) -> str:
        """Format learning entry as Markdown"""
        emoji = self.CATEGORY_EMOJI.get(entry.category, "📝")
        
        files_str = ", ".join(entry.related_files) if entry.related_files else "None"
        pattern_str = entry.pattern_key or "N/A"
        
        md = f"""
### [{emoji}] {entry.category.value.upper()}: {entry.summary}

**Logged:** {entry.created_at.strftime('%Y-%m-%d %H:%M:%S')}  
**Priority:** {entry.priority.value} | **Status:** {entry.status.value}  
**Area:** {entry.area or 'N/A'} | **Source:** {entry.source}

**Summary:** {entry.summary}

**Details:** {entry.details or 'N/A'}

**Suggested Action:** {entry.suggested_action or 'N/A'}

**Metadata:**
- ID: `{entry.id}`
- Pattern-Key: {pattern_str}
- Recurrence: {entry.recurrence_count} time(s)
- First-Seen: {entry.first_seen.strftime('%Y-%m-%d %H:%M:%S')}
- Last-Seen: {entry.last_seen.strftime('%Y-%m-%d %H:%M:%S')}
- Related-Files: {files_str}
"""
        return md
    
    def _append_to_learnings(self, content: str) -> None:
        """Append entry to main LEARNINGS.md file"""
        with open(self.learnings_file, "a", encoding="utf-8") as f:
            f.write(content + "\n\n---\n\n")
    
    def _sync_to_learnings_dir(self, entry: LearningEntry) -> Path:
        """
        Sync entry to .learnings/ directory (compatible with self-improving-agent)
        
        Directory structure:
        ~/.anima/.learnings/
        ├── corrections/
        │   └── {id}_{pattern_key}.md
        ├── insights/
        │   └── {id}_{pattern_key}.md
        ├── best_practices/
        │   └── {id}_{pattern_key}.md
        └── errors/
            └── {id}_{pattern_key}.md
        """
        # Create category subdirectory
        category_dir = self.learnings_compat_dir / entry.category.value
        category_dir.mkdir(exist_ok=True)
        
        # Create filename
        pattern_part = entry.pattern_key or "general"
        # Sanitize pattern_part for filesystem
        pattern_part = pattern_part.replace("/", "_").replace("\\", "_")
        filename = f"{entry.id[:8]}_{pattern_part}.md"
        filepath = category_dir / filename
        
        # Format content
        content = self._format_entry(entry)
        
        # Write file
        filepath.write_text(content, encoding="utf-8")
        
        return filepath
    
    def _update_index(self, entry: LearningEntry) -> None:
        """Update index file with new entry reference"""
        emoji = self.CATEGORY_EMOJI.get(entry.category, "📝")
        
        index_entry = f"- [{emoji}] **{entry.priority.value.upper()}** [{entry.category.value}]: {entry.summary} (`{entry.id[:8]}`)\n"
        
        # Read current index
        current = self.index_file.read_text(encoding="utf-8") if self.index_file.exists() else ""
        
        # Find insertion point (by category)
        lines = current.split("\n")
        insert_idx = len(lines)
        
        for i, line in enumerate(lines):
            if line.startswith(f"## {entry.category.value.upper()}"):
                # Find the last entry under this category
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith("## "):
                        insert_idx = j
                        break
                else:
                    # Add before the last "---"
                    for j in range(len(lines) - 1, i, -1):
                        if lines[j].strip() == "---":
                            insert_idx = j
                            break
                break
        
        # Insert entry
        lines.insert(insert_idx, index_entry.rstrip("\n"))
        
        # Write back
        self.index_file.write_text("\n".join(lines), encoding="utf-8")
    
    def get_recent_entries(self, limit: int = 10) -> List[LearningEntryDisplay]:
        """Get recent learning entries from LEARNINGS.md"""
        if not self.learnings_file.exists():
            return []
        
        content = self.learnings_file.read_text(encoding="utf-8")
        
        # Simple parsing - extract entries
        entries = []
        current_lines = []
        in_entry = False
        
        for line in content.split("\n"):
            if line.startswith("### ["):
                # Save previous entry
                if current_lines:
                    entries.append(self._parse_entry(current_lines))
                
                # Start new entry
                current_lines = [line]
                in_entry = True
            elif in_entry:
                current_lines.append(line)
        
        # Don't forget the last entry
        if current_lines:
            entries.append(self._parse_entry(current_lines))
        
        # Return most recent
        return entries[-limit:] if len(entries) > limit else entries
    
    def _parse_entry(self, lines: List[str]) -> LearningEntryDisplay:
        """Parse entry lines into LearningEntryDisplay"""
        # Simple parsing - extract key fields from lines
        content = "\n".join(lines)
        
        # Extract category from first line
        first_line = lines[0] if lines else ""
        category = "unknown"
        for cat in LearningCategory:
            if cat.value.upper() in first_line.upper():
                category = cat.value
                break
        
        # Extract summary
        summary = ""
        if ":" in first_line:
            summary = first_line.split(":", 1)[1].strip()
        
        # Extract other metadata from content
        priority = "medium"
        status = "pending"
        area = ""
        source = "hook"
        details = ""
        suggested = ""
        pattern_key = None
        recurrence = 1
        files = []
        
        for line in lines:
            if line.startswith("**Priority:**"):
                priority = line.split("**Priority:**")[1].split("|")[0].strip()
            elif line.startswith("**Status:**"):
                status = line.split("**Status:**")[0].split("|")[-1].strip()
            elif line.startswith("**Area:**"):
                area = line.split("**Area:**")[1].split("|")[0].strip()
            elif line.startswith("**Source:**"):
                source = line.split("**Source:**")[1].strip()
            elif line.startswith("**Details:**"):
                details = line.split("**Details:**")[1].strip()
            elif line.startswith("**Suggested Action:**"):
                suggested = line.split("**Suggested Action:**")[1].strip()
            elif "Pattern-Key:" in line:
                pattern_key = line.split("Pattern-Key:")[1].strip()
            elif "Recurrence:" in line:
                try:
                    recurrence = int(line.split("Recurrence:")[1].split("time")[0].strip())
                except:
                    pass
            elif "Related-Files:" in line:
                files_str = line.split("Related-Files:")[1].strip()
                if files_str and files_str != "None":
                    files = [f.strip() for f in files_str.split(",")]
        
        # Find timestamps
        created_at = ""
        first_seen = ""
        last_seen = ""
        
        for line in lines:
            if "Logged:" in line:
                created_at = line.split("Logged:")[1].split("**")[0].strip()
            elif "First-Seen:" in line:
                first_seen = line.split("First-Seen:")[1].strip()
            elif "Last-Seen:" in line:
                last_seen = line.split("Last-Seen:")[1].strip()
        
        # Extract ID
        entry_id = ""
        for line in lines:
            if line.startswith("- ID:"):
                entry_id = line.split("`")[1] if "`" in line else ""
                break
        
        return LearningEntryDisplay(
            id=entry_id,
            category=category,
            priority=priority,
            status=status,
            area=area,
            summary=summary,
            details=details,
            suggested_action=suggested,
            source=source,
            pattern_key=pattern_key,
            recurrence_count=recurrence,
            first_seen=first_seen,
            last_seen=last_seen,
            related_files=files,
            created_at=created_at,
            emoji=self.CATEGORY_EMOJI.get(
                LearningCategory(category) if category != "unknown" else LearningCategory.INSIGHT,
                "📝"
            )
        )
    
    def get_stats(self) -> Dict:
        """Get learning log statistics"""
        if not self.learnings_file.exists():
            return {
                "total": 0,
                "corrections": 0,
                "insights": 0,
                "knowledge_gaps": 0,
                "best_practices": 0,
                "errors": 0
            }
        
        content = self.learnings_file.read_text(encoding="utf-8")
        
        stats = {
            "total": content.count("### ["),
            "corrections": content.count("CORRECTION"),
            "insights": content.count("INSIGHT"),
            "knowledge_gaps": content.count("KNOWLEDGE_GAP"),
            "best_practices": content.count("BEST_PRACTICE"),
            "errors": content.count("ERROR")
        }
        
        return stats
    
    def search(self, query: str, category: Optional[LearningCategory] = None) -> List[LearningEntryDisplay]:
        """
        Search learning entries
        
        Args:
            query: Search query (matches summary and details)
            category: Optional category filter
            
        Returns:
            List of matching entries
        """
        all_entries = self.get_recent_entries(limit=1000)
        
        results = []
        for entry in all_entries:
            if category and entry.category != category.value:
                continue
            
            if query.lower() in entry.summary.lower() or query.lower() in entry.details.lower():
                results.append(entry)
        
        return results
