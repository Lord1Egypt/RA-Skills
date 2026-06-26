## Description: <br>
Automatically discovers and loads CLAUDE.md files in the project root with support for @include directives and reverse order loading up to 40,000 characters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoxiang616](https://clawhub.ai/user/shaoxiang616) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover CLAUDE.md guidance files in a project tree, expand @include directives, and prepare local project guidance for agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatically loaded CLAUDE.md or included files can silently influence agent behavior when repository content is untrusted. <br>
Mitigation: Use the skill only in repositories and parent directories you trust, and review which guidance files are loaded before applying their content. <br>
Risk: Broad upward discovery and @include processing can load unintended local guidance into the agent context. <br>
Mitigation: Prefer an opt-in workflow that limits discovery to the intended project root and treats loaded content as untrusted project guidance rather than privileged instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaoxiang616/claude-md-auto-discovery) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text containing discovered CLAUDE.md content and separators] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Caps combined loaded content at 40,000 characters before returning it.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
