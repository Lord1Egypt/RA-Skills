## Description: <br>
Parses EU Digital Tachograph driver card files (.ddd), converts them to JSON, imports the data into SQLite, and exports driving information and violations to CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanwebgit](https://clawhub.ai/user/sanwebgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, fleet operators, and compliance teams use this skill to process EU Digital Tachograph driver card dumps, store parsed records in SQLite, and export activity, vehicle, driver-hours, and violation data for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive driver-card data and produces databases, CSVs, logs, summaries, and archives that may contain driver records. <br>
Mitigation: Store generated outputs only in restricted locations, apply retention controls, and review access before processing real .ddd files. <br>
Risk: The build guide relies on an external parser source. <br>
Mitigation: Pin and verify the external parser source before building or deploying the parser binary. <br>
Risk: Email alerting can send outbound notifications when MAIL_TO is configured. <br>
Mitigation: Leave MAIL_TO unset unless outbound alerts have been approved for the deployment environment. <br>
Risk: Unsafe filename handling is identified in the security evidence. <br>
Mitigation: Use only trusted .ddd filenames and isolate the inbox used for tachograph file processing. <br>


## Reference(s): <br>
- [Build guide](references/build.md) <br>
- [Certificate details](references/certificates.md) <br>
- [EU JRC Gen 1 public key certificates](https://dtc.jrc.ec.europa.eu/dtc_public_key_certificates_dt.php.html) <br>
- [EU JRC Gen 2 public key certificates](https://dtc.jrc.ec.europa.eu/dtc_public_key_certificates_st.php.html) <br>
- [External tachograph parser source referenced by the build guide](https://github.com/traconiq/tachoparser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON, SQLite, CSV, log, summary, and archive files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes .ddd driver card files into parsed JSON, a SQLite database, CSV exports, operational logs, summary reports, and archived source files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
