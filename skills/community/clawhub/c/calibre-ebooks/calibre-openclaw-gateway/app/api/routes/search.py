from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models import SearchRequest, ContentSearchRequest, SearchResult, BookResponse, SemanticSearchResponse
from app.services.book_service import book_service
from app.services.embedding_service import embedding_service
from app.services.openlibrary_service import openlibrary_service
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("")
async def search_books(
    query: str,
    limit: int = Query(default=50, ge=1, le=100),
    semantic_fallback: bool = Query(
        default=True,
        description="When catalog search returns no results, search embedded content.",
    ),
    semantic_threshold: float = Query(default=0.3, ge=0.0, le=1.0),
    include_totals: bool = Query(
        default=False,
        description="Include total chunks and pages counts in semantic search results.",
    ),
    chunks_before: int = Query(default=0, ge=0, le=10, description="Number of chunks before each result to include"),
    chunks_after: int = Query(default=0, ge=0, le=10, description="Number of chunks after each result to include"),
    pages_before: int = Query(default=0, ge=0, le=10, description="Number of pages before each result to include"),
    pages_after: int = Query(default=0, ge=0, le=10, description="Number of pages after each result to include"),
    openlibrary_search: bool = Query(
        default=True,
        description="Include OpenLibrary search results in catalog search.",
    ),
):
    """Search catalog first, then embedded content when the catalog has no hit.
    
    When include_totals=True and semantic search is used, returns metadata with total chunks and pages above threshold.
    Context expansion parameters (chunks_before/after, pages_before/after) add surrounding context to each result.
    When openlibrary_search=True, includes results from OpenLibrary API.
    """
    try:
        if not query or len(query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        books = book_service.search_books(query, limit)
        results = []
        
        if books:
            results.extend([
                {
                    "result_type": "catalog",
                    **BookResponse(**book).model_dump(mode="json"),
                }
                for book in books
            ])
        
        # Add OpenLibrary search results if enabled
        if openlibrary_search and openlibrary_service.enabled:
            try:
                ol_results = openlibrary_service.search_by_title_author(query, query, limit=limit)
                if ol_results and isinstance(ol_results, list):
                    for work in ol_results[:limit]:
                        # Convert OpenLibrary work to book-like structure
                        ol_book = {
                            "id": None,  # OpenLibrary results don't have local IDs
                            "calibre_id": None,
                            "title": work.get('title'),
                            "author": ', '.join(work.get('authors', [])) if work.get('authors') else None,
                            "file_path": None,
                            "file_size": None,
                            "file_type": None,
                            "metadata": None,
                            "indexed_at": None,
                            "updated_at": None,
                            "publisher": ', '.join(work.get('publisher', [])) if work.get('publisher') else None,
                            "year": work.get('first_publish_year'),
                            "isbn": ', '.join(work.get('isbn', [])) if work.get('isbn') else None,
                            "page_count": None,
                            "rag_processed": False,
                            "rag_in_queue": False,
                            "rag_status": None,
                            "rag_error": None,
                            "openlibrary": {
                                "olid": work.get('olid'),
                                "title": work.get('title'),
                                "authors": work.get('authors', []),
                                "first_publish_year": work.get('first_publish_year'),
                                "cover_url": work.get('cover_url'),
                                "url": f"https://openlibrary.org/books/{work.get('olid')}" if work.get('olid') else None,
                            },
                            "openlibrary_cover_url": work.get('cover_url'),
                            "openlibrary_preview_url": f"https://openlibrary.org/books/{work.get('olid')}" if work.get('olid') else None,
                            "openlibrary_download_available": bool(work.get('ocaid')),
                            "openlibrary_olid": work.get('olid'),
                        }
                        results.append({
                            "result_type": "openlibrary",
                            **ol_book,
                        })
                        logger.info(
                            f"Added OpenLibrary result: {work.get('title')}",
                            extra={"operation": "openlibrary_search", "olid": work.get('olid')}
                        )
            except Exception as e:
                logger.warning(f"OpenLibrary search failed for query '{query}': {e}")
        
        # Return catalog results if we have any
        if results:
            return results[:limit]

        if not semantic_fallback:
            return []

        semantic_response = embedding_service.search_similar_content(
            query=query,
            limit=min(limit, 50),
            threshold=semantic_threshold,
            include_totals=include_totals,
            chunks_before=chunks_before,
            chunks_after=chunks_after,
            pages_before=pages_before,
            pages_after=pages_after,
        )
        
        # Handle backward compatible return (list when include_totals=False, dict when True)
        if include_totals:
            semantic_results = semantic_response.get('results', [])
            return {
                "results": [
                    {
                        "result_type": "semantic",
                        **SearchResult(**result).model_dump(mode="json"),
                    }
                    for result in semantic_results
                ],
                "total_chunks": semantic_response.get('total_chunks'),
                "total_pages": semantic_response.get('total_pages'),
            }
        
        # Backward compatible: semantic_response is a list when include_totals=False
        return [
            {
                "result_type": "semantic",
                **SearchResult(**result).model_dump(mode="json"),
            }
            for result in semantic_response
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching books with query '{query}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/content")
async def search_content(request: ContentSearchRequest):
    """Search for similar content using semantic search (requires embeddings).
    
    When include_totals=True, returns metadata with total chunks and pages above threshold.
    """
    try:
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        response = embedding_service.search_similar_content(
            query=request.query,
            limit=request.limit,
            threshold=request.threshold,
            include_totals=request.include_totals,
            chunks_before=request.chunks_before,
            chunks_after=request.chunks_after,
            pages_before=request.pages_before,
            pages_after=request.pages_after,
        )
        
        # Handle backward compatible return (list when include_totals=False, dict when True)
        if request.include_totals:
            results = response.get('results', [])
            return SemanticSearchResponse(
                results=[SearchResult(**result) for result in results],
                total_chunks=response.get('total_chunks'),
                total_pages=response.get('total_pages')
            )
        
        # Backward compatible: response is a list when include_totals=False
        return [SearchResult(**result) for result in response]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in content search with query '{request.query}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/openlibrary")
async def search_openlibrary(
    query: str,
    limit: int = Query(default=20, ge=1, le=100),
    author: Optional[str] = Query(default=None, description="Optional author name to narrow search"),
):
    """Search OpenLibrary API directly for books.
    
    This endpoint searches only OpenLibrary and returns results with metadata
    including OLID, cover URLs, and links to OpenLibrary pages.
    """
    try:
        if not query or len(query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if not openlibrary_service.enabled:
            raise HTTPException(
                status_code=503,
                detail="OpenLibrary service is not enabled. Set OPENLIBRARY_ENABLED=true in .env"
            )
        
        logger.info(f"Searching OpenLibrary with query: {query}, author: {author}, limit: {limit}")
        
        results = openlibrary_service.search_by_title_author(query, author, limit=limit)
        
        if not results:
            return []
        
        # Convert to response format
        formatted_results = []
        for work in results:
            try:
                formatted_result = {
                    "result_type": "openlibrary",
                    "id": None,
                    "calibre_id": None,
                    "title": work.get('title'),
                    "author": ', '.join(work.get('authors', [])) if work.get('authors') else None,
                    "file_path": None,
                    "file_size": None,
                    "file_type": None,
                    "metadata": None,
                    "indexed_at": None,
                    "updated_at": None,
                    "publisher": ', '.join(work.get('publisher', [])) if work.get('publisher') else None,
                    "year": work.get('first_publish_year'),
                    "isbn": ', '.join(work.get('isbn', [])) if work.get('isbn') else None,
                    "page_count": None,
                    "rag_processed": False,
                    "rag_in_queue": False,
                    "rag_status": None,
                    "rag_error": None,
                    "openlibrary": {
                        "olid": work.get('olid'),
                        "title": work.get('title'),
                        "authors": work.get('authors', []),
                        "first_publish_year": work.get('first_publish_year'),
                        "cover_url": work.get('cover_url'),
                        "url": f"https://openlibrary.org/books/{work.get('olid')}" if work.get('olid') else None,
                    },
                    "openlibrary_cover_url": work.get('cover_url'),
                    "openlibrary_preview_url": f"https://openlibrary.org/books/{work.get('olid')}" if work.get('olid') else None,
                    "openlibrary_download_available": bool(work.get('ocaid')),
                    "openlibrary_olid": work.get('olid'),
                }
                formatted_results.append(formatted_result)
            except Exception as e:
                logger.error(f"Error formatting OpenLibrary result: {e}, work data: {work}")
                continue
        
        return formatted_results
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching OpenLibrary with query '{query}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
