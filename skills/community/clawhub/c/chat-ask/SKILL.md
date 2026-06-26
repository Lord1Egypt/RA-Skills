---
name: chat-ask
description: Chat and ask functionality for OpenClaw
emoji: 💬
author: OpenClaw User
version: 1.0.0
license: MIT
requires:
  bins:
    - python3
tools:
  - name: chat
    description: Start or continue a chat conversation
    parameters:
      type: object
      properties:
        message:
          type: string
          description: The message to send in chat
        context:
          type: string
          description: Additional context for the conversation
          optional: true
      required: [message]
  - name: ask
    description: Ask a question to OpenClaw
    parameters:
      type: object
      properties:
        question:
          type: string
          description: The question to ask
        detailed:
          type: boolean
          description: Whether to provide a detailed answer
          optional: true
          default: false
      required: [question]
  - name: chat_history
    description: Manage chat history
    parameters:
      type: object
      properties:
        action:
          type: string
          description: Action to perform - 'get', 'clear', or 'summary'
          enum: [get, clear, summary]
          default: get
        limit:
          type: number
          description: Number of messages to retrieve
          optional: true
          default: 10
      required: [action]
---

# Chat/Ask Skill

A simple skill for handling chat conversations and Q&A with OpenClaw.

## Description

This skill provides tools for:
- Chat conversations with OpenClaw
- Asking questions and getting answers
- Managing chat history
- Simple conversation analysis

## Tools

### chat
Start or continue a chat conversation.

**Parameters:**
- `message` (string): The message to send in chat
- `context` (string, optional): Additional context for the conversation

**Example:**
```json
{
  "message": "Hello, how are you?",
  "context": "Just checking in"
}
```

### ask
Ask a question to OpenClaw.

**Parameters:**
- `question` (string): The question to ask
- `detailed` (boolean, optional): Whether to provide a detailed answer (default: false)

**Example:**
```json
{
  "question": "What is the weather like?",
  "detailed": true
}
```

### chat-history
Manage chat history.

**Parameters:**
- `action` (string): Action to perform - 'get', 'clear', or 'summary'
- `limit` (number, optional): Number of messages to retrieve (default: 10)

**Example:**
```json
{
  "action": "get",
  "limit": 5
}
```

## Usage

1. **Start a chat:**
   ```
   Use the chat tool to start a conversation
   ```

2. **Ask questions:**
   ```
   Use the ask tool for specific questions
   ```

3. **Manage history:**
   ```
   Use chat-history to review or clear conversations
   ```

## How to Call Tools

### chat tool
```bash
python3 scripts/chat_tool.py '<message>' '[context]'
```

**Example:**
```bash
python3 scripts/chat_tool.py 'Hello, how are you?' 'Just checking in'
```

### ask tool
```bash
python3 scripts/ask_tool.py '<question>' [detailed]
```

**Example:**
```bash
python3 scripts/ask_tool.py 'What is OpenClaw?' true
```

### chat_history tool
```bash
python3 scripts/chat_history_tool.py '<action>' [limit]
```

**Examples:**
```bash
# Get last 10 messages
python3 scripts/chat_history_tool.py 'get' 10

# Clear history
python3 scripts/chat_history_tool.py 'clear'

# Get summary
python3 scripts/chat_history_tool.py 'summary'
```

## Response Format

All tools return JSON with:
- `status`: "success" or "error"
- `timestamp`: ISO format timestamp
- `tool`: Tool name that was called
- Additional tool-specific fields

### chat response
```json
{
  "status": "success",
  "response": "I received your message...",
  "timestamp": "2026-03-16T14:30:00.000Z",
  "tool": "chat"
}
```

### ask response
```json
{
  "status": "success",
  "answer": "OpenClaw is a self-hosted AI assistant...",
  "detailed": true,
  "timestamp": "2026-03-16T14:30:00.000Z",
  "tool": "ask"
}
```

### chat_history response
```json
{
  "status": "success",
  "action": "get",
  "history": [...],
  "count": 5,
  "limit": 10,
  "total": 15
}
```

## Configuration

No special configuration required. The skill works out of the box.

## Notes

- Chat history is stored in memory during the session
- For persistent storage, consider integrating with a database
- The skill is designed for simple conversational interactions