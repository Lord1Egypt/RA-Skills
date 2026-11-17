## Description:

Provides local LLM inventory, model policy and provenance checks, prompt scanning, and opt-in guarded generation for Ollama, llama.cpp, LM Studio, and single-node vLLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to inspect and govern local LLM runtimes, check model policy and provenance, scan prompts for sensitive content, and review guarded usage. It is intended for single-endpoint local models rather than multi-node inference clusters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence, citing model-changing capabilities beyond its stated audit purpose and write operations without a tool-level approval gate; intent is not established.

Mitigation: Run with an account or runtime that cannot modify the model store, or limit the agent to scan and observe tools. Use the CLI dry run and double confirmation before removing a model.

Risk: The security scan is partial because three local references could not be resolved.

Mitigation: Review the skill source and configuration before installation; treat the scan as incomplete rather than conclusive.

Risk: Prompt scanning uses heuristic patterns, so a no-match result does not establish that a prompt is safe.

Mitigation: Interpret no-match as no known pattern matched and review prompt content in context before sending it.

## Reference(s):

- [Capabilities](artifact/references/capabilities.md)
- [Setup and security guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Project homepage](https://github.com/AIops-tools/AI-Guardian)
- [ClawHub release page](https://clawhub.ai/zw008/skills/ai-guardian)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Structured tool results with concise text or Markdown summaries and shell or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Route-through usage records prompt length and redacted findings rather than raw prompt text.]

## Skill Version(s):

0.14.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
