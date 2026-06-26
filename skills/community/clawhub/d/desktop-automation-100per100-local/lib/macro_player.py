"""
Macro Player Module

Load and replay recorded macros with safety and logging.
Thread-safe, robust error handling.
"""

import json
import logging
import os
import time
import threading
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class MacroPlayer:
    """Play recorded macros."""
    
    def __init__(self, action_manager):
        self.action_manager = action_manager
        self.lock = threading.Lock()
        self.is_playing = False
        self.stop_requested = False
        logger.info("MacroPlayer initialized")
    
    def load_macro(self, macro_path: str) -> Optional[List[Dict]]:
        """Load macro from JSON file."""
        if not os.path.exists(macro_path):
            logger.error("Macro file not found: %s", macro_path)
            return None
        
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro = json.load(f)
            logger.info("Loaded macro: %s (%d events)", macro_path, len(macro.get('events', [])))
            return macro
        except Exception as e:
            logger.error("Failed to load macro: %s", str(e))
            return None
    
    def play_macro(self, macro_path: str, speed: float = 1.0, 
                   dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Play a recorded macro."""
        macro = self.load_macro(macro_path)
        if not macro:
            return {"status": "error", "message": f"Failed to load macro: {macro_path}"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] play_macro: %s (speed=%.2f)", macro_path, speed)
                return {"status": "ok", "dry_run": True, "events": len(macro.get('events', []))}
            
            with self.lock:
                self.is_playing = True
                self.stop_requested = False
            
            events = macro.get('events', [])
            executed = 0
            errors = []
            
            for event in events:
                if self.stop_requested:
                    logger.info("Macro playback stopped by user")
                    break
                
                try:
                    action = event.get('action')
                    params = event.get('params', {})
                    wait = event.get('wait', 0)
                    
                    # Apply speed modifier to waits
                    if wait > 0:
                        time.sleep(wait / speed)
                    
                    # Execute action
                    if hasattr(self.action_manager, action):
                        result = getattr(self.action_manager, action)(**params)
                        if result.get('status') != 'ok':
                            errors.append(f"Event {executed}: {action} failed - {result.get('message')}")
                        executed += 1
                    else:
                        errors.append(f"Event {executed}: unknown action '{action}'")
                except Exception as e:
                    errors.append(f"Event {executed}: {str(e)}")
            
            with self.lock:
                self.is_playing = False
            
            logger.info("Macro playback completed: %d/%d events", executed, len(events))
            return {
                "status": "ok",
                "executed": executed,
                "total": len(events),
                "errors": errors
            }
        except Exception as e:
            logger.error("play_macro failed: %s", str(e))
            with self.lock:
                self.is_playing = False
            return {"status": "error", "message": str(e)}
    
    def stop_macro(self) -> Dict[str, Any]:
        """Stop current macro playback."""
        with self.lock:
            self.stop_requested = True
        logger.info("Stop requested for macro")
        return {"status": "ok", "message": "Stop requested"}
    
    def play_macro_with_subroutines(self, macro_path: str, speed: float = 1.0, 
                                    sub_macros_dir: Optional[str] = None,
                                    dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """Play macro with support for nested call_macro events."""
        macro = self.load_macro(macro_path)
        if not macro:
            return {"status": "error", "message": f"Failed to load macro: {macro_path}"}
        
        try:
            if dry_run:
                logger.info("[DRY RUN] play_macro_with_subroutines: %s", macro_path)
                return {"status": "ok", "dry_run": True}
            
            def process_event(event: Dict, depth: int = 0) -> tuple:
                """Process event recursively."""
                action = event.get('action')
                params = event.get('params', {})
                
                if action == 'call_macro':
                    sub_name = params.get('macro_name')
                    if sub_macros_dir:
                        sub_path = os.path.join(sub_macros_dir, sub_name)
                        return self.play_macro(sub_path, speed=speed)
                else:
                    # Regular action
                    wait = event.get('wait', 0)
                    if wait > 0:
                        time.sleep(wait / speed)
                    
                    if hasattr(self.action_manager, action):
                        return getattr(self.action_manager, action)(**params)
                
                return {"status": "error", "message": f"Unknown action: {action}"}
            
            with self.lock:
                self.is_playing = True
                self.stop_requested = False
            
            events = macro.get('events', [])
            executed = 0
            errors = []
            
            for event in events:
                if self.stop_requested:
                    break
                result = process_event(event)
                if result.get('status') == 'ok':
                    executed += 1
                else:
                    errors.append(f"Event {executed}: {result.get('message')}")
            
            with self.lock:
                self.is_playing = False
            
            return {
                "status": "ok",
                "executed": executed,
                "total": len(events),
                "errors": errors
            }
        except Exception as e:
            logger.error("play_macro_with_subroutines failed: %s", str(e))
            with self.lock:
                self.is_playing = False
            return {"status": "error", "message": str(e)}
