## Description:

Content Forge helps Chinese content creators convert WeChat articles, Xiaoyuzhou podcasts, Zsxq posts, Caixin articles, and video links into Chinese-language podcasts, slide decks, mind maps, structured summaries, and deep-reading reports.

This skill is for research and development only.

## Publisher:

[sirkayzh](https://clawhub.ai/user/sirkayzh)

### License/Terms of Use:

MIT

## Use Case:

External users and content teams use this skill to turn Chinese articles, podcasts, paid-media excerpts, and video material into reusable reading notes, summaries, presentations, mind maps, and podcast-style scripts. The skill is especially tailored for workflows that save outputs to local files, Feishu, or IMA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paywall and cookie workflows can mishandle subscription credentials or access controls.

Mitigation: Review the paywall workflows before use; prefer user-provided text/files or official authorized exports; do not paste or export website cookies into chats, commands, or config files.

Risk: Dependency installation and browser automation scripts execute local shell or Node.js code.

Mitigation: Inspect scripts, pin and verify dependencies, and run prerequisite checks in a controlled environment before enabling automation.

Risk: Content sent to NotebookLM, Feishu, IMA, or GetNote may leave the local machine.

Mitigation: Use only content allowed for those services and route sensitive material to local LLM fallback or local file outputs when appropriate.

Risk: AI-generated summaries, podcasts, mind maps, and slide notes may imply more source coverage than actually occurred.

Mitigation: Keep the required source-completeness, warning, confidence, and AI-inference labels in every output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sirkayzh/skills/content-forge-chinese)
- [Installation Guide](references/installation-cn.md)
- [Tool Map](references/tool-map.md)
- [Honesty Rules](references/honesty-rules.md)
- [Paywall Strategies](references/paywall-strategies-cn.md)
- [China Network Configuration](references/china-network.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON metadata, Mermaid diagrams, slide decks, audio/transcript files, and shell command guidance depending on scenario.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to include source-completeness, warning, confidence, and AI-inference labels; configured workflows may save locally or send content to Feishu, IMA, NotebookLM, or GetNote.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
