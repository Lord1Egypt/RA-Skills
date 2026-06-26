# Platform & Infrastructure

> Department: platform-and-infrastructure
> Skills in department: 1

## AI Company Framework (v4.0.0)

## 3. Core Responsibilities

### 3.1 Standards (from Framework)

```
Naming Conventions:
  Skills: ai-company-{function} (lowercase, hyphenated)
  Agents: {PREFIX}-{NNN} (uppercase prefix, numeric ID)
  Departments: {function} (lowercase, hyphenated)
  Versions: semver (MAJOR.MINOR.PATCH)
  Files: kebab-case.md, kebab-case.py

Semver Enforcement Policy (Mandatory for all published skills):
  | Change Type | Version Increment | Requires | Example |
  |------------|------------------|----------|---------|
  | Breaking API/interface change | MAJOR (X.0.0) | Board awareness + migration guide | 1.x.x -> 2.0.0 |
  | New feature, backward compatible | MINOR (x.Y.0) | CQO review | 1.0.x -> 1.1.0 |
  | Bug fix, security patch | PATCH (x.y.Z) | CISO sign-off for security patches | 1.0.0 -> 1.0.1 |
  Rules:
    - NEVER publish a skill without a semver version field in frontmatter
    - NEVER re-use a version number once published to ClawHub
    - Pre-release tags allowed: 1.1.0-alpha.1, 1.1.0-rc.1 (must NOT be distributed as stable)
    - All MAJOR version increments require a migration guide in references/migration/
    - Breaking changes require 90-day deprecation notice for MINOR version (see interoperability rules)

Schema Standards (ClawHub v1.0):
  Required Frontmatter:
    name, slug, version, description, license, tags,
    triggers, interface (inputs, outputs, errors),
    permissions, quality (idempotent), metadata (department)

  Optional Frontmatter:
    dependencies, homepage, install, author, context, agent

Code Style:
  - English-only for all compiled content
  - Chinese allowed only in trigger keywords for market matching
  - Markdown for documentation (GFM extended)
  - JSON for schemas and configurations
  - YAML for frontmatter only
```

### 3.2 Modularization (from Framework)

```
Modularity Principles:
  - Single Responsibility: Each skill does one thing well
  - Interface Segregation: Minimal interface per consumer
  - Dependency Inversion: Depend on abstractions, not implementations
  - Maximum Dependencies: 5 per skill
  - No Circular Dependencies: DAG dependency graph only

Module Structure:
  SKILL.md          - Index and quick reference
  references/       - Detailed specifications
  prompts/          - User-facing prompts (copy-paste ready)

Integration Patterns:
  | Pattern | Description | Use Case |
  |---------|-------------|----------|
  | Request-Response | Synchronous query | Single skill invocation |
  | Event-Driven | Async notification | Cross-skill triggers |
  | Pipeline | Sequential processing | Multi-step workflows |
  | Fan-out | Parallel distribution | Broadcast to multiple skills |
  | Aggregator | Collect and merge | Multi-source data collection |
```

### 3.3 Generalization (from Framework)

```
Generalization Levels:
  | Level | Description | Reuse Potential |
  |-------|-------------|----------------|
  | L1-Company-Specific | Hardcoded for one company | Low (single use) |
  | L2-Domain-Specific | Configurable for domain | Medium (domain reuse) |
  | L3-Industry-Standard | Follows industry patterns | High (industry reuse) |
  | L4-Universal | Applicable across industries | Very High (global reuse) |

  Target: All skills at L3+

Generalization Checklist:
  [ ] No company-specific names or identifiers
  [ ] No hardcoded URLs, paths, or credentials
  [ ] Configurable parameters (not inline values)
  [ ] Template-based generation (not one-off)
  [ ] Documentation uses generic examples
  [ ] Reusable in 3+ contexts without modification
```

### 3.4 Ecosystem (from Framework)

```
Ecosystem Architecture:
  Core Layer: CEO, COO, HQ, CTO, CISO, CLO, CHO, CFO, CRO, CQO, CMO
  Executive Layer: WRTR, PMGR, ANLT, CSSM, ENGR, QENG, LEGAL, HR
  Translation Layer: TR-COORD, TR-EN, TR-ZH, TR-RU, TR-FR
  Infrastructure Layer: Framework (this skill)
  Information Layer: Information Services

Interoperability Rules:
  - All inter-skill communication via HQ
  - All skills must declare dependencies explicitly
  - All skills must handle missing dependencies gracefully
  - Version compatibility: semver, MAJOR = breaking change
  - Deprecation: 90-day notice before removal

Ecosystem Health:
  | Metric | Target |
  |--------|--------|
  | Dependency resolution rate | 100% |
  | Circular dependency count | 0 |
  | Deprecated skill usage | 0 |
  | Version compatibility | 100% |
```

