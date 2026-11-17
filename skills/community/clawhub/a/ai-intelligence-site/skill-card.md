## Description:

Automates creation, daily refresh, traffic-tier analysis, and GitHub Pages deployment for AI intelligence and competitor-analysis sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[griffithkk3-del](https://clawhub.ai/user/griffithkk3-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to maintain AI competitor intelligence pages by discovering sites, refreshing traffic data, organizing tiers and trends, and publishing updates to GitHub Pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an embedded Serper API key, which can expose credentials if reused.

Mitigation: Remove and rotate the embedded key, and require SERPER_API_KEY from a protected secret store.

Risk: The release evidence reports automatic GitHub publishing with broad local change capture.

Mitigation: Run only in a dedicated repository with limited Git credentials, add a dry-run or confirmation step before publishing, and replace broad Git adds with an allowlist of generated data files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/griffithkk3-del/skills/ai-intelligence-site)
- [Serper Search API Endpoint](https://google.serper.dev/search)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces competitor records, traffic tiers, trend arrays, insights, and deployment guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
