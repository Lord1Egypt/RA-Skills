"""
Document chunker for Enterprise Knowledge Base

Splits documents into semantic chunks with overlap.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import re


@dataclass
class Chunk:
    """Document chunk"""
    id: str
    text: str
    document_id: str
    document_name: str
    chunk_index: int
    metadata: Dict[str, Any]


class DocumentChunker:
    """Split documents into overlapping chunks"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize chunker
        
        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str, document_id: str, document_name: str,
                   metadata: Dict[str, Any] = None) -> List[Chunk]:
        """
        Split text into chunks
        
        Args:
            text: Document text
            document_id: Unique document ID
            document_name: Document filename
            metadata: Additional metadata
        
        Returns:
            List[Chunk]: List of chunks
        """
        if not text or not text.strip():
            return []
        
        # Clean text
        text = self._clean_text(text)
        
        # Split into sentences
        sentences = self._split_sentences(text)
        
        # Group sentences into chunks
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence exceeds chunk_size, save current chunk
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append(chunk_text)
                
                # Keep overlap sentences
                overlap_text = chunk_text[-self.chunk_overlap:] if len(chunk_text) > self.chunk_overlap else chunk_text
                current_chunk = [s for s in current_chunk if s in overlap_text]
                current_length = sum(len(s) for s in current_chunk)
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # Add last chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        # Create Chunk objects
        result = []
        for i, chunk_text in enumerate(chunks):
            chunk = Chunk(
                id=f"{document_id}_chunk_{i}",
                text=chunk_text,
                document_id=document_id,
                document_name=document_name,
                chunk_index=i,
                metadata=metadata or {}
            )
            result.append(chunk)
        
        return result
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        
        Uses simple heuristics for sentence boundaries.
        """
        # Split on sentence endings
        sentences = re.split(r'([.!?]+\s+)', text)
        
        # Recombine sentences with their punctuation
        result = []
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i]
            if i + 1 < len(sentences):
                sentence += sentences[i + 1]
            sentence = sentence.strip()
            if sentence:
                result.append(sentence)
        
        # Handle last sentence if no punctuation
        if len(sentences) % 2 == 1 and sentences[-1].strip():
            result.append(sentences[-1].strip())
        
        return result


if __name__ == "__main__":
    # Test chunker
    print("Testing document chunker...")
    
    chunker = DocumentChunker(chunk_size=100, chunk_overlap=20)
    
    test_text = """
    This is the first sentence. This is the second sentence. 
    This is the third sentence. This is the fourth sentence.
    This is the fifth sentence. This is the sixth sentence.
    """
    
    chunks = chunker.chunk_text(
        text=test_text,
        document_id="test_doc",
        document_name="test.txt"
    )
    
    print(f"✓ Created {len(chunks)} chunks")
    for chunk in chunks:
        print(f"\nChunk {chunk.chunk_index}:")
        print(f"  ID: {chunk.id}")
        print(f"  Text: {chunk.text[:80]}...")
        print(f"  Length: {len(chunk.text)} chars")
