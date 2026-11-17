# Industry Architecture Signals

Use these sources to inform production architecture judgment. Do not copy repository code, starters, templates, or vendor-specific cloud stacks. Use them as signals for patterns, tradeoffs, and risk controls.

## How to Use

- Use these sources only after the user brief is known.
- Extract architecture principles, not vendor lock-in.
- Prefer local, testable, minimal implementations unless the brief requires cloud-scale services.
- Translate enterprise/cloud patterns into the target app's actual runtime boundary.
- Do not add orchestration, governance, observability, persistence, queues, or multi-agent layers unless the brief justifies them.

## Sources

- OpenAI, "A practical guide to building agents": https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- OpenAI Agents SDK JS docs: https://openai.github.io/openai-agents-js/
- OpenAI Agents SDK orchestration concepts: https://openai.github.io/openai-agents-python/multi_agent/
- OpenAI Workspace Agents overview: https://openai.com/academy/workspace-agents/
- Anthropic, "Building Effective AI Agents": https://resources.anthropic.com/building-effective-ai-agents
- Anthropic Model Context Protocol docs: https://docs.anthropic.com/en/docs/mcp
- Anthropic computer use tool docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- AWS Architecture Blog, "Architecting for agentic AI development on AWS": https://aws.amazon.com/blogs/architecture/architecting-for-agentic-ai-development-on-aws/
- AWS Prescriptive Guidance, "Agentic AI architecture in the enterprise": https://docs.aws.amazon.com/prescriptive-guidance/latest/govern-architect-agentic-ai/enterprise-architecture.html
- AWS Well-Architected Generative AI Lens update: https://aws.amazon.com/blogs/architecture/announcing-the-updated-aws-well-architected-generative-ai-lens/
- Google Cloud Blog, "Five guides to building and scaling production-ready AI agents": https://cloud.google.com/blog/topics/developers-practitioners/five-guides-to-building-and-scaling-production-ready-ai-agents
- Microsoft Azure Architecture Center, "AI agent orchestration patterns": https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- Microsoft Azure Architecture Center, "Dynamic AI agents at scale pattern": https://learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/ai-agents-at-scale

## Pattern Signals to Consider

- Agent design foundations: model, instructions, tools, orchestration, and guardrails must be explicit.
- Agent loop ownership: decide whether the app owns the loop directly or delegates turn/tool/session handling to a harness SDK.
- Orchestration mode: choose code-orchestrated, LLM-orchestrated, or mixed orchestration deliberately.
- Workflow versus agent: use deterministic workflows for known steps and autonomous agents for adaptive decisions.
- Context protocol: prefer MCP or typed connector boundaries when tools/context must be shared across apps or agents.
- Computer/browser control: treat as broad, slower, and higher risk; prefer APIs, MCP, shell, or browser-specific tools when available.
- Fast feedback loops: local typecheck, tests, build, smoke, and artifact validation should be cheap to run.
- Clear boundaries: separate app surface, harness, provider, tools, state, approvals, and observability.
- Lowest sufficient complexity: start with the simplest reliable harness before multi-agent orchestration.
- Governance by design: privileged tools need approvals, audit traces, and explicit safety classes.
- Observability: record tool calls, approvals, failures, latency, and final status when the app will run real workflows.
- Resumability: add durable stores only when runs must survive restarts, timeouts, or human approval delays.
- Scale patterns: dynamic agent selection, queues, distributed workers, caches, and cloud services are later-stage choices unless required by the brief.

## Required Output When Used

Add this section before implementation:

```markdown
## Industry Signals Applied
- Sources checked:
- Harness signals adopted:
- Signals adopted:
- Signals intentionally not adopted:
- Reason they fit this user brief:
```
