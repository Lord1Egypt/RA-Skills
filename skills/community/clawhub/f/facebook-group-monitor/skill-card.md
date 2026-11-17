## Description:

Monitors Facebook groups for new posts, tracks previously seen posts, captures a stitched feed screenshot, and helps an agent summarize new items with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phuc-nt](https://clawhub.ai/user/phuc-nt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor Facebook group activity, detect new posts, and prepare concise reports that include post details, screenshots when available, and original links for verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an authenticated Facebook browser session locally.

Mitigation: Use a dedicated private workspace and delete .browser-data when the session is no longer needed.

Risk: Screenshots may contain Facebook group content.

Mitigation: Use a private screenshot directory, avoid shared folders, and delete screenshots when they are no longer needed.

Risk: Weak URL and file cleanup safeguards increase risk if untrusted users control inputs.

Mitigation: Pass only real Facebook group URLs or IDs from trusted users and avoid use on hosts where untrusted prompts can control the group URL or screenshot directory.

## Reference(s):

- [Setup Guide](references/SETUP.md)
- [ClawHub Skill Page](https://clawhub.ai/phuc-nt/skills/facebook-group-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON scrape output, JPEG feed screenshots, and Markdown-ready report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tracks seen posts locally and can save screenshots to a workspace-selected directory for later vision analysis.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
