## Description: <br>
Evaluate AI training and RAG data quality using rule-based or LLM-based metrics with Dingo's flexible, multi-format assessment framework and CLI/SDK support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[e06084](https://clawhub.ai/user/e06084) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and AI quality teams use this skill to configure and run Dingo evaluations for datasets, RAG outputs, safety checks, and article fact-checking. It helps agents choose suitable rule-based or LLM-based evaluators, prepare configs, run CLI or SDK workflows, and summarize result artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LLM-based evaluation and article fact-checking can send articles, datasets, prompts, references, and retrieved context to configured model or search providers. <br>
Mitigation: Use rule-based or local modes for confidential data, and require explicit approval before enabling external model or search providers. <br>
Risk: Evaluation and fact-checking workflows can save user content and intermediate artifacts locally. <br>
Mitigation: Choose an appropriate output directory, restrict access to generated files, and delete artifacts when they are no longer needed. <br>
Risk: MCP server use can expose local evaluation capabilities and file paths to connected agents. <br>
Mitigation: Limit MCP access to trusted clients and restrict the file paths and datasets available to the server. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/e06084/dingo) <br>
- [Publisher Profile](https://clawhub.ai/user/e06084) <br>
- [Dingo GitHub Repository](https://github.com/MigoXLab/dingo) <br>
- [Dingo SaaS Platform](https://dingo.openxlab.org.cn/) <br>
- [Dingo PyPI Package](https://pypi.org/project/dingo-python/) <br>
- [Metrics Documentation](https://github.com/MigoXLab/dingo/blob/main/docs/metrics.md) <br>
- [RAG Evaluation Guide](https://github.com/MigoXLab/dingo/blob/main/docs/rag_evaluation_en.md) <br>
- [Advanced Configuration](references/advanced-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, Python code, and structured JSON report interpretation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dingo writes summary and per-item evaluation artifacts to output directories; the bundled fact-checking script prints a structured JSON report to stdout.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
