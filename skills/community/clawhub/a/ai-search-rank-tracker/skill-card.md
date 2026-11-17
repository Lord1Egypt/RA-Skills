## Description:

Estimates AI search visibility for a brand across prompt sets and produces reports with mention, rank, competitor, sentiment, and visibility score data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketing teams, founders, agencies, and developers use this skill to run prompt-set visibility checks for a company, product, or domain and generate simple brand monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may be misleading if simulated AI-engine responses are treated as actual ChatGPT, Claude, Gemini, or Perplexity rankings.

Mitigation: Treat reports as estimates unless the implementation is changed to query those services directly or labels results as simulations.

Risk: Path-handling bugs can read or write outside intended folders.

Mitigation: Restrict promptPack values to bundled pack names and review generated report paths before running the skill.

Risk: Prompts, brand strategy, or related inputs may be sent to configured AI backends.

Mitigation: Avoid confidential prompts or brand strategy, and use scoped API keys through reviewed environment configuration.

Risk: CSV exports may be unsafe to open without review.

Mitigation: Open generated CSV exports cautiously and inspect content before importing them into spreadsheet tools.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/x-rayluan/skills/ai-search-rank-tracker)
- [README.md](artifact/README.md)
- [Prompt Database README](artifact/prompt-db/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, csv, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with shell commands and generated report files in JSON, Markdown, and CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should be reviewed as visibility estimates, especially when generated from simulated assistant responses.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
