#!/usr/bin/env python3
"""Team Division Management Tool

Manages team member information including skills, roles, and work assignments.
Data is stored in ~/.agent-team/team.json by default, or a custom path via --data-file.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Global variable to store custom data file path
_data_file_path: Path | None = None


def set_data_file(path: str | None) -> None:
    """Set a custom data file path."""
    global _data_file_path
    if path:
        _data_file_path = Path(path)


def get_data_file() -> Path:
    """Get the path to the team data file."""
    # 1. Check environment variable (for test isolation)
    env_path = os.environ.get("AGENT_TEAM_DATA_FILE")
    if env_path:
        return Path(env_path)

    # 2. Check global override (--data-file CLI arg)
    if _data_file_path:
        data_file = _data_file_path
        data_file.parent.mkdir(parents=True, exist_ok=True)
        return data_file

    # 3. Default production path
    data_dir = Path.home() / ".agent-team"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "team.json"


def load_data() -> dict:
    """Load team data from JSON file."""
    data_file = get_data_file()
    if not data_file.exists():
        return {"team": {}}

    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict) or "team" not in data:
                return {"team": {}}
            return data
    except (json.JSONDecodeError, IOError):
        return {"team": {}}


def save_data(data: dict) -> None:
    """Save team data to JSON file."""
    data_file = get_data_file()
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def reset_data() -> None:
    """Reset all team data to empty state."""
    save_data({"team": {}})
    print("Team data has been reset to empty.")


def list_members() -> None:
    """List all team members in compact format."""
    data = load_data()
    team = data.get("team", {})

    if not team:
        print("No team members found.")
        return

    print("## Team Members")
    print()

    # Group members by 'group' field
    grouped: dict[str, list] = {}
    for member_id, member in team.items():
        group_name = member.get("group", "")
        if group_name not in grouped:
            grouped[group_name] = []
        grouped[group_name].append((member_id, member))

    # Display grouped members
    for group_name, members in grouped.items():
        if group_name:
            print(f"### Group: {group_name}")
            print()

        for member_id, member in members:
            name = member.get("name", "")
            role = member.get("role", "")
            is_leader = member.get("is_leader", False)
            tags = member.get("tags", [])
            expertise = member.get("expertise", [])
            not_good_at = member.get("not_good_at", [])
            load_workflow = member.get("load_workflow")

            # First line: name, role, tags
            tags_str = ",".join(tags)
            if is_leader:
                print(f"**{name}** ⭐ {role} - {tags_str}")
            else:
                print(f"**{name}** - {role} - {tags_str}")

            # agent_id line
            print(f"- agent_id: {member_id}")

            # expertise line
            if expertise:
                print(f"- expertise: {','.join(expertise)}")

            # not_good_at line
            if not_good_at:
                print(f"- not_good_at: {','.join(not_good_at)}")

            # load_workflow line
            if load_workflow is not None:
                print(f"- load_workflow: {load_workflow}")

            print()

    # Find leader for summary
    leader = next((m for m in team.values() if m.get("is_leader")), None)
    leader_info = f", Leader: {leader.get('name')} ({leader.get('agent_id')})" if leader else ""
    print(f"# Total: {len(team)} member(s){leader_info}")


def update_member(
    agent_id: str,
    name: str,
    role: str,
    is_leader: bool,
    enabled: bool,
    tags: str,
    expertise: str,
    not_good_at: str,
    load_workflow: str | None = None,
    group: str | None = None,
) -> None:
    """Add or update a team member."""
    data = load_data()
    is_new = agent_id not in data["team"]

    # Get existing member data for merge behavior
    existing_member = data["team"].get(agent_id, {})

    # If setting this member as leader, remove leader status from others
    if is_leader:
        for existing_id, existing_member_data in data["team"].items():
            if existing_id != agent_id and existing_member_data.get("is_leader"):
                existing_member_data["is_leader"] = False
                print(f"Note: Removed leader status from {existing_member_data.get('name', existing_id)}")

    member = {
        "agent_id": agent_id,
        "name": name,
        "role": role,
        "is_leader": is_leader,
        "enabled": enabled,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "expertise": [e.strip() for e in expertise.split(",") if e.strip()],
        "not_good_at": [n.strip() for n in not_good_at.split(",") if n.strip()],
    }

    # Preserve or update load_workflow
    if load_workflow is not None:
        member["load_workflow"] = load_workflow == "true"
    elif "load_workflow" in existing_member:
        member["load_workflow"] = existing_member["load_workflow"]

    # Preserve or update group
    if group is not None and group.strip():
        member["group"] = group.strip()
    elif "group" in existing_member:
        member["group"] = existing_member["group"]

    data["team"][agent_id] = member
    save_data(data)

    action = "Added" if is_new else "Updated"
    leader_suffix = " (Leader)" if is_leader else ""
    print(f"{action} member: {name} ({agent_id}){leader_suffix}")


def main():
    parser = argparse.ArgumentParser(
        description="Team Division Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--data-file",
        help="Path to data file (default: ~/.agent-team/team.json)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list command
    subparsers.add_parser("list", help="List all team members")

    # reset command
    subparsers.add_parser("reset", help="Reset all team data to empty")

    # update command
    update_parser = subparsers.add_parser("update", help="Add or update a team member")
    update_parser.add_argument("--agent-id", required=True, help="Member unique ID")
    update_parser.add_argument("--name", required=True, help="Member name")
    update_parser.add_argument("--role", required=True, help="Member role")
    update_parser.add_argument(
        "--is-leader", required=True, choices=["true", "false"],
        help="Is team leader (only one leader allowed per team)"
    )
    update_parser.add_argument(
        "--enabled", required=True, choices=["true", "false"], help="Is member enabled"
    )
    update_parser.add_argument("--tags", required=True, help="Tags (comma separated)")
    update_parser.add_argument(
        "--expertise", required=True, help="Expertise skills (comma separated)"
    )
    update_parser.add_argument(
        "--not-good-at", required=True, help="Weak areas (comma separated)"
    )
    update_parser.add_argument(
        "--load-workflow", choices=["true", "false"],
        help="Whether to load workflow prompts (default: true for leader, false for others)"
    )
    update_parser.add_argument(
        "--group", help="Group name for categorization"
    )

    args = parser.parse_args()

    # Set custom data file if provided
    set_data_file(args.data_file)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "list":
        list_members()
    elif args.command == "reset":
        reset_data()
    elif args.command == "update":
        update_member(
            agent_id=args.agent_id,
            name=args.name,
            role=args.role,
            is_leader=args.is_leader == "true",
            enabled=args.enabled == "true",
            tags=args.tags,
            expertise=args.expertise,
            not_good_at=args.not_good_at,
            load_workflow=args.load_workflow,
            group=args.group,
        )


if __name__ == "__main__":
    main()