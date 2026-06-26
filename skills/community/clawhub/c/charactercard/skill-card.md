## Description: <br>
Imports, parses, validates, converts, and exports SillyTavern character cards across V1, V2, and V3 formats, including PNG cards with embedded JSON and standalone JSON files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FanYin1](https://clawhub.ai/user/FanYin1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect, validate, convert, and export SillyTavern character-card files. It is intended for workflows that need V1, V2, or V3 character-card data handled as PNG-embedded JSON or standalone JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Character-card content can contain untrusted prompt text or unexpected fields. <br>
Mitigation: Treat imported card text as untrusted data and review parsed content before using it in another agent or chat workflow. <br>
Risk: The skill reads user-provided file paths and can write exported card files. <br>
Mitigation: Use explicit card file paths, avoid unrelated private files, and confirm output paths before export to prevent accidental disclosure or overwrite. <br>
Risk: Large PNG or JSON character-card payloads may be slow or impractical to process. <br>
Mitigation: Prefer reasonably sized card files and validate size limits before conversion or export. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FanYin1/charactercard) <br>
- [SillyTavern documentation](https://docs.sillytavern.app/) <br>
- [Character Card Spec V2](https://github.com/malfoyslastname/character-card-spec-v2) <br>
- [PNG file structure specification](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown responses with parsed character-card summaries, validation findings, JSON snippets, and file paths for exported PNG or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read user-selected PNG or JSON files and write converted character-card files when the user confirms the target path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
