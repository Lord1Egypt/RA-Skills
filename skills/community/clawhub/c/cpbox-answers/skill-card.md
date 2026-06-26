## Description: <br>
Provides AI-grounded answers through an OpenAI-compatible chat completions interface with single-search and deep research modes, streaming or blocking responses, and citation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintmint](https://clawhub.ai/user/sprintmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request web-grounded AI answers from a paid x402 endpoint, choosing fast single-search answers or streaming deep research for more comprehensive cited responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically settle x402 payments without clear spending limits or per-request approval. <br>
Mitigation: Use an isolated wallet or strict spending limit, require confirmation before paid calls, and avoid automated retries that could trigger repeated charges. <br>
Risk: Prompts and requests are sent to third-party services for answer generation and payment handling. <br>
Mitigation: Use only if cpbox.io, cppay.finance, and the x402 payment helper are trusted, and do not send sensitive prompts unless the provider's data handling is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sprintmint/cpbox-answers) <br>
- [API provider](https://www.cpbox.io) <br>
- [x402 payment facilitator](https://www.cppay.finance) <br>
- [Answers endpoint](https://www.cpbox.io/api/x402/answers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [OpenAI-compatible JSON or SSE text stream with optional citation, answer, progress, and usage tags.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports blocking single-search responses, streaming single-search responses with citations, and streaming research responses with usage data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
