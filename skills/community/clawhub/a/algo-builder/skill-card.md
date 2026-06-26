## Description: <br>
Build and test systematic daily-to-weekly trading algorithms through hypothesis, signal validation, backtesting, walk-forward validation, and paper-trading readiness steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonbistudio](https://clawhub.ai/user/tonbistudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, systematic traders, and research agents use this skill to structure daily-to-weekly trading strategy research from hypothesis through signal testing, backtesting, walk-forward validation, and paper-trade readiness. It is not intended for high-frequency trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated trading research files and Python templates may be incorrect, incomplete, or unsuitable for live capital decisions. <br>
Mitigation: Use a dedicated workspace, review generated Python before running it, choose data providers deliberately, and treat paper-trading or live-trading steps as manual financial decisions with independent risk controls. <br>
Risk: Generated notes or scripts could expose broker credentials or API keys if users place secrets into research artifacts. <br>
Mitigation: Keep broker credentials and API keys out of generated notes, strategy files, and code templates. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with local file paths and Python code templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local research artifacts under algo-builder/ and asks users to review evidence gates before progressing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
