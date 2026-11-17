## Description:

Parses EU Digital Tachograph driver card (.ddd) files, converts them to JSON, imports records into SQLite, and exports driving activity data to CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanwebgit](https://clawhub.ai/user/sanwebgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and fleet or compliance operators use this skill to process EU tachograph driver-card dumps into JSON, SQLite tables, CSV exports, and health reports for driver hours, violations, and vehicle usage analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted filenames can trigger code execution in the current workflow.

Mitigation: Restrict accepted filenames, fix the python3 -c validation pattern before use, and run the workflow under a dedicated low-privilege account.

Risk: The SQLite database and CSV exports contain sensitive driver and vehicle records.

Mitigation: Keep the data directory private, restrict filesystem access, and review retention and export handling before deployment.

Risk: The workflow depends on an external parser source built into a local binary.

Mitigation: Pin and verify the external parser source before building or installing the parser binary.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sanwebgit/skills/driver-card-tachograph)
- [Build Guide](references/build.md)
- [Certificate Details](references/certificates.md)
- [tachoparser Repository](https://github.com/traconiq/tachoparser)
- [EU JRC Gen 1 Public Key Certificates](https://dtc.jrc.ec.europa.eu/dtc_public_key_certificates_dt.php.html)
- [EU JRC Gen 2 Public Key Certificates](https://dtc.jrc.ec.europa.eu/dtc_public_key_certificates_st.php.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands, plus generated JSON, SQLite database, CSV exports, logs, and summary reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads .ddd files from data/inbox or a provided file path and writes local runtime data under data/ and summaries/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
