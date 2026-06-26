## Description: <br>
Generate LLM-optimized codebase context from any directory using context-builder CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorls](https://clawhub.ai/user/igorls) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to generate scoped, LLM-ready Markdown snapshots of codebases for review, onboarding, architecture analysis, and incremental change analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated context may accidentally include private files or sensitive source content if the skill is run against an overly broad directory. <br>
Mitigation: Run it only against explicit project folders, use filters and ignore rules, avoid home, system, and credential directories, and review the generated Markdown before sharing it. <br>
Risk: Using an unexpected context-builder installation could produce different behavior from the documented release. <br>
Mitigation: Install from the documented upstream source and verify the expected context-builder version before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/igorls/context-builder) <br>
- [Context Builder Repository](https://github.com/igorls/context-builder) <br>
- [Context Builder Releases](https://github.com/igorls/context-builder/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, configuration snippets, and generated codebase context files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file contents or code signatures from the target directory; supports filters, token budgets, diff-only output, and signature-only output.] <br>

## Skill Version(s): <br>
0.8.3-1 (source: server release metadata; artifact frontmatter version: 0.8.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
