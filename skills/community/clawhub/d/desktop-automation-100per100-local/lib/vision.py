#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vision Module — Fast screenshot + image detection + OCR
Uses mss for fast screen capture, OpenCV for template matching, pytesseract for OCR.
"""
import os
import logging
import numpy as np
import cv2

logger = logging.getLogger(__name__)

# Try to import mss (optional but recommended)
try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False
    logger.warning("mss not available — falling back to pyautogui.screenshot")

# Try to import pytesseract (optional)
try:
    import pytesseract
    TESS_AVAILABLE = True
except ImportError:
    TESS_AVAILABLE = False
    logger.warning("pytesseract not available — OCR functions disabled")

def screenshot():
    """
    Capture écran rapide avec mss (si disponible) sinon pyautogui.
    Retourne une image numpy (BGR).
    """
    if MSS_AVAILABLE:
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # monitor primaire
                img = np.array(sct.grab(monitor))
                # mss gives BGRA, convert to BGR for OpenCV
                if img.shape[2] == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                return img
        except Exception as e:
            logger.error(f"mss screenshot failed: {e}, falling back to pyautogui")
            return _screenshot_pyautogui()
    else:
        return _screenshot_pyautogui()

def _screenshot_pyautogui():
    """Fallback using pyautogui"""
    import pyautogui
    img = pyautogui.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def find_on_screen(template_path, threshold=0.8, screen_img=None):
    """
    Trouve un template sur l'écran via OpenCV template matching.

    Args:
        template_path: chemin vers l'image template
        threshold: confiance minimale (0.0-1.0)
        screen_img: image écran optionnelle (pour éviter de recapturer)

    Returns:
        (x, y) coordinates of center if found, else None
    """
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        logger.error(f"Template not found: {template_path}")
        return None

    if screen_img is None:
        screen_img = screenshot()

    result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        h, w = template.shape[:2]
        x = max_loc[0] + w // 2
        y = max_loc[1] + h // 2
        logger.debug(f"Template found at ({x},{y}) conf={max_val:.3f}")
        return (int(x), int(y), float(max_val))
    else:
        logger.debug(f"Template not found (conf={max_val:.3f} < {threshold})")
        return None

def click_position(x, y, duration=0.2, button='left'):
    """
    Déplace la souris vers (x,y) et clique.
    """
    import pyautogui
    pyautogui.moveTo(x, y, duration=duration)
    pyautogui.click(button=button)
    return {"status": "clicked", "x": x, "y": y}

def click_image(template_path, threshold=0.8):
    """
    Trouve une image sur l'écran et clique dessus si trouvée.

    Args:
        template_path: chemin vers le template
        threshold: seuil de confiance

    Returns:
        {"status":"clicked", "position": (x,y), "confidence": float} ou {"status":"not_found"}
    """
    pos = find_on_screen(template_path, threshold)
    if pos:
        x, y, conf = pos
        result = click_position(x, y)
        result['confidence'] = conf
        return result
    return {"status": "not_found"}

def read_text_ocr(lang='fra'):
    """
    Capture l'écran et retourne tout le texte OCRisé.

    Args:
        lang: langue Tesseract (ex: 'fra', 'eng', 'fra+eng')

    Returns:
        {"status":"ok", "text": str} ou erreur
    """
    if not TESS_AVAILABLE:
        return {"status": "error", "message": "pytesseract not installed"}

    try:
        img = screenshot()
        # Convertir en RGB pour pytesseract
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb, lang=lang)
        return {"status": "ok", "text": text.strip()}
    except Exception as e:
        logger.error(f"read_text_ocr error: {e}")
        return {"status": "error", "message": str(e)}

def read_text_region(x, y, width, height, lang='fra'):
    """
    OCR sur une région spécifique de l'écran.

    Args:
        x, y: coin supérieur gauche
        width, height: dimensions
        lang: langue

    Returns:
        {"status":"ok", "text": str}
    """
    if not TESS_AVAILABLE:
        return {"status": "error", "message": "pytesseract not installed"}

    try:
        img = screenshot()
        region = img[y:y+height, x:x+width]
        region_rgb = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(region_rgb, lang=lang)
        return {"status": "ok", "text": text.strip()}
    except Exception as e:
        logger.error(f"read_text_region error: {e}")
        return {"status": "error", "message": str(e)}
