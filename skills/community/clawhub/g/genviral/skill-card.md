## Description: <br>
Complete genviral Partner API automation. Create and schedule posts (video + slideshow) across TikTok, Instagram, and any supported platform. Includes slideshow generation, file uploads, template/pack management, analytics, and full content pipeline automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugenesys](https://clawhub.ai/user/ugenesys) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to manage Genviral Partner API workflows for generating slideshows or videos, scheduling posts, tracking analytics, and iterating social-media content strategy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The self-updater can replace reviewed skill-owned files from GitHub. <br>
Mitigation: Disable the updater or run it only in dry-run mode until a human reviews the diff before applying changes. <br>
Risk: Cron examples can schedule unattended generation, posting, analytics checks, and self-updates for connected accounts. <br>
Mitigation: Avoid unattended posting until account targets, content quality gates, posting cadence, and privacy settings are verified. <br>
Risk: GENVIRAL_API_KEY and any GitHub token used for updates are sensitive credentials. <br>
Mitigation: Store credentials in approved secret handling, avoid printing them in logs, and rotate them if exposed. <br>
Risk: The skill can create, schedule, update, and delete social-media content and related Genviral resources. <br>
Mitigation: Use a Genviral account the user intends to let an agent manage, keep dashboard review enabled, and confirm destructive actions before execution. <br>


## Reference(s): <br>
- [ClawHub Genviral skill page](https://clawhub.ai/ugenesys/genviral) <br>
- [Genviral](https://genviral.io) <br>
- [Genviral Partner API docs](https://docs.genviral.io) <br>
- [Genviral skill homepage](https://github.com/fdarkaou/genviral-skill) <br>
- [Analytics feedback loop](docs/references/analytics-loop.md) <br>
- [Competitor research guide](docs/references/competitor-research.md) <br>
- [Setup guide](docs/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON workspace records, configuration values, and Genviral API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, a Genviral account with Partner API access, and GENVIRAL_API_KEY for authenticated API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
