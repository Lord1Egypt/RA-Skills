## Description: <br>
Provides a checklist for upgrading EmpireCMS 7.5 sites to PHP 8 compatibility, including common fatal errors, deprecated PHP APIs, encoding considerations, and validation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ebandao777-oss](https://clawhub.ai/user/ebandao777-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site maintainers use this skill to plan and review an EmpireCMS 7.5 migration to PHP 8. It guides fixes for fatal errors, deprecated PHP APIs, database extension changes, GBK handling, and post-upgrade testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying broad PHP 8 migration changes mechanically can break an existing EmpireCMS site. <br>
Mitigation: Back up the site, test changes in staging, and review each source-code change before deploying to production. <br>
Risk: The skill provides migration guidance but does not verify the target CMS codebase or runtime behavior. <br>
Mitigation: Run full PHP error reporting and test admin login, content publishing, front-end pages, search, comments, member flows, email, FTP, ZIP, and template rendering after changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ebandao777-oss/empirecms7-php8-upgrade) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline PHP and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes migration checklist items, code snippets, search patterns, and validation steps; outputs should be reviewed before changing a live CMS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
