#!/usr/bin/env python3
"""
🎪 Smart Indexing Engine - AetherCore v3.3.4
Night Market Intelligence Technical Serviceization Practice
High-performance smart indexing system for fast search
"""

import json
import os
import hashlib
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class IndexType(Enum):
    """Types of indexes supported"""
    SEMANTIC = "semantic"      # Semantic search index
    KEYWORD = "keyword"        # Keyword search index
    FULLTEXT = "fulltext"      # Full-text search index
    METADATA = "metadata"      # Metadata index

@dataclass
class IndexEntry:
    """Entry in the smart index"""
    file_path: str
    line_number: int
    content: str
    keywords: List[str]
    semantic_vector: Optional[List[float]] = None
    metadata: Optional[Dict] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

class SmartIndexEngine:
    """Smart indexing engine for fast search and retrieval"""
    
    def __init__(self, index_dir: str = ".index"):
        """
        Initialize smart indexing engine
        
        Args:
            index_dir: Directory to store index files
        """
        self.index_dir = index_dir
        self.indexes = {
            IndexType.SEMANTIC: {},
            IndexType.KEYWORD: {},
            IndexType.FULLTEXT: {},
            IndexType.METADATA: {}
        }
        self.entries = []
        
        # Create index directory if it doesn't exist
        os.makedirs(index_dir, exist_ok=True)
    
    def index_file(self, file_path: str) -> Dict:
        """
        Index a file for fast search
        
        Args:
            file_path: Path to file to index
            
        Returns:
            Dict with indexing results
        """
        print(f"🔍 Indexing file: {file_path}")
        
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into lines for line-level indexing
            lines = content.split('\n')
            indexed_lines = 0
            
            for line_num, line in enumerate(lines, 1):
                if line.strip():  # Skip empty lines
                    entry = self._create_index_entry(file_path, line_num, line)
                    self.entries.append(entry)
                    self._add_to_indexes(entry)
                    indexed_lines += 1
            
            # Save index to disk
            self._save_index()
            
            return {
                "status": "success",
                "file_path": file_path,
                "indexed_lines": indexed_lines,
                "total_lines": len(lines),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to index file: {e}"}
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search indexed content
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of search results
        """
        print(f"🔍 Searching for: {query}")
        
        results = []
        query_lower = query.lower()
        
        # Simple keyword matching (can be enhanced with more sophisticated algorithms)
        for entry in self.entries:
            score = self._calculate_relevance_score(entry, query_lower)
            if score > 0:
                results.append({
                    "file": entry.file_path,
                    "line": entry.line_number,
                    "content": entry.content,
                    "score": score,
                    "keywords": entry.keywords[:5]  # Top 5 keywords
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:limit]
    
    def _create_index_entry(self, file_path: str, line_num: int, content: str) -> IndexEntry:
        """Create an index entry from file content"""
        # Extract keywords (simple implementation)
        keywords = self._extract_keywords(content)
        
        # Create semantic vector (placeholder - can be enhanced with ML models)
        semantic_vector = self._create_semantic_vector(content)
        
        # Extract metadata
        metadata = {
            "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            "file_extension": os.path.splitext(file_path)[1],
            "line_length": len(content),
            "word_count": len(content.split())
        }
        
        return IndexEntry(
            file_path=file_path,
            line_number=line_num,
            content=content,
            keywords=keywords,
            semantic_vector=semantic_vector,
            metadata=metadata
        )
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content (simple implementation)"""
        # Remove common words and punctuation
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        
        words = content.lower().split()
        keywords = []
        
        for word in words:
            # Clean word
            word = word.strip('.,!?;:"\'()[]{}')
            if word and word not in common_words and len(word) > 2:
                keywords.append(word)
        
        return keywords[:10]  # Limit to top 10 keywords
    
    def _create_semantic_vector(self, content: str) -> List[float]:
        """Create semantic vector from content (placeholder)"""
        # This is a placeholder implementation
        # In a real system, you would use word embeddings or other ML techniques
        return [hash(content) % 100 / 100.0 for _ in range(10)]
    
    def _add_to_indexes(self, entry: IndexEntry):
        """Add entry to all indexes"""
        # Add to keyword index
        for keyword in entry.keywords:
            if keyword not in self.indexes[IndexType.KEYWORD]:
                self.indexes[IndexType.KEYWORD][keyword] = []
            self.indexes[IndexType.KEYWORD][keyword].append(entry)
        
        # Add to fulltext index (simplified)
        content_lower = entry.content.lower()
        for word in content_lower.split():
            word = word.strip('.,!?;:"\'()[]{}')
            if word and len(word) > 2:
                if word not in self.indexes[IndexType.FULLTEXT]:
                    self.indexes[IndexType.FULLTEXT][word] = []
                self.indexes[IndexType.FULLTEXT][word].append(entry)
    
    def _calculate_relevance_score(self, entry: IndexEntry, query: str) -> float:
        """Calculate relevance score for search"""
        score = 0.0
        
        # Keyword matching
        for keyword in entry.keywords:
            if query in keyword:
                score += 2.0
            elif keyword in query:
                score += 1.0
        
        # Content matching
        content_lower = entry.content.lower()
        if query in content_lower:
            score += 3.0
        
        # Position bonus (earlier in file is more relevant)
        position_bonus = 1.0 / (entry.line_number ** 0.5)
        score += position_bonus
        
        return score
    
    def _save_index(self):
        """Save index to disk"""
        index_file = os.path.join(self.index_dir, "smart_index.json")
        
        index_data = {
            "entries": [asdict(entry) for entry in self.entries],
            "index_types": {index_type.value: list(index.keys()) 
                           for index_type, index in self.indexes.items()},
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "version": "3.3.4"
        }
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)
    
    def load_index(self) -> bool:
        """Load index from disk"""
        index_file = os.path.join(self.index_dir, "smart_index.json")
        
        if not os.path.exists(index_file):
            return False
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            # Recreate entries
            self.entries = []
            for entry_data in index_data.get("entries", []):
                entry = IndexEntry(
                    file_path=entry_data["file_path"],
                    line_number=entry_data["line_number"],
                    content=entry_data["content"],
                    keywords=entry_data["keywords"],
                    semantic_vector=entry_data.get("semantic_vector"),
                    metadata=entry_data.get("metadata"),
                    timestamp=entry_data.get("timestamp", time.time())
                )
                self.entries.append(entry)
                self._add_to_indexes(entry)
            
            print(f"✅ Loaded index with {len(self.entries)} entries")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load index: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get indexing statistics"""
        return {
            "total_entries": len(self.entries),
            "index_types": {
                index_type.value: len(index) 
                for index_type, index in self.indexes.items()
            },
            "keywords_count": len(self.indexes[IndexType.KEYWORD]),
            "fulltext_words": len(self.indexes[IndexType.FULLTEXT]),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

# Example usage
if __name__ == "__main__":
    # Create smart index engine
    engine = SmartIndexEngine()
    
    # Load existing index or create new
    if not engine.load_index():
        print("📝 No existing index found, creating new index...")
    
    # Example: Index a file
    test_file = "test_memory.md"
    if os.path.exists(test_file):
        result = engine.index_file(test_file)
        print(f"Indexing result: {result}")
    
    # Example: Search
    search_results = engine.search("AetherCore", limit=5)
    print(f"\n🔍 Search results for 'AetherCore':")
    for i, result in enumerate(search_results, 1):
        print(f"  {i}. {result['file']}:{result['line']} - {result['content'][:50]}...")
    
    # Get statistics
    stats = engine.get_stats()
    print(f"\n📊 Index Statistics:")
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Keywords indexed: {stats['keywords_count']}")
    print(f"  Full-text words: {stats['fulltext_words']}")