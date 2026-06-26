"""OpenLibrary service for enriching book metadata."""

from typing import Optional, Dict, Any, List
from collections import namedtuple

from olclient.openlibrary import OpenLibrary
from olclient.config import Config

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OpenLibraryService:
    """Service for interacting with OpenLibrary API to enrich book metadata."""
    
    def __init__(self):
        """Initialize OpenLibrary client with credentials from settings."""
        self.enabled = settings.OPENLIBRARY_ENABLED
        self.client = None
        
        if self.enabled:
            try:
                # Try to initialize with credentials if available
                credentials = None
                if settings.OPENLIBRARY_ACCESS_KEY and settings.OPENLIBRARY_SECRET_KEY:
                    try:
                        from olclient.config import Credentials
                        credentials = Credentials(
                            access=settings.OPENLIBRARY_ACCESS_KEY.get_secret_value(),
                            secret=settings.OPENLIBRARY_SECRET_KEY.get_secret_value()
                        )
                    except Exception as e:
                        logger.warning(f"Could not configure OpenLibrary credentials: {e}")
                
                # Initialize client (with or without credentials)
                # If credentials fail, try without them for read-only access
                try:
                    self.client = OpenLibrary(
                        credentials=credentials,
                        base_url=settings.OPENLIBRARY_BASE_URL
                    )
                except Exception as auth_error:
                    logger.warning(f"OpenLibrary client initialization with credentials failed: {auth_error}")
                    # Try without credentials for read-only access
                    self.client = OpenLibrary(base_url=settings.OPENLIBRARY_BASE_URL)
                
                logger.info(
                    "OpenLibrary client initialized",
                    extra={"operation": "openlibrary_init", "base_url": settings.OPENLIBRARY_BASE_URL, "authenticated": credentials is not None}
                )
            except Exception as e:
                logger.error(f"Failed to initialize OpenLibrary client: {e}")
                # Don't disable the service - it may still work for read-only operations
                # Just log the error and continue with None client
                self.client = None
    
    def search_by_isbn(self, isbn: str) -> Optional[Dict[str, Any]]:
        """Search for a book by ISBN.
        
        Args:
            isbn: ISBN number (10 or 13 digits)
            
        Returns:
            Dictionary with book metadata or None if not found
        """
        if not self.enabled or not self.client:
            logger.warning("OpenLibrary service not enabled or client not initialized")
            return None
        
        try:
            logger.info(f"Searching OpenLibrary by ISBN: {isbn}", extra={"operation": "ol_search_isbn", "isbn": isbn})
            
            # Get metadata from OpenLibrary
            metadata = self.client.Edition.get_metadata('ISBN', isbn)
            
            if not metadata:
                logger.info(f"No book found in OpenLibrary for ISBN: {isbn}")
                return None
            
            # Extract and normalize metadata
            enriched_data = self._extract_metadata(metadata, isbn)
            
            logger.info(
                f"Found book in OpenLibrary for ISBN {isbn}",
                extra={"operation": "ol_found", "isbn": isbn, "title": enriched_data.get('title')}
            )
            
            return enriched_data
            
        except Exception as e:
            logger.error(f"Error searching OpenLibrary by ISBN {isbn}: {e}")
            return None
    
    def search_by_title_author(self, title: str, author: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for books by title and optionally author.
        
        Args:
            title: Book title
            author: Optional author name
            limit: Maximum number of results to return (default: 10)
            
        Returns:
            List of dictionaries with book metadata
        """
        if not self.enabled or not self.client:
            logger.warning("OpenLibrary service not enabled or client not initialized")
            return []
        
        try:
            logger.info(
                f"Searching OpenLibrary by title: {title}, author: {author}, limit: {limit}",
                extra={"operation": "ol_search_title", "title": title, "author": author, "limit": limit}
            )
            
            # Use OpenLibrary search API
            search_url = f"{self.client.base_url}/search.json"
            params = {'title': title, 'limit': str(limit)}
            if author:
                params['author'] = author
            
            response = self.client.session.get(search_url, params=params)
            response.raise_for_status()
            
            results = response.json()
            books = results.get('docs', [])
            
            enriched_books = []
            for book in books[:limit]:  # Limit to requested number of results
                enriched = self._extract_search_result(book)
                if enriched:
                    enriched_books.append(enriched)
            
            logger.info(
                f"Found {len(enriched_books)} books in OpenLibrary for title: {title}",
                extra={"operation": "ol_search_results", "count": len(enriched_books)}
            )
            
            return enriched_books
            
        except Exception as e:
            logger.error(f"Error searching OpenLibrary by title {title}: {e}")
            return []
    
    def get_download_links(self, isbn: Optional[str] = None, olid: Optional[str] = None) -> Dict[str, Any]:
        """Get download links for a book from OpenLibrary.
        
        Args:
            isbn: Optional ISBN to identify the book
            olid: Optional OpenLibrary ID to identify the book
            
        Returns:
            Dictionary with download information including URLs and formats
        """
        if not self.enabled or not self.client:
            logger.warning("OpenLibrary service not enabled or client not initialized")
            return {}
        
        try:
            # Get edition OLID if not provided
            if not olid and isbn:
                olid = self.client.Edition.get_olid_by_isbn(isbn)
                if not olid:
                    logger.info(f"No OpenLibrary ID found for ISBN: {isbn}")
                    return {}
            
            if not olid:
                logger.warning("Either ISBN or OLID must be provided")
                return {}
            
            logger.info(
                f"Getting download links for OLID: {olid}",
                extra={"operation": "ol_download", "olid": olid}
            )
            
            # Get edition details
            edition = self.client.Edition.get(olid=olid)
            if not edition:
                logger.info(f"Edition not found for OLID: {olid}")
                return {}
            
            # Extract download information
            download_info = {
                'olid': olid,
                'title': edition.title,
                'preview_url': None,
                'read_url': None,
                'download_formats': [],
                'public_domain': False
            }
            
            # Check if the book has a preview
            if hasattr(edition, 'ocaid') and edition.ocaid:
                # Archive.org book - has download options
                download_info['preview_url'] = f"https://openlibrary.org/books/{olid}"
                download_info['read_url'] = f"https://openlibrary.org/books/{olid}"
                download_info['public_domain'] = True
                
                # Common download formats from Archive.org
                base_archive_url = f"https://archive.org/download/{edition.ocaid}"
                download_info['download_formats'] = [
                    {
                        'format': 'PDF',
                        'url': f"{base_archive_url}/{edition.ocaid}_text.pdf",
                        'description': 'PDF format'
                    },
                    {
                        'format': 'EPUB',
                        'url': f"{base_archive_url}/{edition.ocaid}.epub",
                        'description': 'EPUB format'
                    },
                    {
                        'format': 'Kindle',
                        'url': f"{base_archive_url}/{edition.ocaid}_mobi.mobi",
                        'description': 'Kindle format'
                    },
                    {
                        'format': 'Daisy',
                        'url': f"{base_archive_url}/{edition.ocaid}_daisy.zip",
                        'description': 'Daisy format for accessibility'
                    }
                ]
            
            logger.info(
                f"Retrieved download info for OLID {olid}: {len(download_info['download_formats'])} formats",
                extra={"operation": "ol_download_success", "olid": olid, "formats": len(download_info['download_formats'])}
            )
            
            return download_info
            
        except Exception as e:
            logger.error(f"Error getting download links for OLID {olid}: {e}")
            return {}
    
    def get_author_info(self, author_name: str) -> Optional[Dict[str, Any]]:
        """Get author information from OpenLibrary.
        
        Args:
            author_name: Name of the author
            
        Returns:
            Dictionary with author information or None if not found
        """
        if not self.enabled or not self.client:
            logger.warning("OpenLibrary service not enabled or client not initialized")
            return None
        
        try:
            logger.info(
                f"Searching OpenLibrary for author: {author_name}",
                extra={"operation": "ol_search_author", "author": author_name}
            )
            
            # Search for author
            authors = self.client.Author.search(author_name, limit=5)
            
            if not authors:
                logger.info(f"No author found in OpenLibrary: {author_name}")
                return None
            
            # Get the first match or exact match
            author_data = None
            for author in authors:
                if author['name'].lower() == author_name.lower():
                    author_data = author
                    break
            
            if not author_data:
                author_data = authors[0]
            
            # Get full author details
            olid = author_data['key'].split('/')[-1]
            author = self.client.Author.get(olid)
            
            enriched_author = {
                'olid': olid,
                'name': author.name,
                'bio': getattr(author, 'bio', None),
                'birth_date': getattr(author, 'birth_date', None),
                'death_date': getattr(author, 'death_date', None),
                'work_count': len(author.works(limit=1)) if hasattr(author, 'works') else 0
            }
            
            logger.info(
                f"Found author in OpenLibrary: {author_name}",
                extra={"operation": "ol_author_found", "author": author_name, "olid": olid}
            )
            
            return enriched_author
            
        except Exception as e:
            logger.error(f"Error getting author info for {author_name}: {e}")
            return None
    
    def _extract_metadata(self, metadata: Dict[str, Any], identifier: str) -> Dict[str, Any]:
        """Extract and normalize metadata from OpenLibrary response.
        
        Args:
            metadata: Raw metadata from OpenLibrary API
            identifier: The identifier used to find the book (ISBN, etc.)
            
        Returns:
            Normalized metadata dictionary
        """
        enriched = {
            'openlibrary_url': metadata.get('info_url'),
            'preview': metadata.get('preview'),
            'preview_url': metadata.get('preview_url'),
            'thumbnail_url': metadata.get('thumbnail_url'),
            'bib_key': metadata.get('bib_key'),
            'identifier': identifier
        }
        
        # Get full edition details if available
        if 'info_url' in metadata:
            try:
                # Extract OLID from info_url (format: http://openlibrary.org/books/OLID/title)
                url_parts = metadata['info_url'].split('/')
                olid = None
                for part in url_parts:
                    if part.startswith('OL') and (part.endswith('M') or part.endswith('W')):
                        olid = part
                        break
                
                if olid:
                    edition = self.client.Edition.get(olid=olid)
                    
                    if edition:
                        enriched.update({
                            'title': edition.title,
                            'subtitle': getattr(edition, 'subtitle', None),
                            'authors': [author.name for author in edition.authors] if edition.authors else [],
                            'publishers': [edition.publisher] if edition.publisher else [],
                            'publish_date': edition.publish_date,
                            'number_of_pages': edition.number_of_pages,
                            'languages': getattr(edition, 'languages', []),
                            'subjects': getattr(edition, 'subjects', []),
                            'description': getattr(edition, 'description', None),
                            'notes': getattr(edition, 'notes', None),
                            'olid': olid,
                            'work_olid': getattr(edition, 'work_olid', None)
                        })
                        
                        # Extract identifiers
                        if hasattr(edition, 'identifiers') and edition.identifiers:
                            for id_type, id_values in edition.identifiers.items():
                                if isinstance(id_values, list):
                                    enriched[f'{id_type}_ids'] = id_values
                                else:
                                    enriched[f'{id_type}_id'] = id_values
            except Exception as e:
                logger.warning(f"Could not fetch full edition details: {e}")
        
        return enriched
    
    def _extract_search_result(self, book: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract metadata from search result.
        
        Args:
            book: Search result document from OpenLibrary
            
        Returns:
            Normalized metadata dictionary
        """
        try:
            return {
                'title': book.get('title'),
                'authors': book.get('author_name', []) if isinstance(book.get('author_name'), list) else [book.get('author_name')] if book.get('author_name') else [],
                'first_publish_year': book.get('first_publish_year'),
                'publish_year': book.get('publish_year'),
                'publisher': book.get('publisher', []),
                'languages': book.get('language', []),
                'subject': book.get('subject', []),
                'olid': book.get('key', '').split('/')[-1] if book.get('key') else None,
                'cover_url': f"https://covers.openlibrary.org/b/id/{book.get('cover_i')}-L.jpg" if book.get('cover_i') else None,
                'isbn': book.get('isbn', []),
                'oclc': book.get('oclc', []),
                'lccn': book.get('lccn', []),
                'ocaid': book.get('ocaid')
            }
        except Exception as e:
            logger.warning(f"Error extracting search result: {e}")
            return None


# Global service instance
openlibrary_service = OpenLibraryService()
