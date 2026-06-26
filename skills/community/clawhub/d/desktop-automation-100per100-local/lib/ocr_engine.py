"""
OCR Engine Module

Uses pytesseract for Optical Character Recognition.
Thread-safe, robust error handling.
"""

import logging
import threading
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class OCREngine:
    """OCR recognition using pytesseract."""
    
    def __init__(self):
        self.lock = threading.Lock()
        try:
            import pytesseract
            self.pytesseract = pytesseract
            logger.info("Tesseract OCR initialized")
        except ImportError:
            logger.warning("pytesseract not installed - OCR unavailable")
            self.pytesseract = None
    
    def find_text_on_screen(self, text: str, lang: str = "fra", dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Find text on screen using OCR."""
        if not self.pytesseract:
            return {"status": "error", "message": "pytesseract not installed"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] find_text_on_screen: '%s' (lang=%s)", text, lang)
                return {"status": "ok", "dry_run": True}
            
            with self.lock:
                import pyautogui
                from pytesseract import Output
                
                screenshot = pyautogui.screenshot()
                data = self.pytesseract.image_to_data(screenshot, lang=lang, output_type=Output.DICT)
                
                results = []
                for i, detected_text in enumerate(data['text']):
                    if text.lower() in detected_text.lower():
                        results.append({
                            "text": detected_text,
                            "x": int(data['left'][i]),
                            "y": int(data['top'][i]),
                            "confidence": int(data['conf'][i])
                        })
                
                if results:
                    logger.info("Found '%s' at %d locations", text, len(results))
                    return {"status": "ok", "locations": results, "count": len(results)}
                
                return {"status": "not_found", "message": f"Text '{text}' not found"}
        except Exception as e:
            logger.error("find_text_on_screen failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def find_all_text_on_screen(self, text: str, lang: str = "fra", 
                                dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Find ALL occurrences of text on screen."""
        if not self.pytesseract:
            return {"status": "error", "message": "pytesseract not installed"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] find_all_text_on_screen: '%s'", text)
                return {"status": "ok", "dry_run": True}
            
            with self.lock:
                import pyautogui
                from pytesseract import Output
                
                screenshot = pyautogui.screenshot()
                data = self.pytesseract.image_to_data(screenshot, lang=lang, output_type=Output.DICT)
                
                results = []
                for i, detected_text in enumerate(data['text']):
                    if detected_text.strip():  # Skip empty
                        results.append({
                            "text": detected_text,
                            "x": int(data['left'][i]),
                            "y": int(data['top'][i]),
                            "width": int(data['width'][i]),
                            "height": int(data['height'][i]),
                            "confidence": int(data['conf'][i])
                        })
                
                logger.info("Extracted %d text elements", len(results))
                return {"status": "ok", "data": results, "count": len(results)}
        except Exception as e:
            logger.error("find_all_text_on_screen failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def read_text_ocr(self, lang: str = "fra", dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Read all text from screen."""
        if not self.pytesseract:
            return {"status": "error", "message": "pytesseract not installed"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] read_text_ocr (lang=%s)", lang)
                return {"status": "ok", "dry_run": True}
            
            with self.lock:
                import pyautogui
                
                screenshot = pyautogui.screenshot()
                text = self.pytesseract.image_to_string(screenshot, lang=lang)
                
                logger.info("OCR read %d characters", len(text))
                return {"status": "ok", "text": text, "length": len(text)}
        except Exception as e:
            logger.error("read_text_ocr failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def read_text_region(self, x: int, y: int, width: int, height: int, 
                        lang: str = "fra", dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Read text from a specific region."""
        if not self.pytesseract:
            return {"status": "error", "message": "pytesseract not installed"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] read_text_region (%d,%d,%d,%d)", x, y, width, height)
                return {"status": "ok", "dry_run": True}
            
            with self.lock:
                import pyautogui
                
                screenshot = pyautogui.screenshot(region=(x, y, width, height))
                text = self.pytesseract.image_to_string(screenshot, lang=lang)
                
                logger.info("OCR region read %d characters", len(text))
                return {"status": "ok", "text": text, "length": len(text)}
        except Exception as e:
            logger.error("read_text_region failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def extract_screen_data(self, region: Optional[Dict] = None, 
                           output_format: str = "json", 
                           lang: str = "fra",
                           dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Extract structured data from screen with bounding boxes."""
        if not self.pytesseract:
            return {"status": "error", "message": "pytesseract not installed"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] extract_screen_data (format=%s)", output_format)
                return {"status": "ok", "dry_run": True}
            
            with self.lock:
                import pyautogui
                from pytesseract import Output
                
                if region:
                    screenshot = pyautogui.screenshot(
                        region=(region.get('x', 0), region.get('y', 0), 
                               region.get('width', 1920), region.get('height', 1080))
                    )
                else:
                    screenshot = pyautogui.screenshot()
                
                data = self.pytesseract.image_to_data(screenshot, lang=lang, output_type=Output.DICT)
                
                results = []
                for i in range(len(data['text'])):
                    if data['text'][i].strip():
                        results.append({
                            "text": data['text'][i],
                            "left": int(data['left'][i]),
                            "top": int(data['top'][i]),
                            "width": int(data['width'][i]),
                            "height": int(data['height'][i]),
                            "conf": int(data['conf'][i])
                        })
                
                logger.info("Extracted %d data elements", len(results))
                return {"status": "ok", "data": results, "count": len(results)}
        except Exception as e:
            logger.error("extract_screen_data failed: %s", str(e))
            return {"status": "error", "message": str(e)}
