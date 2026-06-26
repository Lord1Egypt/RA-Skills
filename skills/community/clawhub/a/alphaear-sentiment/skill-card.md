## Description: <br>
Analyze finance text sentiment using FinBERT or LLM. Use when the user needs to determine the sentiment (positive/negative/neutral) and score of financial text markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouzhonglu8-png](https://clawhub.ai/user/zhouzhonglu8-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to score financial news or market text as positive, negative, or neutral, with a numeric sentiment score and brief reasoning. It supports local FinBERT analysis and agent-driven LLM analysis with optional SQLite updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write sentiment results and related data to a local SQLite database. <br>
Mitigation: Install and run it only where mutation of the configured local database is acceptable, and restrict database paths to the intended skill data store. <br>
Risk: Generic SQL and bulk update helpers could affect data beyond a single sentiment-analysis request if exposed to untrusted input. <br>
Mitigation: Keep the generic SQL helper and batch update paths out of untrusted user workflows; review requested operations before execution. <br>
Risk: LLM provider configuration uses environment variables for external endpoints and API keys. <br>
Mitigation: Verify provider endpoint variables and API keys before use, and avoid exposing unrelated credentials in the runtime environment. <br>
Risk: The local model path may download a model if a cached model is unavailable. <br>
Mitigation: Prefer a locally cached and pinned model before enabling FinBERT analysis in controlled environments. <br>


## Reference(s): <br>
- [ClawHub listing: alphaear-sentiment](https://clawhub.ai/zhouzhonglu8-png/alphaear-sentiment) <br>
- [Publisher profile: zhouzhonglu8-png](https://clawhub.ai/user/zhouzhonglu8-png) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, configuration, guidance] <br>
**Output Format:** [JSON-like sentiment results with score, label, and reason, plus Markdown guidance for agentic analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sentiment scores are normalized from -1.0 to 1.0; database update helpers can persist score and reasoning to SQLite.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
