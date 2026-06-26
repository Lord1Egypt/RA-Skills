"""
Knowledge base manager for Enterprise Knowledge Base

Manages documents, provides statistics, and handles updates/deletions.
"""

import os
from typing import List, Dict, Any
from pathlib import Path

from .chroma_client import ChromaVectorDB


class KnowledgeBaseManager:
    """Manage knowledge base documents"""
    
    def __init__(self, db: ChromaVectorDB, documents_dir: str):
        """
        Initialize manager
        
        Args:
            db: Milvus database client
            documents_dir: Directory where documents are stored
        """
        self.db = db
        self.documents_dir = documents_dir
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all documents in knowledge base
        
        Returns:
            List of document info dictionaries
        """
        return self.db.get_all_documents()
    
    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Delete a document and all its chunks
        
        Args:
            document_id: Document ID to delete
        
        Returns:
            Result dictionary with status
        """
        # Get document info before deletion
        docs = self.db.get_all_documents()
        doc_info = next((d for d in docs if d["document_id"] == document_id), None)
        
        if not doc_info:
            return {
                "success": False,
                "message": f"Document not found: {document_id}"
            }
        
        # Delete from database
        deleted_count = self.db.delete_by_document(document_id)
        
        # Delete file from documents directory
        doc_name = doc_info["document_name"]
        file_pattern = f"{document_id}_*"
        deleted_files = []
        
        for file_path in Path(self.documents_dir).glob(file_pattern):
            try:
                os.remove(file_path)
                deleted_files.append(str(file_path))
            except Exception as e:
                print(f"⚠ Failed to delete file {file_path}: {e}")
        
        return {
            "success": True,
            "document_id": document_id,
            "document_name": doc_name,
            "chunks_deleted": deleted_count,
            "files_deleted": len(deleted_files),
            "message": f"✅ Deleted {doc_name}: {deleted_count} chunks removed"
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get knowledge base statistics
        
        Returns:
            Statistics dictionary
        """
        stats = self.db.get_stats()
        
        # Add file system stats
        doc_files = list(Path(self.documents_dir).glob("*"))
        total_size = sum(f.stat().st_size for f in doc_files if f.is_file())
        
        stats["documents_dir"] = self.documents_dir
        stats["stored_files"] = len(doc_files)
        stats["total_size_mb"] = round(total_size / (1024 * 1024), 2)
        
        return stats
    
    def get_document_info(self, document_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a document
        
        Args:
            document_id: Document ID
        
        Returns:
            Document info dictionary
        """
        docs = self.db.get_all_documents()
        doc_info = next((d for d in docs if d["document_id"] == document_id), None)
        
        if not doc_info:
            return {"error": f"Document not found: {document_id}"}
        
        # Find associated file
        file_pattern = f"{document_id}_*"
        files = list(Path(self.documents_dir).glob(file_pattern))
        
        if files:
            file_path = files[0]
            doc_info["file_path"] = str(file_path)
            doc_info["file_size_kb"] = round(file_path.stat().st_size / 1024, 2)
        
        return doc_info


if __name__ == "__main__":
    # Test manager
    from .config_loader import load_config
    
    print("Testing knowledge base manager...")
    
    config = load_config()
    
    # Initialize
    db = ChromaVectorDB(
        collection_name=config.collection_name
    )
    
    manager = KnowledgeBaseManager(db, config.documents_dir)
    
    # Get stats
    stats = manager.get_statistics()
    print(f"✓ Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # List documents
    docs = manager.list_documents()
    print(f"✓ Found {len(docs)} documents")
    for doc in docs[:3]:  # Show first 3
        print(f"  - {doc['document_name']} ({doc['chunk_count']} chunks)")
