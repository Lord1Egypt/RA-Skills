#!/usr/bin/env python3
"""
Eidolon Search - Index Builder

메모리 파일들을 FTS5 DB로 인덱싱

Usage:
  python scripts/build-index.py [memory_dir] [db_path]
  
  memory_dir: 메모리 파일 디렉토리 (기본: ./memory)
  db_path: DB 파일 경로 (기본: ./memory.db)
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

def get_memory_files(memory_dir):
    """메모리 파일 목록 가져오기"""
    memory_path = Path(memory_dir)
    if not memory_path.exists():
        print(f"❌ Memory directory not found: {memory_dir}")
        return []
    
    # .md 파일만
    files = list(memory_path.glob("**/*.md"))
    return sorted(files)

def init_db(db_path):
    """DB 초기화"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 스키마 생성
    schema_path = Path(__file__).parent.parent / "db" / "schema.sql"
    if schema_path.exists():
        schema = schema_path.read_text()
        conn.executescript(schema)
    else:
        # 스키마 파일 없으면 직접 생성
        c.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
            path,
            content,
            tokenize='porter unicode61 remove_diacritics 2'
        )
        """)
    
    conn.commit()
    return conn

def index_file(conn, file_path, base_dir):
    """파일 인덱싱"""
    try:
        content = file_path.read_text(encoding='utf-8')
        relative_path = str(file_path.relative_to(base_dir))
        
        c = conn.cursor()
        
        # 기존 항목 삭제 (재인덱싱)
        c.execute("DELETE FROM memory_fts WHERE path = ?", (relative_path,))
        
        # 새 항목 추가
        c.execute("""
        INSERT INTO memory_fts (path, content)
        VALUES (?, ?)
        """, (relative_path, content))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"  ⚠️  Error indexing {file_path}: {e}")
        return False

def main():
    memory_dir = sys.argv[1] if len(sys.argv) > 1 else "./memory"
    db_path = sys.argv[2] if len(sys.argv) > 2 else "./memory.db"
    
    print(f"🔍 Eidolon Search - Index Builder")
    print(f"📁 Memory dir: {memory_dir}")
    print(f"💾 DB path: {db_path}")
    print("=" * 60)
    
    # 메모리 파일 찾기
    files = get_memory_files(memory_dir)
    if not files:
        print("❌ No memory files found")
        return
    
    print(f"📝 Found {len(files)} memory files")
    
    # DB 초기화
    conn = init_db(db_path)
    print(f"✅ DB initialized: {db_path}")
    
    # 인덱싱
    base_dir = Path(memory_dir).parent
    success = 0
    
    for file_path in files:
        print(f"  • {file_path.relative_to(base_dir)}...", end=" ")
        if index_file(conn, file_path, base_dir):
            print("✓")
            success += 1
        else:
            print("✗")
    
    conn.close()
    
    print("=" * 60)
    print(f"✅ Indexed {success}/{len(files)} files")
    print(f"\n🔍 Try searching:")
    print(f"  python scripts/search.py 'your query'")
    print(f"  node examples/search.js 'your query'")
    print(f"  ./examples/search-sql.sh 'your query'")

if __name__ == "__main__":
    main()
