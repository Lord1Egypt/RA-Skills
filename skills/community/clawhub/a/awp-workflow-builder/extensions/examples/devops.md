---
name: awp-ext-devops
description: >
  AWP extension for infrastructure automation, CI/CD, and incident response.
  Adds safety checker agent, rollback plans, and shell execution controls.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    tags:
      - awp
      - awp-extension
      - devops
      - infrastructure
      - ci-cd
---

# AWP Extension: DevOps & Infrastructure Workflows

## Extends

base: skill/SKILL.md
adapter: skill/adapters/standalone.md

## Description

Extension for infrastructure automation, CI/CD pipelines, incident response,
and system monitoring workflows.  Enforces safety controls around destructive
operations, requires approval gates for production changes, and includes
built-in rollback awareness.

Use this extension when building workflows that interact with infrastructure,
deploy code, manage incidents, or automate operational tasks.

## Defaults

```yaml
defaults:
  compliance_level: L3             # Memory for incident history
  model: anthropic/claude-sonnet-4
  execution_mode: conditional      # Gates and approvals
  temperature: 0.0                 # Deterministic for infra operations
  memory:
    long_term: true                # Incident knowledge base
    daily_log: true                # Operational log
  observability:
    tracing: true
    metrics: true
    audit: true
```

## Required Agents

```yaml
agents:
  - id: safety_checker
    role: safety-gate
    description: >
      Reviews proposed infrastructure changes before execution.
      Checks for blast radius, rollback feasibility, and compliance
      with operational policies.  Must approve before any destructive
      agent runs.
    tools: []
    output_fields:
      approved:
        type: boolean
        description: "Whether the proposed change is approved"
        shareable: true
        required: true
      risk_level:
        type: string
        description: "low | medium | high | critical"
        shareable: true
        required: true
      rollback_plan:
        type: string
        description: "How to revert if the change fails"
        shareable: true
        required: true
      blocked_reasons:
        type: array
        items: { type: string }
        description: "Reasons for blocking (empty if approved)"
        shareable: true
        required: true
```

The `safety_checker` MUST run before any agent that uses `shell.execute`
or modifies infrastructure.  Destructive agents MUST depend on
`safety_checker` with condition `output.approved == true`.

## Required Output Fields

Every agent in a DevOps workflow MUST include:

```yaml
fields:
  - name: changes_made
    type: array
    items: { type: string }
    description: "List of changes performed (empty if read-only)"
    shareable: true
    required: true

  - name: rollback_possible
    type: boolean
    description: "Whether this action can be reverted"
    shareable: true
    required: true
```

## Additional Rules

- **D1:** Any agent using `shell.execute` MUST depend on `safety_checker` with condition `output.approved == true`.
- **D2:** Agents performing write operations MUST set `changes_made` in their output (empty list for read-only).
- **D3:** Every workflow MUST have memory enabled (incident history for postmortems).
- **D4:** The `safety_checker` prompt MUST include the current environment (staging/production).
- **D5:** No agent MAY run `rm -rf`, `DROP TABLE`, or equivalent destructive commands without `safety_checker` approval.
- **D6:** All `shell.execute` calls MUST have a timeout of 60 seconds or less.
- **D7:** Workflows targeting production MUST have `security.circuit_breaker.enabled: true`.

## Constraints

```yaml
constraints:
  required_memory_tiers:
    - long_term                    # Incident knowledge base
    - daily_log                    # Operational audit trail
  min_compliance: L3
  max_shell_timeout: 60            # Seconds
  required_sections:
    - memory
    - observability
  conditional_requirements:
    - if_tool: shell.execute
      then_depends_on: safety_checker
      condition: "output.approved == true"
```

## Additional Templates

### System Prompt Prefix

```yaml
templates:
  - file: SYSTEM_PROMPT_PREFIX.md
    inject: prepend
    content: |
      ## Operational Safety Guidelines

      You are operating in an infrastructure context.  Follow these rules:

      1. NEVER execute destructive commands without safety_checker approval.
      2. Always prefer read-only operations over write operations.
      3. Log every change you make in `changes_made`.
      4. Assess whether your actions are reversible (`rollback_possible`).
      5. When uncertain, escalate to the safety_checker rather than proceeding.
      6. Include the target environment (staging/production) in all operations.
```

### Safety Checker System Prompt

```yaml
templates:
  - file: safety_checker_SYSTEM_PROMPT.md
    agent: safety_checker
    inject: replace
    content: |
      # Safety Checker

      You are an infrastructure safety gate.  Your job is to review
      proposed changes from other agents and decide whether they are
      safe to execute.

      ## Input

      You receive proposed actions from other agents via the shared state.
      Each proposal includes what will be changed and the target environment.

      ## Evaluation Criteria

      1. **Blast Radius**: How many systems/users are affected?
         - Single service, non-critical: low
         - Multiple services: medium
         - User-facing or data-affecting: high
         - Production database or auth system: critical

      2. **Rollback Feasibility**: Can we undo this?
         - Fully automated rollback: low risk
         - Manual rollback possible: medium risk
         - Irreversible (data deletion, schema migration): high risk

      3. **Change Window**: Is this the right time?
         - During maintenance window: ok
         - Business hours, staging: ok
         - Business hours, production: needs justification

      ## Decision

      - **approved: true** if risk_level is low or medium AND rollback exists
      - **approved: false** if risk_level is critical OR no rollback plan
      - Always provide a rollback_plan even when approving
      - List specific blocked_reasons when rejecting

      ## Output Format

      Respond with valid JSON matching the output schema.
```

