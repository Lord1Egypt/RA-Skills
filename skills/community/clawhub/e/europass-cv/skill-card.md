## Description:

Create or edit a Europass CV in the Candidate XML format that the official europass.europa.eu editor imports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j0ker98](https://clawhub.ai/user/j0ker98)

### License/Terms of Use:

CC-BY-4.0

## Use Case:

External users and developers use this skill to create, convert, repair, validate, and troubleshoot Europass Candidate XML CVs that import correctly into the official Europass editor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real CVs contain personal data, and the optional importer check sends the file to the Europass European Commission service.

Mitigation: Use local build, extraction, and schema validation paths when possible; run the remote importer check on a real CV only with the person's consent or with fictional data.

Risk: The Europass Candidate XML schema is unofficial and derived from exports, editor behavior, and importer responses.

Mitigation: Validate generated XML with the included schema and, when consent allows, check the result against the real importer before relying on it.

Risk: Incorrect or invented CV details could produce misleading professional records.

Mitigation: Collect CV data from the person, keep provided values as given, and avoid inventing missing personal, employment, education, or qualification details.

## Reference(s):

- [Server-resolved source repository](https://github.com/J0ker98/europass-cv)
- [ClawHub skill page](https://clawhub.ai/j0ker98/skills/europass-cv)
- [README](README.md)
- [Candidate XML format reference](docs/format.md)
- [CV JSON input reference](docs/cv-json.md)
- [Codifications](docs/codifications.md)
- [How this format was derived](docs/how-it-was-derived.md)
- [Europass](https://europass.europa.eu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with XML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Europass Candidate XML files and validation or importer-check commands; optional importer checks send CV data to Europass only with consent.]

## Skill Version(s):

0.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
