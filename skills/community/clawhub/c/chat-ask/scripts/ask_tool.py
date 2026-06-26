#!/usr/bin/env python3
"""
Ask tool for OpenClaw chat-ask skill
Handles Q&A functionality
"""

import json
import sys
import datetime
from typing import Dict, Any, Optional

def process_question(question: str, detailed: bool = False) -> Dict[str, Any]:
    """
    Process a question and generate an answer
    """
    print(f"[ask-tool] Processing question: {question} (detailed: {detailed})", file=sys.stderr)
    
    # Base answers for common questions
    base_answers = {
        'hello': 'Hello! How can I help you today?',
        'hi': 'Hi there! What can I do for you?',
        'help': 'I can help you with various tasks. Try asking me about system status, files, or anything else you need.',
        'status': 'The system is running normally. All services are operational.',
        'time': f'Current time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        'weather': 'I need more information to check the weather. Please specify a location.',
        'openclaw': 'OpenClaw is a self-hosted AI assistant platform that gives you control over your AI interactions.',
        'default': f'You asked: "{question}". I\'m an OpenClaw assistant here to help you with various tasks.'
    }
    
    question_lower = question.lower()
    answer = base_answers['default']
    
    # Check for matching keywords
    for key, value in base_answers.items():
        if key != 'default' and key in question_lower:
            answer = value
            break
    
    # Add details if requested
    if detailed:
        answer = f"""{answer}

Additional details:
1. Question analyzed: "{question}"
2. Response generated at: {datetime.datetime.now().isoformat()}
3. Detailed mode: Enabled
4. Question length: {len(question)} characters
5. Contains common phrases: {any(phrase in question_lower for phrase in ['what', 'how', 'when', 'where', 'why', 'can', 'will'])}"""
    
    return {
        "status": "success",
        "answer": answer,
        "detailed": detailed,
        "timestamp": datetime.datetime.now().isoformat(),
        "tool": "ask"
    }

def main():
    """
    Main entry point for the ask tool
    """
    try:
        # Parse command line arguments
        if len(sys.argv) < 2:
            print(json.dumps({
                "status": "error",
                "error": "Missing arguments. Usage: ask_tool.py '<question>' [detailed]"
            }))
            sys.exit(1)
        
        question = sys.argv[1]
        detailed = len(sys.argv) > 2 and sys.argv[2].lower() == 'true'
        
        # Process the question
        result = process_question(question, detailed)
        
        # Output result as JSON
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": f"Ask tool error: {str(e)}"
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()