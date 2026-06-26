## Description: <br>
Generates a structured HTML morning brief for futures and ferrous-industry news from SteelX2 or a user-provided page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lirenming](https://clawhub.ai/user/lirenming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Futures researchers, ferrous-industry analysts, market teams, and financial news editors use this skill to turn a source page into a daily HTML brief with an overview, key highlights, a market table, macro news, and industry news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches SteelX2 or a user-provided URL and creates an HTML report on the user's Desktop. <br>
Mitigation: Use trusted source URLs, review the generated file path and contents, and avoid opening or sharing unexpected HTML output. <br>
Risk: The generated report omits source attribution by design. <br>
Mitigation: Confirm content rights and add any attribution required by the source before external distribution. <br>
Risk: The bundled HTML template contains remote image and link references. <br>
Mitigation: Review the generated HTML before sharing and consider removing or replacing remote references for sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lirenming/futures-morning-brief) <br>
- [Publisher profile](https://clawhub.ai/user/lirenming) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [HTML output format](artifact/references/output-format.md) <br>
- [Default SteelX2 source](https://www.steelx2.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [HTML file with supporting validation screenshot guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves the generated report to the user's Desktop and opens it for screenshot verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
