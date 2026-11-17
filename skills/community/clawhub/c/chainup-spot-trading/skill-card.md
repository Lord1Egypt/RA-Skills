## Description:

ChainUp/OpenAPI V2 spot and margin trading skill. Prefer using the Python script to call `sapi` endpoints through one unified entrypoint and avoid ad hoc signing logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lurenha](https://clawhub.ai/user/lurenha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to access ChainUp OpenAPI V2 spot, margin, account, order, and market-data workflows through a centralized signed Python entrypoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent high-impact financial authority over ChainUp account, order, transfer, and margin operations.

Mitigation: Use least-privilege API keys, avoid transfer or withdrawal permissions unless required, and review balance-changing requests before execution.

Risk: The API destination is configurable, so credentials could be sent to an unverified host if the base URL is misconfigured.

Mitigation: Allow only trusted ChainUp API hosts and do not permit arbitrary `--base-url` values in normal operation.

Risk: The documented `--no-confirm-gate` option can bypass the confirmation control for mutating requests.

Mitigation: Keep the confirmation gate enabled and require a standalone `CONFIRM` before live orders, cancellations, or transfers.

Risk: The skill handles sensitive ChainUp API keys and secret keys.

Mitigation: Store credentials securely, mask secrets in outputs, and avoid echoing full credential-bearing commands.

## Reference(s):

- [Authentication and Signing](references/authentication.md)
- [Spot Endpoints](references/spot-endpoints.md)
- [Margin Endpoints](references/margin-endpoints.md)
- [ChainUp OpenAPI V2 Spot Documentation](https://exchangedocsv2.gitbook.io/open-api-doc-v2/jian-ti-zhong-wen-v2/bi-bi-jiao-yi)
- [ChainUp OpenAPI V2 FAQ](https://exchangedocsv2.gitbook.io/open-api-doc-v2/jian-ti-zhong-wen-v2/chang-jian-wen-ti)
- [ChainUp OpenAPI V2 Margin Documentation](https://exchangedocsv2.gitbook.io/open-api-doc-v2/jian-ti-zhong-wen-v2/gang-gan-jiao-yi)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns exchange JSON by default; prepare-only order flows return originalBody, preparedBody, adjustments, symbolRule, and readyForConfirm.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
