## Description: <br>
克隆龙虾 helps OpenClaw/CatPaw users back up and restore workspace files, configuration, installed skills, system snapshots, and conversation context through a private Git repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiPingjiang](https://clawhub.ai/user/LiPingjiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw/CatPaw users and operators use this skill to maintain private Git backups of agent state and restore selected parts of an agent environment when configuration, workspace files, or installed skills need to be recovered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic backups can upload sensitive agent state, configuration, session data, SSH details, and system information to the configured Git repository. <br>
Mitigation: Use only a private repository you control, review files before pushing, disable automatic or heartbeat backups when not needed, and exclude secrets or session databases unless explicitly required. <br>
Risk: Restore operations can replace local workspace files, configuration, or installed skills with content from the backup repository. <br>
Mitigation: Verify repository contents before restoring, prefer targeted restore modes, and review restored skills and configuration before resuming normal agent use. <br>


## Reference(s): <br>
- [Configuration Guide](references/setup_guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/LiPingjiang/clone-lobster) <br>
- [Meituan Code Repository Setup](https://dev.sankuai.com/code/create-repo) <br>
- [Meituan Code SSH Key Setup](https://dev.sankuai.com/code/home) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead an agent to run Git backup or restore scripts against local OpenClaw/CatPaw state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
