#!/usr/bin/env python3
"""
Conversation Flow Monitor - Prevents stuck conversations and provides recovery mechanisms.

This script monitors conversation health, detects potential hang conditions,
and provides graceful error handling with fallback strategies.
"""

import os
import sys
import time
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

# Configure logging
LOG_DIR = os.path.expanduser("~/.copaw/.logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'conversation_monitor.log')),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class ConversationMonitor:
    """Monitors conversation flow and prevents hanging operations."""
    
    def __init__(self):
        self.operation_start_time = None
        self.current_operation = None
        self.timeout_threshold = 30  # seconds
        self.recovery_attempts = 0
        self.max_recovery_attempts = 3
        
    def start_operation(self, operation_name: str, timeout: int = None):
        """Start monitoring a potentially long-running operation."""
        self.operation_start_time = time.time()
        self.current_operation = operation_name
        self.timeout_threshold = timeout or self.timeout_threshold
        
        logger.info(f"Started operation: {operation_name} (timeout: {self.timeout_threshold}s)")
        
    def check_timeout(self) -> bool:
        """Check if current operation has exceeded timeout threshold."""
        if not self.operation_start_time or not self.current_operation:
            return False
            
        elapsed = time.time() - self.operation_start_time
        if elapsed > self.timeout_threshold:
            logger.warning(f"Operation '{self.current_operation}' exceeded timeout ({elapsed:.1f}s > {self.timeout_threshold}s)")
            return True
        return False
        
    def end_operation(self, success: bool = True):
        """End current operation monitoring."""
        if self.current_operation:
            elapsed = time.time() - self.operation_start_time if self.operation_start_time else 0
            status = "SUCCESS" if success else "FAILED"
            logger.info(f"Ended operation: {self.current_operation} ({status}, {elapsed:.1f}s)")
            
        self.operation_start_time = None
        self.current_operation = None
        
    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle errors gracefully with recovery options."""
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'operation': self.current_operation,
            'recovery_attempt': self.recovery_attempts + 1,
            'max_attempts': self.max_recovery_attempts
        }
        
        logger.error(f"Error in {context}: {error}")
        
        # Determine if we should attempt recovery
        if self.recovery_attempts < self.max_recovery_attempts:
            self.recovery_attempts += 1
            error_info['recovery_action'] = 'attempting_recovery'
            logger.info(f"Attempting recovery #{self.recovery_attempts}")
        else:
            error_info['recovery_action'] = 'max_attempts_reached'
            logger.error("Max recovery attempts reached, requiring user intervention")
            
        return error_info
        
    def get_conversation_health(self) -> Dict[str, Any]:
        """Get current conversation health status."""
        health = {
            'timestamp': datetime.now().isoformat(),
            'current_operation': self.current_operation,
            'operation_elapsed': time.time() - self.operation_start_time if self.operation_start_time else 0,
            'is_healthy': not self.check_timeout(),
            'recovery_attempts': self.recovery_attempts,
            'max_recovery_attempts': self.max_recovery_attempts
        }
        
        if health['current_operation']:
            health['timeout_threshold'] = self.timeout_threshold
            
        return health

    def track_operation(self, operation_name: str, timeout: Optional[int] = None):
        """Context manager for monitoring operations with automatic cleanup.
        
        Usage:
            with monitor.track_operation("browser_navigation", timeout=45):
                # Your operation here
                result = browser_use(action="open", url="https://example.com")
        """
        self.start_operation(operation_name, timeout)
        return self
        
    def __enter__(self):
        """Enter the runtime context for the operation."""
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context and handle any exceptions."""
        if exc_type is None:
            # No exception occurred
            self.end_operation(success=True)
            return False
        else:
            # An exception occurred
            error = exc_value
            context = f"operation:{self.current_operation}"
            self.handle_error(error, context)
            self.end_operation(success=False)
            # Return False to propagate the exception
            return False

def create_safe_tool_wrapper(tool_func, tool_name: str, default_timeout: int = 30):
    """Create a safe wrapper for tool functions with timeout and error handling."""
    def safe_wrapper(*args, **kwargs):
        monitor = ConversationMonitor()
        monitor.start_operation(tool_name, timeout=default_timeout)
        
        try:
            result = tool_func(*args, **kwargs)
            monitor.end_operation(success=True)
            return result
        except Exception as e:
            error_info = monitor.handle_error(e, context=f"tool_call:{tool_name}")
            
            # Return structured error instead of letting it propagate
            return {
                'error': True,
                'tool_name': tool_name,
                'error_details': error_info,
                'suggested_action': 'Check logs and retry with different parameters or shorter timeout'
            }
            
    return safe_wrapper

def monitor_conversation_flow():
    """Main monitoring function that can be integrated into conversation loops."""
    monitor = ConversationMonitor()
    
    # This would be called periodically during conversation processing
    health = monitor.get_conversation_health()
    
    if not health['is_healthy']:
        logger.warning("Conversation flow appears unhealthy - consider intervention")
        return False
        
    return True

# Example usage and integration points
if __name__ == "__main__":
    # Test the monitor
    monitor = ConversationMonitor()
    
    # Simulate a long operation
    monitor.start_operation("test_browser_navigation", timeout=5)
    time.sleep(2)  # Shorter than timeout
    monitor.end_operation(success=True)
    
    print("Monitor test completed successfully")