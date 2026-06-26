## Description: <br>
Helps agents search and parse bearing models, brands, specifications, cross-references, and selection guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openfindbearings](https://clawhub.ai/user/openfindbearings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and procurement users can use this skill to answer bearing model, brand, specification, cross-reference, and selection questions. It is intended for lookup and decision support, not as the sole authority for safety-critical engineering choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearing specifications or selection advice may be incomplete or unsuitable for purchasing or safety-critical engineering decisions. <br>
Mitigation: Confirm dimensions, load ratings, speed limits, and application fit against trusted manufacturer documentation before acting. <br>
Risk: The optional Python helper reads local bearing JSON data from a separate data folder. <br>
Mitigation: Use bearing data files from trusted sources and review them before relying on helper output. <br>


## Reference(s): <br>
- [Bearing Brand Reference](references/brands.md) <br>
- [Bearing Data Structure](references/data-structure.md) <br>
- [Bearing Model Code Rules](references/model-codes.md) <br>
- [SKF](https://www.skf.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands] <br>
**Output Format:** [Markdown or plain text, with optional terminal output from the Python helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local bearing JSON data when the optional helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
