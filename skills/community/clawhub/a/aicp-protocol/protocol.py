#!/usr/bin/env python3
"""AICP (AI Compact Protocol) - Token-efficient wire format parser."""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Message:
    """Single AICP message."""
    op: str
    ref: str
    fields: Dict[str, str] = field(default_factory=dict)
    
    def to_wire(self, glossary: Dict[str, str]) -> str:
        """Convert to compact wire format."""
        parts = [f"op:{self.op}", f"ref:{self.ref}"]
        for key, val in self.fields.items():
            # Use glossary abbreviation if exists
            for abbr, full in glossary.items():
                if val == full:
                    val = abbr
                    break
            parts.append(f"{key}={val}")
        return " ".join(parts)


@dataclass
class Session:
    """AICP session with glossary and messages."""
    version: str = "1"
    session_id: str = ""
    glossary: Dict[str, str] = field(default_factory=dict)
    messages: List[Message] = field(default_factory=list)
    
    def to_wire(self) -> str:
        """Serialize to wire format."""
        lines = [f"VER:{self.version}", f"SID:{self.session_id}"]
        if self.glossary:
            gloss_str = " ".join(f"{k}={v}" for k, v in self.glossary.items())
            lines.append(f"GLOSS: {gloss_str}")
        for msg in self.messages:
            lines.append("MSG:")
            lines.append(f"{msg.to_wire(self.glossary)}")
        return "\n".join(lines)
    
    def to_json(self) -> dict:
        """Convert to JSON representation."""
        return {
            "protocolVersion": self.version,
            "sessionId": self.session_id,
            "glossary": self.glossary,
            "messages": [
                {
                    "op": m.op,
                    "ref": m.ref,
                    "fields": m.fields
                }
                for m in self.messages
            ]
        }


def parse_wire(text: str) -> Session:
    """Parse wire format into Session."""
    session = Session()
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith("VER:"):
            session.version = line[4:].strip()
        elif line.startswith("SID:"):
            session.session_id = line[4:].strip()
        elif line.startswith("GLOSS:"):
            gloss_text = line[6:].strip()
            for part in gloss_text.split():
                if "=" in part:
                    k, v = part.split("=", 1)
                    session.glossary[k] = v.replace('_', ' ')
        elif line == "MSG:":
            i += 1
            if i < len(lines):
                msg_body = lines[i]
                msg = Message(op="", ref="", fields={})
                
                # Parse tokens
                tokens = msg_body.split()
                for token in tokens:
                    if ':' in token:
                        key, val = token.split(':', 1)
                        if key == 'op':
                            msg.op = val
                        elif key == 'ref':
                            msg.ref = val
                    elif '=' in token:
                        key, val = token.split('=', 1)
                        # Expand glossary
                        if val in session.glossary:
                            val = session.glossary[val]
                        msg.fields[key] = val
                
                session.messages.append(msg)
        i += 1
    
    return session


def create_example() -> Session:
    """Create a demo session with token savings."""
    return Session(
        version="1",
        session_id="demo-001",
        glossary={
            "R1": "customer_refund_window",
            "T2": "priority_support",
            "U42": "user_42"
        },
        messages=[
            Message(
                op="upd",
                ref="ticket/8812",
                fields={"status": "closed", "reason": "R1"}
            ),
            Message(
                op="create",
                ref="ticket/new",
                fields={"title": "Payment_issue", "priority": "T2"}
            ),
            Message(
                op="notify",
                ref="U42",
                fields={"subject": "Ticket_resolved"}
            )
        ]
    )


if __name__ == "__main__":
    # Demo: Show token savings
    print("=" * 60)
    print("AICP TOKEN SAVINGS DEMO")
    print("=" * 60)
    
    session = create_example()
    
    # Wire format (compact)
    wire = session.to_wire()
    wire_tokens = len(wire.split())
    
    print("\n1. AICP WIRE FORMAT:")
    print("-" * 40)
    print(wire)
    print(f"\nTokens: ~{wire_tokens}")
    
    # JSON equivalent (verbose)
    json_repr = session.to_json()
    import json
    json_str = json.dumps(json_repr, indent=2)
    json_tokens = len(json_str.split())
    
    print("\n2. EQUIVALENT JSON:")
    print("-" * 40)
    print(json_str[:500] + "...")
    print(f"\nTokens: ~{json_tokens}")
    
    # Savings
    savings = (1 - wire_tokens / json_tokens) * 100
    print("\n3. TOKEN SAVINGS:")
    print("-" * 40)
    print(f"AICP wire:   {wire_tokens} tokens")
    print(f"JSON:        {json_tokens} tokens")
    print(f"SAVINGS:     {savings:.1f}%")
    
    # Parse round-trip
    print("\n4. ROUND-TRIP PARSE:")
    print("-" * 40)
    parsed = parse_wire(wire)
    print(f"Session ID: {parsed.session_id}")
    print(f"Messages: {len(parsed.messages)}")
    for m in parsed.messages:
        print(f"  - {m.op}: {m.ref} ({m.fields})")
