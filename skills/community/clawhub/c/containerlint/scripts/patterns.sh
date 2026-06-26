#!/usr/bin/env bash
# ContainerLint -- Docker & Container Security Anti-Pattern Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Security vulnerability or data exposure from container misconfiguration
#   high     -- Significant security issue that will weaken container posture
#   medium   -- Moderate concern that should be addressed
#   low      -- Best practice suggestion
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.

set -euo pipefail

# ===========================================================================
# DF -- Dockerfile Best Practices (15 patterns: DF-001 to DF-015)
# Free tier
# ===========================================================================

declare -a CONTAINERLINT_DF_PATTERNS=(
  'FROM[[:space:]]+[[:alnum:]_./-]+:latest|high|DF-001|Using :latest tag in FROM makes builds non-reproducible|Pin a specific image version tag (e.g., node:20.11-alpine)'
  'FROM[[:space:]]+[[:alnum:]_./-]+[[:space:]]*$|medium|DF-002|FROM without explicit tag defaults to :latest|Always specify an explicit image version tag in FROM directives'
  'ADD[[:space:]]+https?://|high|DF-003|ADD with URL downloads are uncached and unverified|Use RUN curl or RUN wget with checksum verification instead of ADD'
  'ADD[[:space:]]+[^-]|medium|DF-004|ADD has implicit tar extraction and URL fetch behavior|Use COPY instead of ADD unless you need tar auto-extraction'
  'RUN[[:space:]]+apt-get[[:space:]]+install[[:space:]]+-y[[:space:]]+[[:alnum:]]|medium|DF-005|apt-get install without version pins creates non-reproducible builds|Pin package versions: apt-get install -y package=version'
  'RUN[[:space:]]+apt-get[[:space:]]+update[[:space:]]*$|high|DF-006|apt-get update in separate RUN layer creates stale cache|Combine apt-get update and install in a single RUN layer'
  'RUN[[:space:]]+chmod[[:space:]]+777|high|DF-007|chmod 777 grants world-writable permissions inside container|Use least-privilege permissions (e.g., chmod 755 or chmod 644)'
  'RUN[[:space:]]+curl[[:space:]].*[[:space:]]-k|high|DF-008|curl with -k disables SSL certificate verification|Remove -k flag and use proper TLS certificate verification'
  'COPY[[:space:]]+\.[[:space:]]+\.|medium|DF-009|COPY . . copies entire build context including unneeded files|Use .dockerignore and copy only required files or directories'
  'ENV[[:space:]]+NODE_ENV[[:space:]]*=[[:space:]]*development|medium|DF-010|NODE_ENV set to development in Dockerfile|Set NODE_ENV=production or omit it from Dockerfile for production builds'
  'RUN[[:space:]]+npm[[:space:]]+install[[:space:]]*$|medium|DF-011|npm install without --production includes devDependencies|Use npm ci --only=production for reproducible production builds'
  'WORKDIR[[:space:]]+[^/]|low|DF-012|WORKDIR with relative path depends on previous WORKDIR state|Use absolute paths in WORKDIR directives for clarity'
  'FROM[[:space:]]+ubuntu[[:space:]]*$|medium|DF-013|Using Ubuntu base without version tag pulls latest by default|Pin to a specific version: FROM ubuntu:22.04'
  'LABEL[[:space:]]+maintainer|low|DF-014|LABEL maintainer is deprecated in favor of OCI standard labels|Use LABEL org.opencontainers.image.authors instead'
  'WORKDIR[[:space:]]+/[[:space:]]*$|medium|DF-015|WORKDIR / sets working directory to filesystem root|Use a dedicated application directory: WORKDIR /app'
)

# ===========================================================================
# SC -- Security Context (15 patterns: SC-001 to SC-015)
# Free tier
# ===========================================================================

