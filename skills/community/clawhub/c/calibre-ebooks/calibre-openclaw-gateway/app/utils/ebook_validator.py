"""Ebook format validation utilities."""
from pathlib import Path
from typing import Optional, Tuple
import struct

from app.utils.logger import get_logger

logger = get_logger(__name__)

# Supported ebook formats and their magic bytes/signatures
EBOOK_FORMATS = {
    # PDF
    '.pdf': {
        'magic': b'%PDF',
        'offset': 0,
        'name': 'PDF'
    },
    # EPUB
    '.epub': {
        'magic': b'PK\x03\x04',
        'offset': 0,
        'name': 'EPUB'
    },
    # MOBI
    '.mobi': {
        'magic': b'\x00BOOKMOBI',
        'offset': 60,
        'name': 'MOBI'
    },
    # AZW3
    '.azw3': {
        'magic': b'\x00BOOKMOBI',
        'offset': 60,
        'name': 'AZW3'
    },
    # KFX
    '.kfx': {
        'magic': b'\xeaDRMION',
        'offset': 0,
        'name': 'KFX'
    },
    # DJVU
    '.djvu': {
        'magic': b'AT&TFORM',
        'offset': 0,
        'name': 'DJVU'
    },
    # LIT
    '.lit': {
        'magic': b'ITOLITLS',
        'offset': 0,
        'name': 'LIT'
    },
    # PDB
    '.pdb': {
        'magic': b'\x00\x00\x00\x00',
        'offset': 0,
        'name': 'PDB'
    },
    # TXT
    '.txt': {
        'magic': None,  # Text files have no magic bytes
        'offset': 0,
        'name': 'TXT'
    },
    # RTF
    '.rtf': {
        'magic': b'{\\rtf',
        'offset': 0,
        'name': 'RTF'
    },
    # DOCX (can be used as ebook container)
    '.docx': {
        'magic': b'PK\x03\x04',
        'offset': 0,
        'name': 'DOCX'
    },
    # ODT (can be used as ebook container)
    '.odt': {
        'magic': b'PK\x03\x04',
        'offset': 0,
        'name': 'ODT'
    },
    # FB2
    '.fb2': {
        'magic': b'<?xml',
        'offset': 0,
        'name': 'FictionBook 2.0'
    },
    # HTML (can be used as ebook)
    '.html': {
        'magic': b'<!DOCTYPE',
        'offset': 0,
        'name': 'HTML'
    },
    '.htm': {
        'magic': b'<!DOCTYPE',
        'offset': 0,
        'name': 'HTML'
    },
    # CBZ (comic book archive)
    '.cbz': {
        'magic': b'PK\x03\x04',
        'offset': 0,
        'name': 'CBZ'
    },
    # CBR (comic book RAR)
    '.cbr': {
        'magic': b'Rar!',
        'offset': 0,
        'name': 'CBR'
    },
}


def is_ebook_format(file_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Check if a file is a valid ebook format.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Tuple of (is_valid, format_name)
    """
    suffix = file_path.suffix.lower()
    
    if suffix not in EBOOK_FORMATS:
        logger.warning(f"Unsupported file format: {suffix}")
        return False, None
    
    format_info = EBOOK_FORMATS[suffix]
    
    # For text files, just check extension
    if format_info['magic'] is None:
        logger.info(f"File {file_path.name} validated as {format_info['name']} (extension check)")
        return True, format_info['name']
    
    # Check magic bytes
    try:
        with open(file_path, 'rb') as f:
            f.seek(format_info['offset'])
            magic_bytes = f.read(len(format_info['magic']))
            
            if magic_bytes == format_info['magic']:
                logger.info(f"File {file_path.name} validated as {format_info['name']}")
                return True, format_info['name']
            else:
                logger.warning(f"File {file_path.name} has invalid magic bytes for {format_info['name']}")
                return False, None
    except Exception as e:
        logger.error(f"Error reading file {file_path.name}: {e}")
        return False, None


def is_ebook_bytes(file_data: bytes, filename: str) -> Tuple[bool, Optional[str]]:
    """
    Check if file bytes represent a valid ebook format.
    
    Args:
        file_data: File content as bytes
        filename: Name of the file
        
    Returns:
        Tuple of (is_valid, format_name)
    """
    file_path = Path(filename)
    suffix = file_path.suffix.lower()
    
    if suffix not in EBOOK_FORMATS:
        logger.warning(f"Unsupported file format: {suffix}")
        return False, None
    
    format_info = EBOOK_FORMATS[suffix]
    
    # For text files, just check extension
    if format_info['magic'] is None:
        logger.info(f"File {filename} validated as {format_info['name']} (extension check)")
        return True, format_info['name']
    
    # Check magic bytes
    try:
        offset = format_info['offset']
        magic_bytes = file_data[offset:offset + len(format_info['magic'])]
        
        if magic_bytes == format_info['magic']:
            logger.info(f"File {filename} validated as {format_info['name']}")
            return True, format_info['name']
        else:
            logger.warning(f"File {filename} has invalid magic bytes for {format_info['name']}")
            return False, None
    except Exception as e:
        logger.error(f"Error validating file {filename}: {e}")
        return False, None


def get_supported_formats() -> list[str]:
    """Get list of supported ebook formats."""
    return list(EBOOK_FORMATS.keys())


def validate_file_size(file_path: Path, max_size_mb: int = 100) -> Tuple[bool, Optional[str]]:
    """
    Validate file size is within acceptable limits.
    
    Args:
        file_path: Path to the file
        max_size_mb: Maximum file size in megabytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        size_bytes = file_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        
        if size_mb > max_size_mb:
            error_msg = f"File size ({size_mb:.2f} MB) exceeds maximum allowed size ({max_size_mb} MB)"
            logger.warning(error_msg)
            return False, error_msg
        
        return True, None
    except Exception as e:
        logger.error(f"Error checking file size: {e}")
        return False, f"Error checking file size: {str(e)}"


def validate_bytes_size(file_data: bytes, filename: str, max_size_mb: int = 100) -> Tuple[bool, Optional[str]]:
    """
    Validate file bytes size is within acceptable limits.
    
    Args:
        file_data: File content as bytes
        filename: Name of the file
        max_size_mb: Maximum file size in megabytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        size_bytes = len(file_data)
        size_mb = size_bytes / (1024 * 1024)
        
        if size_mb > max_size_mb:
            error_msg = f"File size ({size_mb:.2f} MB) exceeds maximum allowed size ({max_size_mb} MB)"
            logger.warning(error_msg)
            return False, error_msg
        
        return True, None
    except Exception as e:
        logger.error(f"Error checking file size: {e}")
        return False, f"Error checking file size: {str(e)}"
