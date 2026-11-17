## Description:

Auto Chatlog helps an agent persist important conversation context to daily Markdown memory files and reload recent memory before responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hahaerer](https://clawhub.ai/user/hahaerer)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users who want cross-session continuity use this skill to keep daily conversation notes, long-term preferences, task outcomes, configuration changes, and todos in Markdown memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic memory can persist sensitive or unwanted conversation details across sessions.

Mitigation: Install only when cross-session memory is intended, keep secrets out of MEMORY.md and daily files, and review stored memory regularly.

Risk: The artifact includes unsafe credential-storage guidance for long-term Markdown memory.

Mitigation: Remove or rewrite credential-storage instructions before use and store only non-sensitive references to credentials.

Risk: Scheduled execution can update memory files without interactive review.

Mitigation: Enable scheduled execution only when the command and workspace path are fixed, reviewed, and trusted.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown notes and concise text with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update MEMORY.md and memory/YYYY-MM-DD.md in the configured workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
