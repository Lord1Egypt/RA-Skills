## Description: <br>
Build editable cloud architecture diagrams (Azure/Microsoft, AWS, GCP, Microsoft Fabric) using official vendor icons, output as both .excalidraw and .drawio with icons embedded and labeled arrows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansraj316](https://clawhub.ai/user/hansraj316) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud architects use this skill to turn text descriptions or screenshots into editable architecture diagrams for AWS, Azure/Microsoft, GCP, and Microsoft Fabric. It helps select provider icons, lay out zones and nodes, and produce matching Excalidraw and draw.io files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL-based icons may fetch and embed remote SVG content when icon_url values are supplied. <br>
Mitigation: Prefer bundled provider icons, avoid icon_url values from untrusted sources, and review generated .excalidraw and .drawio files before opening or sharing them. <br>
Risk: Generated architecture diagrams may use an incorrect provider icon or fall back to a labeled box when coverage is partial. <br>
Mitigation: Check the icon-resolution report and preview the rendered diagram before delivering it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hansraj316/cloud-architecture-diagrams) <br>
- [Spec Format & Layout Cookbook](artifact/references/spec-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON diagram specifications plus generated .excalidraw and .drawio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated diagram files embed icons for offline editing and sharing.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
