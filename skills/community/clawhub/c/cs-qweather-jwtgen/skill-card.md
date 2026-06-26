## Description: <br>
Generates and refreshes QWeather API JWT authentication tokens using a local Ed25519 private key and QWeather account identifiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[savior1987](https://clawhub.ai/user/savior1987) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate a QWeather JWT for API authentication and save it for related QWeather automation scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private keys, QWeather identifiers, and generated JWTs are sensitive credentials that can grant API access if exposed. <br>
Mitigation: Keep ~/.myjwtkey/ed25519-private.pem and ~/.myjwtkey/last-token.dat private, avoid sharing terminal output because it includes the full JWT, and use a trusted Python environment for PyJWT. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/savior1987/cs-qweather-jwtgen) <br>
- [Publisher profile](https://clawhub.ai/user/savior1987) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Console text plus a local token file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prints the JWT to stdout and writes it to ~/.myjwtkey/last-token.dat with restricted file permissions.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
