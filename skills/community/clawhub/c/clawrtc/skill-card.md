## Description: <br>
ClawRTC helps an agent mine, hold, and spend RustChain RTC tokens through hardware attestation, wallet setup, and signed RTC transfer commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottcjn](https://clawhub.ai/user/scottcjn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use ClawRTC to configure an RTC wallet, run RustChain mining on eligible physical hardware, inspect miner status, and initiate signed pay, tip, gas, or settlement transfers. It is most relevant where the operator intentionally wants crypto mining and wallet behavior inside an agent environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is a crypto mining and wallet tool that fingerprints the machine, sends stable device identifiers to RustChain infrastructure, and has under-disclosed telemetry. <br>
Mitigation: Install only on hardware the operator is comfortable identifying to RustChain, review the disclosure before use, and prefer a reviewed release with accurate telemetry disclosure. <br>
Risk: Wallet keys and exported wallet files may expose funds if mishandled. <br>
Mitigation: Treat exported wallet files as private keys, store them only in protected locations, and avoid running the wallet flow on shared or untrusted machines. <br>
Risk: Security evidence flags contradictions between the release's TLS or security claims and observed behavior. <br>
Mitigation: Avoid BCOS admin credentials with this version and prefer a reviewed or fixed release with normal TLS verification. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scottcjn/clawrtc) <br>
- [PyPI Package](https://pypi.org/project/clawrtc/) <br>
- [npm Package](https://www.npmjs.com/package/clawrtc) <br>
- [RustChain](https://rustchain.org) <br>
- [Block Explorer](https://rustchain.org/explorer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and command descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce wallet, mining, attestation, and transfer guidance that requires local operator review before execution.] <br>

## Skill Version(s): <br>
1.9.0 (source: server release, pyproject.toml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
