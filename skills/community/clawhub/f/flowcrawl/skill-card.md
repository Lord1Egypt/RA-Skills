## Description:

FlowCrawl is a local CLI skill for extracting website content as markdown, text, or JSON using a three-tier fetch cascade that can escalate from plain HTTP to browser-based fetching when blocked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windseeker1111](https://clawhub.ai/user/windseeker1111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to collect clean page content from authorized websites for AI knowledge bases, research workflows, and data pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to escalate to stealth and browser-based fetching when a site blocks ordinary requests.

Mitigation: Install and run it only for sites you own or are explicitly authorized to test, and respect site terms, robots.txt, and rate limits.

Risk: Crawling can collect sensitive page content and write local markdown, text, or combined output files.

Mitigation: Use a controlled output directory, review collected content before sharing it, and delete unneeded crawl output.

Risk: The runtime depends on Scrapling and browser-backed fetching behavior.

Mitigation: Run in an isolated environment and pin dependencies before operational use.

## Reference(s):

- [ClawHub FlowCrawl release](https://clawhub.ai/windseeker1111/skills/flowcrawl)
- [Scrapling](https://github.com/D4Vinci/Scrapling)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance]

**Output Format:** [Markdown, plain text, or JSON; deep crawls can write per-page files and a combined markdown file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deep crawls default to depth 3 and 50 pages, with local output under ./flowcrawl-output unless overridden.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
