## Description:

Crawl any website and get a 0-100 SEO score with 50+ checks across Technical, On-Page, Schema, Social, and Compliance categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, site operators, and agent workflows use this skill to audit public web pages for SEO issues, industry-specific compliance signals, competitor gaps, and prioritized fixes. With an Anthropic API key, it can also generate SEO article drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to URLs supplied in prompts.

Mitigation: Run it with network egress controls and avoid internal, localhost, staging, cloud metadata, or credential-bearing URLs.

Risk: Article generation sends the requested topic to Anthropic.

Mitigation: Do not submit sensitive, confidential, or regulated content as article topics unless that use is approved for the configured Anthropic account.

Risk: The advertised crawl, 50+ check, and AI-analysis claims may be overstated.

Mitigation: Treat results as heuristic SEO guidance and review important compliance or business decisions before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drivenautoplex1/skills/dfw-seo-audit)
- [OpenClaw skills homepage](https://github.com/drivenautoplex1/openclaw-skills)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, guidance]

**Output Format:** [Plain text or JSON audit reports, Markdown article drafts, and optional output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Demo mode uses a static sample; compliance-only mode fetches a supplied URL without AI analysis; article generation requires ANTHROPIC_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
