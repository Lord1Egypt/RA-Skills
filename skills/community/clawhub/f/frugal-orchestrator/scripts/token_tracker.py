#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

TRACKER_FILE = Path("/a0/usr/projects/frugal_orchestrator/logs/tokens.toon")

class TokenTracker:
    """Token tracking for logging and statistics."""

    def __init__(self):
        self.tracker_file = TRACKER_FILE

    def log_record(self, args):
        self.tracker_file.parent.mkdir(parents=True, exist_ok=True)
        task_type, task_map = args[0], args[1]
        tokens_ai = int(args[2])
        tokens_exec = int(args[3])
        success = args[4].lower() == 'true'
        duration = float(args[5]) if len(args) > 5 else 0.0
        savings = tokens_ai - tokens_exec
        savings_pct = (savings / tokens_ai * 100) if tokens_ai > 0 else 0

        ts = datetime.now().isoformat()
        lines = [
            "timestamp: " + ts,
            "task_type: " + task_type,
            "task_map: " + task_map,
            "tokens_ai_estimate: " + str(tokens_ai),
            "tokens_executed: " + str(tokens_exec),
            "token_savings: " + str(savings),
            "savings_pct: " + str(round(savings_pct, 2)),
            "success: " + str(success),
            "duration_ms: " + str(duration)
        ]
        record = "\n".join(lines)

        with open(self.tracker_file, 'a') as f:
            f.write(record + "\n---\n")

        return {"status": "recorded"}

    def get_stats(self):
        if not self.tracker_file.exists():
            return {"task_count": 0, "total_savings": 0}

        records = []
        blocks = self.tracker_file.read_text().split('---')

        for block in blocks:
            lines = [l.strip() for l in block.split(chr(10)) if l.strip() and not l.strip().startswith('#')]
            rec = {}
            for line in lines:
                if ':' in line:
                    key, val = line.split(':', 1)
                    key = key.strip()
                    val = val.strip()
                    try:
                        if key in ['tokens_ai_estimate', 'tokens_executed', 'token_savings']:
                            val = int(val)
                        elif key in ['savings_pct', 'duration_ms']:
                            val = float(val)
                        elif key == 'success':
                            val = val.lower() == 'true'
                    except:
                        pass
                    rec[key] = val
            if rec and 'task_type' in rec:
                records.append(rec)

        if not records:
            return {"task_count": 0, "total_savings": 0}

        total_ai = sum(r.get('tokens_ai_estimate', 0) for r in records)
        total_exec = sum(r.get('tokens_executed', 0) for r in records)
        successful = sum(1 for r in records if r.get('success'))

        stats = {
            "task_count": len(records),
            "total_savings": total_ai - total_exec,
            "total_ai_tokens": total_ai,
            "total_executed_tokens": total_exec,
            "avg_savings_pct": round((total_ai - total_exec) / total_ai * 100, 2) if total_ai > 0 else 0,
            "success_rate": round(successful / len(records) * 100, 2) if records else 0
        }
        return stats

def main():
    import sys
    tracker = TokenTracker()
    if len(sys.argv) < 2:
        print(json.dumps(tracker.get_stats(), indent=2))
        return

    cmd = sys.argv[1]
    if cmd == 'stats':
        print(json.dumps(tracker.get_stats(), indent=2))
    elif cmd == 'record' and len(sys.argv) >= 7:
        result = tracker.log_record(sys.argv[2:])
        print(json.dumps(result))
    else:
        print(json.dumps(tracker.get_stats(), indent=2))

if __name__ == '__main__':
    main()
