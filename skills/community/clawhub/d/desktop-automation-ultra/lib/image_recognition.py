"""
Image Recognition Module

Uses OpenCV for template matching and multi-scale detection.
Thread-safe, robust error handling.
"""

import logging
import threading
import os
from typing import Dict, Tuple, Optional, List, Any

logger = logging.getLogger(__name__)


class ImageRecognition:
    """Image recognition using OpenCV."""
    
    def __init__(self):
        self.lock = threading.Lock()
        try:
            import cv2
            self.cv2 = cv2
            logger.info("OpenCV initialized")
        except ImportError:
            logger.warning("OpenCV not installed - image recognition unavailable")
            self.cv2 = None
    
    def find_image(self, template_path: str, confidence: float = 0.9, dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Find template image on screen."""
        if not self.cv2:
            return {"status": "error", "message": "OpenCV not installed"}
        
        if not os.path.exists(template_path):
            return {"status": "error", "message": f"Template not found: {template_path}"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] find_image: %s (confidence=%.2f)", template_path, confidence)
                return {"status": "ok", "dry_run": True}
            
            with self.lock:
                import pyautogui
                
                # Take screenshot
                screenshot = pyautogui.screenshot()
                screen_array = self.cv2.cvtColor(
                    self.cv2.UMat(self.cv2.imread(template_path, 0)).get(),
                    self.cv2.COLOR_RGB2BGR
                )
                
                # Load template
                template = self.cv2.imread(template_path, 0)
                if template is None:
                    return {"status": "error", "message": "Failed to load template"}
                
                # Template matching
                result = self.cv2.matchTemplate(
                    self.cv2.cvtColor(
                        self.cv2.UMat(self.cv2.cvtColor(
                            self.cv2.UMat(screenshot).get(),
                            self.cv2.COLOR_RGB2BGR
                        )).get(),
                        self.cv2.COLOR_BGR2GRAY
                    ),
                    template,
                    self.cv2.TM_CCOEFF_NORMED
                )
                
                min_val, max_val, min_loc, max_loc = self.cv2.minMaxLoc(result)
                
                if max_val >= confidence:
                    x, y = max_loc
                    logger.info("Found image at (%d, %d) with confidence %.2f", x, y, max_val)
                    return {
                        "status": "ok",
                        "x": x,
                        "y": y,
                        "confidence": float(max_val)
                    }
                return {"status": "not_found", "message": f"Template not found (max_confidence={max_val:.2f})"}
        except Exception as e:
            logger.error("find_image failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def find_image_multiscale(self, template_path: str, confidence: float = 0.9, 
                              scale_factors: Optional[List[float]] = None, 
                              dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Find image at multiple scales."""
        if not self.cv2:
            return {"status": "error", "message": "OpenCV not installed"}
        
        if scale_factors is None:
            scale_factors = [0.5, 0.75, 1.0, 1.25, 1.5]
        
        if not os.path.exists(template_path):
            return {"status": "error", "message": f"Template not found: {template_path}"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] find_image_multiscale: %s (scales=%s)", template_path, scale_factors)
                return {"status": "ok", "dry_run": True}
            
            with self.lock:
                import pyautogui
                
                screenshot = pyautogui.screenshot()
                template = self.cv2.imread(template_path, 0)
                
                if template is None:
                    return {"status": "error", "message": "Failed to load template"}
                
                for scale in scale_factors:
                    resized = self.cv2.resize(template, None, fx=scale, fy=scale)
                    result = self.cv2.matchTemplate(
                        self.cv2.cvtColor(
                            self.cv2.UMat(screenshot).get(),
                            self.cv2.COLOR_RGB2GRAY
                        ),
                        resized,
                        self.cv2.TM_CCOEFF_NORMED
                    )
                    
                    min_val, max_val, min_loc, max_loc = self.cv2.minMaxLoc(result)
                    
                    if max_val >= confidence:
                        x, y = max_loc
                        logger.info("Found image at scale %.2f (%.2f confidence)", scale, max_val)
                        return {
                            "status": "ok",
                            "x": x,
                            "y": y,
                            "confidence": float(max_val),
                            "scale": scale
                        }
                
                return {"status": "not_found", "message": "Template not found at any scale"}
        except Exception as e:
            logger.error("find_image_multiscale failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def wait_for_image(self, template_path: str, timeout: float = 30.0, 
                       interval: float = 0.5, confidence: float = 0.9, 
                       dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Wait for image to appear on screen."""
        if not os.path.exists(template_path):
            return {"status": "error", "message": f"Template not found: {template_path}"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] wait_for_image: %s (timeout=%.1fs)", template_path, timeout)
                return {"status": "ok", "dry_run": True}
            
            import time
            start = time.time()
            
            while time.time() - start < timeout:
                result = self.find_image(template_path, confidence=confidence)
                if result["status"] == "ok":
                    logger.info("Image appeared after %.1fs", time.time() - start)
                    return result
                time.sleep(interval)
            
            return {"status": "timeout", "message": f"Image not found within {timeout}s"}
        except Exception as e:
            logger.error("wait_for_image failed: %s", str(e))
            return {"status": "error", "message": str(e)}
