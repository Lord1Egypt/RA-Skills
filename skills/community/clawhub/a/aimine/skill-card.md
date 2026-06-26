## Description: <br>
Mine AIT (Proof of AI Work) on BNB Chain. Install, configure, start/stop mining entirely from OpenClaw. No terminal or manual file edits required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nancyuahon](https://clawhub.ai/user/nancyuahon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to install, configure, start, stop, and inspect AIT Proof of AI Work mining from an OpenClaw agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet private keys and OpenAI API keys. <br>
Mitigation: Use a dedicated low-value wallet, avoid pasting private keys into chat, prefer secure environment injection, and limit the OpenAI key. <br>
Risk: The skill installs and runs live remote mining code with npm and Node.js. <br>
Mitigation: Inspect or pin the AIMineRes/PoAIW code before allowing npm install or starting the miner. <br>


## Reference(s): <br>
- [AI Mine skill page](https://clawhub.ai/nancyuahon/aimine) <br>
- [nancyuahon publisher profile](https://clawhub.ai/user/nancyuahon) <br>
- [PoAIW miner repository referenced by the skill](https://github.com/AIMineRes/PoAIW.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize local miner status fields such as miningActive, blocksMined, tokenBalance, bnbBalance, and hashRate.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
