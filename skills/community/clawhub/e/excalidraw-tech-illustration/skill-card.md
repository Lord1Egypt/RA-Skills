## Description: <br>
Generates Excalidraw technical diagrams as editable .excalidraw files and rendered PNG images, selecting from seven diagram styles and organizing outputs into an Excalidraw collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryaction](https://clawhub.ai/user/jerryaction) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to turn technical article content into editable Excalidraw diagrams and PNG images for documentation, architecture explanations, workflows, comparisons, timelines, and state-machine illustrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create diagrams, update collection indexes, and create README files in the project workspace. <br>
Mitigation: Run it only in the intended workspace and review the generated files and index changes before committing or publishing them. <br>
Risk: Rendering uses an external npx Excalidraw CLI command. <br>
Mitigation: Approve package execution only in a trusted environment and review the renderer package source or pinned version when supply-chain controls require it. <br>
Risk: Generated technical diagrams may simplify or misstate the source article. <br>
Mitigation: Review the .excalidraw source and PNG output against the article before using the diagram as authoritative documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryaction/excalidraw-tech-illustration) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Excalidraw JSON files, PNG images, Markdown file references, and rendering commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes diagrams under excalidraw/drafts, excalidraw/output, and excalidraw/collection; updates collection index.json and section README files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
