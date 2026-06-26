## Description: <br>
Converts natural-language descriptions or Mermaid source into flowchart and diagram outputs, with optional DeepSeek or OpenAI generation, templates, multiple Mermaid diagram types, and troubleshooting support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andapeng](https://clawhub.ai/user/andapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and technical writers use this skill to turn process descriptions or existing Mermaid code into flowcharts, architecture diagrams, timelines, and rendered PNG, SVG, or PDF assets for documentation and planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram prompts may be sent to the selected DeepSeek or OpenAI provider when LLM generation is enabled, which can expose sensitive or proprietary process details. <br>
Mitigation: Avoid secrets and confidential content in prompts; use --no-llm, --raw, or a selected template when local-only generation is required. <br>
Risk: The skill reads API credentials from command-line arguments, environment variables, or the OpenClaw configuration file when configured to use an LLM provider. <br>
Mitigation: Provide only least-privilege credentials, prefer environment or managed configuration storage, and rotate credentials if prompts or logs may have exposed them. <br>
Risk: Security evidence flags an unsafe Windows command-execution pattern around Mermaid CLI calls. <br>
Mitigation: Use extra caution on Windows, review commands before execution, and prefer environments where Mermaid CLI invocation has been reviewed or patched. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/andapeng/flowchart-gen) <br>
- [Mermaid documentation](https://mermaid.js.org) <br>
- [Mermaid flowchart syntax](https://mermaid.js.org/syntax/flowchart.html) <br>
- [Mermaid Live Editor](https://mermaid.live) <br>
- [Syntax guide](references/syntax-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Mermaid source and rendered PNG, SVG, or PDF diagram files, with Markdown-style setup and troubleshooting guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and Mermaid CLI; can use DeepSeek or OpenAI credentials when LLM generation is enabled, or stay local with raw Mermaid input and no-LLM template mode.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
