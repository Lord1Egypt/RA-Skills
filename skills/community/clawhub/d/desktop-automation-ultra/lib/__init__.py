"""
Desktop Automation Library

Complete desktop automation toolkit with safety, logging, and testing.
"""

from lib.actions import ActionManager
from lib.image_recognition import ImageRecognition
from lib.ocr_engine import OCREngine
from lib.macro_player import MacroPlayer
from lib.safety_manager import SafetyManager
from lib.utils import setup_logging, save_json, load_json

__version__ = "2.0.0"
__all__ = [
    "ActionManager",
    "ImageRecognition",
    "OCREngine",
    "MacroPlayer",
    "SafetyManager",
    "setup_logging",
    "save_json",
    "load_json",
]

# Initialize logging on import
setup_logging()
