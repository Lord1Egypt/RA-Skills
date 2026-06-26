## Description: <br>
Fetches a specified arXiv paper by ID or URL, classifies it with an LLM agent, and prints Chinese deep-reading notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aurora-1412](https://clawhub.ai/user/Aurora-1412) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and technical readers use this skill to fetch a public arXiv paper, classify it into a reading category, and generate structured Markdown reading notes through a configured OpenAI-compatible LLM endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected paper text and metadata are sent to the LLM provider configured in .env. <br>
Mitigation: Use a trusted or local-compatible endpoint and avoid processing private or unpublished manuscripts. <br>
Risk: Dependency behavior may change over time because requirements use lower-bound version constraints. <br>
Mitigation: Review and pin dependency versions before deploying in sensitive or controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Aurora-1412/arxiv-reader) <br>
- [arXiv abstract URL format](https://arxiv.org/abs/{arxiv_id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reading notes printed to stdout, with setup and run commands documented in the skill.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese output by default; reading behavior depends on the selected category prompt and configured LLM endpoint.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
