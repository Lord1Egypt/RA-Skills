## Description: <br>
Babata Browser provides lightweight Python browser automation with CloakBrowser anti-detection and Playwright fallback for JavaScript-rendered pages, form interactions, screenshots, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meta-evo-creator](https://clawhub.ai/user/meta-evo-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate interactive browser workflows on JavaScript-rendered pages, including navigation, form filling, text and link extraction, table extraction, scrolling, JavaScript execution, and screenshot capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anti-detection browser automation can be used in ways that conflict with site rules or protective controls. <br>
Mitigation: Install and run the skill only when this level of automation is intentional and authorized for the target sites; prefer the Playwright backend for normal browsing. <br>
Risk: Broad page-control features can run JavaScript, submit forms, and capture screenshots that may include sensitive information. <br>
Mitigation: Review JavaScript and form-submission tasks before execution, avoid real credentials on untrusted pages, and check page content before capturing screenshots. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/meta-evo-creator/babata-browser) <br>
- [Publisher Profile](https://clawhub.ai/user/meta-evo-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance, Python return dictionaries, CLI JSON, and screenshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create full-page screenshot files; page text and HTML extraction are capped by the implementation.] <br>

## Skill Version(s): <br>
3.1.0 (source: SKILL.md frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
