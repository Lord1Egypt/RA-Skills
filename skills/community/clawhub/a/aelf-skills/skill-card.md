## Description: <br>
Discovery, download, and configuration hub for the aelf agent skill ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzz780](https://clawhub.ai/user/hzz780) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill to discover, install, configure, route, and health-check aelf ecosystem skills across wallet, DEX, NFT marketplace, explorer, governance, and node workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download and install other blockchain skills. <br>
Mitigation: Install only from trusted sources, prefer bootstrapping one skill at a time with --only, and use --skip-install until downloaded content has been reviewed. <br>
Risk: The routed workflows can lead users toward sensitive wallet, transfer, approval, swap, liquidity, marketplace, contract-send, or governance actions. <br>
Mitigation: Require explicit confirmation before sensitive actions and complete read-only checks such as balance, address, network, allowance, and simulation where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hzz780/aelf-skills) <br>
- [Catalog Schema Semantics](docs/CATALOG_SCHEMA.md) <br>
- [Skill Routing Matrix](docs/SKILL_ROUTING_MATRIX.md) <br>
- [AI End-to-End Execution Scenarios](docs/AI_E2E_SCENARIOS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and routing recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes users to downstream aelf skills and may include bootstrap, setup, health-check, and recovery steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
