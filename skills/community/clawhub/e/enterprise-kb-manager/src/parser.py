"""
Document parser for Enterprise Knowledge Base

Parses various document formats (PDF, DOCX, TXT, MD).
"""

import os
from pathlib import Path
from typing import Optional


class DocumentParser:
    """Parse documents to extract text"""
    
    SUPPORTED_FORMATS = {'.txt', '.md', '.pdf', '.docx'}
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """Check if file format is supported"""
        ext = Path(file_path).suffix.lower()
        return ext in DocumentParser.SUPPORTED_FORMATS
    
    @staticmethod
    def parse(file_path: str) -> str:
        """
        Parse document and extract text
        
        Args:
            file_path: Path to document file
        
        Returns:
            Extracted text content
        
        Raises:
            ValueError: If file format not supported
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        ext = Path(file_path).suffix.lower()
        
        if ext == '.txt':
            return DocumentParser._parse_txt(file_path)
        elif ext == '.md':
            return DocumentParser._parse_md(file_path)
        elif ext == '.pdf':
            return DocumentParser._parse_pdf(file_path)
        elif ext == '.docx':
            return DocumentParser._parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    @staticmethod
    def _parse_txt(file_path: str) -> str:
        """Parse plain text file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    @staticmethod
    def _parse_md(file_path: str) -> str:
        """Parse Markdown file"""
        # For now, treat as plain text
        # Could use markdown library to preserve structure
        return DocumentParser._parse_txt(file_path)
    
    @staticmethod
    def _parse_pdf(file_path: str) -> str:
        """Parse PDF file"""
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")
        
        try:
            reader = PdfReader(file_path)
            text_parts = []
            
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            return "\n\n".join(text_parts)
        
        except Exception as e:
            raise RuntimeError(f"Failed to parse PDF: {e}")
    
    @staticmethod
    def _parse_docx(file_path: str) -> str:
        """Parse DOCX file"""
        try:
            from docx import Document
        except ImportError:
            raise ImportError("python-docx not installed. Run: pip install python-docx")
        
        try:
            doc = Document(file_path)
            text_parts = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            return "\n\n".join(text_parts)
        
        except Exception as e:
            raise RuntimeError(f"Failed to parse DOCX: {e}")


if __name__ == "__main__":
    # Test parser
    print("Testing document parser...")
    
    # Create test file
    test_file = "test_document.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("This is a test document.\n\nIt has multiple paragraphs.")
    
    # Test parsing
    text = DocumentParser.parse(test_file)
    print(f"✓ Parsed text ({len(text)} chars):")
    print(f"  {text[:100]}...")
    
    # Test format check
    print(f"✓ Supported: {DocumentParser.is_supported(test_file)}")
    print(f"✓ Unsupported: {DocumentParser.is_supported('test.exe')}")
    
    # Cleanup
    os.remove(test_file)
    print("✓ Cleaned up test file")
