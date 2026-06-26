#!/usr/bin/env python3
"""
Integration test for conversation flow monitor skill.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from conversation_monitor import ConversationMonitor
from error_handler import ConversationErrorHandler

def test_basic_functionality():
    """Test basic monitoring and error handling."""
    print("Testing Conversation Flow Monitor Integration...")
    
    # Test monitor
    monitor = ConversationMonitor()
    monitor.start_operation("integration_test", timeout=10)
    
    # Simulate work
    import time
    time.sleep(1)
    
    health = monitor.get_conversation_health()
    assert health['is_healthy'], "Health check failed"
    print("✅ Basic monitoring works")
    
    # Test error handler
    handler = ConversationErrorHandler()
    error_summary = handler.get_error_summary()
    assert error_summary['total_errors'] == 0, "Expected no errors initially"
    print("✅ Error handler initialized correctly")
    
    print("\n🎉 All integration tests passed!")
    return True

if __name__ == "__main__":
    test_basic_functionality()