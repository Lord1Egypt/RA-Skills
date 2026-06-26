## Description: <br>
Applies a citation-diversifier budget report by injecting in-scope citations into an existing draft without adding new facts, helping the draft meet a global unique-citation target while avoiding citation dumps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research-writing agents use this skill to update an existing Markdown draft from a citation budget report, adding only allowed citation keys in the relevant subsection and producing a citation injection report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary states that the citation-editing script can add citations outside the stated section scope. <br>
Mitigation: Review the diff for output/DRAFT.md and confirm every added citation is allowed for that subsection before accepting the result. <br>
Risk: The security summary states that the package includes broader research-pipeline tooling than its narrow description suggests. <br>
Mitigation: Review the bundled files and run only the citation-injection workflow needed for the current workspace. <br>
Risk: The automated PASS report may not be sufficient evidence that the citation edits are appropriate. <br>
Mitigation: Check output/DRAFT.md and output/CITATION_INJECTION_REPORT.md manually, as recommended by the security guidance. <br>


## Reference(s): <br>
- [Citation Injector release page](https://clawhub.ai/WILLOSCAR/citation-injector) <br>
- [WILLOSCAR publisher profile](https://clawhub.ai/user/WILLOSCAR) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, code, shell commands, guidance] <br>
**Output Format:** [Markdown draft edits and Markdown citation injection report, with optional Python command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional script updates output/DRAFT.md in place and writes output/CITATION_INJECTION_REPORT.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
