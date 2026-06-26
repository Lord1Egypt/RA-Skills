## Description: <br>
Generates personalized running training plans using Jack Daniels' Running Formula concepts, including VDOT-based paces, E/T/I/R training types, periodization, rest-day placement, and TXT/CSV export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiminshuixing](https://clawhub.ai/user/yiminshuixing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External runners and coaches use this skill to create structured 5K, 10K, half-marathon, and marathon training plans from goals, recent performance, experience, rest-day preferences, and available running days. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated training plans may be saved as TXT and CSV files on the local desktop path named by the skill. <br>
Mitigation: Use chat-only output or request a different filename/path when local storage is not desired, and avoid sharing fitness or schedule details that should not be stored locally. <br>
Risk: Training guidance may not fit a runner's health status, injury history, or recovery needs. <br>
Mitigation: Treat plans as advisory, adjust based on body signals and recovery, and seek qualified medical or coaching advice for pain, injury, or health constraints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yiminshuixing/daniels-running-plan) <br>
- [Skill README](README.md) <br>
- [Running training core knowledge](references/knowledge.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, CSV files, guidance] <br>
**Output Format:** [Markdown-style running plan text plus TXT and UTF-8 BOM CSV file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses week/day labels instead of calendar dates; CSV columns include week, day, name, steps, hr_min, and hr_max.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
