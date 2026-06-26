from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class BookResponse(BaseModel):
    """Response model for book data."""
    id: int
    calibre_id: Optional[int] = None
    title: str
    author: Optional[str] = None
    file_path: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    selected_format: Optional[str] = None
    available_formats: List[str] = Field(default_factory=list)
    indexed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Additional metadata fields (from Calibre)
    publisher: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    page_count: Optional[int] = None
    # RAG processing status
    rag_processed: bool = False
    rag_in_queue: bool = False
    rag_status: Optional[str] = None
    rag_error: Optional[str] = None
    # OpenLibrary enrichment fields (optional, for enhanced display)
    openlibrary: Optional[Dict[str, Any]] = None
    openlibrary_cover_url: Optional[str] = None
    openlibrary_preview_url: Optional[str] = None
    openlibrary_download_available: bool = False
    openlibrary_olid: Optional[str] = None
    
    class Config:
        from_attributes = True


class BookListResponse(BaseModel):
    """Response model for book list."""
    books: List[BookResponse]
    total: int
    limit: int
    offset: int


class SearchRequest(BaseModel):
    """Request model for search."""
    query: str = Field(..., min_length=1, description="Search query")
    limit: int = Field(default=50, ge=1, le=100, description="Maximum results")


class ContentSearchRequest(BaseModel):
    """Request model for content search."""
    query: str = Field(..., min_length=1, description="Search query for content")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum results")
    threshold: float = Field(default=0.3, ge=0.0, le=1.0, description="Similarity threshold")
    include_totals: bool = Field(default=False, description="Include total chunks and pages counts")
    chunks_before: int = Field(default=0, ge=0, le=10, description="Number of chunks before each result to include")
    chunks_after: int = Field(default=0, ge=0, le=10, description="Number of chunks after each result to include")
    pages_before: int = Field(default=0, ge=0, le=10, description="Number of pages before each result to include")
    pages_after: int = Field(default=0, ge=0, le=10, description="Number of pages after each result to include")


class SearchResult(BaseModel):
    """Response model for search result."""
    id: int
    chunk_id: int
    book_id: int
    chunk_index: int
    content: str
    title: str
    author: Optional[str] = None
    similarity: float
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    section_title: Optional[str] = None
    citation: Optional[str] = None
    # Book indexing timestamps
    indexed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    selected_format: Optional[str] = None
    available_formats: List[str] = Field(default_factory=list)
    # Additional book metadata (from Calibre)
    publisher: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    page_count: Optional[int] = None
    # RAG processing status
    rag_processed: bool = False
    rag_in_queue: bool = False
    rag_status: Optional[str] = None
    rag_error: Optional[str] = None
    # OpenLibrary enrichment fields (optional, for enhanced display)
    openlibrary: Optional[Dict[str, Any]] = None
    openlibrary_cover_url: Optional[str] = None
    openlibrary_preview_url: Optional[str] = None
    openlibrary_download_available: bool = False
    openlibrary_olid: Optional[str] = None
    
    class Config:
        from_attributes = True


class EmbeddingStatusResponse(BaseModel):
    """Response model for embedding status."""
    book_id: int
    has_embeddings: bool
    chunk_count: int
    ready: bool
    error: Optional[str] = None


class EmbeddingQueueResponse(BaseModel):
    """Response model for embedding queue."""
    book_id: int
    status: str
    queue_id: Optional[int] = None
    queue_status: Optional[str] = None


class QueueItemResponse(BaseModel):
    """Response model for queue item."""
    id: int
    book_id: int
    title: str
    status: str
    priority: int
    estimated_seconds: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class EmbeddingModelInfoResponse(BaseModel):
    """Response model for the active embedding model / version info."""
    model: str
    dimension: Optional[int] = None
    chunk_size: int
    chunk_overlap: int
    embedding_version: int
    citation_schema_version: Optional[int] = None
    current_signature: Optional[str] = None
    stored_signature: Optional[str] = None
    stored_model: Optional[str] = None
    stored_dimension: Optional[str] = None
    up_to_date: Optional[bool] = None
    error: Optional[str] = None


class EmbeddingReindexResponse(BaseModel):
    """Response model for a forced embedding reconciliation/reindex."""
    changed: bool
    invalidated: Optional[int] = None
    baseline: Optional[bool] = None
    signature: Optional[str] = None
    old_signature: Optional[str] = None
    new_signature: Optional[str] = None
    reason: Optional[str] = None
    error: Optional[str] = None


class SyncResponse(BaseModel):
    """Response model for sync operation."""
    synced_count: int
    message: str


class BookFormatConversionRequest(BaseModel):
    """Request model for converting and registering a Calibre book format."""
    book_id: Optional[int] = Field(default=None, description="Internal OpenClaw/PostgreSQL book ID")
    calibre_id: Optional[int] = Field(default=None, description="Native Calibre book ID")
    title: Optional[str] = Field(default=None, description="Exact book title when it uniquely identifies one book")
    target_format: str = Field(..., min_length=1, description="Requested output format")
    source_format: Optional[str] = Field(default=None, description="Optional preferred source format")
    force: bool = Field(default=False, description="Replace/recreate the target format if it already exists")


class BookFormatConversionResponse(BaseModel):
    """Response model for a format conversion and registration operation."""
    success: bool
    message: str
    book_id: Optional[int] = None
    calibre_id: int
    title: str
    source_format: Optional[str] = None
    target_format: str
    output_path: Optional[str] = None
    already_available: bool = False
    registered: bool = False
    synced_count: int = 0


class BookFormatInfoResponse(BaseModel):
    """Details about one format available for a Calibre book."""
    format: str
    filename: str
    media_type: str
    size: Optional[int] = None
    exists: bool = False
    selected: bool = False


class BookFormatsResponse(BaseModel):
    """Response model for formats available for a book."""
    book_id: int
    calibre_id: Optional[int] = None
    title: str
    selected_format: Optional[str] = None
    available_formats: List[str] = Field(default_factory=list)
    formats: List[BookFormatInfoResponse] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str
    detail: Optional[str] = None


class SemanticSearchResponse(BaseModel):
    """Response model for semantic search with optional totals metadata."""
    results: List[SearchResult]
    total_chunks: Optional[int] = None
    total_pages: Optional[int] = None


class DownloadQueueItem(BaseModel):
    """Model for download queue item."""
    id: int
    title: str
    author: Optional[str] = None
    source: str
    source_id: Optional[str] = None
    olid: Optional[str] = None
    ocaid: Optional[str] = None
    download_url: Optional[str] = None
    preferred_format: str = "PDF"
    status: str = "pending"
    priority: int = 0
    error_message: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    file_hash: Optional[str] = None
    download_available: bool = True
    calibre_book_id: Optional[int] = None
    added_to_calibre_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class DownloadQueueRequest(BaseModel):
    """Request model for adding item to download queue."""
    title: str = Field(..., min_length=1, description="Book title")
    author: Optional[str] = Field(default=None, description="Book author")
    source: str = Field(..., description="Source: 'openlibrary' or 'archive'")
    source_id: Optional[str] = Field(default=None, description="Source-specific ID")
    olid: Optional[str] = Field(default=None, description="OpenLibrary ID")
    ocaid: Optional[str] = Field(default=None, description="Archive.org ID")
    download_url: Optional[str] = Field(default=None, description="Direct download URL")
    preferred_format: str = Field(default="PDF", description="Preferred format: PDF, EPUB, Kindle")
    priority: int = Field(default=0, ge=0, le=100, description="Download priority (higher = first)")


class DownloadQueueResponse(BaseModel):
    """Response model for download queue operations."""
    id: int
    message: str
