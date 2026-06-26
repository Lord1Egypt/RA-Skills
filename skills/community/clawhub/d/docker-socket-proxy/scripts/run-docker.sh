#!/usr/bin/env bash
set -euo pipefail

# Resolve proxy URL
if [[ -n "${DOCKER_PROXY_URL:-}" ]]; then
  BASE_URL="${DOCKER_PROXY_URL}"
elif [[ -n "${DOCKER_HOST:-}" ]]; then
  BASE_URL="${DOCKER_HOST/tcp:\/\//http://}"
else
  BASE_URL="http://localhost:2375"
fi
BASE_URL="${BASE_URL%/}"

# Print TSV as an aligned table (column -t replacement)
fmt_table() {
  awk -F'\t' '
    { rows[NR] = $0; for (i=1;i<=NF;i++) if (length($i)>w[i]) w[i]=length($i) }
    END { for (r=1;r<=NR;r++) {
      n = split(rows[r], f, "\t")
      for (i=1;i<=n;i++) printf "%-*s%s", w[i], f[i], (i<n ? "  " : "\n")
    }}
  '
}

mode="${1:-}"
if [[ -z "$mode" ]]; then
  cat >&2 <<'EOF'
Usage: run-docker.sh <mode> [args...]

System:
  ping                        Health check
  version                     Docker version
  info                        Docker host info
  events [--since T] [--until T] [--filters k=v...]  Stream events (non-blocking, 1s window)
  system-df                   Disk usage

Containers:
  list                        Running containers
  list-all                    All containers
  inspect <name>              Container details
  top <name> [ps-args]        Running processes
  logs <name> [tail]          Container logs (default tail=100)
  stats <name>                CPU/memory stats
  changes <name>              Filesystem changes
  start <name>                Start container
  stop <name> [timeout]       Stop container
  restart <name> [timeout]    Restart container
  kill <name> [signal]        Kill container (default SIGKILL)
  pause <name>                Pause container
  unpause <name>              Unpause container
  rename <name> <new-name>    Rename container
  exec <name> <cmd> [args...] Run command in container
  prune-containers            Remove stopped containers

Images:
  images                      List images
  image-inspect <name>        Image details
  image-history <name>        Image layer history
  prune-images                Remove unused images

Networks:
  networks                    List networks
  network-inspect <name>      Network details
  prune-networks              Remove unused networks

Volumes:
  volumes                     List volumes
  volume-inspect <name>       Volume details
  prune-volumes               Remove unused volumes

Swarm:
  swarm                       Swarm info
  nodes                       List swarm nodes
  node-inspect <name>         Node details
  services                    List swarm services
  service-inspect <name>      Service details
  service-logs <name> [tail]  Service logs
  tasks                       List swarm tasks
  configs                     List swarm configs
  secrets                     List swarm secrets (if enabled)

Plugins:
  plugins                     List plugins
EOF
  exit 1
fi

# HTTP helpers

docker_req() {
  local method="$1" path="$2" body="${3:-}"
  local args=(-sf --write-out $'\n%{http_code}' -X "$method")
  [[ -n "$body" ]] && args+=(-H 'Content-Type: application/json' -d "$body")
  local response http_code body_out
  response=$(curl "${args[@]}" "${BASE_URL}${path}" 2>&1) || {
    echo "Error: request to ${BASE_URL}${path} failed" >&2; exit 1
  }
  http_code=$(tail -n1 <<< "$response")
  body_out=$(head -n -1 <<< "$response")
  if [[ "$http_code" -ge 400 ]]; then
    echo "Error: HTTP $http_code from ${path}" >&2
    echo "$body_out" | jq -r '.message // empty' 2>/dev/null >&2 || true
    exit 1
  fi
  echo "$body_out"
}

docker_get()  { docker_req GET  "$1"; }
docker_post() { docker_req POST "$1" "${2:-}"; }

# Strip Docker's 8-byte multiplexed stream frame headers and print clean text
strip_frames() { strings; }

