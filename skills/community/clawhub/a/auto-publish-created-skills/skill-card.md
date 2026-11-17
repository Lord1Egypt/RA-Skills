## Description:

Automatically publishes reviewed and committed local skills to ClawHub when a user has explicitly requested ongoing publication for assistant-created skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g-hanasq](https://clawhub.ai/user/g-hanasq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to publish newly created, reviewed, and committed local skills to ClawHub through the verified publish flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish using an authenticated ClawHub session.

Mitigation: Only install or invoke it when you want assistant-created skills published to ClawHub, and confirm the target skill has been reviewed and committed before allowing publication.

Risk: A draft or incomplete skill could be published if review gates are skipped.

Mitigation: Require explicit user intent, a valid SKILL.md, a local review, a successful commit, and post-publish verification before treating publication as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g-hanasq/skills/auto-publish-created-skills)
- [ClawHub publisher profile](https://clawhub.ai/user/g-hanasq)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown status report with command results and release details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes skill name, version, publish result, final URL, and verification status when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
