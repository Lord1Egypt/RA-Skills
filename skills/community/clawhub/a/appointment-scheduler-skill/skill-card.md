## Description: <br>
Schedule appointments with doctors, salons, mechanics, or any service provider. Polly calls, finds available times, and books it for you. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhugelaing888](https://clawhub.ai/user/zhugelaing888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to schedule service appointments by phone through PollyReach. It also supports related outbound calls, inbound call answering, call summaries, transcripts, recordings, and credit-balance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is framed as an appointment scheduler but security evidence says it enables broader outbound calling, automatic inbound answering, and transcript or recording exposure. <br>
Mitigation: Use it only when a broad PollyReach phone agent is intended, keep call prompts narrowly scoped, and review call summaries, transcripts, and recording links before relying on results. <br>
Risk: The skill stores a local PollyReach token and sends call tasks, call content, transcripts, and related call details to PollyReach. <br>
Mitigation: Protect the token file, revoke or rotate the token when access changes, and review PollyReach data retention, caller notice, and recording-consent controls before sensitive use. <br>
Risk: Phone calls can consume paid credits and may involve business, medical, legal, or other sensitive communications. <br>
Mitigation: Confirm billing and top-up expectations before use, monitor credit balance, and escalate sensitive or unauthorized decisions to the human. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhugelaing888/appointment-scheduler-skill) <br>
- [PollyReach](https://pollyreach.ai) <br>
- [PollyReach agent dashboard](https://agent.pollyreach.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl, jq, and bc; reads and writes the local PollyReach token file at ~/.config/PollyReach/key.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
