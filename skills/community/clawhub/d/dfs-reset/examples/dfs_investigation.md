# DFS Detection & Reset Example

## Scenario
Operator reports that some clients at a site are experiencing intermittent connectivity issues. Suspect DFS radar events forcing APs to change channels.

## Tool Flow

**Step 1: List devices at the site**
```
→ list_devices(site="Tower-North")
← [
    {name: "TN-AP-01", ip: "10.0.1.10", model: "R5AC-Prism", ...},
    {name: "TN-AP-02", ip: "10.0.1.11", model: "R5AC-Prism", ...},
    {name: "TN-AP-03", ip: "10.0.1.12", model: "R5AC-Lite", ...}
  ]
```

**Step 2: Detect DFS events on each AP**
```
→ detect_dfs(ip="10.0.1.10")
← {configured_mhz: 5745, actual_mhz: 5745, dfs_event: false, ...}

→ detect_dfs(ip="10.0.1.11")
← {configured_mhz: 5580, actual_mhz: 5660, dfs_event: true, ...}

→ detect_dfs(ip="10.0.1.12")
← {configured_mhz: 5500, actual_mhz: 5500, dfs_event: false, ...}
```

**Step 3: Report findings**
> TN-AP-02 has a DFS event. It was configured for 5580 MHz but radar detection forced it to 5660 MHz. TN-AP-01 and TN-AP-03 are on their configured frequencies.
>
> The device is still operational on 5660 MHz. Would you like me to reset TN-AP-02 to restore it to 5580 MHz? This will briefly disconnect its clients (~1-2 minutes).

**Step 4 (after operator confirms): Reset the affected AP**
```
→ reset_device(identifier="TN-AP-02")
← {status: "reset_initiated", device: "TN-AP-02", ...}
```

**Step 5: Verify recovery (~60 seconds later)**
```
→ detect_dfs(ip="10.0.1.11")
← {configured_mhz: 5580, actual_mhz: 5580, dfs_event: false, ...}
```

> TN-AP-02 is back on its configured frequency (5580 MHz). DFS event resolved.

**Step 6 (optional): Verify client reconnection**
```
→ get_clients(ip="10.0.1.11")
← [{mac: "AA:BB:CC:DD:EE:01", signal_dbm: -68, ...}, ...]
```
