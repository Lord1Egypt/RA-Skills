## Description: <br>
Generates structured answer templates for CIE A-Level Physics (9702) exam questions using a fine-tuned Qwen3-4B LoRA model for local MLX inference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevin0818-lxd](https://clawhub.ai/user/kevin0818-lxd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External students, educators, and developers use this skill to turn text-based CIE 9702 questions into structured answer frameworks for exam practice and tutoring. Maintainers may also use optional pipeline scripts to rebuild datasets, retrain adapters, and evaluate robustness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional retraining and full-pipeline commands can download exam PDFs, create local datasets, and send question or mark-scheme text to DeepSeek when configured with an API key. <br>
Mitigation: Run those workflows only intentionally, with approved source material and API-key handling, and avoid private or licensing-sensitive content. <br>
Risk: The normal local inference path may download Hugging Face base weights on first use. <br>
Mitigation: Confirm model access, network policy, and model terms before first-run deployment; use local cached weights where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kevin0818-lxd/alevel-physics-cie) <br>
- [Project homepage](https://github.com/kevin0818-lxd/alevel-physics-cie) <br>
- [Training pipeline reference](skill/references/training.md) <br>
- [Answer template format reference](skill/references/answer_template_format.md) <br>
- [Xie et al. 2024 adversarial robustness paper](https://arxiv.org/abs/2402.17916) <br>
- [CIE 9702 paper source used by optional scraper](https://cie.fraft.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with structured sections and plain-text math] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normal inference runs locally, requires no DeepSeek API key, and should avoid LaTeX dollar delimiters in final user-facing math.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
