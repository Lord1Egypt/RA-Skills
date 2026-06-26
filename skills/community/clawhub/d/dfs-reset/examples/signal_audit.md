# Signal Audit Example

## Scenario
Operator wants a network-wide signal quality report for a specific site to identify clients that may need antenna realignment.

## Tool Flow

**Step 1: Sweep the site**
```
→ sweep_clients(site="Hilltop")
← {
    summary: {aps_total: 4, aps_ok: 3, aps_failed: 1, total_clients: 47},
    results: [
      {ap: "HT-AP-01", ip: "10.0.2.10", status: "ok", client_count: 15, clients: [
        {mac: "...", signal_dbm: -58, noise_floor_dbm: -92, ...},
        {mac: "...", signal_dbm: -72, noise_floor_dbm: -91, ...},
        ...
      ]},
      {ap: "HT-AP-02", ip: "10.0.2.11", status: "ok", client_count: 20, clients: [...]},
      {ap: "HT-AP-03", ip: "10.0.2.12", status: "error", error: "Timeout connecting to 10.0.2.12", clients: []},
      {ap: "HT-AP-04", ip: "10.0.2.13", status: "ok", client_count: 12, clients: [...]}
    ]
  }
```

**Step 2: Analyze and report**
> **Hilltop Site Signal Audit**
>
> Swept 4 APs — 3 responding, 1 unreachable (HT-AP-03 at 10.0.2.12 — timed out, may need investigation).
>
> **Clients needing attention (signal < -75 dBm):**
> | Client MAC | AP | Signal | Noise Floor | Distance |
> |---|---|---|---|---|
> | AA:BB:CC:11:22:33 | HT-AP-01 | -78 dBm | -91 dBm | 3200m |
> | DD:EE:FF:44:55:66 | HT-AP-02 | -82 dBm | -90 dBm | 5100m |
> | 11:22:33:AA:BB:CC | HT-AP-04 | -77 dBm | -92 dBm | 2800m |
>
> 3 of 47 clients are in the poor/unusable range. The client at -82 dBm on HT-AP-02 is at risk of link drops. Recommend checking antenna alignment for all three.
