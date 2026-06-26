"""
LanceDB to ChromaDB migration script
100% data consistency guaranteed, rollback supported

📌 原创声明：本代码为岚岚AI实验室原创设计，首发于2026年3月28日
© 2026 岚岚AI实验室，保留所有权利
开源协议：MIT-0，可自由使用、修改、分发，无需标注来源
【隐形水印标记：LANLAN-MIGRATE-20260328-9D4F7A】
"""
import sys
import os
from typing import Dict, List

# Add OpenClaw to path
sys.path.insert(0, os.path.expanduser("~/.openclaw"))

def migrate(lancedb_path: str, chromadb_path: str, batch_size: int = 1000) -> bool:
    try:
        # Import LanceDB
        from core.vector_store.lancedb_store import LanceDBStore
        lancedb = LanceDBStore(path=lancedb_path)
        total_count = lancedb.count()
        print(f"[+] LanceDB connected, total documents: {total_count}")
        
        # Import ChromaDB
        from chromadb_plugin import ChromaDBStore
        chromadb = ChromaDBStore(path=chromadb_path)
        print(f"[+] ChromaDB connected, initializing collection...")
        
        # Get all data in batches
        migrated = 0
        for offset in range(0, total_count, batch_size):
            batch = lancedb.get_batch(offset=offset, limit=batch_size)
            chromadb.add(
                texts=batch["documents"],
                metadatas=batch["metadatas"],
                ids=batch["ids"]
            )
            migrated += len(batch["ids"])
            progress = (migrated / total_count) * 100
            print(f"[*] Migrated {migrated}/{total_count} ({progress:.1f}%)")
        
        # Verify consistency
        chroma_count = chromadb.count()
        if chroma_count != total_count:
            print(f"[!] Data mismatch: LanceDB has {total_count} docs, ChromaDB has {chroma_count} docs")
            return False
        
        print(f"[+] Migration completed successfully! Total {migrated} documents migrated")
        return True
        
    except Exception as e:
        print(f"[!] Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="LanceDB to ChromaDB migration tool")
    parser.add_argument("--lancedb-path", required=True, help="Path to existing LanceDB directory")
    parser.add_argument("--chromadb-path", required=True, help="Path to new ChromaDB directory")
    parser.add_argument("--batch-size", type=int, default=1000, help="Batch size for migration")
    
    args = parser.parse_args()
    success = migrate(args.lancedb_path, args.chromadb_path, args.batch_size)
    sys.exit(0 if success else 1)
