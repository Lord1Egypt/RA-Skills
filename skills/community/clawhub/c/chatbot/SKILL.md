---
name: senseaudio-voice-chatbot
description: Build real-time voice chatbot applications with natural conversation flow and customizable personalities. Use when users want to create voice assistants, conversational AI, or interactive voice agents.
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: API_KEY
homepage: https://senseaudio.cn
source: https://github.com/anthropics/skills
---

# SenseAudio Voice Chatbot

Build real-time voice chatbot applications with natural conversation flow, emotion recognition, and customizable personalities.

## What This Skill Does

- Create voice-enabled chatbot applications
- Support real-time voice dialogue with low latency
- Enable multi-turn conversations with context
- Customize chatbot personality and knowledge
- Integrate with existing applications

## Implementation Guide

### Step 1: Get Available Agents

```python
import requests

def get_available_agents(page=1, size=10):
    url = "https://api.senseaudio.cn/v1/realtime/agents"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"page": page, "size": size}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example response:
# {
#   "total": 10,
#   "list": [
#     {
#       "id": "690f53770e9d9d60d98ba7a8",
#       "title": "Customer Service Agent",
#       "avatar": "https://example.com/avatar.jpg",
#       "intro": "Professional customer service assistant"
#     }
#   ]
# }
```

### Step 2: Create Dialogue Session

```python
def create_dialogue_session(agent_id, new_dialogue=True, conv_id=None):
    url = "https://api.senseaudio.cn/v1/realtime/invoke"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "agent_id": agent_id,
        "new_dialogue": new_dialogue
    }

    if not new_dialogue and conv_id:
        payload["conv_id"] = conv_id

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Returns:
# {
#   "conv_id": "9b8260e2-19d9-4609-abe7-3b74ac16b677",
#   "app_id": "d4432b04117aj77r7755c2d8e86e140b",
#   "room_id": "lO81loRAfmUMFIwY",
#   "room_user_id": 360706506,
#   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
# }
```

### Step 3: Connect to Real-Time Voice

```python
import asyncio
import websockets
import json

async def voice_chatbot_session(room_id, token, app_id):
    # Use WebRTC or WebSocket for real-time audio
    # This is a simplified example

    session_info = {
        "room_id": room_id,
        "token": token,
        "app_id": app_id
    }

    # Connect to voice service
    # Implementation depends on the real-time communication protocol
    # Typically uses WebRTC for browser-based applications

    return session_info
```

### Step 4: Manage Conversation State

```python
class VoiceChatbot:
    def __init__(self, agent_id, api_key):
        self.agent_id = agent_id
        self.api_key = api_key
        self.conv_id = None
        self.room_id = None
        self.session_active = False

    def start_conversation(self):
        """Start a new conversation"""
        result = create_dialogue_session(
            agent_id=self.agent_id,
            new_dialogue=True
        )

        self.conv_id = result["conv_id"]
        self.room_id = result["room_id"]
        self.session_active = True

        return result

    def continue_conversation(self):
        """Continue existing conversation"""
        if not self.conv_id:
            raise ValueError("No active conversation to continue")

        result = create_dialogue_session(
            agent_id=self.agent_id,
            new_dialogue=False,
            conv_id=self.conv_id
        )

        self.room_id = result["room_id"]
        return result

    def check_status(self):
        """Check if agent is running"""
        url = "https://api.senseaudio.cn/v1/realtime/status"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"room_id": self.room_id}

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def end_conversation(self):
        """Stop the agent"""
        url = "https://api.senseaudio.cn/v1/realtime/leave"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"room_id": self.room_id}

        response = requests.post(url, headers=headers, json=payload)
        self.session_active = False
        return response.json()
```

## Advanced Features

### Web-Based Voice Chatbot

