## Description: <br>
Book Infographic helps agents parse PDF books, extract core concepts and chapter summaries, and produce editable HTML or Markdown infographics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luemery](https://clawhub.ai/user/luemery) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content teams use this skill to turn a supplied PDF book into structured summaries, concept maps, chapter overviews, and editable infographic files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF contents may be extracted into local JSON or HTML output files. <br>
Mitigation: Use controlled output paths, avoid confidential PDFs unless appropriate, and delete generated files when they are no longer needed. <br>
Risk: Generated HTML may load ECharts from a third-party CDN. <br>
Mitigation: For sensitive or offline use, replace the CDN script with a local pinned ECharts copy before opening the generated HTML. <br>


## Reference(s): <br>
- [Infographic editing guide](references/infographic-guide.md) <br>
- [Book Infographic ClawHub page](https://clawhub.ai/luemery/book-infographic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON extraction data plus editable HTML or Markdown infographic content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON and HTML output files from user-provided PDFs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
