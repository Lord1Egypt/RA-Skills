## Description: <br>
DeBox Community helps agents query DeBox group information, verify membership and eligibility, and produce community engagement reports for DAO and NFT communities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZanyK4502](https://clawhub.ai/user/ZanyK4502) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and community operators use this skill to check DeBox group membership, validate DAO or NFT community eligibility, batch-verify wallet lists, and generate user or group activity reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes an API-key-like value in config.json. <br>
Mitigation: Delete or replace the bundled config.json, use DEBOX_API_KEY from an environment variable or secret manager, and rotate any key that may have been published. <br>
Risk: Membership, profile, wallet, voting, lottery, and praise lookups can expose sensitive community or user information. <br>
Mitigation: Run lookups and batch verification only for users, wallets, and groups you are authorized to check, and limit sharing of generated reports. <br>
Risk: The optional image report mode can fetch remote avatar images and write local PNG files. <br>
Mitigation: Use image output only when remote avatar fetching and local report files are acceptable, and review output paths before sharing generated images. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ZanyK4502/debox-community-zanyk) <br>
- [DeBox API Reference](references/api.md) <br>
- [DeBox Developer Platform](https://developer.debox.pro) <br>
- [DeBox API Base URL](https://open.debox.pro/openapi) <br>
- [DeBox Documentation](https://docs.debox.pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples; command output is text or JSON, with optional PNG profile reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEBOX_API_KEY and network access to DeBox APIs; batch verification reads local wallet-list files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
