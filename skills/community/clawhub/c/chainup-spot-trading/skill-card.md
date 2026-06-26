## Description: <br>
ChainUp/OpenAPI V2 spot and margin trading skill that routes account, market-data, order, cancellation, transfer, and margin requests through a unified signed Python entrypoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lurenha](https://clawhub.ai/user/lurenha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to work with ChainUp OpenAPI V2 spot and margin endpoints for market data, account queries, order placement, cancellation, asset transfer, and trade-history workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use ChainUp/OpenAPI V2 credentials for live trades, cancellations, transfers, and margin actions. <br>
Mitigation: Use least-privilege API keys, verify the base URL and credential source, and require explicit confirmation before live balance-changing requests. <br>
Risk: A documented confirmation bypass can skip the normal live-action gate. <br>
Mitigation: Do not allow the confirmation bypass on live accounts unless the operator has deliberately accepted that risk. <br>
Risk: Credential exposure could occur if secrets are passed through visible command lines or copied into responses. <br>
Mitigation: Prefer configured credential sources, avoid inlining secrets in commands, and mask API keys or secret keys in output. <br>


## Reference(s): <br>
- [ChainUp Spot Trading release page](https://clawhub.ai/lurenha/chainup-spot-trading) <br>
- [ChainUp OpenAPI V2 spot endpoints](https://exchangedocsv2.gitbook.io/open-api-doc-v2/jian-ti-zhong-wen-v2/bi-bi-jiao-yi) <br>
- [ChainUp OpenAPI V2 authentication FAQ](https://exchangedocsv2.gitbook.io/open-api-doc-v2/jian-ti-zhong-wen-v2/chang-jian-wen-ti) <br>
- [ChainUp OpenAPI V2 margin endpoints](https://exchangedocsv2.gitbook.io/open-api-doc-v2/jian-ti-zhong-wen-v2/gang-gan-jiao-yi) <br>
- [Authentication reference](references/authentication.md) <br>
- [Spot endpoints reference](references/spot-endpoints.md) <br>
- [Margin endpoints reference](references/margin-endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and raw JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses signed ChainUp/OpenAPI V2 requests and returns raw exchange JSON by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
