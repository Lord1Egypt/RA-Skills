#!/usr/bin/env python3
"""Discord Event Planner - Event management script"""

import json
import sys
import os
import uuid
from datetime import datetime

EVENTS_FILE = "events.json"

def load_events():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"events": {}, "next_id": 1}

def save_events(data):
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def create_event(title, date, time, description=""):
    data = load_events()
    event_id = f"evt_{data['next_id']:03d}"
    data["events"][event_id] = {
        "id": event_id,
        "title": title,
        "date": date,
        "time": time,
        "description": description,
        "rsvps": {"attend": [], "maybe": [], "decline": []}
    }
    data["next_id"] += 1
    save_events(data)
    print(f"[CREATED] Event '{title}' ({event_id}) on {date} at {time}")

def list_events():
    data = load_events()
    if not data["events"]:
        print("No events scheduled.")
        return
    
    sorted_events = sorted(data["events"].items(), 
                         key=lambda x: (x[1]["date"], x[1]["time"]))
    
    for event_id, evt in sorted_events:
        attend = len(evt["rsvps"]["attend"])
        maybe = len(evt["rsvps"]["maybe"])
        print(f"\n{event_id}: {evt['title']}")
        print(f"  Date: {evt['date']} at {evt['time']}")
        if evt['description']:
            print(f"  Info: {evt['description']}")
        print(f"  RSVPs: {attend} attending, {maybe} maybe")

def rsvp_event(event_id, status):
    data = load_events()
    if event_id not in data["events"]:
        print(f"[ERROR] Event '{event_id}' not found")
        return
    
    evt = data["events"][event_id]
    # Remove from all lists first
    for lst in evt["rsvps"].values():
        if "user" in lst:
            lst.remove("user")
    
    if status in ["attend", "maybe", "decline"]:
        evt["rsvps"][status].append("user")
        save_events(data)
        print(f"[RSVP] Updated for '{evt['title']}' - {status}")
    else:
        print("[ERROR] Status must be: attend, maybe, or decline")

def show_event(event_id):
    data = load_events()
    if event_id not in data["events"]:
        print(f"[ERROR] Event '{event_id}' not found")
        return
    
    evt = data["events"][event_id]
    print(f"\n=== {evt['title']} ===")
    print(f"ID: {event_id}")
    print(f"Date: {evt['date']} at {evt['time']}")
    if evt['description']:
        print(f"Description: {evt['description']}")
    print(f"\nRSVPs:")
    print(f"  Attending: {', '.join(evt['rsvps']['attend']) or 'none'}")
    print(f"  Maybe: {', '.join(evt['rsvps']['maybe']) or 'none'}")
    print(f"  Declined: {', '.join(evt['rsvps']['decline']) or 'none'}")

def cancel_event(event_id):
    data = load_events()
    if event_id not in data["events"]:
        print(f"[ERROR] Event '{event_id}' not found")
        return
    
    evt = data["events"].pop(event_id)
    save_events(data)
    print(f"[CANCELLED] Event '{evt['title']}' has been removed")

def main():
    if len(sys.argv) < 2:
        print("Usage: event_manager.py <command> [args]")
        print("Commands: create, list, rsvp, show, cancel")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "create" and len(sys.argv) >= 5:
        create_event(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "")
    elif cmd == "list":
        list_events()
    elif cmd == "rsvp" and len(sys.argv) >= 4:
        rsvp_event(sys.argv[2], sys.argv[3])
    elif cmd == "show" and len(sys.argv) >= 3:
        show_event(sys.argv[2])
    elif cmd == "cancel" and len(sys.argv) >= 3:
        cancel_event(sys.argv[2])
    else:
        print("[ERROR] Invalid command or missing arguments")

if __name__ == "__main__":
    main()