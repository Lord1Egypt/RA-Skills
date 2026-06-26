## Description: <br>
Aistro provides astrology consultation workflows for chat Q&A and personalized natal, prediction, synastry, and moon phase reports using local calculation scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lban2049](https://clawhub.ai/user/lban2049) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for astrology Q&A and personalized horoscope, birth chart, compatibility, and lunar influence readings. The agent collects birth details when needed and uses the included local scripts to calculate chart placements, moon phases, and deterministic report scores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for birth date, birth time, and birth place, which can be personal information. <br>
Mitigation: Only provide birth details you are comfortable sharing, and do not provide another person's birth details without permission or a legitimate reason. <br>
Risk: The skill may install and run local Node dependencies for astrology calculations. <br>
Mitigation: Review the bundled scripts and dependency manifest before deployment, and allow npm installation only in environments where local script execution is acceptable. <br>
Risk: Astrology readings and scores may be interpreted as advice despite being entertainment-oriented guidance. <br>
Mitigation: Treat reports as interpretive guidance rather than factual, medical, legal, financial, or safety-critical advice. <br>


## Reference(s): <br>
- [Natal Chart Report](references/natal-report.md) <br>
- [Horoscope Prediction Report](references/predict-report.md) <br>
- [Synastry Compatibility Report](references/synastry-report.md) <br>
- [Moon Phase Report](references/moon-phase-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Conversational text and Markdown reports, with local shell commands used for JSON-producing astrology calculations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include overview-first reports, expandable detail sections, tables, scores, and same-language responses based on the user's input.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
