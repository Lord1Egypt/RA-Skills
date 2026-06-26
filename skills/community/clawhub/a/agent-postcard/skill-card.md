## Description: <br>
Generate and send AI-created postcards featuring an agent persona at real locations in multiple artistic styles through the Turai Postcard API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JPaulGrayson](https://clawhub.ai/user/JPaulGrayson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to let an agent create a location-themed postcard image from either its persona file or an explicit selfie prompt. It supports choosing a destination, art style, optional message, and output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends postcard details and a persona-derived selfie prompt to Turai. <br>
Mitigation: Review SOUL.md or IDENTITY.md before use, or pass --selfie to avoid reading persona text. <br>
Risk: The script requires a Turai API key and writes generated output to disk. <br>
Mitigation: Use an API key intended for this workflow and choose output paths deliberately. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JPaulGrayson/agent-postcard) <br>
- [Turai](https://turai.org) <br>
- [Turai Postcard API endpoint](https://turai.org/api/agent/postcard) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Image files, Guidance] <br>
**Output Format:** [PNG image file or JSON image response, with console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TURAI_API_KEY; may read SOUL.md or IDENTITY.md unless --selfie is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
