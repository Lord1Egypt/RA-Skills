## Description:

Analyze a URL and download it with minimal steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgartlab](https://clawhub.ai/user/cgartlab)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can provide a URL to identify an appropriate download path and save supported files or platform media locally. Magnet and cloud-drive links are identified but not downloaded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preset proxies may be used without clear approval.

Mitigation: Remove unapproved built-in proxies and get explicit user approval before retrying through a proxy.

Risk: Saved logins may be used without clear approval.

Mitigation: Ask for explicit permission before using saved logins.

Risk: Filename protections are incomplete, and unsafe command argument handling may expose downloads to unintended paths or commands.

Mitigation: Correct filename validation and use safe command argument handling.

Risk: Persistent Windows proxy settings can affect other applications.

Mitigation: Use temporary proxy settings unless the user explicitly requests a persistent change.

## Reference(s):

- [CGArtLab Down on ClawHub](https://clawhub.ai/cgartlab/skills/cgartlab-down)
- [Tool Matrix and Selection Rules](artifact/references/tool-matrix.md)
- [Anti-Bot and Restricted Sites](artifact/references/anti-bot.md)
- [Usage Documentation](artifact/docs/USAGE.md)
- [yt-dlp Issue Tracker](https://github.com/yt-dlp/yt-dlp/issues)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [Downloaded files with concise natural-language status or limitation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads use a user- or environment-selected location; magnet and cloud-drive links receive guidance rather than downloads.]

## Skill Version(s):

0.2.0 (source: frontmatter, CHANGELOG, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
