#!/usr/bin/env bash
# ConfigSafe — Misconfiguration Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical — Immediate security exposure, exploitable
#   high     — Significant security weakness
#   medium   — Best practice violation, potential risk
#   low      — Informational, improvement opportunity
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use literal quotes instead of \x27
# - Avoid Perl-only features (\d, \w, etc.)

set -euo pipefail

# ─── Pattern registries by config type ──────────────────────────────────────
#
# Format: "regex|severity|check_id|description|recommendation"
# Patterns use POSIX extended grep regex (ERE) syntax.

# ═══════════════════════════════════════════════════════════════════════════
# 1. DOCKERFILE PATTERNS
# ═══════════════════════════════════════════════════════════════════════════

declare -a CONFIGSAFE_DOCKERFILE_PATTERNS=()

CONFIGSAFE_DOCKERFILE_PATTERNS+=(
  # Running as root
  'PLACEHOLDER_NO_USER_CHECK|critical|DF-001|No USER directive — container runs as root|Add a USER directive to run as a non-root user: USER appuser'

  # Using latest tag
  'FROM[[:space:]]+[a-zA-Z0-9_./-]+:latest|high|DF-002|Using :latest tag — unpinned, non-reproducible builds|Pin to a specific version tag or SHA digest: FROM image:1.2.3'
  'FROM[[:space:]]+[a-zA-Z0-9_./-]+[[:space:]]*$|high|DF-003|FROM without tag — defaults to :latest|Pin to a specific version tag: FROM image:1.2.3'

  # ADD instead of COPY
  'ADD[[:space:]]+[^h][^t][^t][^p]|medium|DF-004|ADD used instead of COPY — ADD has tar extraction and URL side effects|Use COPY unless you specifically need ADD tar extraction or URL features'

  # Exposing sensitive ports
  'EXPOSE[[:space:]]+22([[:space:]]|$)|high|DF-005|Exposing SSH port 22 in container|Remove SSH port exposure; use docker exec for debugging'
  'EXPOSE[[:space:]]+3306([[:space:]]|$)|high|DF-006|Exposing MySQL port 3306|Do not expose database ports directly; use internal networking'
  'EXPOSE[[:space:]]+5432([[:space:]]|$)|high|DF-007|Exposing PostgreSQL port 5432|Do not expose database ports directly; use internal networking'
  'EXPOSE[[:space:]]+6379([[:space:]]|$)|high|DF-008|Exposing Redis port 6379|Do not expose Redis directly; use internal networking'
  'EXPOSE[[:space:]]+27017([[:space:]]|$)|high|DF-009|Exposing MongoDB port 27017|Do not expose MongoDB directly; use internal networking'

  # Missing health check (handled in analyzer via file-level check)
  'PLACEHOLDER_NO_HEALTHCHECK|medium|DF-010|No HEALTHCHECK directive — orchestrator cannot detect unhealthy containers|Add HEALTHCHECK --interval=30s CMD curl -f http://localhost/ || exit 1'

  # apt-get without --no-install-recommends
  'apt-get[[:space:]]+install[[:space:]]+(.)*$|low|DF-011|apt-get install without --no-install-recommends|Add --no-install-recommends to reduce image size and attack surface'

  # Secrets in ENV
  'ENV[[:space:]]+(PASSWORD|SECRET|API_KEY|TOKEN|PRIVATE_KEY|AWS_SECRET|DB_PASSWORD)[[:space:]]*=|critical|DF-012|Secret value hardcoded in ENV directive|Use build args, Docker secrets, or runtime environment variables instead'

  # curl | bash
  'curl[[:space:]].*\|[[:space:]]*bash|critical|DF-013|curl piped to bash — remote code execution risk|Download scripts first, verify checksum, then execute'
  'curl[[:space:]].*\|[[:space:]]*sh|critical|DF-014|curl piped to sh — remote code execution risk|Download scripts first, verify checksum, then execute'
  'wget[[:space:]].*\|[[:space:]]*bash|critical|DF-015|wget piped to bash — remote code execution risk|Download scripts first, verify checksum, then execute'

  # Missing multi-stage build (handled in analyzer)
  'PLACEHOLDER_NO_MULTISTAGE|medium|DF-016|Single-stage build — build tools included in final image|Use multi-stage builds to separate build and runtime environments'

  # chmod 777
  'chmod[[:space:]]+777|high|DF-017|chmod 777 — world-writable file permissions|Use specific permissions: chmod 755 for dirs, chmod 644 for files'
  'chmod[[:space:]]+[0-7]*7[0-7]*[[:space:]]|high|DF-018|World-executable permissions in chmod|Restrict permissions to owner and group only'

  # Running as root explicitly
  'USER[[:space:]]+root|critical|DF-019|USER explicitly set to root|Change to a non-root user: USER appuser'

  # Apt-get without clean
  'apt-get[[:space:]]+install.*&&[[:space:]]*.*$|low|DF-020|apt-get install without cleanup — increases image size|Add && rm -rf /var/lib/apt/lists/* after apt-get install'
)

