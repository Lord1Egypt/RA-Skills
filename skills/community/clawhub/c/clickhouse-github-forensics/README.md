# clickhouse-github-forensics

Query 10+ billion GitHub events for supply chain investigations, actor profiling, and incident timeline reconstruction.

## What It Does

Uses [ClickHouse's public GitHub events dataset](https://ghe.clickhouse.tech/) to investigate:
- **Supply chain attacks** — tag poisoning, release tampering, compromised CI/CD
- **Actor behavior** — account history, first-time access patterns, anomalies
- **Incident timelines** — minute-by-minute reconstruction from public events

## Origin

Built during the [Trivy supply chain compromise investigation](https://socket.dev/blog/trivy-under-attack-again-github-actions-compromise) (March 2026) where it was used to:
- Reconstruct the full attack timeline from ClickHouse data
- Identify the compromised `aqua-bot` service account
- Discover additional affected repos (`traceeshark`, `setup-trivy`) not in initial reports
- Verify responder accounts as legitimate maintainers

## Quick Start

```bash
curl -s "https://play.clickhouse.com/?user=play" \
  --data "SELECT created_at, event_type, actor_login, repo_name
          FROM github_events 
          WHERE repo_name = 'aquasecurity/trivy-action'
          AND created_at >= '2026-03-19'
          ORDER BY created_at
          FORMAT PrettyCompact"
```

## Author

**Rufio** @ [Permiso Security](https://permiso.io)

## License

MIT
