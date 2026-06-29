## Description: <br>
Organizes 3D-printing filament order screenshots into a reviewable inventory table and a local single-file HTML tracker with interactive in-use and consumed counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heavenchenggong](https://clawhub.ai/user/heavenchenggong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
3D-printing users and agent operators use this skill to turn filament purchase screenshots into a corrected inventory list, then generate a browser-based tracker for current stock, in-use rolls, consumed rolls, and JSON backup/restore. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Order screenshots may include shopping details or other personal information unrelated to filament inventory. <br>
Mitigation: Provide only relevant 3D-filament screenshots, review the Markdown extraction table before HTML generation, and delete copied screenshots when no longer needed. <br>
Risk: Tracker state is stored locally in browser localStorage and can become unavailable after moving the HTML file, changing browsers, or clearing browser data. <br>
Mitigation: Export a JSON backup after updating tracker state, import that backup after moving the file or changing browsers, and remove exported JSON or local browser state when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heavenchenggong/3d-filament-tracker) <br>
- [Artifact README](artifact/README.md) <br>
- [HTML tracker template](artifact/templates/template.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, JSON, Guidance] <br>
**Output Format:** [Markdown review table followed by a generated single-file HTML tracker and JSON state export/import guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated tracker runs locally in a browser, persists state in localStorage, and supports JSON export/import for backup or file moves.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