# ═══════════════════════════════════════════════════════════════════════════
# 2. DOCKER-COMPOSE PATTERNS
# ═══════════════════════════════════════════════════════════════════════════

declare -a CONFIGSAFE_COMPOSE_PATTERNS=()

CONFIGSAFE_COMPOSE_PATTERNS+=(
  # Privileged mode
  'privileged:[[:space:]]*true|critical|DC-001|privileged: true — container has full host capabilities|Remove privileged mode; use specific capabilities with cap_add instead'

  # Host network mode
  'network_mode:[[:space:]]*"?host"?|high|DC-002|Host network mode — container shares host network stack|Use bridge networking with explicit port mappings'
  'network_mode:[[:space:]]*host|high|DC-003|Host network mode — container shares host network stack|Use bridge networking with explicit port mappings'

  # Docker socket mount
  '/var/run/docker\.sock|critical|DC-004|Docker socket mounted — gives container control over Docker daemon|Remove Docker socket mount; use Docker API over TLS if needed'

  # Missing resource limits (handled in analyzer via file-level check)
  'PLACEHOLDER_NO_RESOURCE_LIMITS|medium|DC-005|No resource limits defined — container can consume all host resources|Add mem_limit, cpus, or deploy.resources.limits'

  # Plaintext secrets in environment
  'environment:.*PASSWORD[[:space:]]*[:=][[:space:]]*[^$]|critical|DC-006|Password in plaintext in environment section|Use Docker secrets, .env files, or external secret management'
  'environment:.*SECRET[[:space:]]*[:=][[:space:]]*[^$]|critical|DC-007|Secret in plaintext in environment section|Use Docker secrets, .env files, or external secret management'
  'environment:.*API_KEY[[:space:]]*[:=][[:space:]]*[^$]|critical|DC-008|API key in plaintext in environment section|Use Docker secrets, .env files, or external secret management'
  'environment:.*TOKEN[[:space:]]*[:=][[:space:]]*[^$]|critical|DC-009|Token in plaintext in environment section|Use Docker secrets, .env files, or external secret management'
  '[A-Z_]*PASSWORD[[:space:]]*:[[:space:]]*["\x27]?[a-zA-Z0-9]|critical|DC-010|Password hardcoded in docker-compose|Use environment variable references ($PASSWORD) or Docker secrets'
  '[A-Z_]*SECRET[[:space:]]*:[[:space:]]*["\x27]?[a-zA-Z0-9]|critical|DC-011|Secret hardcoded in docker-compose|Use environment variable references or Docker secrets'

  # Ports exposed without binding to localhost
  'ports:.*"[0-9]+:[0-9]+"|(^[[:space:]]*-[[:space:]]*"?)[0-9]+:[0-9]+|high|DC-012|Port exposed without binding to 127.0.0.1|Bind to localhost: "127.0.0.1:8080:8080" instead of "8080:8080"'

  # Missing restart policy (handled in analyzer)
  'PLACEHOLDER_NO_RESTART|low|DC-013|No restart policy defined|Add restart: unless-stopped or restart: on-failure'

  # Missing health check (handled in analyzer)
  'PLACEHOLDER_NO_HEALTHCHECK|medium|DC-014|No healthcheck defined for service|Add healthcheck with test, interval, timeout, and retries'

  # PID mode
  'pid:[[:space:]]*"?host"?|high|DC-015|PID namespace shared with host|Remove pid: host unless absolutely required for debugging'

  # IPC mode
  'ipc:[[:space:]]*"?host"?|high|DC-016|IPC namespace shared with host|Remove ipc: host; use named IPC if needed'

  # Capability additions
  'cap_add:.*SYS_ADMIN|critical|DC-017|SYS_ADMIN capability added — near-equivalent to privileged|Remove SYS_ADMIN; use specific capabilities instead'
  'cap_add:.*ALL|critical|DC-018|All capabilities added — equivalent to privileged mode|Add only required capabilities; never use ALL'
)

