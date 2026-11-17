## Description:

Chinese-language file organizer that classifies local files into type-based folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to organize files in Desktop, Downloads, Documents, or a supplied Windows path into folders by file type, and to report file counts and sizes on request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move many local files as soon as broad Chinese trigger words are invoked with Desktop, Downloads, Documents, or a supplied Windows path.

Mitigation: Use it first on a small test folder and require the agent to confirm the exact target directory and planned moves before execution.

Risk: The evidence reports no preview, confirmation, or undo path before organization occurs.

Mitigation: Avoid broad requests on important folders unless the files are backed up or the target directory is disposable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyingzhuangk/skills/file-organizer-zh-1-0-0)
- [Publisher profile](https://clawhub.ai/user/zhangyingzhuangk)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text messages in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also move files into type-based folders in the target directory when invoked.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
