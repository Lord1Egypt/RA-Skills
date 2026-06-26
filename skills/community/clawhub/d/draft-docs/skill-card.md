## Description: <br>
Generate first-draft technical documentation from code analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to generate draft Tutorial, How-To, Reference, or Explanation documentation from project code and existing documentation context before human review and publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated drafts may contain incorrect or incomplete documentation if code analysis misses relevant project behavior. <br>
Mitigation: Review each draft for accuracy before publishing, and keep the documented draft review gate in place. <br>
Risk: Publishing mode can move documentation files and update navigation. <br>
Mitigation: Require an explicit destination, avoid overwriting files without approval, and run the documented post-publish verification before treating the document as live. <br>


## Reference(s): <br>
- [Diataxis](https://diataxis.fr/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown documentation drafts with inline shell commands and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes draft documentation to docs/drafts/ for review before publishing.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
