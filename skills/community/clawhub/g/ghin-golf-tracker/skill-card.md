## Description: <br>
Analyzes local GHIN golf JSON data to report handicap trends, scoring patterns, course statistics, and yearly performance without external connections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Golfers and developers use this skill to analyze an already-collected GHIN data JSON file and produce handicap, scoring, course, and yearly performance summaries for review or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The input GHIN export may contain personal golf history or account-adjacent data. <br>
Mitigation: Use a manually exported local JSON file when possible and review any separate collection tool independently before giving it credentials or account access. <br>
Risk: The analyzer depends on the structure and completeness of the supplied JSON file. <br>
Mitigation: Check that the file includes expected GHIN fields such as scores or handicap_index before relying on trend and scoring summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pfrederiksen/ghin-golf-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/pfrederiksen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Analysis, Guidance] <br>
**Output Format:** [Plain text report or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-provided GHIN JSON file locally and does not write files.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
