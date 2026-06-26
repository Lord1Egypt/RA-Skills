## Description: <br>
A tool for downloading and configuring Android SDKs for projects, supporting Windows and macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-smith-max](https://clawhub.ai/user/noah-smith-max) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to detect Android and Flutter project dependencies, download missing SDK tooling, configure project environments, and build supported mobile projects on Windows or macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs an unverified external executable. <br>
Mitigation: Use only in a disposable or well-contained development environment and independently verify the GitHub release binary before execution. <br>
Risk: The wrapper forwards arguments through an unsafe shell command. <br>
Mitigation: Avoid passing untrusted project paths or arguments until subprocess execution is made safe. <br>
Risk: The release does not provide a declared license. <br>
Mitigation: Confirm license and terms of use with the publisher before commercial deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/noah-smith-max/android-build) <br>
- [Windows pi Release Binary](https://github.com/noah-smith-max/pi_public/releases/download/r0.0.1/pi.exe) <br>
- [macOS pi Release Binary](https://github.com/noah-smith-max/pi_public/releases/download/r0.0.1/pi) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download and execute platform-specific external binaries for Windows or macOS.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