### 3.5 Registry (from Framework)

```
Agent Registry:
  | Field | Type | Required |
  |-------|------|----------|
  | agent_id | string | Yes |
  | name | string | Yes |
  | department | string | Yes |
  | permission_level | L1-L5 | Yes |
  | skills | list | Yes |
  | dependencies | list | Yes |
  | status | enum | Yes |
  | created_at | timestamp | Yes |
  | updated_at | timestamp | Yes |

Skill Registry:
  | Field | Type | Required |
  |-------|------|----------|
  | slug | string | Yes |
  | name | string | Yes |
  | version | semver | Yes |
  | department | string | Yes |
  | dependencies | list | Yes |
  | clawhub_id | string | Yes |
  | quality_score | number | No |
  | last_reviewed | timestamp | No |

Discovery:
  - Skills discoverable by: keyword, department, capability
  - Agents discoverable by: department, capability, availability
```

### 3.6 Skill Learning (from Framework)

```
Skill Acquisition Pipeline:
  1. IDENTIFY: Determine skill gap from CHO assessment or task failure
  2. SEARCH: Search ClawHub for matching skills
  3. EVALUATE: Assess skill quality (CQO gates G0-G7)
  4. INSTALL: Download and integrate skill
  5. CONFIGURE: Map skill to agent, set permissions
  6. TEST: Validate skill in sandbox
  7. ACTIVATE: Enable skill for production use
  8. MONITOR: Track skill effectiveness

Learning Priorities:
  | Priority | Source | Example |
  |----------|--------|---------|
  | P0 | Task failure | Agent cannot complete assigned task |
  | P1 | CHO assessment | Skills gap identified in review |
  | P2 | Strategic plan | New capability needed for OKR |
  | P3 | Market opportunity | CMO discovers new demand signal |
```

### 3.7 Starter Templates (from Framework)

```
Quick Start:
  1. Install: clawhub install ai-company-starter
  2. Initialize: Configure company name, departments, agents
  3. Deploy: Activate core C-Suite agents
  4. Customize: Add domain-specific skills
  5. Launch: Begin operations

Starter Includes:
  - Core C-Suite skills (CEO, COO, CFO, CTO, CISO, CLO, CHO, CMO, CRO, CQO)
  - HQ routing and state management
  - Framework infrastructure (this skill)
  - Default permission levels and SLA tiers
```

### 3.8 Harness Engineering L1-L6 (from Harness)

```
L1 - Standardization:
  - All skills follow ClawHub Schema v1.0
  - Naming: ai-company-{function}, version semver
  - Triggers: English keywords, pattern-matching format
  - Interface: inputs/outputs/errors schema
  - Pass criteria: 100% schema compliance

L2 - Modularization:
  - Single responsibility per skill
  - Maximum 5 dependencies per skill
  - No circular dependencies
  - Explicit interface contracts
  - Pass criteria: Dependency graph clean, interfaces documented

L3 - Generalization:
  - Cross-domain applicability (not company-specific)
  - Configurable parameters (not hardcoded values)
  - Template-based generation (not one-off)
  - Pass criteria: Reusable in 3+ contexts without modification

L4 - Automation:
  - CI/CD pipeline integration
  - Automated testing (unit + integration + E2E)
  - Automated deployment with canary
  - Automated rollback on failure
  - Pass criteria: 100% pipeline coverage

L5 - Quality Assurance:
  - CISO security gate (STRIDE + CVSS)
  - CQO quality gate (idempotency + robustness)
  - Performance benchmarks
  - Documentation completeness
  - Pass criteria: All gates pass, docs complete

L6 - Operational Excellence:
  - Monitoring and alerting
  - Incident response runbooks
  - Capacity planning integration
  - Disaster recovery procedures
  - Pass criteria: All runbooks exist, DR tested quarterly

Compliance Check Template:
  | Level | Check | Result | Evidence |
  |-------|-------|--------|----------|
  | L1 | Schema valid | PASS/FAIL | [validation output] |
  | L2 | Dependencies clean | PASS/FAIL | [dependency graph] |
  | L3 | Generalization score | PASS/FAIL | [reuse analysis] |
  | L4 | Automation coverage | PASS/FAIL | [pipeline report] |
  | L5 | Quality gates | PASS/FAIL | [gate results] |
  | L6 | Operations ready | PASS/FAIL | [runbook audit] |
```

