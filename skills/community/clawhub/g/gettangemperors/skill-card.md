## Description: <br>
Query a local backend API for Tang Dynasty emperor information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzlpypy](https://clawhub.ai/user/hzlpypy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query a trusted local service for information about the first three Tang Dynasty emperors and return either formatted text or raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill prints whatever JSON the local backend returns. <br>
Mitigation: Use it only with a trusted service on 127.0.0.1:8080 and review returned content before relying on it. <br>
Risk: The client depends on a local backend, python3, and the requests package. <br>
Mitigation: Confirm the backend is expected to be running and dependencies are installed before invoking the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hzlpypy/gettangemperors) <br>
- [Local Tang Emperors API endpoint](http://127.0.0.1:8080/api/v1/test) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code, guidance] <br>
**Output Format:** [Plain text or JSON from a localhost API client, with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests dependency, and a trusted local backend on 127.0.0.1:8080.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
