## Description:

Searches for resources using Bing or Baidu, finds Baidu Netdisk share links, verifies access details, and saves or transfers selected files to a user's Baidu Netdisk account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nameefef](https://clawhub.ai/user/nameefef)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search for Baidu Netdisk resources, verify share links and extraction codes, and save chosen content into a Baidu Netdisk account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can browse third-party share links and may surface unknown or infringing resources.

Mitigation: Confirm each discovered resource before transfer and avoid unknown, suspicious, or infringing shares.

Risk: The skill can make persistent changes in a Baidu Netdisk account through bdpan commands or an authenticated browser session.

Mitigation: Use it only with an account session where the user accepts account changes, and verify file details, quota, and destination folder before saving.

## Reference(s):

- [Browser Automation Patterns for Baidu Netdisk](references/browser-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and transfer status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include discovered share links, extraction codes, file details, quota findings, destination folders, and success or failure status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
