## Description:

Retrieve business listings and information in North America (via AJAX endpoint).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zheng108](https://clawhub.ai/user/zheng108)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve structured Dealmoon business listings for North American real estate, retail, and service searches.

### Deployment Geography for Use:

North America

## Known Risks and Mitigations:

Risk: The skill makes requests to Dealmoon for business-directory searches.

Mitigation: Install only if that network access is acceptable and review generated requests before execution.

Risk: Search parameters could expose private personal data, secrets, or unrelated sensitive information.

Mitigation: Limit inputs to business-directory search terms and exclude secrets or sensitive personal data.

## Reference(s):

- [Dealmoon business directory endpoint](https://www.dealmoon.com/local-category/updata?lang=cn)
- [ClawHub skill page](https://clawhub.ai/zheng108/skills/dealmoon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; avoid placing private personal data, secrets, or unrelated sensitive information into search parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
