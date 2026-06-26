#!/usr/bin/env python3
"""
FIS Lifecycle Pro - Enhanced version with auto-archival detection and better session management
"""

import json
import os
import sys
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from fis_config import get_shared_hub_path, get_workspace_path


class FISLifecyclePro:
    def __init__(self, hub_path=None):
        self.hub_path = str(hub_path) if hub_path else str(get_shared_hub_path())
        self.tickets_dir = os.path.join(self.hub_path, "tickets")
        self.active_dir = os.path.join(self.tickets_dir, "active")
        self.completed_dir = os.path.join(self.tickets_dir, "completed")
        self.archive_dir = os.path.join(self.tickets_dir, "archived")

        for d in [self.active_dir, self.completed_dir, self.archive_dir]:
            os.makedirs(d, exist_ok=True)

        self.channel_map = {
            "theory": "THEORY_FORUM_ID",
            "simulation": "SIMULATION_FORUM_ID",
            "coding": "CODING_FORUM_ID",
            "drafts": "DRAFTS_FORUM_ID",
        }

        self.workspace_map = {
            "researcher": "workspace-research",
            "engineer": "workspace-code",
            "writer": "workspace-writer",
            "main": "workspace",
            "cybermao": "workspace",
        }

    def create_ticket(
        self,
        agent,
        task,
        role="worker",
        source_session=None,
        channel_type=None,
        discord_thread_id=None,
    ):
        """Create a new ticket with enhanced metadata"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ticket_id = f"TASK_{timestamp}_{agent.upper()}"

        # Auto-detect source session
        if source_session is None:
            source_session = self._detect_current_session()

        # Determine target channel
        target_channel = self._resolve_target_channel(agent, channel_type)

        # Role ID mapping for Discord mentions
        role_map = {
            "researcher": "1477719718692392984",
            "engineer": "1477720570400346298",
            "writer": "1477721585036165375",
        }

        agent_role = role_map.get(agent.lower(), "")
        mention = f"<@&{agent_role}>" if agent_role else f"@{agent}"

        ticket = {
            "ticket_id": ticket_id,
            "agent_id": agent,
            "role": role,
            "task": task,
            "status": "todo",
            "source_session": source_session,
            "source_channel": self._extract_channel(source_session),
            "target_channel": target_channel,
            "discord_thread_id": discord_thread_id,
            "current_bindings": [source_session] if source_session else [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "deliverables": [],
            "notes": [],
        }

        filepath = os.path.join(self.active_dir, f"{ticket_id}.json")
        with open(filepath, "w") as f:
            json.dump(ticket, f, indent=2)

        print(f"✓ Created: {filepath}")
        print(f"  Ticket ID: {ticket_id}")
        print(f"  Target: {agent} ({target_channel})")
        print(f"  Mention: {mention}")

        return ticket_id, ticket

    def _detect_current_session(self):
        """Detect current session from OpenClaw environment.

        Attempts to identify the active session via:
        1. OPENCLAW_SESSION_KEY env var (set by OpenClaw runtime)
        2. `openclaw sessions list --json` CLI (fallback for manual runs)
        3. Returns "manual" if neither is available
        """
        session_key = os.environ.get("OPENCLAW_SESSION_KEY", "")
        if session_key:
            return session_key

        # Fallback: query OpenClaw CLI for active sessions.
        # This subprocess call is intentional — it's the only way to detect
        # the current session context when running outside the OpenClaw runtime.
        try:
            result = subprocess.run(
                ["openclaw", "sessions", "list", "--json"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                sessions = json.loads(result.stdout)
                if sessions and len(sessions) > 0:
                    return sessions[0].get("key", "unknown")
        except (
            subprocess.TimeoutExpired,
            FileNotFoundError,
            json.JSONDecodeError,
            OSError,
        ):
            pass

        return "manual"

    def _resolve_target_channel(self, agent, channel_type):
        """Resolve target Forum channel for agent"""
        if channel_type and channel_type in self.channel_map:
            return self.channel_map[channel_type]

        # Default mapping
        agent_channel_map = {
            "researcher": ["theory", "simulation"],
            "engineer": ["coding"],
            "writer": ["drafts"],
        }

        channels = agent_channel_map.get(agent.lower(), [])
        return channels[0] if channels else "general"

    def _extract_channel(self, session_key):
        """Extract channel type from session key"""
        if not session_key:
            return "unknown"
        if ":" in session_key:
            return session_key.split(":")[0]
        return "unknown"

    def update_status(self, ticket_id, status, note=None):
        """Update ticket status with optional note"""
        filepath = os.path.join(self.active_dir, f"{ticket_id}.json")

        if not os.path.exists(filepath):
            print(f"✗ Ticket not found: {ticket_id}")
            return False

        with open(filepath, "r") as f:
            ticket = json.load(f)

        old_status = ticket.get("status", "unknown")
        ticket["status"] = status
        ticket["updated_at"] = datetime.now().isoformat()

        if note:
            ticket["notes"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "status": status,
                    "note": note,
                }
            )

        with open(filepath, "w") as f:
            json.dump(ticket, f, indent=2)

        # Status emoji
        status_emoji = {
            "todo": "🟡",
            "doing": "🔵",
            "review": "🟠",
            "done": "🟢",
            "archived": "⚪",
        }

        print(f"{status_emoji.get(status, '⬜')} {ticket_id}: {old_status} → {status}")
        return True

    def complete_ticket(self, ticket_id, deliverables=None):
        """Mark ticket as completed with deliverables"""
        src = os.path.join(self.active_dir, f"{ticket_id}.json")

        if not os.path.exists(src):
            print(f"✗ Ticket not found: {ticket_id}")
            return False

        with open(src, "r") as f:
            ticket = json.load(f)

        # Update status
        ticket["status"] = "done"
        ticket["updated_at"] = datetime.now().isoformat()
        ticket["completed_at"] = datetime.now().isoformat()

        if deliverables:
            ticket["deliverables"] = deliverables
        else:
            # Auto-detect deliverables
            ticket["deliverables"] = self._auto_detect_deliverables(ticket_id, ticket)

        with open(src, "w") as f:
            json.dump(ticket, f, indent=2)

        # Move to completed
        dst = os.path.join(self.completed_dir, f"{ticket_id}.json")
        os.rename(src, dst)

        print(f"✅ Completed: {ticket_id}")
        print(f"   Deliverables: {len(ticket['deliverables'])} files")

        return True

    def _auto_detect_deliverables(self, ticket_id, ticket):
        agent_id = ticket.get("agent_id", "")
        workspace_path = get_workspace_path(agent_id)

        deliverables = []
        output_dirs = [
            str(workspace_path / "output"),
            str(workspace_path / "deliverables"),
        ]

        ticket_time_str = ticket.get("created_at", "")
        try:
            ticket_time = datetime.fromisoformat(ticket_time_str)
        except (ValueError, TypeError):
            ticket_time = None

        for output_dir in output_dirs:
            if os.path.exists(output_dir):
                for f in os.listdir(output_dir):
                    filepath = os.path.join(output_dir, f)
                    if os.path.isfile(filepath):
                        stat = os.stat(filepath)
                        mtime = datetime.fromtimestamp(stat.st_mtime)

                        # Include if created after ticket or matches ticket ID
                        include = False
                        if ticket_time and mtime >= ticket_time:
                            include = True
                        if ticket_id.lower() in f.lower():
                            include = True

                        if include:
                            deliverables.append(
                                {
                                    "file": f,
                                    "path": filepath,
                                    "size": stat.st_size,
                                    "modified": mtime.isoformat(),
                                }
                            )

        # Sort by modified time
        deliverables.sort(key=lambda x: x["modified"], reverse=True)
        return deliverables[:10]  # Limit to 10 most recent

    def archive_ticket(self, ticket_id):
        """Archive a completed ticket"""
        # Check completed first
        src = os.path.join(self.completed_dir, f"{ticket_id}.json")

        if not os.path.exists(src):
            # Check active
            src = os.path.join(self.active_dir, f"{ticket_id}.json")
            if not os.path.exists(src):
                print(f"✗ Ticket not found: {ticket_id}")
                return False

        with open(src, "r") as f:
            ticket = json.load(f)

        ticket["status"] = "archived"
        ticket["archived_at"] = datetime.now().isoformat()
        ticket["updated_at"] = datetime.now().isoformat()

        with open(src, "w") as f:
            json.dump(ticket, f, indent=2)

        # Move to archive
        dst = os.path.join(self.archive_dir, f"{ticket_id}.json")
        os.rename(src, dst)

        print(f"⚪ Archived: {ticket_id}")
        return True

    def list_active(self, agent=None):
        """List active tickets with optional agent filter"""
        tickets = []
        for f in os.listdir(self.active_dir):
            if f.endswith(".json"):
                with open(os.path.join(self.active_dir, f)) as fp:
                    ticket = json.load(fp)
                    if agent is None or ticket.get("agent_id") == agent:
                        tickets.append(ticket)

        # Sort by creation time
        tickets.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return tickets

    def list_completed(self, days=7):
        """List completed tickets from last N days"""
        tickets = []
        cutoff = datetime.now().timestamp() - (days * 86400)

        for f in os.listdir(self.completed_dir):
            if f.endswith(".json"):
                filepath = os.path.join(self.completed_dir, f)
                with open(filepath) as fp:
                    ticket = json.load(fp)
                    completed_at = ticket.get("completed_at", "")
                    if completed_at:
                        try:
                            completed_ts = datetime.fromisoformat(
                                completed_at
                            ).timestamp()
                            if completed_ts >= cutoff:
                                tickets.append(ticket)
                        except (ValueError, TypeError):
                            pass

        tickets.sort(key=lambda x: x.get("completed_at", ""), reverse=True)
        return tickets

    def get_ticket(self, ticket_id):
        """Get ticket from active, completed, or archived"""
        for d in [self.active_dir, self.completed_dir, self.archive_dir]:
            filepath = os.path.join(d, f"{ticket_id}.json")
            if os.path.exists(filepath):
                with open(filepath) as fp:
                    return json.load(fp), os.path.basename(d)
        return None, None

    def check_archivable(self):
        """Check which completed tickets can be archived (older than 7 days)"""
        archivable = []
        cutoff = datetime.now().timestamp() - (7 * 86400)

        for f in os.listdir(self.completed_dir):
            if f.endswith(".json"):
                filepath = os.path.join(self.completed_dir, f)
                with open(filepath) as fp:
                    ticket = json.load(fp)
                    completed_at = ticket.get("completed_at", "")
                    if completed_at:
                        try:
                            completed_ts = datetime.fromisoformat(
                                completed_at
                            ).timestamp()
                            if completed_ts < cutoff:
                                archivable.append(ticket["ticket_id"])
                        except (ValueError, TypeError):
                            pass

        return archivable

    def generate_report(self, ticket_id):
        """Generate completion report for a ticket"""
        ticket, status = self.get_ticket(ticket_id)
        if not ticket:
            return None

        report = f"""## 📋 Task Report: {ticket_id}

