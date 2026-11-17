## Description:

Provides real-time spoken announcements of AI activity with asynchronous playback, multi-platform audio support, local caching, and integration verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wililam](https://clawhub.ai/user/wililam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add spoken receive, task, completion, and error status announcements to an OpenClaw-style agent workflow. It is suited for local activity awareness when announcement text is intentionally concise and non-sensitive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-wide spoken status updates and persistent behavior edits may be broader than intended.

Mitigation: Enable the skill only for workflows that deliberately need spoken status updates, and review or remove any installed announcement rules, hooks, or startup checks that make announcements persistent.

Risk: Announcement text may be sent to an external TTS service.

Mitigation: Keep announcement messages generic and non-sensitive, or disable announcements for confidential prompts and tasks.

Risk: Local audio caching can retain generated speech files derived from announcement text.

Mitigation: Avoid sensitive announcement text and periodically review, limit, or clear the local audio cache.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wililam/skills/beep-skills)
- [Publisher profile](https://clawhub.ai/user/wililam)
- [Package repository link from artifact metadata](https://github.com/wililam/beep-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime output is spoken audio plus CLI/status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration and cached audio files under user home directories.]

## Skill Version(s):

2.2.1 (source: server release metadata; artifact files report 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
