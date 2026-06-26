#!/usr/bin/env python3
"""
CogniMemo Memory Manager
Demonstrates core memory operations for AI agents.
"""

import os
import sys
from datetime import datetime
from typing import Optional, List, Dict

# Mock implementation for demonstration
# In production: from cognimemo import CogniMemo

class MemoryManager:
    """Manages persistent memory for AI agents using CogniMemo."""
    
    def __init__(self, user_id: str, api_key: Optional[str] = None):
        """
        Initialize memory manager.
        
        Args:
            user_id: Unique identifier for the user
            api_key: CogniMemo API key (or set COGNIMEMO_API_KEY env var)
        """
        self.user_id = user_id
        self.api_key = api_key or os.environ.get("COGNIMEMO_API_KEY")
        
        if not self.api_key:
            print("Warning: No API key set. Set COGNIMEMO_API_KEY or pass api_key.")
            print("Using mock storage for demonstration.")
            self._use_mock = True
            self._mock_storage: Dict[str, List] = {}
        else:
            self._use_mock = False
            # In production: self.client = CogniMemo(api_key=self.api_key)
            self._use_mock = True  # Still mock for demo
            self._mock_storage: Dict[str, List] = {}
    
    def store(self, content: str, memory_type: str = "context", 
              metadata: Optional[Dict] = None) -> str:
        """
        Store a memory.
        
        Args:
            content: The memory content
            memory_type: Type of memory (preference, decision, task, fact, context)
            metadata: Additional metadata
        
        Returns:
            Memory ID
        """
        memory_id = f"mem_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        entry = {
            "id": memory_id,
            "user_id": self.user_id,
            "content": content,
            "type": memory_type,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }
        
        if self._use_mock:
            if self.user_id not in self._mock_storage:
                self._mock_storage[self.user_id] = []
            self._mock_storage[self.user_id].append(entry)
        
        print(f"✓ Stored: [{memory_type}] {content[:50]}...")
        return memory_id
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search memories semantically.
        
        Args:
            query: Search query
            limit: Maximum results
        
        Returns:
            List of matching memories
        """
        if self._use_mock:
            memories = self._mock_storage.get(self.user_id, [])
            # Simple keyword matching for demo
            query_lower = query.lower()
            results = [
                m for m in memories
                if query_lower in m["content"].lower()
            ][:limit]
        else:
            # In production:
            # results = self.client.search(
            #     user_id=self.user_id,
            #     query=query,
            #     limit=limit
            # )
            results = []
        
        return results
    
    def get_by_type(self, memory_type: str) -> List[Dict]:
        """Get all memories of a specific type."""
        if self._use_mock:
            memories = self._mock_storage.get(self.user_id, [])
            return [m for m in memories if m["type"] == memory_type]
        return []
    
    def get_recent(self, hours: int = 24) -> List[Dict]:
        """Get memories from the last N hours."""
        if self._use_mock:
            memories = self._mock_storage.get(self.user_id, [])
            cutoff = datetime.now().timestamp() - (hours * 3600)
            return [
                m for m in memories
                if datetime.fromisoformat(m["created_at"]).timestamp() > cutoff
            ]
        return []
    
    def get_preferences(self) -> Dict:
        """Get all user preferences."""
        preferences = self.get_by_type("preference")
        return {p["content"]: p["metadata"] for p in preferences}
    
    def get_decisions(self) -> List[str]:
        """Get all user decisions."""
        decisions = self.get_by_type("decision")
        return [d["content"] for d in decisions]
    
    def get_tasks(self, pending_only: bool = True) -> List[Dict]:
        """Get user tasks."""
        tasks = self.get_by_type("task")
        if pending_only:
            return [t for t in tasks if not t["metadata"].get("completed")]
        return tasks
    
    def remember_preference(self, preference: str, category: str = "general"):
        """Convenience method to store a preference."""
        return self.store(
            content=preference,
            memory_type="preference",
            metadata={"category": category}
        )
    
    def remember_decision(self, decision: str, context: str = ""):
        """Convenience method to store a decision."""
        return self.store(
            content=decision,
            memory_type="decision",
            metadata={"context": context}
        )
    
    def remember_task(self, task: str, deadline: Optional[str] = None,
                      priority: str = "medium"):
        """Convenience method to store a task."""
        return self.store(
            content=task,
            memory_type="task",
            metadata={"deadline": deadline, "priority": priority, "completed": False}
        )
    
    def complete_task(self, task_content: str):
        """Mark a task as completed."""
        if self._use_mock:
            memories = self._mock_storage.get(self.user_id, [])
            for m in memories:
                if m["type"] == "task" and task_content in m["content"]:
                    m["metadata"]["completed"] = True
                    print(f"✓ Completed task: {task_content[:50]}...")
                    return True
        print("Task not found")
        return False
    
    def summary(self) -> Dict:
        """Get a summary of stored memories."""
        if self._use_mock:
            memories = self._mock_storage.get(self.user_id, [])
            return {
                "total": len(memories),
                "preferences": len([m for m in memories if m["type"] == "preference"]),
                "decisions": len([m for m in memories if m["type"] == "decision"]),
                "tasks": len([m for m in memories if m["type"] == "task"]),
                "facts": len([m for m in memories if m["type"] == "fact"]),
                "contexts": len([m for m in memories if m["type"] == "context"])
            }
        return {"total": 0}


def demo():
    """Demonstrate memory manager usage."""
    print("=== CogniMemo Memory Manager Demo ===\n")
    
    # Initialize
    memory = MemoryManager(user_id="demo-user-123")
    
    print("1. Storing preferences...")
    memory.remember_preference("Prefers dark mode in all applications", "ui")
    memory.remember_preference("Likes bullet points over paragraphs", "communication")
    memory.remember_preference("Prefers Portuguese language", "language")
    
    print("\n2. Storing decisions...")
    memory.remember_decision(
        decision="Use React for frontend project",
        context="Team discussion on March 16"
    )
    memory.remember_decision(
        decision="Choose PostgreSQL over MongoDB",
        context="Database selection for main app"
    )
    
    print("\n3. Storing tasks...")
    memory.remember_task(
        task="Finish quarterly report",
        deadline="2026-03-20",
        priority="high"
    )
    memory.remember_task(
        task="Review pull requests",
        priority="medium"
    )
    
    print("\n4. Storing facts...")
    memory.store(
        content="User works at Acme Corp as senior developer",
        memory_type="fact",
        metadata={"source": "profile", "verified": True}
    )
    
    print("\n5. Searching memories...")
    results = memory.search("preferences")
    print(f"Found {len(results)} results for 'preferences'")
    for r in results:
        print(f"  - {r['content'][:50]}...")
    
    print("\n6. Getting preferences...")
    prefs = memory.get_preferences()
    for pref, meta in prefs.items():
        print(f"  - {pref} (category: {meta.get('category', 'general')})")
    
    print("\n7. Memory summary:")
    summary = memory.summary()
    for key, value in summary.items():
        print(f"  - {key}: {value}")
    
    print("\n=== Usage in AI Agent ===")
    print("```python")
    print("from cognimemo import CogniMemo")
    print("")
    print("memory = CogniMemo(api_key='your-key')")
    print("")
    print("# Get user context before responding")
    print("context = memory.search(user_id, query='What are my preferences?')")
    print("")
    print("# Store important info from conversation")
    print("memory.store(user_id, 'User asked about React components')")
    print("```")


if __name__ == "__main__":
    demo()