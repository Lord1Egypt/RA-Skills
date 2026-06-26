# Cluster Gateway Node Skill

**Status:** 🚧 Vorbereitend - Wartet auf Messaging-Schnittstelle

## Zweck
Verwaltet das OpenClaw Gateway als zentraler Hub für Sub-Agent-Kommunikation, Task-Verteilung und Cluster-Koordination.

## Verwendung
```bash
# Gateway-Status prüfen
openclaw cluster gateway status

# Sub-Agent auf Node deployen
openclaw cluster gateway deploy --node <node-id> --agent <agent-type>

# Task an Worker Node senden
openclaw cluster gateway task --target <node-id> --command "<task>"

# Relay Node konfigurieren
openclaw cluster gateway relay --enable --node <node-id>
```

## Architektur

```
┌─────────────────────────────────────┐
│         CLUSTER GATEWAY              │
│        (Node 1 - Haupt-Hub)          │
├─────────────────────────────────────┤
│  • Task Queue                         │
│  • Node Registry                      │
│  • Sub-Agent Orchestration            │
│  • Resource Scheduler                 │
│  • Messaging Router (zukünftig)       │
└──────────────┬──────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌──▼───┐  ┌───▼──┐
│ Node 2│  │Node 3│  │Node 4│
│Worker │  │Relay │  │Worker│
└───────┘  └──────┘  └──────┘
```

## Node-Typen

| Typ | Funktion | Beispiel |
|-----|----------|----------|
| `gateway` | Zentraler Hub | Node 1 |
| `worker` | Task-Ausführung | Node 2, Node 4 |
| `relay` | Weiterleitung/Proxy | Node 3 |
| `storage` | Datenspeicherung | Node 5 |

## Konfiguration

```json
// cluster-gateway.config.json
{
  "gateway": {
    "id": "node-1",
    "role": "hub",
    "bind": "0.0.0.0",
    "port": 18789
  },
  "nodes": [
    {"id": "node-2", "role": "worker", "host": "10.10.0.2"},
    {"id": "node-3", "role": "relay", "host": "10.10.0.3"},
    {"id": "node-4", "role": "worker", "host": "10.10.0.4"}
  ],
  "messaging": {
    "enabled": false,
    "provider": "pending"
  }
}
```

## Offene Punkte (Blocker)
- [ ] Messaging-Schnittstelle wählen (Slack/WebChat/GMX/SMTP/anderes)
- [ ] Node 4 (Redmi) Anbindung abschließen
- [ ] SMTP-Tests durchführen
- [ ] Alerting-System implementieren

## Siehe auch
- [Worker Node Skill](../worker-node/SKILL.md)
- [Relay Node Skill](../relay-node/SKILL.md)
- [Resource Manager Skill](../resource-manager/SKILL.md)
