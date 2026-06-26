import io
import os
import re
from typing import Union
from urllib.parse import urlparse

_MISSING_DEPENDENCIES = []

try:
    import ddddocr
except ImportError:
    _MISSING_DEPENDENCIES.append("ddddocr")

try:
    import cv2
except ImportError:
    _MISSING_DEPENDENCIES.append("opencv-python")

try:
    import numpy as np
except ImportError:
    _MISSING_DEPENDENCIES.append("numpy")

try:
    from PIL import Image
except ImportError:
    _MISSING_DEPENDENCIES.append("Pillow")

try:
    import requests
except ImportError:
    _MISSING_DEPENDENCIES.append("requests")


def check_dependencies() -> None:
    if _MISSING_DEPENDENCIES:
        missing = ", ".join(_MISSING_DEPENDENCIES)
        raise ImportError(
            f"Missing required dependencies: {missing}\n"
            f"Please install them with: pip install {' '.join(_MISSING_DEPENDENCIES)}"
        )


class CaptchaRecognizer:
    def __init__(self, show_ad: bool = False):
        check_dependencies()
        self.ocr = ddddocr.DdddOcr(show_ad=show_ad)
    
    def recognize_from_file(self, image_path: str, preprocess: bool = False) -> str:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        if preprocess:
            image_bytes = self._preprocess_image(image_bytes)
        
        result = self.ocr.classification(image_bytes)
        return result
    
    def recognize_from_url(self, url: str, preprocess: bool = False, timeout: int = 10) -> str:
        if url.startswith("blob:"):
            raise ValueError(
                "Blob URLs (blob:https://...) cannot be directly accessed from server-side code. "
                "Blob URLs are only valid in the browser context. "
                "Please provide the actual image URL or download the image first."
            )
        
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Invalid URL scheme: {parsed.scheme}. Only http and https are supported.")
        
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to fetch image from URL: {e}")
        
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            extension = os.path.splitext(parsed.path)[1].lower()
            if extension not in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"):
                raise ValueError(f"URL does not appear to be an image. Content-Type: {content_type}")
        
        image_bytes = response.content
        
        if preprocess:
            image_bytes = self._preprocess_image(image_bytes)
        
        result = self.ocr.classification(image_bytes)
        return result
    
    def recognize_from_bytes(self, image_bytes: bytes, preprocess: bool = False) -> str:
        if preprocess:
            image_bytes = self._preprocess_image(image_bytes)
        
        result = self.ocr.classification(image_bytes)
        return result
    
    def recognize_from_pil(self, pil_image: Image.Image, preprocess: bool = False) -> str:
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        
        if preprocess:
            image_bytes = self._preprocess_image(image_bytes)
        
        result = self.ocr.classification(image_bytes)
        return result
    
    def _preprocess_image(self, image_bytes: bytes) -> bytes:
        img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        is_success, buffer = cv2.imencode(".png", binary)
        if not is_success:
            raise RuntimeError("Failed to encode preprocessed image")
        
        return io.BytesIO(buffer).getvalue()


_recognizer: CaptchaRecognizer = None


def get_recognizer(show_ad: bool = False) -> CaptchaRecognizer:
    global _recognizer
    if _recognizer is None:
        _recognizer = CaptchaRecognizer(show_ad=show_ad)
    return _recognizer


def recognize_captcha(image: Union[str, bytes, Image.Image], preprocess: bool = False, show_ad: bool = False, timeout: int = 10) -> str:
    recognizer = get_recognizer(show_ad=show_ad)
    
    if isinstance(image, str):
        if _is_url(image):
            return recognizer.recognize_from_url(image, preprocess=preprocess, timeout=timeout)
        return recognizer.recognize_from_file(image, preprocess=preprocess)
    elif isinstance(image, bytes):
        return recognizer.recognize_from_bytes(image, preprocess=preprocess)
    elif isinstance(image, Image.Image):
        return recognizer.recognize_from_pil(image, preprocess=preprocess)
    else:
        raise TypeError(f"Unsupported image type: {type(image)}")


def _is_url(path: str) -> bool:
    if path.startswith("blob:"):
        return True
    parsed = urlparse(path)
    return parsed.scheme in ("http", "https")


if __name__ == "__main__":
    import sys
    
    try:
        check_dependencies()
    except ImportError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("Usage: python captcha.py <image_path_or_url> [--preprocess]")
        print("  image_path_or_url: Local file path or HTTP/HTTPS URL to captcha image")
        print("  --preprocess: Enable image preprocessing (grayscale, binarization)")
        sys.exit(1)
    
    image_path = sys.argv[1]
    preprocess = "--preprocess" in sys.argv
    
    try:
        result = recognize_captcha(image_path, preprocess=preprocess, show_ad=False)
        print(f"Captcha recognition result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
