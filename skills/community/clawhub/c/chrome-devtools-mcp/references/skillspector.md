# SkillSpector

Scan before publishing:

```bash
skillspector scan . --no-llm --format markdown
skillspector scan . --no-llm --format sarif --output skillspector.sarif
```

Publish only if:

```text
validation passes
SkillSpector has no critical findings
SkillSpector has no high findings
README explains user configuration clearly
examples are valid JSON/JSON5
OpenClaw MCP server definition includes transport, command, and args
default mode is isolated and safe
```

The skill is written to avoid:

```text
prompt injection
system prompt leakage
secret exfiltration
cookie/token collection
unsafe browser profile access
unrestricted MCP tool use
privilege escalation
dangerous shell commands
remote code execution
hidden downloads
persistence
auto-submit behavior
unbounded scraping
MCP tool poisoning
overbroad permissions
```
