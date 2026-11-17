## Description:

Claude Sonnet 4 Lite Agent guides an agent through efficient content creation workflows with strict limits on retries, search use, and final submission timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teamolab](https://clawhub.ai/user/teamolab)

### License/Terms of Use:


## Use Case:

External users and content creators use this skill to configure an agent for fast content drafting, structured planning, limited follow-up search, and document, presentation, webpage, or attachment generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts to redefine the host agent's role and impose broad workflow, search, tool-use, and file-generation rules.

Mitigation: Review and narrow the skill before installation so host identity, verification behavior, search policy, clarification choices, and file-generation safeguards remain controlled by the host agent.

Risk: Strict two-attempt failure handling and one-search limits may cause incomplete verification or premature continuation after blocked subtasks.

Mitigation: Require higher-priority verification and completion policies to override these limits for tasks where accuracy, safety, or user requirements demand additional checks.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with workflow and tool-use instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct creation of documents, presentations, webpages, or other file attachments depending on the task.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
