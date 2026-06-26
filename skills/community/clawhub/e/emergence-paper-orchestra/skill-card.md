## Description: <br>
High-rigor, multi-agent scholarly writing framework based on the PaperOrchestra methodology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[symbolscience](https://clawhub.ai/user/symbolscience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research teams use this skill to scaffold and guide high-rigor academic manuscript projects through interview, planning, literature strategy, modular drafting, and review phases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scaffold creates local project files that may later contain sensitive research content. <br>
Mitigation: Run scaffold.sh only in an intended new directory and review generated files before adding sensitive research. <br>
Risk: The artifact references external Emergence Science discovery endpoints. <br>
Mitigation: Verify the referenced API and content index before allowing an agent to use external discovery endpoints. <br>
Risk: Academic-writing assistance can introduce unsupported claims or citation errors. <br>
Mitigation: Use the skill's verification loop to check candidate papers by DOI or arXiv identifiers before adding them to the citation bank. <br>


## Reference(s): <br>
- [PaperOrchestra arXiv paper](https://arxiv.org/abs/2604.05018) <br>
- [ClawHub skill page](https://clawhub.ai/symbolscience/emergence-paper-orchestra) <br>
- [Emergence Science OpenAPI description](https://api.emergence.science/openapi.json) <br>
- [Emergence Science content index](https://api.emergence.science/content/index.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local academic-writing scaffold with idea.md, metadata.json, README.md, section folders, asset folders, and notes folders.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata; artifact frontmatter declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
