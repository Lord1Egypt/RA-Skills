## Description: <br>
Run eBay seller account activity cycles through ADS Power by searching, browsing, favoriting, and adding items to cart on a rotating schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[powerzzjohn](https://clawhub.ai/user/powerzzjohn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run scheduled ADS Power browser sessions for eBay seller accounts, rotating accounts and performing search, browse, watchlist, and cart actions. Use only with accounts the operator owns or is explicitly authorized to manage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates live marketplace account behavior, including watchlist and cart actions, which may affect account state or marketplace standing. <br>
Mitigation: Run it only on accounts the operator owns or is explicitly authorized to manage, and review marketplace rules before enabling account-state-changing actions. <br>
Risk: ADS Power API credentials are required to operate the automation. <br>
Mitigation: Store ADS Power credentials outside source control using local configuration or environment variables, and rotate exposed keys. <br>
Risk: The security verdict identifies insufficient guardrails for a marketplace account workflow. <br>
Mitigation: Review the scripts before installation, start with the quick test, and disable watchlist or cart behavior unless there is explicit account-level approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/powerzzjohn/ebay-account-automation) <br>
- [Publisher profile](https://clawhub.ai/user/powerzzjohn) <br>
- [Metadata homepage](https://github.com/yourrepo/ebay-account-automation) <br>
- [Artifact README](artifact/references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JavaScript configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces runnable Node.js automation guidance and scripts that require ADS Power Local API access and an ADS Power API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
