#!/usr/bin/env python3
"""
Chat tool for OpenClaw chat-ask skill
Handles chat conversations
"""

import json
import sys
import datetime
from typing import Dict, Any, Optional

def process_chat(message: str, context: Optional[str] = None) -> Dict[str, Any]:
    """
    Process a chat message and generate a response
    """
    print(f"[chat-tool] Processing chat message: {message}", file=sys.stderr)
    
    responses = [
        f"I received your message: '{message}'. How can I assist you further?",
        f"Thanks for your message! '{message}' - is there anything specific you'd like to discuss?",
        f"Got it: '{message}'. I'm here to help! What would you like to know?",
        f"Message received: '{message}'. Let me know how I can assist you."
    ]
    
    import random
    response = random.choice(responses)
    
    if context:
        response = f"{response} (Context: {context})"
    
    return {
        "status": "success",
        "response": response,
        "timestamp": datetime.datetime.now().isoformat(),
        "tool": "chat"
    }

def main():
    """
    Main entry point for the chat tool
    """
    try:
        # Parse command line arguments
        if len(sys.argv) < 2:
            print(json.dumps({
                "status": "error",
                "error": "Missing arguments. Usage: chat_tool.py '<message>' '[context]'"
            }))
            sys.exit(1)
        
        message = sys.argv[1]
        context = sys.argv[2] if len(sys.argv) > 2 else None
        
        # Process the chat
        result = process_chat(message, context)
        
        # Output result as JSON
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": f"Chat tool error: {str(e)}"
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()