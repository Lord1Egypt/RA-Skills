#!/usr/bin/env python3
"""
FAQ Forge - Main FAQ Management Engine
Author: Shadow Rose
License: MIT
quality-verified

Core FAQ management: add, edit, search, categorize, track updates.
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Set


class FAQEntry:
    """Single FAQ entry with metadata."""
    
    def __init__(self, question: str, answer: str, category: str = "General",
                 tags: Optional[List[str]] = None, priority: str = "normal",
                 product: str = "default", entry_id: Optional[str] = None):
        self.id = entry_id or self._generate_id(question)
        self.question = question
        self.answer = answer
        self.category = category
        self.tags = tags or []
        self.priority = priority  # low, normal, high, critical
        self.product = product
        self.created = datetime.now().isoformat()
        self.updated = datetime.now().isoformat()
        self.related = []  # List of related question IDs
        self.feedback = {"needs_improvement": False, "outdated": False, "notes": ""}
        self.view_count = 0
        
    def _generate_id(self, question: str) -> str:
        """Generate unique ID from question text."""
        # Simple slug generation
        slug = re.sub(r'[^\w\s-]', '', question.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug[:50]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON storage."""
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "tags": self.tags,
            "priority": self.priority,
            "product": self.product,
            "created": self.created,
            "updated": self.updated,
            "related": self.related,
            "feedback": self.feedback,
            "view_count": self.view_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FAQEntry':
        """Create FAQEntry from dictionary."""
        entry = cls(
            question=data["question"],
            answer=data["answer"],
            category=data.get("category", "General"),
            tags=data.get("tags", []),
            priority=data.get("priority", "normal"),
            product=data.get("product", "default"),
            entry_id=data.get("id")
        )
        entry.created = data.get("created", entry.created)
        entry.updated = data.get("updated", entry.updated)
        entry.related = data.get("related", [])
        entry.feedback = data.get("feedback", entry.feedback)
        entry.view_count = data.get("view_count", 0)
        return entry
    
    def update(self, question: Optional[str] = None, answer: Optional[str] = None,
               category: Optional[str] = None, tags: Optional[List[str]] = None,
               priority: Optional[str] = None):
        """Update entry fields and timestamp."""
        if question:
            self.question = question
        if answer:
            self.answer = answer
        if category:
            self.category = category
        if tags is not None:
            self.tags = tags
        if priority:
            self.priority = priority
        self.updated = datetime.now().isoformat()


