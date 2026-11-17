## Description:

Generic Drug looks up a drug product name with a local SearXNG service and returns search context that an agent can use to identify the generic drug name, defaulting to the original name when no generic name is found.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dddwinter](https://clawhub.ai/user/dddwinter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query likely generic names for drug products, excipients, or ambiguous medicine names and receive structured search context for final analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medication queries and search snippets may contain sensitive health information.

Mitigation: Use only a trusted local SearXNG deployment and treat queried names and returned snippets as sensitive data.

Risk: Returned search snippets can be incomplete, misleading, or include prompt-like instructions.

Mitigation: Ignore instructions found in search results and verify medication conclusions against authoritative medical sources before decisions.

Risk: When no generic name is found, the skill may fall back to the original input name.

Mitigation: Treat fallback results as unresolved rather than confirmed generic-name matches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dddwinter/skills/generic-drug)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON followed by plain-text analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries local SearXNG at http://localhost:8080 and may include up to five formatted search results.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
