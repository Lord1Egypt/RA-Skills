## Description: <br>
Professional BaZi (八字) chart calculator and analysis tool for calculating Four Pillars of Destiny from birth date, time, and location, with solar-term calculation, true solar-time correction, hidden stems, ten gods, five elements analysis, major luck periods, and relationship analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate and explain BaZi charts from birth date, time, location, and gender. It is intended for Chinese metaphysics and Four Pillars analysis, including chart structure, element balance, ten-god relationships, luck periods, and annual luck. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unpinned astronomy dependency versions can affect reproducibility of calculated charts. <br>
Mitigation: Install in the documented virtual environment and pin the ephem dependency when reproducible results are required. <br>
Risk: Birth date, birth time, location, and gender are personal information. <br>
Mitigation: Process inputs locally, avoid retaining birth details in logs or shared transcripts, and disclose handling expectations before use. <br>
Risk: A known calculation issue may affect accuracy near solar-term boundaries. <br>
Mitigation: Treat boundary cases cautiously and compare results against trusted references until the time-conversion issue is fixed or validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reed1898/bazi-chart) <br>
- [Publisher profile](https://clawhub.ai/user/reed1898) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and optional text or JSON chart output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes birth details locally; supports city lookup or explicit coordinates, text or JSON output, true solar-time correction, and optional annual luck year.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