**Status**: {ticket.get("status", "unknown").upper()}
**Agent**: {ticket.get("agent_id", "unknown")}
**Created**: {ticket.get("created_at", "unknown")[:10]}

### 📝 Task Description
{ticket.get("task", "No description")}

### 📁 Deliverables
"""

        deliverables = ticket.get("deliverables", [])
        if deliverables:
            for d in deliverables[:5]:  # Top 5
                size = d.get("size", 0)
                size_str = f"{size / 1024:.1f} KB" if size > 1024 else f"{size} B"
                report += f"- `{d['file']}` ({size_str})\n"
        else:
            report += "- No deliverables found\n"

        # Notes
        notes = ticket.get("notes", [])
        if notes:
            report += "\n### 📝 Progress Notes\n"
            for note in notes[-3:]:  # Last 3 notes
                report += (
                    f"- [{note.get('status', 'unknown')}] {note.get('note', '')}\n"
                )

        return report


def main():
    parser = argparse.ArgumentParser(description="FIS Lifecycle Pro")
    parser.add_argument(
        "command",
        choices=["create", "list", "status", "complete", "archive", "report", "clean"],
    )
    parser.add_argument("--agent", "-a", help="Target agent")
    parser.add_argument("--task", "-t", help="Task description")
    parser.add_argument("--role", "-r", default="worker", help="Role (worker/reviewer)")
    parser.add_argument("--ticket-id", "-i", help="Ticket ID")
    parser.add_argument(
        "--channel-type", "-c", help="Channel type (theory/simulation/coding/drafts)"
    )
    parser.add_argument("--status", "-s", help="New status (todo/doing/review/done)")
    parser.add_argument("--note", "-n", help="Status update note")

    args = parser.parse_args()

    fis = FISLifecyclePro()

    if args.command == "create":
        if not args.agent or not args.task:
            print(
                "Usage: fis create --agent <agent> --task <task> [--channel-type <type>]"
            )
            sys.exit(1)
        ticket_id, ticket = fis.create_ticket(
            args.agent, args.task, args.role, channel_type=args.channel_type
        )
        print(f"\nNext step: A2A notify the agent")
        print(
            f"  sessions_send(sessionKey='{args.agent}', message='New ticket: {ticket_id}')"
        )

    elif args.command == "list":
        print("\n🟡 Active Tickets:")
        active = fis.list_active(args.agent)
        for t in active[:10]:
            emoji = {"todo": "🟡", "doing": "🔵", "review": "🟠"}.get(t["status"], "⬜")
            print(f"  {emoji} {t['ticket_id']} [{t['agent_id']}] {t['task'][:50]}...")

        if not active:
            print("  (no active tickets)")

        # Show archivable count
        archivable = fis.check_archivable()
        if archivable:
            print(f"\n⚪ {len(archivable)} tickets ready for archival")

    elif args.command == "status":
        if not args.ticket_id or not args.status:
            print(
                "Usage: fis status --ticket-id <id> --status <status> [--note <note>]"
            )
            sys.exit(1)
        fis.update_status(args.ticket_id, args.status, args.note)

    elif args.command == "complete":
        if not args.ticket_id:
            print("Usage: fis complete --ticket-id <id>")
            sys.exit(1)
        fis.complete_ticket(args.ticket_id)

    elif args.command == "archive":
        if args.ticket_id:
            fis.archive_ticket(args.ticket_id)
        else:
            # Auto-archive old completed tickets
            archivable = fis.check_archivable()
            if archivable:
                print(f"Archiving {len(archivable)} old tickets...")
                for tid in archivable:
                    fis.archive_ticket(tid)
            else:
                print("No tickets ready for archival")

    elif args.command == "report":
        if not args.ticket_id:
            print("Usage: fis report --ticket-id <id>")
            sys.exit(1)
        report = fis.generate_report(args.ticket_id)
        if report:
            print(report)
        else:
            print(f"Ticket not found: {args.ticket_id}")

    elif args.command == "clean":
        archivable = fis.check_archivable()
        if archivable:
            print(f"Found {len(archivable)} tickets ready for archival")
            print("Run 'fis archive' to archive them")
        else:
            print("No cleanup needed")


if __name__ == "__main__":
    main()
