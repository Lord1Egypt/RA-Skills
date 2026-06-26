#!/usr/bin/env python3
"""Initialize the amarin-memory database."""

import os
import sys

def main():
    try:
        from amarin_memory import MemoryEngine
    except ImportError:
        print("ERROR: amarin-memory not installed. Run: pip install amarin-memory")
        sys.exit(1)

    db_dir = os.path.expanduser("~/.amarin")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "agent.db")

    embedding_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")

    engine = MemoryEngine(db_path=db_path, embedding_url=embedding_url)
    engine.init_db()
    print(f"Amarin Memory initialized at {db_path}")
    print(f"Embedding service: {embedding_url}")

if __name__ == "__main__":
    main()
