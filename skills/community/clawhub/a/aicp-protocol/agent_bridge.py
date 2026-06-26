#!/usr/bin/env python3
"""AICP Agent Bridge - Use compact protocol for subagent communication."""

import sys
import json
from pathlib import Path

# Add protocol to path
sys.path.insert(0, str(Path(__file__).parent))
from protocol import Session, Message, parse_wire


class AgentCommunicator:
    """Bridge for agent-to-agent communication using AICP."""
    
    def __init__(self, session_id: str = None):
        self.session = Session(
            version="1",
            session_id=session_id or f"agent-{id(self)}"
        )
        self._setup_default_glossary()
    
    def _setup_default_glossary(self):
        """Define common abbreviations for agent tasks."""
        self.session.glossary = {
            "TSK": "task",
            "RPT": "report",
            "QRY": "query",
            "CFG": "config",
            "GEN": "generate",
            "ANL": "analyze",
            "DBG": "debug",
            "DEP": "deploy",
            "TST": "test",
            "DOC": "document",
            "OK": "success",
            "ERR": "error",
            "PEND": "pending",
            "DONE": "completed",
            "CRIT": "critical",
            "WARN": "warning",
            "INFO": "information"
        }
    
    def add_custom_terms(self, terms: dict):
        """Add domain-specific glossary terms."""
        self.session.glossary.update(terms)
    
    def create_task(self, task_type: str, target: str, params: dict = None) -> str:
        """Create a task message in AICP format."""
        msg = Message(
            op="create",
            ref=f"{task_type}/{target}",
            fields=params or {}
        )
        self.session.messages.append(msg)
        return msg.to_wire(self.session.glossary)
    
    def update_status(self, ref: str, status: str, details: dict = None) -> str:
        """Update status of a task/resource."""
        fields = {"status": status}
        if details:
            fields.update(details)
        
        msg = Message(
            op="upd",
            ref=ref,
            fields=fields
        )
        self.session.messages.append(msg)
        return msg.to_wire(self.session.glossary)
    
    def query_status(self, ref: str, fields_requested: list = None) -> str:
        """Query status of a resource."""
        params = {}
        if fields_requested:
            params["fields"] = ",".join(fields_requested)
        
        msg = Message(
            op="qry",
            ref=ref,
            fields=params
        )
        self.session.messages.append(msg)
        return msg.to_wire(self.session.glossary)
    
    def notify_completion(self, ref: str, result: str, metrics: dict = None) -> str:
        """Notify completion of a task."""
        fields = {"result": result}
        if metrics:
            fields.update(metrics)
        
        msg = Message(
            op="notify",
            ref=ref,
            fields=fields
        )
        self.session.messages.append(msg)
        return msg.to_wire(self.session.glossary)
    
    def get_wire_payload(self) -> str:
        """Get full session as wire format."""
        return self.session.to_wire()
    
    def get_session_summary(self) -> dict:
        """Get human-readable summary."""
        return {
            "session_id": self.session.session_id,
            "glossary_terms": len(self.session.glossary),
            "messages": len(self.session.messages),
            "wire_tokens": len(self.session.to_wire().split()),
            "json_tokens": len(json.dumps(self.session.to_json()).split())
        }


def demo_agent_communication():
    """Demo: Agent spawning subagent with AICP."""
    
    print("=" * 70)
    print("AICP AGENT-TO-AGENT COMMUNICATION DEMO")
    print("=" * 70)
    
    # Parent agent creates communication session
    comm = AgentCommunicator(session_id="main-session-001")
    
    # Add domain-specific terms
    comm.add_custom_terms({
        "IMG": "image_generation",
        "AICP": "ai_compact_protocol",
        "LLM": "local_language_model",
        "TOK": "token_savings"
    })
    
    print("\n1. PARENT AGENT → SPAWNS SUBAGENT")
    print("-" * 50)
    
    # Instead of verbose text, send compact AICP
    task_wire = comm.create_task(
        task_type="TSK",
        target="IMG-setup",
        params={
            "type": "IMG",
            "priority": "PEND",
            "out": "OK"
        }
    )
    print(f"Wire: {task_wire}")
    print(f"Tokens: {len(task_wire.split())}")
    
    # vs verbose alternative
    verbose = 'Create task: Set up image generation (type=image_generation, priority=pending, expected_output=success)'
    print(f"\nVerbose: {verbose}")
    print(f"Tokens: {len(verbose.split())}")
    print(f"Savings: {(1 - len(task_wire.split())/len(verbose.split()))*100:.1f}%")
    
    print("\n2. SUBAGENT → REPORTS STATUS")
    print("-" * 50)
    
    subagent_comm = AgentCommunicator(session_id="subagent-001")
    subagent_comm.add_custom_terms(comm.session.glossary)  # Share glossary
    
    status_wire = subagent_comm.update_status(
        ref="TSK/IMG-setup",
        status="DONE",
        details={
            "TOK": "63%",
            "files": "2",
            "LOC": "150"
        }
    )
    print(f"Wire: {status_wire}")
    
    print("\n3. SUBAGENT → NOTIFIES COMPLETION")
    print("-" * 50)
    
    notify_wire = subagent_comm.notify_completion(
        ref="TSK/IMG-setup",
        result="OK",
        metrics={
            "time": "45s",
            "TOK": "20 vs 55"
        }
    )
    print(f"Wire: {notify_wire}")
    
    print("\n4. FULL SESSION DUMP")
    print("-" * 50)
    print(subagent_comm.get_wire_payload())
    
    print("\n5. TOKEN COMPARISON")
    print("-" * 50)
    summary = subagent_comm.get_session_summary()
    print(f"Session: {summary['session_id']}")
    print(f"Messages: {summary['messages']}")
    print(f"Wire tokens: {summary['wire_tokens']}")
    print(f"JSON tokens: {summary['json_tokens']}")
    print(f"Savings: {(1 - summary['wire_tokens']/summary['json_tokens'])*100:.1f}%")


if __name__ == "__main__":
    demo_agent_communication()
