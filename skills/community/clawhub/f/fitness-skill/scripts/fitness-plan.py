#!/usr/bin/env python3
"""
fitness-plan — Create, view, or update a fitness plan.

Usage:
    fitness-plan init                          Interactive plan creation
    fitness-plan create --goals "gym,tennis" --frequency 4 --level intermediate
    fitness-plan show                          Display current plan (Markdown)
    fitness-plan update --frequency 4          Patch existing plan
    fitness-plan sync                          Push plan to Feishu doc
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fitness_skill import FitnessSkill


def cmd_init(skill: FitnessSkill):
    print("=== Fitness Plan Setup ===\n")

    if skill.has_plan():
        choice = input("A plan already exists. (c)ontinue with it / (n)ew plan? [c/n]: ").strip().lower()
        if choice != "n":
            print(skill.plan_to_markdown())
            return

    goals_raw = input("Goals (comma-separated, e.g. muscle_gain,cardio,flexibility): ").strip()
    goals = [g.strip() for g in goals_raw.split(",") if g.strip()] or ["general_fitness"]

    sport_raw = input("Sport preference (comma-separated, e.g. gym,tennis,cardio): ").strip()
    sport_pref = [s.strip() for s in sport_raw.split(",") if s.strip()] or ["gym"]

    freq_raw = input("Sessions per week (1-7) [3]: ").strip()
    frequency = int(freq_raw) if freq_raw.isdigit() and 1 <= int(freq_raw) <= 7 else 3

    level = input("Level (beginner/intermediate/advanced) [beginner]: ").strip().lower()
    if level not in ("beginner", "intermediate", "advanced"):
        level = "beginner"

    constraints = input("Any constraints (injuries, time limits)? [none]: ").strip()

    reminder = input("Daily reminder time (HH:MM, 24h) [08:00]: ").strip()
    if not reminder or ":" not in reminder:
        reminder = "08:00"

    profile = {
        "goals": goals,
        "sport_pref": sport_pref,
        "frequency": frequency,
        "level": level,
        "constraints": constraints,
        "reminder_time": reminder,
    }

    plan = skill.create_plan(profile)
    print("\n" + skill.plan_to_markdown())
    print(f"\nPlan saved to {skill.plan.__class__.__name__} ✓")


def cmd_show(skill: FitnessSkill):
    print(skill.plan_to_markdown())


def cmd_update(skill: FitnessSkill, argv: list):
    changes = {}
    i = 0
    while i < len(argv):
        key = argv[i].lstrip("-")
        if i + 1 < len(argv):
            val = argv[i + 1]
            if key in ("goals", "sport_pref"):
                changes[key] = [v.strip() for v in val.split(",")]
            elif key == "frequency":
                changes[key] = int(val)
            else:
                changes[key] = val
            i += 2
        else:
            i += 1

    if not changes:
        print("No changes provided. Example: fitness-plan update --frequency 4 --level intermediate")
        return

    plan = skill.update_plan(changes)
    print("Plan updated ✓\n")
    print(skill.plan_to_markdown())


def cmd_create(skill: FitnessSkill, argv: list):
    """Non-interactive plan creation from CLI flags."""
    opts = {
        "goals": ["general_fitness"],
        "sport_pref": ["gym"],
        "frequency": 3,
        "level": "beginner",
        "constraints": "",
        "reminder_time": "08:00",
    }
    i = 0
    while i < len(argv):
        key = argv[i].lstrip("-")
        if i + 1 < len(argv):
            val = argv[i + 1]
            if key in ("goals", "sport_pref"):
                opts[key] = [v.strip() for v in val.split(",")]
            elif key == "frequency":
                opts[key] = int(val)
            else:
                opts[key] = val
            i += 2
        else:
            i += 1

    skill.create_plan(opts)
    print("Plan created ✓\n")
    print(skill.plan_to_markdown())


def cmd_sync(skill: FitnessSkill):
    try:
        skill.sync_to_feishu()
        print("Plan synced to Feishu ✓")
    except Exception as e:
        print(f"Sync failed: {e}")


def main():
    skill = FitnessSkill()
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return

    cmd = args[0]
    if cmd == "init":
        cmd_init(skill)
    elif cmd == "create":
        cmd_create(skill, args[1:])
    elif cmd == "show":
        cmd_show(skill)
    elif cmd == "update":
        cmd_update(skill, args[1:])
    elif cmd == "sync":
        cmd_sync(skill)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__.strip())
        sys.exit(1)


if __name__ == "__main__":
    main()