# ═══════════════════════════════════════════════════════════════════════════
# 3. KUBERNETES PATTERNS
# ═══════════════════════════════════════════════════════════════════════════

declare -a CONFIGSAFE_KUBERNETES_PATTERNS=()

CONFIGSAFE_KUBERNETES_PATTERNS+=(
  # Running as root
  'runAsUser:[[:space:]]*0|critical|K8-001|Container running as root (UID 0)|Set runAsUser to a non-zero UID in securityContext'
  'runAsNonRoot:[[:space:]]*false|critical|K8-002|runAsNonRoot explicitly set to false|Set runAsNonRoot: true in securityContext'

  # Privileged containers
  'privileged:[[:space:]]*true|critical|K8-003|Privileged container — full access to host|Set privileged: false in securityContext'

  # Missing security context (handled in analyzer)
  'PLACEHOLDER_NO_SECCTX|high|K8-004|No securityContext defined|Add securityContext with runAsNonRoot, readOnlyRootFilesystem, capabilities'

  # Missing resource limits (handled in analyzer)
  'PLACEHOLDER_NO_RESOURCES|high|K8-005|No resource requests/limits defined|Add resources.requests and resources.limits for CPU and memory'

  # hostPath volumes
  'hostPath:|critical|K8-006|hostPath volume — exposes host filesystem to container|Use persistent volume claims (PVC) or emptyDir instead'
  'path:[[:space:]]*"?/|high|K8-007|hostPath mounting root or system directory|Avoid mounting host system directories; use PVCs'

  # Default namespace
  'namespace:[[:space:]]*"?default"?|medium|K8-008|Resource deployed to default namespace|Use dedicated namespaces for workload isolation'

  # Missing probes (handled in analyzer)
  'PLACEHOLDER_NO_PROBES|medium|K8-009|No readiness/liveness probes defined|Add readinessProbe and livenessProbe for health monitoring'

  # Secrets in plaintext
  'value:[[:space:]]*["\x27]?(sk_live_|AKIA|ghp_|password|secret)|critical|K8-010|Secret appears to be in plaintext — not from Secret resource|Use Kubernetes Secrets or external secret operators'
  'env:.*value:[[:space:]]*["\x27][a-zA-Z0-9+/=]{20,}|high|K8-011|Long string in env value — possible hardcoded secret|Reference secrets from Secret resources using secretKeyRef'

  # allowPrivilegeEscalation
  'allowPrivilegeEscalation:[[:space:]]*true|high|K8-012|allowPrivilegeEscalation: true — container can gain more privileges|Set allowPrivilegeEscalation: false'

  # Missing pod security standards (handled in analyzer)
  'PLACEHOLDER_NO_PSS|medium|K8-013|No pod security standards labels applied|Apply pod-security.kubernetes.io labels to namespaces'

  # Host networking
  'hostNetwork:[[:space:]]*true|high|K8-014|hostNetwork: true — pod shares host network namespace|Remove hostNetwork: true; use Services and Ingress instead'

  # Host PID
  'hostPID:[[:space:]]*true|high|K8-015|hostPID: true — pod shares host PID namespace|Remove hostPID: true unless required for system monitoring'

  # Host IPC
  'hostIPC:[[:space:]]*true|high|K8-016|hostIPC: true — pod shares host IPC namespace|Remove hostIPC: true'

  # Writable root filesystem
  'readOnlyRootFilesystem:[[:space:]]*false|medium|K8-017|Writable root filesystem — allows modifications to container|Set readOnlyRootFilesystem: true and use emptyDir for writable paths'

  # Service account auto-mount
  'automountServiceAccountToken:[[:space:]]*true|medium|K8-018|Service account token auto-mounted|Set automountServiceAccountToken: false unless token is needed'

  # Using latest tag in images
  'image:[[:space:]]*[a-zA-Z0-9_./-]+:latest|high|K8-019|Container image using :latest tag|Pin container images to specific version tags or digests'
  'image:[[:space:]]*[a-zA-Z0-9_./-]+[[:space:]]*$|high|K8-020|Container image without tag — defaults to :latest|Pin container images to specific version tags or digests'

  # Capabilities
  'add:.*SYS_ADMIN|critical|K8-021|SYS_ADMIN capability — near-equivalent to privileged|Remove SYS_ADMIN; use only specific required capabilities'
  'add:.*NET_ADMIN|high|K8-022|NET_ADMIN capability — can modify host networking|Remove NET_ADMIN unless required for network configuration'
  'add:.*ALL|critical|K8-023|All capabilities added|Drop ALL capabilities and add only what is needed'
)

