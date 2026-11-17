## Description:

Reviews recent agent edits to an LLM wiki, corrects or reverts problematic changes, promotes approved drafts, and sends the owner a concise digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexio](https://clawhub.ai/user/dexio)

### License/Terms of Use:

MIT-0

## Use Case:

Wiki maintainers and authorized agents use this skill to inspect changes against their diffs, fix or revert harmful edits, promote valid drafts, and report outstanding decisions to the wiki owner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Edits, reversions, or draft promotions may affect the wrong wiki or content.

Mitigation: Confirm the target wiki path and editing authority before use; inspect each diff and act on individual changes.

Risk: A secret removed from a page may remain exposed in its history.

Mitigation: Escalate the finding and rotate the affected credential after removing the visible value.

Risk: The review digest could be sent to the wrong recipient.

Mitigation: Confirm the wiki owner's channel before sending the digest.

## Reference(s):

- [Wiki Review (Dexio) skill listing](https://clawhub.ai/dexio/skills/dexio-wiki-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Short plain-text or Markdown review digest with suggested or executed wiki corrections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tracks the last reviewed change and unresolved items; may update or restore wiki pages when authorized.]

## Skill Version(s):

1.1.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
