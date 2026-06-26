## Description: <br>
Security advisory feed package for OpenClaw-related threats and vulnerabilities. The upstream feed is updated daily; local automation is handled by clawsec-suite or the operator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Developers and operators use this skill to add an agent-readable security advisory feed, inspect current advisories, and cross-reference affected skills or plugins. Standalone automation remains the responsibility of clawsec-suite or the operator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quick latest-release curl path can skip the stronger signed and pinned verification workflow. <br>
Mitigation: Use the documented signed release manifest, public-key fingerprint, and checksum verification steps before installing on production hosts. <br>
Risk: The advisory feed includes broader agent-security records and should not be treated as OpenClaw-only data. <br>
Mitigation: Scope notifications and filtering to the operator's installed tools, and present feed matches as advisory signals for review. <br>
Risk: Standalone installation does not create recurring polling or local enforcement. <br>
Mitigation: Run clawsec-suite or an operator-managed scheduler when automated monitoring or host-side enforcement is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-feed) <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>
- [Prompt Security](https://prompt.security) <br>
- [ClawSec feed releases](https://api.github.com/repos/prompt-security/ClawSec/releases?skill=clawsec-feed) <br>
- [Default advisory feed](https://raw.githubusercontent.com/prompt-security/ClawSec/main/advisories/feed.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON feed examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory review guidance and local installation or feed-check commands; standalone use does not create scheduled automation.] <br>

## Skill Version(s): <br>
0.0.11 (source: frontmatter and changelog, released 2026-06-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
