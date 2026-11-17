## Description:

Read Android device logs in real time via adb logcat using C++ or Python backends with generator-style streaming output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and Android engineers use this skill for guidance on reading live device logs from the pywayne.adb.logcat_reader module, including backend selection and streaming log handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Android logcat output may contain app identifiers, URLs, debug messages, stack traces, or secrets.

Mitigation: Avoid unnecessary persistence, redact sensitive log lines before sharing, and review captured logs before using them outside the local debugging context.

Risk: The artifact states that logs are cleared automatically when the reader stops, but server security guidance says not to rely on that behavior without verification.

Mitigation: Verify the underlying library behavior before assuming logs are cleared, and handle stop and cleanup steps explicitly in operational guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyendt/skills/adb-logcat-reader)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands]

**Output Format:** [Markdown with Python examples and adb-related command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generator-style streaming log lines; users may choose the C++ or Python backend.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