# Resolve container name to ID (exact match, then substring)
resolve_container() {
  local input="$1"
  local all
  all=$(docker_get "/containers/json?all=1")
  local matches
  matches=$(echo "$all" | jq -r '.[] | .Id + " " + (.Names[0] | ltrimstr("/"))' | \
    awk -v q="$input" '$2 == q { print; next } index($2, q) { print }')
  if [[ -z "$matches" ]]; then
    echo "Error: no container matching '${input}'" >&2; exit 1
  fi
  local count
  count=$(echo "$matches" | grep -c .)
  if [[ "$count" -gt 1 ]]; then
    echo "Error: ambiguous name '${input}', matches:" >&2
    echo "$matches" | awk '{print "  " $2}' >&2; exit 1
  fi
  echo "$matches" | awk '{print $1}'
}

# Resolve image name to ID (exact RepoTag match, then substring)
resolve_image() {
  local input="$1"
  local all
  all=$(docker_get "/images/json?all=1")
  local matches
  matches=$(echo "$all" | jq -r '.[] | .Id + " " + ((.RepoTags // []) | join(" "))' | \
    awk -v q="$input" 'index($0, q) { print $1; exit }')
  if [[ -z "$matches" ]]; then
    echo "$input"  # fall back to passing name directly to API
  else
    echo "$matches"
  fi
}

# Resolve network/volume/service/node/config/secret by name substring
resolve_named() {
  local endpoint="$1" field="$2" input="$3"
  local all
  all=$(docker_get "$endpoint")
  local matches
  matches=$(echo "$all" | jq -r --arg q "$input" --arg f "$field" \
    '.[] | select(.[$f] | test($q; "i")) | .ID // .Id')
  if [[ -z "$matches" ]]; then
    echo "$input"  # fall back: pass name directly
  else
    echo "$matches" | head -1
  fi
}

