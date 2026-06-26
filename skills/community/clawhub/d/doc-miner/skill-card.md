## Description: <br>
Extract summaries, answers, or structured data from any URL, PDF, or raw text. Auto-detects mode from task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and developers use Doc Miner to summarize long documents, answer questions about document contents, and extract entities, dates, or numeric facts from URLs, PDFs, webpages, or pasted text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided URLs, documents, or pasted text are sent to AIProx and downstream analysis providers. <br>
Mitigation: Avoid submitting confidential, regulated, or internal-only material unless AIProx terms, retention promises, and provider handling meet the user's requirements. <br>
Risk: The AIPROX_SPEND_TOKEN environment variable is used for paid API access. <br>
Mitigation: Use a spend token with appropriate limits and keep it out of prompts, shared logs, and committed files. <br>


## Reference(s): <br>
- [AIProx](https://aiprox.dev) <br>
- [AIProx orchestration API](https://aiprox.dev/api/orchestrate) <br>
- [Doc Miner on ClawHub](https://clawhub.ai/unixlamadev-spec/doc-miner) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON responses with summary, Q&A, or extraction fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mode-specific fields may include summary, key_points, word_count, answer, context, confidence, entities, dates, numbers, and source_type.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
