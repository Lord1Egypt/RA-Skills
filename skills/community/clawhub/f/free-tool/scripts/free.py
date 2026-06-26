#!/usr/bin/env python3
with open('/proc/meminfo') as f:
    for line in f:
        if any(x in line for x in ['MemTotal', 'MemFree', 'MemAvailable', 'SwapTotal', 'SwapFree']):
            print(line.strip())
