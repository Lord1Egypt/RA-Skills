#!/usr/bin/env python3
"""
Document Converter to Markdown with Semantic Search

This script converts PDF, EPUB, Djvu and other formats to Markdown,
extracts semantic embeddings and enables content search.

Usage:
    python document_semantic_rag.py --convert file.pdf
    python document_semantic_rag.py --calibre-id 123 --format PDF
    python document_semantic_rag.py --search "search term"
    python document_semantic_rag.py --convert-all ./folder
    python document_semantic_rag.py --list
    python document_semantic_rag.py --check
"""

# Basic imports (always necessary)
import os
import sys
import re
import argparse
import json
import hashlib
import signal
import string
import random
import sqlite3
import contextlib
import inspect
from pathlib import Path
from typing import List, Dict, Any, Optional
import subprocess
import shutil
from datetime import datetime
import time
from dotenv import load_dotenv
import importlib.util

# Global variables for loaded library control
_doc_libraries_loaded = False
_embedding_libraries_loaded = False
_chroma_loaded = False

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_DATA_DIR = Path("/tmp/openclaw-calibre-rag/data")
DEFAULT_CONVERTED_DIR = Path("/tmp/openclaw-calibre-rag/converteds")
DEFAULT_CALIBRE_METADATA_DB = None
RAG_REQUIREMENTS = SKILL_DIR / "scripts" / "requirements-rag.txt"
FORMAT_PRIORITY = ["PDF", "EPUB", "DJVU", "AZW3", "MOBI", "FB2", "TXT", "RTF", "DOCX", "HTMLZ"]
SECTION_PREFIX_RE = re.compile(
    r"^\s*(cap[ií]tulo|chapter|parte|part|se[cç][aã]o|section|livro|book|"
    r"pref[aá]cio|introdu[cç][aã]o|conclus[aã]o|ap[eê]ndice|appendix)\b",
    re.IGNORECASE,
)


