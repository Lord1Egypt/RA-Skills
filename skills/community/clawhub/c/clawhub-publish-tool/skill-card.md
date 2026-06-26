## Description: <br>
ClawHub发布工具 helps publish a local skill directory to ClawHub with slug, display name, version, path, and changelog inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhaichao87](https://clawhub.ai/user/wuhaichao87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to package and publish local ClawHub skills from a command line or Python call. It is intended for release workflows that need explicit slug, name, version, path, and changelog parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a bundled publishing credential. <br>
Mitigation: Remove and rotate the exposed token, and require users to authenticate with their own credential before publishing. <br>
Risk: The release evidence reports that uploaded local files are under-explained. <br>
Mitigation: Document the exact file extensions and paths uploaded, and inspect the target directory for secrets or proprietary content before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuhaichao87/clawhub-publish-tool) <br>
- [Publisher profile](https://clawhub.ai/user/wuhaichao87) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, API calls] <br>
**Output Format:** [CLI status text, Markdown usage examples, and Python dictionary results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes selected local skill files and returns success or error status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
