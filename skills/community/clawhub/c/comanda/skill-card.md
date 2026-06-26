## Description: <br>
Generate, visualize, and execute declarative AI pipelines using the comanda CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kris-hansen](https://clawhub.ai/user/kris-hansen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Comanda to create, inspect, edit, and run YAML-based LLM workflows across multiple model providers and agent CLIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Comanda workflows can call models, run allowlisted shell tools, read or write files, and persist indexes or loop output. <br>
Mitigation: Review generated YAML before running workflows, keep tool allowlists narrow, and avoid untrusted shell-enabled workflows. <br>
Risk: Workflows may use external provider credentials or process private repository content. <br>
Mitigation: Scope provider API keys where possible and be careful when indexing private repositories or running long agentic loops. <br>


## Reference(s): <br>
- [Comanda homepage](https://comanda.sh) <br>
- [Comanda repository](https://github.com/kris-hansen/comanda) <br>
- [Comanda Workflow Spec](references/WORKFLOW-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML workflow examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce workflow files, command suggestions, charts, and execution guidance for the comanda CLI.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