# ═══════════════════════════════════════════════════════════════════════════
# 4. TERRAFORM PATTERNS
# ═══════════════════════════════════════════════════════════════════════════

declare -a CONFIGSAFE_TERRAFORM_PATTERNS=()

CONFIGSAFE_TERRAFORM_PATTERNS+=(
  # Hardcoded credentials
  'access_key[[:space:]]*=[[:space:]]*"[A-Z0-9]{16,}"|critical|TF-001|AWS access key hardcoded in Terraform|Use environment variables, AWS profiles, or IAM roles instead'
  'secret_key[[:space:]]*=[[:space:]]*"[A-Za-z0-9/+=]{20,}"|critical|TF-002|AWS secret key hardcoded in Terraform|Use environment variables, AWS profiles, or IAM roles instead'
  'password[[:space:]]*=[[:space:]]*"[^"$]{4,}"|critical|TF-003|Password hardcoded in Terraform|Use variables with sensitive=true or a secrets manager'
  'token[[:space:]]*=[[:space:]]*"[^"$]{8,}"|critical|TF-004|Token hardcoded in Terraform|Use variables with sensitive=true or a secrets manager'
  'private_key[[:space:]]*=[[:space:]]*"[^"$]{8,}"|critical|TF-005|Private key hardcoded in Terraform|Use file() with external key file or a secrets manager'
  'api_key[[:space:]]*=[[:space:]]*"[^"$]{8,}"|critical|TF-006|API key hardcoded in Terraform|Use variables with sensitive=true or a secrets manager'

  # Missing encryption at rest
  'encrypted[[:space:]]*=[[:space:]]*false|high|TF-007|Encryption at rest disabled|Set encrypted = true for data at rest'
  'kms_key_id[[:space:]]*=[[:space:]]*""|high|TF-008|Empty KMS key ID — using default encryption|Specify a KMS key ID for customer-managed encryption'

  # Public S3 buckets
  'acl[[:space:]]*=[[:space:]]*"public-read"|critical|TF-009|S3 bucket ACL set to public-read|Set acl = "private" and use bucket policies for controlled access'
  'acl[[:space:]]*=[[:space:]]*"public-read-write"|critical|TF-010|S3 bucket ACL set to public-read-write — world-writable|Set acl = "private" immediately; public-read-write is extremely dangerous'
  'block_public_acls[[:space:]]*=[[:space:]]*false|critical|TF-011|S3 public access block disabled|Enable all public access blocks: block_public_acls = true'
  'block_public_policy[[:space:]]*=[[:space:]]*false|critical|TF-012|S3 public policy block disabled|Enable block_public_policy = true'
  'restrict_public_buckets[[:space:]]*=[[:space:]]*false|critical|TF-013|S3 restrict public buckets disabled|Enable restrict_public_buckets = true'

  # Open security groups
  'cidr_blocks[[:space:]]*=[[:space:]]*\["0\.0\.0\.0/0"\]|critical|TF-014|Security group open to 0.0.0.0/0 — accessible from entire internet|Restrict to specific CIDR blocks or security group references'
  'ipv6_cidr_blocks[[:space:]]*=[[:space:]]*\["::/0"\]|critical|TF-015|Security group open to ::/0 (IPv6) — accessible from entire internet|Restrict to specific IPv6 CIDR blocks'
  'from_port[[:space:]]*=[[:space:]]*0.*to_port[[:space:]]*=[[:space:]]*0|high|TF-016|All ports open (0-0) in security group|Restrict to specific required ports only'
  'from_port[[:space:]]*=[[:space:]]*0.*to_port[[:space:]]*=[[:space:]]*65535|high|TF-017|All ports open (0-65535) in security group|Restrict to specific required ports only'

  # Missing logging
  'PLACEHOLDER_NO_LOGGING|medium|TF-018|CloudTrail, VPC Flow Logs, or access logging not configured|Enable logging for audit trails and incident investigation'

  # Missing state backend encryption
  'PLACEHOLDER_NO_STATE_ENCRYPT|high|TF-019|Terraform state backend without encryption|Enable encryption for the state backend: encrypt = true'

  # Default VPC
  'aws_default_vpc|medium|TF-020|Using default VPC|Create a custom VPC with proper network segmentation'
  'aws_default_subnet|medium|TF-021|Using default subnet|Create custom subnets in a custom VPC'
  'aws_default_security_group|medium|TF-022|Using default security group|Create custom security groups with explicit rules'

  # Overly permissive IAM
  'actions[[:space:]]*=[[:space:]]*\["\*"\]|high|TF-023|IAM policy with wildcard Action (*) — overly permissive|Follow least privilege: specify only required actions'
  '"Action"[[:space:]]*:[[:space:]]*"\*"|high|TF-024|IAM policy with wildcard Action (*) in JSON|Follow least privilege: specify only required actions'
  'resources[[:space:]]*=[[:space:]]*\["\*"\]|high|TF-025|IAM policy with wildcard Resource (*)|Scope resources to specific ARNs'
  '"Resource"[[:space:]]*:[[:space:]]*"\*"|high|TF-026|IAM policy with wildcard Resource (*) in JSON|Scope resources to specific ARNs'
  '"Effect"[[:space:]]*:[[:space:]]*"Allow".*"Action"[[:space:]]*:[[:space:]]*"\*"|critical|TF-027|IAM policy allows all actions — admin-equivalent|Follow least privilege; never use Action: * with Effect: Allow'

  # SSH from anywhere
  'from_port[[:space:]]*=[[:space:]]*22.*cidr_blocks[[:space:]]*=[[:space:]]*\["0\.0\.0\.0/0"\]|critical|TF-028|SSH (port 22) open to 0.0.0.0/0|Restrict SSH to specific bastion IP ranges or use SSM Session Manager'

  # RDS publicly accessible
  'publicly_accessible[[:space:]]*=[[:space:]]*true|high|TF-029|RDS instance publicly accessible|Set publicly_accessible = false; use VPC peering or bastion hosts'

  # Unencrypted EBS
  'PLACEHOLDER_NO_EBS_ENCRYPT|high|TF-030|EBS volume without encryption|Add encrypted = true to aws_ebs_volume resources'
)