declare -a CONTAINERLINT_SC_PATTERNS=(
  'privileged[[:space:]]*:[[:space:]]*true|critical|SC-001|Container running in privileged mode has full host access|Remove privileged: true and use specific capabilities instead'
  'USER[[:space:]]+root|high|SC-002|Container explicitly runs as root user|Use a non-root USER directive (e.g., USER 1001 or USER appuser)'
  'ENV[[:space:]]+[[:alnum:]_]*PASSWORD[[:space:]]*=|critical|SC-003|Password hardcoded in ENV directive is visible in image layers|Use Docker secrets or runtime environment variables for passwords'
  'ENV[[:space:]]+[[:alnum:]_]*SECRET[[:space:]]*=|critical|SC-004|Secret hardcoded in ENV directive is visible in image layers|Use Docker secrets or a secrets manager for sensitive values'
  'ENV[[:space:]]+[[:alnum:]_]*API_KEY[[:space:]]*=|critical|SC-005|API key hardcoded in ENV directive is visible in image layers|Use Docker secrets or runtime environment variables for API keys'
  'ENV[[:space:]]+[[:alnum:]_]*TOKEN[[:space:]]*=|high|SC-006|Token hardcoded in ENV directive is visible in image layers|Use Docker secrets or runtime environment variables for tokens'
  'ARG[[:space:]]+[[:alnum:]_]*PASSWORD|high|SC-007|Password in ARG is visible in build history|Use --secret flag in docker build or multi-stage builds for secrets'
  'allowPrivilegeEscalation[[:space:]]*:[[:space:]]*true|critical|SC-008|allowPrivilegeEscalation lets processes gain more privileges|Set allowPrivilegeEscalation: false in security context'
  'readOnlyRootFilesystem[[:space:]]*:[[:space:]]*false|high|SC-009|Writable root filesystem allows attackers to modify binaries|Set readOnlyRootFilesystem: true and use emptyDir for write paths'
  'runAsNonRoot[[:space:]]*:[[:space:]]*false|high|SC-010|runAsNonRoot: false allows the container to run as UID 0|Set runAsNonRoot: true and specify a non-root runAsUser'
  'RUN[[:space:]]+echo[[:space:]]+["\x27].*[pP]ass|high|SC-011|Password echoed in RUN layer is stored in image history|Use build secrets or mount secrets at runtime instead'
  'hostPID[[:space:]]*:[[:space:]]*true|critical|SC-012|hostPID exposes all host processes to the container|Remove hostPID: true -- containers should use their own PID namespace'
  'hostIPC[[:space:]]*:[[:space:]]*true|high|SC-013|hostIPC allows container to access host shared memory segments|Remove hostIPC: true unless absolutely required for IPC'
  'COPY[[:space:]]+.*\.pem|high|SC-014|Copying private key files into image exposes credentials|Mount certificates at runtime; never bake private keys into images'
  'COPY[[:space:]]+.*id_rsa|critical|SC-015|Copying SSH private key into image exposes credentials permanently|Use SSH agent forwarding or BuildKit secrets for build-time SSH access'
)

# ===========================================================================
# HC -- Health & Readiness (15 patterns: HC-001 to HC-015)
# Pro tier
# ===========================================================================

