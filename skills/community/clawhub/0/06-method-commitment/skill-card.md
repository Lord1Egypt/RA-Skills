## Description: <br>
Use when the user has a selected Candidate Method, multiple Candidate Methods to merge, a user-authored rough method, or a reconstructed chat method and wants to converge on one human-owned method outcome before experiment design, research framing, or risk review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snake-fan](https://clawhub.ai/user/snake-fan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and research-writing agents use this skill to converge from a selected, merged, rough, or chat-reconstructed method into one status-labeled method outcome before experiment design, research framing, or risk review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create or update local method-commitment markdown files. <br>
Mitigation: Review generated artifacts before relying on them or routing them into downstream research workflows. <br>
Risk: A method may be treated as downstream-ready before the researcher has explicitly committed to it. <br>
Mitigation: Require explicit researcher confirmation before assigning the committed status; otherwise use a non-committed status with clear routing warnings. <br>
Risk: Referenced template files are not included in the artifact. <br>
Mitigation: Reconstruct template structure from the main instructions when needed and preserve existing user edits when resuming a workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snake-fan/skills/06-method-commitment) <br>
- [Server-resolved GitHub provenance](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/06-method-commitment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown files and concise conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates method-commitment artifacts under a workspace path; committed outputs require explicit researcher confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
