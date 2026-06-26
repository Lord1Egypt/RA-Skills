## Description: <br>
Fund Invest Advisor helps agents produce fund-investment calculations, dollar-cost averaging simulations, asset allocation suggestions, risk checks, rebalancing guidance, and fund education material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to explore fund investing scenarios, compare DCA outcomes, generate allocation and rebalancing suggestions, review portfolio risk, and produce educational guidance. It is not a substitute for personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate projections, allocation suggestions, and fund guidance that may be mistaken for guaranteed returns or personalized financial advice. <br>
Mitigation: Treat outputs as educational planning support, verify assumptions independently, and consult a qualified financial professional before making investment decisions. <br>
Risk: Portfolio commands may store entered fund positions and transaction history in local plaintext files. <br>
Mitigation: Avoid entering sensitive portfolio details unless local plaintext storage is acceptable, and review or remove local data files when no longer needed. <br>
Risk: The artifact includes bash and embedded Python scripts that execute locally. <br>
Mitigation: Review commands before running them and install only if local script execution is acceptable. <br>


## Reference(s): <br>
- [Fund Invest Advisor release page](https://clawhub.ai/ckchzh/fund-invest-advisor) <br>
- [Fund investment practical guide](artifact/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prose with inline shell commands and calculator-style text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some portfolio commands may write local JSONL and log files under the user's fund-invest-advisor data directory.] <br>

## Skill Version(s): <br>
2.3.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
