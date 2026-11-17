## Description:

Create and maintain a privacy-respecting Cruit profile for an AI-native developer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwang783](https://clawhub.ai/user/nwang783)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers use this skill in supported coding agents to connect to Cruit, assemble a recruiter-searchable profile from approved project metadata and optional resume facts, publish only after review, and set up profile refreshes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote instructions can change the workflow after installation or approval.

Mitigation: Review the latest fetched instructions before use and enforce the documented fixed-host restriction plus non-overridable consent and privacy rules.

Risk: Remote installer use may execute unreviewed changes if run directly from a shell pipeline.

Mitigation: Prefer a marketplace-reviewed package, or download and inspect the installer before running it; install only into user-level skill folders.

Risk: The skill stores a local access token and can publish candidate profile data to cruit.dev.

Mitigation: Use browser device auth, never paste secrets, keep credential files user-only, inspect only approved folders, and publish only after the user approves the profile draft.

## Reference(s):

- [Cruit Candidate on ClawHub](https://clawhub.ai/nwang783/skills/cruit-candidate)
- [Cruit Candidate Instructions](https://cruit.dev/skills/candidate/INSTRUCTIONS.md)
- [Cruit](https://cruit.dev)
- [Security Notes](SECURITY.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API calls, Configuration, Shell commands]

**Output Format:** [Markdown guidance with API payload shapes, shell command snippets, and local JSON configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes approved profile data to cruit.dev and stores local credentials and refresh configuration under ~/.cruit during setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
