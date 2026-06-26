## Description: <br>
Find nearby BnB stays. Invoke when user asks for BnB stays near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users invoke this skill when they want nearby BnB, short-term rental, or guesthouse options based on an authorized location or city. It standardizes lodging search inputs, result fields, and common error handling for agent responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location-based lodging searches can expose sensitive precise-location information. <br>
Mitigation: Use the skill only with user-authorized location data, prefer approximate location when exact coordinates are unnecessary, and avoid retaining precise coordinates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/bnb-stays) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown or structured text describing nearby lodging results and errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses location, radius, limit, and optional filters; results should avoid retaining precise coordinates unless needed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
