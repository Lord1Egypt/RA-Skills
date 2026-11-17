## Description:

Search, register, and manage domains via Bloomfilter x402 API - pay with USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eronmmer](https://clawhub.ai/user/eronmmer)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to search domain availability, register or renew domains with USDC on Base, and manage DNS records through Bloomfilter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate paid domain registration, renewal, and DNS mutation flows when configured with a wallet key.

Mitigation: Require explicit confirmation before registration, renewal, or DNS changes, and keep the wallet funded only for intended domain purchases.

Risk: The local agent runtime uses EVM_PRIVATE_KEY for payment and authentication signing.

Mitigation: Install only when the publisher and Bloomfilter registrar are trusted, and provide a wallet key dedicated to this use case.

## Reference(s):

- [Bloomfilter](https://bloomfilter.xyz)
- [Bloomfilter Documentation](https://docs.bloomfilter.xyz)
- [ClawHub Skill Page](https://clawhub.ai/eronmmer/skills/bloomfilter)
- [Publisher Profile](https://clawhub.ai/user/eronmmer)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with API endpoint examples and request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include domain names, DNS record details, wallet setup guidance, and x402 payment flow instructions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
