## Description: <br>
Azure AI Evaluation SDK for Python helps evaluate generative AI applications with quality, safety, and custom evaluators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI engineers use this skill to configure Azure AI Evaluation, run single-row or batch evaluations, create custom evaluators, and optionally log results to Azure AI Foundry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation inputs and outputs may be sent to or stored in Azure services when AI-assisted evaluators or Foundry logging are used. <br>
Mitigation: Review and redact datasets before evaluation, avoid sensitive data where possible, and confirm Azure retention and access controls for the target project. <br>
Risk: The skill uses Azure credentials and can access Azure OpenAI or Azure AI Foundry resources. <br>
Mitigation: Run in a virtual environment with least-privilege Azure credentials and verify the installed azure-ai-evaluation package source before use. <br>


## Reference(s): <br>
- [Built-in Evaluators Reference](references/built-in-evaluators.md) <br>
- [Custom Evaluators Reference](references/custom-evaluators.md) <br>
- [Azure AI Evaluation Py on ClawHub](https://clawhub.ai/thegovind/azure-ai-evaluation-py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks; optional JSON result files from the batch evaluation script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Azure OpenAI credentials and Azure AI Foundry project configuration when running AI-assisted, safety, or logged evaluations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
