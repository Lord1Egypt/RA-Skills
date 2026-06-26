## Description: <br>
Fn Fpk helps developers build and package third-party fnOS FPK applications for Feiniu NAS, covering native and Docker app structure, manifests, permissions, lifecycle scripts, runtime services, packaging, testing, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dalingo81](https://clawhub.ai/user/dalingo81) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, configure, package, test, and prepare third-party fnOS FPK applications for Feiniu NAS. It supports both native applications and Docker-based applications with guidance for manifests, permissions, lifecycle scripts, UI entries, middleware, and appcenter-cli installation testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FPK projects created from the guidance can run with significant authority on a NAS, including privileged modes, shared-folder permissions, uninstall-time data deletion, Docker environment variables, and stored passwords. <br>
Mitigation: Review generated FPK projects before installing them, with particular attention to privilege mode, shared-folder access, uninstall behavior, Docker environment variables, and any stored credentials. <br>


## Reference(s): <br>
- [ClawHub Fn Fpk release page](https://clawhub.ai/dalingo81/fn-fpk) <br>
- [fnOS developer documentation](https://developer.fnnas.com) <br>
- [fnpack 1.2.1 download pattern](https://static2.fnnas.com/fnpack/fnpack-1.2.1-{os}-{arch}) <br>
- [FNOSP CGI collection](https://github.com/FNOSP/fnosAppCenterCgiCollection) <br>
- [fnpack icon package](https://static.fnnas.com/appcenter-marketing/fnpack_ICON_256.zip) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell, JSON, INI, YAML, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated FPK projects should be reviewed before installation on a NAS.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release evidence, changelog dated 2026-06-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
