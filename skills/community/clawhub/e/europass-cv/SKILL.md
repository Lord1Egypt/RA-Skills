---
name: europass-cv
description: Create or edit a Europass CV in the Candidate XML format that the official europass.europa.eu editor imports (2020 format, HR-XML 3 based). Use when asked to produce, convert, fix or check a Europass CV/XML/PDF for import into Europass, or when an import 'shows only personal data' or is rejected as an old format.
license: CC-BY-4.0
metadata:
  author: Stefano Zeppieri
  repository: europass-cv
---

# Europass CV (Candidate XML)

The current Europass editor imports and exports one format: an HR-XML 3
"Candidate" document with Europass and EURES extensions, embedded as
`attachment.xml` in its PDFs. There is no official schema. This skill gives
you a reference, an unofficial XSD, a JSON to XML generator, a PDF extractor
and a checker that asks the real importer what it understood.

## Workflow: create a CV

1. Collect the data and write it as JSON following `docs/cv-json.md`
   (see `examples/cv.json`). Only `person.givenName` and `person.familyName`
   are mandatory. Keep the person's data as given; do not invent values.
2. Generate: `node tools/build-cv.mjs cv.json > cv.xml`. Read stderr: a
   warning means a value outside a codified list (the editor will flag that
   field); an error means the importer would reject the file (impossible date,
   blank entry title, unknown phone country code).
3. Validate the structure: `sh tools/validate.sh cv.xml` (needs `xmllint`).
4. Check against the real importer, if allowed to send the data to the
   Europass service: `node tools/check-import.mjs cv.xml`. It prints the
   sections the editor will display and a count per section; all expected
   sections must be listed and the field errors must be `none`.
5. Deliver `cv.xml`. The person imports it at europass.europa.eu, "Create your
   CV" then "Import Europass CV", and downloads the official PDF from there.
   If you also produce a PDF, embed the XML as an attachment named
   `attachment.xml` with MIME type `text/xml`; the importer reads such PDFs
   exactly like the bare XML.

## Workflow: edit an existing Europass CV

1. Get the XML: from a PDF exported by the editor,
   `node tools/extract-xml.mjs cv.pdf > cv.xml`; an XML file is used as is.
2. Edit the XML directly, following `docs/format.md`. Keep every element you
   do not understand: the importer ignores unknown elements and other tools
   may need them. When adding content, mirror the shapes already in the file.
3. Validate and check as in steps 3 and 4 above.

## Rules the importer enforces (the schema cannot express them)

- `RenderingInformation/Design/SectionsOrder` must list every section that
  should be visible (`work-experience`, `education-training`, `language`,
  `profile-skills`, `driving-licence`, `publication`...). Sections that are
  imported but not listed stay hidden; the person sees only personal data.
- A `Telephone` communication needs `CountryDialing`, `oa:DialNumber` and
  `CountryCode`; without the dialing code the whole file is rejected.
- Dates are `YYYY`, `YYYY-MM` or `YYYY-MM-DD`; an impossible day rejects the
  whole file.
- `Social Media` `UseCode` is one of facebook, twitter, instagram, linkedin,
  youtube, pinterest, tumblr. Other links use `ChannelCode Web`.
- Custom sections: one `Others` per entry, all with the same `Title`; the
  importer keeps only the last `Other` of an `Others` and merges same-titled
  `Others`. Every `Other` needs a non-blank `Title`.
- Digital skills (`Skills/PersonCompetency/hr:CompetencyName`) must be distinct.
- Long texts are HTML escaped inside the text node (`&lt;p&gt;...&lt;/p&gt;`).
- `CandidateProfile` needs `languageCode`; `PersonName` is mandatory.
- The old SkillsPassport v3 XML (namespace `europass.cedefop.europa.eu`) is
  rejected as an old format: never produce it.

## Where things go

| Content | Element |
| --- | --- |
| Name | `CandidatePerson/PersonName` (`oa:GivenName`, `hr:FamilyName`) |
| E-mail, phone, links, address | `CandidatePerson/Communication` (see `docs/format.md`) |
| Nationality, birth date, sex, mother tongue | `NationalityCode`, `hr:BirthDate`, `GenderCode`, `PrimaryLanguageCode` |
| About me | `CandidateProfile/hr:ExecutiveSummary` |
| Work experience | `EmploymentHistory/EmployerHistory/PositionHistory` |
| Education | `EducationHistory/EducationOrganizationAttendance` (`EducationLevelCode` = EQF, sibling of `EducationDegree`) |
| Languages | `PersonQualifications/PersonCompetency` with `eures:CompetencyDimension` per CEFR skill |
| Digital skills | `Skills/PersonCompetency` (`hr:TaxonomyID` Digital_Skill) |
| Driving licence | `eures:Licenses/eures:License/hr:LicenseTypeCode` |
| Publications | `PublicationHistory/Publication` |
| Anything else (soft skills, certifications, hobbies...) | `Others` custom sections |
| Profile picture | `eures:Attachment` (base64 data URI, base64 encoded again) |

Not importable: a personal headline or motto (put it as the first bold line
of the summary), instant messengers, legal documents, a separate
certifications section.

## Files

- `docs/format.md`: every element, its editor field and the importer's
  responses to known mistakes.
- `docs/codifications.md`: the closed value lists (section names, social
  media, telephone types, licence categories, NACE, CEFR, EQF, languages).
- `docs/cv-json.md`: the generator's input.
- `schema/europass-candidate.xsd`: the unofficial XSD (four namespaces).
- `examples/`: `minimal.xml`, `full.xml`, `cv.json`, all fictional.
- `tools/build-cv.mjs`, `tools/extract-xml.mjs`, `tools/check-import.mjs`,
  `tools/validate.sh`.

## Privacy

`check-import.mjs` sends the file to a European Commission server. Only do
that with the person's consent or with fictional data. Never paste a real CV
into an issue or a log.
