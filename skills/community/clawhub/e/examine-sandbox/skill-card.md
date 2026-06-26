## Description: <br>
Use this skill when the user wants to check what data their shared agent can access, inspect what's being shared, review privacy, or see what guests will see. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who manage shared agent links use this skill to audit exposed data, visitor activity, and share-link permissions before or after sending a link. It helps identify sensitive content in shared scope and propose scoped downgrade or revoke actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to change or revoke live share links. <br>
Mitigation: Use read-only reporting by default and require explicit approval for the exact linkId, action, and expected impact before PATCH or DELETE requests. <br>
Risk: The skill requires PULSE_API_KEY access to account-sharing data. <br>
Mitigation: Install only when the agent is trusted with that credential and account data, and keep the credential out of shared outputs. <br>
Risk: Sensitive note-search results may expose private or confidential content during an audit. <br>
Mitigation: Report minimal findings, avoid reproducing secrets or unnecessary personal data, and focus recommendations on narrowing or revoking access. <br>


## Reference(s): <br>
- [Examine Sandbox API Reference](artifact/reference/API.md) <br>
- [Audit Link Example](artifact/examples/audit-link.md) <br>
- [ClawHub skill page](https://clawhub.ai/xisen-w/examine-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with API call summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive audit findings from account data; should summarize only what is needed for the user's review.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
