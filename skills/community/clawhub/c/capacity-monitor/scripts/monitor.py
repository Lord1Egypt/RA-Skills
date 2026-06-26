# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime


def run():
    cpu_idle = 75.0
    mem_available_mb = 4096

    try:
        loadavg = open("/proc/loadavg").read().strip()
        parts = loadavg.split()
        load_1min = float(parts[0])
        cpu_count = os.cpu_count() or 1
        cpu_idle = max(0, (1 - load_1min / cpu_count) * 100)
    except Exception:
        pass

    try:
        meminfo = open("/proc/meminfo").read()
        for line in meminfo.split("\n"):
            if line.startswith("MemAvailable:"):
                mem_available_mb = int(line.split()[1]) / 1024
                break
    except Exception:
        pass

    return {
        "monitor_timestamp": datetime.utcnow().isoformat(),
        "cpu_percent_idle": round(cpu_idle, 1),
        "memory_mb_available": round(mem_available_mb, 0),
        "status": "completed",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
