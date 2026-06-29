# Chat Feature PRD

## Overview

Add real-time chat to the dashboard. Supports **1:1** and **group** conversations.

### Target Users

- Dashboard users who need team communication
- Customer support agents handling live chats

## Features

### Core Features

1. Real-time message delivery via WebSocket
2. Message history with infinite scroll
3. Typing indicators and read receipts
4. File/image sharing (max 25MB)

### Premium Features

- Video calling (WebRTC)
- Message search with filters
- Custom emoji sets
- Chat analytics dashboard

## API Design

| Endpoint        | Method | Auth Required | Rate Limit | Description          |
|-----------------|--------|---------------|------------|----------------------|
| /chat/send      | POST   | Yes           | 10/s       | Send a message       |
| /chat/history   | GET    | Yes           | 30/s       | Get chat history     |
| /chat/rooms     | GET    | Yes           | 30/s       | List user's rooms    |
| /chat/upload    | POST   | Yes           | 5/min      | Upload attachment    |

## Technical Architecture

The chat service consists of three components:

```python
# Message handler
class ChatHandler:
    def __init__(self, ws_manager, db):
        self.ws_manager = ws_manager
        self.db = db

    async def handle_message(self, user_id: str, room_id: str, content: str):
        """Process and broadcast a chat message."""
        msg = await self.db.save_message(user_id, room_id, content)
        await self.ws_manager.broadcast(room_id, msg)
        return msg
```

## Data Model

> **Important:** All messages must be encrypted at rest and in transit.

Message schema:
- `id`: UUID (primary key)
- `room_id`: UUID (foreign key)
- `sender_id`: UUID (foreign key)
- `content`: text (encrypted)
- `created_at`: timestamp
- `edited_at`: timestamp (nullable)

## Timeline

- **Alpha**: Week 1-2 (core messaging)
- **Beta**: Week 3-4 (file sharing, search)
- **GA**: Week 5 (all features, bug fixes)

## Success Metrics

- Message delivery latency < 200ms (P99)
- 99.95% uptime SLA
- User satisfaction score > 4.5/5
