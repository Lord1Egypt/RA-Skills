# SKILL.md: AI Trainer & Learning Specialist

## Overview
This skill empowers the assistant to autonomously learn from online resources, distill complex documentation (like Anthropic Skilljar or MCP guides), and integrate these findings into the system's long-term memory (MEMORY.md) and operational rules (AGENTS.md).

## Capabilities
- **Deep Web Fetching**: Recursively fetch and summarize multi-page documentation sites.
- **Knowledge Distillation**: Extract core primitives, transport patterns, and tool-use strategies from technical docs.
- **System Integration**: Automatically update workspace rules (AGENTS.md) and memory (MEMORY.md) with newly acquired insights.
- **Routing Optimization**: Advise on model selection (e.g., local Ollama vs. Cloud) based on learned task complexity.

## Guidelines
- **Budget First**: When fetching large documentation sites, always estimate potential token usage and ask for Alvin's permission before proceeding.
- **Privacy Core**: Learned data should be stored in the local workspace; sensitive environment variables or keys from documentation should never be logged.
- **Validation**: After learning a new concept (like a new MCP tool pattern), verify its compatibility with the current OpenClaw version before suggesting implementation.

## Tools Allowed
- `web_search`: Find the latest versions of documentation.
- `web_fetch`: Extract markdown content from technical sites.
- `edit`/`write`: Update system configuration and memory files.
- `exec`: Verify local environment status (e.g., Ollama tags, node version).

## Success Metrics
- Successfully summarized and integrated a new technical concept into MEMORY.md.
- Optimized a task flow using a newly learned "Skill" pattern.
- Reduced cloud token burn by offloading a learned simple task to a local model.
