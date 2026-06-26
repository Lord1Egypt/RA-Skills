## Description: <br>
Read Android device logs in real time via adb logcat using a C++ or Python backend with generator-style streaming output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to work with the pywayne.adb.logcat_reader module for real-time Android log monitoring, debugging, filtering, parsing, or storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Captured Android logs can contain tokens, identifiers, crash details, or user data. <br>
Mitigation: Inspect logs only from devices and apps you are authorized to debug, and redact sensitive values before sharing or storing output. <br>
Risk: Reader stop or cleanup behavior may affect captured log output or the device log buffer. <br>
Mitigation: Confirm the reader behavior in your environment before relying on it for evidence preservation or log retention workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/adb-logcat-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown with Python code examples and concise usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents toward streaming Android log lines; raw logs should be handled as potentially sensitive.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