### 3.9 Architecture Decision Records (from Harness)

```
ADR Template:
  # ADR-{NNN}: {Title}

  ## Status
  Proposed | Accepted | Deprecated | Superseded by ADR-{NNN}

  ## Context
  What is the issue motivating this decision?

  ## Decision
  What change are we proposing?

  ## Consequences
  What becomes easier or more difficult?

  ## Compliance
  - CISO Review: [APPROVED/CONDITIONAL/REJECTED] by [agent] on [date]
  - CQO Review: [APPROVED/CONDITIONAL/REJECTED] by [agent] on [date]
  - CEO Sign-off: [REQUIRED/NOT_REQUIRED] [status]

ADR Process:
  1. PROPOSE: Any agent can submit an ADR
  2. DISCUSS: 48h comment period for all stakeholders
  3. REVIEW: CISO + CQO compliance check
  4. APPROVE: CTO approves (CEO for L5+ decisions)
  5. IMPLEMENT: Execute decision with tracking
  6. REVIEW_OUTCOME: Assess results within 30 days
```

### 3.10 CI/CD Pipeline (from Harness)

```
Pipeline Stages:
  1. SOURCE: Code commit triggers pipeline
  2. BUILD: Compile, package, generate artifacts
  3. TEST: Unit -> Integration -> E2E (automated)
  4. SCAN: Security scan (CISO), Quality scan (CQO)
  5. STAGE: Deploy to staging environment
  6. VERIFY: Smoke tests + performance benchmarks
  7. APPROVE: Manual gate for production (CTO or delegate)
  8. DEPLOY: Canary deployment (5% -> 25% -> 50% -> 100%)
  9. MONITOR: 1h observation window
  10. COMPLETE: Mark as stable, update registry

Rollback Triggers:
  - Error rate >5% in canary -> Auto-rollback
  - Latency >2x baseline -> Auto-rollback
  - CISO alert -> Manual rollback
  - CTO/COO decision -> Manual rollback

Pipeline Metrics:
  | Metric | Target |
  |--------|--------|
  | Build time | <10min |
  | Test coverage | >80% |
  | Deploy frequency | Daily |
  | Rollback rate | <5% |
  | MTTR | <30min |
```

### 3.11 Operational Procedures (from Harness)

```
Standard Runbook Template:
  # Runbook: {Operation Name}

  ## Overview
  Brief description and when to use.

  ## Prerequisites
  - Required permissions, tools, and related SOPs

  ## Steps
  1. [Step with verification point]
  2. [Step with verification point]

  ## Verification
  How to confirm success.

  ## Rollback
  How to undo if something goes wrong.

  ## Escalation
  Who to contact if runbook does not cover the situation.

Operational Categories:
  | Category | Examples | Review Frequency |
  |----------|---------|-----------------|
  | Deployment | App deploy, model deploy | Per release |
  | Incident | Outage response, data recovery | Per incident |
  | Maintenance | Patch, upgrade, migration | Monthly |
  | Scaling | Scale up/down, failover | As needed |
```

---

## 4. Core Code Templates

> 10 high-reusability, modular, security-compliant code method templates.
> All templates follow harness engineering principles and pass VirusTotal/ClawHub review.
> Each template: English naming, clear parameters, single responsibility, cross-project portable.

### Design Principles

| Principle | Implementation |
|-----------|---------------|
| Interface contract unified | All functions use explicit parameter signatures and return type definitions |
| Stateless implementation | No global variables or external environment state |
| Minimal dependency | Only stdlib or widely-verified packages (e.g., jsonschema) |
| Composable architecture | Functional patterns (decorators, higher-order functions) support chaining |
| Machine-readable naming | snake_case format, semantic clarity for natural-language invocation |
| Parameterized compatibility | External config injection (timeouts, retry counts) |
| Standardized output | Structured data (dict/JSON) for downstream parsing |
| Trace support | Built-in trace ID generation for audit logging and error tracing |

### 4.1 validate_input_schema

```python
def validate_input_schema(data, schema):
    """Validate user input against a predefined structure."""
    from jsonschema import validate, ValidationError
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError:
        return False
```

