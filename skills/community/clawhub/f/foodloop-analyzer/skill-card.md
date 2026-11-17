## Description:

Reverse-engineer and analyze any FoodLoop AI deployment when given a FoodLoop AI URL to analyze, audit, trace, map, or inspect its workflow, API, or architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justhackr](https://clawhub.ai/user/justhackr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to map FoodLoop AI frontend and backend behavior, inspect FastAPI endpoints, trace user workflows, and summarize findings from a target deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prompt an agent to make live requests against FoodLoop deployments, including endpoints that upload photos, create demo users, mutate preferences or sessions, trigger webhooks, or generate PDFs.

Mitigation: Confirm authorization for the exact target before use, approve the backend destination, and require manual approval for write actions.

Risk: Photo analysis workflows can involve sensitive images or personal data.

Mitigation: Avoid uploading sensitive photos or personal data unless the user explicitly authorizes the upload and understands the destination service.

Risk: The workflow can leave local analysis files or temporary upload files behind.

Mitigation: Use non-sensitive test data and remove temporary files and generated reports when they are no longer needed.

## Reference(s):

- [FoodLoop AI Full API Workflow Reference](references/api_workflow.md)
- [FoodLoop live backend](https://foodrecycler.onrender.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with endpoint tables, API request examples, JSON excerpts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live API observations, schema summaries, architecture notes, and local report file paths.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
