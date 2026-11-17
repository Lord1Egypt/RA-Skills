## Description:

All-in-one Skill fuer GeeLark: Setup, lokale API, nativer Sync-Transport, UI/RPA-Fallback, Posting-Flow, Verifikation und Troubleshooting in einem durchgaengigen Runbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagebabe](https://clawhub.ai/user/pagebabe)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to set up, diagnose, and operate GeeLark workflows through local API checks, native sync commands, UI fallback, posting preparation, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to operate GeeLark locally through APIs and UI automation, including workflows that may affect browser profiles or external accounts.

Mitigation: Review actions before browser, profile, or posting workflows and require explicit confirmation before any externally visible account action.

Risk: The skill references GEELARK_API_KEY for local API access.

Mitigation: Keep the key private and avoid saving secrets in memory, logs, or troubleshooting notes.

Risk: Automation can report success without the intended GeeLark state being reached.

Mitigation: Follow the skill's required dual verification: confirm the foreground app or window and confirm the target content such as URL, session ID, or API response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pagebabe/skills/geelark-complete)
- [Publisher profile](https://clawhub.ai/user/pagebabe)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verification and troubleshooting steps for local GeeLark workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
