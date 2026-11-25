## Description:

Connects backend code to Didit's passive liveness API to check a single selfie for liveness and spoofing, and interpret its score, status, and warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating selfie-based liveness checks use this skill to send a single selfie to Didit's API and handle the result, including decline, spoofing, duplicate-face, and blocklist warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a selfie and API key to Didit's external liveness service; saved requests store the image and enroll a face in the search index.

Mitigation: Use an API key with only the access needed, review Didit's data handling for your use case, and set save_api_request=false when storage and enrollment are not needed.

Risk: The security review is partial because some local references could not be resolved, and the skill does not declare its tool scope.

Mitigation: Review the complete skill and script behavior, and confirm the API key's permissions before deployment.

## Reference(s):

- [Didit Passive Liveness API Reference](https://docs.didit.me/standalone-apis/passive-liveness)
- [Didit Liveness Feature Guide](https://docs.didit.me/core-technology/liveness/overview)
- [Didit Documentation](https://docs.didit.me)

## Skill Output:

**Output Type(s):** [API calls, Code, Shell commands, Guidance]

**Output Format:** [Markdown documentation with Python and TypeScript examples and JSON response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes request and response examples, setup instructions, and result-handling guidance.]

## Skill Version(s):

1.4.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