declare -a CONTAINERLINT_HC_PATTERNS=(
  'HEALTHCHECK[[:space:]]+NONE|high|HC-001|HEALTHCHECK NONE explicitly disables health monitoring|Define a proper HEALTHCHECK CMD for container health monitoring'
  'livenessProbe[[:space:]]*:[[:space:]]*\{\}|high|HC-002|Empty livenessProbe object provides no health checking|Define exec, httpGet, or tcpSocket action for livenessProbe'
  'readinessProbe[[:space:]]*:[[:space:]]*\{\}|high|HC-003|Empty readinessProbe object provides no readiness checking|Define exec, httpGet, or tcpSocket action for readinessProbe'
  'startupProbe[[:space:]]*:[[:space:]]*\{\}|medium|HC-004|Empty startupProbe object provides no startup checking|Define startupProbe with sufficient failureThreshold for slow-starting apps'
  'initialDelaySeconds[[:space:]]*:[[:space:]]*0[[:space:]]*$|medium|HC-005|Zero initial delay may fail on slow-starting containers|Set initialDelaySeconds to allow time for application startup'
  'periodSeconds[[:space:]]*:[[:space:]]*1[[:space:]]*$|medium|HC-006|Probe period of 1 second creates excessive health check load|Use periodSeconds >= 10 to reduce probe overhead'
  'failureThreshold[[:space:]]*:[[:space:]]*1[[:space:]]*$|medium|HC-007|failureThreshold of 1 restarts on first failure without retry|Set failureThreshold >= 3 to allow transient failures'
  'timeoutSeconds[[:space:]]*:[[:space:]]*[0-9][0-9][0-9]|medium|HC-008|Very high probe timeout (100s+) delays failure detection|Reduce timeoutSeconds to 5-10 seconds for faster failure detection'
  'STOPSIGNAL[[:space:]]+SIGKILL|high|HC-009|STOPSIGNAL SIGKILL prevents graceful application shutdown|Use STOPSIGNAL SIGTERM to allow graceful connection draining'
  'terminationGracePeriodSeconds[[:space:]]*:[[:space:]]*0|high|HC-010|Zero termination grace period prevents graceful pod shutdown|Set terminationGracePeriodSeconds to at least 30 for production workloads'
  'CMD[[:space:]]+\["sleep"|medium|HC-011|Using sleep as CMD indicates container is not running a proper service|Replace sleep with actual application process or use init system'
  'ENTRYPOINT[[:space:]]+[^[]|medium|HC-012|Shell form ENTRYPOINT does not receive Unix signals properly|Use exec form ENTRYPOINT ["executable", "param1"] for proper signal handling'
  'stop_grace_period[[:space:]]*:[[:space:]]*0|high|HC-013|Zero grace period kills container immediately without cleanup|Set stop_grace_period to at least 10s for graceful shutdown'
  'HEALTHCHECK.*--retries[[:space:]]*=[[:space:]]*1[[:space:]]|medium|HC-014|HEALTHCHECK with 1 retry restarts on transient failures|Use --retries=3 or higher to tolerate transient failures'
  'restart_policy.*max_attempts[[:space:]]*:[[:space:]]*0|medium|HC-015|Max restart attempts set to 0 means unlimited restarts of failing container|Set a reasonable max_attempts limit to prevent crash loops'
)

# ===========================================================================
# RS -- Resource Management (15 patterns: RS-001 to RS-015)
# Pro tier
# ===========================================================================

