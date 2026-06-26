"""
Utilities Module

Helper functions for logging, file management, data conversion.
"""

import logging
import os
import json
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def setup_logging(log_dir: Optional[str] = None) -> None:
    """Setup logging with daily rotation."""
    if log_dir is None:
        log_dir = os.path.expanduser("~/.openclaw/skills/desktop-automation-logs")
    
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(
        log_dir,
        f"automation_{datetime.now().strftime('%Y-%m-%d')}.log"
    )
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    logger.info("Logging initialized: %s", log_file)


def save_json(data: Dict, filepath: str) -> bool:
    """Save data to JSON file with UTF-8 encoding."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("Saved JSON: %s", filepath)
        return True
    except Exception as e:
        logger.error("Failed to save JSON: %s", str(e))
        return False


def load_json(filepath: str) -> Optional[Dict]:
    """Load JSON file with UTF-8 encoding."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info("Loaded JSON: %s", filepath)
        return data
    except Exception as e:
        logger.error("Failed to load JSON: %s", str(e))
        return None


def ensure_directory(directory: str) -> bool:
    """Ensure directory exists."""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logger.error("Failed to create directory: %s", str(e))
        return False


def file_exists(filepath: str) -> bool:
    """Check if file exists."""
    return os.path.isfile(os.path.expanduser(filepath))


def get_screen_resolution() -> tuple:
    """Get screen resolution."""
    try:
        import pyautogui
        return pyautogui.size()
    except Exception as e:
        logger.error("Failed to get screen resolution: %s", str(e))
        return (1920, 1080)


class ThreadSafeCounter:
    """Thread-safe counter."""
    
    def __init__(self, initial: int = 0):
        self.value = initial
        self.lock = threading.Lock()
    
    def increment(self) -> int:
        with self.lock:
            self.value += 1
            return self.value
    
    def get(self) -> int:
        with self.lock:
            return self.value


def format_coordinates(x: int, y: int) -> str:
    """Format coordinates for logging."""
    return f"({x}, {y})"


def validate_coordinates(x: int, y: int) -> bool:
    """Validate coordinates are within screen bounds."""
    width, height = get_screen_resolution()
    return 0 <= x <= width and 0 <= y <= height


def log_action(action: str, params: Dict, result: Dict) -> None:
    """Log action execution."""
    status = result.get('status', 'unknown')
    logger.info("Action: %s | Params: %s | Status: %s", action, params, status)
