## Description: <br>
Search and download ready-to-print 3D model files (STL/3MF/ZIP) for a concept or specific part by querying Printables first. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajmwagar](https://clawhub.ai/user/ajmwagar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and fabrication-oriented agents use this skill to find existing printable models, download model files, and preserve source, license, attribution, file hash, and manifest details for quoting or printing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and extracts public 3D model archives from remote sources without strong local path and file-safety checks. <br>
Mitigation: Use a dedicated output folder, avoid sensitive directories, inspect downloaded files before opening or printing them, and add path containment, file-type, file-size, and safer ZIP extraction checks before routine use. <br>
Risk: Downloaded models may carry licensing or attribution constraints that affect remixing, commercial use, quoting, or printing. <br>
Mitigation: Review the generated manifest and upstream Printables model page before reuse, and preserve license and attribution metadata with the downloaded files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ajmwagar/find-stl) <br>
- [Printables](https://www.printables.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands] <br>
**Output Format:** [Terminal text, optional JSON search results, downloaded STL/3MF/ZIP model files, and manifest.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch output includes source URL, author, license id, downloaded files, SHA-256 hashes, and fetch timestamp when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
