"""
agent_bridge.py — Isaac/Hermes shared filesystem message bus.

Usage (Isaac side):
    from agent_bridge import AgentBridge
    bridge = AgentBridge(agent_id="isaac")
    
    # Send a message to Hermes
    bridge.send("hermes", subject="Research request", body="Please analyze X...")
    
    # Check for new messages from Hermes
    messages = bridge.receive()
    for msg in messages:
        print(msg["from"], msg["subject"], msg["body"])
        bridge.mark_processed(msg)
"""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional


SHARED_DIR = Path(__file__).parent


class AgentBridge:
    def __init__(self, agent_id: str, shared_dir: Path = None):
        self.agent_id = agent_id
        self.shared_dir = shared_dir or SHARED_DIR
        self.inbox = self.shared_dir / f"{agent_id}-inbox"
        self.processed = self.shared_dir / "processed"
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.processed.mkdir(parents=True, exist_ok=True)

    def send(
        self,
        to: str,
        subject: str,
        body: str,
        thread_id: str = None,
        reply_to: str = None,
    ) -> str:
        """Write a message to the recipient's inbox. Returns message_id."""
        message_id = str(uuid.uuid4())[:8]
        ts = datetime.now(timezone.utc).isoformat()
        msg = {
            "message_id": message_id,
            "from": self.agent_id,
            "to": to,
            "subject": subject,
            "body": body,
            "timestamp": ts,
            "thread_id": thread_id or message_id,
            "reply_to": reply_to,
            "status": "pending",
        }
        outbox = self.shared_dir / f"{to}-inbox"
        outbox.mkdir(parents=True, exist_ok=True)
        filename = f"{ts.replace(':', '-')}_{message_id}.json"
        (outbox / filename).write_text(json.dumps(msg, indent=2))
        return message_id

    def receive(self) -> List[Dict[str, Any]]:
        """Read all pending messages from inbox. Returns list of message dicts."""
        messages = []
        for f in sorted(self.inbox.glob("*.json")):
            try:
                msg = json.loads(f.read_text())
                msg["_file"] = str(f)
                messages.append(msg)
            except Exception:
                pass
        return messages

    def mark_processed(self, msg: Dict[str, Any]) -> None:
        """Move a message file to processed/ after handling."""
        f = Path(msg.get("_file", ""))
        if f.exists():
            dest = self.processed / f.name
            f.rename(dest)

    def reply(self, original: Dict[str, Any], body: str) -> str:
        """Reply to a message. Returns new message_id."""
        return self.send(
            to=original["from"],
            subject=f"Re: {original['subject']}",
            body=body,
            thread_id=original.get("thread_id"),
            reply_to=original["message_id"],
        )

    def pending_count(self) -> int:
        return len(list(self.inbox.glob("*.json")))
