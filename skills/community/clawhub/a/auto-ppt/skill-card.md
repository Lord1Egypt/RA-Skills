## Description: <br>
Generates polished presentation decks by using Google NotebookLM to turn user-provided content, optional YouTube sources, and style guidance into PDF slides, with optional PDF merging, duplicate-page cleanup, and PPTX export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to create NotebookLM-based presentation PDFs from a topic, draft, or multipart research outline. It is also intended for workflows that gather YouTube sources, generate several deck sections, merge the resulting PDFs, and optionally export a cleaned PPTX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the user's logged-in NotebookLM browser session and send presentation content or optional YouTube queries to external services. <br>
Mitigation: Use it only with content that may be shared with those services, and review NotebookLM account/session state before running the workflow. <br>
Risk: The post-processing workflow can process every PDF on the user's Desktop when run with --all-desktop. <br>
Mitigation: Prefer explicit PDF filenames for merge and cleanup, or use --all-desktop only after moving unrelated Desktop PDFs elsewhere. <br>
Risk: Generated and cleaned outputs are written to Desktop and may overwrite or sit alongside similarly named presentation files. <br>
Mitigation: Choose specific output names and review the generated PDF or PPTX before sharing or using it as final material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kelcey2023/auto-ppt) <br>
- [Deep-research multipart workflow](artifact/references/deep-research-multipart-workflow.md) <br>
- [Google NotebookLM](https://notebooklm.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated PDF or PPTX files on Desktop] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can add YouTube links as NotebookLM sources, generate one or more PDFs, merge Desktop PDFs, remove similar pages with a heuristic, and export a cleaned PPTX.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
