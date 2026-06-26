## Description: <br>
Iteratively densifies text summaries with Chain-of-Density for compressing verbose documentation, condensing requirements, or creating executive summaries while preserving information density. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killerapp](https://clawhub.ai/user/killerapp) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, analysts, and content authors use this skill to compress long documentation, requirements, and reports into dense summaries with optional entity history and deterministic word-count checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The original source text is passed through repeated summarization iterations, which can expose private or regulated content to the configured cod-iteration subagent. <br>
Mitigation: Use only an approved cod-iteration subagent and data-handling environment for sensitive documents, or avoid using the skill on regulated content. <br>
Risk: Dense summaries can omit nuance and the artifact explicitly discourages use on legal, compliance, tutorial, already concise, or specification content. <br>
Mitigation: Reserve the skill for ordinary summarization tasks and require human review before relying on dense summaries for high-precision materials. <br>


## Reference(s): <br>
- [From Sparse to Dense: GPT-4 Summarization with Chain of Density Prompting](https://arxiv.org/abs/2309.04269) <br>
- [Hugging Face chain_of_density dataset](https://huggingface.co/datasets/griffin/chain_of_density) <br>
- [ClawHub Chain of Density release](https://clawhub.ai/killerapp/chain-of-density) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text summary or YAML-style Markdown history, with optional shell commands for deterministic text metrics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final summaries maintain a target word count across iterations; optional history records missing entities and per-iteration summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
