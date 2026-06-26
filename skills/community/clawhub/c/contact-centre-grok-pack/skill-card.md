## Description: <br>
Triage call-centre and voice support transcripts into summaries, sentiment, urgency, routing queues, and follow-up actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Contact-centre teams, support operators, clinics, councils, and SMEs use this skill to turn transcripts or voice-agent notes into a JSON triage package for review and downstream routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input transcripts and JSON output may contain sensitive customer, health, housing, or support data. <br>
Mitigation: Process only transcripts the user is allowed to handle, avoid saving JSON output unless needed, and store saved results as sensitive operational data. <br>
Risk: Heuristic routing or urgency labels may be incomplete or incorrect for live CRM, helpdesk, clinic, or council workflows. <br>
Mitigation: Keep the documented human review step before routing results into live systems. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON triage output with optional saved file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes summary, sentiment, urgency, route, actions, and evidence fields; human review is expected before live routing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
