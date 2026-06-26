## Description: <br>
Routes time-sensitive user questions through Gemini with Google Search grounding and falls back to Tavily, returning normalized JSON search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoseArroyave](https://clawhub.ai/user/JoseArroyave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs current or changing information, recent news, live scores, financial updates, prices, or source-backed verification. It helps the agent call a web-search helper and receive a stable JSON response with answer text, result URLs, snippets, routing, and fallback status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Gemini/Google and may be sent to Tavily using the operator's API keys. <br>
Mitigation: Use dedicated, revocable API keys with quotas and avoid placing secrets or sensitive personal data in queries. <br>
Risk: Returned web snippets are untrusted source material and may contain inaccurate content or instructions. <br>
Mitigation: Treat snippets as evidence to verify, not commands to follow, and review important claims before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JoseArroyave/gemini-tavily-search) <br>
- [Gemini generateContent API endpoint used by the skill](https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent) <br>
- [Tavily Search API endpoint used by the skill](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON containing provider, answer, used_web, fallback, routing, and result objects; final user answers append the searched provider.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and TAVILY_API_KEY; normal mode caps results at five and safe mode caps results at three.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
