"""Virus scanning service using VirusTotal API with vt-py library."""
import hashlib
from typing import Optional, Dict, Any
from pathlib import Path
import io

import vt

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class VirusService:
    """Service for scanning files using VirusTotal API via vt-py library."""
    
    def __init__(self):
        self.api_key = settings.VT_API_KEY.get_secret_value() if settings.VT_API_KEY else None
        self.enabled = bool(self.api_key)
        
        if self.enabled:
            logger.info("VirusTotal API integration enabled")
        else:
            logger.info("VirusTotal API integration disabled (VT_API_KEY not set)")
    
    def is_enabled(self) -> bool:
        """Check if virus scanning is enabled."""
        return self.enabled
    
    async def scan_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Scan a file using VirusTotal API.
        
        Args:
            file_path: Path to the file to scan
            
        Returns:
            Dictionary with scan results including:
            - scan_id: ID of the scan
            - malicious: Boolean indicating if file is malicious
            - detection_ratio: e.g., "5/60" (5/60 engines detected malware)
            - summary: Brief summary of results
        """
        if not self.enabled:
            return {
                "scanned": False,
                "reason": "VirusTotal API not configured",
                "malicious": None,
            }
        
        try:
            logger.info(f"Starting virus scan for file: {file_path.name}")
            
            # Calculate file hash
            file_hash = self._calculate_sha256(file_path)
            logger.info(f"File SHA256: {file_hash}")
            
            # Create VirusTotal client
            async with vt.Client(self.api_key) as client:
                # First check if file already exists in VirusTotal database
                try:
                    file_info = await client.get_object(f"/files/{file_hash}")
                    logger.info(f"File already analyzed in VirusTotal")
                    return self._parse_file_object(file_info, file_hash)
                except vt.error.NotFoundError:
                    logger.info(f"File not found in VirusTotal database, uploading for scanning")
                
                # Upload file for scanning
                with open(file_path, "rb") as f:
                    analysis = await client.scan_file(f, wait_for_completion=True)
                
                logger.info(f"Analysis completed for {file_path.name}")
                
                # Get the file object with analysis results
                file_info = await client.get_object(f"/files/{file_hash}")
                return self._parse_file_object(file_info, file_hash)
            
        except vt.error.APIError as e:
            logger.error(f"VirusTotal API error: {e}", exc_info=True)
            return {
                "scanned": False,
                "reason": f"VirusTotal API error: {str(e)}",
                "malicious": None,
            }
        except Exception as e:
            logger.error(f"Error during virus scan: {e}", exc_info=True)
            return {
                "scanned": False,
                "reason": f"Scan error: {str(e)}",
                "malicious": None,
            }
    
    async def scan_bytes(self, file_data: bytes, filename: str) -> Dict[str, Any]:
        """
        Scan file bytes using VirusTotal API.
        
        Args:
            file_data: File content as bytes
            filename: Name of the file
            
        Returns:
            Dictionary with scan results
        """
        if not self.enabled:
            return {
                "scanned": False,
                "reason": "VirusTotal API not configured",
                "malicious": None,
            }
        
        try:
            logger.info(f"Starting virus scan for file bytes: {filename}")
            
            # Calculate file hash
            file_hash = hashlib.sha256(file_data).hexdigest()
            logger.info(f"File SHA256: {file_hash}")
            
            # Create VirusTotal client
            async with vt.Client(self.api_key) as client:
                # First check if file already exists in VirusTotal database
                try:
                    file_info = await client.get_object(f"/files/{file_hash}")
                    logger.info(f"File already analyzed in VirusTotal")
                    return self._parse_file_object(file_info, file_hash)
                except vt.error.NotFoundError:
                    logger.info(f"File not found in VirusTotal database, uploading for scanning")
                
                # Upload file bytes for scanning
                file_like = io.BytesIO(file_data)
                analysis = await client.scan_file(file_like, wait_for_completion=True)
                
                logger.info(f"Analysis completed for {filename}")
                
                # Get the file object with analysis results
                file_info = await client.get_object(f"/files/{file_hash}")
                return self._parse_file_object(file_info, file_hash)
            
        except vt.error.APIError as e:
            logger.error(f"VirusTotal API error: {e}", exc_info=True)
            return {
                "scanned": False,
                "reason": f"VirusTotal API error: {str(e)}",
                "malicious": None,
            }
        except Exception as e:
            logger.error(f"Error during virus scan: {e}", exc_info=True)
            return {
                "scanned": False,
                "reason": f"Scan error: {str(e)}",
                "malicious": None,
            }
    
    def _calculate_sha256(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def _parse_file_object(self, file_obj: vt.Object, file_hash: str) -> Dict[str, Any]:
        """Parse VirusTotal file object to extract scan results."""
        # Get last analysis stats
        stats = getattr(file_obj, "last_analysis_stats", None)
        
        if not stats:
            stats = file_obj.get("last_analysis_stats", {})
        
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        harmless = stats.get("harmless", 0)
        undetected = stats.get("undetected", 0)
        
        total = malicious + suspicious + harmless + undetected
        detection_ratio = f"{malicious + suspicious}/{total}" if total > 0 else "0/0"
        
        is_malicious = (malicious + suspicious) > 0
        
        return {
            "scanned": True,
            "malicious": is_malicious,
            "detection_ratio": detection_ratio,
            "file_hash": file_hash,
            "stats": stats,
            "summary": f"Detection ratio: {detection_ratio}" if total > 0 else "No analysis data"
        }


virus_service = VirusService()
