#!/usr/bin/env python3
"""
AICP OpenClaw Integration - Use compact protocol for subagent communication.

Usage:
    python3 openclaw_aicp.py spawn --task "Set up image generation"
    python3 openclaw_aicp.py status --session <session_id>
    python3 openclaw_aicp.py complete --session <session_id> --result "Done"
"""

import argparse
import sys
import uuid
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from protocol import Session, Message, parse_wire
from agent_bridge import AgentCommunicator


class OpenClawAICP:
    """AICP integration for OpenClaw subagent workflows."""
    
    def __init__(self):
        self.active_sessions = {}
    
    def spawn_subagent(self, task_type: str, params: dict = None) -> str:
        """
        Spawn a subagent with AICP-optimized task description.
        
        Instead of verbose text, sends compact wire format.
        Returns the wire payload that would be sent to subagent.
        """
        session_id = f"subagent-{uuid.uuid4().hex[:8]}"
        comm = AgentCommunicator(session_id=session_id)
        
        # Add task-specific glossary
        domain_glossary = self._get_glossary_for_task(task_type)
        comm.add_custom_terms(domain_glossary)
        
        # Create task message
        task_ref = f"{task_type}/{datetime.now().strftime('%H%M%S')}"
        comm.create_task(
            task_type=task_type[:3].upper(),
            target=task_ref.split('/')[-1],
            params=params or {}
        )
        
        wire = comm.get_wire_payload()
        self.active_sessions[session_id] = comm
        
        return {
            "session_id": session_id,
            "wire_payload": wire,
            "wire_tokens": len(wire.split()),
            "estimated_json_tokens": len(comm.session.to_json().__str__().split()),
            "savings_percent": self._calc_savings(wire, comm)
        }
    
    def _get_glossary_for_task(self, task_type: str) -> dict:
        """Get domain-specific glossary for task type."""
        glossaries = {
            "image": {"GEN": "generate", "IMG": "image", "RES": "resolution", "FMT": "format"},
            "code": {"REF": "refactor", "TST": "test", "DOC": "document", "IMP": "implement"},
            "data": {"ETL": "extract_transform_load", "AGG": "aggregate", "QRY": "query"},
            "llm": {"MDL": "model", "TKN": "token", "CTX": "context", "INF": "inference"},
            "aicp": {"PRO": "protocol", "CMP": "compact", "WIR": "wire", "EXP": "expand"}
        }
        for key in glossaries:
            if key in task_type.lower():
                return glossaries[key]
        return {}
    
    def _calc_savings(self, wire: str, comm: AgentCommunicator) -> float:
        """Calculate token savings vs JSON."""
        wire_tokens = len(wire.split())
        import json
        json_str = json.dumps(comm.session.to_json())
        json_tokens = len(json_str.split())
        return round((1 - wire_tokens / json_tokens) * 100, 1)
    
    def report_status(self, session_id: str, status: str, metrics: dict = None) -> str:
        """Generate status update wire message."""
        if session_id not in self.active_sessions:
            comm = AgentCommunicator(session_id=session_id)
        else:
            comm = self.active_sessions[session_id]
        
        comm.update_status(
            ref=f"TSK/{session_id}",
            status=status[:4].upper() if len(status) > 4 else status.upper(),
            details=metrics or {}
        )
        
        return comm.get_wire_payload()
    
    def complete_task(self, session_id: str, result: str, summary: dict = None) -> str:
        """Generate completion notification."""
        if session_id not in self.active_sessions:
            comm = AgentCommunicator(session_id=session_id)
        else:
            comm = self.active_sessions[session_id]
        
        comm.notify_completion(
            ref=f"TSK/{session_id}",
            result=result[:2].upper() if len(result) > 2 else result.upper(),
            metrics=summary or {}
        )
        
        return comm.get_wire_payload()


def main():
    parser = argparse.ArgumentParser(description="AICP for OpenClaw subagents")
    sub = parser.add_subparsers(dest="command", required=True)
    
    # Spawn command
    p_spawn = sub.add_parser("spawn", help="Spawn subagent with AICP")
    p_spawn.add_argument("--task", required=True, help="Task description")
    p_spawn.add_argument("--type", default="general", help="Task type (image/code/data/llm/aicp)")
    p_spawn.add_argument("--priority", default="normal", help="Priority (CRIT/WARN/INFO)")
    
    # Status command
    p_status = sub.add_parser("status", help="Report subagent status")
    p_status.add_argument("--session", required=True, help="Session ID")
    p_status.add_argument("--status", default="running", help="Status (PEND/DONE/ERR)")
    
    # Complete command
    p_complete = sub.add_parser("complete", help="Complete subagent task")
    p_complete.add_argument("--session", required=True, help="Session ID")
    p_complete.add_argument("--result", default="OK", help="Result (OK/ERR)")
    
    args = parser.parse_args()
    
    aicp = OpenClawAICP()
    
    if args.command == "spawn":
        result = aicp.spawn_subagent(
            task_type=args.type,
            params={"task": args.task, "pri": args.priority.upper()[:4]}
        )
        print(json.dumps(result, indent=2))
        
    elif args.command == "status":
        wire = aicp.report_status(args.session, args.status)
        print(wire)
        
    elif args.command == "complete":
        wire = aicp.complete_task(args.session, args.result)
        print(wire)


if __name__ == "__main__":
    import json  # Add import here for __main__
    
    # Demo mode
    if len(sys.argv) == 1:
        print("OPENCLAW AICP INTEGRATION DEMO")
        print("=" * 60)
        
        aicp = OpenClawAICP()
        
        # Demo 1: Spawn image generation subagent
        print("\n1. SPAWN: Image generation subagent")
        print("-" * 40)
        result = aicp.spawn_subagent(
            task_type="image",
            params={"type": "IMG", "count": "1", "style": "cyberpunk"}
        )
        print(f"Session: {result['session_id']}")
        print(f"Wire tokens: {result['wire_tokens']}")
        print(f"Savings: {result['savings_percent']}%")
        print(f"\nWire payload:\n{result['wire_payload']}")
        
        # Demo 2: Report status
        print("\n2. STATUS: Update from subagent")
        print("-" * 40)
        status = aicp.report_status(
            result['session_id'],
            "DONE",
            {"TOK": "50%", "time": "30s", "files": "1"}
        )
        print(status)
        
        # Demo 3: Complete
        print("\n3. COMPLETE: Task finished")
        print("-" * 40)
        complete = aicp.complete_task(
            result['session_id'],
            "OK",
            {"IMG": "generated", "RES": "1024x1024"}
        )
        print(complete)
        
        sys.exit(0)
    
    main()
