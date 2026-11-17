## Description:

Discover which AI prompts and topics matter for a brand's Answer Engine Optimization using free tools, site crawling, web search, and LLM reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

Marketing, content, and growth teams use this skill to research conversational AI prompts for a brand, prioritize AEO opportunities, audit existing coverage, and identify content gaps without paid APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional shell crawler can be directed at internal or private network targets without safeguards.

Mitigation: Prefer web_fetch for public pages, and only run the shell crawler for intentionally trusted domains after adding public-host validation or network egress controls.

## Reference(s):

- [AEO Prompt Research Methodology](references/aeo-methodology.md)
- [ClawHub skill page](https://clawhub.ai/psyduckler/skills/aeo-prompt-research-free)
- [Publisher profile](https://clawhub.ai/user/psyduckler)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with prioritized prompts, coverage ratings, content gap analysis, and recommended next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional shell crawler output when the user intentionally runs the bundled crawl script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
