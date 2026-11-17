## Description:

Run eBay seller account activity cycles via ADS Power: search, browse, favorite, and cart actions on a rotating schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powerzzjohn](https://clawhub.ai/user/powerzzjohn)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators use this skill to run scheduled ADS Power browser sessions that rotate through eBay seller accounts and perform search, browsing, favorite, and cart actions. It is intended for accounts the operator owns or is authorized to manage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change marketplace state across multiple browser profiles by favoriting items and adding items to carts.

Mitigation: Run it only against accounts you own or are authorized to operate, and review eBay and marketplace rules before scheduling automation.

Risk: Scheduled browser automation may affect every ADS Power profile returned by the local API if the operating environment is not constrained.

Mitigation: Use a dedicated ADS Power group or account allowlist before deployment.

Risk: The ADS Power API key is required for execution and could be exposed if stored in source control.

Mitigation: Keep ADS_API_KEY outside source control, preferably in local configuration or environment variables.

Risk: Selector diagnostics and browser automation may fail or behave unexpectedly when eBay page structure changes.

Mitigation: Run selector diagnostics in a controlled test account and fix diagnostic cleanup before production use.

Risk: Unpinned dependencies can change automation behavior across installs.

Mitigation: Pin dependencies with a lockfile before operational use.

## Reference(s):

- [Skill documentation](artifact/references/README.md)
- [ADS Power Local API documentation](https://localapi-doc-zh.adspower.net/)
- [eBay website](https://www.ebay.com)
- [Project homepage](https://github.com/yourrepo/ebay-account-automation)
- [ClawHub skill page](https://clawhub.ai/powerzzjohn/skills/ebay-account-automation)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions and runnable Node.js scripts for ADS Power and eBay browser automation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
