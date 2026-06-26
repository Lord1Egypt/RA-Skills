## Description: <br>
Proactively updates a concise rolling session summary so an agent can preserve key decisions, blockers, progress, and next steps while managing context size. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sabatech-dev](https://clawhub.ai/user/sabatech-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add rolling session summaries that preserve task progress, decisions, blockers, and next steps during long conversations or tool-heavy workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rolling summaries can preserve sensitive session details in SESSION-STATE.md if private inputs, secrets, or confidential decisions are summarized. <br>
Mitigation: Keep summaries concise, avoid recording secrets or unnecessary private details, and protect or remove SESSION-STATE.md according to the user's retention expectations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with a SESSION-STATE.md summary template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are intended to stay concise, with each section under 200 characters and the total rolling summary under 500 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
