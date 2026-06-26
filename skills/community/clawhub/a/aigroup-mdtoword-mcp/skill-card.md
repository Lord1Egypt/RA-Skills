## Description: <br>
Use `aigroup-mdtoword-mcp` to convert Markdown into `.docx`, including Markdown file conversion, generated Markdown conversion, table-to-Markdown preprocessing, formula handling, table handling, and page-layout requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document authors use this skill to convert existing or generated Markdown into Word `.docx` files. It is suited for notes, reports, memos, formula-heavy documents, structured tables, headers, footers, page numbers, and local images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external MCP package on documents selected for conversion. <br>
Mitigation: Install only if the upstream converter and runtime are trusted, and avoid converting sensitive Markdown or local images unless that trust is established. <br>
Risk: Generated `.docx` files may contain formatting assumptions or unintended document content. <br>
Mitigation: Review generated Word files before sharing and check formulas, tables, page layout, headers, footers, and images. <br>


## Reference(s): <br>
- [Markdown to Word MCP Capabilities](references/capabilities.md) <br>
- [ClawHub release page](https://clawhub.ai/jackdark425/aigroup-mdtoword-mcp) <br>
- [Upstream project homepage](https://github.com/jackdark425/aigroup-mdtoword-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool routing, generated `.docx` file paths, and formatting summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke the `aigroup-mdtoword-mcp` MCP server through stdio to produce Word documents from Markdown.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
