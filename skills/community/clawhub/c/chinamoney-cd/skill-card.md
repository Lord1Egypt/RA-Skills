## Description:

Queries ChinaMoney interbank certificate-of-deposit issuance information for bank institutions with exact bank matching and structured results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avalon-996](https://clawhub.ai/user/avalon-996)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agent users can query public ChinaMoney pending interbank certificate-of-deposit issuance by bank name or abbreviation. The skill returns structured issuance details and saves a local screenshot for review or recordkeeping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each query launches Chromium and accesses ChinaMoney over the network.

Mitigation: Run the skill only in environments where ChinaMoney access is permitted and validate results against the live source when decisions depend on freshness.

Risk: Saved screenshots in the system temp directory may contain bank search terms and issuance results.

Mitigation: Clean up cd_result_[bank].png files after use and restrict temp directory access in sensitive environments.

Risk: Unpinned browser automation dependencies can change runtime behavior in controlled deployments.

Mitigation: Pin and test Playwright and Chromium versions before deploying the skill in production workflows.

## Reference(s):

- [Server-resolved source repository](https://github.com/avalon-996/chinamoney-cd)
- [ChinaMoney interbank certificate-of-deposit issuance page](https://www.chinamoney.com.cn/chinese/tycdfxxx/)
- [ClawHub skill page](https://clawhub.ai/avalon-996/skills/chinamoney-cd)
- [Publisher profile](https://clawhub.ai/user/avalon-996)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text query results with a saved PNG screenshot file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on live ChinaMoney availability and are filtered by the requested bank name or abbreviation.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter version 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
