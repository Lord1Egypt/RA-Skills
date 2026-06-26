# Snapshot JSON Schema

When using `format: "json"`, the API returns a `SnapshotData` object instead of an image.

## SnapshotData

```typescript
interface SnapshotData {
  gateway: {
    status: 'up' | 'down' | 'connecting';
    version: string;
    uptime: string;
    cpu: number;
    memoryMB: number;
  } | null;

  channels: Array<{
    name: string | null;
    provider: string;
    connected: boolean;
    latencyMs: number | null;
  }> | null;

  timestamp: string; // ISO 8601
  range: string; // e.g. "6h"
  time: string; // Human-readable time string
  hostname: string;

  summary: {
    activeSessions: number;
    totalSessions: number;
    tokens: number;
    tokensDisplay: string; // e.g. "42.1k"
    errors: number;
    warnings: number;
    uptimePercent: number;
    totalMessages: number;
  } | null;

  tokensByModel: Array<{
    model: string; // e.g. "anthropic/claude-opus-4-5"
    modelDisplay: string; // e.g. "Claude Opus 4.5"
    tokensK: number;
    percent: number;
  }> | null;

  tokensTrend?: string; // e.g. "↑12%" or "↓5%" (⚠️ prefix when >100%)

  buckets?: Array<{
    sessions?: number;
    tokensK?: number;
    tokens?: number;
    errors?: number;
    warnings?: number;
    uptimePercent?: number;
  }> | null;

  sessions?: Array<{
    name: string;
    status: string;
    model: string;
    modelDisplay: string;
    channel: string;
    totalTokens: number;
    totalTokensDisplay: string;
    usagePercent: number;
    updatedAt: string;
    turnCount: number;
    subAgentCount: number;
    subAgents?: Array<{
      name: string;
      status: string;
      completed: boolean;
      updatedAt: string;
    }>;
  }> | null;

  recentErrors?: Array<{
    timestamp: string;
    type: string;
    module: string;
    message: string;
  }> | null;

  companionDays: number | null;
  totalConversations: number | null;

  _meta?: {
    degradedSources: string[]; // Sources that failed to load
  };
}
```

## Field Notes

| Field           | When null              | Notes                                                                                                                                           |
| --------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `gateway`       | Gateway unreachable    | `version` is the Claw Insights app version (not gateway CLI version). Includes CPU/memory of the gateway process.                               |
| `channels`      | No channels configured | Provider names: telegram, discord, slack, etc.                                                                                                  |
| `summary`       | No data for range      | `tokensDisplay` is pre-formatted (e.g. "1.2k")                                                                                                  |
| `tokensByModel` | No token data          | Sorted by usage descending, `percent` sums to 100                                                                                               |
| `sessions`      | No active sessions     | Includes sub-agent tree when `detail=full`                                                                                                      |
| `recentErrors`  | No errors in range     | Only present when `detail=standard` or `full`                                                                                                   |
| `buckets`       | No metrics data        | Time-series bins for charts. All fields optional: `sessions` (peak), `tokensK`/`tokens` (sum), `errors`/`warnings` (sum), `uptimePercent` (min) |
| `_meta`         | All sources healthy    | Lists degraded data sources for transparency                                                                                                    |

## Example Response

```json
{
  "gateway": {
    "status": "up",
    "version": "1.2.3",
    "uptime": "3d 14h",
    "cpu": 2.4,
    "memoryMB": 128
  },
  "channels": [{ "name": "main", "provider": "telegram", "connected": true, "latencyMs": 45 }],
  "timestamp": "2026-03-13T15:30:00.000Z",
  "range": "6h",
  "time": "Mar 13, 15:30",
  "hostname": "my-server",
  "summary": {
    "activeSessions": 3,
    "totalSessions": 12,
    "tokens": 42100,
    "tokensDisplay": "42.1k",
    "errors": 2,
    "warnings": 5,
    "uptimePercent": 99.8,
    "totalMessages": 156
  },
  "tokensByModel": [
    { "model": "anthropic/claude-opus-4-5", "modelDisplay": "Claude Opus 4.5", "tokensK": 28.3, "percent": 67 },
    { "model": "anthropic/claude-sonnet-4", "modelDisplay": "Claude Sonnet 4", "tokensK": 13.8, "percent": 33 }
  ],
  "tokensTrend": "↑12%",
  "companionDays": 42,
  "totalConversations": 1580
}
```
