## Description: <br>
Automates CNKI advanced-search workflows for CSSCI journal papers, including keyword expansion, citation-count sorting, abstract view, and Word export of citation-format records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yipng05-max](https://clawhub.ai/user/yipng05-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and research-support staff use this skill to run repeatable CNKI advanced searches for CSSCI journal papers and export bibliographic records with abstracts for review or literature mapping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates CNKI in a browser and sends user-provided search keywords to CNKI. <br>
Mitigation: Confirm the keyword expansion and search scope before running the browser workflow. <br>
Risk: The skill saves exported research files locally and may generate a spreadsheet fallback when CNKI export is unavailable. <br>
Mitigation: Review the export count, output path, and fallback format before relying on or sharing generated files. <br>


## Reference(s): <br>
- [CNKI Advanced Search](https://kns.cnki.net/kns8s/AdvSearch) <br>
- [ClawHub skill page](https://clawhub.ai/yipng05-max/cnki-advanced-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, guidance] <br>
**Output Format:** [Progress updates and exported Word or spreadsheet files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports are saved locally under Downloads when CNKI export succeeds; a spreadsheet fallback may be generated if export is blocked.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