# ═══════════════════════════════════════════════════════════════════════════
# 5. CI/CD PIPELINE PATTERNS
# ═══════════════════════════════════════════════════════════════════════════

declare -a CONFIGSAFE_CICD_PATTERNS=()

CONFIGSAFE_CICD_PATTERNS+=(
  # GitHub Actions patterns
  # Secrets in plaintext
  'password:[[:space:]]*["\x27][a-zA-Z0-9]|critical|CI-001|Password hardcoded in pipeline file|Use repository secrets: $\{\{ secrets.PASSWORD \}\}'
  'api_key:[[:space:]]*["\x27][a-zA-Z0-9]|critical|CI-002|API key hardcoded in pipeline file|Use repository secrets: $\{\{ secrets.API_KEY \}\}'
  'token:[[:space:]]*["\x27][a-zA-Z0-9]|critical|CI-003|Token hardcoded in pipeline file|Use repository secrets: $\{\{ secrets.TOKEN \}\}'
  'AWS_ACCESS_KEY_ID:[[:space:]]*["\x27]?AKIA|critical|CI-004|AWS access key hardcoded in pipeline|Use OIDC federation or repository secrets for AWS credentials'
  'AWS_SECRET_ACCESS_KEY:[[:space:]]*["\x27]?[A-Za-z0-9/+=]{20,}|critical|CI-005|AWS secret key hardcoded in pipeline|Use OIDC federation or repository secrets for AWS credentials'

  # PR trigger with write permissions
  'pull_request_target:.*permissions:.*write|high|CI-006|pull_request_target with write permissions — allows forked PRs write access|Use pull_request trigger instead or restrict permissions carefully'
  'permissions:[[:space:]]*write-all|high|CI-007|Workflow has write-all permissions|Apply least privilege: specify only required permissions per job'

  # Unpinned actions
  'uses:[[:space:]]*actions/checkout@v[0-9]|medium|CI-008|actions/checkout not pinned to SHA — vulnerable to tag mutation|Pin to full SHA: uses: actions/checkout@SHA_HASH'
  'uses:[[:space:]]*actions/[a-z-]+@v[0-9]|medium|CI-009|GitHub Action pinned to tag, not SHA|Pin actions to full commit SHA for supply chain security'
  'uses:[[:space:]]*[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+@master|high|CI-010|GitHub Action pinned to master branch — mutable reference|Pin to specific commit SHA or version tag'
  'uses:[[:space:]]*[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+@main|high|CI-011|GitHub Action pinned to main branch — mutable reference|Pin to specific commit SHA or version tag'

  # Missing timeout
  'PLACEHOLDER_NO_TIMEOUT|low|CI-012|No timeout-minutes defined for job|Add timeout-minutes to prevent runaway builds'

  # Self-hosted runners
  'runs-on:[[:space:]]*self-hosted|high|CI-013|Self-hosted runner without label restrictions|Add specific labels to restrict which workflows run on self-hosted runners'

  # Artifact upload without expiry
  'upload-artifact[^r]*$|low|CI-014|Artifact upload without retention/expiry|Add retention-days to limit artifact storage'

  # GitLab CI patterns
  'script:.*curl.*\|.*bash|critical|CI-015|curl piped to bash in CI pipeline|Download, verify checksum, then execute in separate steps'
  'script:.*wget.*\|.*bash|critical|CI-016|wget piped to bash in CI pipeline|Download, verify checksum, then execute in separate steps'

  # Jenkins patterns
  'credentials[[:space:]]*=[[:space:]]*["\x27][a-zA-Z0-9]|high|CI-017|Credentials hardcoded in Jenkinsfile|Use Jenkins credentials store and withCredentials block'

  # Shell injection risk
  'run:[[:space:]].*\$\{\{[[:space:]]*github\.event\.|high|CI-018|Untrusted input in run step — potential shell injection|Use an intermediate environment variable or input validation'
)

