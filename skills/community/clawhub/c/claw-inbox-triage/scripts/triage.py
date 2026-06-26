#!/usr/bin/env python3
"""
Inbox Triage - Automated message categorization and prioritization

Usage:
    python triage.py --input messages.json --output digest.md
    python triage.py --input messages.json --draft-responses
"""

import json
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Configuration
CONFIG_PATH = Path.home() / ".inbox-triage" / "config.yaml"
CORRECTIONS_PATH = Path.home() / ".inbox-triage" / "corrections.log"


class Message:
    """Represents a single message to be categorized."""
    
    def __init__(self, content: str, sender: str = "unknown", 
                 timestamp: str = None, subject: str = None):
        self.content = content
        self.sender = sender
        self.timestamp = timestamp or datetime.now().isoformat()
        self.subject = subject or "No subject"
        self.priority: Optional[str] = None
        self.drafted_response: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        return cls(
            content=data.get("content", ""),
            sender=data.get("sender", "unknown"),
            timestamp=data.get("timestamp"),
            subject=data.get("subject")
        )


class InboxTriage:
    """Main triage engine."""
    
    def __init__(self):
        self.config = self._load_config()
        self.corrections = self._load_corrections()
        
        # Priority scoring weights (tune based on corrections)
        self.weights = {
            "urgent_keywords": 3,
            "question_patterns": 2,
            "spam_keywords": 2,
            "notification_patterns": 1.5
        }
    
    def _load_config(self) -> dict:
        """Load configuration or return defaults."""
        defaults = {
            "sources": ["signal", "telegram"],
            "rules": {
                "urgent_keywords": ["asap", "urgent", "immediately", "deadline"],
                "spam_keywords": ["discount", "sale", "promo"],
                "question_patterns": ["can you", "please help", "need response"],
                "notification_patterns": ["password", "login", "verification"]
            }
        }
        
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH) as f:
                return yaml.safe_load(f) or defaults
        return defaults
    
    def _load_corrections(self) -> List[dict]:
        """Load correction history for learning."""
        if not CORRECTIONS_PATH.exists():
            return []
        
        corrections = []
        with open(CORRECTIONS_PATH) as f:
            for line in f:
                corrections.append(json.loads(line.strip()))
        return corrections
    
    def calculate_priority(self, message: Message) -> str:
        """Calculate priority score for a message."""
        content_lower = message.content.lower()
        subject_lower = message.subject.lower()
        sender_lower = message.sender.lower()
        
        # Score for urgent
        urgent_score = 0
        for keyword in self.config["rules"]["urgent_keywords"]:
            if keyword in content_lower or keyword in subject_lower:
                urgent_score += self.weights["urgent_keywords"]
        
        # Score for questions (usually urgent)
        question_score = 0
        for pattern in self.config["rules"]["question_patterns"]:
            if re.search(pattern, content_lower, re.IGNORECASE):
                question_score += self.weights["question_patterns"]
        
        # Score for spam
        spam_score = 0
        for keyword in self.config["rules"]["spam_keywords"]:
            if keyword in content_lower:
                spam_score += self.weights["spam_keywords"]
        
        # Score for notifications (usually spam)
        notification_score = 0
        for pattern in self.config["rules"]["notification_patterns"]:
            if re.search(pattern, content_lower, re.IGNORECASE):
                notification_score += self.weights["notification_patterns"]
        
        total = urgent_score + question_score + spam_score + notification_score
        
        if total == 0:
            return "unknown"
        
        # Normalize scores
        urg_pct = (urgent_score + question_score) / total
        spam_pct = (spam_score + notification_score) / total
        
        if urg_pct > 0.7:
            return "urgent"
        elif spam_pct > 0.7:
            return "spam"
        else:
            return "normal"
    
    def draft_response(self, message: Message) -> str:
        """Generate a draft response based on priority."""
        if message.priority == "urgent":
            return None  # Urgent messages should not auto-draft
        
        if message.priority == "spam":
            return None  # Don't respond to spam
        
        # Normal priority - draft acknowledgment
        templates = [
            f"Thanks for reaching out! I'll review and get back to you soon.",
            f"Thanks for the update on '{message.subject}'. Appreciate you keeping me in the loop.",
            f"Got it! I'll take a look and respond by EOD.",
            f"Thanks for letting me know about this. I'll review and follow up.",
        ]
        
        import random
        return random.choice(templates)
    
    def triage(self, messages: List[Message]) -> Dict:
        """Run triage on a list of messages."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "total": len(messages),
            "urgent": [],
            "normal": [],
            "spam": [],
            "drafted_responses": []
        }
        
        for msg in messages:
            msg.priority = self.calculate_priority(msg)
            msg.drafted_response = self.draft_response(msg)
            
            # Categorize
            if msg.priority == "urgent":
                results["urgent"].append(msg.__dict__)
            elif msg.priority == "spam":
                results["spam"].append(msg.__dict__)
            else:
                results["normal"].append(msg.__dict__)
            
            # Track drafted responses
            if msg.drafted_response:
                results["drafted_responses"].append({
                    "sender": msg.sender,
                    "subject": msg.subject,
                    "priority": msg.priority,
                    "draft": msg.drafted_response
                })
        
        return results
    
    def generate_digest(self, results: Dict, format: str = "markdown") -> str:
        """Generate a daily digest from triage results."""
        if format == "json":
            return json.dumps(results, indent=2)
        
        lines = [
            f"# Daily Inbox Digest - {datetime.now().strftime('%Y-%m-%d')}",
            "",
            f"🔴 **URGENT** ({len(results['urgent'])}):",
        ]
        
        for msg in results["urgent"]:
            lines.append(f"  - {msg['subject'][:50]}... from {msg['sender']}")
        
        lines.append("")
        lines.append(f"🟡 **NORMAL** ({len(results['normal'])}):")
        
        for msg in results["normal"]:
            lines.append(f"  - {msg['subject'][:50]}... from {msg['sender']}")
        
        lines.append("")
        lines.append(f"🟢 **SPAM/NOISE** ({len(results['spam'])}): Filtered")
        
        lines.append("")
        lines.append("---")
        lines.append(f"**Drafted responses available**: {len(results['drafted_responses'])}")
        
        return "\n".join(lines)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Inbox Triage - Message categorization")
    parser.add_argument("--input", required=True, help="Input file (JSON)")
    parser.add_argument("--output", help="Output file (MD)")
    parser.add_argument("--draft-responses", action="store_true", help="Generate draft responses")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", 
                       help="Output format")
    
    args = parser.parse_args()
    
    # Load messages
    with open(args.input) as f:
        messages_data = json.load(f)
    
    messages = [Message.from_dict(m) for m in messages_data]
    
    # Run triage
    triage = InboxTriage()
    results = triage.triage(messages)
    
    # Output results
    if args.format == "json":
        output = json.dumps(results, indent=2)
    else:
        output = triage.generate_digest(results, format="markdown")
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"✅ Digest saved to {args.output}")
    else:
        print(output)
    
    if args.draft_responses:
        print(f"\n📝 Drafted responses: {len(results['drafted_responses'])}")


if __name__ == "__main__":
    main()
