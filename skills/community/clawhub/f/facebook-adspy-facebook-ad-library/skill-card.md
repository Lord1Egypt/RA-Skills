## Description:

Research Facebook ad creatives and Meta Ad Library results using PipiAds adspy and ad library tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyanggod](https://clawhub.ai/user/fanyanggod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for focused Facebook ad research, including keyword, advertiser, region, product, creative, and Meta Ad Library lookups through PipiAds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a third-party MCP server globally through npm.

Mitigation: Install only after deciding that the pipiads-mcp-server package is trusted, and avoid elevated privileges during installation.

Risk: The MCP server receives a PipiAds API key.

Mitigation: Use a narrowly scoped, revocable API key where possible and rotate or revoke it if the environment is no longer trusted.

Risk: PipiAds API calls may consume account credits.

Mitigation: Use specific platform, region, advertiser, and keyword filters before broad searches, and monitor account credit usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanyanggod/skills/facebook-adspy-facebook-ad-library)
- [PipiAds product website](https://www.pipiads.com)
- [PipiAds account and API key management](https://www.pipispy.com/)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions]

**Output Format:** [Markdown guidance with tool and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a PipiAds API key and may consume account credits for search and detail requests.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
