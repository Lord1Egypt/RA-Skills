## Description: <br>
Organizes meeting notes into review-ready action items, owner mappings, follow-up cadence, email drafts, next-sync agenda topics, and open questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team leads use this skill to turn meeting notes, participant roles, and priorities into structured follow-up material that can be reviewed before anything is sent or acted on. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags the local Python helper as including under-disclosed local audit and secret-scanning behavior outside the meeting follow-up purpose. <br>
Mitigation: Use the skill only on explicit meeting-note inputs, avoid broad folders or unrelated repositories, review drafts before sending, and prefer removing or separating the audit modes before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/follow-up-commander) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Structured Specification](resources/spec.json) <br>
- [Output Template](resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Structured Markdown by default, with optional JSON from the local helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review-ready drafts and can write generated output to a local file when run with an explicit output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
