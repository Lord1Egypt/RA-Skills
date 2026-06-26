#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clawwork Learning Check-in Skill
A workplace check-in skill for Agent (小龙虾) with personalized greetings.
"""

import os
import sys
import json
import datetime
import random

# Fix Windows console encoding for UTF-8
if sys.platform == "win32":
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# Configuration
VERSION = "1.0.1"
VERSION_CHECK_URL = "https://github.com/daizongyu/clawwork_learning-checkin"

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Data will be stored in a 'data' subfolder next to the script
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
PROFILE_FILE = os.path.join(DATA_DIR, "profile.json")
GREETINGS_FILE = os.path.join(DATA_DIR, "greetings.json")
VERSION_FILE = os.path.join(DATA_DIR, "version.txt")

# Welcome message prompt for Agent (no emoji)
WELCOME_PROMPT = {
    "type": "welcome",
    "description": "Generate an energetic workplace check-in welcome message",
    "requirements": [
        "Encourage the user to start their work day",
        "Be energetic and positive",
        "Keep it concise (1-2 sentences)",
        "No emoji, plain text only",
        "In the user's preferred language"
    ],
    "examples": [
        "Time to check in and start your productive day!",
        "Ready to make today count? Let's check in!",
        "Fresh start today! Check in and let's go!"
    ]
}

# Daily greeting prompt for Agent (no emoji)
DAILY_GREETING_PROMPT = {
    "type": "daily_greeting",
    "description": "Generate a casual question to ask after check-in",
    "requirements": [
        "Be conversational and friendly",
        "Ask about their day, plans, or how they're feeling",
        "Keep it short (1 sentence)",
        "No emoji, plain text only",
        "In the user's preferred language",
        "Avoid repeating questions from the past 5 days"
    ],
    "examples": [
        "How are you feeling today?",
        "What's your plan for today?",
        "Any exciting tasks on your plate?",
        "What's top of your mind today?"
    ]
}

# Success message prompt for Agent
SUCCESS_PROMPT = {
    "type": "success",
    "description": "Generate a check-in success message with streak",
    "requirements": [
        "Congratulate the user on their check-in",
        "Include the streak count",
        "Be energetic and encouraging",
        "Keep it concise (1-2 sentences)",
        "No emoji, plain text only",
        "In the user's preferred language"
    ],
    "special_streaks": {
        "1": "First day - welcome to the streak!",
        "7": "One week streak - keep it up!",
        "30": "One month - amazing consistency!",
        "100": "100 days - you're a pro!"
    }
}


def ensure_dir():
    """Ensure data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_profile():
    """Load user profile (nickname, language, etc.)."""
    if not os.path.exists(PROFILE_FILE):
        return {
            "nickname": None,
            "language": None,
            "first_run": True,
            "initialized_at": None
        }
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "nickname": None,
            "language": None,
            "first_run": True,
            "initialized_at": None
        }


def save_profile(profile):
    """Save user profile."""
    ensure_dir()
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def load_greetings():
    """Load greeting history to avoid repetition."""
    if not os.path.exists(GREETINGS_FILE):
        return {
            "welcome_history": {},      # {"2026-03-22": "message"}
            "greeting_history": {},     # {"2026-03-22": "message"}
            "past_5_days": []           # List of recent messages for deduplication
        }
    try:
        with open(GREETINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "welcome_history": {},
            "greeting_history": {},
            "past_5_days": []
        }