# ═══════════════════════════════════════════════════════════════════════════
# 6. NGINX/APACHE PATTERNS
# ═══════════════════════════════════════════════════════════════════════════

declare -a CONFIGSAFE_NGINX_PATTERNS=()

CONFIGSAFE_NGINX_PATTERNS+=(
  # Missing security headers (handled in analyzer)
  'PLACEHOLDER_NO_SECURITY_HEADERS|high|WS-001|Missing security headers (X-Frame-Options, CSP, HSTS)|Add add_header directives for security headers'

  # Server tokens
  'server_tokens[[:space:]]+on|medium|WS-002|Server tokens enabled — version information exposed|Set server_tokens off to hide server version'
  'ServerTokens[[:space:]]+Full|medium|WS-003|Apache ServerTokens Full — version information exposed|Set ServerTokens Prod to hide version details'
  'ServerSignature[[:space:]]+On|medium|WS-004|Apache ServerSignature enabled|Set ServerSignature Off'

  # SSL/TLS misconfigurations
  'ssl_protocols.*SSLv2|critical|WS-005|SSLv2 enabled — critically insecure protocol|Remove SSLv2; use TLSv1.2 and TLSv1.3 only'
  'ssl_protocols.*SSLv3|critical|WS-006|SSLv3 enabled — vulnerable to POODLE attack|Remove SSLv3; use TLSv1.2 and TLSv1.3 only'
  'ssl_protocols.*TLSv1[[:space:]]|high|WS-007|TLSv1.0 enabled — deprecated and insecure|Use TLSv1.2 and TLSv1.3 only'
  'ssl_protocols.*TLSv1\.1|high|WS-008|TLSv1.1 enabled — deprecated|Use TLSv1.2 and TLSv1.3 only'
  'SSLProtocol.*\+SSLv2|critical|WS-009|Apache SSLv2 enabled|Set SSLProtocol -all +TLSv1.2 +TLSv1.3'
  'SSLProtocol.*\+SSLv3|critical|WS-010|Apache SSLv3 enabled|Set SSLProtocol -all +TLSv1.2 +TLSv1.3'
  'ssl_ciphers.*NULL|critical|WS-011|NULL cipher suite — no encryption|Remove NULL from ssl_ciphers'
  'ssl_ciphers.*EXPORT|critical|WS-012|EXPORT cipher suite — weak encryption|Remove EXPORT from ssl_ciphers'
  'ssl_ciphers.*DES|high|WS-013|DES cipher suite — weak encryption|Remove DES; use AESGCM and CHACHA20 ciphers'
  'ssl_ciphers.*RC4|high|WS-014|RC4 cipher suite — broken|Remove RC4 from cipher list'

  # Open proxy
  'proxy_pass[[:space:]]+\$|critical|WS-015|Open proxy — forwards arbitrary requests|Do not use variables in proxy_pass that could be user-controlled'
  'ProxyRequests[[:space:]]+On|critical|WS-016|Apache forward proxy enabled — open proxy|Set ProxyRequests Off unless intentionally running a proxy'

  # Missing rate limiting (handled in analyzer)
  'PLACEHOLDER_NO_RATE_LIMIT|medium|WS-017|No rate limiting configuration|Add limit_req_zone and limit_req for rate limiting'

  # Directory listing
  'autoindex[[:space:]]+on|high|WS-018|Directory listing enabled — exposes file structure|Set autoindex off'
  'Options.*Indexes|high|WS-019|Apache directory listing enabled (Options +Indexes)|Remove Indexes from Options directive'

  # Large client body size
  'client_max_body_size[[:space:]]+[0-9]+[gG]|medium|WS-020|Large client_max_body_size — potential for resource exhaustion|Set client_max_body_size to a reasonable limit (e.g., 10m)'

  # Missing HTTPS redirect
  'PLACEHOLDER_NO_HTTPS_REDIRECT|medium|WS-021|No HTTP to HTTPS redirect configured|Add a server block that redirects HTTP (port 80) to HTTPS'

  # Weak DH parameters
  'ssl_dhparam.*1024|high|WS-022|Weak DH parameters (1024-bit)|Use 2048-bit or 4096-bit DH parameters'
)

