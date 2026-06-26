## Description: <br>
Automated soul synthesis that reads local memory, finds recurring patterns, and builds an identity document grounded in evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to synthesize a SOUL.md identity document from local memory and session history, inspect provenance for generated identity claims, check synthesis status, and roll back generated identity files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads broad personal memory files and local OpenClaw session history, then sends that content to the configured Ollama endpoint. <br>
Mitigation: Start with --dry-run, review sensitive memory and session content before synthesis, and use only the intended local or trusted Ollama endpoint. <br>
Risk: The skill persists generated identity data in SOUL.md and .neon-soul, and those files may be committed into local git history. <br>
Mitigation: Review generated files before relying on or sharing them, adjust output paths when needed, and exclude sensitive generated identity files from commits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/consciousness-soul-identity) <br>
- [Live Neon homepage](https://liveneon.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, conversational summaries, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes SOUL.md and .neon-soul state, cache, and backup files unless run with --dry-run.] <br>

## Skill Version(s): <br>
0.4.9 (source: server release evidence; artifact frontmatter reports 0.4.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