def save_greetings(greetings):
    """Save greeting history."""
    ensure_dir()
    with open(GREETINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(greetings, f, ensure_ascii=False, indent=2)


def get_today():
    """Get today's date string."""
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_past_5_days():
    """Get list of past 5 days (including today)."""
    today = datetime.datetime.now()
    days = []
    for i in range(5):
        day = today - datetime.timedelta(days=i)
        days.append(day.strftime("%Y-%m-%d"))
    return days


def get_used_messages(greetings_data, msg_type):
    """Get messages used in past 5 days for a specific type."""
    past_5_days = get_past_5_days()
    history = greetings_data.get(f"{msg_type}_history", {})
    used = []
    for day in past_5_days:
        if day in history:
            msg = history[day]
            if msg:
                used.append(msg)
    return used


def register_message(msg_type, message):
    """Register a message used today for history tracking."""
    greetings_data = load_greetings()
    today = get_today()

    # Save to today's history
    history_key = f"{msg_type}_history"
    if history_key not in greetings_data:
        greetings_data[history_key] = {}

    greetings_data[history_key][today] = message

    # Update past_5_days list
    past_5_days = greetings_data.get("past_5_days", [])
    if message not in past_5_days:
        past_5_days.append(message)
    # Keep only last 10 messages (2 days worth to be safe)
    greetings_data["past_5_days"] = past_5_days[-10:]

    # Clean old entries (keep only last 7 days)
    cutoff = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    for key in ["welcome_history", "greeting_history"]:
        hist = greetings_data.get(key, {})
        filtered = {k: v for k, v in hist.items() if k >= cutoff}
        greetings_data[key] = filtered

    save_greetings(greetings_data)
    return True


def get_welcome_prompt():
    """Get welcome message generation prompt for Agent."""
    greetings_data = load_greetings()
    used_messages = get_used_messages(greetings_data, "welcome")

    result = {
        "prompt": WELCOME_PROMPT,
        "used_recently": used_messages,
        "user_language": load_profile().get("language", "en")
    }
    return result


def get_greeting_prompt():
    """Get daily greeting generation prompt for Agent."""
    greetings_data = load_greetings()
    used_messages = get_used_messages(greetings_data, "greeting")

    result = {
        "prompt": DAILY_GREETING_PROMPT,
        "used_recently": used_messages,
        "user_language": load_profile().get("language", "en")
    }
    return result


def get_success_prompt(streak):
    """Get success message generation prompt for Agent."""
    profile = load_profile()
    special = SUCCESS_PROMPT.get("special_streaks", {})

    result = {
        "prompt": SUCCESS_PROMPT,
        "streak": streak,
        "special_message": special.get(str(streak)),
        "user_language": profile.get("language", "en")
    }
    return result


def get_version():
    """Return current version."""
    return VERSION


def check_learning_checkin_installed():
    """Check if learning-checkin skill is installed."""
    # Check common locations
    possible_paths = []

    # Current directory (skill next to this one)
    possible_paths.append(os.path.join(SCRIPT_DIR, "..", "learning-checkin"))
    possible_paths.append(os.path.join(SCRIPT_DIR, "..", "learning_checkin"))

    # Parent of parent
    possible_paths.append(os.path.join(SCRIPT_DIR, "..", "..", "learning-checkin"))

    # Look in active_skills
    if "OPENCLAW_DIR" in os.environ:
        possible_paths.append(os.path.join(os.environ["OPENCLAW_DIR"], "active_skills", "learning-checkin"))

    # Check if learning_checkin.py exists in any of these paths
    for path in possible_paths:
        check_file = os.path.join(path, "learning_checkin.py")
        if os.path.exists(check_file):
            return True, path

    return False, None


# CLI Interface
def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("Usage: python clawwork_checkin.py <command> [args]")
        print("Commands:")
        print("  check-installed    - Check if learning-checkin is installed")
        print("  welcome-prompt     - Get welcome message generation prompt")
        print("  greeting-prompt    - Get daily greeting generation prompt")
        print("  success-prompt     - Get success message prompt (requires streak)")
        print("  register-welcome <msg>   - Register welcome message used today")
        print("  register-greeting <msg>  - Register daily greeting used today")
        print("  checkin            - Perform workplace check-in")
        print("  version            - Get current version")
        print("  profile            - Get user profile")
        print("  set-nickname <name> - Set user nickname")
        print("  set-language <lang> - Set user language")
        print("  status             - Get check-in status")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "check-installed":
        installed, path = check_learning_checkin_installed()
        result = {
            "installed": installed,
            "path": path,
            "needs_installation": not installed,
            "install_url": "https://clawhub.ai/daizongyu/learning-checkin"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "welcome-prompt":
        result = get_welcome_prompt()
        result["version"] = VERSION
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "greeting-prompt":
        result = get_greeting_prompt()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "success-prompt":
        streak = 0
        if len(sys.argv) >= 3:
            try:
                streak = int(sys.argv[2])
            except ValueError:
                pass
        result = get_success_prompt(streak)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "register-welcome":
        if len(sys.argv) < 3:
            print("Usage: python clawwork_checkin.py register-welcome <message>")
            sys.exit(1)
        message = " ".join(sys.argv[2:])  # Join remaining args
        register_message("welcome", message)
        result = {
            "success": True,
            "message": "Welcome message registered",
            "registered": message
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "register-greeting":
        if len(sys.argv) < 3:
            print("Usage: python clawwork_checkin.py register-greeting <message>")
            sys.exit(1)
        message = " ".join(sys.argv[2:])  # Join remaining args
        register_message("greeting", message)
        result = {
            "success": True,
            "message": "Greeting message registered",
            "registered": message
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "checkin":
        # First check if learning-checkin is installed
        installed, path = check_learning_checkin_installed()
        if not installed:
            result = {
                "success": False,
                "error": "learning-checkin not installed",
                "needs_installation": True,
                "install_url": "https://clawhub.ai/daizongyu/learning-checkin",
                "message": "Please install learning-checkin first"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)

        # Call learning-checkin's checkin command
        checkin_script = os.path.join(path, "learning_checkin.py")
        import subprocess

        try:
            proc = subprocess.run(
                [sys.executable, checkin_script, "checkin"],
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="ignore"
            )
            if proc.returncode == 0:
                try:
                    checkin_result = json.loads(proc.stdout)
                    # Get profile for personalized response
                    profile = load_profile()
                    nickname = profile.get("nickname", "friend")

                    # Get check-in streak from learning-checkin
                    streak = checkin_result.get("streak", 0)

                    # Get prompts for Agent to generate messages
                    welcome_prompt = get_welcome_prompt()
                    greeting_prompt = get_greeting_prompt()
                    success_prompt = get_success_prompt(streak)

                    result = {
                        "success": True,
                        "streak": streak,
                        "nickname": nickname,
                        "welcome_prompt": welcome_prompt["prompt"],
                        "welcome_used_recently": welcome_prompt["used_recently"],
                        "greeting_prompt": greeting_prompt["prompt"],
                        "greeting_used_recently": greeting_prompt["used_recently"],
                        "success_prompt": success_prompt["prompt"],
                        "special_streak_message": success_prompt.get("special_message"),
                        "user_language": profile.get("language", "en"),
                        "note": f"You can check for newer versions at {VERSION_CHECK_URL}"
                    }
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                except json.JSONDecodeError:
                    result = {
                        "success": True,
                        "message": "Check-in recorded!",
                        "greeting_prompt": get_greeting_prompt()["prompt"]
                    }
                    print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                result = {
                    "success": False,
                    "error": proc.stderr or "Unknown error",
                    "message": "Check-in failed"
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))
        except subprocess.TimeoutExpired:
            result = {
                "success": True,
                "message": "Check-in may have succeeded (timeout)",
                "note": "Version check timed out, skipping"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "message": "Check-in failed"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "version":
        result = {
            "version": VERSION,
            "check_url": VERSION_CHECK_URL,
            "note": "Check the URL above for the latest version"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "profile":
        profile = load_profile()
        print(json.dumps(profile, ensure_ascii=False, indent=2))

    elif command == "set-nickname":
        if len(sys.argv) < 3:
            print("Usage: python clawwork_checkin.py set-nickname <name>")
            sys.exit(1)
        nickname = sys.argv[2]
        profile = load_profile()
        profile["nickname"] = nickname
        save_profile(profile)
        result = {
            "success": True,
            "nickname": nickname,
            "message": f"Nickname set to: {nickname}"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "set-language":
        if len(sys.argv) < 3:
            print("Usage: python clawwork_checkin.py set-language <lang>")
            print("Example: python clawwork_checkin.py set-language zh")
            sys.exit(1)
        lang = sys.argv[2]
        profile = load_profile()
        profile["language"] = lang
        save_profile(profile)
        result = {
            "success": True,
            "language": lang,
            "message": f"Language set to: {lang}"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "status":
        # Check learning-checkin status
        installed, path = check_learning_checkin_installed()
        if not installed:
            result = {
                "checked_in_today": False,
                "learning_checkin_installed": False,
                "message": "Please install learning-checkin first"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(0)

        # Get status from learning-checkin
        checkin_script = os.path.join(path, "learning_checkin.py")
        import subprocess

        try:
            proc = subprocess.run(
                [sys.executable, checkin_script, "status"],
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="ignore"
            )
            if proc.returncode == 0:
                try:
                    status_result = json.loads(proc.stdout)
                    profile = load_profile()

                    result = {
                        "checked_in_today": status_result.get("checked_in_today", False),
                        "streak": status_result.get("streak", 0),
                        "total_checkins": status_result.get("total_checkins", 0),
                        "learning_checkin_installed": True,
                        "nickname": profile.get("nickname")
                    }
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                except json.JSONDecodeError:
                    result = {
                        "checked_in_today": False,
                        "learning_checkin_installed": True,
                        "error": "Failed to parse status"
                    }
                    print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                result = {
                    "checked_in_today": False,
                    "learning_checkin_installed": True,
                    "error": "Failed to get status"
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))
        except subprocess.TimeoutExpired:
            result = {
                "checked_in_today": False,
                "learning_checkin_installed": True,
                "note": "Status check timed out"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            result = {
                "checked_in_today": False,
                "learning_checkin_installed": True,
                "error": str(e)
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()