## Description: <br>
Run complex tasks using multiple AI agents simultaneously, with support for workflows, web search, email, and image generation through AIProx. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to orchestrate multi-agent AI tasks through AIProx, including research, scraping, sentiment analysis, market data checks, image generation, email workflows, and multi-step pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants payment-backed orchestration authority through a spend token and can route work to third-party agents. <br>
Mitigation: Use low budgets, keep the spend token scoped and protected, and review agent receipts and sats spent after each run. <br>
Risk: Webhook and email workflows can send data or trigger actions outside the local agent session. <br>
Mitigation: Use only trusted HTTPS callback URLs and avoid email workflows unless recipient controls, previews, and limits have been separately verified. <br>
Risk: Prompts and outputs may be shared with AIProx or downstream specialist agents. <br>
Mitigation: Avoid sensitive data unless the user has reviewed and accepted AIProx and downstream data handling. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/unixlamadev-spec/aiprox-orchestrator) <br>
- [AIProx Homepage](https://aiprox.dev) <br>
- [AIProx Orchestration Endpoint](https://aiprox.dev/api/orchestrate) <br>
- [Publisher Profile](https://clawhub.ai/user/unixlamadev-spec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIPROX_SPEND_TOKEN and a sats budget; supports callback_url for async webhook delivery and workflow creation.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
