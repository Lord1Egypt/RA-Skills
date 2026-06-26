## Description: <br>
Generates in-depth weekly AI and computer-vision reports by aggregating data from multiple sources with a plugin-based pipeline and multi-channel delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llx9826](https://clawhub.ai/user/llx9826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Host AI agents and developers use this skill to plan AI and computer-vision briefings, fetch and deduplicate source material, and render completed reports. It can also run as a standalone report-generation pipeline when configured with an LLM provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external-skill proxy can execute configured Python modules and functions under the agent's privileges. <br>
Mitigation: Enable only trusted sources, avoid untrusted skill_proxy module or function names, and run the skill with least-privilege filesystem and credential access. <br>
Risk: Standalone mode may send prompts, profile preferences, and fetched report material to the configured LLM provider. <br>
Mitigation: Review the configured LLM provider and avoid using sensitive prompts, user profiles, or source material unless that data handling is acceptable. <br>
Risk: Rendered reports are saved locally. <br>
Mitigation: Use a controlled output directory and review local file permissions and retention for generated HTML, PDF, PNG, Markdown, and JSON reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/llx9826/ai-cv-weekly) <br>
- [README](artifact/README.md) <br>
- [Host AI skill guide](artifact/clawcat_skill/SKILL.md) <br>
- [Adapter registry](artifact/clawcat/adapters/registry.json) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration instructions, JSON, Markdown, Files, Text] <br>
**Output Format:** [JSON dictionaries plus rendered report files in HTML, PDF, PNG, Markdown, and JSON formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PDF and PNG export depend on Playwright and a local Chromium or Chrome runtime.] <br>

## Skill Version(s): <br>
7.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