declare -a CONTAINERLINT_RS_PATTERNS=(
  'resources[[:space:]]*:[[:space:]]*\{\}|high|RS-001|Empty resources block sets no CPU or memory limits|Define both requests and limits for CPU and memory'
  'limits[[:space:]]*:[[:space:]]*\{\}|high|RS-002|Empty limits block allows unbounded resource usage|Set memory and cpu limits to prevent resource exhaustion'
  'mem_limit[[:space:]]*:[[:space:]]*0|critical|RS-003|Memory limit of 0 means unlimited -- container can exhaust host memory|Set a reasonable memory limit (e.g., mem_limit: 512m)'
  'memswap_limit[[:space:]]*:[[:space:]]*-1|high|RS-004|Unlimited swap allows container to use all host swap|Set memswap_limit equal to mem_limit to disable swap'
  'pids_limit[[:space:]]*:[[:space:]]*-1|medium|RS-005|Unlimited PIDs can enable fork bomb attacks|Set pids_limit to a reasonable value (e.g., 200)'
  '--oom-kill-disable|high|RS-006|Disabling OOM killer can hang the host when memory is exhausted|Remove --oom-kill-disable and set appropriate memory limits instead'
  'shm_size[[:space:]]*:[[:space:]]*["\x27]?[0-9]+g|medium|RS-007|Large shared memory allocation may waste host resources|Set shm_size to the minimum required (default 64m is often sufficient)'
  'requests[[:space:]]*:[[:space:]]*\{\}|medium|RS-008|Empty requests block prevents proper scheduling|Define CPU and memory requests for proper Kubernetes scheduling'
  'storage[[:space:]]*:[[:space:]]*["\x27]?[0-9]+Ti|high|RS-009|Terabyte-level storage claim is likely misconfigured|Verify storage size is correct; use Gi instead of Ti if appropriate'
  '--memory[[:space:]]*=[[:space:]]*0|high|RS-010|Docker run memory limit of 0 means unlimited|Set a reasonable memory limit: --memory=512m'
  '--cpus[[:space:]]*=[[:space:]]*0|medium|RS-011|Docker run CPU limit of 0 means unlimited|Set CPU limit: --cpus=1.0 or appropriate for workload'
  'LimitNOFILE[[:space:]]*=[[:space:]]*infinity|medium|RS-012|Unlimited file descriptors can exhaust kernel resources|Set LimitNOFILE to a bounded value matching application needs'
  '--tmpfs.*size=0|medium|RS-013|tmpfs without size limit uses up to half of host memory|Always set a size limit for tmpfs mounts: --tmpfs /tmp:size=100m'
  'ephemeral-storage[[:space:]]*:[[:space:]]*["\x27]?[0-9]+Gi|low|RS-014|Large ephemeral storage limit may fill node disk|Right-size ephemeral-storage based on actual temporary storage needs'
  'ulimits[[:space:]]*:.*nofile[[:space:]]*:.*soft[[:space:]]*:[[:space:]]*[0-9]{6}|medium|RS-015|Very high file descriptor ulimit may waste kernel resources|Set nofile ulimits to match application requirements (e.g., 65535)'
)

# ===========================================================================
# NW -- Networking & Exposure (15 patterns: NW-001 to NW-015)
# Team tier
# ===========================================================================

declare -a CONTAINERLINT_NW_PATTERNS=(
  'EXPOSE[[:space:]]+0-65535|critical|NW-001|Exposing entire port range makes all services accessible|Expose only the specific ports your application requires'
  'hostNetwork[[:space:]]*:[[:space:]]*true|critical|NW-002|Host networking bypasses container network isolation|Use bridge or overlay networking; remove hostNetwork: true'
  'network_mode[[:space:]]*:[[:space:]]*["\x27]?host|critical|NW-003|Host network mode bypasses container network isolation|Use bridge or overlay network mode instead of host'
  '0\.0\.0\.0:[0-9]+:[0-9]+|high|NW-004|Publishing port on 0.0.0.0 binds to all network interfaces|Bind to 127.0.0.1 or a specific interface for non-public services'
  'EXPOSE[[:space:]]+22[[:space:]]|high|NW-005|Exposing SSH port 22 in container is an anti-pattern|Use docker exec or kubectl exec instead of SSH into containers'
  'EXPOSE[[:space:]]+23[[:space:]]|critical|NW-006|Exposing Telnet port 23 is a critical security risk|Never expose Telnet; use SSH or docker exec for remote access'
  'insecure-registries|critical|NW-007|Insecure registries allow unencrypted image pulls|Use TLS-secured registries for all image pulls'
  'hostPort[[:space:]]*:[[:space:]]*[0-9]|high|NW-008|hostPort binds container directly to host port|Use NodePort or LoadBalancer service type instead of hostPort'
  'EXPOSE[[:space:]]+3306|medium|NW-009|Exposing MySQL port 3306 may allow unauthorized database access|Do not expose database ports; use internal networking only'
  'EXPOSE[[:space:]]+5432|medium|NW-010|Exposing PostgreSQL port 5432 may allow unauthorized database access|Do not expose database ports; use internal networking only'
  'EXPOSE[[:space:]]+6379|medium|NW-011|Exposing Redis port 6379 -- Redis has no auth by default|Do not expose Redis ports; use internal networking and enable AUTH'
  'EXPOSE[[:space:]]+27017|medium|NW-012|Exposing MongoDB port 27017 may allow unauthorized access|Do not expose database ports; use internal networking only'
  'EXPOSE[[:space:]]+2375|critical|NW-013|Exposing Docker daemon port 2375 allows unauthenticated container control|Never expose Docker socket; use TLS on port 2376 if remote access needed'
  'dnsPolicy[[:space:]]*:[[:space:]]*["\x27]?None|medium|NW-014|DNS policy None disables all DNS resolution in the pod|Use Default or ClusterFirst DNS policy unless custom DNS is required'
  'loadBalancerSourceRanges[[:space:]]*:[[:space:]]*\[\]|high|NW-015|Empty loadBalancerSourceRanges allows traffic from any IP|Restrict loadBalancerSourceRanges to trusted CIDR blocks'
)

