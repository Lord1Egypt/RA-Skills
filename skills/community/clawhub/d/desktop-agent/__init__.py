"""
Desktop AI Agent - Core Module
Enables AI to see, control, and learn from desktop operations
"""

import pyautogui
import mss
import numpy as np
from PIL import Image
import json
import os
from datetime import datetime
from pathlib import Path

class DesktopAgent:
    def __init__(self, workspace_path: str):
        self.workspace = Path(workspace_path)
        self.tasks_dir = self.workspace / "learned_tasks"
        self.tasks_dir.mkdir(exist_ok=True)
        
        # Safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # Screen info
        self.screen_size = pyautogui.size()
        
        # OCR reader (lazy load)
        self._ocr_reader = None
        
    # ==================== VISION ====================
    
    def capture_screen(self, region: tuple = None) -> np.ndarray:
        """Capture screen or region. Returns numpy array."""
        with mss.mss() as sct:
            if region:
                x, y, w, h = region
                screenshot = sct.grab((x, y, x + w, y + h))
            else:
                screenshot = sct.grab(sct.monitors[1])
                
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            return np.array(img)
    
    def capture_to_file(self, filepath: str, region: tuple = None):
        """Capture screen and save to file."""
        img = self.capture_screen(region)
        Image.fromarray(img).save(filepath)
        return filepath
    
    def get_pixel_color(self, x: int, y: int) -> tuple:
        """Get RGB color at specific coordinate."""
        img = self.capture_screen()
        return tuple(img[y, x])
    
    # ==================== OCR ====================
    
    def _get_ocr_reader(self):
        """Get or create OCR reader."""
        if self._ocr_reader is None:
            import easyocr
            self._ocr_reader = easyocr.Reader(['en'], gpu=False)
        return self._ocr_reader
    
    def read_screen_text(self, region: tuple = None) -> list:
        """
        Read all text from screen or region.
        Returns list of dicts with text, confidence, bbox, center.
        """
        img = self.capture_screen(region)
        img_pil = Image.fromarray(img)
            
        reader = self._get_ocr_reader()
        results = reader.readtext(np.array(img_pil))
        
        text_items = []
        for bbox, text, confidence in results:
            if confidence > 0.3:
                x1 = int(min([p[0] for p in bbox]))
                y1 = int(min([p[1] for p in bbox]))
                x2 = int(max([p[0] for p in bbox]))
                y2 = int(max([p[1] for p in bbox]))
                
                text_items.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': (x1, y1, x2, y2),
                    'center': ((x1+x2)//2, (y1+y2)//2)
                })
                
        return text_items
    
    def find_text(self, text: str, region: tuple = None) -> list:
        """
        Find all occurrences of text on screen.
        Returns list of matches with coordinates.
        """
        items = self.read_screen_text(region)
        matches = []
        
        text_lower = text.lower()
        for item in items:
            if text_lower in item['text'].lower():
                matches.append(item)
                
        return matches
    
    def click_text(self, text: str, instance: int = 0) -> bool:
        """
        Click on text. instance 0 = first match, 1 = second, etc.
        """
        matches = self.find_text(text)
        
        if not matches:
            print(f"Text '{text}' not found")
            return False
            
        if instance >= len(matches):
            print(f"Only {len(matches)} matches, instance {instance} doesn't exist")
            return False
            
        x, y = matches[instance]['center']
        self.click(x, y)
        print(f"Clicked on '{text}' at ({x}, {y})")
        return True
    
    # ==================== COMPUTER VISION ====================
    
    def find_image(self, template_path: str, confidence: float = 0.8) -> tuple:
        """
        Find an image on screen using template matching.
        Returns (x, y, confidence) if found.
        """
        import cv2
        
        screen = self.capture_screen()
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"Template not found: {template_path}")
            return None
            
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= confidence:
            h, w = template.shape
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y, max_val)
            
        return None
    
    def click_image(self, template_path: str, confidence: float = 0.8) -> bool:
        """Click on an image template on screen."""
        result = self.find_image(template_path, confidence)
        
        if result:
            x, y, conf = result
            self.click(x, y)
            print(f"Clicked image at ({x}, {y}) conf={conf:.2f}")
            return True
            
        print(f"Image not found: {template_path}")
        return False
    
    # ==================== MOUSE ====================
    
    def get_mouse_position(self) -> tuple:
        """Get current mouse position."""
        return pyautogui.position()
    
    def move_to(self, x: int, y: int, duration: float = 0.3):
        """Move mouse to position smoothly."""
        pyautogui.moveTo(x, y, duration=duration)
        
    def click(self, x: int = None, y: int = None, button: str = "left", clicks: int = 1):
        """Click at position or current location."""
        if x is not None and y is not None:
            pyautogui.click(x, y, clicks=clicks, button=button)
        else:
            pyautogui.click(clicks=clicks, button=button)
            
    def double_click(self, x: int = None, y: int = None):
        """Double click."""
        self.click(x, y, clicks=2)
        
    def right_click(self, x: int = None, y: int = None):
        """Right click."""
        self.click(x, y, button="right")
        
    def drag_to(self, x: int, y: int, duration: float = 0.5):
        """Drag mouse to position."""
        pyautogui.dragTo(x, y, duration=duration)
    
    # ==================== KEYBOARD ====================
    
    def type(self, text: str, interval: float = 0.05):
        """Type text."""
        pyautogui.write(text, interval=interval)
        
    def press(self, *keys):
        """Press key(s). Examples: 'enter', 'ctrl', 'c', 'alt', 'tab'"""
        for key in keys:
            pyautogui.press(key)
            
    def hotkey(self, *keys):
        """Press key combination. Examples: 'ctrl', 'c' for copy."""
        pyautogui.hotkey(*keys)
        
    # ==================== LEARNING SYSTEM ====================
    
    def save_task(self, task_name: str, steps: list):
        """Save a learned task with its steps."""
        task_data = {
            "name": task_name,
            "created": datetime.now().isoformat(),
            "steps": steps
        }
        
        filepath = self.tasks_dir / f"{task_name.replace(' ', '_')}.json"
        with open(filepath, 'w') as f:
            json.dump(task_data, f, indent=2)
            
        return str(filepath)
    
    def load_task(self, task_name: str) -> dict:
        """Load a saved task."""
        filepath = self.tasks_dir / f"{task_name.replace(' ', '_')}.json"
        with open(filepath, 'r') as f:
            return json.load(f)
            
    def list_tasks(self) -> list:
        """List all learned tasks."""
        tasks = []
        for f in self.tasks_dir.glob("*.json"):
            tasks.append(f.stem)
        return tasks
    
    def execute_task(self, task_name: str, **variables):
        """Execute a learned task with optional variables."""
        task = self.load_task(task_name)
        
        results = []
        for step in task["steps"]:
            step_type = step.get("type")
            
            # Replace variables in text
            text = step.get("text", "")
            for key, value in variables.items():
                text = text.replace("{" + key + "}", value)
            
            if step_type == "click":
                self.click(step.get("x"), step.get("y"))
                results.append(f"Clicked {step.get('x')}, {step.get('y')}")
                
            elif step_type == "type":
                self.type(text)
                results.append(f"Typed: {text}")
                
            elif step_type == "press":
                self.press(*step.get("keys"))
                results.append(f"Pressed: {step.get('keys')}")
                
            elif step_type == "hotkey":
                self.hotkey(*step.get("keys"))
                results.append(f"Hotkey: {step.get('keys')}")
                
            elif step_type == "wait":
                import time
                time.sleep(step.get("seconds", 1))
                results.append(f"Waited {step.get('seconds')}s")
                
            elif step_type == "screenshot":
                self.capture_to_file(step.get("filepath"))
                results.append(f"Screenshot: {step.get('filepath')}")
                
            elif step_type == "click_text":
                self.click_text(text)
                results.append(f"Clicked text: {text}")
                
        return results


# Singleton instance
_agent = None

def get_agent(workspace: str = None) -> DesktopAgent:
    """Get or create desktop agent instance."""
    global _agent
    if _agent is None:
        workspace = workspace or os.environ.get(
            'OPENCLAW_WORKSPACE', 
            r'C:\Users\funky\.openclaw\workspace'
        )
        _agent = DesktopAgent(workspace)
    return _agent
