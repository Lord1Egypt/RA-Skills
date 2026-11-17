## Description:

Search and download ready-to-print 3D model files (STL/3MF/ZIP) for a concept or specific part by querying Printables (first). Use when an agent needs to find an existing model, capture license/attribution, download the source files, and output a local folder + manifest for quoting/printing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajmwagar](https://clawhub.ai/user/ajmwagar)

### License/Terms of Use:


## Use Case:

Developers, engineers, and agents use this skill to search Printables for existing printable 3D models, download selected STL/3MF/ZIP assets, and preserve attribution, license, file hashes, and source metadata in a local manifest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote filenames or archive contents may write files outside the intended download directory.

Mitigation: Run fetches only in a scratch directory, inspect downloaded archives before reuse, and add filename and path containment checks before normal use.

Risk: Search and fetch requests are sent to Printables.

Mitigation: Avoid submitting sensitive, proprietary, or private model concepts in search queries.

Risk: Downloaded 3D model files may carry license or attribution obligations.

Mitigation: Review the generated manifest and source model page before printing, quoting, redistributing, or using files commercially.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajmwagar/skills/find-stl)
- [Printables](https://www.printables.com)
- [scripts/find_stl.py](artifact/scripts/find_stl.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, local downloaded files, and JSON manifest output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch operations write model files and manifest.json to a local output directory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
