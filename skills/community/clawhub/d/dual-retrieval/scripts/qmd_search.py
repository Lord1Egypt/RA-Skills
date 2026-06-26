"""QMD Search Implementation - Direct SQLite query"""
import sqlite3
from typing import List, Dict, Any, Optional
from pathlib import Path

QMD_DB_PATH = "C:/Users/Administrator/.cache/qmd/index.sqlite"


class QMDSearcher:
    """QMD searcher using direct SQLite queries"""
    
    def __init__(self, db_path: str = QMD_DB_PATH):
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
    
    def _get_connection(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn
    
    def search(self, query: str, top_k: int = 5, collection: str = None) -> List[Dict[str, Any]]:
        """
        Search QMD using LIKE query
        
        Args:
            query: Search query string
            top_k: Number of results to return
            collection: Optional collection filter
        
        Returns:
            List of search results with filepath, title, body, collection
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        search_terms = query.strip().split()
        
        if not search_terms:
            return []
        
        # Use LIKE search
        like_pattern = f"%{'%'.join(search_terms)}%"
        
        sql = """
            SELECT d.path, d.title, d.collection,
                   SUBSTR(c.doc, 1, 500) as content
            FROM documents d
            LEFT JOIN content c ON d.hash = c.hash
            WHERE d.active = 1 AND (d.title LIKE ? OR c.doc LIKE ?)
        """
        
        if collection:
            sql += " AND d.collection = ?"
            cursor.execute(sql + " ORDER BY d.modified_at DESC LIMIT ?", 
                         (like_pattern, like_pattern, collection, top_k))
        else:
            cursor.execute(sql + " ORDER BY d.modified_at DESC LIMIT ?", 
                         (like_pattern, like_pattern, top_k))
        
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                "filepath": row["path"],
                "title": row["title"],
                "content": row["content"] or "",
                "collection": row["collection"]
            })
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get QMD statistics"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM documents WHERE active = 1")
        doc_count = cursor.fetchone()["count"]
        
        cursor.execute("SELECT COUNT(DISTINCT collection) as count FROM documents WHERE active = 1")
        coll_count = cursor.fetchone()["count"]
        
        return {
            "document_count": doc_count,
            "collection_count": coll_count,
            "db_path": self.db_path
        }
    
    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None


# Test
if __name__ == "__main__":
    searcher = QMDSearcher()
    
    print("=== QMD Searcher Test ===")
    
    # Test stats
    stats = searcher.get_stats()
    print(f"Stats: {stats}")
    
    # Test search
    queries = ["python programming", "openclaw agent", "memory system"]
    for q in queries:
        results = searcher.search(q, top_k=3)
        print(f"\nSearch results for '{q}': {len(results)} found")
        for i, r in enumerate(results[:3], 1):
            print(f"  {i}. [{r['collection']}] {r['title']}")
    
    searcher.close()
