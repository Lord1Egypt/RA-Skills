## Description: <br>
Generates aliases for Chinese company names in Excel workbooks, prioritizing listed-company short names, preserving government organization names, filtering generic or regional terms, and supplementing aliases through web lookup behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyqdq888](https://clawhub.ai/user/hyqdq888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data operations teams use this skill to standardize Chinese company names for entity matching, fuzzy search, and spreadsheet data-cleaning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet company names may be sent to Baidu during alias generation. <br>
Mitigation: Use only non-sensitive company lists, or disable the lookup path and require explicit opt-in before any external query is made. <br>
Risk: The script depends on an absolute external import path that is not bundled with the release artifact. <br>
Mitigation: Bundle the dependency or replace the absolute import with a declared, reviewable module before deployment. <br>
Risk: The published documentation describes web lookup as optional or disabled, while the artifact behavior can still invoke it. <br>
Mitigation: Align documentation and runtime behavior so operators can reliably understand when network access occurs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hyqdq888/company-alias-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Excel .xlsx workbook with a generated alias column, pipe-delimited alias strings, and command-line progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and the openpyxl and requests packages; the bundled script may invoke curl for Baidu lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, artifact frontmatter, and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
