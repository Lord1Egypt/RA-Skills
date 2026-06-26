## Description: <br>
Bocha Web Search wraps Bocha's Web Search, AI Search, Agent Search, and Semantic Reranker APIs through Node.js and shell scripts with standard parameters plus raw JSON passthrough. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YIKAILucas](https://clawhub.ai/user/YIKAILucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call Bocha search and reranking services for Chinese web retrieval, AI-assisted search, source-backed answers, fact checking, industry report discovery, and document reranking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and raw JSON payloads are sent to Bocha as an external provider. <br>
Mitigation: Avoid submitting secrets, confidential material, or sensitive personal data in queries or raw JSON payloads. <br>
Risk: The skill requires a Bocha API key for authenticated API calls. <br>
Mitigation: Use a dedicated Bocha API key, prefer the BOCHA_API_KEY environment variable, and keep local config.json out of shared repositories. <br>
Risk: Search and AI-search results may contain incomplete, outdated, or misleading information. <br>
Mitigation: Review returned sources and prioritize authoritative institutional references before using results in downstream answers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/YIKAILucas/bocha-web-search-yikailucas) <br>
- [Bocha Web Search API Endpoint](https://api.bochaai.com/v1/web-search) <br>
- [Bocha AI Search API Endpoint](https://api.bochaai.com/v1/ai-search) <br>
- [Bocha Agent Search API Endpoint](https://api.bochaai.com/v1/agent-search) <br>
- [Bocha Semantic Reranker API Endpoint](https://api.bochaai.com/v1/semantic-reranker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses from Bocha APIs, with optional pretty-printed JSON and shell usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bocha API key via BOCHA_API_KEY or local config.json; sends queries and raw JSON payloads to Bocha.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
