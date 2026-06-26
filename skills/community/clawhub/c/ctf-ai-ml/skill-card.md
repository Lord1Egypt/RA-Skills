## Description: <br>
Provides AI and machine learning techniques for CTF challenges, including model analysis, adversarial examples, model extraction, prompt injection, membership inference, data poisoning, fine-tuning manipulation, neural network analysis, LoRA adapter exploitation, and LLM jailbreaking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gandli](https://clawhub.ai/user/gandli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security learners, and authorized CTF or red-team participants use this skill as a quick reference for AI and machine learning challenge techniques. It helps agents generate command examples, Python snippets, and tactical guidance for analyzing or attacking ML models in lab environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives operational exploit guidance for AI and machine learning attack techniques. <br>
Mitigation: Use it only for authorized CTF, lab, or internal red-team work, and do not apply the techniques to third-party systems without explicit permission. <br>
Risk: Examples may target network services or external model APIs. <br>
Mitigation: Review every network target before running examples and restrict testing to disposable, isolated environments. <br>
Risk: Loading untrusted PyTorch model files can execute unsafe deserialization paths. <br>
Mitigation: Avoid loading untrusted .pt files with torch.load; prefer safer formats such as safetensors when possible. <br>


## Reference(s): <br>
- [CTF AI/ML skill source](artifact/SKILL.md) <br>
- [Model attacks reference](artifact/model-attacks.md) <br>
- [Adversarial ML reference](artifact/adversarial-ml.md) <br>
- [LLM attacks reference](artifact/llm-attacks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational examples for authorized CTF, lab, or internal red-team use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
