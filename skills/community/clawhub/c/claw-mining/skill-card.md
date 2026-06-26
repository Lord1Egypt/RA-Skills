## Description: <br>
Mine $CLAW tokens via Proof of AI Work on Ethereum with an agent-guided workflow for setup, status checks, and mining commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minewithclaw](https://clawhub.ai/user/minewithclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to configure and run CLAW mining on Ethereum, including status checks, single-cycle mining, and continuous mining. The workflow guides credential setup and local execution of the bundled miner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a hot wallet private key to sign Ethereum transactions and spend gas. <br>
Mitigation: Use only a dedicated low-balance hot wallet, never a main wallet or seed phrase, and inspect the exact code before running mining commands. <br>
Risk: Mining can call paid third-party AI APIs and may continue running in automatic mode. <br>
Mitigation: Monitor AI API and gas spending, configure spending limits where available, and run automatic mode only when ongoing mining is intentional. <br>
Risk: Custom AI API or Oracle endpoints can change trust assumptions. <br>
Mitigation: Avoid custom AI endpoints unless they are trusted, and keep the default HTTPS Oracle endpoint unless there is a specific reason to change it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minewithclaw/claw-mining) <br>
- [Project homepage](https://minewithclaw.com) <br>
- [Project repository from skill metadata](https://github.com/Cliai21/clawing) <br>
- [Mining guide](docs/MINING_GUIDE.md) <br>
- [Oracle service](https://oracle.minewithclaw.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce setup guidance for environment variables, wallet configuration, mining status checks, and commands that initiate paid API calls or Ethereum transactions.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