# ===========================================================================
# OR -- Orchestration & Compose (15 patterns: OR-001 to OR-015)
# Team tier
# ===========================================================================

declare -a CONTAINERLINT_OR_PATTERNS=(
  'restart[[:space:]]*:[[:space:]]*["\x27]?no["\x27]?[[:space:]]*$|medium|OR-001|No restart policy means container stays down after failure|Use restart: unless-stopped or restart: always for production services'
  'replicas[[:space:]]*:[[:space:]]*1[[:space:]]*$|medium|OR-002|Single replica has no redundancy for high availability|Use replicas >= 2 for production workloads requiring availability'
  'image[[:space:]]*:[[:space:]]*[[:alnum:]_./-]+:latest|high|OR-003|Using :latest tag in orchestration config makes deployments non-reproducible|Pin specific image version tags in all orchestration files'
  'image[[:space:]]*:[[:space:]]*[[:alnum:]_./-]+[[:space:]]*$|medium|OR-004|Image reference without tag defaults to :latest|Always specify an explicit image version tag'
  '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+:[0-9]+|medium|OR-005|Hardcoded IP address in port mapping reduces portability|Use service names or DNS instead of hardcoded IP addresses'
  'version[[:space:]]*:[[:space:]]*["\x27][12]\.|low|OR-006|Docker Compose v1/v2 schema is outdated|Migrate to Docker Compose v3+ or omit version field for latest'
  'volumes_from[[:space:]]*:|medium|OR-007|volumes_from shares all volumes between containers|Use named volumes with explicit mount points instead of volumes_from'
  'links[[:space:]]*:|low|OR-008|Docker links are legacy and deprecated|Use Docker networks for inter-container communication instead of links'
  'container_name[[:space:]]*:|low|OR-009|Fixed container_name prevents scaling with docker-compose up --scale|Remove container_name to allow container scaling'
  'environment[[:space:]]*:.*PASSWORD[[:space:]]*=|high|OR-010|Password in compose environment is stored in plaintext|Use Docker secrets or env_file with proper file permissions for passwords'
  'environment[[:space:]]*:.*SECRET[[:space:]]*=|high|OR-011|Secret in compose environment is stored in plaintext|Use Docker secrets or env_file with proper file permissions for secrets'
  'stdin_open[[:space:]]*:[[:space:]]*true|low|OR-012|stdin_open: true keeps STDIN open; usually only needed for debugging|Remove stdin_open: true for production deployments'
  'tty[[:space:]]*:[[:space:]]*true|low|OR-013|tty: true allocates a terminal; usually only needed for debugging|Remove tty: true for production deployments'
  'driver[[:space:]]*:[[:space:]]*["\x27]?none|medium|OR-014|Logging driver none discards all container logs|Use json-file, syslog, or a centralized logging driver'
  'COPY[[:space:]]+.*\.env|high|OR-015|Copying .env file into image exposes secrets in image layers|Never copy .env files; inject environment variables at runtime'
)

# ===========================================================================
# Utility Functions
# ===========================================================================

