import argparse
import os
import json
from datetime import datetime

# Optional: Import ChromaDB and LangChain if available
try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

def sync_to_kb(summary, file_path, collection_name="code_changes"):
    """
    Syncs a summary of code changes to a ChromaDB collection.
    """
    if not CHROMA_AVAILABLE:
        print("Warning: chromadb or langchain is not installed. Saving to local logs instead.")
        log_to_file(summary, file_path)
        return

    try:
        # Connect to ChromaDB (local persistence)
        client = chromadb.PersistentClient(path="./.gemini/kb")
        collection = client.get_or_create_collection(name=collection_name)

        # Generate a unique ID
        doc_id = f"{file_path}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Add document
        collection.add(
            documents=[summary],
            metadatas=[{"file": file_path, "timestamp": str(datetime.now())}],
            ids=[doc_id]
        )
        print(f"Successfully synced to knowledge base: {doc_id}")
    except Exception as e:
        print(f"Error syncing to knowledge base: {e}")
        log_to_file(summary, file_path)

def log_to_file(summary, file_path):
    """
    Fallback: Log changes to a JSONL file in the project.
    """
    log_entry = {
        "timestamp": str(datetime.now()),
        "file": file_path,
        "summary": summary
    }
    log_path = "./.gemini/changelog.jsonl"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    print(f"Logged change to {log_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync code change summaries to a knowledge base.")
    parser.add_argument("--summary", required=True, help="Summary of the code changes.")
    parser.add_argument("--file", required=True, help="Path to the file changed.")
    args = parser.parse_args()

    sync_to_kb(args.summary, args.file)
