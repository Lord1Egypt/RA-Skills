# Device Reset Workflow Example

## Scenario
Operator reports that an AP seems unresponsive to clients but is still pingable. Wants to try a reset.

## Tool Flow

**Step 1: Confirm device identity**
```
→ get_device(identifier="Valley-AP-05")
← {name: "Valley-AP-05", model: "R5AC-Prism", ip: "10.0.3.15",
    site: "Valley", status: "active", firmware: "8.7.11", device_id: "abc123..."}
```

**Step 2: Check for DFS event and current state**
```
→ detect_dfs(ip="10.0.3.15")
← {configured_mhz: 5580, actual_mhz: 5580, dfs_event: false, ...}

→ get_device_stats(ip="10.0.3.15")
← {hostname: "Valley-AP-05", model: "R5AC-Prism", firmware: "8.7.11",
    uptime_seconds: 8640000, cpu_load_percent: 95, memory_used_percent: 88,
    temperature_c: 72}
```

**Step 3: Report and ask for confirmation**
> Valley-AP-05 (10.0.3.15) is a Rocket 5AC Prism at the Valley site.
> - No DFS event — operating on configured frequency (5580 MHz)
> - CPU load: 95% (very high)
> - Memory: 88% used
> - Temperature: 72°C
> - Uptime: 100 days
>
> High CPU and memory suggest the device is overloaded — a reset should help.
> **Shall I proceed with resetting Valley-AP-05?** This will disconnect all clients on this AP temporarily (~1-2 minutes).

**Step 4: Reset (only after operator confirms)**
```
→ reset_device(identifier="Valley-AP-05")
← {status: "reset_initiated", device: "Valley-AP-05",
    device_id: "abc123...", timestamp: "2026-04-10T15:30:00Z"}
```

**Step 5: Verify recovery (~60 seconds later)**
```
→ detect_dfs(ip="10.0.3.15")
← {configured_mhz: 5580, actual_mhz: 5580, dfs_event: false, ...}

→ get_device_stats(ip="10.0.3.15")
← {hostname: "Valley-AP-05", uptime_seconds: 45, cpu_load_percent: 12,
    memory_used_percent: 34, temperature_c: 55}
```

> Valley-AP-05 is back online on its configured frequency (5580 MHz). Uptime: 45 seconds, CPU: 12%, memory: 34%. The reset resolved the resource exhaustion. Monitor over the next hour to see if the issue recurs.
