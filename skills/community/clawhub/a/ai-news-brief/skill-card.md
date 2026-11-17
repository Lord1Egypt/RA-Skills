## Description:

Ai News Brief gathers AI, compute, large-model, GPU, memory, and policy news from configured sources and generates concise briefings with optional PDF and email delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[17oko](https://clawhub.ai/user/17oko)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect AI, compute, GPU, large-model, memory, and policy news from multiple media and government sources, then generate a brief report for reading or sharing. Optional configuration enables PDF generation, LLM-assisted summaries, translation hooks, and email delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include untrusted article content and links.

Mitigation: Review generated Markdown, HTML, and PDF reports before opening, sharing, or forwarding them, especially when content comes from unfamiliar sources.

Risk: Optional email and LLM features can send generated reports, article text, recipient addresses, and configured credentials through third-party providers.

Mitigation: Keep email and LLM features disabled unless those providers are approved for the intended data, and store credentials only in user-controlled configuration.

Risk: The skill fetches external websites and uses local Chrome automation, which can be brittle or unsuitable for unattended use.

Mitigation: Run it in an isolated, pinned Python environment and review behavior before enabling scheduled or unattended execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/17oko/skills/ai-news-brief)
- [Publisher profile](https://clawhub.ai/user/17oko)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown briefing with optional HTML and PDF report files; configuration guidance may include shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use local Chrome automation, configured news sources, optional LLM summarization, optional translation, optional PDF generation, and optional SMTP email delivery.]

## Skill Version(s):

1.5.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
