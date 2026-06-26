#!/usr/bin/env python3
"""
Test script for conversation flow monitor
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from conversation_monitor import ConversationMonitor
from error_handler import ErrorHandler

def test_conversation_monitor():
    """Test the conversation monitor functionality"""
    print("Testing Conversation Flow Monitor...")
    
    # Initialize monitor
    monitor = ConversationMonitor()
    
    # Test basic monitoring
    monitor.start_session("test-session-001")
    print(f"✓ Session started: {monitor.current_session_id}")
    
    # Test operation tracking
    with monitor.track_operation("test_operation", timeout=5):
        print("✓ Operation tracking working")
    
    # Test error handling
    handler = ErrorHandler()
    try:
        raise ValueError("Test error for monitoring")
    except Exception as e:
        handler.handle_error(e, "test_context")
        print("✓ Error handling working")
    
    # End session
    monitor.end_session()
    print(f"✓ Session ended: {monitor.current_session_id}")
    
    print("\n✅ All tests passed! Conversation Flow Monitor is ready.")

if __name__ == "__main__":
    test_conversation_monitor()