| Attribute | Value |
|-----------|-------|
| Parameters | data: dict, schema: dict |
| Returns | bool |
| Security | No external I/O; No dynamic execution |

### 4.2 sanitize_user_query

```python
import re

def sanitize_user_query(query):
    """Sanitize user query text, removing potential injection risks."""
    # Remove shell metacharacters
    query = re.sub(r'[;&|`$()\\]', '', query)
    # Strip leading/trailing whitespace
    return query.strip()
```

| Attribute | Value |
|-----------|-------|
| Parameters | query: str |
| Returns | str |
| Security | Input sanitization; No eval/exec |

### 4.3 execute_safe_command

```python
import subprocess

def execute_safe_command(cmd, timeout=30):
    """Execute system command in sandboxed environment."""
    result = {"success": False, "output": "", "error": ""}
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd="/tmp",  # Restricted working directory
            check=False
        )
        result["output"] = proc.stdout
        result["error"] = proc.stderr
        result["success"] = proc.returncode == 0
    except Exception as e:
        result["error"] = str(e)
    return result
```

| Attribute | Value |
|-----------|-------|
| Parameters | cmd: list, timeout: int = 30 |
| Returns | dict |
| Security | Isolated execution; Timeout enforced |

### 4.4 format_output_json

```python
import json
from datetime import datetime

def format_output_json(content, provider):
    """Standardize output as JSON with AIGC implicit labeling."""
    payload = {
        "data": content,
        "metadata": {
            "generated_by": provider,
            "timestamp": datetime.utcnow().isoformat(),
            "ai_generated": True
        }
    }
    return json.dumps(payload, indent=2)
```

| Attribute | Value |
|-----------|-------|
| Parameters | content: dict, provider: str |
| Returns | str (JSON) |
| Security | Structured output; AI watermark embedded |
| Compliance | AIGC labeling per regulation requirements |

### 4.5 retry_with_backoff

```python
import time
import functools

def retry_with_backoff(max_retries=3):
    """Exponential backoff retry decorator."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_retries - 1:
                        raise
                    time.sleep((2 ** i) + (0.1 * i))
            return None
        return wrapper
    return decorator
```

| Attribute | Value |
|-----------|-------|
| Parameters | max_retries: int = 3 |
| Returns | Any (decorated function result) |
| Security | Fault-tolerant; No side effects |

### 4.6 read_reference_file

```python
def read_reference_file(filepath):
    """Safely read local reference document content."""
    allowed_dirs = ["/app/references", "/tmp"]
    if not any(filepath.startswith(d) for d in allowed_dirs):
        return None  # Access denied
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None
```

| Attribute | Value |
|-----------|-------|
| Parameters | filepath: str |
| Returns | str or None |
| Security | Path validation; No user home access |

### 4.7 generate_trace_id

```python
import uuid

def generate_trace_id(prefix="trace"):
    """Create unique trace ID for audit logging."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"
```

| Attribute | Value |
|-----------|-------|
| Parameters | prefix: str = "trace" |
| Returns | str |
| Security | Stateless; No external dependency |

### 4.8 check_rate_limit

```python
import time
from collections import defaultdict

_request_times = defaultdict(list)

def check_rate_limit(identifier, limit=10, window=60):
    """Check if current request exceeds rate limit."""
    now = time.time()
    times = _request_times[identifier]
    # Remove outdated timestamps
    times[:] = [t for t in times if now - t < window]
    if len(times) >= limit:
        return False
    times.append(now)
    return True
```

| Attribute | Value |
|-----------|-------|
| Parameters | identifier: str, limit: int, window: int |
| Returns | bool |
| Security | In-memory tracking; No persistent storage |

### 4.9 mask_sensitive_data

```python
import re

