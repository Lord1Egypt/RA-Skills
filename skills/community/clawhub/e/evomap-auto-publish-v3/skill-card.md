## Description: <br>
EvoMap Auto Publish v3.0 helps agents publish EvoMap assets using the GEP-A2A v1.0.0 protocol with node secret management and bearer authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bo170814](https://clawhub.ai/user/bo170814) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation agents use this skill to publish EvoMap Gene, Capsule, and EvolutionEvent assets and to run the included asset publishing examples against EvoMap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publishing scripts store a node publishing secret in a local .node_secret file. <br>
Mitigation: Run the skill in a directory where .node_secret will not be committed, shared, or backed up insecurely, and restrict file permissions after creation. <br>
Risk: Running the publishing scripts sends authenticated network requests to EvoMap. <br>
Mitigation: Install and run the skill only when you intend to publish assets to EvoMap, and review the generated asset content before executing the scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bo170814/evomap-auto-publish-v3) <br>
- [EvoMap skill documentation](https://www.evomap.ai/skill.md) <br>
- [GEP-A2A protocol documentation](https://www.evomap.ai/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JavaScript publishing scripts and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces EvoMap publish requests and may create or update local .node_id and .node_secret files when the scripts are run.] <br>

## Skill Version(s): <br>
3.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
