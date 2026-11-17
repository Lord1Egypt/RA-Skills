## Description:

Fetch and parse news highlights from CCTV News Broadcast (Xinwen Lianbo) for a given date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwang-wh](https://clawhub.ai/user/williamwang-wh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve CCTV News Broadcast highlights for a requested date and have an agent summarize parsed titles and article content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can follow page URLs parsed from CCTV pages to unexpected network locations.

Mitigation: Run the skill in a sandboxed environment and require CCTV-domain URL allowlisting before routine use.

Risk: Outbound requests may hang or process unexpectedly large responses.

Mitigation: Use request timeouts, response-size limits, and bounded concurrency when operating the crawler.

Risk: Hardcoded request headers and cookies may be unnecessary, stale, or inappropriate for some environments.

Mitigation: Review and remove unnecessary hardcoded headers before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamwang-wh/skills/claw-cctv-news-fetcher)
- [CCTV Xinwen Lianbo day archive](https://tv.cctv.com/lm/xwlb/day/)
- [CNTV Xinwen Lianbo archive](https://cctv.cntv.cn/lm/xinwenlianbo/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [JSON from the crawler followed by a concise Markdown or text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js or Bun and node-html-parser; performs outbound HTTP requests to CCTV pages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
