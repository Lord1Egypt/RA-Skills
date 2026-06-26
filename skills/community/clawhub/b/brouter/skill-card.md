## Description: <br>
Generate GPX bike routes via brouter.de for a route between two places, optionally using a selected routing profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[si-gr](https://clawhub.ai/user/si-gr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn cycling route requests into downloadable GPX tracks. It is suited for routes where the user can provide or allow derivation of start and destination coordinates and choose a brouter routing profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route endpoints and route details may be sent to brouter.de and retained locally in logs. <br>
Mitigation: Avoid sensitive home, work, or routine routes unless logging is disabled or redacted and users consent to sharing route endpoints with brouter.de. <br>
Risk: The skill can write route output beyond the narrow routes directory expected for generated GPX files. <br>
Mitigation: Run the skill with a confined working directory and restrict output to a fixed routes folder before use in shared or sensitive environments. <br>
Risk: The implementation uses an unsecured HTTP endpoint for brouter requests. <br>
Mitigation: Prefer a secured transport path or review the request environment before using the skill for sensitive route data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/si-gr/brouter) <br>
- [brouter.de routing service](https://brouter.de) <br>
- [brouter.de routing endpoint](http://brouter.de/brouter) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, API calls] <br>
**Output Format:** [JSON-like result object with a GPX file path and attachment metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces GPX files in a routes directory and may include route summary and debug request metadata.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
