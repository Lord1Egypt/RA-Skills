## Description: <br>
Provides a workflow for downloading public Chinese A-share annual report PDFs from cninfo.com.cn and extracting structured financial statement data for validation and batch analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shihugh5-lab](https://clawhub.ai/user/shihugh5-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data engineers use this skill to collect public Chinese A-share annual reports and convert supported financial statement tables into structured data for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may send PDF text summaries to OpenAI when locating financial statement pages. <br>
Mitigation: Use public annual reports or documents approved for external processing, and provide an OpenAI API key only when that data handling is acceptable. <br>
Risk: The release is described as markdown workflow guidance; separately obtained runnable scripts may not be covered by the same evidence. <br>
Mitigation: Inspect and scan any implementation scripts before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shihugh5-lab/financial-data-gateway) <br>
- [cninfo announcement search API](http://www.cninfo.com.cn/new/hisAnnouncement/query) <br>
- [cninfo company search API](http://www.cninfo.com.cn/new/information/topSearch/query) <br>
- [cninfo static PDF download endpoint](https://static.cninfo.com.cn/{adjunctUrl}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with command snippets and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PDF file paths for report downloads and structured JSON examples for extracted financial statements.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
