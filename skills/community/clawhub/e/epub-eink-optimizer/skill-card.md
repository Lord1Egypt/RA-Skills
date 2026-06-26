## Description: <br>
Optimizes EPUB files for e-ink readers by deduplicating images, removing tiny decorative images, resizing oversized images, and recompressing JPEGs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangkf](https://clawhub.ai/user/wangkf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, ebook maintainers, and developers use this skill to reduce EPUB file size for Kindle, Kobo, Boox, and other e-ink devices while preserving readability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optimizer can permanently change the selected EPUB file. <br>
Mitigation: Use the skill on a copy or keep a backup, and run the bundled script with --dry-run before applying changes. <br>
Risk: The optimizer depends on Pillow for image processing. <br>
Mitigation: Install Pillow from a trusted source in an isolated Python environment when possible. <br>


## Reference(s): <br>
- [Manual fixes guide](references/manual-fixes.md) <br>
- [ClawHub skill page](https://clawhub.ai/wangkf/epub-eink-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose dry-run checks and local EPUB file modifications through the bundled optimizer script.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
