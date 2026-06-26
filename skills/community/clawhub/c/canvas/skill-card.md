## Description: <br>
Display and control HTML content on connected Mac, iOS, or Android OpenClaw nodes through a web-based canvas with live reload and remote actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lura2](https://clawhub.ai/user/lura2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to present, navigate, hide, evaluate JavaScript in, and snapshot HTML canvas content on connected device nodes. It is suited for displaying generated HTML, dashboards, games, visualizations, and interactive demos on Mac, iOS, or Android nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Canvas actions can display or control content on connected OpenClaw nodes, including remote nodes. <br>
Mitigation: Confirm the target node and URL before presenting, navigating, hiding, evaluating JavaScript, or taking snapshots. <br>
Risk: The canvas host serves files from a configurable local root and can bind beyond loopback. <br>
Mitigation: Keep the canvas root limited to non-sensitive display files and use the narrowest bind mode that works for the intended nodes. <br>
Risk: JavaScript evaluation and snapshots can expose private data or run untrusted behavior in the canvas. <br>
Mitigation: Run eval only with trusted JavaScript and avoid snapshotting canvases that show secrets or private information. <br>


## Reference(s): <br>
- [ClawHub Canvas skill page](https://clawhub.ai/lura2/canvas) <br>
- [Publisher profile: lura2](https://clawhub.ai/user/lura2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and action syntax] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides canvas presentation, navigation, JavaScript evaluation, screenshots, live reload, bind modes, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
