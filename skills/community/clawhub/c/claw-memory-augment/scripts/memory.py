#!/usr/bin/env python3
"""
Memory Augment - Long-term memory storage and retrieval for OpenClaw agents

Usage:
    python memory.py store "Remember user prefers Python"
    python memory.py search "what did I decide about income"
    python memory.py list --type decision
"""

import json
import re
import yaml
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher


class MemoryStore:
    """Stores and retrieves memories."""
    
    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path.home() / ".memory-augment" / "config.yaml"
        self.storage_path = Path.home() / ".memory-augment" / "storage.yaml"
        self.config = self._load_config()
        self.memories = self._load_memories()
    
    def _load_config(self) -> dict:
        """Load configuration or return defaults."""
        defaults = {
            "storage": {"path": str(self.storage_path), "format": "yaml"},
            "settings": {
                "max_memories": 1000,
                "default_expiry": 7,
                "score_decay": 0.95
            },
            "search": {"top_k": 20, "min_score": 0.3},
            "auto_inject": {"enabled": True, "max_tokens": 5000}
        }
        
        if self.config_path.exists():
            with open(self.config_path) as f:
                return yaml.safe_load(f) or defaults
        return defaults
    
    def _load_memories(self) -> List[dict]:
        """Load memories from storage file."""
        if not self.storage_path.exists():
            return []
        
        with open(self.storage_path) as f:
            data = yaml.safe_load(f)
            if data and "memories" in data:
                memories = data["memories"]
            else:
                # Handle old format (list of dicts)
                memories = data if isinstance(data, list) else []
        
        # Filter out expired memories
        return [m for m in memories if self._is_expired(m) is False]
    
    def _save_memories(self):
        """Save memories to storage file."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {"memories": self.memories}
        with open(self.storage_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
    
    def _is_expired(self, memory: dict) -> bool:
        """Check if a memory has expired."""
        expiry = memory.get("expires")
        if not expiry:
            return False
        
        expiry_date = datetime.fromisoformat(expiry.replace("Z", "+00:00"))
        return datetime.now(expiry_date.tzinfo) > expiry_date
    
    def store(self, content: str, memory_type: str = "context", 
              tags: List[str] = None, score: float = None) -> str:
        """Store a new memory."""
        memory = {
            "id": str(uuid.uuid4()),
            "content": content,
            "type": memory_type,
            "tags": tags or [],
            "created": datetime.now().isoformat(),
            "expires": None,
            "score": score or 0.5
        }
        
        # Set expiry for non-permanent types
        if memory_type not in ["preference", "decision", "learning"]:
            days = self.config["settings"]["default_expiry"]
            expiry = datetime.now() + timedelta(days=days)
            memory["expires"] = expiry.isoformat()
        
        self.memories.append(memory)
        
        # Cap total memories
        if len(self.memories) > self.config["settings"]["max_memories"]:
            # Remove oldest memories
            self.memories.sort(key=lambda m: m.get("created", ""))
            self.memories = self.memories[-self.config["settings"]["max_memories"]:]
        
        self._save_memories()
        return memory["id"]
    
    def search(self, query: str, top_k: int = None, min_score: float = None) -> List[dict]:
        """Search memories by query."""
        top_k = top_k or self.config["search"]["top_k"]
        min_score = min_score or self.config["search"]["min_score"]
        
        query_lower = query.lower()
        query_tags = self._extract_tags(query_lower)
        
        results = []
        for memory in self.memories:
            score = self._score_memory(memory, query, query_tags)
            if score >= min_score:
                results.append({
                    "id": memory["id"],
                    "content": memory["content"],
                    "score": score,
                    "type": memory["type"],
                    "tags": memory["tags"],
                    "created": memory["created"],
                    "expires": memory.get("expires")
                })
        
        # Sort by score descending
        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:top_k]
    
    def _score_memory(self, memory: dict, query: str, query_tags: List[str]) -> float:
        """Calculate relevance score for a memory."""
        score = 0.0
        
        # 1. Content similarity (text match)
        content_match = SequenceMatcher(
            None, 
            query.lower(), 
            memory["content"].lower()
        ).ratio()
        score += content_match * 0.4
        
        # 2. Tag match
        tag_match = len(set(query_tags) & set(memory["tags"]))
        if memory["tags"]:
            tag_score = tag_match / len(memory["tags"])
        else:
            tag_score = 0
        score += tag_score * 0.3
        
        # 3. Type weight
        type_weights = {
            "preference": 1.0,
            "decision": 0.9,
            "learning": 0.85,
            "context": 0.7
        }
        type_score = type_weights.get(memory["type"], 0.5)
        score += type_score * 0.2
        
        # 4. Recency bonus
        created = datetime.fromisoformat(memory["created"].replace("Z", "+00:00"))
        days_ago = (datetime.now(created.tzinfo) - created).days
        recency = max(0, 1 - (days_ago / 30))  # 1.0 today, 0.0 after 30 days
        score += recency * 0.1
        
        return score
    
    def _extract_tags(self, query: str) -> List[str]:
        """Extract tags from query (format: #tag1 #tag2)."""
        return re.findall(r'#(\w+)', query)
    
    def list(self, memory_type: str = None, since: str = None, 
             tag: str = None) -> List[dict]:
        """List memories with filters."""
        results = self.memories
        
        if memory_type:
            results = [m for m in results if m["type"] == memory_type]
        
        if tag:
            results = [m for m in results if tag in m["tags"]]
        
        if since:
            since_date = self._parse_date(since)
            results = [m for m in results 
                      if datetime.fromisoformat(m["created"].replace("Z", "+00:00")) >= since_date]
        
        return results
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime."""
        if "ago" in date_str.lower():
            days = int(re.search(r'(\d+)\s*(d|days)', date_str.lower())[1])
            return datetime.now() - timedelta(days=days)
        return datetime.fromisoformat(date_str)
    
    def delete(self, memory_id: str) -> bool:
        """Delete a memory by ID."""
        for i, memory in enumerate(self.memories):
            if memory["id"] == memory_id:
                self.memories.pop(i)
                self._save_memories()
                return True
        return False
    
    def delete_by_criteria(self, older_than_days: int = None, 
                           tag: str = None) -> int:
        """Delete memories matching criteria."""
        count = 0
        deleted_ids = []
        
        for memory in self.memories:
            should_delete = False
            
            if older_than_days:
                created = datetime.fromisoformat(memory["created"].replace("Z", "+00:00"))
                if (datetime.now(created.tzinfo) - created).days > older_than_days:
                    should_delete = True
            
            if tag and tag not in memory["tags"]:
                should_delete = False  # Keep if doesn't have tag
            
            if should_delete:
                deleted_ids.append(memory["id"])
                count += 1
        
        self.memories = [m for m in self.memories if m["id"] not in deleted_ids]
        self._save_memories()
        return count
    
    def export(self) -> str:
        """Export memories to JSON."""
        return json.dumps({"memories": self.memories}, indent=2)
    
    def import_memories(self, json_data: str):
        """Import memories from JSON."""
        data = json.loads(json_data)
        imported = data.get("memories", [])
        
        self.memories.extend(imported)
        self._save_memories()
        return len(imported)
    
    def summarize(self, since: str = None) -> str:
        """Generate summary of memories."""
        since_date = self._parse_date(since) if since else datetime.now() - timedelta(days=7)
        
        recent = [m for m in self.memories 
                  if datetime.fromisoformat(m["created"].replace("Z", "+00:00")) >= since_date]
        
        by_type = {}
        for m in recent:
            mtype = m["type"]
            by_type[mtype] = by_type.get(mtype, 0) + 1
        
        lines = [
            f"# Memory Summary ({since or 'Last 7 days'})",
            f"",
            f"**Total memories:** {len(recent)}",
            f"",
            f"**By type:**"
        ]
        
        for mtype, count in sorted(by_type.items()):
            lines.append(f"- {mtype}: {count}")
        
        return "\n".join(lines)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Augment - Long-term storage")
    parser.add_argument("command", choices=["store", "search", "list", "delete", "export", "import", "summarize"])
    parser.add_argument("text", nargs="?", help="Text for store/import or search query")
    parser.add_argument("--type", help="Memory type (preference, decision, learning, context)")
    parser.add_argument("--tag", action="append", help="Add tag(s)")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--top-k", type=int, help="Max results for search")
    parser.add_argument("--min-score", type=float, help="Minimum score for search")
    parser.add_argument("--since", help="Show memories since date (e.g., '2026-04-14' or '7 days ago')")
    parser.add_argument("--older-than", help="Delete memories older than (e.g., '7d', '30 days')")
    parser.add_argument("--import-file", help="File to import from (JSON)")
    
    args = parser.parse_args()
    
    store = MemoryStore()
    
    if args.command == "store":
        memory_id = store.store(
            args.text or "",
            memory_type=args.type or "context",
            tags=args.tag
        )
        print(f"✅ Memory stored with ID: {memory_id}")
    
    elif args.command == "search":
        results = store.search(
            args.text or "",
            top_k=args.top_k,
            min_score=args.min_score
        )
        
        if args.format == "json":
            print(json.dumps({"results": results, "total": len(results)}, indent=2))
        else:
            for r in results:
                print(f"### {r['type']} (score: {r['score']:.2f})")
                print(f"**Content:** {r['content']}")
                print(f"**Tags:** {', '.join(r['tags'])}")
                print()
    
    elif args.command == "list":
        results = store.list(
            memory_type=args.type,
            since=args.since
        )
        
        print(f"# Found {len(results)} memories")
        for r in results:
            print(f"- [{r['type']}] {r['content'][:60]}... ({r['tags']})")
    
    elif args.command == "delete":
        if args.text:  # ID provided as text
            if store.delete(args.text):
                print(f"✅ Memory {args.text} deleted")
            else:
                print(f"❌ Memory {args.text} not found")
        elif args.older_than:
            days = int(re.search(r'(\d+)', args.older_than)[1])
            count = store.delete_by_criteria(older_than_days=days)
            print(f"✅ Deleted {count} old memories")
    
    elif args.command == "export":
        print(store.export())
    
    elif args.command == "import":
        if args.import_file:
            with open(args.import_file) as f:
                count = store.import_memories(f.read())
            print(f"✅ Imported {count} memories")
        else:
            print("❌ Use --import-file <path> to specify file")
    
    elif args.command == "summarize":
        print(store.summarize(since=args.since))


if __name__ == "__main__":
    main()
