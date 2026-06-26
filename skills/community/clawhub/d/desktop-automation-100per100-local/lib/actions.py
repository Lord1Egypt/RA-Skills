"""
Desktop Automation Actions Module

Core actions for mouse, keyboard, and window control.
Thread-safe, error handling, logging integrated.
"""

import pyautogui
import pygetwindow as gw
import time
import threading
import logging
from typing import Dict, Tuple, Optional, Any, List
from PIL import Image

logger = logging.getLogger(__name__)


class ActionManager:
    """Manages desktop automation actions with safety and logging."""
    
    def __init__(self, safe_mode: bool = True):
        self.safe_mode = safe_mode
        self.lock = threading.Lock()
        pyautogui.FAILSAFE = True
        logger.info("ActionManager initialized with safe_mode=%s", self.safe_mode)
    
    def set_safe_mode(self, enabled: bool) -> Dict[str, Any]:
        """Enable or disable safe mode."""
        with self.lock:
            self.safe_mode = enabled
            logger.info("Safe mode set to %s", enabled)
            return {"status": "ok", "safe_mode": self.safe_mode}
    
    def _check_safe(self, action: str, params: Dict) -> bool:
        """Check if action is safe to execute."""
        if not self.safe_mode:
            return True
        
        dangerous_actions = {"type", "press_key", "click", "drag"}
        dangerous_patterns = ["rm ", "del ", "C:\\Windows\\", "/etc/", "sudo"]
        
        if action not in dangerous_actions:
            return True
        
        # Check parameters for dangerous patterns
        for key, value in params.items():
            if isinstance(value, str):
                for pattern in dangerous_patterns:
                    if pattern.lower() in value.lower():
                        logger.warning("Safe mode blocked action %s: dangerous pattern '%s'", action, pattern)
                        return False
        
        return True
    
    def click(self, x: int, y: int, button: str = "left", dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Click at coordinates."""
        params = {"x": x, "y": y, "button": button}
        
        if not self._check_safe("click", params):
            return {"status": "blocked", "reason": "Safe mode active"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] click at (%d, %d) button=%s", x, y, button)
                return {"status": "ok", "dry_run": True, "x": x, "y": y}
            
            with self.lock:
                pyautogui.click(x, y, button=button)
                logger.info("Clicked at (%d, %d) with %s button", x, y, button)
            return {"status": "ok", "x": x, "y": y}
        except Exception as e:
            logger.error("click failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def type(self, text: str, interval: float = 0.05, dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Type text."""
        params = {"text": text}
        
        if not self._check_safe("type", params):
            return {"status": "blocked", "reason": "Safe mode active"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] type '%s' with interval %.2f", text, interval)
                return {"status": "ok", "dry_run": True, "text": text}
            
            with self.lock:
                pyautogui.typewrite(text, interval=interval)
                logger.info("Typed: %s", text)
            return {"status": "ok", "text": text}
        except Exception as e:
            logger.error("type failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def press_key(self, key: str, dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Press a single key."""
        params = {"key": key}
        
        if not self._check_safe("press_key", params):
            return {"status": "blocked", "reason": "Safe mode active"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] press key '%s'", key)
                return {"status": "ok", "dry_run": True, "key": key}
            
            with self.lock:
                pyautogui.press(key)
                logger.info("Pressed key: %s", key)
            return {"status": "ok", "key": key}
        except Exception as e:
            logger.error("press_key failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5, dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Move mouse to coordinates."""
        try:
            if dry_run:
                logger.info("[DRY RUN] move mouse to (%d, %d)", x, y)
                return {"status": "ok", "dry_run": True, "x": x, "y": y}
            
            with self.lock:
                pyautogui.moveTo(x, y, duration=duration)
                logger.info("Moved mouse to (%d, %d)", x, y)
            return {"status": "ok", "x": x, "y": y}
        except Exception as e:
            logger.error("move_mouse failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def scroll(self, amount: int = 5, dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Scroll up/down."""
        try:
            if dry_run:
                logger.info("[DRY RUN] scroll %d", amount)
                return {"status": "ok", "dry_run": True, "amount": amount}
            
            with self.lock:
                pyautogui.scroll(amount)
                logger.info("Scrolled %d", amount)
            return {"status": "ok", "amount": amount}
        except Exception as e:
            logger.error("scroll failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, 
             duration: float = 0.5, button: str = "left", dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Drag from one position to another."""
        params = {"start": (start_x, start_y), "end": (end_x, end_y)}
        
        if not self._check_safe("drag", params):
            return {"status": "blocked", "reason": "Safe mode active"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] drag from (%d,%d) to (%d,%d)", start_x, start_y, end_x, end_y)
                return {"status": "ok", "dry_run": True}
            
            with self.lock:
                pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration, button=button)
                logger.info("Dragged from (%d,%d) to (%d,%d)", start_x, start_y, end_x, end_y)
            return {"status": "ok"}
        except Exception as e:
            logger.error("drag failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def screenshot(self, path: str = "~/Desktop/screenshot.png", dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Take a screenshot."""
        try:
            if dry_run:
                logger.info("[DRY RUN] screenshot to %s", path)
                return {"status": "ok", "dry_run": True, "path": path}
            
            import os
            full_path = os.path.expanduser(path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with self.lock:
                screenshot = pyautogui.screenshot()
                screenshot.save(full_path)
                logger.info("Screenshot saved to %s", full_path)
            return {"status": "ok", "path": full_path}
        except Exception as e:
            logger.error("screenshot failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def get_active_window(self, dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Get active window info."""
        try:
            with self.lock:
                active = gw.getActiveWindow()
                if active:
                    result = {
                        "status": "ok",
                        "title": active.title,
                        "x": active.left,
                        "y": active.top,
                        "width": active.width,
                        "height": active.height
                    }
                    logger.info("Active window: %s", active.title)
                    return result
                return {"status": "error", "message": "No active window"}
        except Exception as e:
            logger.error("get_active_window failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def list_windows(self, dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """List all windows."""
        try:
            with self.lock:
                windows = []
                for w in gw.getAllWindows():
                    windows.append({
                        "title": w.title,
                        "x": w.left,
                        "y": w.top,
                        "width": w.width,
                        "height": w.height,
                        "is_active": w == gw.getActiveWindow()
                    })
                logger.info("Listed %d windows", len(windows))
                return {"status": "ok", "windows": windows, "count": len(windows)}
        except Exception as e:
            logger.error("list_windows failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def activate_window(self, title_substring: str, dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Activate window by title substring."""
        try:
            if dry_run:
                logger.info("[DRY RUN] activate window containing '%s'", title_substring)
                return {"status": "ok", "dry_run": True}
            
            with self.lock:
                for w in gw.getAllWindows():
                    if title_substring.lower() in w.title.lower():
                        w.activate()
                        logger.info("Activated window: %s", w.title)
                        return {"status": "ok", "title": w.title}
                return {"status": "error", "message": f"Window '{title_substring}' not found"}
        except Exception as e:
            logger.error("activate_window failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def copy_to_clipboard(self, text: str, dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Copy text to clipboard."""
        try:
            if dry_run:
                logger.info("[DRY RUN] copy to clipboard: %s", text[:50])
                return {"status": "ok", "dry_run": True}
            
            try:
                import pyperclip
                with self.lock:
                    pyperclip.copy(text)
                    logger.info("Copied to clipboard (%d chars)", len(text))
                return {"status": "ok"}
            except ImportError:
                return {"status": "error", "message": "pyperclip not installed"}
        except Exception as e:
            logger.error("copy_to_clipboard failed: %s", str(e))
            return {"status": "error", "message": str(e)}
    
    def paste_from_clipboard(self, dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Paste from clipboard."""
        try:
            try:
                import pyperclip
                with self.lock:
                    text = pyperclip.paste()
                    pyautogui.typewrite(text, interval=0.01)
                    logger.info("Pasted from clipboard (%d chars)", len(text))
                return {"status": "ok", "length": len(text)}
            except ImportError:
                return {"status": "error", "message": "pyperclip not installed"}
        except Exception as e:
            logger.error("paste_from_clipboard failed: %s", str(e))
            return {"status": "error", "message": str(e)}
