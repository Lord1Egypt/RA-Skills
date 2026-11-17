## Description:

Guides an agent through exporting and analyzing full chat histories from the Gemini and ChatGPT web products, including ChatGPT JSON exports and Gemini HTML exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaoqing404](https://clawhub.ai/user/shaoqing404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to help users retrieve ChatGPT or Gemini web chat exports, inspect their file formats, and run practical searches, timeline summaries, and cross-platform analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles complete ChatGPT and Gemini exports that can contain sensitive private chat and account data.

Mitigation: Use a private working directory with owner-only permissions, redact sensitive records before sharing reports, and delete intermediate files after analysis.

Risk: The documented examples include fixed temporary-file paths that can expose sensitive analysis artifacts.

Mitigation: Avoid fixed /tmp paths for real exports and use private, per-user temporary directories or explicit secure output locations.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/shaoqing404/ai-chat-timeline-skills/tree/main/skills/gemini-openai-chat-export-analyze)
- [ClawHub skill page](https://clawhub.ai/shaoqing404/skills/gemini-openai-chat-export-analyze)
- [Google Account data and privacy](https://myaccount.google.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code]

**Output Format:** [Markdown with inline bash, jq, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local intermediate text or JSONL analysis files when the user supplies export paths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
