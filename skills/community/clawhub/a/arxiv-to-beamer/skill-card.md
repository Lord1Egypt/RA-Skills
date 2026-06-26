## Description: <br>
Given an arxiv identifier or arxiv abs/pdf URL, download the LaTeX source or use MinerU's PDF-to-Markdown fallback, ask an OpenRouter model to generate a Beamer presentation introducing the work, and package the result as an Overleaf-uploadable zip. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dirtycomputer](https://clawhub.ai/user/dirtycomputer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and agents use this skill to turn an arXiv identifier or URL into an Overleaf-ready Beamer slide deck. It is intended for paper-introduction workflows where source TeX is available or a PDF-only paper can be converted through MinerU. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded paper archives may contain paths that write outside the temporary working folder during extraction. <br>
Mitigation: Run the skill only on papers you trust, use a sandboxed working directory, and harden archive extraction before regular use. <br>
Risk: Paper content is sent to OpenRouter and may be sent to MinerU for PDF-only fallback processing. <br>
Mitigation: Avoid using the skill with confidential or restricted papers, and use dedicated API keys with limited scope. <br>
Risk: The generated Beamer project may contain inaccurate or misleading model-authored summaries of the source paper. <br>
Mitigation: Review the generated slides against the original paper before presenting or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dirtycomputer/arxiv-to-beamer) <br>
- [arXiv](https://arxiv.org) <br>
- [MinerU](https://mineru.net) <br>
- [OpenRouter API](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command output; generated artifact is an Overleaf-uploadable ZIP containing LaTeX project files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and may require MINERU_API_TOKEN for PDF-only papers; source text is capped before model submission.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
