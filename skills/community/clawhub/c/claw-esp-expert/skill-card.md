## Description: <br>
Claw ESP Expert helps agents inspect ESP-IDF environments, navigate examples, audit GPIO usage, and diagnose builds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MoveCall](https://clawhub.ai/user/MoveCall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to work with ESP-IDF projects by checking the local toolchain, finding examples, auditing pin usage, diagnosing build failures, decoding panic logs, and optionally running flash/monitor workflows against connected hardware. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Build and flash workflows can change connected ESP devices or execute local ESP-IDF tooling. <br>
Mitigation: Use flash_and_monitor and execute_project only when the user explicitly wants device interaction, and confirm the target project, chip, and port before running them. <br>
Risk: Component lookup can suggest dependency changes from online registry data. <br>
Mitigation: Review registry suggestions and generated manifest snippets before adding dependencies to a project. <br>
Risk: Project inspection can expose local ESP project contents. <br>
Mitigation: Point the skill only at relevant ESP-IDF project directories and avoid unrelated private directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MoveCall/claw-esp-expert) <br>
- [ESP Component Registry](https://components.espressif.com) <br>
- [ESP-IDF repository](https://github.com/espressif/esp-idf.git) <br>
- [ESP-IDF Gitee mirror](https://gitee.com/EspressifSystems/esp-idf.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, structured JSON-style tool results, shell commands, and patch-style before/after suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include diagnostics, command suggestions, dependency snippets, partition-table drafts, decoded panic locations, and flash/monitor summaries.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
