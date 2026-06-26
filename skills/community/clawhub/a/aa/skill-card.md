## Description: <br>
Automatically drafts and, when configured, sends Gmail replies matching a client's tone, sign-off, templates, and reply rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azvast](https://clawhub.ai/user/azvast) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, assistants, or client-facing operators use this skill to draft professional Gmail replies on behalf of a client, using the client's preferred tone, sign-off, templates, and escalation rules. It can support semi-automated reply workflows, with review before sending by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require access to a Gmail account. <br>
Mitigation: Use the narrowest available Gmail permissions and keep credentials outside the skill in secure configuration. <br>
Risk: Auto-send settings could send replies without enough human review. <br>
Mitigation: Keep draft-review mode enabled by default and enable auto-send only for low-risk senders, labels, or templates with clear rules. <br>
Risk: Replies may use an inappropriate tone or make commitments outside the client's scope. <br>
Mitigation: Provide a client profile with tone, sign-off, escalation topics, and do-not-answer rules before drafting or sending replies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/azvast/aa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown email draft with optional template placeholders and sending guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-review mode is the default; auto-send should be limited to explicit rules for low-risk senders, labels, or templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
