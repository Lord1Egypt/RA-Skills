## Description: <br>
Search and analyze your own session logs (older/parent conversations) using jq. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect prior OpenClaw conversations, search historical session transcripts, and summarize message or cost details from local JSONL session logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local session logs may contain secrets, personal information, or private context from prior conversations. <br>
Mitigation: Use targeted dates, session IDs, and keywords, and avoid exposing unrelated transcript excerpts in responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1yihui/dalong-session-logs) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/1yihui) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local jq and rg binaries and access to the user's OpenClaw session log directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
