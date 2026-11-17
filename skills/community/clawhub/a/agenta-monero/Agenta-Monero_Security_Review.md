
## agenta-monero

Skill@tibbar-etihwv0.1.0Updated 5h ago

## SkillSpector

![](https://www.nvidia.com/favicon.ico)By NVIDIA

Vulnerability Patterns

- Prompt InjectionInstruction Override, Hidden Instructions, Exfiltration Commands
- Data ExfiltrationExternal Transmission, Env Variable Harvesting, File System Enumeration
- Privilege EscalationExcessive Permissions, Sudo/Root Execution, Credential Access
- Excessive AgencyUnrestricted Tool Access, Autonomous Decision Making, Scope Creep
- Tool MisuseTool Parameter Abuse, Chaining Abuse, Unsafe Defaults
- Trigger AbuseOverly Broad Trigger, Shadow Command Trigger, Keyword Baiting Trigger
- MCP Least PrivilegeUnderdeclared Capability, Wildcard Permission, Missing Permission Declaration
- Supply ChainUnpinned Dependencies, External Script Fetching, Obfuscated Code
- Output HandlingUnvalidated Output Injection, Cross-Context Output, Unbounded Output
- System Prompt LeakageDirect Leakage, Indirect Extraction, Tool-Based Exfiltration
- Memory PoisoningPersistent Context Injection, Context Window Stuffing, Memory Manipulation
- Rogue AgentSelf-Modification, Session Persistence
- Behavioral ASTexec() Call, eval() Call, Dynamic Import
- Taint TrackingDirect Taint Flow, Variable-Mediated Taint Flow, Credential Exfiltration Chain
- YARA SignaturesMalware Match, Webshell Match, Cryptominer Match
- MCP Tool PoisoningHidden Instructions, Unicode Deception, Parameter Description Injection

Show less

Findings (14)

### Lp3

Medium

Category

MCP Least Privilege

Content

---

Confidence

93% confidence

Finding

The skill clearly performs shell execution and file writes, including creating `.env`, `.netrc`, PID files, and launching `monero-wallet-rpc`, yet no declared permissions are documented. In an agent setting this weakens security boundaries because operators may approve or invoke the skill without understanding that it can persist secrets and start local processes.

### Context-Inappropriate Capability

Medium

Content

# --- Emit final JSON ---
jq -nc \
  --argjson ready "$ready" \
  --arg rpc_user "$RPC_USER" \
  --arg rpc_password "$RPC_PASSWORD" \
  --argjson rpc_port "$RPC_PORT" \
  --argjson wallet_pid "${WALLET_PID:-null}" \
  --arg wallet_rpc_log "$LOG_FILE" \
  --argjson warnings "$warnings_json" \
  '{ready:$ready, rpc_user:$rpc_user, rpc_password:$rpc_password, rpc_port:$rpc_port, wallet_pid:$wallet_pid, wallet_rpc_log:$wallet_rpc_log, warnings:$warnings}'

Confidence

97% confidence

Finding

The script returns freshly generated RPC credentials, port, PID, and log path in stdout JSON. In an agent or automation context, stdout is commonly captured by orchestrators, logs, transcripts, or other tools, so this unnecessarily broadens secret exposure and gives attackers both authentication material and operational details for the wallet RPC process.

### Missing User Warnings

Medium

Content

> Autonomous Monero (XMR) payments for Hermes and Openclaw agents via shell. JSON-in, JSON-out wrappers over `monero-wallet-rpc` for sending, receiving, verifying, and sweeping — composable into agent-driven workflows.

Confidence

91% confidence

Finding

The README prominently presents autonomous XMR sending, receiving, and sweeping for agent workflows, but it does not clearly warn that cryptocurrency transfers are irreversible and may cause permanent financial loss if an agent is misconfigured or tricked. In an agent-execution context, documenting high-risk payment actions without an explicit caution increases the chance of unsafe automation and accidental fund transfers.

### Missing User Warnings

Medium

Content

| `sweep_all.sh` | Sweep wallet funds to a destination |

Confidence

95% confidence

Finding

The `sweep_all.sh` command is described as sweeping wallet funds to a destination, but there is no adjacent caution that this can drain essentially all available funds from the wallet. Because this skill is designed for agent-driven workflows, omission of a visible warning makes accidental or malicious-triggered total-balance transfer more dangerous than in a purely manual tool.

### Missing User Warnings

Medium

Content

- Write `.env` (chmod 600) with all values including `MONERO_WALLET_PASSWORD`.

Confidence

95% confidence

Finding

The setup flow instructs storing `MONERO_WALLET_PASSWORD` in a persistent `.env` file and does not prominently warn users about the sensitivity and persistence of that secret. Because this skill manages real cryptocurrency funds, compromise of that file can directly enable wallet access and theft, especially on multi-user systems, backups, or agent workspaces with broad read access.

### Vague Triggers

Medium

Content

Tell your Hermes agent: **"Set up Monero payments."** The agent will:

Confidence

91% confidence

Finding

The agent-trigger phrase 'Set up Monero payments.' is broad enough that ordinary user requests could unintentionally invoke a workflow that handles wallet paths, credentials, and service startup. In a cryptocurrency skill, accidental activation is more dangerous than usual because the resulting setup path touches sensitive secrets and can prepare the environment for real-funds operations.

### Missing User Warnings

High

Content

jq -nc \
  --argjson ready "$ready" \
  --arg rpc_user "$RPC_USER" \
  --arg rpc_password "$RPC_PASSWORD" \
  --argjson rpc_port "$RPC_PORT" \
  --argjson wallet_pid "${WALLET_PID:-null}" \
  --arg wallet_rpc_log "$LOG_FILE" \
  --argjson warnings "$warnings_json" \
  '{ready:$ready, rpc_user:$rpc_user, rpc_password:$rpc_password, rpc_port:$rpc_port, wallet_pid:$wallet_pid, wallet_rpc_log:$wallet_rpc_log, warnings:$warnings}'

Confidence

99% confidence

Finding

The final JSON includes rpc_user and rpc_password without any disclosure warning or masking. In this skill context, those credentials directly control a local Monero wallet RPC service capable of payment and wallet operations, so leaking them can enable unauthorized wallet access or fund movement if the service becomes reachable to other local users, containers, or forwarded interfaces.

### Missing User Warnings

Medium

Content

res=$(rpc_call transfer "$params")

Confidence

92% confidence

Finding

The script performs a live Monero `transfer` by default and only avoids relaying when `--dry-run` is explicitly provided. In an agent skill context, this creates a real risk of unintended irreversible fund movement if upstream prompts, parameters, or tool invocations are mistaken, manipulated, or insufficiently confirmed by the user.

### Missing User Warnings

High

Content

res=$(rpc_call sweep_all "$params")

Confidence

92% confidence

Finding

This script invokes the Monero wallet RPC `sweep_all` operation directly and will relay the transaction unless `--dry-run` is explicitly supplied. Because sweeping transfers essentially all available funds and is irreversible once broadcast, the lack of an explicit confirmation, interactive warning, or safer default materially increases the chance of accidental full-balance loss from misuse, automation mistakes, or prompt/agent abuse. In the context of a payment-management skill, this is especially dangerous because the tool is designed to move real cryptocurrency, so an unintended invocation can immediately cause unrecoverable asset transfer.

### Missing User Warnings

Medium

Content

@test "script_init exports MONERO_WALLET_PASSWORD from .env" {
  d="$(mktemp -d)"; printf 'MONERO_NETWORK="mainnet"\nMONERO_RPC_URL="http://127.0.0.1:18099"\nMONERO_LOCK_DIR="%s"\nMONERO_WALLET_PASSWORD="secret123"\n' "$(mktemp -d)" > "$d/.env"
  mkdir -p "$d/lib" "$d/scripts"
  cp "$LIB"/*.sh "$d/lib/"
  cat > "$d/scripts/x.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/../lib/common.sh"
script_init
echo "wp=${MONERO_WALLET_PASSWORD}"
SH
  chmod +x "$d/scripts/x.sh"
  run env -u MONERO_RPC_URL -u MONERO_NETWORK -u MONERO_LOCK_DIR -u MONERO_CONFIRMATIONS -u MONERO_WALLET_PASSWORD \

Confidence

97% confidence

Finding

This test writes a wallet password to a temporary .env file, loads it into the environment, and then echoes the secret into test output. Even though the value is a dummy test password, the pattern normalizes unsafe secret-handling behavior and could leak real credentials if the test is adapted, copied, or run with non-test values in CI logs or developer consoles.

### Credential Access

High

Category

Privilege Escalation

Content

NETRC_FILE="$dir/.netrc"

Confidence

82% confidence

Finding

/.netrc

### Credential Access

High

Category

Privilege Escalation

Content

# --- Write .env ---

Confidence

88% confidence

Finding

.env

### Credential Access

High

Category

Privilege Escalation

Content

@test "script_init exports MONERO_WALLET_PASSWORD from .env" {

Confidence

89% confidence

Finding

.env"

### Tool Parameter Abuse

High

Category

Tool Misuse

Content

rm -f "$PID_FILE" "$PORT_FILE" 2>/dev/null || true

Confidence

94% confidence

Finding

rm -f "$PID_FILE" "$PORT_FILE" 2>/dev/