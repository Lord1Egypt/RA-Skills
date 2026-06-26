#!/usr/bin/env python3
"""
Error Handling Utilities for Conversation Flow Monitoring
Provides robust error handling, timeout management, and recovery strategies.
"""

import asyncio
import logging
import time
from typing import Any, Callable, Optional, Dict, List
from pathlib import Path

class ConversationErrorHandler:
    """Comprehensive error handler for conversation flow issues."""
    
    def __init__(self, max_retries: int = 3, default_timeout: int = 30):
        self.max_retries = max_retries
        self.default_timeout = default_timeout
        self.error_log = []
        self.recovery_strategies = {}
        
    async def execute_with_timeout(self, 
                                 func: Callable, 
                                 timeout: Optional[int] = None,
                                 *args, **kwargs) -> Any:
        """
        Execute a function with timeout protection.
        
        Args:
            func: Function to execute
            timeout: Timeout in seconds (defaults to self.default_timeout)
            *args, **kwargs: Arguments to pass to func
            
        Returns:
            Result of function execution
            
        Raises:
            asyncio.TimeoutError: If function times out
            Exception: If function raises an exception
        """
        if timeout is None:
            timeout = self.default_timeout
            
        try:
            if asyncio.iscoroutinefunction(func):
                result = await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
            else:
                # For sync functions, run in thread pool
                loop = asyncio.get_event_loop()
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, lambda: func(*args, **kwargs)), 
                    timeout=timeout
                )
            return result
        except asyncio.TimeoutError as e:
            error_info = {
                'timestamp': time.time(),
                'error_type': 'timeout',
                'function': func.__name__,
                'timeout': timeout,
                'args': str(args)[:100],  # Truncate long args
                'kwargs': str(kwargs)[:100]
            }
            self.error_log.append(error_info)
            logging.warning(f"Timeout in {func.__name__}: {e}")
            raise
        except Exception as e:
            error_info = {
                'timestamp': time.time(),
                'error_type': 'exception',
                'function': func.__name__,
                'exception': str(e),
                'args': str(args)[:100],
                'kwargs': str(kwargs)[:100]
            }
            self.error_log.append(error_info)
            logging.error(f"Exception in {func.__name__}: {e}")
            raise
    
    async def execute_with_retry(self,
                                func: Callable,
                                retry_strategy: Optional[Dict] = None,
                                *args, **kwargs) -> Any:
        """
        Execute a function with retry logic.
        
        Args:
            func: Function to execute
            retry_strategy: Dict with retry configuration
            *args, **kwargs: Arguments to pass to func
            
        Returns:
            Result of function execution
        """
        if retry_strategy is None:
            retry_strategy = {'max_retries': self.max_retries, 'backoff': 1}
            
        max_retries = retry_strategy.get('max_retries', self.max_retries)
        backoff = retry_strategy.get('backoff', 1)
        
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return await self.execute_with_timeout(func, *args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < max_retries:
                    wait_time = backoff * (2 ** attempt)  # Exponential backoff
                    logging.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)
                else:
                    logging.error(f"All {max_retries + 1} attempts failed")
                    break
        
        # Log final failure
        error_info = {
            'timestamp': time.time(),
            'error_type': 'retry_exhausted',
            'function': func.__name__,
            'attempts': max_retries + 1,
            'final_exception': str(last_exception)
        }
        self.error_log.append(error_info)
        raise last_exception
    
    def register_recovery_strategy(self, error_pattern: str, strategy: Callable):
        """Register a recovery strategy for specific error patterns."""
        self.recovery_strategies[error_pattern] = strategy
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of all logged errors."""
        if not self.error_log:
            return {'total_errors': 0, 'error_types': {}}
            
        error_types = {}
        for error in self.error_log:
            error_type = error['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
            
        return {
            'total_errors': len(self.error_log),
            'error_types': error_types,
            'recent_errors': self.error_log[-5:]  # Last 5 errors
        }
    
    def clear_errors(self):
        """Clear the error log."""
        self.error_log.clear()

# Global error handler instance
error_handler = ConversationErrorHandler()

def safe_tool_call(tool_func: Callable, timeout: int = 30, max_retries: int = 2):
    """
    Decorator for making tool calls safer with timeout and retry protection.
    
    Usage:
    @safe_tool_call(timeout=45, max_retries=3)
    def my_tool_function():
        # tool implementation
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            retry_strategy = {'max_retries': max_retries, 'backoff': 1}
            return await error_handler.execute_with_retry(
                func, retry_strategy, *args, **kwargs
            )
        return wrapper
    return decorator

# Common error patterns and recovery strategies
COMMON_ERROR_PATTERNS = {
    'browser_timeout': lambda: "Browser operation timed out. Consider using shorter operations or checking page load.",
    'file_not_found': lambda: "File not found. Verify path exists before operation.",
    'skill_registration_failed': lambda: "Skill registration failed. Check YAML front matter and required fields.",
    'network_timeout': lambda: "Network request timed out. Try again with longer timeout or check connectivity.",
    'memory_exceeded': lambda: "Memory usage high. Consider breaking task into smaller steps."
}

def analyze_conversation_stuck_pattern(error_logs: List[Dict]) -> str:
    """Analyze error logs to identify why conversation got stuck."""
    if not error_logs:
        return "No errors detected"
    
    # Look for timeout patterns
    timeouts = [e for e in error_logs if e.get('error_type') == 'timeout']
    if timeouts:
        return f"Conversation likely stuck due to {len(timeouts)} timeout(s) in browser/file operations"
    
    # Look for skill registration errors
    skill_errors = [e for e in error_logs if 'skill' in e.get('function', '').lower()]
    if skill_errors:
        return "Conversation stuck due to skill registration/dependency issues"
    
    # Look for file operation errors
    file_errors = [e for e in error_logs if 'file' in e.get('function', '').lower() or 'read' in e.get('function', '').lower()]
    if file_errors:
        return "Conversation stuck due to file system access issues"
    
    return f"Conversation stuck due to {len(error_logs)} unclassified errors"