# Count total patterns
containerlint_pattern_count() {
  local count=0
  count=$((count + ${#CONTAINERLINT_DF_PATTERNS[@]}))
  count=$((count + ${#CONTAINERLINT_SC_PATTERNS[@]}))
  count=$((count + ${#CONTAINERLINT_HC_PATTERNS[@]}))
  count=$((count + ${#CONTAINERLINT_RS_PATTERNS[@]}))
  count=$((count + ${#CONTAINERLINT_NW_PATTERNS[@]}))
  count=$((count + ${#CONTAINERLINT_OR_PATTERNS[@]}))
  echo "$count"
}

# Count patterns in a specific category
containerlint_category_count() {
  local cat="$1"
  case "$cat" in
    DF) echo "${#CONTAINERLINT_DF_PATTERNS[@]}" ;;
    SC) echo "${#CONTAINERLINT_SC_PATTERNS[@]}" ;;
    HC) echo "${#CONTAINERLINT_HC_PATTERNS[@]}" ;;
    RS) echo "${#CONTAINERLINT_RS_PATTERNS[@]}" ;;
    NW) echo "${#CONTAINERLINT_NW_PATTERNS[@]}" ;;
    OR) echo "${#CONTAINERLINT_OR_PATTERNS[@]}" ;;
    *)  echo "0" ;;
  esac
}

# Get the bash array name for a category code
get_containerlint_patterns_for_category() {
  local cat="$1"
  case "$cat" in
    DF) echo "CONTAINERLINT_DF_PATTERNS" ;;
    SC) echo "CONTAINERLINT_SC_PATTERNS" ;;
    HC) echo "CONTAINERLINT_HC_PATTERNS" ;;
    RS) echo "CONTAINERLINT_RS_PATTERNS" ;;
    NW) echo "CONTAINERLINT_NW_PATTERNS" ;;
    OR) echo "CONTAINERLINT_OR_PATTERNS" ;;
    *)  echo "" ;;
  esac
}

# Get human-readable label for a category code
get_containerlint_category_label() {
  local cat="$1"
  case "$cat" in
    DF) echo "Dockerfile Best Practices" ;;
    SC) echo "Security Context" ;;
    HC) echo "Health & Readiness" ;;
    RS) echo "Resource Management" ;;
    NW) echo "Networking & Exposure" ;;
    OR) echo "Orchestration & Compose" ;;
    *)  echo "Unknown" ;;
  esac
}

# Get space-separated list of category codes available at a given tier level.
# Tier levels: 0=free (DF, SC), 1=pro (DF, SC, HC, RS), 2/3=team/enterprise (all)
get_containerlint_categories_for_tier() {
  local tier_level="$1"
  case "$tier_level" in
    0) echo "DF SC" ;;
    1) echo "DF SC HC RS" ;;
    2|3) echo "DF SC HC RS NW OR" ;;
    *) echo "DF SC" ;;
  esac
}

# Severity to point deduction mapping
severity_to_points() {
  local severity="$1"
  case "$severity" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo  8 ;;
    low)      echo  3 ;;
    *)        echo  0 ;;
  esac
}

# Validate that a string is a known category code
is_valid_containerlint_category() {
  local cat="$1"
  case "$cat" in
    DF|SC|HC|RS|NW|OR) return 0 ;;
    *) return 1 ;;
  esac
}

# List patterns in a given category or "all"
containerlint_list_patterns() {
  local filter="${1:-all}"

  local categories="DF SC HC RS NW OR"
  if [[ "$filter" != "all" ]]; then
    filter=$(echo "$filter" | tr '[:lower:]' '[:upper:]')
    categories="$filter"
  fi

  for cat in $categories; do
    local label
    label=$(get_containerlint_category_label "$cat")
    echo -e "${BOLD:-}--- ${cat}: ${label} ---${NC:-}"

    local arr_name
    arr_name=$(get_containerlint_patterns_for_category "$cat")
    [[ -z "$arr_name" ]] && continue

    local -n _arr="$arr_name"
    for entry in "${_arr[@]}"; do
      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
      local sev_upper
      sev_upper=$(echo "$severity" | tr '[:lower:]' '[:upper:]')
      echo "  [$sev_upper] $check_id: $description"
    done
    echo ""
  done
}
