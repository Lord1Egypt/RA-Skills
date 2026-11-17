# Optional feedback handoff

This skill does not collect telemetry. After a run, the agent may ask:

> Would you like to tell the maintainer what changed? Nothing is sent automatically; you choose whether to share a redacted result.

If the user says yes, prepare this draft and let them review it. Do not submit it automatically.

## Copyable result report

```markdown
## AI Coding Token Optimizer result

- Host: <Claude Code / Codex / another agent>
- Project type: <brief category, no project name or URL>
- Entry point measured: <CLAUDE.md / AGENTS.md / other>
- Before: <bytes> (~<tokens> tokens)
- After: <bytes> (~<tokens> tokens)
- Reduction: <bytes> (<percentage>%)
- Maps or routers created/refreshed: <short list, generic names only>
- Validation: <no-loss / links / anchors / tests>
- Practical result: <what became easier or faster>
- What should improve: <optional>
```

## Redaction checklist

Before sharing, remove:

- source code, instruction text and file contents
- secrets, tokens, credentials and environment values
- private or machine-specific paths
- repository URLs, company names, customer names and project identifiers
- screenshots or logs containing any of the above

Byte counts and approximate tokens are useful without revealing the project. The estimate uses bytes ÷ 4 and is directional; actual tokenization varies by model and tokenizer.

## Where to share

The user chooses one channel:

- [GitHub feedback issue](https://github.com/Asif2BD/AI-Coding-Token-Optimizer/issues/new?template=feedback.md)
- the skill's [ProSkills page](https://proskills.md/skills/coding/ai-coding-token-optimizer) review/rating
- the skill's [ClawHub page](https://clawhub.ai/asif2bd/ai-coding-token-optimizer) review/star

Feedback is voluntary. A skipped report is valid, and self-reported examples are not a representative benchmark.
