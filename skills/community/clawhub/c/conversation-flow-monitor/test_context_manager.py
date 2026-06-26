#!/usr/bin/env python3
"""
Test script for the track_operation context manager.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from conversation_monitor import ConversationMonitor

def test_context_manager():
    """Test the track_operation context manager."""
    print("Testing track_operation context manager...")
    
    monitor = ConversationMonitor()
    
    # Test successful operation
    try:
        with monitor.track_operation("test_success", timeout=5):
            print("   ✓ Inside context manager")
            # Simulate work
            import time
            time.sleep(1)
        print("   ✓ Context manager exited successfully")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False
    
    # Test operation with exception
    try:
        with monitor.track_operation("test_exception", timeout=5):
            print("   ✓ Inside context manager (will raise exception)")
            raise ValueError("Test exception")
        print("   ❌ Should not reach here")
        return False
    except ValueError as e:
        print(f"   ✓ Exception properly propagated: {e}")
    except Exception as e:
        print(f"   ❌ Wrong exception type: {e}")
        return False
    
    print("✅ All context manager tests passed!")
    return True

if __name__ == "__main__":
    success = test_context_manager()
    sys.exit(0 if success else 1)