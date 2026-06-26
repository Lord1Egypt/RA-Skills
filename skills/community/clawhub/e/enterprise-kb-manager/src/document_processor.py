"""
Document processor for Enterprise Knowledge Base

Orchestrates document parsing, chunking, embedding, and storage.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
import hashlib
from datetime import datetime

from .parser import DocumentParser
from .chunker import DocumentChunker
from .embedder import Embedder
from .chroma_client import ChromaVectorDB


@dataclass
class ProcessResult:
    """Result of document processing"""
    success: bool
    document_id: str
    document_name: str
    chunk_count: int
    message: str
    error: str = ""


class DocumentProcessor:
    """Process documents end-to-end"""
    
    def __init__(self, config):
        """
        Initialize processor
        
        Args:
            config: KnowledgeBaseConfig object
        """
        self.config = config
        
        # Initialize components
        self.parser = DocumentParser()
        self.chunker = DocumentChunker(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap
        )
        self.embedder = Embedder(
            model=config.embedding_model,
            api_key=config.embedding_api_key,
            provider=getattr(config, 'embedding_provider', 'openai'),
            base_url=getattr(config, 'embedding_base_url', None)
        )
        self.db = ChromaVectorDB(
            collection_name=config.collection_name
        )
        
        # Ensure documents directory exists
        os.makedirs(config.documents_dir, exist_ok=True)
    
    def process_document(self, file_path: str, document_name: str = None) -> ProcessResult:
        """
        Process a document: parse → chunk → embed → store
        
        Args:
            file_path: Path to document file
            document_name: Optional custom name (default: filename)
        
        Returns:
            ProcessResult with status and details
        """
        try:
            # Validate file
            if not os.path.exists(file_path):
                return ProcessResult(
                    success=False,
                    document_id="",
                    document_name=document_name or "",
                    chunk_count=0,
                    message="",
                    error=f"File not found: {file_path}"
                )
            
            if not self.parser.is_supported(file_path):
                ext = Path(file_path).suffix
                return ProcessResult(
                    success=False,
                    document_id="",
                    document_name=document_name or "",
                    chunk_count=0,
                    message="",
                    error=f"Unsupported file format: {ext}. Supported: {', '.join(DocumentParser.SUPPORTED_FORMATS)}"
                )
            
            # Generate document ID
            if document_name is None:
                document_name = Path(file_path).name
            
            document_id = self._generate_document_id(document_name)
            
            # Check if document already exists
            existing_count = self.db.count_by_document(document_id)
            if existing_count > 0:
                # Delete existing chunks
                self.db.delete_by_document(document_id)
                print(f"⚠ Replaced existing document with {existing_count} chunks")
            
            # Parse document
            print(f"📄 Parsing {document_name}...")
            text = self.parser.parse(file_path)
            
            if not text or not text.strip():
                return ProcessResult(
                    success=False,
                    document_id=document_id,
                    document_name=document_name,
                    chunk_count=0,
                    message="",
                    error="Document is empty or contains no extractable text"
                )
            
            # Chunk document
            print(f"✂️  Chunking document...")
            chunks = self.chunker.chunk_text(
                text=text,
                document_id=document_id,
                document_name=document_name,
                metadata={"uploaded_at": datetime.now().isoformat()}
            )
            
            if not chunks:
                return ProcessResult(
                    success=False,
                    document_id=document_id,
                    document_name=document_name,
                    chunk_count=0,
                    message="",
                    error="Failed to create chunks from document"
                )
            
            print(f"   Created {len(chunks)} chunks")
            
            # Generate embeddings
            print(f"🔢 Generating embeddings...")
            chunk_texts = [chunk.text for chunk in chunks]
            embeddings = self.embedder.embed_texts(chunk_texts)
            
            # Prepare data for Milvus
            milvus_data = []
            for chunk, embedding in zip(chunks, embeddings):
                milvus_data.append({
                    "id": chunk.id,
                    "vector": embedding,
                    "text": chunk.text,
                    "document_id": chunk.document_id,
                    "document_name": chunk.document_name,
                    "chunk_index": chunk.chunk_index,
                    "metadata": chunk.metadata
                })
            
            # Store in Milvus
            print(f"💾 Storing in vector database...")
            inserted_count = self.db.add_chunks(milvus_data)
            
            # Copy file to documents directory
            dest_path = os.path.join(self.config.documents_dir, f"{document_id}_{document_name}")
            shutil.copy2(file_path, dest_path)
            
            return ProcessResult(
                success=True,
                document_id=document_id,
                document_name=document_name,
                chunk_count=inserted_count,
                message=f"✅ Successfully processed {document_name}: {inserted_count} chunks created"
            )
        
        except Exception as e:
            return ProcessResult(
                success=False,
                document_id=document_id if 'document_id' in locals() else "",
                document_name=document_name or "",
                chunk_count=0,
                message="",
                error=f"Processing failed: {str(e)}"
            )
    
    def _generate_document_id(self, document_name: str) -> str:
        """Generate unique document ID from name"""
        # Use hash of name + timestamp for uniqueness
        content = f"{document_name}_{datetime.now().isoformat()}"
        hash_obj = hashlib.md5(content.encode())
        return f"doc_{hash_obj.hexdigest()[:12]}"


if __name__ == "__main__":
    # Test document processor
    from .config_loader import load_config
    
    print("Testing document processor...")
    
    # Load config
    config = load_config()
    
    # Create test document
    test_file = "test_doc.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("This is a test document. " * 50)
    
    # Process
    processor = DocumentProcessor(config)
    result = processor.process_document(test_file)
    
    if result.success:
        print(f"✓ {result.message}")
        print(f"  Document ID: {result.document_id}")
        print(f"  Chunks: {result.chunk_count}")
    else:
        print(f"❌ {result.error}")
    
    # Cleanup
    os.remove(test_file)
    print("✓ Cleaned up test file")
