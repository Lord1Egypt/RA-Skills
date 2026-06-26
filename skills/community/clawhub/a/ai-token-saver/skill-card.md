## Description: <br>
한국어 특화 Context DB로 AI 토큰 사용량을 최대 96% 절감하며 프롬프트를 최적화하고 메모리 검색을 지원합니다. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorongss](https://clawhub.ai/user/dorongss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to save Korean-language context, search stored memory at different detail levels, and reduce prompt size when working with repeated project or business context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved context and search queries are sent to and may be persisted by TokenSaver's external service. <br>
Mitigation: Avoid storing secrets, credentials, customer data, regulated data, or private project material unless the service's retention and privacy terms are acceptable. <br>
Risk: Broad activation triggers for token saving, memory search, context storage, and prompt optimization could lead to unintended context upload. <br>
Mitigation: Confirm user intent before saving or searching sensitive context, and use the API key only through the documented environment variable or constructor input. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dorongss/ai-token-saver) <br>
- [TokenSaver service](https://tokensaver.ai) <br>
- [TokenSaver API endpoint](https://api.tokensaver.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell snippets, plus JSON-like API responses and CLI text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a TokenSaver API key and may return saved memory, search results, usage counts, token estimates, and endpoint configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
