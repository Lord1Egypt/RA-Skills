## Description: <br>
Hourly X engagement loop for an X account, with interactive human approval and scheduled auto-posting under configurable safety filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rabgpt](https://clawhub.ai/user/rabgpt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and operators use this skill to draft, approve, post, repost, and summarize X engagement activity for a configured account. It is intended for accounts whose owners intentionally allow an agent to use an existing logged-in X browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public posts or reposts from a logged-in X account. <br>
Mitigation: Install only for accounts where that behavior is intended, start in interactive mode, and keep scheduled mode disabled until the configuration and caps are reviewed. <br>
Risk: Scheduled reposts can amplify content as an endorsement. <br>
Mitigation: Use a small repost allowlist, low daily caps, and conservative topic and banned-phrase filters. <br>
Risk: Persisting configuration globally can make the behavior available in future projects. <br>
Mitigation: Write configuration to a global CLAUDE.md only when that scope is intentional; otherwise keep it project-local or session-only. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rabgpt/boost-x-engagement) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, configuration, guidance] <br>
**Output Format:** [Markdown guidance with a structured JSON run summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce public X posts and reposts through the user's logged-in browser session when approved or when scheduled-mode filters pass.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
