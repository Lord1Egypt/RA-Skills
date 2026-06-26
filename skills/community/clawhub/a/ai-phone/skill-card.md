## Description: <br>
AI Phone lets Polly manage calls, screen unknown numbers, transcribe voicemails, and provide AI-enhanced phone support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhugelaing888](https://clawhub.ai/user/zhugelaing888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register and operate a PollyReach AI phone number for outbound calls, incoming call answering, voicemail transcription, call summaries, and answering-prompt updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place calls, answer calls, retrieve call artifacts, update answering prompts, check balance, and store a local bearer token. <br>
Mitigation: Install only when the user authorizes these actions, protect the token file with restrictive permissions, and review call activity before relying on results. <br>
Risk: The security evidence reports that inbound retrieval reads unread SMS messages and prints sender numbers and message contents while the skill presents it as incoming-call summary retrieval. <br>
Mitigation: Disclose SMS access before use, avoid scheduled inbound polling unless explicitly requested, and consider privacy or legal obligations for call and message handling. <br>
Risk: Call transcripts, recordings, phone numbers, account balances, and bearer tokens are sensitive data. <br>
Mitigation: Limit retention and sharing of call outputs, avoid exposing recordings or transcripts to unauthorized parties, and follow applicable consent requirements for calls and transcriptions. <br>


## Reference(s): <br>
- [AI Phone on ClawHub](https://clawhub.ai/zhugelaing888/ai-phone) <br>
- [PollyReach](https://pollyreach.ai) <br>
- [PollyReach Agent Dashboard](https://agent.pollyreach.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces call task identifiers, activation status, balance checks, inbound message summaries, call transcripts, recording/detail links, and prompt update status when PollyReach APIs return them.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
