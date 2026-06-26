#!/usr/bin/env python3
"""
fitness-log — Log workouts, one-shot or via live session.

One-shot (after workout):
    fitness-log "played tennis 2 hours, felt exhausted"
    fitness-log "gym: bench press 60kg x 8 x 3, squat 80kg x 5 x 4"

Live session (during workout):
    fitness-log start [type]              Begin a session (e.g. "start gym")
    fitness-log "bench press 60kg x 8 x 3"   Append to active session
    fitness-log end ["final notes"]       Finalize and save to log
    fitness-log status                    Show active session info
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fitness_skill import FitnessSkill


def print_entry(entry: dict):
    print(f"Workout logged  [{entry['date']}]")
    print(f"  Type:     {entry['type']}")
    print(f"  Duration: {entry['duration_min']} min")
    if entry["exercises"]:
        print("  Exercises:")
        for ex in entry["exercises"]:
            parts = [ex["name"]]
            if ex.get("weight_kg"):
                parts.append(f"{ex['weight_kg']}kg")
            if ex.get("sets") and ex.get("reps"):
                parts.append(f"{ex['sets']}x{ex['reps']}")
            print(f"    - {' '.join(parts)}")
    if entry["feeling"]:
        print(f"  Feeling:  {entry['feeling']}")
    if entry.get("session_meta"):
        print(f"  Messages: {entry['session_meta']['message_count']}")
    if entry["recovery_advice"]:
        print(f"\n  {entry['recovery_advice']}")


def _print_stale_notice(info: dict, auto_closed_entry: dict = None):
    """Warn the user that a stale session was found or auto-closed."""
    if auto_closed_entry:
        print("⚠️  Previous session was stale and auto-closed.")
        print(f"   Date: {auto_closed_entry['date']}  "
              f"Type: {auto_closed_entry['type']}  "
              f"Duration: {auto_closed_entry['duration_min']} min  "
              f"Exercises: {len(auto_closed_entry['exercises'])}")
        print()
    elif info and info.get("stale"):
        print("⚠️  Active session looks stale "
              f"(running for {info['elapsed_min']} min).")
        print("   It will be auto-closed on the next action.")
        print()


def main():
    skill = FitnessSkill()
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return

    cmd = args[0]

    # --- session start ---
    if cmd == "start":
        sport = args[1] if len(args) > 1 else ""
        try:
            session = skill.session_start(sport)
            print(f"Session started [{session['type']}]")
            print("Send exercises one by one, then run `fitness-log end` when done.")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        return

    # --- session end ---
    if cmd == "end":
        final_text = " ".join(args[1:]) if len(args) > 1 else ""
        try:
            entry = skill.session_end(final_text)
            print("Session ended.\n")
            print_entry(entry)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        return

    # --- session status (with stale warning) ---
    if cmd == "status":
        info = skill.session_status()
        if not info:
            print("No active session.")
        else:
            _print_stale_notice(info)
            print(f"Active session: {info['type']}")
            print(f"  Elapsed:    {info['elapsed_min']} min")
            print(f"  Idle:       {info['idle_min']} min")
            print(f"  Exercises:  {info['exercises_logged']}")
            print(f"  Messages:   {info['messages']}")
            if info["feeling"]:
                print(f"  Feeling:    {info['feeling']}")
            if info.get("should_ask"):
                print(f"\n  💡 Owner idle for {info['idle_min']} min — "
                      "consider asking if workout is done.")
        return

    # --- session append (if active) or one-shot log ---
    raw_text = " ".join(args)
    active = skill.session_status()
    if active:
        try:
            result = skill.session_append(raw_text)
            total = result["total_exercises"]
            print(f"Added to session  [total: {total} exercises]")
            if result["added_exercises"]:
                for ex in result["added_exercises"]:
                    parts = [ex["name"]]
                    if ex.get("weight_kg"):
                        parts.append(f"{ex['weight_kg']}kg")
                    if ex.get("sets") and ex.get("reps"):
                        parts.append(f"{ex['sets']}x{ex['reps']}")
                    print(f"  + {' '.join(parts)}")
            if result["feeling"]:
                print(f"  Feeling: {result['feeling']}")
        except ValueError as e:
            print(f"⚠️  {e}")
            sys.exit(1)
    else:
        entry = skill.log_workout(raw_text)
        print_entry(entry)


if __name__ == "__main__":
    main()
