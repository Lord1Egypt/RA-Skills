"""Download service for handling book downloads from OpenLibrary/Archive.org."""

import os
import hashlib
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urlparse

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DownloadService:
    """Service for downloading books from OpenLibrary/Archive.org."""
    
    def __init__(self):
        """Initialize download service."""
        self.download_dir = Path(settings.DOWNLOAD_DIR) if settings.DOWNLOAD_DIR else None
        self.enabled = settings.DOWNLOAD_QUEUE_ENABLED
        
        if self.enabled and self.download_dir:
            self.download_dir.mkdir(parents=True, exist_ok=True)
            logger.info(
                f"Download service initialized with directory: {self.download_dir}",
                extra={"operation": "download_init", "download_dir": str(self.download_dir)}
            )
        else:
            logger.warning("Download service disabled: DOWNLOAD_DIR not configured")
    
    def calculate_file_hash(self, file_path: Path) -> Optional[str]:
        """Calculate SHA256 hash of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            SHA256 hash as hex string or None if error
        """
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating file hash for {file_path}: {e}")
            return None
    
    def get_download_url(self, ocaid: str, format: str = "PDF") -> Optional[str]:
        """Get download URL for Archive.org book.
        
        Args:
            ocaid: Archive.org identifier
            format: Preferred format (PDF, EPUB, Kindle, Daisy)
            
        Returns:
            Download URL or None if not available
        """
        base_url = f"https://archive.org/download/{ocaid}"
        
        format_urls = {
            "PDF": f"{base_url}/{ocaid}_text.pdf",
            "EPUB": f"{base_url}/{ocaid}.epub",
            "Kindle": f"{base_url}/{ocaid}_mobi.mobi",
            "Daisy": f"{base_url}/{ocaid}_daisy.zip"
        }
        
        url = format_urls.get(format)
        if not url:
            logger.warning(f"Unsupported format: {format}")
            return None
        
        # Verify URL is accessible
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                logger.info(f"Download URL available for {ocaid} in {format}", extra={"operation": "download_url_check", "ocaid": ocaid, "format": format})
                return url
            else:
                logger.warning(f"Download URL not accessible: {url} (status: {response.status_code})")
                return None
        except Exception as e:
            logger.error(f"Error checking download URL {url}: {e}")
            return None
    
    def check_download_available(self, ocaid: Optional[str], download_url: Optional[str], 
                                preferred_format: str = "PDF") -> bool:
        """Check if download is available for a book.
        
        Args:
            ocaid: Archive.org identifier
            download_url: Direct download URL
            preferred_format: Preferred format
            
        Returns:
            True if download is available, False otherwise
        """
        if download_url:
            # Check if direct URL is accessible
            try:
                response = requests.head(download_url, timeout=10, allow_redirects=True)
                return response.status_code == 200
            except Exception as e:
                logger.error(f"Error checking download URL {download_url}: {e}")
                return False
        
        if ocaid:
            # Check Archive.org URL
            url = self.get_download_url(ocaid, preferred_format)
            return url is not None
        
        return False
    
    def download_file(self, url: str, filename: str) -> Optional[Path]:
        """Download file from URL to download directory.
        
        Args:
            url: Download URL
            filename: Target filename
            
        Returns:
            Path to downloaded file or None if failed
        """
        if not self.download_dir:
            logger.error("Download directory not configured")
            return None
        
        file_path = self.download_dir / filename
        
        try:
            logger.info(f"Starting download: {url} -> {file_path}", extra={"operation": "download_start", "url": url, "path": str(file_path)})
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Write file in chunks
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = file_path.stat().st_size
            file_hash = self.calculate_file_hash(file_path)
            
            logger.info(
                f"Download completed: {file_path} ({file_size} bytes, hash: {file_hash})",
                extra={"operation": "download_complete", "path": str(file_path), "size": file_size, "hash": file_hash}
            )
            
            return file_path
            
        except requests.RequestException as e:
            logger.error(f"Download failed for {url}: {e}")
            # Clean up partial file
            if file_path.exists():
                file_path.unlink()
            return None
        except Exception as e:
            logger.error(f"Error saving file {file_path}: {e}")
            if file_path.exists():
                file_path.unlink()
            return None
    
    def sanitize_filename(self, title: str, author: Optional[str] = None) -> str:
        """Sanitize title and author to create safe filename.
        
        Args:
            title: Book title
            author: Optional author name
            
        Returns:
            Sanitized filename without extension
        """
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        safe_title = ''.join(c for c in title if c not in invalid_chars).strip()
        
        if author:
            safe_author = ''.join(c for c in author if c not in invalid_chars).strip()
            return f"{safe_author} - {safe_title}"
        
        return safe_title
    
    def download_book(self, title: str, author: Optional[str], ocaid: Optional[str], 
                      download_url: Optional[str], preferred_format: str = "PDF") -> Dict[str, Any]:
        """Download a book from OpenLibrary/Archive.org.
        
        Args:
            title: Book title
            author: Optional author
            ocaid: Archive.org identifier
            download_url: Direct download URL (overrides ocaid)
            preferred_format: Preferred format
            
        Returns:
            Dictionary with download result
        """
        if not self.download_dir:
            return {
                "success": False,
                "error": "Download directory not configured"
            }
        
        # Determine download URL
        url = download_url
        if not url and ocaid:
            url = self.get_download_url(ocaid, preferred_format)
        
        if not url:
            return {
                "success": False,
                "error": "No download URL available",
                "download_available": False
            }
        
        # Determine file extension
        ext_map = {"PDF": ".pdf", "EPUB": ".epub", "Kindle": ".mobi", "Daisy": ".zip"}
        ext = ext_map.get(preferred_format, ".pdf")
        
        # Create safe filename
        base_name = self.sanitize_filename(title, author)
        filename = f"{base_name}{ext}"
        
        # Download file
        file_path = self.download_file(url, filename)
        
        if file_path and file_path.exists():
            file_hash = self.calculate_file_hash(file_path)
            return {
                "success": True,
                "file_path": str(file_path),
                "file_size": file_path.stat().st_size,
                "file_hash": file_hash,
                "format": preferred_format,
                "download_available": True
            }
        else:
            return {
                "success": False,
                "error": "Download failed",
                "download_available": False
            }


# Global service instance
download_service = DownloadService()
