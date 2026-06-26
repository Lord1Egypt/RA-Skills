## Description: <br>
Automatically converts long OpenClaw conversation logs into structured, topic-based Markdown memory cards with source pointers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mashirops](https://clawhub.ai/user/Mashirops) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to incrementally distill local session logs into long-term Markdown memory organized by topic. It is intended for environments where sending selected conversation content to Gemini and storing persistent local memory files is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private OpenClaw session logs and send conversation content to Gemini for summarization. <br>
Mitigation: Run it manually first, use a dedicated Gemini API key, and redact or exclude sensitive sessions before enabling scheduled automation. <br>
Risk: The skill stores distilled long-term memory in persistent local Markdown files. <br>
Mitigation: Review generated files in ~/.openclaw/workspace/memory/topics and confirm local file permissions and retention expectations before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mashirops/auto-memory-distiller) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown topic files, JSON cursor state, and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes new OpenClaw JSONL session lines incrementally and writes topic files under the local OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
