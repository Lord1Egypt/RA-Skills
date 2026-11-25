## Description:

Read-only access to public Douyin data for keyword video and image-post search, creator lookup, post details and comments, and trending lists, with structured JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can collect public Douyin videos, creator profiles, post details, comments, and trending topics for content research, competitor monitoring, and sentiment analysis. The structured results can support topic and demand analysis or public lead research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send relevant Douyin links or IDs to the third-party Guaikei API.

Mitigation: Use only public content, and avoid submitting links or IDs you do not want sent to that service. Keep GUAIKEI_API_TOKEN private.

Risk: The security scan is only partially complete, and the tool misuse analyzer was degraded, so some behavior could not be fully assessed.

Mitigation: Review the skill files before installation and consider whether the documented third-party data handling is acceptable; the scan guidance identifies these inspection limits.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guaikei/skills/dy-voc)
- [Guaikei API service and token access](https://www.guaikei.com)
- [Output contract](references/contract.md)
- [CLI options](references/options.md)
- [Error handling](references/errors.md)
- [Demand mining guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON data, Analysis, Guidance]

**Output Format:** [Structured JSON envelopes with concise text analysis when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or later and GUAIKEI_API_TOKEN. Returned cost, when present, is an estimate.]

## Skill Version(s):

1.5.1 (source: release metadata, SKILL.md frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
