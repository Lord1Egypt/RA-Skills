## Description: <br>
Analyzes local or downloaded MP4/MOV videos with Volcengine/Kickart services to extract metadata, shot breakdowns, and Seedance-ready outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to upload short product or marketing videos, request cloud analysis, and turn the results into readable shot metadata or Seedance-oriented generation input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud credentials may be exposed if users paste AK/SK secrets into chat or run commands that echo secret values. <br>
Mitigation: Provide credentials through a secure secret mechanism, avoid echoing credential environment variables, and review logging before use. <br>
Risk: Video files and metadata are sent to remote Volcengine/Kickart services for analysis. <br>
Mitigation: Use only media approved for that remote processing path and avoid private or sensitive video unless the service terms and account controls are acceptable. <br>
Risk: Security evidence flags account-affecting and under-disclosed backend actions. <br>
Mitigation: Review or patch package-registration behavior before using the skill with real accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-kickart-video-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/volcengine-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces original analysis JSON and Seedance-formatted JSON; requires cloud credentials and sends video files or metadata to remote Volcengine/Kickart services.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