```html
<!DOCTYPE html>
<html>
<head>
    <title>Voice Chatbot</title>
</head>
<body>
    <div id="chatbot">
        <button id="startBtn">Start Conversation</button>
        <button id="stopBtn" disabled>Stop Conversation</button>
        <div id="status">Ready</div>
    </div>

    <script>
        let chatbot = null;
        let roomId = null;

        document.getElementById('startBtn').onclick = async () => {
            const response = await fetch('/api/start-chatbot', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({agent_id: 'YOUR_AGENT_ID'})
            });

            const data = await response.json();
            roomId = data.room_id;

            // Initialize WebRTC connection
            await initializeVoiceConnection(data);

            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            document.getElementById('status').textContent = 'Connected';
        };

        document.getElementById('stopBtn').onclick = async () => {
            await fetch('/api/stop-chatbot', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({room_id: roomId})
            });

            document.getElementById('startBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
            document.getElementById('status').textContent = 'Disconnected';
        };

        async function initializeVoiceConnection(sessionData) {
            // WebRTC setup code here
            // Use sessionData.token for authentication
        }
    </script>
</body>
</html>
```

### Multi-User Support

```python
class ChatbotManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.active_sessions = {}

    def create_session(self, user_id, agent_id):
        chatbot = VoiceChatbot(agent_id, self.api_key)
        session_info = chatbot.start_conversation()

        self.active_sessions[user_id] = {
            "chatbot": chatbot,
            "session_info": session_info,
            "started_at": datetime.now()
        }

        return session_info

    def get_session(self, user_id):
        return self.active_sessions.get(user_id)

    def end_session(self, user_id):
        if user_id in self.active_sessions:
            session = self.active_sessions[user_id]
            session["chatbot"].end_conversation()
            del self.active_sessions[user_id]
```

### Conversation Analytics

```python
def track_conversation_metrics(conv_id, room_id):
    metrics = {
        "conv_id": conv_id,
        "room_id": room_id,
        "start_time": datetime.now(),
        "end_time": None,
        "duration": None,
        "user_messages": 0,
        "agent_responses": 0
    }

    return metrics

def update_metrics(metrics, event_type):
    if event_type == "user_message":
        metrics["user_messages"] += 1
    elif event_type == "agent_response":
        metrics["agent_responses"] += 1
    elif event_type == "session_end":
        metrics["end_time"] = datetime.now()
        metrics["duration"] = (metrics["end_time"] - metrics["start_time"]).total_seconds()

    return metrics
```

## Use Cases

### Customer Service Bot

```python
def create_customer_service_bot(agent_id):
    """Create a customer service voice bot"""

    chatbot = VoiceChatbot(agent_id, API_KEY)

    # Start conversation
    session = chatbot.start_conversation()

    # Monitor status
    while chatbot.session_active:
        status = chatbot.check_status()
        if status["status"] == "STOPPED":
            break

        time.sleep(5)

    return session
```

### Educational Assistant

```python
def create_learning_assistant(agent_id, student_id):
    """Create personalized learning assistant"""

    chatbot = VoiceChatbot(agent_id, API_KEY)

    # Start new lesson
    session = chatbot.start_conversation()

    # Track learning progress
    metrics = track_conversation_metrics(
        session["conv_id"],
        session["room_id"]
    )

    return session, metrics
```

### Companion Bot

```python
def create_companion_bot(agent_id, user_id):
    """Create emotional support companion"""

    chatbot = VoiceChatbot(agent_id, API_KEY)

    # Continue previous conversation if exists
    if has_previous_conversation(user_id):
        conv_id = get_previous_conv_id(user_id)
        session = chatbot.continue_conversation()
    else:
        session = chatbot.start_conversation()

    return session
```

## Error Handling

```python
def safe_chatbot_operation(operation, *args, **kwargs):
    try:
        return operation(*args, **kwargs)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            if "400087" in str(e.response.content):
                return {"error": "Insufficient quota"}
            return {"error": "Invalid parameters"}
        elif e.response.status_code == 401:
            return {"error": "Unauthorized"}
        elif e.response.status_code == 404:
            return {"error": "Conversation not found"}
        else:
            return {"error": f"HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
```

## Output Format

- Session credentials (room_id, token)
- Conversation ID for continuity
- Status information
- Analytics and metrics

## Tips for Best Results

- Always check agent status before operations
- Properly end sessions to free resources
- Handle network interruptions gracefully
- Store conv_id for conversation continuity
- Monitor quota usage
- Implement timeout mechanisms

## Example Usage

**User request**: "Create a voice chatbot for customer support"

**Skill actions**:
1. Get list of available agents
2. Select appropriate customer service agent
3. Create dialogue session
4. Set up WebRTC connection
5. Implement conversation management
6. Add status monitoring
7. Provide integration code

## Reference

See SenseAudio Agent API documentation in `references/` directory.
