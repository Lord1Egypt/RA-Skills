## Description:

Baidupan helps agents manage Baidu Netdisk files through bypy, including upload, download, listing, syncing, authorization, and quota checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[libin771018-sketch](https://clawhub.ai/user/libin771018-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to authorize bypy and manage Baidu Netdisk files from an agent-assisted shell workflow, including listing, transferring, syncing, and checking quota.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorizing bypy grants access to the user's Baidu Netdisk account.

Mitigation: Install only when that account access is acceptable, complete authorization intentionally, and protect local bypy credentials such as files under ~/.bypy/.

Risk: Upload, download, sync, and --force operations can change local files or cloud files.

Mitigation: Review local and remote paths before execution, avoid --force unless replacement is intended, and use backups or a test path before bidirectional sync.

Risk: The skill depends on the third-party bypy package.

Mitigation: Pin or vet the bypy package before use in sensitive environments.

## Reference(s):

- [Baidupan ClawHub Release](https://clawhub.ai/libin771018-sketch/skills/baidupan)
- [bypy Project](https://github.com/houtianze/bypy)
- [Baidu Netdisk Open Platform](https://pan.baidu.com/union)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the bypy command-line tool and user authorization for Baidu Netdisk access.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