def log_event(level: str, message: str, **params):
    """
    Register event in PDCL structured format (captures line automatically)
    
    Args:
        level: Log level (INFO, ALERT, ERROR, SUCCESS, DEBUG, START, END, DATA, TOOL, CACHE, SAVE)
        message: Event message
        **params: Additional parameters
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emoji_map = {
        'INFO': 'ℹ️',
        'ALERT': '⚠️',
        'ERROR': '❌',
        'SUCCESS': '✅',
        'DEBUG': '🔍',
        'START': '🚀',
        'END': '🏁',
        'DATA': '📊',
        'TOOL': '🔧',
        'CACHE': '📂',
        'SAVE': '💾'
    }
    emoji = emoji_map.get(level, 'ℹ️')
    
    # Automatically capture file, function and line
    frame = inspect.currentframe().f_back
    file = inspect.getfile(frame)
    func = inspect.getframeinfo(frame).function
    line = inspect.getframeinfo(frame).lineno
    
    param_str = ''
    if params:
        param_str = ' - ' + ', '.join(f'{k}={v}' for k, v in params.items())
    
    print(f"[{timestamp}] [{file}:{func}:{line}] {emoji} {message}{param_str}", file=sys.stderr)


def resolve_calibre_document(book_id: int, fmt: str | None = None, metadata_db: str | None = DEFAULT_CALIBRE_METADATA_DB) -> Path:
    """Resolve the actual path of a book format in Calibre's metadata.db."""
    if not metadata_db:
        raise FileNotFoundError("metadata.db path is not configured. Use the calibre-ebooks Books API first, or pass --calibre-metadata-db / set CALIBRE_METADATA_DB for local fallback.")
    db_path = Path(metadata_db).expanduser().resolve()
    if not db_path.exists():
        raise FileNotFoundError(f"metadata.db not found: {db_path}")

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT b.path, d.name, d.format
            FROM books b
            JOIN data d ON d.book = b.id
            WHERE b.id = ?
            ORDER BY d.format
            """,
            (book_id,),
        ).fetchall()
        if not rows:
            raise FileNotFoundError(f"Book {book_id} has no available formats")

        row = None
        if fmt:
            row = next((r for r in rows if r["format"].upper() == fmt.upper()), None)
            if row is None:
                formats = ", ".join(r["format"] for r in rows) or "none"
                raise FileNotFoundError(f"Book {book_id} has no format {fmt}. Available formats: {formats}")
        else:
            row = min(
                rows,
                key=lambda r: (
                    FORMAT_PRIORITY.index(r["format"].upper())
                    if r["format"].upper() in FORMAT_PRIORITY
                    else len(FORMAT_PRIORITY),
                    r["format"].upper(),
                ),
            )

        file_path = db_path.parent / row["path"] / f"{row['name']}.{row['format'].lower()}"
        if not file_path.exists():
            raise FileNotFoundError(f"Calibre file not found: {file_path}")
        return file_path
    finally:
        conn.close()


def runtime_check() -> Dict[str, Any]:
    """Check Python dependencies and external binaries without loading heavy modules."""
    python_modules = [
        "fitz",
        "ebooklib",
        "pytesseract",
        "PIL",
        "pdf2image",
        "markdownify",
        "bs4",
        "numpy",
        "sentence_transformers",
        "ollama",
        "chromadb",
        "dotenv",
    ]
    binaries = ["ollama", "tesseract", "pdftoppm", "calibredb"]
    return {
        "python": sys.version.split()[0],
        "modules": {name: importlib.util.find_spec(name) is not None for name in python_modules},
        "binaries": {name: shutil.which(name) for name in binaries},
        "skill_dir": str(SKILL_DIR),
        "calibre_metadata_db": str(DEFAULT_CALIBRE_METADATA_DB) if DEFAULT_CALIBRE_METADATA_DB else None,
        "calibre_metadata_db_exists": Path(DEFAULT_CALIBRE_METADATA_DB).exists() if DEFAULT_CALIBRE_METADATA_DB else None,
    }

# Functions to load libraries on demand
def load_document_libraries():
    """Load document processing libraries only when necessary."""
    global _doc_libraries_loaded
    if _doc_libraries_loaded:
        return
    
    log_event('START', 'Loading document processing libraries')
    try:
        global fitz, ebooklib, epub, pytesseract, Image, pdf2image, markdownify, BeautifulSoup
        import fitz  # PyMuPDF
        log_event('SUCCESS', 'PyMuPDF loaded')
        import ebooklib
        from ebooklib import epub
        log_event('SUCCESS', 'Ebooklib loaded')
        import pytesseract
        log_event('SUCCESS', 'Pytesseract loaded')
        from PIL import Image
        log_event('SUCCESS', 'PIL loaded')
        import pdf2image
        log_event('SUCCESS', 'PDF2Image loaded')
        import markdownify
        log_event('SUCCESS', 'Markdownify loaded')
        from bs4 import BeautifulSoup
        log_event('SUCCESS', 'BeautifulSoup loaded')
        log_event('SUCCESS', 'Document processing libraries loaded successfully')
        _doc_libraries_loaded = True
    except ImportError as e:
        log_event('ERROR', 'Required library not found', error=str(e))
        log_event('INFO', 'Install dependencies', command=f'pip install -r {RAG_REQUIREMENTS}')
        sys.exit(1)

def load_embedding_libraries():
    """Load embedding libraries only when necessary."""
    global _embedding_libraries_loaded
    if _embedding_libraries_loaded:
        return
    
    log_event('START', 'Loading embedding and semantic search libraries')
    try:
        global np, SentenceTransformer, ollama
        import numpy as np
        log_event('SUCCESS', 'NumPy loaded')
        log_event('INFO', 'Loading SentenceTransformer')
        from sentence_transformers import SentenceTransformer
        log_event('SUCCESS', 'SentenceTransformers loaded')
        import ollama
        log_event('SUCCESS', 'Ollama loaded')
        log_event('SUCCESS', 'Embedding libraries loaded successfully')
        _embedding_libraries_loaded = True
    except ImportError as e:
        log_event('ERROR', 'Required library not found', error=str(e))
        log_event('INFO', 'Install dependencies', command=f'pip install -r {RAG_REQUIREMENTS}')
        sys.exit(1)

def load_chroma_library():
    """Load ChromaDB only when necessary."""
    global _chroma_loaded
    if _chroma_loaded:
        return
    
    try:
        global chromadb
        import chromadb
        log_event('SUCCESS', 'ChromaDB loaded')
        _chroma_loaded = True
    except ImportError as e:
        log_event('ERROR', 'Required library not found', error=str(e))
        log_event('INFO', 'Install dependencies', command=f'pip install -r {RAG_REQUIREMENTS}')
        sys.exit(1)


class DocumentConverter:
    def __init__(self, data_dir: str = None, embedding_model: str = None,
                 converted_dir: str = None, tesseract_lang: str = "por", 
                 chunk_size: int = 500, chunk_overlap: int = 50, command_type: str = "full",
                 allow_model_mismatch: bool = False, allow_model_pull: bool = False):
        # Load skill environment variables first. A .env from CWD can complement
        # without overwriting this skill's specific configuration.
        skill_env = SKILL_DIR / '.env'
        cwd_env = Path.cwd() / '.env'
        if skill_env.is_file():
            load_dotenv(dotenv_path=skill_env, override=False)
        if cwd_env.is_file() and cwd_env.resolve() != skill_env.resolve():
            load_dotenv(dotenv_path=cwd_env, override=False)
        load_dotenv(override=False)
        
        # Override with environment variables if they exist
        self._data_dir_explicit = data_dir is not None
        data_dir_env = data_dir or os.getenv('DATA_DIR') or DEFAULT_DATA_DIR
        self.data_dir = Path(data_dir_env).expanduser().resolve()
        self.embedding_model = embedding_model or os.getenv('OLLAMA_MODEL', 'nomic-embed-text-v2-moe')
        self.tesseract_lang = os.getenv('TESSERACT_LANG', tesseract_lang)
        self.chunk_size = int(os.getenv('CHUNK_SIZE', str(chunk_size)))
        self.chunk_overlap = int(os.getenv('CHUNK_OVERLAP', str(chunk_overlap)))
        self.similarity_threshold = float(os.getenv('SIMILARITY_THRESHOLD', '0.3'))
        self.allow_model_mismatch = allow_model_mismatch or os.getenv('RAG_ALLOW_MODEL_MISMATCH', '').lower() in {'1', 'true', 'yes', 's', 'sim'}
        self.allow_model_pull = allow_model_pull or os.getenv('RAG_ALLOW_MODEL_PULL', '').lower() in {'1', 'true', 'yes', 's', 'sim'}
        
        # Configure converted documents folder
        if converted_dir:
            self.docs_dir = Path(converted_dir).expanduser().resolve()
        else:
            converted_dir_env = os.getenv('CONVERTED_DIR')
            if converted_dir_env:
                self.docs_dir = Path(converted_dir_env).expanduser().resolve()
            else:
                self.docs_dir = Path(DEFAULT_CONVERTED_DIR).expanduser().resolve()
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        log_event('SUCCESS', 'Directories created/verified successfully', data_dir=str(self.data_dir), docs_dir=str(self.docs_dir))
        
        # Interruption control
        self.interrupted = False
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        log_event('SUCCESS', 'Signal handlers configured')
        
        # Configure logging
        log_event('INFO', 'Configuring logging system')
        self._setup_logging()
        
        # Configure databases according to command
        log_event('INFO', 'Configuring databases')
        self._setup_databases(command_type=command_type)  # Use the passed command type
        log_event('SUCCESS', 'Initialization completed')
    
    def _signal_handler(self, signum, frame):
        """Handler for graceful interruption."""
        log_event('ALERT', 'Interruption detected! Finishing gracefully', signal=signum)
        log_event('INFO', 'Already processed files were saved')
        log_event('INFO', 'You can continue from where you left off')
        self.interrupted = True
    
    def _setup_logging(self):
        """Configure logging system."""
        self.log_file = self.data_dir / f"converter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.start_time = time.time()
        
        # Initialize chroma_path here to be able to use in alert.
        chroma_env = None if self._data_dir_explicit else os.getenv('CHROMA_DB_PATH')
        self.chroma_path = Path(chroma_env).expanduser().resolve() if chroma_env else self.data_dir / "chroma_db"
        
        log_event('INFO', 'Log started', log_file=str(self.log_file))
        log_event('INFO', 'Output folder', docs_dir=str(self.docs_dir))
        log_event('INFO', 'Embedding model', model=self.embedding_model)
        log_event('INFO', 'OCR language', lang=self.tesseract_lang)
        log_event('INFO', 'Chunk size', size=self.chunk_size)
        log_event('INFO', 'Chunk overlap', overlap=self.chunk_overlap)
        log_event('INFO', 'Similarity threshold', threshold=self.similarity_threshold)
        
        # Alert about embedding model
        if self.chroma_path.exists() and any(self.chroma_path.iterdir()):
            log_event('ALERT', 'Embedding base already exists', chroma_path=str(self.chroma_path))
            log_event('ALERT', 'To change model, delete the .data directory and recreate with new model')
            log_event('ALERT', 'Current model', model=self.embedding_model)
    
    def _log(self, message: str, level: str = "INFO"):
        """Register message in log and console using log_event."""
        # Use log_event for structured logging
        log_event(level, message)
        
        # Also save to file
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def _show_progress(self, current: int, total: int, prefix: str = "", suffix: str = ""):
        """Show progress bar."""
        if total == 0:
            return
            
        percent = (current / total) * 100
        filled_length = int(50 * current // total)
        bar = '█' * filled_length + '-' * (50 - filled_length)
        
        print(f'\r{prefix} |{bar}| {percent:.1f}% {current}/{total} {suffix}', end='', flush=True)
        
        if current == total:
            print()  # New line when complete
    
    def _format_time(self, seconds: float) -> str:
        """Format time in readable format."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
    
    def _ensure_ollama_model(self):
        """Check if Ollama model is installed, if not, install it."""
        try:
            self._log("Checking Ollama model...", "INFO")
            # Check available models
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if self.embedding_model not in result.stdout:
                if not self.allow_model_pull:
                    self._log(f"Model {self.embedding_model} not found. Run 'ollama pull {self.embedding_model}' or enable RAG_ALLOW_MODEL_PULL.", "ERROR")
                    raise Exception("Ollama model is missing and automatic model pull is disabled")
                self._log(f"Model {self.embedding_model} not found. Installing...", "WARN")
                self._show_progress(0, 1, "Installing model", self.embedding_model)
                install_result = subprocess.run(['ollama', 'pull', self.embedding_model], 
                                              capture_output=True, text=True)
                self._show_progress(1, 1, "Installing model", self.embedding_model)
                if install_result.returncode == 0:
                    self._log(f"Model {self.embedding_model} installed successfully!", "INFO")
                else:
                    self._log(f"Error installing model: {install_result.stderr}", "ERROR")
                    raise Exception("Model installation failed")
            else:
                self._log(f"Model {self.embedding_model} is already installed", "INFO")
        except FileNotFoundError:
            self._log("Error: Ollama is not installed or not in PATH", "ERROR")
            self._log("Install Ollama at: https://ollama.ai/", "INFO")
            sys.exit(1)
    
    def _init_embedding_model(self):
        """Initialize the embedding model."""
        # Ensure embedding libraries are loaded
        load_embedding_libraries()
        
        try:
            # Try to use Ollama first
            self.model_type = "ollama"
            self._log(f"Using Ollama model: {self.embedding_model}", "INFO")
        except Exception as e:
            self._log(f"Error initializing Ollama: {e}", "ERROR")
            # Fallback to sentence-transformers
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self.model_type = "sentence_transformers"
                self._log("Using Sentence Transformers as fallback", "INFO")
            except Exception as e2:
                self._log(f"Error loading fallback model: {e2}", "ERROR")
                sys.exit(1)
    
    def get_embedding(self, text: str) -> Any:
        """Generate embedding for a text."""
        # Ensure embedding libraries are loaded
        load_embedding_libraries()
        
        if self.model_type == "ollama":
            try:
                result = ollama.embeddings(model=self.embedding_model, prompt=text)
                return np.array(result['embedding'])
            except Exception as e:
                log_event('ERROR', 'Error generating embedding with Ollama', error=str(e))
                # Fallback
                if self.model:
                    return self.model.encode(text)
                else:
                    raise e
        else:
            return self.model.encode(text)
    
    def convert_pdf_to_md(self, pdf_path: Path) -> str:
        """Convert PDF to Markdown cleanly."""
        # Load document libraries only when necessary
        load_document_libraries()
        
        try:
            self._log(f"Starting PDF conversion: {pdf_path.name}", "INFO")
            doc = fitz.open(str(pdf_path))
            total_pages = len(doc)
            markdown_content = []
            
            self._show_progress(0, total_pages, "Converting PDF", f"pages")
            
            for page_num in range(total_pages):
                if self.interrupted:
                    self._log("Conversion interrupted by user", "WARN")
                    return ""
                
                page = doc[page_num]
                
                # Extract text
                text = page.get_text()
                section_title = self._detect_section_title(text)
                
                # Clean the text
                text = self._clean_text(text)
                
                if text.strip():
                    section_marker = (
                        f"\n\n### Section: {section_title}"
                        if section_title
                        else ""
                    )
                    markdown_content.append(
                        f"## Page {page_num + 1}{section_marker}\n\n{text}\n"
                    )
                
                self._show_progress(page_num + 1, total_pages, "Converting PDF", f"pages")
            
            doc.close()
            self._log(f"PDF converted: {total_pages} pages processed", "SUCCESS")
            return "\n".join(markdown_content)
        except Exception as e:
            self._log(f"Error converting PDF {pdf_path}: {e}", "ERROR")
            return ""
    
    def convert_epub_to_md(self, epub_path: Path) -> str:
        """Convert EPUB to Markdown."""
        # Load document libraries only when necessary
        load_document_libraries()
        
        try:
            book = epub.read_epub(str(epub_path))
            markdown_content = []
            
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    # Convert HTML to Markdown
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    # Remove scripts and styles
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Convert to Markdown
                    html_content = str(soup)
                    md_content = markdownify.markdownify(html_content)
                    
                    # Clean content
                    md_content = self._clean_markdown(md_content)
                    
                    if md_content.strip():
                        markdown_content.append(md_content)
            
            return "\n\n".join(markdown_content)
        except Exception as e:
            log_event('ERROR', 'Error converting EPUB', file=str(epub_path), error=str(e))
            return ""
    
    def convert_djvu_to_md(self, djvu_path: Path) -> str:
        """Convert Djvu to Markdown using OCR (requires manual DjVu support installation)."""
        # Load document libraries only when necessary
        load_document_libraries()
        
        try:
            # Check if DjVu support is available
            try:
                import djvu.decode
            except ImportError:
                log_event('ALERT', 'DjVu support is not available')
                log_event('INFO', 'Install dependencies manually')
                log_event('INFO', 'sudo apt-get install djvulibre-bin  # Ubuntu/Debian')
                log_event('INFO', 'brew install djvulibre  # macOS')
                log_event('INFO', 'Or download from https://djvu.org/  # Windows')
                return ""
            
            # Convert Djvu to images
            images = pdf2image.convert_from_path(str(djvu_path))
            
            markdown_content = []
            
            for i, image in enumerate(images):
            # OCR using Tesseract
                text = pytesseract.image_to_string(image, lang=self.tesseract_lang)
                
                # Clean text
                text = self._clean_text(text)
                
                if text.strip():
                    markdown_content.append(f"## Page {i + 1}\n\n{text}\n")
            
            return "\n".join(markdown_content)
        except Exception as e:
            log_event('ERROR', 'Error converting Djvu', file=str(djvu_path), error=str(e))
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean text extracted from documents."""
        # Remove excessive line breaks
        text = ' '.join(text.split())
        
        # Remove problematic special characters
        text = text.replace('ﬁ', 'fi').replace('ﬂ', 'fl')
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('"', '"').replace('"', '"')
        
        # Normalize spaces
        text = ' '.join(text.split())
        
        return text
    
    def _clean_markdown(self, md_content: str) -> str:
        """Clean Markdown content."""
        # Remove residual HTML tags
        md_content = re.sub(r'<[^>]+>', '', md_content)
        
        # Clean excessive spaces
        md_content = re.sub(r'\n\s*\n', '\n\n', md_content)
        
        return md_content.strip()

    def _detect_section_title(self, text: str) -> Optional[str]:
        """Detect a likely chapter/section title in raw document text."""
        for raw_line in (text or "").splitlines():
            line = " ".join(raw_line.strip().split())
            if self._looks_like_section_title(line):
                return line[:160]
        return None

    @staticmethod
    def _looks_like_section_title(line: str) -> bool:
        if not line or len(line) < 4 or len(line) > 140:
            return False
        if not re.search(r"[A-Za-zÀ-ÖØ-öø-ÿ]", line):
            return False
        if line.endswith((".", ",", ";", ":")) and not SECTION_PREFIX_RE.search(line):
            return False
        words = line.split()
        if len(words) > 14:
            return False
        if SECTION_PREFIX_RE.search(line):
            return True
        letters = [char for char in line if char.isalpha()]
        if letters:
            uppercase_ratio = sum(1 for char in letters if char.isupper()) / len(letters)
            if uppercase_ratio >= 0.65:
                return True
        title_like_words = sum(1 for word in words if word[:1].isupper())
        return len(words) <= 8 and title_like_words >= max(1, len(words) // 2)
    
    def process_document(self, file_path: Path) -> Dict[str, Any]:
        """Process a document and extract embeddings using databases."""
        if self.interrupted:
            self._log("Processing interrupted", "WARN")
            return {}
        
        # Generate unique ID for the book
        book_id = self._generate_id()
        
        # Check if book already exists in SQLite
        absolute_file_path = file_path.resolve()
        cursor = self.conn.execute('SELECT id FROM books WHERE file_path = ?', (str(absolute_file_path),))
        existing_book = cursor.fetchone()
        existing_book_id = existing_book['id'] if existing_book else None
        
        # If book exists and hasn't changed, skip processing
        if existing_book_id and self._is_book_unchanged(file_path, existing_book_id):
            self._log(f"Book {file_path.name} already processed and unchanged (ID: {existing_book_id})", "INFO")
            return {'book_id': existing_book_id}
        
        # If book exists but changed, remove old data
        if existing_book_id:
            self._log(f"Book {file_path.name} modified, reprocessing (ID: {existing_book_id})", "INFO")
            self.delete_book(existing_book_id)
        
        file_hash = self._get_file_hash(file_path)
        md_path = self.docs_dir / f"{file_path.stem}.md"
        
        # Convert to Markdown
        self._log(f"Processing {file_path.name} (ID: {book_id})...", "INFO")
        self._log(f"Saving to: {self.docs_dir}", "INFO")
        
        start_time = time.time()
        
        if file_path.suffix.lower() == '.pdf':
            md_content = self.convert_pdf_to_md(file_path)
        elif file_path.suffix.lower() == '.epub':
            md_content = self.convert_epub_to_md(file_path)
        elif file_path.suffix.lower() == '.djvu':
            md_content = self.convert_djvu_to_md(file_path)
        else:
            self._log(f"Unsupported format: {file_path.suffix}", "ERROR")
            return {}
        
        if self.interrupted:
            return {}
            
        if not md_content:
            self._log(f"Failed to convert {file_path.name}", "ERROR")
            return {}
        
        # Save Markdown
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        conversion_time = time.time() - start_time
        self._log(f"Conversion completed in {self._format_time(conversion_time)}", "SUCCESS")
        
        # Extract embeddings
        self._log(f"Extracting embeddings from {file_path.name}...", "INFO")
        chunk_dicts = self._split_into_chunks(md_content, file_path.stem, chunk_size=None, chunk_overlap=None)
        
        # Filter empty chunks before generating embeddings
        valid_chunks = [c for c in chunk_dicts if c['text'].strip()]
        
        # Generate embeddings for each valid chunk
        total_valid = len(valid_chunks)
        embeddings = []
        for i, chunk_info in enumerate(valid_chunks):
            if self.interrupted:
                return {}
            embedding = self.get_embedding(chunk_info['text'])
            embeddings.append(embedding)
            if (i + 1) % 10 == 0 or i == total_valid - 1:
                self._show_progress(i + 1, total_valid, "Generating embeddings", "chunks")
        
        embedding_time = time.time() - start_time - conversion_time
        self._log(f"Embeddings generated in {self._format_time(embedding_time)}", "SUCCESS")
        
        # Save to databases
        self._save_book_to_sqlite(book_id, file_path, {
            'chunk_count': len(valid_chunks),
            'embedding_count': len(embeddings),
            'conversion_time': conversion_time
        })
        
        self._save_chunks_to_sqlite(book_id, valid_chunks)
        self._save_embeddings_to_chroma(book_id, valid_chunks, embeddings)
        
        total_time = time.time() - start_time
        self._log(f"Book {file_path.name} processed successfully! ID: {book_id} ({self._format_time(total_time)})", "SUCCESS")
        return {'book_id': book_id}
    
    def _split_into_chunks(self, content: str, doc_name: str = None, chunk_size: int = None, chunk_overlap: int = None) -> List[Dict[str, Any]]:
        """Divide content into chunks with page tracking.
        
        Returns list of dicts:
        [{'text': str, 'page': str, 'section_title': Optional[str]}, ...]
        """
        chunk_size = chunk_size or self.chunk_size
        chunk_overlap = chunk_overlap or self.chunk_overlap
        
        # If overlap is larger than chunk size, adjust
        if chunk_overlap >= chunk_size:
            chunk_overlap = chunk_size // 4  # 25% overlap as fallback
        
        self._log(f"Dividing content into chunks of {chunk_size} characters with {chunk_overlap} overlap", "INFO")
        
        # Pattern to detect page markers
        page_pattern = re.compile(r'## Page (\d+)')
        section_pattern = re.compile(r'### Section:\s*(.+)')
        
        # Split by paragraphs and track current page
        paragraphs = content.split('\n\n')
        chunks = []  # Lista de {'text': str, 'page': str, 'section_title': str}
        
        current_chunk = ""
        current_page = "1"
        chunk_start_page = "1"
        current_section = None
        chunk_start_section = None
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Detect page marker in paragraph
            page_match = page_pattern.search(paragraph)
            if page_match:
                current_page = page_match.group(1)

            section_match = section_pattern.search(paragraph)
            if section_match:
                current_section = section_match.group(1).strip()[:160]
            else:
                detected_section = self._detect_section_title(paragraph)
                if detected_section:
                    current_section = detected_section
            
            # If adding paragraph doesn't exceed chunk size
            if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
                    chunk_start_page = current_page
                    chunk_start_section = current_section
            else:
                # Save current chunk if not empty
                if current_chunk.strip():
                    chunks.append({
                        'text': current_chunk.strip(),
                        'page': chunk_start_page,
                        'section_title': chunk_start_section,
                    })
                
                # Start new chunk with paragraph
                current_chunk = paragraph
                chunk_start_page = current_page
                chunk_start_section = current_section
        
        # Save last chunk
        if current_chunk.strip():
            chunks.append({
                'text': current_chunk.strip(),
                'page': chunk_start_page,
                'section_title': chunk_start_section,
            })
        
        # Add overlap between chunks
        if chunk_overlap > 0 and len(chunks) > 1:
            overlapped_chunks = []
            
            for i, chunk_info in enumerate(chunks):
                # Keep original chunk
                overlapped_chunks.append(chunk_info)
                
                # If not last chunk, add overlapped chunk
                if i < len(chunks) - 1:
                    next_chunk = chunks[i + 1]
                    
                    # Take start of next chunk for overlap
                    overlap_text = next_chunk['text'][:chunk_overlap]
                    
                    # Create overlapped chunk (inherits page from current chunk)
                    overlapped_text = chunk_info['text'][-chunk_overlap:] + " " + overlap_text
                    overlapped_chunks.append({
                        'text': overlapped_text.strip(),
                        'page': chunk_info['page'],
                        'section_title': chunk_info.get('section_title'),
                    })
            
            self._log(f"Created {len(chunks)} original chunks + {len(chunks)-1} overlapped chunks = {len(overlapped_chunks)} total", "INFO")
            return overlapped_chunks
        
        self._log(f"Created {len(chunks)} chunks without overlap", "INFO")
        return chunks
    
    def _setup_databases(self, command_type: str = "full"):
        """Configure SQLite and ChromaDB databases according to the command."""
        log_event('INFO', 'Configuring SQLite')
        # Configure SQLite
        sqlite_env = None if self._data_dir_explicit else os.getenv('SQLITE_DB_PATH')
        self.db_path = Path(sqlite_env).expanduser().resolve() if sqlite_env else self.data_dir / "documents.db"
        self._init_sqlite()
        log_event('SUCCESS', 'SQLite configured', db_path=str(self.db_path))
        
        # Load embedding libraries only if necessary
        if command_type in ["search", "convert", "interactive"]:
            load_embedding_libraries()
            load_chroma_library()
            
            log_event('INFO', 'Configuring ChromaDB')
            # Configure ChromaDB (chroma_path was already created in _setup_logging)
            self._init_chroma()
            log_event('SUCCESS', 'ChromaDB configured', chroma_path=str(self.chroma_path))
            
            log_event('INFO', 'Checking Ollama model')
            # Check and install Ollama model if necessary
            self._ensure_ollama_model()
            
            log_event('INFO', 'Initializing embedding model')
            # Initialize embedding model
            self.model = None
            self._init_embedding_model()
            log_event('SUCCESS', 'Embedding model initialized', model=self.embedding_model)
            
            log_event('INFO', 'Checking model compatibility')
            # Check model compatibility with existing database
            self._check_embedding_model_compatibility()
        
        self._log("Databases configured", "INFO")
    
    def _init_sqlite(self):
        """Initialize SQLite database."""
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row  # To access columns by name
            
            # Create tables
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id TEXT PRIMARY KEY,
                    file_path TEXT UNIQUE,
                    file_hash TEXT,
                    file_size INTEGER,
                    processed_at TIMESTAMP,
                    chunk_count INTEGER,
                    embedding_count INTEGER,
                    conversion_time REAL,
                    metadata TEXT
                )
            ''')
            
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    book_id TEXT,
                    chunk_index INTEGER,
                    content TEXT,
                    page_number TEXT,
                    section_title TEXT,
                    created_at TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books (id)
                )
            ''')
            self.conn.execute(
                'ALTER TABLE chunks ADD COLUMN section_title TEXT'
            )
        except sqlite3.OperationalError as e:
            if 'duplicate column name' not in str(e).lower():
                raise
        try:
            
            # Table for system metadata
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS system_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            self._log("SQLite database initialized", "INFO")
        except Exception as e:
            self._log(f"Error initializing SQLite: {e}", "ERROR")
            raise
    
    def _save_embedding_model(self):
        """Save current embedding model in metadata."""
        try:
            self.conn.execute('''
                INSERT OR REPLACE INTO system_metadata (key, value, updated_at)
                VALUES (?, ?, ?)
            ''', ('embedding_model', self.embedding_model, datetime.now().isoformat()))
            self.conn.commit()
            self._log(f"Embedding model saved: {self.embedding_model}", "INFO")
        except Exception as e:
            self._log(f"Error saving embedding model: {e}", "ERROR")
    
    def _get_stored_embedding_model(self) -> Optional[str]:
        """Get stored embedding model from database."""
        try:
            cursor = self.conn.execute('SELECT value FROM system_metadata WHERE key = ?', ('embedding_model',))
            result = cursor.fetchone()
            return result['value'] if result else None
        except Exception as e:
            self._log(f"Error getting stored model: {e}", "ERROR")
            return None
    
    def _check_embedding_model_compatibility(self):
        """Check if current model is compatible with existing database."""
        stored_model = self._get_stored_embedding_model()
        
        if stored_model is None:
            # First initialization - save current model
            self._save_embedding_model()
            return
        
        if stored_model != self.embedding_model:
            self._log(f"⚠️  **CRITICAL MODEL ALERT**", "ERROR")
            self._log(f"Stored model: {stored_model}", "ERROR")
            self._log(f"Current model: {self.embedding_model}", "ERROR")
            self._log(f"Embeddings were generated with '{stored_model}' and are not compatible with '{self.embedding_model}'", "ERROR")
            self._log(f"**Solutions:**", "ERROR")
            self._log(f"1. Use the same model: --embedding-model {stored_model}", "ERROR")
            self._log(f"2. Delete the database and recreate with new model:", "ERROR")
            self._log(f"   move or clean {self.data_dir}", "ERROR")
            self._log(f"3. Migrate embeddings (advanced)", "ERROR")

            if self.allow_model_mismatch:
                self._log("⚠️  Continuing due to RAG_ALLOW_MODEL_MISMATCH/--allow-model-mismatch", "WARN")
                self._save_embedding_model()
                return

            if not sys.stdin.isatty():
                self._log("Non-interactive environment: aborting due to model incompatibility", "ERROR")
                sys.exit(1)
            
            # Ask user if they want to continue
            print(f"\n{'='*80}")
            print(f"⚠️  **MODEL INCOMPATIBILITY DETECTED**")
            print(f"{'='*80}")
            print(f"Model in database: {stored_model}")
            print(f"Current model:    {self.embedding_model}")
            print(f"\nUsing different models may cause incorrect search results!")
            print(f"\nDo you want to continue anyway? [y/N]: ", end="")
            
            try:
                response = input().strip().lower()
                if response not in ['s', 'sim', 'yes', 'y']:
                    log_event('ALERT', 'Operation cancelled by user')
                    print("❌ Operation cancelled by user")
                    sys.exit(1)
                else:
                    log_event('ALERT', 'User chose to continue with incompatible model')
                    self._log("User chose to continue with incompatible model", "WARN")
                    # Update model in database to avoid future alerts
                    self._save_embedding_model()
            except KeyboardInterrupt:
                log_event('ALERT', 'Operation cancelled by user')
                print("\n❌ Operation cancelled by user")
                sys.exit(1)
        else:
            self._log(f"✅ Compatible embedding model: {self.embedding_model}", "INFO")
    
    def _init_chroma(self):
        """Initialize ChromaDB for embeddings."""
        # Ensure ChromaDB is loaded
        load_chroma_library()
        
        try:
            # Use local persistence
            self.chroma_client = chromadb.PersistentClient(path=str(self.chroma_path))
            
            # Create or get collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="document_embeddings",
                metadata={"hnsw:space": "cosine"}
            )
            
            self._log("ChromaDB initialized", "INFO")
        except Exception as e:
            self._log(f"Error initializing ChromaDB: {e}", "ERROR")
            raise
    
    def _save_book_to_sqlite(self, book_id: str, file_path: Path, metadata: Dict[str, Any]):
        """Save book information to SQLite."""
        try:
            file_metadata = self._get_file_metadata(file_path)
            
            # Ensure path is absolute in database
            absolute_file_path = file_path.resolve()
            
            self.conn.execute('''
                INSERT OR REPLACE INTO books 
                (id, file_path, file_hash, file_size, processed_at, chunk_count, embedding_count, conversion_time, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                book_id,
                str(absolute_file_path),
                file_metadata['hash'],
                file_metadata['size'],
                datetime.now().isoformat(),
                metadata.get('chunk_count', 0),
                metadata.get('embedding_count', 0),
                metadata.get('conversion_time', 0),
                json.dumps(metadata)
            ))
            
            self.conn.commit()
            self._log(f"Book {book_id} saved to SQLite", "INFO")
        except Exception as e:
            self._log(f"Error saving book to SQLite: {e}", "ERROR")
    
    def _save_chunks_to_sqlite(self, book_id: str, chunks: List[Dict[str, Any]]):
        """Save chunks to SQLite with page and optional section metadata."""
        try:
            chunk_data = []
            for i, chunk_info in enumerate(chunks):
                chunk_id = f"{book_id}_chunk_{i}"
                
                chunk_data.append((
                    chunk_id,
                    book_id,
                    i,
                    chunk_info['text'],
                    chunk_info['page'],
                    chunk_info.get('section_title'),
                    datetime.now().isoformat()
                ))
            
            self.conn.executemany('''
                INSERT OR REPLACE INTO chunks 
                (id, book_id, chunk_index, content, page_number, section_title, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', chunk_data)
            
            self.conn.commit()
            self._log(f"{len(chunks)} chunks saved to SQLite", "INFO")
        except Exception as e:
            self._log(f"Error saving chunks to SQLite: {e}", "ERROR")
    
    def _save_embeddings_to_chroma(self, book_id: str, chunks: List[Dict[str, Any]], embeddings: List[Any]):
        """Save embeddings to ChromaDB with page and section metadata."""
        try:
            batch_size = 500
            total = len(chunks)
            
            for start in range(0, total, batch_size):
                end = min(start + batch_size, total)
                
                ids = [f"{book_id}_chunk_{i}" for i in range(start, end)]
                documents = [c['text'] for c in chunks[start:end]]
                metadatas = [
                    {
                        "book_id": book_id,
                        "chunk_index": i,
                        "page": chunks[i]['page'],
                        "section_title": chunks[i].get('section_title') or "",
                    }
                    for i in range(start, end)
                ]
                embeddings_list = [emb.tolist() for emb in embeddings[start:end]]
                
                self.collection.add(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas,
                    embeddings=embeddings_list
                )
            
            self._log(f"{total} embeddings saved to ChromaDB", "INFO")
        except Exception as e:
            self._log(f"Error saving embeddings to ChromaDB: {e}", "ERROR")
    
    def _search_chroma(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search embeddings in ChromaDB."""
        try:
            # Generate query embedding
            query_embedding = self.get_embedding(query)
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Process results
            search_results = []
            for i, (doc_ids, documents, metadatas, distances) in enumerate(zip(
                results['ids'], results['documents'], results['metadatas'], results['distances']
            )):
                for j in range(len(doc_ids)):
                    document = documents[j]
                    metadata = metadatas[j]
                    distance = distances[j]
                    similarity = 1 - distance  # Convert distance to similarity
                    
                    book_id = metadata['book_id']
                    page = metadata.get('page', 'N/A')
                    section_title = metadata.get('section_title') or None
                    
                    # Get book name from SQLite
                    book_name = self._get_book_name(book_id)
                    
                    # Extract relevant part
                    relevant_chunk = self._extract_relevant_chunk(document, query)
                    clean_phrase = self._clean_chunk_for_display(relevant_chunk)
                    
                    search_results.append({
                        'query': query,
                        'book': book_name,
                        'page': page,
                        'section_title': section_title,
                        'citation': self._format_result_citation(book_name, page, section_title),
                        'phrase': clean_phrase,
                        'relevant_chunk': relevant_chunk,
                        'full_chunk': document,
                        'similarity': float(similarity),
                        'book_id': book_id,
                        'chunk_index': metadata['chunk_index'],
                        'match_type': 'semantic'
                    })
            
            return search_results
        except Exception as e:
            self._log(f"Error searching in ChromaDB: {e}", "ERROR")
            return []
    
    def _get_book_name(self, book_id: str) -> str:
        """Get book name by ID."""
        try:
            cursor = self.conn.execute('SELECT file_path FROM books WHERE id = ?', (book_id,))
            result = cursor.fetchone()
            if result:
                return Path(result['file_path']).name
            return 'Unknown'
        except Exception:
            return 'Unknown'
    
    def _delete_book_from_databases(self, book_id: str):
        """Remove a book from databases."""
        try:
            # Get actual chunk IDs from SQLite
            cursor = self.conn.execute(
                'SELECT id FROM chunks WHERE book_id = ?', (book_id,)
            )
            chunk_ids = [row['id'] for row in cursor.fetchall()]
            
            # Remove from ChromaDB in batches when collection is initialized.
            if chunk_ids and hasattr(self, 'collection'):
                batch_size = 500
                for i in range(0, len(chunk_ids), batch_size):
                    batch = chunk_ids[i:i + batch_size]
                    try:
                        self.collection.delete(ids=batch)
                    except Exception as e:
                        self._log(f"Error removing batch from ChromaDB: {e}", "WARN")
                self._log(f"{len(chunk_ids)} embeddings of book {book_id} removed from ChromaDB", "INFO")
            
            # Remove from SQLite
            self.conn.execute('DELETE FROM chunks WHERE book_id = ?', (book_id,))
            self.conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
            self.conn.commit()
            
            self._log(f"Book {book_id} removed from SQLite", "INFO")
        except Exception as e:
            self._log(f"Error removing book from databases: {e}", "ERROR")
    
    def interactive_search(self):
        """Interactive search mode for documents."""
        print(f"\n🔍 **Interactive Search Mode**")
        print(f"📚 Searching in {len(self._get_indexed_books())} indexed books")
        print(f"💡 Tips: Use specific terms for better results")
        print(f"⚡ Type 'sair', 'exit' or 'quit' to exit")
        print(f"📋 Type 'list' to see all indexed books")
        print(f"🔍 Type 'help' for help")
        print(f"{'='*80}")
        
        while True:
            try:
                # Get user input
                query = input(f"\n🔎 **Enter your search**: ").strip()
                
                # Special commands
                if query.lower() in ['sair', 'exit', 'quit']:
                    print(f"\n👋 Exiting interactive mode. Goodbye!")
                    break
                
                if query.lower() == 'help':
                    self._show_interactive_help()
                    continue
                
                if query.lower() == 'list':
                    self.list_indexed_books()
                    continue
                
                if not query:
                    print(f"⚠️  Please enter a search term.")
                    continue
                
                # Perform search
                print(f"\n🔍 Searching for: '{query}'...")
                results = self.search_documents(query)
                
                if not results:
                    print(f"❌ No results found for '{query}'")
                    print(f"💡 Try using different or more generic terms.")
                    continue
                
                # Display results
                print(f"\n📊 {len(results)} results found:")
                print(f"{'='*80}")
                
                for i, result in enumerate(results, 1):
                    match_type = result.get('match_type', 'semantic')
                    match_icon = "📌" if match_type == 'text' else "🧠"
                    print(f"\n**Result {i}** (Similarity: {result['similarity']:.3f}) {match_icon} [{match_type}]")
                    print(f"📄 **Document:** {result['book']}")
                    print(f"📖 **Page:** {result['page']}")
                    if result.get('section_title'):
                        print(f"📚 **Section/Chapter:** {result['section_title']}")
                    if result.get('citation'):
                        print(f"🔖 **Citation:** {result['citation']}")
                    print(f"🎯 **Relevant Chunk:** {result['relevant_chunk']}")
                    
                    # Options for the result
                    print(f"\n🔧 **Options:**")
                    print(f"   [1-{len(results)}] View more details of result {i}")
                    if i == 1:
                        print(f"   [n] New search")
                        print(f"   [s] Exit")
                    
                    print("-" * 60)
                
                # Ask if they want to see details or do a new search
                while True:
                    action = input(f"\n🤔 **What do you want to do?** [n-new, s-exit, 1-{len(results)}-details]: ").strip().lower()
                    
                    if action in ['n', 'nova', 'new']:
                        break  # Return to new search
                    
                    if action in ['s', 'sair', 'exit', 'quit']:
                        print(f"\n👋 Exiting interactive mode. Goodbye!")
                        return
                    
                    # Check if it's a valid number
                    try:
                        result_num = int(action)
                        if 1 <= result_num <= len(results):
                            self._show_detailed_result(results[result_num - 1])
                            break
                        else:
                            print(f"⚠️  Invalid number. Enter between 1 and {len(results)}.")
                    except ValueError:
                        print(f"⚠️  Invalid option. Try again.")
                
            except KeyboardInterrupt:
                print(f"\n\n⚠️  Interruption detected! Exiting interactive mode.")
                break
            except Exception as e:
                print(f"\n❌ Error during search: {e}")
                print(f"💡 Try again or use 'sair' to exit.")
    
    def _show_interactive_help(self):
        """Display interactive mode help."""
        print(f"\n📖 **Interactive Mode Help**")
        print(f"{'='*60}")
        print(f"🔍 **Available Commands:**")
        print(f"   • **search term** - Search in indexed documents")
        print(f"   • **help** - Display this help")
        print(f"   • **list** - List all indexed books")
        print(f"   • **sair/exit/quit** - Exit interactive mode")
        print(f"\n💡 **Search Tips:**")
        print(f"   • Use specific terms: 'redes neurais convolucionais'")
        print(f"   • Use technical terms: 'backpropagation' instead of 'treinamento'")
        print(f"   • Combine concepts: 'transformer attention mechanism'")
        print(f"   • Vary terms if no results found")
        print(f"\n📊 **Results:**")
        print(f"   • Similarity ranges from 0.0 to 1.0 (higher = more relevant)")
        print(f"   • Can view details of each result")
        print(f"   • Current base: {len(self._get_indexed_books())} books")
        print(f"{'='*60}")
    
    def _show_detailed_result(self, result):
        """Display complete details of a result."""
        print(f"\n📋 **Complete Result Details**")
        print(f"{'='*80}")
        print(f"📄 **Document:** {result['book']}")
        print(f"📖 **Page:** {result['page']}")
        if result.get('section_title'):
            print(f"📚 **Section/Chapter:** {result['section_title']}")
        if result.get('citation'):
            print(f"🔖 **Citation:** {result['citation']}")
        print(f"🎯 **Similarity:** {result['similarity']:.3f}")
        print(f"🔍 **Original Query:** {result['query']}")
        print(f"\n📝 **Relevant Chunk:**")
        print(f"{result['relevant_chunk']}")
        print(f"\n📄 **Full Chunk:**")
        print(f"{result['full_chunk']}")
        print(f"{'='*80}")
        
        input(f"\n⏎  Press Enter to continue...")
    
    def _get_indexed_books(self):
        """Get list of indexed books from SQLite."""
        try:
            cursor = self.conn.execute('SELECT id, file_path FROM books')
            books = cursor.fetchall()
            return {book['id']: book['file_path'] for book in books}
        except Exception as e:
            self._log(f"Error getting indexed books: {e}", "ERROR")
            return {}
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate file hash for change verification."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _generate_id(self, length: int = 10) -> str:
        """Generate unique alphanumeric ID."""
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choices(chars, k=length))
    
    def _get_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Get complete file metadata for change verification."""
        try:
            stat = file_path.stat()
            return {
                'size': stat.st_size,
                'mtime': stat.st_mtime,
                'ctime': stat.st_ctime,
                'hash': self._get_file_hash(file_path)
            }
        except Exception as e:
            self._log(f"Error getting metadata from {file_path}: {e}", "ERROR")
            return {}
    
    def _is_book_unchanged(self, file_path: Path, book_id: str) -> bool:
        """Check if book has changed since last processing using SQLite."""
        try:
            cursor = self.conn.execute('''
                SELECT file_hash, file_size FROM books WHERE id = ?
            ''', (book_id,))
            
            result = cursor.fetchone()
            if not result:
                return False
            
            current_metadata = self._get_file_metadata(file_path)
            
            # Compare metadata
            return (current_metadata.get('size') == result['file_size'] and
                    current_metadata.get('hash') == result['file_hash'])
        except Exception as e:
            self._log(f"Error checking book changes: {e}", "ERROR")
            return False
    
    def list_indexed_books(self):
        """List all indexed books from SQLite."""
        try:
            cursor = self.conn.execute('''
                SELECT id, file_path, file_size, processed_at, chunk_count, embedding_count
                FROM books 
                ORDER BY processed_at DESC
            ''')
            
            books = cursor.fetchall()
            
            if not books:
                print("📚 No indexed books found.")
                return
            
            print(f"📚 {len(books)} indexed books:\n")
            print("| ID | Book | Size | Processed at | Chunks |")
            print("|----|-------|--------|--------------|--------|")
            
            for book in books:
                file_path = Path(book['file_path'])
                size_mb = book['file_size'] / (1024*1024)
                processed_date = book['processed_at']
                chunk_count = book['chunk_count']
                
                # Format date
                try:
                    dt = datetime.fromisoformat(processed_date)
                    processed_date = dt.strftime('%d/%m/%Y %H:%M')
                except:
                    pass
                
                print(f"| {book['id']} | {file_path.name} | {size_mb:.1f}MB | {processed_date} | {chunk_count} |")
            
            print(f"\n📁 Files in: {self.docs_dir}")
            print(f"💾 Database: {self.db_path}")
            print(f"🔍 Embeddings: {self.chroma_path}")
        except Exception as e:
            self._log(f"Error listing books: {e}", "ERROR")
            print(f"❌ Error listing books: {e}")
    
    def delete_book(self, book_id: str) -> bool:
        """Remove a book from databases and associated files."""
        try:
            # Check if book exists
            cursor = self.conn.execute('SELECT file_path FROM books WHERE id = ?', (book_id,))
            result = cursor.fetchone()
            
            if not result:
                print(f"❌ Book with ID '{book_id}' not found.")
                return False
            
            file_path = Path(result['file_path'])
            book_name = file_path.stem
            
            print(f"🗑️  Removing book: {file_path.name} (ID: {book_id})")
            
            # Remove Markdown file
            md_path = self.docs_dir / f"{book_name}.md"
            if md_path.exists():
                md_path.unlink()
                print(f"✅ Removed: {md_path}")
            
            # Remove from databases
            self._delete_book_from_databases(book_id)
            
            print(f"✅ Book '{book_id}' removed successfully!")
            return True
        except Exception as e:
            self._log(f"Error removing book: {e}", "ERROR")
            print(f"❌ Error removing book: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Return RAG base summary status."""
        books = self._get_indexed_books()
        chunk_count = 0
        try:
            cursor = self.conn.execute('SELECT COUNT(*) AS count FROM chunks')
            row = cursor.fetchone()
            chunk_count = row['count'] if row else 0
        except Exception:
            chunk_count = 0

        return {
            'data_dir': str(self.data_dir),
            'sqlite_db': str(self.db_path),
            'chroma_db': str(self.chroma_path),
            'converted_dir': str(self.docs_dir),
            'embedding_model': self.embedding_model,
            'indexed_books': len(books),
            'chunks': chunk_count,
            'chunk_size': self.chunk_size,
            'chunk_overlap': self.chunk_overlap,
            'similarity_threshold': self.similarity_threshold,
        }
    
    def search_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Hybrid search: exact text (SQLite) + semantic (ChromaDB)."""
        log_event('INFO', 'Searching for', query=query)
        
        # 1. Exact/partial text search in SQLite
        text_results = self._search_text(query, top_k)
        
        # 2. Semantic search in ChromaDB
        semantic_results = self._search_chroma(query, top_k)
        
        # 3. Combine results (exact text first, no duplicates)
        seen_chunk_ids = set()
        combined = []
        
        # Add text results first (similarity boost)
        for r in text_results:
            chunk_key = f"{r['book_id']}_{r['chunk_index']}"
            if chunk_key not in seen_chunk_ids:
                seen_chunk_ids.add(chunk_key)
                combined.append(r)
        
        # Add semantic results that are not duplicates
        for r in semantic_results:
            if r['similarity'] <= self.similarity_threshold:
                continue
            chunk_key = f"{r['book_id']}_{r['chunk_index']}"
            if chunk_key not in seen_chunk_ids:
                seen_chunk_ids.add(chunk_key)
                combined.append(r)
        
        # Sort by similarity (descending)
        combined.sort(key=lambda x: x['similarity'], reverse=True)
        
        return combined[:top_k]
    
    def _search_text(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Text search in SQLite (exact and partial match)."""
        try:
            # Search chunks containing query text
            cursor = self.conn.execute('''
                SELECT c.book_id, c.chunk_index, c.content, c.page_number, c.section_title, b.file_path
                FROM chunks c
                JOIN books b ON c.book_id = b.id
                WHERE c.content LIKE ?
                ORDER BY 
                    CASE WHEN c.content LIKE ? THEN 0 ELSE 1 END,
                    c.chunk_index
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', top_k))
            
            results = []
            for row in cursor.fetchall():
                file_path = Path(row['file_path'])
                relevant_chunk = self._extract_relevant_chunk(row['content'], query)
                clean_phrase = self._clean_chunk_for_display(relevant_chunk)
                section_title = row['section_title'] if 'section_title' in row.keys() else None
                
                results.append({
                    'query': query,
                    'book': file_path.name,
                    'page': row['page_number'] or 'N/A',
                    'section_title': section_title,
                    'citation': self._format_result_citation(
                        file_path.name,
                        row['page_number'] or 'N/A',
                        section_title,
                    ),
                    'phrase': clean_phrase,
                    'relevant_chunk': relevant_chunk,
                    'full_chunk': row['content'],
                    'similarity': 1.0,  # Exact match = maximum similarity
                    'book_id': row['book_id'],
                    'chunk_index': row['chunk_index'],
                    'match_type': 'text'
                })
            
            if results:
                self._log(f"Text search: {len(results)} results found", "INFO")
            
            return results
        except Exception as e:
            self._log(f"Error in text search: {e}", "ERROR")
            return []
    
    def _clean_chunk_for_display(self, chunk: str) -> str:
        """Clean chunk for table display."""
        # Remove page markers
        chunk = re.sub(r'## Page \d+', '', chunk)
        chunk = re.sub(r'### Section:\s*.+', '', chunk)
        chunk = re.sub(r'Page \d+', '', chunk)
        
        # Remove excessive line breaks
        chunk = ' '.join(chunk.split())
        
        # Keep full chunk for detailed display
        return chunk.strip()

    @staticmethod
    def _format_result_citation(book_name: str, page: Any, section_title: Optional[str] = None) -> str:
        location_parts = []
        if page and str(page) != 'N/A':
            location_parts.append(f"p. {page}")
        if section_title:
            location_parts.append(f"section/chapter: {section_title}")
        location = "; ".join(location_parts) if location_parts else "location not provided"
        return f"{book_name} ({location})"
    
    def _extract_relevant_chunk(self, chunk: str, query: str) -> str:
        """Extract the most relevant part of the chunk in relation to the query."""
        # 1. Try exact match of query in chunk (context window around)
        chunk_lower = chunk.lower()
        query_lower = query.lower()
        pos = chunk_lower.find(query_lower)
        if pos != -1:
            # Expand to include context around (150 chars each side)
            context = 150
            start = max(0, pos - context)
            end = min(len(chunk), pos + len(query) + context)
            excerpt = chunk[start:end].strip()
            if start > 0:
                excerpt = '...' + excerpt
            if end < len(chunk):
                excerpt = excerpt + '...'
            return excerpt
        
        # 2. Split chunk into sentences and search for greater term overlap
        sentences = re.split(r'[.!?]+', chunk)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return chunk.strip()
        
        # Filter short stop words to avoid false positives
        query_terms = [t for t in query_lower.split() if len(t) > 3]
        if not query_terms:
            query_terms = query_lower.split()
        
        # Score sentences by the amount of query terms present
        scored = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            score = sum(1 for term in query_terms if term in sentence_lower)
            if score > 0:
                scored.append((score, sentence))
        
        if scored:
            scored.sort(key=lambda x: x[0], reverse=True)
            # Return sentences with highest score
            best = [s for _, s in scored[:3]]
            return ' '.join(best)
        
        # 3. Fallback: return start of chunk
        return chunk[:300] + '...' if len(chunk) > 300 else chunk
    
    def convert_all_in_directory(self, directory: Path):
        """Convert all supported documents in a directory."""
        supported_extensions = {'.pdf', '.epub', '.djvu'}
        
        # Find all supported files
        all_files = []
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                all_files.append(file_path)
        
        if not all_files:
            self._log(f"No supported documents found in {directory}", "WARN")
            return
        
        total_files = len(all_files)
        self._log(f"Found {total_files} documents to process", "INFO")
        
        processed = 0
        skipped = 0
        failed = 0
        
        start_time = time.time()
        
        for i, file_path in enumerate(all_files):
            if self.interrupted:
                self._log("Batch processing interrupted", "WARN")
                break
            
            self._show_progress(i, total_files, "Processing files", f"{file_path.name}")
            
            # Check if already processed via SQLite
            cursor = self.conn.execute('SELECT id FROM books WHERE file_path = ?', (str(file_path),))
            existing = cursor.fetchone()
            existing_book_id = existing['id'] if existing else None
            
            if existing_book_id and self._is_book_unchanged(file_path, existing_book_id):
                skipped += 1
                continue
            
            try:
                result = self.process_document(file_path)
                if result:
                    processed += 1
                else:
                    failed += 1
            except Exception as e:
                self._log(f"Error processing {file_path.name}: {e}", "ERROR")
                failed += 1
        
        self._show_progress(total_files, total_files, "Processing files", "completed")
        
        total_time = time.time() - start_time
        self._log(f"Processing completed!", "SUCCESS")
        self._log(f"✅ Processed: {processed}", "INFO")
        self._log(f"⏭️  Skipped: {skipped}", "INFO")
        self._log(f"❌ Failed: {failed}", "INFO")
        self._log(f"⏱️  Total time: {self._format_time(total_time)}", "INFO")


def main():
    parser = argparse.ArgumentParser(description='Document Converter with Semantic Search')
    parser.add_argument('target', nargs='?', help='File or directory to convert')
    parser.add_argument('--convert', type=str, help='Convert specific file')
    parser.add_argument('--convert-all', type=str, help='Convert all documents in directory')
    parser.add_argument('--calibre-id', type=int, help='Convert and index a book by Calibre ID')
    parser.add_argument('--format', help='Format to use with --calibre-id. If omitted, the best available format is selected')
    parser.add_argument('--calibre-metadata-db', default=os.getenv('CALIBRE_METADATA_DB') or DEFAULT_CALIBRE_METADATA_DB, help='Path to Calibre metadata.db for local fallback')
    parser.add_argument('--search', type=str, help='Search in processed documents')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive search mode')
    parser.add_argument('--list', action='store_true', help='List all indexed books')
    parser.add_argument('--status', action='store_true', help='Show RAG base status')
    parser.add_argument('--check', action='store_true', help='Check dependencies without initializing RAG base')
    parser.add_argument('--delete', type=str, help='Remove a book by ID')
    parser.add_argument('--data-dir', type=str, help=f'Data directory (default: DATA_DIR or {DEFAULT_DATA_DIR})')
    parser.add_argument('--converted-dir', type=str, help=f'Folder for converted files (default: CONVERTED_DIR or {DEFAULT_CONVERTED_DIR})')
    parser.add_argument('--lang', type=str, default='por', help='OCR language (default: por)')
    parser.add_argument('--chunk-size', type=int, help='Chunk size (default: 500)')
    parser.add_argument('--chunk-overlap', type=int, help='Overlap between chunks (default: 50)')
    parser.add_argument('--embedding-model', type=str, help='Embedding model (default: OLLAMA_MODEL or nomic-embed-text-v2-moe)')
    parser.add_argument('--allow-model-mismatch', action='store_true', help='Allow continuing when current model differs from model stored in base')
    parser.add_argument('--allow-model-pull', action='store_true', help='Allow this script to run ollama pull when the embedding model is missing')
    parser.add_argument('--json', action='store_true', help='Output JSON for automation-friendly commands')
    
    args = parser.parse_args()
    
    # If no argument provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return

    if args.check:
        check = runtime_check()
        if args.json:
            print(json.dumps(check, ensure_ascii=False, indent=2))
        else:
            print("Python Dependencies:")
            for name, ok in check["modules"].items():
                print(f"  {'OK' if ok else 'MISSING'} {name}")
            print("Binaries:")
            for name, path in check["binaries"].items():
                print(f"  {'OK' if path else 'MISSING'} {name}: {path or '-'}")
            print(f"metadata.db: {'OK' if check['calibre_metadata_db_exists'] else 'MISSING'} {check['calibre_metadata_db']}")
        return
    
    # Determine command type to optimize loading
    target_for_conversion = args.target and not args.target.startswith('-')
    command_type = "basic"
    if args.search or args.interactive:
        command_type = "search"
    elif args.convert or args.convert_all or args.calibre_id or target_for_conversion:
        command_type = "convert"
    elif args.delete:
        command_type = "delete"
    
    kwargs = {
        'data_dir': args.data_dir,
        'converted_dir': args.converted_dir,
        'tesseract_lang': args.lang,
        'command_type': command_type,
        'allow_model_mismatch': args.allow_model_mismatch,
        'allow_model_pull': args.allow_model_pull,
    }
    if args.chunk_size is not None:
        kwargs['chunk_size'] = args.chunk_size
    if args.chunk_overlap is not None:
        kwargs['chunk_overlap'] = args.chunk_overlap
    if args.embedding_model is not None:
        kwargs['embedding_model'] = args.embedding_model
    
    if args.json:
        with contextlib.redirect_stdout(sys.stderr):
            converter = DocumentConverter(**kwargs)
    else:
        converter = DocumentConverter(**kwargs)
    
    # Processar argumentos
    if args.list:
        if args.json:
            books = []
            cursor = converter.conn.execute('''
                SELECT id, file_path, file_size, processed_at, chunk_count, embedding_count
                FROM books
                ORDER BY processed_at DESC
            ''')
            for row in cursor.fetchall():
                books.append(dict(row))
            print(json.dumps(books, ensure_ascii=False, indent=2))
        else:
            converter.list_indexed_books()
        return

    if args.status:
        status = converter.get_status()
        if args.json:
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            for key, value in status.items():
                print(f"{key}: {value}")
        return
    
    if args.delete:
        if args.json:
            with contextlib.redirect_stdout(sys.stderr):
                ok = converter.delete_book(args.delete)
            print(json.dumps({"deleted": ok, "book_id": args.delete}, ensure_ascii=False, indent=2))
        else:
            converter.delete_book(args.delete)
        return
    
    if args.interactive:
        converter.interactive_search()
        return
    
    if args.search:
        if args.json:
            with contextlib.redirect_stdout(sys.stderr):
                results = converter.search_documents(args.search)
        else:
            results = converter.search_documents(args.search)
        
        if not results:
            if args.json:
                print("[]")
            else:
                print("❌ No results found")
            return

        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return
        
        log_event('DATA', 'Results found', count=len(results), query=args.search)
        
        print(f"📈 **Result Details:**")
        for i, result in enumerate(results, 1):
            match_type = result.get('match_type', 'semantic')
            match_icon = "📌" if match_type == 'text' else "🧠"
            print(f"\n**Result {i}** (Similarity: {result['similarity']:.3f}) {match_icon} [{match_type}]")
            print(f"📄 **Document:** {result['book']}")
            print(f"📖 **Page:** {result['page']}")
            if result.get('section_title'):
                print(f"📚 **Section/Chapter:** {result['section_title']}")
            if result.get('citation'):
                print(f"🔖 **Citation:** {result['citation']}")
            print(f"🎯 **Relevant Chunk:** {result['relevant_chunk']}")
            print("-" * 80)
        
        total_time = time.time() - converter.start_time
        log_event('INFO', 'Total execution time', time=converter._format_time(total_time))
        log_event('INFO', 'Log saved to', log_file=str(converter.log_file))
        return
    
    if args.calibre_id:
        try:
            file_path = resolve_calibre_document(args.calibre_id, args.format, args.calibre_metadata_db)
        except Exception as e:
            log_event('ERROR', 'Error locating book in Calibre', error=str(e))
            return
        if args.json:
            with contextlib.redirect_stdout(sys.stderr):
                result = converter.process_document(file_path)
        else:
            result = converter.process_document(file_path)
        if args.json:
            print(json.dumps({"source": str(file_path), "result": result}, ensure_ascii=False, indent=2))
        return

    if args.convert:
        file_path = Path(args.convert)
        if not file_path.exists():
            log_event('ERROR', 'File not found', file=str(file_path))
            return
        if args.json:
            with contextlib.redirect_stdout(sys.stderr):
                result = converter.process_document(file_path)
        else:
            result = converter.process_document(file_path)
        if args.json:
            print(json.dumps({"source": str(file_path), "result": result}, ensure_ascii=False, indent=2))
        return
    
    if args.convert_all:
        directory = Path(args.convert_all)
        if not directory.exists():
            log_event('ERROR', 'Directory not found', dir=str(directory))
            return
        converter.convert_all_in_directory(directory)
        return
    
    if args.target:
        target = Path(args.target)
        
        if not target.exists():
            log_event('ERROR', 'File or directory not found', target=str(target))
            return
        
        if target.is_file():
            if not args.json:
                log_event('INFO', 'Converting file', file=str(target))
            if args.json:
                with contextlib.redirect_stdout(sys.stderr):
                    result = converter.process_document(target)
            else:
                result = converter.process_document(target)
            if args.json:
                print(json.dumps({"source": str(target), "result": result}, ensure_ascii=False, indent=2))
        elif target.is_dir():
            log_event('START', 'Converting all documents in folder', dir=str(target))
            converter.convert_all_in_directory(target)
        return
    


if __name__ == "__main__":
    main()
