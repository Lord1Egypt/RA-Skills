## Description:

Open browser and search for keywords. Use when user wants to search online.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sldjs](https://clawhub.ai/user/sldjs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to open Baidu search results for a provided query in the local default browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search text is sent to Baidu and may disclose the exact query outside the local environment.

Mitigation: Do not use the skill for confidential queries unless that disclosure is acceptable.

Risk: The skill opens the local default browser as part of execution.

Mitigation: Install and run it only in environments where browser launches are expected and permitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sldjs/skills/baidu-search-sldjs)
- [Publisher profile](https://clawhub.ai/user/sldjs)
- [Baidu search endpoint](https://www.baidu.com/s)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text status message after opening a browser search URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Opens the default browser and sends the user-provided query to Baidu.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
