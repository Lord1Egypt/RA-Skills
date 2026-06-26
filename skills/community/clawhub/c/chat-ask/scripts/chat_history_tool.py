#!/usr/bin/env python3
"""
Chat history tool for OpenClaw chat-ask skill
Manages chat history
"""

import json
import sys
import datetime
from typing import Dict, Any, List

# Simple in-memory chat history storage
# In a real implementation, this would be persisted to a database
chat_history: List[Dict[str, Any]] = []

def get_chat_history(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get chat history with limit
    """
    return chat_history[-limit:] if chat_history else []

def clear_chat_history() -> None:
    """
    Clear all chat history
    """
    global chat_history
    chat_history = []

def add_to_history(role: str, content: str, tool: str = "unknown") -> None:
    """
    Add a message to chat history
    """
    chat_history.append({
        "role": role,
        "content": content,
        "tool": tool,
        "timestamp": datetime.datetime.now().isoformat(),
        "id": len(chat_history) + 1
    })

def get_history_summary() -> Dict[str, Any]:
    """
    Generate a summary of chat history
    """
    if not chat_history:
        return {
            "total_messages": 0,
            "summary": "No chat history available",
            "first_message": None,
            "last_message": None
        }
    
    # Simple summary based on message types
    user_messages = [msg for msg in chat_history if msg.get("role") == "user"]
    assistant_messages = [msg for msg in chat_history if msg.get("role") == "assistant"]
    
    # Extract common topics (simplified)
    all_content = " ".join([msg.get("content", "") for msg in chat_history])
    common_words = ["help", "question", "chat", "ask", "status", "time", "weather"]
    topics = [word for word in common_words if word in all_content.lower()]
    
    return {
        "total_messages": len(chat_history),
        "user_messages": len(user_messages),
        "assistant_messages": len(assistant_messages),
        "first_message": chat_history[0] if chat_history else None,
        "last_message": chat_history[-1] if chat_history else None,
        "common_topics": topics[:5],  # Top 5 topics
        "time_span": {
            "start": chat_history[0].get("timestamp") if chat_history else None,
            "end": chat_history[-1].get("timestamp") if chat_history else None
        },
        "summary": f"Chat history contains {len(chat_history)} messages with topics: {', '.join(topics[:3]) if topics else 'various'}"
    }

def process_history_action(action: str, limit: int = 10) -> Dict[str, Any]:
    """
    Process chat history actions
    """
    print(f"[history-tool] Processing action: {action} (limit: {limit})", file=sys.stderr)
    
    if action == "get":
        history = get_chat_history(limit)
        return {
            "status": "success",
            "action": "get",
            "history": history,
            "count": len(history),
            "limit": limit,
            "total": len(chat_history)
        }
    
    elif action == "clear":
        clear_chat_history()
        return {
            "status": "success",
            "action": "clear",
            "message": "Chat history cleared successfully",
            "cleared_count": len(chat_history)  # This would be the count before clearing
        }
    
    elif action == "summary":
        summary = get_history_summary()
        return {
            "status": "success",
            "action": "summary",
            "summary": summary
        }
    
    else:
        return {
            "status": "error",
            "error": f"Unknown action: {action}. Valid actions: get, clear, summary"
        }

def main():
    """
    Main entry point for the chat history tool
    """
    try:
        # Parse command line arguments
        if len(sys.argv) < 2:
            print(json.dumps({
                "status": "error",
                "error": "Missing arguments. Usage: chat_history_tool.py '<action>' [limit]"
            }))
            sys.exit(1)
        
        action = sys.argv[1]
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        
        # Add some sample data for testing if history is empty
        if not chat_history and action in ["get", "summary"]:
            # Add sample messages
            add_to_history("user", "Hello, how are you?", "chat")
            add_to_history("assistant", "I'm doing well, thank you! How can I help you today?", "chat")
            add_to_history("user", "What time is it?", "ask")
            add_to_history("assistant", f"Current time: {datetime.datetime.now().strftime('%H:%M:%S')}", "ask")
        
        # Process the action
        result = process_history_action(action, limit)
        
        # Output result as JSON
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": f"Chat history tool error: {str(e)}"
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()