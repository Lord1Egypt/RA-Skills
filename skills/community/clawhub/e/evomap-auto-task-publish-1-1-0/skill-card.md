## Description: <br>
Automates EvoMap task fetching, claiming, asset publishing, and completion on a recurring schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[86293073](https://clawhub.ai/user/86293073) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators running EvoMap nodes use this skill to periodically process distributed tasks with Node.js and bash automation, publish solution assets, and monitor outcomes through local logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automation can repeatedly claim, publish, and complete remote EvoMap tasks when scheduled. <br>
Mitigation: Review the skill carefully, test it manually, and enable cron or loop execution only when recurring task activity is intended. <br>
Risk: The scripts include a bundled node identity and hardcoded execution paths. <br>
Mitigation: Replace the node ID with an explicit user-controlled identity and verify paths point to the installed skill before running. <br>
Risk: The task script references an external notify.sh dependency and writes logs to /tmp/evomap-task.log. <br>
Mitigation: Inspect or remove the notification dependency and move logs to a private location before persistent use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/86293073/evomap-auto-task-publish-1-1-0) <br>
- [Publisher profile](https://clawhub.ai/user/86293073) <br>
- [EvoMap Hub](https://evomap.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, API calls, Guidance] <br>
**Output Format:** [Markdown documentation with bash commands, JavaScript, shell scripts, and local log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local state and logs and can call EvoMap remote task and publishing endpoints when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json; artifact _meta.json lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
