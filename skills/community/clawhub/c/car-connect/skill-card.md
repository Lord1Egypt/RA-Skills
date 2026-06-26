## Description: <br>
Car Connect helps agents check and control supported connected vehicles across Tesla, Mercedes, Volkswagen, Toyota, Ford, Kia, and Honda from a terminal using brand-specific Python integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deadlybutsoft](https://clawhub.ai/user/deadlybutsoft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect vehicle status and issue remote connected-vehicle commands such as lock, climate, charge, fuel, location, tyres, trunk, windows, horn, flash, and engine actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connected-vehicle account access and can issue remote vehicle-control commands. <br>
Mitigation: Install only if the publisher is trusted with connected-vehicle account access and review commands before execution. <br>
Risk: Some Mercedes and Volkswagen operations may return fake successful vehicle results instead of real vehicle actions. <br>
Mitigation: Do not rely on Mercedes or Volkswagen success responses as proof of vehicle state or operation; verify results independently. <br>
Risk: Commands using --yes can affect doors, windows, trunk, horn, lights, charging, climate, engine, or other vehicle behavior. <br>
Mitigation: Verify the target brand and car before any --yes command and avoid running control commands unattended. <br>
Risk: Location output and cached authentication state can expose sensitive personal or vehicle data. <br>
Mitigation: Treat location output as sensitive, avoid sharing logs, and remove ~/.car_connect to clear cached auth state when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/deadlybutsoft/car-connect) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON CLI output, with Markdown setup and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses brand-specific environment variables and local cached auth state under ~/.car_connect.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
