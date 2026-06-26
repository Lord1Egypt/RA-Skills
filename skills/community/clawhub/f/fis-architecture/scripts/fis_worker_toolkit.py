#!/usr/bin/env python3
"""
FIS Worker Toolkit - Engineer/Researcher/Writer spawn sub-agents for complex tasks
Sub-agents run in background without creating new Threads
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from fis_lifecycle_pro import FISLifecyclePro


class FISWorkerToolkit:
    def __init__(self):
        self.fis = FISLifecyclePro()

    def spawn_for_subtask(self, parent_ticket_id, subtask_description):
        """Spawn sub-agent for complex subtask - runs in background"""
        print("=" * 60)
        print("🔄 Spawning SubAgent for Complex Subtask")
        print("=" * 60)

        sub_agent = self._select_sub_agent(subtask_description)

        sub_ticket_id, sub_ticket = self.fis.create_ticket(
            agent=sub_agent,
            task=f"[Subtask of {parent_ticket_id}] {subtask_description}",
            role="subagent",
        )

        print(f"\n✅ Sub-ticket created: {sub_ticket_id}")
        print(f"SubAgent: {sub_agent}")
        print(f"Parent: {parent_ticket_id}")

        spawn_cmd = f"""sessions_spawn(
    agentId="{sub_agent}",
    task="{subtask_description}",
    mode="run",
    label="{sub_ticket_id}"
)"""

        print(f"\n📋 Execute this to spawn sub-agent:")
        print(spawn_cmd)

        print(f"\n⚠️ IMPORTANT: Sub-agent runs in BACKGROUND")
        print("- No new Discord Thread created")
        print("- Sub-agent works silently")
        print("- You (Worker) manage and monitor the sub-agent")
        print("- Integrate sub-agent results into main task")
        print("- Report final result to CyberMao in main Thread")

        return sub_ticket_id

    def _select_sub_agent(self, task_description):
        task_lower = task_description.lower()

        if any(
            k in task_lower
            for k in ["code", "python", "implement", "algorithm", "debug"]
        ):
            return "opencode"
        elif any(k in task_lower for k in ["research", "paper", "theory", "analysis"]):
            return "claude"
        elif any(k in task_lower for k in ["doc", "write", "markdown", "latex"]):
            return "writer"
        else:
            return "opencode"

    def report_to_cybermao(self, ticket_id, summary, deliverables=None, issues=None):
        """Generate A2A completion report for CyberMao"""
        status_emoji = "✅" if not issues else "⚠️"

        report = f"""{status_emoji} Task Complete: {ticket_id}

**Summary**: {summary}

**Status**: {"Complete" if not issues else "Completed with issues"}
"""

        if deliverables:
            report += "\n**Deliverables**:\n"
            for d in deliverables:
                report += f"- `{d}`\n"

        if issues:
            report += "\n**Issues**:\n"
            for issue in issues:
                report += f"- {issue}\n"

        print(report)
        print("\n📤 Send to CyberMao via A2A:")
        print(
            f'sessions_send(\n    sessionKey="main",\n    message="{report[:100]}..."\n)'
        )
        print(f"\nFull report length: {len(report)} chars")

        return report

    def update_progress(self, ticket_id, status, note):
        self.fis.update_status(ticket_id, status, note)
        print(f"📝 Updated {ticket_id}: {status}")
        if note:
            print(f"   Note: {note}")

    def check_subagent_status(self, sub_ticket_id):
        """Check if sub-agent task is complete"""
        ticket, status = self.fis.get_ticket(sub_ticket_id)
        if ticket:
            print(f"📋 SubAgent Task: {sub_ticket_id}")
            print(f"   Status: {ticket.get('status', 'unknown')}")
            return ticket.get("status") == "done"
        return False


def main():
    parser = argparse.ArgumentParser(description="FIS Worker Toolkit")
    parser.add_argument("action", choices=["spawn", "report", "status", "check-sub"])
    parser.add_argument("--parent-ticket", "-p", required=True, help="Parent ticket ID")
    parser.add_argument("--subtask", "-s", help="Subtask description")
    parser.add_argument("--summary", "-m", help="Completion summary")
    parser.add_argument("--deliverables", "-d", nargs="+", help="Deliverable files")
    parser.add_argument("--status", choices=["todo", "doing", "review", "done"])
    parser.add_argument("--note", "-n", help="Progress note")

    args = parser.parse_args()
    toolkit = FISWorkerToolkit()

    if args.action == "spawn":
        if not args.subtask:
            print("Usage: spawn --parent-ticket <id> --subtask <desc>")
            sys.exit(1)
        toolkit.spawn_for_subtask(args.parent_ticket, args.subtask)

    elif args.action == "report":
        if not args.summary:
            print("Usage: report --parent-ticket <id> --summary <text>")
            sys.exit(1)
        toolkit.report_to_cybermao(args.parent_ticket, args.summary, args.deliverables)

    elif args.action == "status":
        if not args.status:
            print("Usage: status --parent-ticket <id> --status <status>")
            sys.exit(1)
        toolkit.update_progress(args.parent_ticket, args.status, args.note)

    elif args.action == "check-sub":
        toolkit.check_subagent_status(args.parent_ticket)


if __name__ == "__main__":
    main()
