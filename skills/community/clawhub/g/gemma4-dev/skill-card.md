## Description: <br>
A development and orchestration skill for working with the Gemma 4 model family, supporting thinking modes and multi-step agentic workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johngreenfield](https://clawhub.ai/user/johngreenfield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to configure Gemma-focused coding, architecture, debugging, and multi-step reasoning workflows. The artifact also includes sample local, browser, and Vertex AI app code for Gemma model use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sample apps may download Gemma model artifacts or consume local compute. <br>
Mitigation: Review the sample scripts and runtime environment before execution, and run them only where model downloads and compute use are acceptable. <br>
Risk: The Gradio sample may open a local app server. <br>
Mitigation: Run the Gradio app only in an intended local or controlled environment and review its launch behavior before exposing it. <br>
Risk: The Vertex AI sample uses Google Cloud project, location, and endpoint configuration and may consume cloud quota. <br>
Mitigation: Confirm the target Google Cloud project, endpoint, permissions, and cost controls before running the Vertex AI example. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/johngreenfield/gemma4-dev) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Gradio sample app](artifact/assets/gradio-app.py) <br>
- [Transformers.js sample app](artifact/assets/transformers-js-app.js) <br>
- [Vertex AI sample app](artifact/assets/vertex-ai-app.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands, configuration values, and sample Python or JavaScript code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve local model downloads, a local Gradio app, WebGPU execution, or Google Cloud Vertex AI endpoint configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
