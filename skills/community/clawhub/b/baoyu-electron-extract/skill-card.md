## Description: <br>
Extracts resources and JavaScript from installed Electron app .asar bundles, restoring original sources from embedded source maps when available or formatting bundled code otherwise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect installed Electron desktop applications, unpack app.asar resources, and recover readable JavaScript or original source files when source maps include sourcesContent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted Electron app output can include proprietary code, configuration, or secrets. <br>
Mitigation: Treat extracted directories and reports as sensitive, review before sharing, and store them only in appropriate local work locations. <br>
Risk: Ambiguous app discovery or forced reuse of an existing output directory can inspect or overwrite unintended files. <br>
Mitigation: Run with --dry-run when the target is uncertain, confirm the resolved app or asar path, and use --force only when intentionally reusing an existing output folder. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jimliu/baoyu-electron-extract) <br>
- [Publisher Profile](https://clawhub.ai/user/jimliu) <br>
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-electron-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and paths to extracted files, plus optional JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The extraction script can create an extract-report.json file, extracted and restored source directories, and copied unpacked resources when present.] <br>

## Skill Version(s): <br>
1.119.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