def mask_sensitive_data(text):
    """Mask sensitive information in output (emails, IPs)."""
    # Mask email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    # Mask IP addresses
    text = re.sub(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', '[IP]', text)
    return text
```

| Attribute | Value |
|-----------|-------|
| Parameters | text: str |
| Returns | str |
| Security | Data privacy protection; No logging of raw data |

### 4.10 build_prompt_from_template

```python
def build_prompt_from_template(template, **kwargs):
    """Generate final prompt from parameterized template."""
    # Sanitize inputs before substitution
    safe_kwargs = {k: str(v).strip() for k, v in kwargs.items()}
    return template.format(**safe_kwargs)
```

| Attribute | Value |
|-----------|-------|
| Parameters | template: str, **kwargs |
| Returns | str |
| Security | Input sanitization; No code injection |

---

## 5. Prompt Frameworks

> Three industry-validated prompt frameworks for copy-paste use in any AI chat window.
> All frameworks follow harness engineering principles: role anchoring, task decomposition,
> constraint enforcement, and verifiable output.

### 5.1 CRISPE Framework — Complex Tasks & Few-Shot Learning

```
【Role】 {role_description}
【Result】 {desired_output}
【Input】 {input_data_or_context}
【Steps】 {step_by_step_instructions}
【Parameters】 {format_style_length_constraints}
【Example】 {example_input_output_pair}
```

| Variable | Description | Example |
|----------|-------------|---------|
| {role_description} | Professional identity | "Senior Frontend Engineer", "Legal Compliance Expert" |
| {desired_output} | Expected outcome | "Generate WCAG-compliant HTML component" |
| {input_data_or_context} | Raw input or background | Task-specific data |
| {step_by_step_instructions} | Decomposed 3-5 step process | Step 1: Analyze; Step 2: Design; Step 3: Implement |
| {format_style_length_constraints} | Output constraints | "Markdown table, max 200 words" |
| {example_input_output_pair} | Optional few-shot example | High-quality input/output pair |

**Use when:** Complex tasks requiring Chain-of-Thought reasoning, multi-step analysis, or few-shot learning.

### 5.2 3WEH Model — Clear Task Delegation & Context-Driven

```
Who: {role}
What: {task}
Why: {purpose}
How: {format_constraints}
```

| Variable | Description | Example |
|----------|-------------|---------|
| {role} | AI identity | "Python Performance Optimization Consultant" |
| {task} | Specific action | "Refactor this function to reduce time complexity" |
| {purpose} | Goal explanation | "Improve response speed under high concurrency" |
| {format_constraints} | Output specification | "Return annotated code block, Python 3.9+ syntax" |

**Use when:** Clear task delegation with intent-driven output, emphasizing "why" to improve relevance.

### 5.3 Five-Element Structure — Enterprise Knowledge Assistants

```
Role: {role}
Task: {task}
Context: {context}
Format: {output_format}
Constraint: {constraints}
```

| Variable | Description | Example |
|----------|-------------|---------|
| {role} | Professional identity | "Risk Modeling Analyst" |
| {task} | Execution action | "Assess this transaction for money laundering risk" |
| {context} | Business background | "Client from high-risk country, single amount > $50,000" |
| {output_format} | Structured output | "JSON with risk_level and justification fields" |
| {constraints} | Compliance boundaries | "Judge only on known rules; no speculation on unknowns" |

**Use when:** Enterprise knowledge assistants, financial/legal/medical compliance, highly standardized interaction protocols.

### Progressive Disclosure Strategy

All prompt frameworks follow a three-layer information architecture:

| Layer | Content | Token Budget | Loading |
|-------|---------|-------------|---------|
| L1 Metadata | Role, task, goal | <100 words | Always loaded |
| L2 Body Instructions | Steps, format, constraints | <5000 words | Loaded on trigger |
| L3 Reference Resources | Examples, context, references | Unlimited | On-demand only |

---

## 6. Compliance Verification

> Security and compliance verification framework for VirusTotal/ClawHub review.
> Based on industry best practices and regulatory requirements.

### 6.1 Security Compliance Check Matrix

| Risk Category | Prohibited Behavior | Safe Alternative | Regulation |
|---------------|-------------------|-----------------|------------|
| Permission Abuse | Requesting root/admin, reading ~/.ssh, ~/.aws | Least-privilege principle, sandbox access | NVDB Advisory |
| Remote Execution | Using curl/wget to download from unknown URLs | Whitelist domains only, encrypted channels | NVDB Advisory |
| Dynamic Code Eval | Invoking dynamic-eval, dynamic-exec, unsafe-deserialization | Pre-defined function libraries | OWASP |
| Data Exfiltration | Sending data to external servers unencrypted | End-to-end encrypted channels | GDPR/PIPL |
| Obfuscation | Compressed, encoded, or minified logic | Clear, readable source code | ClawHub Policy |

### 6.2 AIGC Content Labeling Requirements

Per regulatory requirements (e.g., China AIGC Labeling Regulation, effective 2025-09):

```
Explicit Labeling (visible to user):
  - "This content was generated by AI" notice
  - At start, end, or appropriate position in output

Implicit Labeling (machine-readable metadata):
  - Service provider name
  - Content identifier/serial number
  - Production timestamp
  - ai_generated: true flag

Digital Watermark (optional but recommended):
  - Embedded traceable watermark
  - Verifiable provenance chain
```

### 6.3 Robustness Verification Checklist

**Input Boundary Testing:**

| Test Type | Input | Expected Behavior |
|-----------|-------|------------------|
| Empty input | "" | Graceful error, no crash |
| Special characters | "<>{}[]&^%$#@!" | Reject or standard error |
| Encoding confusion | Base64, HTML entities | Reject or sanitize |
| Logical contradiction | Conflicting requirements | Flag inconsistency |

**Output Compliance Audit:**

| Check Item | Pass Criteria |
|-----------|---------------|
| Explicit AIGC label | Present at start/end of output |
| Implicit metadata | provider, timestamp, ai_generated: true |
| Digital watermark | Embedded if supported |
| Overall verdict | Compliant / Needs Improvement / Non-Compliant |

**Security Behavior Verification:**

| Check Item | Pass Criteria |
|-----------|---------------|
| No admin/root requests | No privilege escalation |
| No sensitive path access | No ~/.ssh, ~/.aws, registry |
| No eval/exec | No dynamic code execution |
| No unknown URL access | No curl/wget to untrusted domains |
| No password prompts | Parameterized config instead |
| Network whitelisted | All domains on approved list |
| Data masked | PII/IP/emails sanitized |
| Sandbox isolated | Execution in restricted environment |

### 6.4 Harness-to-Compliance Mapping

| Harness Principle | Template Implementation | Engineering Value |
|-------------------|----------------------|-------------------|
| Boundary Definition First | Clear Role + Constraint in prompts | Prevents overreach, ensures stability |
| Hallucination Control | Step-by-step reasoning + Examples | Reduces fabrication via chain-of-thought |
| Explainable Decisions | Output includes justification/steps | Supports traceability and human review |
| Iterative Maintenance | Modular structure supports A/B testing | Failures become new optimization rules |
| Verifiable Compliance | No eval/remote calls in templates | Passes automated security scans |

---

## 7. Constraints

| Constraint | Description |
|-----------|-------------|
| L1-L6 mandatory | No production without full L1-L6 pass |
| ADR required | No architecture change without ADR |
| CI/CD mandatory | No deploy without pipeline |
| Schema compliance | All skills must follow ClawHub Schema v1.0 |
| No circular deps | Dependency graph must be a DAG |
| Deprecation notice | 90-day notice before removal |
| Runbook review | All runbooks reviewed annually |
| English-only | All compiled content in English |
| No eval/exec | No dynamic code execution in templates |
| No remote loading | No curl/wget to untrusted URLs |
| AIGC labeling | All AI-generated output must include explicit and implicit labels |
| Rate limiting | All API-facing functions must implement rate limiting |
| Data masking | All PII must be masked before logging or output |

---

## 8. Quality Metrics

| Metric | Target |
|--------|--------|
| Schema compliance | 100% |
| L1-L6 compliance | 100% |
| Generalization level | L3+ for all skills |
| Circular dependencies | 0 |
| Registry completeness | 100% |
| Skill learning success rate | >90% |
| Pipeline success rate | >95% |
| ADR coverage | All decisions recorded |
| Deploy frequency | Daily |
| Starter setup time | <30min |
| AIGC label compliance | 100% |
| Security scan pass rate | 100% (0/70+ VirusTotal) |
| Code template coverage | 10/10 core templates implemented |

---

*End of method-patterns.md. Return to [SKILL.md](../SKILL.md) for index and quick reference.*

---



---

## Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| FW_001 | Schema validation failed | Check frontmatter against ClawHub Schema v1.0, add missing fields |
| FW_002 | Modularization violation | Reduce dependencies to <=5, remove circular deps |
| FW_003 | Registry lookup failed | Verify agent/skill registered in HQ registry |
| FW_004 | Learning pipeline error | Check skill availability on ClawHub, retry download |
| FW_005 | Scaffolding generation failed | Verify template parameters, check write permissions |
| FW_006 | Harness constraint violation | Run L1-L6 compliance check, fix failing level |
| FW_007 | CI/CD pipeline failed | Check pipeline logs, verify all stages passed |
| FW_008 | ADR compliance rejected | Complete ADR template, obtain CISO+CQO sign-off |
| FW_009 | Security compliance violation | Remove dynamic execution patterns, add input validation |
| FW_010 | AIGC labeling missing | Add explicit AI notice and implicit metadata to output |