## Additional Skills

```yaml
skills:
  - name: incident_response
    content: |
      # Incident Response Playbook

      ## Severity Levels

      | Level | Response Time | Escalation |
      |-------|--------------|------------|
      | SEV1 (Critical) | Immediate | Page on-call, start bridge |
      | SEV2 (Major) | 15 minutes | Notify team lead |
      | SEV3 (Minor) | 1 hour | Create ticket |
      | SEV4 (Low) | Next business day | Add to backlog |

      ## Response Steps

      1. **Assess**: Determine severity and blast radius
      2. **Mitigate**: Apply immediate fix or rollback
      3. **Communicate**: Update status page and stakeholders
      4. **Resolve**: Deploy permanent fix
      5. **Review**: Postmortem within 48 hours

  - name: infrastructure_patterns
    content: |
      # Infrastructure Patterns

      ## Safe Deployment

      - Blue-green deployments for zero-downtime
      - Canary releases for gradual rollout
      - Feature flags for instant rollback
      - Database migrations must be backwards-compatible

      ## Monitoring Checklist

      - CPU, memory, disk utilization
      - Request latency (p50, p95, p99)
      - Error rate (4xx, 5xx)
      - Queue depth and processing lag
      - SSL certificate expiry
```

## Additional Tools

```yaml
tools:
  - fqn: infra.health_check
    description: "Check health of a service endpoint"
    template: |
      from __future__ import annotations
      from typing import Any, Dict
      try:
          from mcp.server.fastmcp import FastMCP
      except Exception:
          class FastMCP:
              def __init__(self, name): self.name = name
              def tool(self, _name):
                  def _d(fn): return fn
                  return _d

      app = FastMCP("infra")

      @app.tool("infra.health_check")
      def health_check(*, url: str, timeout: int = 10) -> Dict[str, Any]:
          """Check if a service endpoint is healthy.

          Args:
              url: Health check URL (e.g., https://api.example.com/health).
              timeout: Request timeout in seconds.
          """
          try:
              import httpx
              resp = httpx.get(url, timeout=timeout)
              return {
                  "ok": True,
                  "status": resp.status_code,
                  "data": {
                      "healthy": resp.status_code == 200,
                      "status_code": resp.status_code,
                      "response_time_ms": resp.elapsed.total_seconds() * 1000,
                  },
                  "error": None,
              }
          except Exception as e:
              return {"ok": False, "status": 503, "data": {}, "error": str(e)}

  - fqn: infra.run_command
    description: "Execute a shell command with safety constraints"
    template: |
      from __future__ import annotations
      import subprocess
      from typing import Any, Dict
      try:
          from mcp.server.fastmcp import FastMCP
      except Exception:
          class FastMCP:
              def __init__(self, name): self.name = name
              def tool(self, _name):
                  def _d(fn): return fn
                  return _d

      app = FastMCP("infra")

      BLOCKED_PATTERNS = ["rm -rf /", "DROP DATABASE", "DROP TABLE", "mkfs", "dd if="]

      @app.tool("infra.run_command")
      def run_command(*, command: str, timeout: int = 60) -> Dict[str, Any]:
          """Execute a shell command with safety checks.

          Args:
              command: Shell command to execute.
              timeout: Max execution time in seconds (max 60).
          """
          timeout = min(timeout, 60)
          for pattern in BLOCKED_PATTERNS:
              if pattern.lower() in command.lower():
                  return {
                      "ok": False,
                      "status": 403,
                      "data": {},
                      "error": f"Blocked: command matches dangerous pattern '{pattern}'",
                  }
          try:
              result = subprocess.run(
                  command, shell=True, capture_output=True, text=True, timeout=timeout,
              )
              return {
                  "ok": result.returncode == 0,
                  "status": 200 if result.returncode == 0 else 500,
                  "data": {
                      "stdout": result.stdout[:10000],
                      "stderr": result.stderr[:5000],
                      "returncode": result.returncode,
                  },
                  "error": result.stderr[:500] if result.returncode != 0 else None,
              }
          except subprocess.TimeoutExpired:
              return {"ok": False, "status": 408, "data": {}, "error": f"Timeout after {timeout}s"}
```

## Example Usage

Tell the AI:

> "Build a workflow that deploys a new version of our API service
>  to staging, runs health checks, then promotes to production.
>  Use the devops extension."

The AI will:
1. Load `SKILL.md` + adapter + this extension
2. Generate user's agents (e.g., `deployer`, `health_checker`, `promoter`)
3. Add `safety_checker` before any agent using `shell.execute`
4. Wire conditional dependency: `deployer` depends on `safety_checker.approved == true`
5. Add `changes_made` and `rollback_possible` to every output contract
6. Prepend safety guidelines to every system prompt
7. Enable memory (L3) for incident knowledge
8. Place `infra.health_check` and `infra.run_command` tools in `mcp/`
9. Place `incident_response` and `infrastructure_patterns` skills in `skills/`
10. Validate against R1-R24 + D1-D7