case "$mode" in

  # ── System ──────────────────────────────────────────────────────────────────

  ping)
    result=$(docker_get "/_ping")
    echo "OK: $result"
    ;;

  version)
    docker_get "/version" | jq '{
      Version: .Version,
      ApiVersion: .ApiVersion,
      Os: .Os,
      Arch: .Arch,
      KernelVersion: .KernelVersion,
      BuildTime: .BuildTime
    }'
    ;;

  info)
    docker_get "/info" | jq '{
      Name: .Name,
      Containers: .Containers,
      ContainersRunning: .ContainersRunning,
      ContainersPaused: .ContainersPaused,
      ContainersStopped: .ContainersStopped,
      Images: .Images,
      ServerVersion: .ServerVersion,
      MemTotal: (.MemTotal / 1073741824 * 100 | round / 100 | tostring + " GB")
    }'
    ;;

  events)
    shift
    local_args=""
    since="" until_t="" filters=()
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --since) since="$2"; shift 2 ;;
        --until) until_t="$2"; shift 2 ;;
        --filters) filters+=("filters=$2"); shift 2 ;;
        *) shift ;;
      esac
    done
    qs="until=$(($(date +%s) + 1))"
    [[ -n "$since" ]] && qs="since=${since}&${qs}"
    for f in "${filters[@]}"; do qs="${qs}&${f}"; done
    curl -sf "${BASE_URL}/events?${qs}" | jq -r '
      "\(.time | todate) \(.Type) \(.Action) \(.Actor.Attributes.name // .Actor.ID[:12])"'
    ;;

  system-df)
    docker_get "/system/df" | jq '{
      Images: {
        count: (.Images | length),
        active: ([.Images[] | select(.Containers > 0)] | length),
        reclaimable: .LayersSize
      },
      Containers: {
        count: (.Containers | length),
        running: ([.Containers[] | select(.State == "running")] | length),
        reclaimable: ([.Containers[] | select(.State != "running") | .SizeRootFs] | add // 0)
      },
      Volumes: {
        count: (.Volumes | length),
        reclaimable: ([.Volumes[] | select(.UsageData.RefCount == 0) | .UsageData.Size] | add // 0)
      }
    }'
    ;;

  # ── Containers ──────────────────────────────────────────────────────────────

  list)
    docker_get "/containers/json" | jq -r '
      ["NAME","IMAGE","STATUS","PORTS"],
      (.[] | [
        (.Names[0] | ltrimstr("/")),
        (.Image | split(":")[0] | split("/")[-1]),
        .Status,
        ([.Ports[] | select(.PublicPort) | "\(.PublicPort)->\(.PrivatePort)/\(.Type)"] | join(", "))
      ]) | @tsv' | fmt_table
    ;;

  list-all)
    docker_get "/containers/json?all=1" | jq -r '
      ["NAME","IMAGE","STATUS","STATE"],
      (.[] | [
        (.Names[0] | ltrimstr("/")),
        (.Image | split(":")[0] | split("/")[-1]),
        .Status,
        .State
      ]) | @tsv' | fmt_table
    ;;

  inspect)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 inspect <name>" >&2; exit 1; }
    id=$(resolve_container "$name")
    docker_get "/containers/${id}/json" | jq '{
      Name: (.Name | ltrimstr("/")),
      Image: .Config.Image,
      State: .State.Status,
      StartedAt: .State.StartedAt,
      FinishedAt: .State.FinishedAt,
      RestartPolicy: .HostConfig.RestartPolicy.Name,
      RestartCount: .RestartCount,
      Mounts: [.Mounts[] | {src: .Source, dst: .Destination, mode: .Mode}],
      Env: .Config.Env,
      Labels: .Config.Labels,
      Ports: .NetworkSettings.Ports,
      Networks: (.NetworkSettings.Networks | keys)
    }'
    ;;

  top)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 top <name> [ps-args]" >&2; exit 1; }
    ps_args="${3:-aux}"
    id=$(resolve_container "$name")
    docker_get "/containers/${id}/top?ps_args=${ps_args}" | jq -r '
      .Titles,
      (.Processes[]) | @tsv' | fmt_table
    ;;

  logs)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 logs <name> [tail]" >&2; exit 1; }
    tail="${3:-100}"
    id=$(resolve_container "$name")
    curl -sf "${BASE_URL}/containers/${id}/logs?stdout=1&stderr=1&tail=${tail}" | strip_frames
    ;;

  stats)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 stats <name>" >&2; exit 1; }
    id=$(resolve_container "$name")
    docker_get "/containers/${id}/stats?stream=false" | jq '
      def cpu_pct:
        ((.cpu_stats.cpu_usage.total_usage - .precpu_stats.cpu_usage.total_usage) /
         (.cpu_stats.system_cpu_usage - .precpu_stats.system_cpu_usage)) *
        (.cpu_stats.online_cpus // (.cpu_stats.cpu_usage.percpu_usage | length)) * 100
        | . * 100 | round / 100;
      def mem_mb: .memory_stats.usage / 1048576 | . * 10 | round / 10;
      def mem_limit_mb: .memory_stats.limit / 1048576 | round;
      {
        cpu_percent: (cpu_pct | tostring + "%"),
        mem_usage_mb: (mem_mb | tostring + " MB"),
        mem_limit_mb: (mem_limit_mb | tostring + " MB"),
        mem_percent: (((.memory_stats.usage / .memory_stats.limit) * 100) | . * 10 | round / 10 | tostring + "%"),
        net_rx_mb: (([.networks // {} | .[] | .rx_bytes] | add // 0) / 1048576 | . * 10 | round / 10 | tostring + " MB"),
        net_tx_mb: (([.networks // {} | .[] | .tx_bytes] | add // 0) / 1048576 | . * 10 | round / 10 | tostring + " MB"),
        block_read_mb: ((.blkio_stats.io_service_bytes_recursive // [] | map(select(.op=="read")) | .[0].value // 0) / 1048576 | . * 10 | round / 10 | tostring + " MB"),
        block_write_mb: ((.blkio_stats.io_service_bytes_recursive // [] | map(select(.op=="write")) | .[0].value // 0) / 1048576 | . * 10 | round / 10 | tostring + " MB")
      }'
    ;;

  changes)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 changes <name>" >&2; exit 1; }
    id=$(resolve_container "$name")
    docker_get "/containers/${id}/changes" | jq -r '.[] | "\(if .Kind==0 then "C" elif .Kind==1 then "A" else "D" end) \(.Path)"'
    ;;

  start)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 start <name>" >&2; exit 1; }
    id=$(resolve_container "$name")
    docker_post "/containers/${id}/start"
    echo "Started: ${name}"
    ;;

  stop)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 stop <name> [timeout]" >&2; exit 1; }
    timeout="${3:-}"
    id=$(resolve_container "$name")
    qs=""; [[ -n "$timeout" ]] && qs="?t=${timeout}"
    docker_post "/containers/${id}/stop${qs}"
    echo "Stopped: ${name}"
    ;;

  restart)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 restart <name> [timeout]" >&2; exit 1; }
    timeout="${3:-}"
    id=$(resolve_container "$name")
    qs=""; [[ -n "$timeout" ]] && qs="?t=${timeout}"
    docker_post "/containers/${id}/restart${qs}"
    echo "Restarted: ${name}"
    ;;

  kill)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 kill <name> [signal]" >&2; exit 1; }
    signal="${3:-SIGKILL}"
    id=$(resolve_container "$name")
    docker_post "/containers/${id}/kill?signal=${signal}"
    echo "Killed: ${name} (${signal})"
    ;;

  pause)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 pause <name>" >&2; exit 1; }
    id=$(resolve_container "$name")
    docker_post "/containers/${id}/pause"
    echo "Paused: ${name}"
    ;;

  unpause)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 unpause <name>" >&2; exit 1; }
    id=$(resolve_container "$name")
    docker_post "/containers/${id}/unpause"
    echo "Unpaused: ${name}"
    ;;

  rename)
    name="${2:-}"; new_name="${3:-}"
    [[ -z "$name" || -z "$new_name" ]] && { echo "Usage: $0 rename <name> <new-name>" >&2; exit 1; }
    id=$(resolve_container "$name")
    docker_post "/containers/${id}/rename?name=${new_name}"
    echo "Renamed: ${name} → ${new_name}"
    ;;

  exec)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 exec <name> <cmd> [args...]" >&2; exit 1; }
    shift 2
    [[ $# -eq 0 ]] && { echo "Usage: $0 exec <name> <cmd> [args...]" >&2; exit 1; }
    id=$(resolve_container "$name")
    cmd_json=$(printf '%s\n' "$@" | jq -R . | jq -sc .)
    exec_body="{\"AttachStdout\":true,\"AttachStderr\":true,\"Cmd\":${cmd_json}}"
    exec_id=$(docker_post "/containers/${id}/exec" "$exec_body" | jq -r '.Id')
    curl -sf -X POST -H 'Content-Type: application/json' \
      -d '{"Detach":false,"Tty":false}' \
      "${BASE_URL}/exec/${exec_id}/start" | strip_frames
    ;;

  prune-containers)
    docker_post "/containers/prune" | jq '{
      deleted: (.ContainersDeleted // []),
      space_reclaimed_mb: ((.SpaceReclaimed // 0) / 1048576 | . * 10 | round / 10)
    }'
    ;;

  # ── Images ──────────────────────────────────────────────────────────────────

  images)
    docker_get "/images/json" | jq -r '
      ["REPOSITORY","TAG","ID","SIZE"],
      (.[] | (.RepoTags // ["<none>:<none>"])[] | split(":") as [$repo,$tag] |
       [., $tag, "dummy", "dummy"]) |
      if type == "array" and (.[0] | type) == "string" and (.[0] | contains(":")) then
        . as $rt | $rt[0] | split(":") as [$repo,$tag] |
        [$repo, $tag, "?", "?"]
      else . end |
      @tsv' 2>/dev/null || \
    docker_get "/images/json" | jq -r '
      ["REPOSITORY","TAG","ID","SIZE_MB"],
      (.[] |
        ((.RepoTags // ["<none>:<none>"])[0] | split(":")) as [$repo,$tag] |
        [
          ($repo // "<none>"),
          ($tag // "<none>"),
          (.Id | ltrimstr("sha256:") | .[0:12]),
          (.Size / 1048576 | . * 10 | round / 10 | tostring + " MB")
        ]
      ) | @tsv' | fmt_table
    ;;

  image-inspect)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 image-inspect <name>" >&2; exit 1; }
    docker_get "/images/${name}/json" | jq '{
      Id: (.Id | ltrimstr("sha256:") | .[0:12]),
      RepoTags: .RepoTags,
      Created: .Created,
      Size_MB: (.Size / 1048576 | . * 10 | round / 10),
      Os: .Os,
      Architecture: .Architecture,
      Author: .Author,
      Cmd: .Config.Cmd,
      Entrypoint: .Config.Entrypoint,
      Env: .Config.Env,
      ExposedPorts: (.Config.ExposedPorts // {} | keys),
      Labels: .Config.Labels
    }'
    ;;

  image-history)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 image-history <name>" >&2; exit 1; }
    docker_get "/images/${name}/history" | jq -r '
      ["CREATED","SIZE_MB","CREATED_BY"],
      (.[] | [
        (.Created | todate),
        (.Size / 1048576 | . * 10 | round / 10 | tostring + " MB"),
        (.CreatedBy | .[0:80])
      ]) | @tsv' | fmt_table
    ;;

  prune-images)
    docker_post "/images/prune" | jq '{
      deleted: ([(.ImagesDeleted // [])[] | .Deleted // .Untagged] | map(select(. != null))),
      space_reclaimed_mb: ((.SpaceReclaimed // 0) / 1048576 | . * 10 | round / 10)
    }'
    ;;

  # ── Networks ─────────────────────────────────────────────────────────────────

  networks)
    docker_get "/networks" | jq -r '
      ["NAME","DRIVER","SCOPE","ID"],
      (.[] | [.Name, .Driver, .Scope, (.Id | .[0:12])]) | @tsv' | fmt_table
    ;;

  network-inspect)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 network-inspect <name>" >&2; exit 1; }
    docker_get "/networks/${name}" | jq '{
      Name: .Name,
      Id: (.Id | .[0:12]),
      Driver: .Driver,
      Scope: .Scope,
      IPAM: .IPAM,
      Containers: ([.Containers // {} | to_entries[] | {name: .value.Name, ip: .value.IPv4Address}])
    }'
    ;;

  prune-networks)
    docker_post "/networks/prune" | jq '{deleted: (.NetworksDeleted // [])}'
    ;;

  # ── Volumes ──────────────────────────────────────────────────────────────────

  volumes)
    docker_get "/volumes" | jq -r '
      ["NAME","DRIVER","MOUNTPOINT"],
      (.Volumes[] | [.Name, .Driver, .Mountpoint]) | @tsv' | fmt_table
    ;;

  volume-inspect)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 volume-inspect <name>" >&2; exit 1; }
    docker_get "/volumes/${name}" | jq '{
      Name: .Name,
      Driver: .Driver,
      Mountpoint: .Mountpoint,
      Labels: .Labels,
      Options: .Options,
      UsageData: .UsageData
    }'
    ;;

  prune-volumes)
    docker_post "/volumes/prune" | jq '{
      deleted: (.VolumesDeleted // []),
      space_reclaimed_mb: ((.SpaceReclaimed // 0) / 1048576 | . * 10 | round / 10)
    }'
    ;;

  # ── Swarm ────────────────────────────────────────────────────────────────────

  swarm)
    docker_get "/swarm" | jq '{
      ID: .ID,
      CreatedAt: .CreatedAt,
      UpdatedAt: .UpdatedAt,
      Nodes: .JoinTokens | keys,
      Spec: {
        Name: .Spec.Name,
        TaskHistoryRetentionLimit: .Spec.Orchestration.TaskHistoryRetentionLimit
      }
    }'
    ;;

  nodes)
    docker_get "/nodes" | jq -r '
      ["ID","HOSTNAME","ROLE","STATUS","AVAILABILITY","ENGINE"],
      (.[] | [
        (.ID | .[0:12]),
        .Description.Hostname,
        .Spec.Role,
        .Status.State,
        .Spec.Availability,
        .Description.Engine.EngineVersion
      ]) | @tsv' | fmt_table
    ;;

  node-inspect)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 node-inspect <name>" >&2; exit 1; }
    docker_get "/nodes/${name}" | jq '{
      ID: (.ID | .[0:12]),
      Hostname: .Description.Hostname,
      Role: .Spec.Role,
      Availability: .Spec.Availability,
      Status: .Status.State,
      EngineVersion: .Description.Engine.EngineVersion,
      Labels: .Spec.Labels,
      Platform: .Description.Platform
    }'
    ;;

  services)
    docker_get "/services" | jq -r '
      ["ID","NAME","IMAGE","REPLICAS","PORTS"],
      (.[] | [
        (.ID | .[0:12]),
        .Spec.Name,
        (.Spec.TaskTemplate.ContainerSpec.Image | split("@")[0] | split(":")[0] | split("/")[-1]),
        (if .Spec.Mode.Replicated then "\(.ServiceStatus.RunningTasks // "?")/\(.Spec.Mode.Replicated.Replicas)" else "global" end),
        ([.Endpoint.Ports // [] | .[] | "\(.PublishedPort)->\(.TargetPort)/\(.Protocol)"] | join(", "))
      ]) | @tsv' | fmt_table
    ;;

  service-inspect)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 service-inspect <name>" >&2; exit 1; }
    docker_get "/services/${name}" | jq '{
      ID: (.ID | .[0:12]),
      Name: .Spec.Name,
      Image: (.Spec.TaskTemplate.ContainerSpec.Image | split("@")[0]),
      Replicas: .Spec.Mode.Replicated.Replicas,
      UpdateConfig: .Spec.UpdateConfig,
      Ports: .Endpoint.Ports,
      Labels: .Spec.Labels,
      CreatedAt: .CreatedAt,
      UpdatedAt: .UpdatedAt
    }'
    ;;

  service-logs)
    name="${2:-}"; [[ -z "$name" ]] && { echo "Usage: $0 service-logs <name> [tail]" >&2; exit 1; }
    tail="${3:-100}"
    curl -sf "${BASE_URL}/services/${name}/logs?stdout=1&stderr=1&tail=${tail}" | strip_frames
    ;;

  tasks)
    docker_get "/tasks" | jq -r '
      ["ID","SERVICE","NODE","STATE","DESIRED","IMAGE"],
      (.[] | [
        (.ID | .[0:12]),
        .ServiceID[0:12],
        .NodeID[0:12],
        .Status.State,
        .DesiredState,
        (.Spec.ContainerSpec.Image | split("@")[0] | split(":")[0] | split("/")[-1])
      ]) | @tsv' | fmt_table
    ;;

  configs)
    docker_get "/configs" | jq -r '
      ["ID","NAME","CREATED"],
      (.[] | [(.ID | .[0:12]), .Spec.Name, .CreatedAt]) | @tsv' | fmt_table
    ;;

  secrets)
    docker_get "/secrets" | jq -r '
      ["ID","NAME","CREATED"],
      (.[] | [(.ID | .[0:12]), .Spec.Name, .CreatedAt]) | @tsv' | fmt_table
    ;;

  # ── Plugins ──────────────────────────────────────────────────────────────────

  plugins)
    docker_get "/plugins" | jq -r '
      ["NAME","TAG","ENABLED"],
      (.[] | [.Name, .Tag, (.Enabled | tostring)]) | @tsv' | fmt_table
    ;;

  *)
    echo "Unknown mode: ${mode}" >&2
    echo "Run without arguments for usage." >&2
    exit 1
    ;;
esac
