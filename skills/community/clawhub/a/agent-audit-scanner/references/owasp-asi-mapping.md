# OWASP Agentic AI Top 10 → Agent Audit Rules

Quick reference for the OpenClaw agent. 56 rules across all 10 OWASP ASI categories.

## ASI-01: Goal Hijacking / Prompt Injection

| Rule | CWE | Detection |
|------|-----|-----------|
| AGENT-010 | CWE-74 | Prompt injection via f-string, concat, format, augassign |
| AGENT-011 | CWE-74 | Agent without input guard |
| AGENT-027 | CWE-79 | LangChain system prompt injectable |
| AGENT-050 | CWE-400 | LangChain AgentExecutor missing safety params |

## ASI-02: Tool Misuse

| Rule | CWE | Detection |
|------|-----|-----------|
| AGENT-026 | CWE-918 | SSRF in tool / expanded |
| AGENT-029 | CWE-732 | MCP overly broad filesystem access |
| AGENT-032 | CWE-250 | MCP stdio without sandbox |
| AGENT-034 | CWE-20 | Tool input without validation (eval/exec/subprocess) |
| AGENT-041 | CWE-89 | SQL injection (f-string/format/concat) |

## ASI-03: Excessive Permissions

| Rule | CWE | Detection |
|------|-----|-----------|
| AGENT-013 | CWE-269 | Hardcoded credential in agent |
| AGENT-014 | CWE-285 | Excessive tools / auto-approval |
| AGENT-028 | CWE-400 | AgentExecutor max_iterations unbounded |
| AGENT-042 | CWE-250 | Excessive MCP servers |

## ASI-04: Supply Chain

| Rule | CWE | Detection |
|------|-----|-----------|
| AGENT-015 | CWE-829 | npx unfixed version / unofficial MCP source |
| AGENT-016 | CWE-494 | Unvalidated RAG ingestion |
| AGENT-030 | CWE-494 | MCP unverified server source |
| **AGENT-062** | CWE-494 | **OpenClaw: fake dependency social engineering** |

## ASI-05: RCE / Unsandboxed Execution

| Rule | CWE | Detection |
|------|-----|-----------|
| AGENT-017 | CWE-94 | Unsandboxed code execution in tool |
| AGENT-031 | CWE-798 | MCP sensitive env exposure |
| AGENT-035 | CWE-77 | Tool unrestricted execution |
| AGENT-049 | CWE-502 | Unsafe deserialization (pickle/torch/joblib) |
| AGENT-053 | CWE-94 | Agent self-modification (importlib) |
| **AGENT-058** | CWE-78 | **OpenClaw: obfuscated shell commands in SKILL.md** |
| **AGENT-061** | CWE-693 | **OpenClaw: sandbox override (sandbox:false)** |

## ASI-06: Memory Poisoning

| Rule | CWE | Detection |
|------|-----|-----------|
| AGENT-018 | CWE-1321 | Unsanitized memory write |
| AGENT-019 | CWE-1321 | Unbounded memory growth |
| **AGENT-059** | CWE-1321 | **OpenClaw: critical file modification (SOUL.md/AGENTS.md)** |

## ASI-07: Inter-Agent Communication

| Rule | CWE | Detection |
|------|-----|-----------|
| AGENT-020 | CWE-311 | Multi-agent no auth / no TLS |

## ASI-08: Cascading Failure

| Rule | CWE | Detection |
|------|-----|-----------|
| AGENT-021 | CWE-754 | Missing circuit breaker |
| AGENT-022 | CWE-754 | Tool without error handling |

## ASI-09: Trust & Transparency

| Rule | CWE | Detection |
|------|-----|-----------|
| AGENT-023 | CWE-345 | Opaque agent output |
| AGENT-033 | CWE-306 | MCP missing authentication |
| AGENT-037 | CWE-862 | Missing human-in-the-loop |
| AGENT-038 | CWE-290 | Agent impersonation risk |
| AGENT-039 | CWE-290 | Trust boundary violation |
| AGENT-040 | CWE-20 | MCP tool schema security |
| **AGENT-060** | CWE-918 | **OpenClaw: suspicious network endpoints in frontmatter** |

## ASI-10: Kill Switch / Observability

| Rule | CWE | Detection |
|------|-----|-----------|
| AGENT-024 | CWE-441 | No kill switch |
| AGENT-025 | CWE-441 | No observability |
| **AGENT-063** | CWE-269 | **OpenClaw: daemon persistence (launchd/systemd)** |
| **AGENT-064** | CWE-862 | **OpenClaw: always:true auto-invocation** |

## General / Cross-Category

| Rule | CWE | Detection |
|------|-----|-----------|
| AGENT-004 | CWE-798 | Hardcoded credentials (secret scanner) |
| AGENT-036 | CWE-862 | Tool output trusted blindly |
| AGENT-043 | CWE-269 | Daemon privilege |
| AGENT-044 | CWE-269 | Sudoers NOPASSWD |
| AGENT-045 | CWE-269 | Browser no-sandbox |
| AGENT-046 | CWE-522 | System credential store access |
| AGENT-047 | CWE-250 | Subprocess without sandbox |
| AGENT-048 | CWE-863 | Extension privilege boundary violation |
| AGENT-052 | CWE-532 | Sensitive data logging |

**Bold** = OpenClaw-specific rules (AGENT-058~064)
