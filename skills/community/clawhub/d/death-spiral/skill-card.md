## Description: <br>
Guides agents through diagnosing self-reinforcing competitive decline, mapping moat breaches, early warnings, cascade timing, and intervention windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Strategy teams, founders, investors, board directors, and analysts use this skill to determine whether a company's decline is structural rather than cyclical and to produce a death spiral risk map with intervention timing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt analysis of sensitive company performance, competitor, or strategy information. <br>
Mitigation: Use normal workspace privacy controls and avoid sharing confidential metrics unless the environment is appropriate for that information. <br>
Risk: A cyclical or execution issue could be misclassified as a structural death spiral, leading to misleading strategic guidance. <br>
Mitigation: Apply the skill's gate and false-positive checks by testing cyclicality, reviewing trailing metrics, and requiring named moat breach scenarios before treating the spiral as active. <br>


## Reference(s): <br>
- [Sources - death-spiral](references/sources.md) <br>
- [Kodak's Death Spiral (1994-2012)](examples/kodaks-death-spiral-1994-2012.md) <br>
- [Competitive Advantage: Creating and Sustaining Superior Performance](https://www.simonandschuster.com/books/Competitive-Advantage/Michael-E-Porter/9780684841465) <br>
- [The Innovator's Dilemma](https://www.hbs.edu/faculty/Pages/item.aspx?num=46) <br>
- [Kodak SEC Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000031235) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, analysis] <br>
**Output Format:** [Markdown risk map with structured diagnostic sections and coaching questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause for user input at WAIT points in coach mode; final output can include a moat audit, early warnings, cascade map, intervention window, and actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
