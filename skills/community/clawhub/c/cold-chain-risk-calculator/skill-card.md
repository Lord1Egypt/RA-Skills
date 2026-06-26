## Description: <br>
Calculates cold chain transport risks from route, duration, and packaging inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanruoyu](https://clawhub.ai/user/shanruoyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and external users use this skill to estimate temperature-excursion risk for cold chain transport and compare packaging options for a route and duration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The calculator is a simplified draft and is not validated as an operational or regulatory decision tool. <br>
Mitigation: Review the scoring formula and validate it against cold-chain requirements before relying on it for real shipments. <br>
Risk: The skill runs a local Python script to calculate and print risk estimates. <br>
Mitigation: Run it in a sandboxed workspace and review the script before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shanruoyu/cold-chain-risk-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text risk report with optional Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires route and duration inputs; packaging defaults to dry-ice.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
