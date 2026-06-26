#!/usr/bin/env python3
"""
Document Manager - Automated document creation, storage, and tracking
Manages document lifecycle: creation, indexing, versioning, and archival
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

DOCS_ROOT = Path("/home/node/clawd/docs")
BASE_URL = "http://45.197.148.41:18792/docs"
INDEX_FILE = DOCS_ROOT / "INDEX.md"

def ensure_docs_dir():
    """Create docs directory structure if it doesn't exist"""
    DOCS_ROOT.mkdir(parents=True, exist_ok=True)
    (DOCS_ROOT / "archive").mkdir(exist_ok=True)

def create_document(title, doc_type, content, slug=None):
    """
    Create a new document with complete metadata
    
    Args:
        title: Document title
        doc_type: Type (Report, Analysis, Guide, Proposal, etc.)
        content: Main content (markdown)
        slug: URL slug (auto-generated if not provided)
    
    Returns:
        dict with document info and URL
    """
    ensure_docs_dir()
    
    # Generate slug if not provided
    if not slug:
        slug = title.lower().replace(" ", "-").replace("/", "-")[:50]
    
    # Create timestamped folder
    timestamp = datetime.now().strftime("%Y%m%d")
    folder_name = f"doc-{timestamp}-{slug}"
    doc_folder = DOCS_ROOT / folder_name
    doc_folder.mkdir(exist_ok=True)
    
    # Create metadata
    now = datetime.now().strftime("%Y-%m-%d %H:%M GMT+8")
    readme_content = f"""# {title}

**Type:** {doc_type}
**Created:** {now}
**Purpose:** {title}
**Status:** Draft

## Document Info
- Generated automatically by doc-manager
- See content.md for full document
- Accessible via: {BASE_URL}/{folder_name}/content.md
"""
    
    # Write files
    (doc_folder / "README.md").write_text(readme_content, encoding="utf-8")
    (doc_folder / "content.md").write_text(content, encoding="utf-8")
    
    # Create index.json
    index_data = {
        "title": title,
        "type": doc_type,
        "created": now,
        "slug": slug,
        "folder": folder_name,
        "url": f"{BASE_URL}/{folder_name}/content.md"
    }
    (doc_folder / "index.json").write_text(json.dumps(index_data, indent=2, ensure_ascii=False), encoding="utf-8")
    
    return index_data

def update_index():
    """Update master INDEX.md with all documents"""
    ensure_docs_dir()
    
    # Scan all document folders
    documents = []
    for item in sorted(DOCS_ROOT.iterdir()):
        if item.is_dir() and item.name.startswith("doc-") and item.name != "archive":
            index_file = item / "index.json"
            if index_file.exists():
                data = json.loads(index_file.read_text(encoding="utf-8"))
                documents.append(data)
    
    # Generate INDEX.md
    index_md = """# 📚 Document Index

All generated documents are listed below. Click the URL to preview.

| Document | Type | Created | URL |
|----------|------|---------|-----|
"""
    
    for doc in sorted(documents, key=lambda x: x["created"], reverse=True):
        index_md += f"| {doc['title']} | {doc['type']} | {doc['created']} | [{doc['folder']}]({doc['url']}) |\n"
    
    INDEX_FILE.write_text(index_md, encoding="utf-8")
    return len(documents)

def list_documents():
    """List all available documents"""
    ensure_docs_dir()
    
    if not INDEX_FILE.exists():
        update_index()
    
    return INDEX_FILE.read_text(encoding="utf-8")

def get_document_url(slug):
    """Get URL for a specific document"""
    for item in DOCS_ROOT.iterdir():
        if item.is_dir() and slug in item.name:
            return f"{BASE_URL}/{item.name}/content.md"
    return None

def archive_document(slug):
    """Move document to archive"""
    for item in DOCS_ROOT.iterdir():
        if item.is_dir() and slug in item.name and item.name.startswith("doc-"):
            archive_path = DOCS_ROOT / "archive" / item.name
            item.rename(archive_path)
            update_index()
            return f"Archived: {item.name}"
    return "Document not found"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: doc-manager.py <command> [args]")
        print("Commands:")
        print("  create <title> <type> <content_file> [slug]")
        print("  list")
        print("  update-index")
        print("  archive <slug>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "create" and len(sys.argv) >= 5:
        title = sys.argv[2]
        doc_type = sys.argv[3]
        content_file = sys.argv[4]
        slug = sys.argv[5] if len(sys.argv) > 5 else None
        
        content = Path(content_file).read_text(encoding="utf-8")
        result = create_document(title, doc_type, content, slug)
        update_index()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "list":
        print(list_documents())
    
    elif cmd == "update-index":
        count = update_index()
        print(f"Updated index with {count} documents")
    
    elif cmd == "archive" and len(sys.argv) > 2:
        slug = sys.argv[2]
        print(archive_document(slug))
