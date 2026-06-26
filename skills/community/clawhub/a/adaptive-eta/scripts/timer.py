import argparse
import json
import time
import os
from pathlib import Path

# Define the path for the state file relative to the script's location
# This makes the script portable within the skill's structure.
STATE_FILE = Path(__file__).parent.parent / ".timer_state.json"

def start_timer(eta_seconds: int):
    """Starts the timer and saves the state."""
    if eta_seconds <= 0:
        print("Error: ETA must be a positive number of seconds.")
        return

    start_time = time.time()
    state = {
        "start_time": start_time,
        "eta_seconds": eta_seconds,
        "status": "RUNNING"
    }
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
        print(f"Timer started. ETA: {eta_seconds} seconds. State saved to {STATE_FILE}")
    except IOError as e:
        print(f"Error: Could not write to state file {STATE_FILE}. {e}")


def check_timer():
    """Checks the timer's status."""
    if not STATE_FILE.exists():
        print("STATUS: NOT_RUNNING")
        return

    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error: Could not read or parse state file {STATE_FILE}. {e}")
        return

    start_time = state.get("start_time", 0)
    eta_seconds = state.get("eta_seconds", 0)

    if not start_time or not eta_seconds:
        print(f"Error: Invalid state file content.")
        return

    elapsed_time = time.time() - start_time
    threshold_time = eta_seconds * 0.9

    status = "RUNNING"
    if elapsed_time >= eta_seconds:
        status = "EXPIRED"
    elif elapsed_time >= threshold_time:
        status = "THRESHOLD_REACHED"

    print(f"STATUS: {status}")
    print(f"ELAPSED_SECONDS: {elapsed_time:.2f}")
    print(f"ETA_SECONDS: {eta_seconds}")
    print(f"THRESHOLD_SECONDS: {threshold_time:.2f}")


def stop_timer():
    """Stops the timer by deleting the state file."""
    if STATE_FILE.exists():
        try:
            os.remove(STATE_FILE)
            print(f"Timer stopped. State file {STATE_FILE} removed.")
        except OSError as e:
            print(f"Error: Could not remove state file {STATE_FILE}. {e}")
    else:
        print("No active timer to stop.")

def main():
    """Main function to parse arguments and call the appropriate handler."""
    parser = argparse.ArgumentParser(description="A simple timer for Alma's long-running tasks.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Start command
    parser_start = subparsers.add_parser("start", help="Start the timer with a given ETA in seconds.")
    parser_start.add_argument("--eta", type=int, required=True, help="Estimated time in seconds.")

    # Check command
    subparsers.add_parser("check", help="Check the current status of the timer.")

    # Stop command
    subparsers.add_parser("stop", help="Stop the timer and clean up.")

    args = parser.parse_args()

    if args.command == "start":
        start_timer(args.eta)
    elif args.command == "check":
        check_timer()
    elif args.command == "stop":
        stop_timer()

if __name__ == "__main__":
    main()
