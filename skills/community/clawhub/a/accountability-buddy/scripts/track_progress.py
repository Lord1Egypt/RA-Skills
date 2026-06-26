#!/usr/bin/env python3
"""
Progress tracker for Accountability Buddy skill.
Tracks streaks, logs daily check-ins, and calculates stats.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Default data directory
DATA_DIR = Path.home() / ".openclaw" / "skills" / "accountability-buddy" / "data"
DATA_FILE = DATA_DIR / "progress.json"


def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_progress():
    """Load progress data from JSON file."""
    ensure_data_dir()
    if not DATA_FILE.exists():
        return {
            "topic": None,
            "startDate": None,
            "dailyGoal": None,
            "currentStreak": 0,
            "longestStreak": 0,
            "totalDays": 0,
            "checkIns": []
        }

    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_progress(data):
    """Save progress data to JSON file."""
    ensure_data_dir()
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def start_tracking(topic, daily_goal):
    """Start tracking a new learning goal."""
    data = load_progress()
    data["topic"] = topic
    data["startDate"] = datetime.now().strftime("%Y-%m-%d")
    data["dailyGoal"] = daily_goal
    data["currentStreak"] = 0
    data["longestStreak"] = 0
    data["totalDays"] = 0
    data["checkIns"] = []
    save_progress(data)
    return data


def log_check_in(status, note=""):
    """Log a daily check-in.

    Args:
        status: "completed", "partial", or "missed"
        note: Optional note about the session
    """
    data = load_progress()
    today = datetime.now().strftime("%Y-%m-%d")

    # Check if already logged today
    existing = [c for c in data["checkIns"] if c["date"] == today]
    if existing:
        # Update existing check-in
        existing[0]["status"] = status
        existing[0]["note"] = note
    else:
        # Add new check-in
        data["checkIns"].append({
            "date": today,
            "status": status,
            "note": note
        })
        data["totalDays"] += 1

    # Update streak
    if status in ["completed", "partial"]:
        data["currentStreak"] += 1
        if data["currentStreak"] > data["longestStreak"]:
            data["longestStreak"] = data["currentStreak"]
    else:
        data["currentStreak"] = 0

    save_progress(data)
    return data


def get_streak_message(streak):
    """Get celebration message for streak milestone."""
    if streak >= 30:
        return "🏆 30-DAY STREAK! You're unstoppable!"
    elif streak >= 14:
        return "🔥🔥🔥 Two weeks of consistency!"
    elif streak >= 7:
        return "🔥🔥 One week strong!"
    elif streak >= 3:
        return "🔥 You're building a habit!"
    else:
        return f"Day {streak} — Keep going!"


def get_stats():
    """Get current progress stats."""
    data = load_progress()

    if not data["topic"]:
        return {"status": "not_started", "message": "No active goal. Start with: 'Start accountability for [topic]'"}

    return {
        "status": "active",
        "topic": data["topic"],
        "startDate": data["startDate"],
        "dailyGoal": data["dailyGoal"],
        "currentStreak": data["currentStreak"],
        "longestStreak": data["longestStreak"],
        "totalDays": data["totalDays"],
        "message": get_streak_message(data["currentStreak"])
    }


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 2:
        print("Usage: track_progress.py <command> [args]")
        print("Commands: start, checkin, stats")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        if len(sys.argv) < 4:
            print("Usage: track_progress.py start <topic> <daily_goal>")
            sys.exit(1)
        topic = sys.argv[2]
        goal = sys.argv[3]
        data = start_tracking(topic, goal)
        print(f"Started tracking: {topic} ({goal}/day)")

    elif command == "checkin":
        if len(sys.argv) < 3:
            print("Usage: track_progress.py checkin <completed|partial|missed> [note]")
            sys.exit(1)
        status = sys.argv[2]
        note = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        data = log_check_in(status, note)
        print(f"Logged: {status}")
        print(get_streak_message(data["currentStreak"]))

    elif command == "stats":
        stats = get_stats()
        print(json.dumps(stats, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
