## Description: <br>
Use CareerMax when the user wants to review their career context, manage their job pipeline, improve career materials, prepare for interviews, find referrals, or build skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rahulphenomenon](https://clawhub.ai/user/rahulphenomenon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to their CareerMax account for career profile review, job pipeline management, resume and cover letter assistance, interview preparation, referrals, LinkedIn feedback, and learning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a CareerMax API key that can access the user's connected CareerMax account. <br>
Mitigation: Use a dedicated CareerMax agent key, store CAREERMAX_API_KEY only in secure environment storage, and never expose, repeat, or log the key. <br>
Risk: Some workflows can create or update lasting CareerMax records or consume CareerMax credits. <br>
Mitigation: Confirm durable record changes before repeating tokenized requests, and show credit costs or balances when the user asks or when insufficient credits block an action. <br>


## Reference(s): <br>
- [CareerMax AI Agent](https://careermax.ai/ai-agent) <br>
- [CareerMax on ClawHub](https://clawhub.ai/rahulphenomenon/careermax) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline tool names, setup commands, and configuration values.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CAREERMAX_API_KEY and the CareerMax MCP toolkit; durable CareerMax record changes require user confirmation.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
