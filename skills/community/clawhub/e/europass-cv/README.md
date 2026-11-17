# europass-cv

Schema, reference, tools and an agent skill for the Europass Candidate XML format, the CV format the europass.europa.eu editor imports and exports.

Documentation, an unofficial XSD, tooling and an agent skill for the
**Europass Candidate** XML format: the CV format that the Europass editor at
[europass.europa.eu](https://europass.europa.eu) has imported and exported
since 2020. The European Commission does not publish this format. This
repository documents it from real exports, from the editor's code and from
the behaviour of its importer, so that any tool can produce CVs that open in
the official editor with every section in place.

```
SKILL.md     agent skill: how to create or edit a Europass CV with the tools below
schema/      XSD for the four namespaces (europass.eu/1.0, hr-xml.org/3, oagis/9, europass_eures.eu/1.0)
docs/        element-by-element reference, codification lists, JSON input, how it was derived
examples/    fictional CVs: minimal.xml, full.xml, cv.json
tools/       build-cv.mjs, extract-xml.mjs, check-import.mjs, validate.sh
```

## Background

The old Europass XML ("SkillsPassport" v3, namespace
`http://europass.cedefop.europa.eu/Europass`, 2013 to 2020) had a published
XSD and a REST API, and most open-source Europass tools still produce it. The
current editor rejects it as an old format. Its replacement is an HR-XML 3
"Candidate" document with Europass and EURES extensions, embedded as
`attachment.xml` in every PDF the editor exports. See
[docs/how-it-was-derived.md](docs/how-it-was-derived.md) for the method and
[docs/format.md](docs/format.md) for the reference.

## Quick start

Build a CV from JSON (no dependencies, Node 20 or later):

```bash
node tools/build-cv.mjs examples/cv.json > cv.xml
```

Validate against the schema (`xmllint`, preinstalled on macOS and most Linux
distributions):

```bash
sh tools/validate.sh cv.xml
```

Ask the real importer what it makes of a file, XML or PDF with the XML
embedded. This sends the file to a European Commission server: use it with
fictional data or with the person's consent.

```bash
node tools/check-import.mjs cv.xml
node tools/check-import.mjs my-europass.pdf --json
```

Extract the XML from a PDF exported by the editor, to edit it:

```bash
node tools/extract-xml.mjs my-europass.pdf > cv.xml
```

## Import rules the schema cannot express

1. **Sections are displayed only if listed in `RenderingInformation/Design/SectionsOrder`.**
   Without that list the importer reads everything and the editor shows only
   the personal information. Titles: `work-experience`, `education-training`,
   `language`, `profile-skills`, `driving-licence`, `publication`, ...
2. **A telephone without `CountryDialing`, or an impossible date such as
   `1990-02-31`, makes the importer reject the whole file.**
3. **Social media types are a closed list** (facebook, twitter, instagram,
   linkedin, youtube, pinterest, tumblr). Other links use `ChannelCode Web`.
4. **Of a custom section (`Others`) with several `Other` entries the importer
   keeps only the last.** Write one `Others` per entry with the same `Title`;
   the importer merges them. Every entry needs a non-blank `Title`.
5. **Unknown elements are ignored** and child order is not enforced, which is
   why the schema uses repeatable choices where real exports differ.

Full reference: [docs/format.md](docs/format.md). Closed value lists:
[docs/codifications.md](docs/codifications.md).

## Use as an agent skill

[SKILL.md](SKILL.md) follows the Agent Skills format. Point an agent at this
repository (or install it with a skills manager) and it can create a CV from
collected data, edit an existing Europass PDF or XML, validate the result and
check it against the importer, following the rules above.

## Minimal document

```xml
<Candidate xmlns="http://www.europass.eu/1.0" xmlns:oa="http://www.openapplications.org/oagis/9"
           xmlns:eures="http://www.europass_eures.eu/1.0" xmlns:hr="http://www.hr-xml.org/3">
  <hr:DocumentID schemeID="x" schemeName="DocumentIdentifier" schemeAgencyName="EUROPASS" schemeVersionID="4.0"/>
  <CandidateSupplier>...</CandidateSupplier>
  <CandidatePerson>
    <PersonName><oa:GivenName>Giulia</oa:GivenName><hr:FamilyName>Rossi</hr:FamilyName></PersonName>
    <Communication><ChannelCode>Email</ChannelCode><oa:URI>giulia@example.com</oa:URI></Communication>
  </CandidatePerson>
  <CandidateProfile languageCode="en">
    <hr:ExecutiveSummary>&lt;p&gt;About me.&lt;/p&gt;</hr:ExecutiveSummary>
    <EmploymentHistory>...</EmploymentHistory>
  </CandidateProfile>
  <RenderingInformation><Design>
    <SectionsOrder><Section><Title>work-experience</Title></Section></SectionsOrder>
  </Design></RenderingInformation>
</Candidate>
```

The complete version is [examples/minimal.xml](examples/minimal.xml).

## Status and contributing

Everything here describes the observed behaviour of a public service as of
September 2026 and can change without notice. If a file that validates here
is rejected by the editor, or an element found in a real export is missing,
please open an issue with the *structure* of the file (element names and code
values, never personal data).

## Licence and attribution

Copyright 2026 Stefano Zeppieri. Released under the
[Creative Commons Attribution 4.0 International](LICENSE) licence (CC BY 4.0):
you may copy, redistribute, adapt and build upon this material for any
purpose, including commercially, provided you give appropriate credit, for
example:

> Based on *europass-cv* by Stefano Zeppieri, CC BY 4.0.

Europass is a service of the European Commission. This project is not
affiliated with, endorsed by or supported by the European Commission, Cedefop
or EURES.
