## Description: <br>
Convert between JSON, YAML, and TOML formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Formatgate to convert structured content between JSON, YAML, and TOML through a local FastAPI endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Round-trip safety may be overstated for strict semantic preservation or complex TOML. <br>
Mitigation: Check converted output before relying on it in workflows that require exact semantic round trips. <br>
Risk: The conversion server could be exposed beyond the local machine if bound to a public interface. <br>
Mitigation: Keep the FastAPI server bound to localhost unless intentional external exposure has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/formatgate) <br>
- [Publisher profile](https://clawhub.ai/user/mirni) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, YAML, TOML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns converted content with success and error fields from the local conversion endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
