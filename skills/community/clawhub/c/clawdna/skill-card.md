## Description: <br>
Generate a public, privacy-safe persona/card/wiki lead from historical behavior when the user explicitly asks to run ClawDNA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buzuweidao](https://clawhub.ai/user/buzuweidao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate a concise, public, privacy-redacted profile from approved historical behavior after an explicit ClawDNA request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may analyze sensitive local OpenClaw history or memory files when a user approves local history access. <br>
Mitigation: Request explicit confirmation before local access, prefer curated user-provided exports or summaries, and keep analysis limited to the listed history and memory paths. <br>
Risk: A generated public profile could expose private details or unsupported claims if reviewed carelessly. <br>
Mitigation: Redact sensitive details by default, omit unsupported claims, avoid raw transcript excerpts, and review the Markdown profile before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buzuweidao/clawdna) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown display profile] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public privacy-safe profile only; no audit appendix or raw transcript excerpts.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
