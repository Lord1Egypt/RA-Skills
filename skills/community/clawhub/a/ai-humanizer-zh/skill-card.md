## Description:

This skill helps Chinese content teams diagnose AI-like writing patterns and produce more natural rewrites with notes on problematic passages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as Chinese marketers, operators, content creators, and product teams use this skill to turn AI-generated or draft Chinese text into more natural publishing-ready copy. It supports pasted text, uploaded text files, or public text links and can return AI-writing diagnostics, a naturalized rewrite, notes on problem passages, and next-step guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner can send the API key and submitted content to an environment-selected service endpoint.

Mitigation: Install only in trusted runner environments, keep AISKILLS_API_KEY secret, and pin AISKILLS_BASE_URL to the intended HTTPS service.

Risk: Submitted drafts may contain confidential, regulated, unpublished, or otherwise sensitive content.

Mitigation: Use the skill for sensitive material only after the provider's data handling has been approved for that content.

Risk: Implicit invocation may run the skill when a user did not explicitly request external processing.

Mitigation: Disable implicit invocation when explicit user approval is required before sending content to the provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allinherog-star/skills/ai-humanizer-zh)
- [Form schema](artifact/references/form-schema.json)
- [Skill metadata](artifact/references/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON result envelope containing Chinese prose suitable for Markdown rendering]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected result content includes summary, items, and artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