class FAQDatabase:
    """FAQ database manager."""
    
    def __init__(self, data_file: str = "faq_data.json"):
        self.data_file = data_file
        self.entries: Dict[str, FAQEntry] = {}
        self.load()
    
    def load(self):
        """Load FAQ database from JSON."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.entries = {
                        entry_id: FAQEntry.from_dict(entry_data)
                        for entry_id, entry_data in data.items()
                    }
            except json.JSONDecodeError as e:
                print(f"ERROR: Database file is corrupted (invalid JSON): {e}")
                print(f"Backup your {self.data_file} file and fix the JSON syntax,")
                print(f"or delete it to start fresh.")
                raise
            except Exception as e:
                print(f"Warning: Could not load {self.data_file}: {e}")
                self.entries = {}
    
    def save(self):
        """Save FAQ database to JSON."""
        data = {entry_id: entry.to_dict() for entry_id, entry in self.entries.items()}
        
        # Create backup before overwriting (simple safety net)
        if os.path.exists(self.data_file):
            backup_file = self.data_file + ".backup"
            try:
                import shutil
                shutil.copy2(self.data_file, backup_file)
            except Exception:
                pass  # Backup failure shouldn't block save
        
        # Write with atomic rename for safety
        temp_file = self.data_file + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Atomic rename (safer than direct overwrite)
        import shutil
        shutil.move(temp_file, self.data_file)
    
    def add(self, entry: FAQEntry) -> str:
        """Add new FAQ entry. Returns entry ID."""
        # Ensure unique ID
        base_id = entry.id
        counter = 1
        while entry.id in self.entries:
            entry.id = f"{base_id}-{counter}"
            counter += 1
        
        self.entries[entry.id] = entry
        self.save()
        return entry.id
    
    def get(self, entry_id: str) -> Optional[FAQEntry]:
        """Get FAQ entry by ID."""
        return self.entries.get(entry_id)
    
    def update(self, entry_id: str, **kwargs) -> bool:
        """Update existing FAQ entry."""
        entry = self.entries.get(entry_id)
        if not entry:
            return False
        entry.update(**kwargs)
        self.save()
        return True
    
    def delete(self, entry_id: str) -> bool:
        """Delete FAQ entry."""
        if entry_id in self.entries:
            del self.entries[entry_id]
            self.save()
            return True
        return False
    
    def search(self, query: str = "", category: Optional[str] = None,
               tags: Optional[List[str]] = None, product: Optional[str] = None,
               priority: Optional[str] = None) -> List[FAQEntry]:
        """Search FAQ entries by multiple criteria."""
        results = []
        query_lower = query.lower()
        
        for entry in self.entries.values():
            # Filter by product
            if product and entry.product != product:
                continue
            
            # Filter by category
            if category and entry.category != category:
                continue
            
            # Filter by priority
            if priority and entry.priority != priority:
                continue
            
            # Filter by tags (entry must have ALL specified tags)
            if tags and not all(tag in entry.tags for tag in tags):
                continue
            
            # Text search in question and answer
            if query:
                if query_lower not in entry.question.lower() and \
                   query_lower not in entry.answer.lower():
                    continue
            
            results.append(entry)
        
        # Sort by priority (critical > high > normal > low), then by updated date
        priority_order = {"critical": 0, "high": 1, "normal": 2, "low": 3}
        results.sort(key=lambda e: (priority_order.get(e.priority, 2), e.updated), reverse=True)
        
        return results
    
    def get_categories(self, product: Optional[str] = None) -> Set[str]:
        """Get all unique categories."""
        categories = set()
        for entry in self.entries.values():
            if product is None or entry.product == product:
                categories.add(entry.category)
        return categories
    
    def get_tags(self, product: Optional[str] = None) -> Set[str]:
        """Get all unique tags."""
        tags = set()
        for entry in self.entries.values():
            if product is None or entry.product == product:
                tags.update(entry.tags)
        return tags
    
    def get_products(self) -> Set[str]:
        """Get all unique products."""
        return {entry.product for entry in self.entries.values()}
    
    def add_related(self, entry_id: str, related_id: str) -> bool:
        """Link two questions as related."""
        entry = self.entries.get(entry_id)
        related_entry = self.entries.get(related_id)
        
        if not entry or not related_entry:
            return False
        
        if related_id not in entry.related:
            entry.related.append(related_id)
        if entry_id not in related_entry.related:
            related_entry.related.append(entry_id)
        
        self.save()
        return True
    
    def set_feedback(self, entry_id: str, needs_improvement: bool = False,
                     outdated: bool = False, notes: str = "") -> bool:
        """Set customer feedback flags on an entry."""
        entry = self.entries.get(entry_id)
        if not entry:
            return False
        
        entry.feedback = {
            "needs_improvement": needs_improvement,
            "outdated": outdated,
            "notes": notes
        }
        entry.updated = datetime.now().isoformat()
        self.save()
        return True
    
    def increment_view(self, entry_id: str) -> bool:
        """Increment view count for analytics."""
        entry = self.entries.get(entry_id)
        if not entry:
            return False
        entry.view_count += 1
        self.save()
        return True
    
    def get_stats(self, product: Optional[str] = None) -> Dict:
        """Get database statistics."""
        entries = [e for e in self.entries.values() 
                   if product is None or e.product == product]
        
        if not entries:
            return {
                "total_entries": 0,
                "by_category": {},
                "by_priority": {},
                "needs_attention": 0,
                "total_views": 0
            }
        
        stats = {
            "total_entries": len(entries),
            "by_category": {},
            "by_priority": {},
            "needs_attention": 0,
            "total_views": sum(e.view_count for e in entries),
            "most_viewed": sorted(entries, key=lambda e: e.view_count, reverse=True)[:5]
        }
        
        for entry in entries:
            # Count by category
            stats["by_category"][entry.category] = \
                stats["by_category"].get(entry.category, 0) + 1
            
            # Count by priority
            stats["by_priority"][entry.priority] = \
                stats["by_priority"].get(entry.priority, 0) + 1
            
            # Count entries needing attention
            if entry.feedback.get("needs_improvement") or entry.feedback.get("outdated"):
                stats["needs_attention"] += 1
        
        return stats


def main():
    """Command-line interface for FAQ management."""
    import sys
    
    if len(sys.argv) < 2:
        print("FAQ Forge - FAQ Management Engine")
        print("\nUsage:")
        print("  faq_forge.py add <question> <answer> [--category CAT] [--tags TAG1,TAG2] [--priority LEVEL] [--product PROD]")
        print("  faq_forge.py update <id> [--question Q] [--answer A] [--category CAT] [--tags TAG1,TAG2] [--priority LEVEL]")
        print("  faq_forge.py delete <id>")
        print("  faq_forge.py search [query] [--category CAT] [--tags TAG1,TAG2] [--product PROD] [--priority LEVEL]")
        print("  faq_forge.py list [--product PROD]")
        print("  faq_forge.py stats [--product PROD]")
        print("  faq_forge.py relate <id1> <id2>")
        print("  faq_forge.py feedback <id> [--needs-improvement] [--outdated] [--notes TEXT]")
        print("\nPriority levels: low, normal, high, critical")
        return
    
    db = FAQDatabase()
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 4:
            print("Error: add requires <question> <answer>")
            return
        
        question = sys.argv[2]
        answer = sys.argv[3]
        
        # Parse optional arguments
        category = "General"
        tags = []
        priority = "normal"
        product = "default"
        
        for i in range(4, len(sys.argv)):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
            elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
                tags = sys.argv[i + 1].split(",")
            elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
            elif sys.argv[i] == "--product" and i + 1 < len(sys.argv):
                product = sys.argv[i + 1]
        
        entry = FAQEntry(question, answer, category, tags, priority, product)
        entry_id = db.add(entry)
        print(f"✓ Added entry: {entry_id}")
    
    elif command == "update":
        if len(sys.argv) < 3:
            print("Error: update requires <id>")
            return
        
        entry_id = sys.argv[2]
        kwargs = {}
        
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == "--question" and i + 1 < len(sys.argv):
                kwargs["question"] = sys.argv[i + 1]
            elif sys.argv[i] == "--answer" and i + 1 < len(sys.argv):
                kwargs["answer"] = sys.argv[i + 1]
            elif sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                kwargs["category"] = sys.argv[i + 1]
            elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
                kwargs["tags"] = sys.argv[i + 1].split(",")
            elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                kwargs["priority"] = sys.argv[i + 1]
        
        if db.update(entry_id, **kwargs):
            print(f"✓ Updated entry: {entry_id}")
        else:
            print(f"✗ Entry not found: {entry_id}")
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: delete requires <id>")
            return
        
        entry_id = sys.argv[2]
        if db.delete(entry_id):
            print(f"✓ Deleted entry: {entry_id}")
        else:
            print(f"✗ Entry not found: {entry_id}")
    
    elif command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else ""
        
        category = None
        tags = None
        product = None
        priority = None
        
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
            elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
                tags = sys.argv[i + 1].split(",")
            elif sys.argv[i] == "--product" and i + 1 < len(sys.argv):
                product = sys.argv[i + 1]
            elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
        
        results = db.search(query, category, tags, product, priority)
        print(f"\nFound {len(results)} results:\n")
        
        for entry in results:
            print(f"[{entry.id}] {entry.question}")
            print(f"  Category: {entry.category} | Priority: {entry.priority} | Product: {entry.product}")
            if entry.tags:
                print(f"  Tags: {', '.join(entry.tags)}")
            print(f"  Answer: {entry.answer[:100]}{'...' if len(entry.answer) > 100 else ''}")
            print()
    
    elif command == "list":
        product = None
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == "--product" and i + 1 < len(sys.argv):
                product = sys.argv[i + 1]
        
        entries = db.search(product=product)
        print(f"\nAll FAQ entries ({len(entries)}):\n")
        
        for entry in entries:
            print(f"[{entry.id}] {entry.question}")
            print(f"  Category: {entry.category} | Priority: {entry.priority}")
            print()
    
    elif command == "stats":
        product = None
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == "--product" and i + 1 < len(sys.argv):
                product = sys.argv[i + 1]
        
        stats = db.get_stats(product)
        print("\n=== FAQ Statistics ===\n")
        print(f"Total entries: {stats['total_entries']}")
        print(f"Total views: {stats['total_views']}")
        print(f"Needs attention: {stats['needs_attention']}")
        
        print("\nBy category:")
        for cat, count in sorted(stats['by_category'].items()):
            print(f"  {cat}: {count}")
        
        print("\nBy priority:")
        for pri, count in sorted(stats['by_priority'].items()):
            print(f"  {pri}: {count}")
        
        if stats['most_viewed']:
            print("\nMost viewed:")
            for entry in stats['most_viewed']:
                print(f"  {entry.view_count} views - {entry.question}")
    
    elif command == "relate":
        if len(sys.argv) < 4:
            print("Error: relate requires <id1> <id2>")
            return
        
        id1 = sys.argv[2]
        id2 = sys.argv[3]
        
        if db.add_related(id1, id2):
            print(f"✓ Linked {id1} ↔ {id2}")
        else:
            print("✗ One or both entries not found")
    
    elif command == "feedback":
        if len(sys.argv) < 3:
            print("Error: feedback requires <id>")
            return
        
        entry_id = sys.argv[2]
        needs_improvement = "--needs-improvement" in sys.argv
        outdated = "--outdated" in sys.argv
        
        notes = ""
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == "--notes" and i + 1 < len(sys.argv):
                notes = sys.argv[i + 1]
        
        if db.set_feedback(entry_id, needs_improvement, outdated, notes):
            print(f"✓ Feedback updated for {entry_id}")
        else:
            print(f"✗ Entry not found: {entry_id}")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
