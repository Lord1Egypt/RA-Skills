"""
Safety Manager Module

Manages safe mode and protection against dangerous operations.
Thread-safe.
"""

import logging
import threading
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class SafetyManager:
    """Manages safety constraints and restrictions."""
    
    DANGEROUS_PATTERNS = [
        "rm ", "del ", "rmdir ", "format ",
        "C:\\Windows\\", "/etc/", "/sys/",
        "sudo ", "taskkill ", "shutdown",
        "--force", "/f"
    ]
    
    DANGEROUS_ACTIONS = {
        "type", "press_key", "click", "drag"
    }
    
    def __init__(self, safe_mode_enabled: bool = True):
        self.safe_mode_enabled = safe_mode_enabled
        self.lock = threading.Lock()
        logger.info("SafetyManager initialized (safe_mode=%s)", safe_mode_enabled)
    
    def enable_safe_mode(self) -> Dict[str, Any]:
        """Enable safe mode."""
        with self.lock:
            self.safe_mode_enabled = True
        logger.info("Safe mode enabled")
        return {"status": "ok", "safe_mode": True}
    
    def disable_safe_mode(self) -> Dict[str, Any]:
        """Disable safe mode."""
        with self.lock:
            self.safe_mode_enabled = False
        logger.warning("Safe mode disabled")
        return {"status": "ok", "safe_mode": False}
    
    def is_safe_mode_enabled(self) -> bool:
        """Check if safe mode is enabled."""
        with self.lock:
            return self.safe_mode_enabled
    
    def is_dangerous_action(self, action: str) -> bool:
        """Check if action is inherently dangerous."""
        return action in self.DANGEROUS_ACTIONS
    
    def contains_dangerous_pattern(self, text: str) -> bool:
        """Check if text contains dangerous patterns."""
        if not isinstance(text, str):
            return False
        
        text_lower = text.lower()
        for pattern in self.DANGEROUS_PATTERNS:
            if pattern.lower() in text_lower:
                logger.warning("Dangerous pattern detected: %s", pattern)
                return True
        return False
    
    def check_action_safety(self, action: str, params: Dict) -> tuple:
        """Check if action is safe to execute.
        
        Returns: (is_safe: bool, reason: str)
        """
        if not self.safe_mode_enabled:
            return True, None
        
        if not self.is_dangerous_action(action):
            return True, None
        
        # Check parameters for dangerous patterns
        for key, value in params.items():
            if isinstance(value, str):
                if self.contains_dangerous_pattern(value):
                    reason = f"Parameter '{key}' contains dangerous pattern"
                    logger.warning("Action %s blocked: %s", action, reason)
                    return False, reason
        
        return True, None
    
    def get_safety_status(self) -> Dict[str, Any]:
        """Get current safety status."""
        return {
            "status": "ok",
            "safe_mode_enabled": self.is_safe_mode_enabled(),
            "dangerous_patterns": len(self.DANGEROUS_PATTERNS),
            "dangerous_actions": list(self.DANGEROUS_ACTIONS)
        }
    
    def audit_action(self, action: str, params: Dict, result: Dict, 
                     blocked: bool = False) -> None:
        """Audit log an action execution."""
        if blocked:
            logger.warning("Action blocked - %s with params %s", action, params)
        else:
            logger.info("Action executed - %s | Result: %s", action, result.get('status', 'unknown'))
