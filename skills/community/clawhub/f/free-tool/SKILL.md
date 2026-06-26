---
name: free-tool
description: Display amount of free and used memory in the system. Use for monitoring memory usage and diagnosing performance issues.
---
# Free - Memory Usage Reporter
Show system memory statistics including total, used, free, shared, buffer/cache, and available memory. Essential for system monitoring and capacity planning.
## Usage
```bash
free-tool [options]
```
## Options
- `-h`: Human-readable output (KB/MB/GB)
- `-m`: Output in megabytes
- `-g`: Output in gigabytes
- `-t`: Show totals line
## Examples
```bash
free-tool -h
free-tool -m
free-tool -h -t
```