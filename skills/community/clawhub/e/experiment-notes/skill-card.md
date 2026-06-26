## Description: <br>
Track, search, and learn from experiments. Automatic logging of trial-and-error, success/failure patterns, and distilled lessons. Prevents repeating mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[besty0121](https://clawhub.ai/user/besty0121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to keep local experiment history, search prior attempts, and distill lessons so repeated tasks can benefit from earlier successes and failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Experiment notes may contain secrets, private keys, session cookies, proprietary prompts, or sensitive error traces if users log them directly. <br>
Mitigation: Do not record sensitive values; periodically review or delete files under ~/.openclaw/memory/experiments when notes are no longer needed. <br>
Risk: The skill stores user- or agent-provided experiment history persistently on local disk. <br>
Mitigation: Install only when local persistent experiment memory is desired, and manage the JSONL files according to the user's retention needs. <br>


## Reference(s): <br>
- [Agent integration snippet](templates/agents-snippet.md) <br>
- [ClawHub skill page](https://clawhub.ai/besty0121/experiment-notes) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [CLI text output and markdown command snippets backed by local JSONL files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reads local experiment and lesson records under ~/.openclaw/memory/experiments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
