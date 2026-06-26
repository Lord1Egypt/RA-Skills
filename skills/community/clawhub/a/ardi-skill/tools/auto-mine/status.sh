#!/usr/bin/env bash
# status.sh — emit a JSON snapshot of auto-mine state.
#
# Designed for an LLM agent to consume and narrate to the user. Keep the
# fields stable; downstream may parse with jq.

set -euo pipefail

ardi_bin="$(command -v ardi-agent || true)"
runtime=""
[[ -f "$HOME/.ardi-agent/auto-mine.env" ]] && \
  runtime="$(grep -E '^ARDI_AGENT_RUNTIME=' "$HOME/.ardi-agent/auto-mine.env" | cut -d= -f2)"

# systemd unit state
timer_state="not_installed"
service_last="never"
next_tick="unknown"
if systemctl --user is-enabled ardi-mine.timer >/dev/null 2>&1; then
  timer_state="$(systemctl --user is-active ardi-mine.timer 2>/dev/null || echo unknown)"
  next_tick="$(systemctl --user list-timers ardi-mine.timer --no-pager 2>/dev/null \
               | awk 'NR==2{print $1, $2}')"
  service_last="$(systemctl --user show ardi-mine.service -p ExecMainExitTimestamp \
                  --value 2>/dev/null || echo never)"
fi

# Local commits summary (skill state, not chain state)
commits_total=0
commits_committed=0
commits_revealed=0
commits_won=0
commits_inscribed=0
commits_lost=0
if [[ -n "$ardi_bin" ]]; then
  if cj="$($ardi_bin commits 2>/dev/null)"; then
    # tolerate either pretty or compact JSON; just count keywords
    commits_total="$(echo "$cj" | grep -cE '"epoch_id"' || true)"
    commits_committed="$(echo "$cj" | grep -cE '"status"\s*:\s*"committed"' || true)"
    commits_revealed="$(echo "$cj" | grep -cE '"status"\s*:\s*"revealed"' || true)"
    commits_won="$(echo "$cj" | grep -cE '"status"\s*:\s*"won"' || true)"
    commits_inscribed="$(echo "$cj" | grep -cE '"status"\s*:\s*"inscribed"' || true)"
    commits_lost="$(echo "$cj" | grep -cE '"status"\s*:\s*"lost"' || true)"
  fi
fi

# Recent journal lines (helpful for debugging when paste'd to user)
recent_log="$(journalctl --user -u ardi-mine -n 5 --no-pager -o cat 2>/dev/null \
              | sed 's/"/\\"/g' | tr '\n' '|' | sed 's/|$//')"

cat <<EOF
{
  "timer_state": "$timer_state",
  "runtime": "$runtime",
  "ardi_agent_path": "$ardi_bin",
  "next_tick": "$next_tick",
  "service_last_exit": "$service_last",
  "local_commits": {
    "total": $commits_total,
    "committed_pending_reveal": $commits_committed,
    "revealed_pending_inscribe": $commits_revealed,
    "won_pending_inscribe": $commits_won,
    "inscribed_minted": $commits_inscribed,
    "lost": $commits_lost
  },
  "recent_log_pipe_separated": "$recent_log"
}
EOF
