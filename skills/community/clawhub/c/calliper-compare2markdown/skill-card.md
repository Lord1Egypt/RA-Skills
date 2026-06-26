## Description: <br>
Compare two local documents and convert differences into LLM-ready Markdown in one synchronous call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paodingai](https://clawhub.ai/user/paodingai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-review teams use this skill to compare two local PDF, Word, PowerPoint, or image documents through Calliper/PaodingAI and receive a structured Markdown diff for review, extraction, validation, or downstream agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compared documents are uploaded to a configured Calliper/PaodingAI endpoint for processing. <br>
Mitigation: Use the skill only when remote processing is approved for the documents, especially for confidential or regulated content. <br>
Risk: The workflow depends on bearer tokens and a configurable routing base URL. <br>
Mitigation: Store PAODINGAI_API_KEY and CALLIPER_ACCESS_TOKEN as secrets and verify PD_ROUTER_BASE_URL before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paodingai/calliper-compare2markdown) <br>
- [PaodingAI platform endpoint](https://platform.paodingai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown diff text, optionally written to a file and also printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, a bearer token from PAODINGAI_API_KEY or CALLIPER_ACCESS_TOKEN, and network access to the configured PD Router endpoint.] <br>

## Skill Version(s): <br>
1.3.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
