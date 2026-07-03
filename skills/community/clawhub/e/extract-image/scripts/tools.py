from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def extract_image_from_file(
    file_path: str,
    resize: Optional[bool] = True,
    max_width: Optional[float] = 512.0,
    max_height: Optional[float] = 512.0
) -> Dict[str, Any]:
    """
    Extract and analyze images from local file paths. Supports visual content understanding, OCR text extraction, and object recognition for screenshots, photos, diagrams, and documents.
    
    Args:
        file_path: Path to the image file to analyze (supports screenshots, photos, diagrams, and documents in PNG, JPG, GIF, WebP formats)
        resize: For backward compatibility only. Images are always automatically resized to optimal dimensions (max 512x512) for LLM analysis
        max_width: For backward compatibility only. Default maximum width is now 512px
        max_height: For backward compatibility only. Default maximum height is now 512px
    
    Returns:
        
    """
    arguments = {
        "file_path": file_path,
        "resize": resize,
        "max_width": max_width,
        "max_height": max_height
    }
    
    return call_api("1777316659462147", "extract_image_from_file", arguments)

def extract_image_from_url(
    url: str,
    resize: Optional[bool] = True,
    max_width: Optional[float] = 512.0,
    max_height: Optional[float] = 512.0
) -> Dict[str, Any]:
    """
    Extract and analyze images from web URLs. Perfect for analyzing web screenshots, online photos, diagrams, or any image accessible via HTTP/HTTPS for visual content analysis and text extraction.
    
    Args:
        url: URL of the image to analyze for visual content, text extraction, or object recognition (supports web screenshots, photos, diagrams)
        resize: For backward compatibility only. Images are always automatically resized to optimal dimensions (max 512x512) for LLM analysis
        max_width: For backward compatibility only. Default maximum width is now 512px
        max_height: For backward compatibility only. Default maximum height is now 512px
    
    Returns:
        
    """
    arguments = {
        "url": url,
        "resize": resize,
        "max_width": max_width,
        "max_height": max_height
    }
    
    return call_api("1777316659462147", "extract_image_from_url", arguments)

def extract_image_from_base64(
    base64: str,
    mime_type: Optional[str] = "image/png",
    resize: Optional[bool] = True,
    max_width: Optional[float] = 512.0,
    max_height: Optional[float] = 512.0
) -> Dict[str, Any]:
    """
    Extract and analyze images from base64-encoded data. Ideal for processing screenshots from clipboard, dynamically generated images, or images embedded in applications without requiring file system access.
    
    Args:
        base64: Base64-encoded image data to analyze (useful for screenshots, images from clipboard, or dynamically generated visuals)
        mime_type: MIME type of the image (e.g., image/png, image/jpeg)
        resize: For backward compatibility only. Images are always automatically resized to optimal dimensions (max 512x512) for LLM analysis
        max_width: For backward compatibility only. Default maximum width is now 512px
        max_height: For backward compatibility only. Default maximum height is now 512px
    
    Returns:
        
    """
    arguments = {
        "base64": base64,
        "mime_type": mime_type,
        "resize": resize,
        "max_width": max_width,
        "max_height": max_height
    }
    
    return call_api("1777316659462147", "extract_image_from_base64", arguments)

