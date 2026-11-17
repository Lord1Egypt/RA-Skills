#!/usr/bin/env bash
# replay_reserve cache ttl capacity peer message-id [now]; 0=new, 2=replay, 3=fail closed.

replay_capacity_for_window() {
  local ttl="$1" global_per_minute="$2" minutes
  [[ "$ttl" =~ ^[1-9][0-9]*$ && "$global_per_minute" =~ ^[1-9][0-9]*$ ]] || return 1
  minutes=$(( (ttl + 59) / 60 + 2 ))
  printf '%s\n' "$((minutes * global_per_minute))"
}

replay_cache_valid() {
  jq -e '
    type == "object" and (keys == ["entries"]) and (.entries | type == "array") and
    all(.entries[];
      type == "object" and (keys | sort == ["id", "peer", "seen"]) and
      (.peer | type == "string" and length > 0) and
      (.id | type == "string" and test("^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")) and
      (.seen | type == "number" and floor == . and . >= 0))
  ' "$1" >/dev/null 2>&1
}

replay_reserve() {
  local cache="$1" ttl="$2" capacity="$3" peer="$4" id="$5" now="${6:-$(date +%s)}"
  local dir lock tmp next fd rc=3
  dir=$(dirname "$cache"); lock="${cache}.lock"
  [[ ! -L "$dir" && ( ! -e "$dir" || -d "$dir" ) ]] || return 3
  mkdir -p "$dir" && chmod 0700 "$dir" || return 3
  [[ ! -L "$lock" && ( ! -e "$lock" || -f "$lock" ) ]] || return 3
  touch "$lock" && chmod 0600 "$lock" || return 3
  exec {fd}>>"$lock" || return 3
  flock -x "$fd" || { exec {fd}>&-; return 3; }
  [[ ! -L "$cache" && ( ! -e "$cache" || -f "$cache" ) ]] || { exec {fd}>&-; return 3; }
  tmp=$(mktemp "$dir/.replay.XXXXXX") || { exec {fd}>&-; return 3; }
  next=$(mktemp "$dir/.replay-next.XXXXXX") || { rm -f "$tmp"; exec {fd}>&-; return 3; }
  chmod 0600 "$tmp" "$next" || { rm -f "$tmp" "$next"; exec {fd}>&-; return 3; }
  if [[ -f "$cache" ]] && ! replay_cache_valid "$cache"; then
    rm -f "$tmp" "$next"; exec {fd}>&-; return 3
  fi
  if [[ -f "$cache" ]]; then
    jq --argjson cutoff "$((now - ttl))" '{entries:[.entries[] | select(.seen > $cutoff)]}' "$cache" >"$tmp" 2>/dev/null || true
  else
    printf '{"entries":[]}' >"$tmp"
  fi
  if ! replay_cache_valid "$tmp"; then :
  elif jq -e --arg p "$peer" --arg id "$id" 'any(.entries[]; .peer == $p and .id == $id)' "$tmp" >/dev/null; then
    mv -T "$tmp" "$cache" && rc=2
  elif jq --arg p "$peer" --arg id "$id" --argjson now "$now" '.entries += [{peer:$p,id:$id,seen:$now}]' "$tmp" >"$next" &&
       (( $(jq '.entries | length' "$next") <= capacity )) && mv -T "$next" "$cache"; then
    chmod 0600 "$cache" && rc=0
  fi
  rm -f "$tmp" "$next"; exec {fd}>&-; return "$rc"
}
