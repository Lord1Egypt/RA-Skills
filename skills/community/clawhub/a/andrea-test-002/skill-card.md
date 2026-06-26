## Description: <br>
AlphaClaw is a SkillHub CLI guide for searching, installing, publishing, and managing Claude Code skills with AK/SK authentication, keyword search, one-command installation and publishing, favorites, and comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iyunya](https://clawhub.ai/user/iyunya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill as a command guide for installing and operating the AlphaClaw CLI to search, install, publish, list, favorite, and comment on SkillHub skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged as suspicious because it points to an unreviewed global npm package and makes official-sounding claims that registry metadata does not corroborate. <br>
Mitigation: Install only after independently verifying that 1688alphaclaw and the ClawHub entry are authentic and operated by the claimed 1688 or AlphaClaw publisher. <br>
Risk: The workflow uses AK/SK credentials and stores authentication material under ~/.alphaclaw/auth.json. <br>
Mitigation: Use least-privileged credentials where possible and protect the local credential file from unintended access. <br>
Risk: Commands such as --force, --yes, custom API URLs, publishing directories, and workspace skill installation can change local files or publish content with reduced prompting. <br>
Mitigation: Review commands, target directories, and API endpoints before execution, especially before publishing or overwriting installed skills. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/iyunya/andrea-test-002) <br>
- [AlphaClaw SkillHub site](https://skill.alphashop.cn/) <br>
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command syntax, installation steps, authentication guidance, configuration paths, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
