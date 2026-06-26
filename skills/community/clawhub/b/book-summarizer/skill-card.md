## Description: <br>
Use this skill when the user wants a long-form book summarized in the user's preferred language at an explicitly verified 20 percent compression ratio, with the result rejected if it falls outside the allowed range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyxyz22](https://clawhub.ai/user/dannyxyz22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to produce substantial, language-matched summaries of long plain-text books while checking that the final summary stays within an 18 to 22 percent compression range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent reads the selected book file and may create local batch and summary files. <br>
Mitigation: Use a dedicated working folder for sensitive texts and delete intermediate batch files after use. <br>
Risk: Large books may consume many tokens because summarization can run across multiple batches until the target compression ratio is met. <br>
Mitigation: Estimate batches before summarization and validate the final summary ratio before accepting the output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dannyxyz22/book-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown summaries with optional local shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces batch files and aggregated summary files when the workflow uses the packaged local helpers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
