## Description:

deeply helps an agent retrieve sourced first-person viewpoints from selected interviews, articles, podcast transcripts, and research reports for judgment-oriented questions in finance, technology, business, and ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[komako-workshop](https://clawhub.ai/user/komako-workshop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to support research, analysis, and decision-making by retrieving dated, sourced quotes from named people before composing an answer. It is intended for judgment and opinion discovery, not live news, current prices, health, mystical, or relationship advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relevant research questions may be sent to a third-party API.

Mitigation: Use only when the user accepts that query content will be submitted to Deeply, and avoid sending confidential or sensitive questions.

Risk: Token-bearing installation commands can expose credentials if pasted into chat or logs.

Mitigation: Configure DEEPLY_TOKEN through a trusted local secret or environment mechanism, and review commands from the website before running them.

Risk: The corpus is not live and can miss current prices, breaking news, or out-of-scope domains.

Mitigation: Use the skill for sourced historical viewpoints, and use separate current sources for live facts or unsupported domains.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/komako-workshop/skills/deeply)
- [deeply website](https://deeply.dev)
- [Deeply evidence search API](https://api.deeply.dev/v2/evidence/search)
- [Deeply unit retrieval API](https://api.deeply.dev/api/unit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ranked evidence items that can include author, biography, publication date, title, source URL, claim, quote, coverage status, and unit identifiers.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
