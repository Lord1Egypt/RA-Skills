"""
Pattern Recorder - Record and recall task patterns

This module provides pattern recording and retrieval for workflow optimization.
All pattern recordings require user confirmation.
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Pattern:
    """Task pattern record."""
    id: str
    name: str
    description: str
    task_type: str
    steps: List[str]
    conditions: Dict[str, Any]
    success_rate: float
    usage_count: int
    created_at: str
    updated_at: str
    user_confirmed: bool = True


class PatternRecorder:
    """
    Records and recalls task patterns for workflow optimization.
    
    Features:
    - Pattern recording with user confirmation
    - Pattern matching and retrieval
    - Success rate tracking
    - Pattern cleanup
    
    All recordings require explicit user consent.
    """
    
    def __init__(self, storage_dir: str = "./patterns"):
        """
        Initialize pattern recorder.
        
        Args:
            storage_dir: Local directory for pattern storage
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self.db_path = self.storage_dir / "patterns.db"
        self._init_database()
        
        # Configuration
        self.config = {
            "min_occurrences": 3,
            "confidence_threshold": 0.7,
            "min_match_score": 0.5,
            "max_patterns": 1000
        }
    
    def _init_database(self):
        """Initialize SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS patterns (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    task_type TEXT,
                    steps TEXT,
                    conditions TEXT,
                    success_rate REAL,
                    usage_count INTEGER,
                    created_at TEXT,
                    updated_at TEXT,
                    user_confirmed INTEGER
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pattern_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_id TEXT,
                    timestamp TEXT,
                    success INTEGER,
                    FOREIGN KEY (pattern_id) REFERENCES patterns(id)
                )
            """)
            
            conn.commit()
    
    def _generate_id(self, content: str) -> str:
        """Generate unique ID."""
        return hashlib.md5(
            f"{content}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
    
    def _generate_name(self, task_type: str, steps: List[str]) -> str:
        """Generate pattern name."""
        step_count = len(steps)
        return f"{task_type}_workflow_{step_count}步"
    
    # ==================== Pattern Recording ====================
    
    def record(
        self,
        task_type: str,
        steps: List[str],
        context: Dict[str, Any],
        success: bool = True,
        name: Optional[str] = None,
        description: Optional[str] = None,
        user_confirmed: bool = True
    ) -> str:
        """
        Record a new pattern.
        
        IMPORTANT: user_confirmed must be True for pattern to be stored.
        
        Args:
            task_type: Type of task
            steps: List of workflow steps
            context: Task context
            success: Whether task was successful
            name: Optional pattern name
            description: Optional description
            user_confirmed: MUST be True to store pattern
            
        Returns:
            Pattern ID if recorded, empty string if not confirmed
        """
        if not user_confirmed:
            print("⚠️ Pattern recording requires user confirmation")
            return ""
        
        # Check for similar existing pattern
        existing = self._find_similar(task_type, steps)
        
        if existing:
            # Update existing pattern
            return self._update_pattern(existing.id, success)
        
        # Create new pattern
        pattern_id = self._generate_id(task_type + str(steps))
        now = datetime.now().isoformat()
        
        pattern = Pattern(
            id=pattern_id,
            name=name or self._generate_name(task_type, steps),
            description=description or f"自动记录的{task_type}工作流程",
            task_type=task_type,
            steps=steps,
            conditions=context,
            success_rate=1.0 if success else 0.0,
            usage_count=1,
            created_at=now,
            updated_at=now,
            user_confirmed=True
        )
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO patterns
                   (id, name, description, task_type, steps, conditions, 
                    success_rate, usage_count, created_at, updated_at, user_confirmed)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    pattern.id,
                    pattern.name,
                    pattern.description,
                    pattern.task_type,
                    json.dumps(pattern.steps),
                    json.dumps(pattern.conditions),
                    pattern.success_rate,
                    pattern.usage_count,
                    pattern.created_at,
                    pattern.updated_at,
                    1
                )
            )
            
            # Record usage
            conn.execute(
                """INSERT INTO pattern_usage (pattern_id, timestamp, success)
                   VALUES (?, ?, ?)""",
                (pattern.id, now, 1 if success else 0)
            )
            
            conn.commit()
        
        print(f"✅ 已记录模式: {pattern.name}")
        return pattern_id
    
    def _find_similar(self, task_type: str, steps: List[str]) -> Optional[Pattern]:
        """Find similar existing pattern."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM patterns WHERE task_type = ?",
                (task_type,)
            )
            
            for row in cursor.fetchall():
                existing_steps = json.loads(row["steps"])
                # Check if steps are similar (same order, same actions)
                if existing_steps == steps:
                    return Pattern(
                        id=row["id"],
                        name=row["name"],
                        description=row["description"],
                        task_type=row["task_type"],
                        steps=existing_steps,
                        conditions=json.loads(row["conditions"]),
                        success_rate=row["success_rate"],
                        usage_count=row["usage_count"],
                        created_at=row["created_at"],
                        updated_at=row["updated_at"],
                        user_confirmed=bool(row["user_confirmed"])
                    )
        
        return None
    
    def _update_pattern(self, pattern_id: str, success: bool) -> str:
        """Update existing pattern with new usage."""
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            # Get current stats
            cursor = conn.execute(
                "SELECT success_rate, usage_count FROM patterns WHERE id = ?",
                (pattern_id,)
            )
            row = cursor.fetchone()
            if row:
                current_rate = row[0]
                current_count = row[1]
                
                # Update success rate (exponential moving average)
                alpha = 0.1
                new_rate = alpha * (1.0 if success else 0.0) + (1 - alpha) * current_rate
                
                conn.execute(
                    """UPDATE patterns 
                       SET success_rate = ?, usage_count = ?, updated_at = ?
                       WHERE id = ?""",
                    (new_rate, current_count + 1, now, pattern_id)
                )
                
                # Record usage
                conn.execute(
                    """INSERT INTO pattern_usage (pattern_id, timestamp, success)
                       VALUES (?, ?, ?)""",
                    (pattern_id, now, 1 if success else 0)
                )
                
                conn.commit()
        
        return pattern_id
    
    # ==================== Pattern Retrieval ====================
    
    def recall(
        self,
        context: Dict[str, Any],
        task_type: Optional[str] = None,
        limit: int = 5
    ) -> List[Tuple[Pattern, float]]:
        """
        Recall patterns matching current context.
        
        Args:
            context: Current task context
            task_type: Optional task type filter
            limit: Maximum patterns to return
            
        Returns:
            List of (pattern, score) tuples
        """
        candidates = self._get_candidates(task_type)
        
        # Score each pattern
        scored = []
        for pattern in candidates:
            score = self._calculate_match_score(pattern, context)
            if score >= self.config["min_match_score"]:
                scored.append((pattern, score))
        
        # Sort by score
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return scored[:limit]
    
    def _get_candidates(self, task_type: Optional[str]) -> List[Pattern]:
        """Get candidate patterns from database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            if task_type:
                cursor = conn.execute(
                    "SELECT * FROM patterns WHERE task_type = ? AND user_confirmed = 1",
                    (task_type,)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM patterns WHERE user_confirmed = 1"
                )
            
            patterns = []
            for row in cursor.fetchall():
                patterns.append(Pattern(
                    id=row["id"],
                    name=row["name"],
                    description=row["description"],
                    task_type=row["task_type"],
                    steps=json.loads(row["steps"]),
                    conditions=json.loads(row["conditions"]),
                    success_rate=row["success_rate"],
                    usage_count=row["usage_count"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                    user_confirmed=bool(row["user_confirmed"])
                ))
            
            return patterns
    
    def _calculate_match_score(self, pattern: Pattern, context: Dict) -> float:
        """
        Calculate how well a pattern matches current context.
        
        Factors:
        - Context similarity (40%)
        - Success rate (30%)
        - Usage frequency (20%)
        - Recency (10%)
        """
        # Context similarity
        context_score = self._compare_context(pattern.conditions, context)
        
        # Success rate
        success_score = pattern.success_rate
        
        # Usage frequency (normalized)
        usage_score = min(pattern.usage_count / 50, 1.0)
        
        # Recency
        recency_score = self._calculate_recency(pattern.updated_at)
        
        return (
            0.4 * context_score +
            0.3 * success_score +
            0.2 * usage_score +
            0.1 * recency_score
        )
    
    def _compare_context(self, pattern_context: Dict, current_context: Dict) -> float:
        """Compare context similarity."""
        if not pattern_context or not current_context:
            return 0.5
        
        # Count matching keys
        keys1 = set(pattern_context.keys())
        keys2 = set(current_context.keys())
        
        if not keys1 and not keys2:
            return 1.0
        
        common_keys = keys1 & keys2
        if not common_keys:
            return 0.0
        
        # Check value matches
        matches = 0
        for key in common_keys:
            if pattern_context[key] == current_context[key]:
                matches += 1
        
        return matches / len(common_keys)
    
    def _calculate_recency(self, updated_at: str) -> float:
        """Calculate recency score (1.0 = very recent, 0.0 = very old)."""
        try:
            updated = datetime.fromisoformat(updated_at)
            age_days = (datetime.now() - updated).days
            
            # Decay over 90 days
            return max(0.0, 1.0 - (age_days / 90))
        except:
            return 0.5
    
    def get_pattern(self, pattern_id: str) -> Optional[Pattern]:
        """Get pattern by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM patterns WHERE id = ?",
                (pattern_id,)
            )
            
            row = cursor.fetchone()
            if row:
                return Pattern(
                    id=row["id"],
                    name=row["name"],
                    description=row["description"],
                    task_type=row["task_type"],
                    steps=json.loads(row["steps"]),
                    conditions=json.loads(row["conditions"]),
                    success_rate=row["success_rate"],
                    usage_count=row["usage_count"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                    user_confirmed=bool(row["user_confirmed"])
                )
        
        return None
    
    # ==================== Pattern Management ====================
    
    def list_patterns(
        self,
        task_type: Optional[str] = None,
        min_success_rate: float = 0.0
    ) -> List[Pattern]:
        """
        List all patterns.
        
        Args:
            task_type: Optional filter by task type
            min_success_rate: Minimum success rate filter
            
        Returns:
            List of patterns
        """
        patterns = self._get_candidates(task_type)
        
        # Filter by success rate
        patterns = [p for p in patterns if p.success_rate >= min_success_rate]
        
        # Sort by success rate and usage
        patterns.sort(key=lambda p: (p.success_rate, p.usage_count), reverse=True)
        
        return patterns
    
    def delete_pattern(self, pattern_id: str) -> bool:
        """
        Delete a pattern.
        
        Args:
            pattern_id: Pattern ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM patterns WHERE id = ?",
                (pattern_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
    
    def cleanup(
        self,
        min_success_rate: float = 0.5,
        min_usage: int = 3,
        max_age_days: int = 90
    ) -> Dict[str, int]:
        """
        Clean up low-quality patterns.
        
        Args:
            min_success_rate: Minimum success rate to keep
            min_usage: Minimum usage count to keep
            max_age_days: Maximum age in days
            
        Returns:
            Cleanup statistics
        """
        cutoff = datetime.now() - timedelta(days=max_age_days)
        
        with sqlite3.connect(self.db_path) as conn:
            # Count patterns to delete
            cursor = conn.execute(
                """SELECT COUNT(*) FROM patterns 
                   WHERE success_rate < ? 
                   OR usage_count < ? 
                   OR updated_at < ?""",
                (min_success_rate, min_usage, cutoff.isoformat())
            )
            deleted_count = cursor.fetchone()[0]
            
            # Delete
            conn.execute(
                """DELETE FROM patterns 
                   WHERE success_rate < ? 
                   OR usage_count < ? 
                   OR updated_at < ?""",
                (min_success_rate, min_usage, cutoff.isoformat())
            )
            
            # Clean up orphaned usage records
            conn.execute(
                """DELETE FROM pattern_usage 
                   WHERE pattern_id NOT IN (SELECT id FROM patterns)"""
            )
            
            conn.commit()
        
        return {"deleted_patterns": deleted_count}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pattern statistics."""
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute("SELECT COUNT(*) FROM patterns").fetchone()[0]
            confirmed = conn.execute(
                "SELECT COUNT(*) FROM patterns WHERE user_confirmed = 1"
            ).fetchone()[0]
            avg_success = conn.execute(
                "SELECT AVG(success_rate) FROM patterns"
            ).fetchone()[0] or 0.0
        
        return {
            "total_patterns": total,
            "confirmed_patterns": confirmed,
            "avg_success_rate": round(avg_success, 2),
            "by_task_type": self._get_task_type_distribution()
        }
    
    def _get_task_type_distribution(self) -> Dict[str, int]:
        """Get pattern count by task type."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT task_type, COUNT(*) as count FROM patterns GROUP BY task_type"
            )
            return {row[0]: row[1] for row in cursor.fetchall()}


# Example usage
if __name__ == "__main__":
    # Initialize recorder
    recorder = PatternRecorder()
    
    # Record a pattern (with user confirmation)
    pattern_id = recorder.record(
        task_type="document_analysis",
        steps=["load", "extract", "analyze", "summarize", "save"],
        context={"file_type": "pdf", "pages": 50},
        success=True,
        name="PDF文档分析流程",
        description="完整的PDF文档分析工作流程",
        user_confirmed=True  # REQUIRED
    )
    
    # Recall patterns
    matches = recorder.recall(
        context={"file_type": "pdf"},
        task_type="document_analysis"
    )
    
    print(f"\n找到 {len(matches)} 个匹配模式:")
    for pattern, score in matches:
        print(f"  - {pattern.name} (相关度: {score:.0%})")
    
    # Get stats
    stats = recorder.get_stats()
    print(f"\n统计: {stats}")
