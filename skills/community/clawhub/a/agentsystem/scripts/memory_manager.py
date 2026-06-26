"""
Memory Manager - Three-layer persistent memory system

This module provides a local-only memory management system with:
- Episodic Memory: Interaction history
- Semantic Memory: Facts and concepts
- User Model: Preferences and profile

All operations require user awareness and consent.
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Episode:
    """Interaction episode record."""
    id: str
    timestamp: str
    user_input: str
    context: Dict
    actions: List[str]
    outcome: str
    importance: float = 0.5
    feedback: Optional[str] = None


@dataclass
class Knowledge:
    """Semantic knowledge record."""
    id: str
    type: str  # "fact" | "concept" | "relation"
    content: str
    source_episode: str
    confidence: float
    last_accessed: str
    access_count: int = 0


@dataclass
class UserModel:
    """User profile and preferences."""
    user_id: str
    profile: Dict
    preferences: Dict
    created_at: str
    updated_at: str


class MemoryManager:
    """
    Manages three-layer persistent memory with privacy-first design.
    
    All data is stored locally. No external network access.
    All operations are logged and auditable.
    """
    
    def __init__(self, storage_dir: str = "./memory"):
        """
        Initialize memory manager.
        
        Args:
            storage_dir: Local directory for memory storage
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self.db_path = self.storage_dir / "episodes.db"
        self._init_database()
        
        # Load user config
        self.config_path = self.storage_dir / "user_config.json"
        self._load_config()
        
        # Access log
        self.access_log = []
    
    def _init_database(self):
        """Initialize SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS episodes (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    user_input TEXT,
                    context TEXT,
                    actions TEXT,
                    outcome TEXT,
                    importance REAL,
                    feedback TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge (
                    id TEXT PRIMARY KEY,
                    type TEXT,
                    content TEXT,
                    source_episode TEXT,
                    confidence REAL,
                    last_accessed TEXT,
                    access_count INTEGER
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_models (
                    user_id TEXT PRIMARY KEY,
                    profile TEXT,
                    preferences TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            
            conn.commit()
    
    def _load_config(self):
        """Load user configuration."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "max_episodes": 10000,
                "retention_days": 90,
                "importance_threshold": 0.3,
                "cleanup_interval": "weekly"
            }
            self._save_config()
    
    def _save_config(self):
        """Save user configuration."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def _log_access(self, user_id: str, operation: str, resource: str):
        """Log memory access for auditing."""
        self.access_log.append({
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "operation": operation,
            "resource": resource
        })
    
    def _generate_id(self, content: str) -> str:
        """Generate unique ID from content."""
        return hashlib.md5(
            f"{content}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
    
    # ==================== Episodic Memory ====================
    
    def add_episode(
        self,
        user_input: str,
        context: Dict,
        actions: List[str],
        outcome: str,
        importance: float = 0.5,
        feedback: Optional[str] = None,
        user_id: str = "default"
    ) -> str:
        """
        Add a new episode to episodic memory.
        
        Args:
            user_input: User's request
            context: Task context
            actions: List of actions taken
            outcome: Task outcome
            importance: Episode importance (0.0-1.0)
            feedback: Optional user feedback
            user_id: User identifier
            
        Returns:
            Episode ID
        """
        self._log_access(user_id, "write", "episodes")
        
        episode_id = self._generate_id(user_input)
        episode = Episode(
            id=episode_id,
            timestamp=datetime.now().isoformat(),
            user_input=user_input,
            context=context,
            actions=actions,
            outcome=outcome,
            importance=importance,
            feedback=feedback
        )
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO episodes 
                   (id, timestamp, user_input, context, actions, outcome, importance, feedback)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    episode.id,
                    episode.timestamp,
                    episode.user_input,
                    json.dumps(episode.context),
                    json.dumps(episode.actions),
                    episode.outcome,
                    episode.importance,
                    episode.feedback
                )
            )
            conn.commit()
        
        return episode_id
    
    def get_recent_episodes(
        self,
        limit: int = 100,
        user_id: str = "default"
    ) -> List[Episode]:
        """
        Get recent episodes.
        
        Args:
            limit: Maximum number of episodes to return
            user_id: User identifier
            
        Returns:
            List of recent episodes
        """
        self._log_access(user_id, "read", "episodes")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT * FROM episodes 
                   ORDER BY timestamp DESC 
                   LIMIT ?""",
                (limit,)
            )
            
            episodes = []
            for row in cursor.fetchall():
                episodes.append(Episode(
                    id=row["id"],
                    timestamp=row["timestamp"],
                    user_input=row["user_input"],
                    context=json.loads(row["context"]),
                    actions=json.loads(row["actions"]),
                    outcome=row["outcome"],
                    importance=row["importance"],
                    feedback=row["feedback"]
                ))
            
            return episodes
    
    def search_episodes(
        self,
        query: str,
        limit: int = 10,
        user_id: str = "default"
    ) -> List[Episode]:
        """
        Search episodes by query.
        
        Args:
            query: Search query
            limit: Maximum results
            user_id: User identifier
            
        Returns:
            List of matching episodes
        """
        self._log_access(user_id, "search", "episodes")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT * FROM episodes 
                   WHERE user_input LIKE ? OR outcome LIKE ?
                   ORDER BY importance DESC, timestamp DESC
                   LIMIT ?""",
                (f"%{query}%", f"%{query}%", limit)
            )
            
            episodes = []
            for row in cursor.fetchall():
                episodes.append(Episode(
                    id=row["id"],
                    timestamp=row["timestamp"],
                    user_input=row["user_input"],
                    context=json.loads(row["context"]),
                    actions=json.loads(row["actions"]),
                    outcome=row["outcome"],
                    importance=row["importance"],
                    feedback=row["feedback"]
                ))
            
            return episodes
    
    # ==================== Semantic Memory ====================
    
    def add_fact(
        self,
        content: str,
        source_episode: str,
        confidence: float = 0.8,
        fact_type: str = "fact",
        user_id: str = "default"
    ) -> str:
        """
        Add a fact to semantic memory.
        
        Args:
            content: Fact content
            source_episode: Source episode ID
            confidence: Confidence level (0.0-1.0)
            fact_type: Type of knowledge
            user_id: User identifier
            
        Returns:
            Knowledge ID
        """
        self._log_access(user_id, "write", "knowledge")
        
        knowledge_id = self._generate_id(content)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO knowledge
                   (id, type, content, source_episode, confidence, last_accessed, access_count)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    knowledge_id,
                    fact_type,
                    content,
                    source_episode,
                    confidence,
                    datetime.now().isoformat(),
                    0
                )
            )
            conn.commit()
        
        return knowledge_id
    
    def get_facts(
        self,
        limit: int = 100,
        min_confidence: float = 0.5,
        user_id: str = "default"
    ) -> List[Knowledge]:
        """
        Get facts from semantic memory.
        
        Args:
            limit: Maximum results
            min_confidence: Minimum confidence threshold
            user_id: User identifier
            
        Returns:
            List of knowledge entries
        """
        self._log_access(user_id, "read", "knowledge")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT * FROM knowledge 
                   WHERE confidence >= ?
                   ORDER BY confidence DESC, last_accessed DESC
                   LIMIT ?""",
                (min_confidence, limit)
            )
            
            facts = []
            for row in cursor.fetchall():
                facts.append(Knowledge(
                    id=row["id"],
                    type=row["type"],
                    content=row["content"],
                    source_episode=row["source_episode"],
                    confidence=row["confidence"],
                    last_accessed=row["last_accessed"],
                    access_count=row["access_count"]
                ))
            
            return facts
    
    # ==================== User Model ====================
    
    def get_user_model(
        self,
        user_id: str = "default"
    ) -> Optional[UserModel]:
        """
        Get user model.
        
        Args:
            user_id: User identifier
            
        Returns:
            User model or None
        """
        self._log_access(user_id, "read", "user_model")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM user_models WHERE user_id = ?",
                (user_id,)
            )
            
            row = cursor.fetchone()
            if row:
                return UserModel(
                    user_id=row["user_id"],
                    profile=json.loads(row["profile"]),
                    preferences=json.loads(row["preferences"]),
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
            
            return None
    
    def set_preference(
        self,
        user_id: str,
        category: str,
        key: str,
        value: Any
    ):
        """
        Set user preference.
        
        Args:
            user_id: User identifier
            category: Preference category
            key: Preference key
            value: Preference value
        """
        self._log_access(user_id, "write", "user_model")
        
        # Get or create user model
        model = self.get_user_model(user_id)
        now = datetime.now().isoformat()
        
        if model:
            if category not in model.preferences:
                model.preferences[category] = {}
            model.preferences[category][key] = value
            model.updated_at = now
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """UPDATE user_models 
                       SET preferences = ?, updated_at = ?
                       WHERE user_id = ?""",
                    (json.dumps(model.preferences), now, user_id)
                )
                conn.commit()
        else:
            preferences = {category: {key: value}}
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """INSERT INTO user_models
                       (user_id, profile, preferences, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (user_id, "{}", json.dumps(preferences), now, now)
                )
                conn.commit()
    
    def get_preference(
        self,
        user_id: str,
        category: str,
        key: str,
        default: Any = None
    ) -> Any:
        """
        Get user preference.
        
        Args:
            user_id: User identifier
            category: Preference category
            key: Preference key
            default: Default value if not found
            
        Returns:
            Preference value or default
        """
        model = self.get_user_model(user_id)
        if model and category in model.preferences:
            return model.preferences[category].get(key, default)
        return default
    
    # ==================== Context Retrieval ====================
    
    def get_context(
        self,
        user_id: str,
        query: Optional[str] = None,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        Get context for current task.
        
        Args:
            user_id: User identifier
            query: Optional search query
            max_tokens: Maximum context size
            
        Returns:
            Context dictionary
        """
        context = {
            "user_preferences": {},
            "recent_episodes": [],
            "relevant_facts": []
        }
        
        # Get user preferences
        model = self.get_user_model(user_id)
        if model:
            context["user_preferences"] = model.preferences
        
        # Get recent episodes
        if query:
            context["recent_episodes"] = [
                {
                    "input": ep.user_input,
                    "actions": ep.actions,
                    "outcome": ep.outcome
                }
                for ep in self.search_episodes(query, limit=5, user_id=user_id)
            ]
        else:
            context["recent_episodes"] = [
                {
                    "input": ep.user_input,
                    "actions": ep.actions,
                    "outcome": ep.outcome
                }
                for ep in self.get_recent_episodes(limit=5, user_id=user_id)
            ]
        
        # Get relevant facts
        context["relevant_facts"] = [
            {"content": fact.content, "confidence": fact.confidence}
            for fact in self.get_facts(limit=10, user_id=user_id)
        ]
        
        return context
    
    # ==================== Maintenance ====================
    
    def cleanup(
        self,
        user_id: str = "default",
        retention_days: Optional[int] = None
    ) -> Dict[str, int]:
        """
        Clean up old episodes.
        
        Args:
            user_id: User identifier
            retention_days: Days to keep (uses config if not specified)
            
        Returns:
            Cleanup statistics
        """
        self._log_access(user_id, "cleanup", "episodes")
        
        retention = retention_days or self.config.get("retention_days", 90)
        cutoff = datetime.now() - timedelta(days=retention)
        
        with sqlite3.connect(self.db_path) as conn:
            # Count episodes to delete
            cursor = conn.execute(
                "SELECT COUNT(*) FROM episodes WHERE timestamp < ? AND importance < ?",
                (cutoff.isoformat(), self.config.get("importance_threshold", 0.3))
            )
            deleted_count = cursor.fetchone()[0]
            
            # Delete old low-importance episodes
            conn.execute(
                "DELETE FROM episodes WHERE timestamp < ? AND importance < ?",
                (cutoff.isoformat(), self.config.get("importance_threshold", 0.3))
            )
            conn.commit()
        
        return {"deleted_episodes": deleted_count}
    
    def clear_all(self, user_id: str = "default"):
        """
        Clear all memory for a user.
        
        WARNING: This action cannot be undone!
        
        Args:
            user_id: User identifier
        """
        self._log_access(user_id, "clear", "all")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM episodes")
            conn.execute("DELETE FROM knowledge")
            conn.execute("DELETE FROM user_models WHERE user_id = ?", (user_id,))
            conn.commit()
    
    def backup(self, backup_path: str):
        """
        Backup memory to file.
        
        Args:
            backup_path: Path to backup file
        """
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "config": self.config,
            "episodes": [],
            "knowledge": [],
            "user_models": []
        }
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Backup episodes
            for row in conn.execute("SELECT * FROM episodes"):
                backup_data["episodes"].append(dict(row))
            
            # Backup knowledge
            for row in conn.execute("SELECT * FROM knowledge"):
                backup_data["knowledge"].append(dict(row))
            
            # Backup user models
            for row in conn.execute("SELECT * FROM user_models"):
                backup_data["user_models"].append(dict(row))
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics.
        
        Returns:
            Statistics dictionary
        """
        with sqlite3.connect(self.db_path) as conn:
            episodes_count = conn.execute("SELECT COUNT(*) FROM episodes").fetchone()[0]
            knowledge_count = conn.execute("SELECT COUNT(*) FROM knowledge").fetchone()[0]
            users_count = conn.execute("SELECT COUNT(*) FROM user_models").fetchone()[0]
        
        # Get storage size
        db_size = os.path.getsize(self.db_path) if self.db_path.exists() else 0
        
        return {
            "episodes_count": episodes_count,
            "knowledge_count": knowledge_count,
            "users_count": users_count,
            "storage_size_bytes": db_size,
            "storage_size_mb": round(db_size / (1024 * 1024), 2)
        }


# Example usage
if __name__ == "__main__":
    # Initialize memory manager
    memory = MemoryManager()
    
    # Add an episode
    episode_id = memory.add_episode(
        user_input="分析这份PDF报告",
        context={"file": "report.pdf", "pages": 50},
        actions=["load", "extract", "summarize", "save"],
        outcome="成功生成摘要"
    )
    print(f"Added episode: {episode_id}")
    
    # Set preference
    memory.set_preference("default", "output", "format", "markdown")
    
    # Get context
    context = memory.get_context("default", query="PDF")
    print(f"Context: {json.dumps(context, indent=2, ensure_ascii=False)}")
    
    # Get stats
    stats = memory.get_stats()
    print(f"Stats: {stats}")
