#!/usr/bin/env python3
"""
Database Manager for EPO Patent Intelligence
Deterministic database operations
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

class DatabaseManager:
    """Manages SQLite database for patent storage."""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection."""
        if db_path is None:
            # Default to skill data directory
            skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(skill_dir, 'data', 'patents.db')
        
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema if not exists."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create patents table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patent_id TEXT UNIQUE,
            title TEXT,
            inventor TEXT,
            company TEXT,
            filing_date DATE,
            publication_date DATE,
            abstract TEXT,
            category TEXT,
            technology_area TEXT,
            secondary_effects TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create indexes for faster queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patent_id ON patents(patent_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_company ON patents(company)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_publication_date ON patents(publication_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON patents(category)')
        
        conn.commit()
        conn.close()
    
    def save_patent(self, patent_data: Dict[str, Any]) -> bool:
        """
        Save a patent to database with deduplication.
        
        Args:
            patent_data: Dictionary with patent fields
            
        Returns:
            True if saved, False if duplicate
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check for duplicate
            cursor.execute(
                'SELECT id FROM patents WHERE patent_id = ?',
                (patent_data.get('patent_id'),)
            )
            if cursor.fetchone():
                conn.close()
                return False  # Duplicate
            
            # Insert new patent
            cursor.execute('''
            INSERT INTO patents (
                patent_id, title, inventor, company, filing_date,
                publication_date, abstract, category, technology_area,
                secondary_effects, image_url, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patent_data.get('patent_id'),
                patent_data.get('title'),
                patent_data.get('inventor'),
                patent_data.get('company'),
                patent_data.get('filing_date'),
                patent_data.get('publication_date'),
                patent_data.get('abstract'),
                patent_data.get('category', ''),
                patent_data.get('technology_area', ''),
                patent_data.get('secondary_effects', ''),
                patent_data.get('image_url', ''),
                patent_data.get('created_at', datetime.now().isoformat())
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error saving patent: {e}")
            return False
    
    def get_patents_by_company(self, company: str, limit: int = 50) -> List[Dict]:
        """Get patents by company name."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM patents 
        WHERE company LIKE ? 
        ORDER BY publication_date DESC 
        LIMIT ?
        ''', (f'%{company}%', limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_recent_patents(self, days: int = 7, limit: int = 100) -> List[Dict]:
        """Get patents from the last N days."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM patents 
        WHERE publication_date >= date('now', ?) 
        ORDER BY publication_date DESC 
        LIMIT ?
        ''', (f'-{days} days', limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_patent_count(self) -> int:
        """Get total number of patents in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM patents')
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def vacuum(self):
        """Optimize database file size."""
        conn = sqlite3.connect(self.db_path)
        conn.execute('VACUUM')
        conn.close()


def main():
    """Test the database manager."""
    db = DatabaseManager()
    print(f"✅ Database initialized at: {db.db_path}")
    print(f"📊 Patent count: {db.get_patent_count()}")


if __name__ == "__main__":
    main()
