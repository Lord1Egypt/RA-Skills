import json
import sys


def minutes(value):
    hour, minute = map(int, value.split(":"))
    if not 0 <= hour < 24 or not 0 <= minute < 60:
        raise ValueError("Invalid time")
    return hour * 60 + minute


def clock(value):
    return f"{value // 60:02d}:{value % 60:02d}"


def plan(data):
    start = minutes(data.get("day_start", "08:00"))
    end = minutes(data.get("day_end", "18:00"))

    if start >= end:
        raise ValueError("Invalid planning window")

    busy = []
    for event in data.get("events", []):
        a, b = minutes(event["start"]), minutes(event["end"])
        if a >= b:
            raise ValueError("Invalid event")
        busy.append((a, b))

    priorities = {"high": 0, "medium": 1, "low": 2}
    tasks = sorted(
        data.get("tasks", []),
        key=lambda task: priorities.get(task.get("priority", "medium"), 1),
    )

    scheduled = []
    unscheduled = []

    for task in tasks:
        duration = int(task["minutes"])
        if duration <= 0:
            raise ValueError("Task duration must be positive")

        cursor = start
        placed = False

        while cursor + duration <= end:
            finish = cursor + duration
            conflict = next(
                ((a, b) for a, b in sorted(busy)
                 if cursor < b and finish > a),
                None,
            )

            if conflict is None:
                scheduled.append({
                    "task": task["name"],
                    "start": clock(cursor),
                    "end": clock(finish),
                    "priority": task.get("priority", "medium"),
                })
                busy.append((cursor, finish))
                placed = True
                break

            cursor = max(cursor, conflict[1])

        if not placed:
            unscheduled.append(task["name"])

    return {
        "scheduled": sorted(scheduled, key=lambda x: x["start"]),
        "unscheduled": unscheduled,
    }


if __name__ == "__main__":
    try:
        print(json.dumps(plan(json.load(sys.stdin)), indent=2))
    except (ValueError, KeyError, TypeError) as error:
        print(f"PLANNING_ERROR: {error}", file=sys.stderr)
        sys.exit(1)
