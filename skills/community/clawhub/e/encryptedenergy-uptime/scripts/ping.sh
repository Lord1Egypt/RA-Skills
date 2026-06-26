#!/bin/bash
# encryptedenergy-uptime ping script
# Builds a comprehensive health payload from the local openclaw CLI
# (`openclaw health --json` + `openclaw status --json`) and POSTs it to
# encryptedenergy.com so the agent status page can render it.
#
# Anything sensitive — gateway IP, channel bot identities, raw session
# keys — is intentionally left out. The payload is derived from local
# CLI output only; nothing else is read.

PING_URL="${ENCRYPTED_ENERGY_PING_URL:-https://encryptedenergy.com/api/v1/ping}"
API_KEY="${ENCRYPTED_ENERGY_API_KEY}"

if [ -z "$API_KEY" ]; then
  echo "Error: ENCRYPTED_ENERGY_API_KEY not set"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  PAYLOAD='{"ok":false,"error":"jq not installed"}'
else
  HEALTH_JSON=$(openclaw health --json --timeout 3000 2>/dev/null)
  STATUS_JSON=$(openclaw status --json --timeout 3000 2>/dev/null)
  [ -z "$HEALTH_JSON" ] && HEALTH_JSON='{}'
  [ -z "$STATUS_JSON" ] && STATUS_JSON='{}'

  PAYLOAD=$(jq -n -c \
    --argjson health "$HEALTH_JSON" \
    --argjson status "$STATUS_JSON" \
    '
    def num: . // 0;

    # Per-channel reshape: derive a single status string the ee-web
    # partial can color, plus the rich detail it should surface on
    # owner triage (lastError, probe latency, etc.).
    def channel_entry(name; raw):
      {
        (name): {
          label: ($health.channelLabels[name] // name),
          status: (
            if   raw.configured == false then "not configured"
            elif raw.running    == true  and (raw.probe.ok // false) then "connected"
            elif raw.running    == true  then "error"
            elif raw.configured == true  then "down"
            else "unknown"
            end
          ),
          configured:  raw.configured,
          running:     raw.running,
          lastError:   raw.lastError,
          lastStartAt: raw.lastStartAt,
          lastStopAt:  raw.lastStopAt,
          lastProbeAt: raw.lastProbeAt,
          tokenSource: raw.tokenSource,
          mode:        raw.mode,
          probeOk:     (raw.probe.ok // null),
          probeMs:     (raw.probe.elapsedMs // null)
        }
      };

    {
      ok:      ($health.ok // false),
      status:  (if $health.ok then "live" else "down" end),
      version: ($status.gateway.self.version // $status.runtimeVersion),

      host: (
        if $status.gateway.self.host or $status.os.label then {
          name:     ($status.gateway.self.host // null),
          platform: ($status.os.label // null)
        } else null end
      ),

      gateway: {
        reachable:        ($status.gateway.reachable // null),
        mode:             ($status.gateway.mode // null),
        connectLatencyMs: ($status.gateway.connectLatencyMs // null),
        misconfigured:    ($status.gateway.misconfigured // null)
      },

      update: (
        if $status.update or $status.updateChannel then {
          channel:     ($status.updateChannel // null),
          current:     ($status.gateway.self.version // $status.runtimeVersion),
          latest:      ($status.update.registry.latestVersion // null),
          installKind: ($status.update.installKind // null)
        } else null end
      ),

      channels: (
        [ ($health.channels // {}) | to_entries[] | channel_entry(.key; .value) ]
        | add // {}
      ),

      tasks: {
        pending:  ($status.tasks.byStatus.queued    | num),
        failed:   ($status.tasks.byStatus.failed    | num),
        lost:     ($status.tasks.byStatus.lost      | num),
        timedOut: ($status.tasks.byStatus.timed_out | num),
        active:   ($status.tasks.active             | num),
        total:    ($status.tasks.total              | num),
        byRuntime:($status.tasks.byRuntime          // {})
      },

      tokenUsage: {
        input:      ([$status.sessions.recent[]?.inputTokens]  | add // 0),
        output:     ([$status.sessions.recent[]?.outputTokens] | add // 0),
        cacheRead:  ([$status.sessions.recent[]?.cacheRead]    | add // 0),
        cacheWrite: ([$status.sessions.recent[]?.cacheWrite]   | add // 0),
        total:      ([$status.sessions.recent[]?.totalTokens]  | add // 0)
      },

      sessions: {
        count: ($status.sessions.count | num),
        topContext: (
          [ $status.sessions.recent[]?
            | { model: .model, percentUsed: (.percentUsed // 0) }
          ]
          | sort_by(-.percentUsed)
          | .[0:3]
        )
      },

      heartbeat: (
        ($health.agents // [])
        | map(select(.isDefault))
        | .[0].heartbeat // null
        | if . then {
            enabled: (.enabled // false),
            every:   (.every // null),
            everyMs: (.everyMs // null)
          } else null end
      )
    }
  ' 2>/dev/null)
fi

if [ -z "$PAYLOAD" ]; then
  PAYLOAD='{"ok":false,"error":"payload build failed"}'
fi

curl -s --max-time 10 \
  -X POST "$PING_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$PAYLOAD" \
  > /dev/null 2>&1