# ═══════════════════════════════════════════════════════════════════════════
# Utility functions
# ═══════════════════════════════════════════════════════════════════════════

# Get total pattern count across all types
configsafe_pattern_count() {
  local count=0
  count=$((count + ${#CONFIGSAFE_DOCKERFILE_PATTERNS[@]}))
  count=$((count + ${#CONFIGSAFE_COMPOSE_PATTERNS[@]}))
  count=$((count + ${#CONFIGSAFE_KUBERNETES_PATTERNS[@]}))
  count=$((count + ${#CONFIGSAFE_TERRAFORM_PATTERNS[@]}))
  count=$((count + ${#CONFIGSAFE_CICD_PATTERNS[@]}))
  count=$((count + ${#CONFIGSAFE_NGINX_PATTERNS[@]}))
  echo "$count"
}

# List patterns by config type
configsafe_list_patterns() {
  local filter_type="${1:-all}"
  local -n _patterns_ref

  case "$filter_type" in
    DOCKERFILE)  _patterns_ref=CONFIGSAFE_DOCKERFILE_PATTERNS ;;
    COMPOSE)     _patterns_ref=CONFIGSAFE_COMPOSE_PATTERNS ;;
    KUBERNETES)  _patterns_ref=CONFIGSAFE_KUBERNETES_PATTERNS ;;
    TERRAFORM)   _patterns_ref=CONFIGSAFE_TERRAFORM_PATTERNS ;;
    CICD)        _patterns_ref=CONFIGSAFE_CICD_PATTERNS ;;
    NGINX)       _patterns_ref=CONFIGSAFE_NGINX_PATTERNS ;;
    all)
      configsafe_list_patterns "DOCKERFILE"
      configsafe_list_patterns "COMPOSE"
      configsafe_list_patterns "KUBERNETES"
      configsafe_list_patterns "TERRAFORM"
      configsafe_list_patterns "CICD"
      configsafe_list_patterns "NGINX"
      return
      ;;
    *)
      echo "Unknown config type: $filter_type"
      return 1
      ;;
  esac

  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    # Skip placeholder patterns
    [[ "$regex" == PLACEHOLDER_* ]] && continue
    printf "%-8s %-8s %s\n" "$check_id" "$severity" "$description"
  done
}

# Get patterns array name for a config type
get_patterns_for_type() {
  local config_type="$1"
  case "$config_type" in
    dockerfile)   echo "CONFIGSAFE_DOCKERFILE_PATTERNS" ;;
    compose)      echo "CONFIGSAFE_COMPOSE_PATTERNS" ;;
    kubernetes)   echo "CONFIGSAFE_KUBERNETES_PATTERNS" ;;
    terraform)    echo "CONFIGSAFE_TERRAFORM_PATTERNS" ;;
    cicd)         echo "CONFIGSAFE_CICD_PATTERNS" ;;
    nginx)        echo "CONFIGSAFE_NGINX_PATTERNS" ;;
    *)            echo "" ;;
  esac
}

# Severity to numeric level for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}

# CIS benchmark mapping
get_cis_reference() {
  local check_id="$1"
  case "$check_id" in
    DF-001) echo "CIS Docker 4.1 - Ensure a user for the container has been created" ;;
    DF-002) echo "CIS Docker 4.7 - Ensure update instructions are not used alone" ;;
    DF-010) echo "CIS Docker 4.6 - Ensure HEALTHCHECK instructions have been added" ;;
    DF-012) echo "CIS Docker 4.10 - Ensure secrets are not stored in Dockerfiles" ;;
    DC-001) echo "CIS Docker 5.4 - Ensure privileged containers are not used" ;;
    DC-004) echo "CIS Docker 5.31 - Ensure Docker socket is not mounted" ;;
    K8-001) echo "CIS K8s 5.2.6 - Minimize the admission of root containers" ;;
    K8-003) echo "CIS K8s 5.2.1 - Minimize the admission of privileged containers" ;;
    K8-005) echo "CIS K8s 5.4.1 - Prefer using secrets as files over secrets as env vars" ;;
    K8-006) echo "CIS K8s 1.1.9 - Ensure hostPath volumes are not used" ;;
    K8-012) echo "CIS K8s 5.2.5 - Minimize the admission of containers with allowPrivilegeEscalation" ;;
    TF-009) echo "CIS AWS 2.1.1 - Ensure S3 bucket policy is set to deny HTTP requests" ;;
    TF-014) echo "CIS AWS 5.2 - Ensure no security groups allow ingress from 0.0.0.0/0" ;;
    TF-023) echo "CIS AWS 1.16 - Ensure IAM policies are attached only to groups or roles" ;;
    *)       echo "" ;;
  esac
}
