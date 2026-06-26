#!/usr/bin/env python3

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from fis_lifecycle_pro import FISLifecyclePro
from fis_config import get_scripts_dir


class FISCoordinator:
    def __init__(self):
        self.fis = FISLifecyclePro()
        self.forum_channels = {
            "theory": "theory-derivation",
            "simulation": "gpr-simulation",
            "coding": "coding",
            "drafts": "drafts",
        }
        self.scripts_dir = get_scripts_dir()

    def create_and_delegate(self, agent, task, forum_channel=None):
        print("=" * 60)
        print("STEP 1: Creating FIS Ticket")
        print("=" * 60)

        channel_type = forum_channel or self._infer_channel_type(agent)
        ticket_id, ticket = self.fis.create_ticket(
            agent=agent, task=task, role="worker", channel_type=channel_type
        )

        print("\n" + "=" * 60)
        print("STEP 2: Forum Thread Template")
        print("=" * 60)
        thread_template = self._generate_thread_template(ticket, channel_type)
        print(thread_template)

        print("\n" + "=" * 60)
        print("STEP 3: A2A Notify Worker")
        print("=" * 60)
        a2a_message = self._build_a2a_message(ticket, channel_type)
        print(a2a_message)

        print("\n" + "=" * 60)
        print("✅ COORDINATION COMPLETE")
        print("=" * 60)
        print(f"Ticket: {ticket_id}")
        print(f"Agent: {agent}")
        print(f"Forum: {self.forum_channels.get(channel_type, 'coding')}")
        print("\n📋 NEXT STEPS:")
        print("1. Copy the Thread template above")
        print("2. Create a new post in the Forum channel using `message` tool")
        print("3. Get the Thread ID from the response")
        print("4. Run: fis_coordinator notify --ticket-id " + ticket_id + " --thread-id <THREAD_ID>")

        return ticket_id

    def notify_worker(self, ticket_id, thread_id, thread_name=""):
        """Generate final A2A message with Thread ID after Thread is created"""
        ticket, status = self.fis.get_ticket(ticket_id)
        if not ticket:
            print(f"❌ Ticket not found: {ticket_id}")
            return None

        agent_id = ticket['agent_id']
        agent_mention = {
            "engineer": "<@&1477720570400346298>",
            "researcher": "<@&1477719718692392984>",
            "writer": "<@&1477721585036165375>"
        }.get(agent_id.lower(), f"@{agent_id}")

        thread_display = thread_name or f"Thread ID: {thread_id}"

        final_a2a = f"""🎯 **New FIS Task: {ticket_id}**

**Task**: {ticket['task']}

**📍 Thread Location**: 
- Forum: #{self.forum_channels.get(ticket.get('channel_type', 'coding'))}
- Thread: {thread_display}
- Thread ID: `{thread_id}`

**⚠️ IMPORTANT**: Reply in THIS Thread, not your current session!

**Steps**:
1. Use `message` tool to reply to Thread ID `{thread_id}`
2. Confirm receipt: "收到任务，开始执行"
3. Update status: 🟡 TODO → 🔵 DOING
4. Execute task
5. Update status: 🔵 DOING → 🟢 DONE
6. Report completion via A2A to me

**Status Command**:
```
python3 {self.scripts_dir}/fis_lifecycle_pro.py status --ticket-id {ticket_id} --status doing
```

**Completion Command**:
```
python3 {self.scripts_dir}/fis_lifecycle_pro.py complete --ticket-id {ticket_id}
```

Then A2A report to me with summary.

Reply in Thread `{thread_id}` NOW!"""

        print("=" * 60)
        print("FINAL A2A MESSAGE (Send after Thread created)")
        print("=" * 60)
        print(final_a2a)
        print("\n" + "=" * 60)
        print("COPY ABOVE and send via sessions_send to", agent_id)
        print("=" * 60)

        return final_a2a

    def _infer_channel_type(self, agent):
        mapping = {"researcher": "theory", "engineer": "coding", "writer": "drafts"}
        return mapping.get(agent.lower(), "coding")

    def _generate_thread_template(self, ticket, channel_type):
        forum_name = self.forum_channels.get(channel_type, "coding")
        thread_title = f"{ticket['ticket_id']}: {ticket['task'][:50]}"

        template = f"""
🎯 **{ticket["ticket_id"]}**

**Task**: {ticket["task"]}

**Status**: 🟡 TODO
**Assigned to**: @{ticket["agent_id"]}

**TODO List**:
- [ ] Review task requirements
- [ ] Execute task
- [ ] Verify deliverables
- [ ] Report completion

**Instructions for Worker**:
1. Reply in this thread to confirm receipt
2. Update status: 🟡 → 🔵 DOING
3. Execute the task
4. Report completion via A2A to CyberMao

---
Forum: {forum_name}
Ticket: {ticket["ticket_id"]}
"""
        return template

    def _build_a2a_message(self, ticket, channel_type):
        forum_name = self.forum_channels.get(channel_type, "coding")

        msg = f"""🎯 New FIS Task: {ticket["ticket_id"]}

**Task**: {ticket["task"]}

**Instructions**:
1. Go to the {forum_name} Forum channel
2. Create a new post with title: "{ticket["ticket_id"]}: {ticket["task"][:30]}..."
3. Work in that thread
4. Update status: 🟡 TODO → 🔵 DOING → 🟢 DONE
5. Report completion via A2A to me

**Status Tracking**:
```
python3 {self.scripts_dir}/fis_lifecycle_pro.py status --ticket-id {ticket["ticket_id"]} --status doing
```

**Completion**:
```
python3 {self.scripts_dir}/fis_lifecycle_pro.py complete --ticket-id {ticket["ticket_id"]}

sessions_send(
    sessionKey="main",
    message="Task {ticket["ticket_id"]} complete. Summary: ..."
)
```

Reply here if you need clarification."""

        return msg

    def handle_worker_response(self, ticket_id, worker_message):
        ticket, status = self.fis.get_ticket(ticket_id)
        if not ticket:
            print(f"❌ Ticket not found: {ticket_id}")
            return False

        print("=" * 60)
        print(f"📨 Worker Response: {ticket_id}")
        print("=" * 60)
        print(f"From: {ticket['agent_id']}")
        print(f"Message: {worker_message[:200]}...")

        if any(
            word in worker_message.lower() for word in ["complete", "done", "finished"]
        ):
            print("\n✅ Worker reports completion")
            report = self.fis.generate_report(ticket_id)
            if report:
                print("\n" + report)

            print("\n📋 Actions for CyberMao:")
            print("1. Review deliverables in the Forum thread")
            print("2. Verify task completion")
            print("3. Archive the Forum thread manually")
            print(f"4. Run: fis complete --ticket-id {ticket_id}")
            print("5. Report to User")
        else:
            print("\n📝 Progress update received")
            self.fis.update_status(ticket_id, "doing", worker_message[:100])

        return True


