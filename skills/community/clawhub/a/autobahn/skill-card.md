## Description: <br>
Operate autonomous onchain-governed entities via agents: identity, governance, contracts, and registry/community workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unifiedh](https://clawhub.ai/user/unifiedh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and operator agents use Autobahn to manage autonomous on-chain entity workflows, including identity, governance, formation documents, contracts, lending, litigation preparation, and registry/community operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release installs an unverified external CLI that may handle wallet keys and high-impact legal or financial actions. <br>
Mitigation: Install only when the publisher and release source are trusted, verify the downloaded CLI out of band, and begin with a low-value wallet or entity. <br>
Risk: Autobahn workflows can trigger irreversible on-chain, governance, transfer, document-signing, public-posting, bounty, and legal-document actions. <br>
Mitigation: Manually review every transaction, governance action, document hash, public post, bounty, and transfer before confirming execution. <br>
Risk: Secrets may be exposed if private keys or passwords are passed or logged through command-line workflows. <br>
Mitigation: Avoid passing private keys or passwords on the command line and keep outputs redacted when handling secrets. <br>


## Reference(s): <br>
- [Autobahn ClawHub release](https://clawhub.ai/unifiedh/autobahn) <br>
- [Autobahn homepage](https://autobahn.surf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI/API instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs agents to use the autobahn CLI with --json and route human-readable progress to stderr.] <br>

## Skill Version(s): <br>
0.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
