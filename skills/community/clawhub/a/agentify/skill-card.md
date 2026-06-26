## Description: <br>
Agentify analyzes web pages and code for agent-friendliness, rewrites web templates with semantic and automation-friendly markup, and generates design specs for agent-friendly web development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and web teams use this skill to audit pages, HTML, and component templates for accessibility, structured data, stable selectors, and machine-readable signals, then apply or specify improvements for agents, crawlers, and automation tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad file globs or URL fetching can expose more site or repository content than intended. <br>
Mitigation: Provide specific URLs or file paths and avoid broad globs over sensitive repositories. <br>
Risk: Generated markup, JSON-LD, ARIA, or data-testid changes may be incorrect for a site's semantics or workflow. <br>
Mitigation: Review generated diffs and confirm structured data and selectors before deployment. <br>


## Reference(s): <br>
- [Agentify README](README.md) <br>
- [Agent-Friendliness Checklist](references/checklist.md) <br>
- [Framework Adapters](references/frameworks.md) <br>
- [Agent-Friendliness Knowledge Base](references/knowledge-base.md) <br>
- [Agent-Friendly Patterns](references/patterns.md) <br>
- [Agent-Friendliness Scoring](references/scoring.md) <br>
- [Agent-Friendly Spec Template](references/spec-template.md) <br>
- [schema.org](https://schema.org) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown reports, code edits or examples, and generated specification files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or write agent-friendly-spec.md and may recommend HTML, JSX, Vue, or Svelte markup changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