def main():
    parser = argparse.ArgumentParser(description="FIS Coordinator")
    parser.add_argument("action", choices=["delegate", "notify", "respond", "report"])
    parser.add_argument("--agent", "-a", help="Target agent (required for delegate)")
    parser.add_argument("--task", "-t", help="Task description")
    parser.add_argument(
        "--forum", "-f", choices=["theory", "simulation", "coding", "drafts"]
    )
    parser.add_argument("--ticket-id", "-i", help="Ticket ID")
    parser.add_argument("--message", "-m", help="Worker response message")
    parser.add_argument("--thread-id", help="Discord Thread ID (for notify)")
    parser.add_argument("--thread-name", help="Thread name (optional)")

    args = parser.parse_args()
    coordinator = FISCoordinator()

    if args.action == "delegate":
        if not args.task:
            print("Usage: delegate --agent <agent> --task <task>")
            sys.exit(1)
        coordinator.create_and_delegate(args.agent, args.task, args.forum)

    elif args.action == "notify":
        if not args.ticket_id or not args.thread_id:
            print("Usage: notify --ticket-id <id> --thread-id <thread_id>")
            print("Example: notify --ticket-id TASK_20260306_xxx --thread-id 1479154945809977475")
            sys.exit(1)
        coordinator.notify_worker(args.ticket_id, args.thread_id, args.thread_name)

    elif args.action == "respond":
        if not args.ticket_id or not args.message:
            print("Usage: respond --ticket-id <id> --message <msg>")
            sys.exit(1)
        coordinator.handle_worker_response(args.ticket_id, args.message)

    elif args.action == "report":
        if not args.ticket_id:
            print("Usage: report --ticket-id <id>")
            sys.exit(1)
        report = coordinator.fis.generate_report(args.ticket_id)
        if report:
            print(report)


if __name__ == "__main__":
    main()
