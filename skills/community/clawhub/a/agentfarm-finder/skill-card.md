## Description: <br>
Monitors Twitter/X daily to find and filter new AI Agent, Crypto, and DeFi project posts matching configured keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torchesfrms](https://clawhub.ai/user/torchesfrms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and crypto researchers use this skill to monitor social posts for early AI Agent, Crypto, and DeFi project leads and produce raw and filtered result files for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release declares wallet, purchase, transaction-signing, and OAuth capabilities that are not justified by the observed monitoring scripts. <br>
Mitigation: Review capability declarations before installation and do not grant wallet, transaction-signing, purchasing, or OAuth access unless a trusted reviewer confirms the need. <br>
Risk: The scripts write collected results to a hard-coded local output path. <br>
Mitigation: Change output paths to the intended workspace before running the skill. <br>
Risk: Bundled and generated social-media rows may contain untrusted promotional content. <br>
Mitigation: Treat results as leads for independent review, not as investment, wallet, or operational instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/torchesfrms/agentfarm-finder) <br>
- [Publisher profile](https://clawhub.ai/user/torchesfrms) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, csv, shell commands, configuration] <br>
**Output Format:** [Shell output plus JSON, CSV, and Markdown result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs searches with configurable keyword, count, and time-window settings and writes raw and filtered social-media results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
