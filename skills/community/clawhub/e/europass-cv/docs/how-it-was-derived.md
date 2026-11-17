# How this format was derived

The European Commission publishes no schema for the Candidate XML that the
Europass editor (europass.europa.eu, since 2020) imports and exports. The
`Candidate.xsd` named in `xsi:schemaLocation` is not downloadable from any
Europass, Cedefop, EURES or code.europa.eu location (the `cv`
folders in the ELM repositories on code.europa.eu are *controlled
vocabularies*, not curricula). Everything in this repository was established
empirically, in four ways.

## 1. The editor's own exports

Every PDF the editor produces embeds the complete CV as an attachment named
`attachment.xml` (MIME type `text/xml`, produced with pdf-lib; the file
specification carries `/Desc`, `/UF` and an `/AF` array on the catalog). From
two real exports (July 2026) only the *structure* was extracted: element names,
attributes, code values and the shape of dates. No personal values were retained.

## 2. The editor's importer

When a file is uploaded, the editor's frontend posts it to

```
POST https://europa.eu/europass/eportfolio/api/eprofile/europass-cv
Content-Type: multipart/form-data; field "file"
Cookie: XSRF-TOKEN=...       (set when loading the editor page)
X-XSRF-TOKEN: ...            (same value)
Accept-Language: it          (language of the validation messages)
```

No account is needed. The response is

```json
{ "profile": { ... },      // what the importer understood
  "errors": { ... },       // per-field validation errors, or {}
  "userPicture": "...",     // base64 photo, if any
  "template": { ... } }    // rendering choices
```

or, when the whole file is refused,
`{"errorCode":"not-compliant","errorMessage":"Error while trying to map XML to model: ..."}`.

`tools/check-import.mjs` calls this endpoint. Fictional CVs were submitted,
removing or changing one element at a time, to establish which elements are
read, which are ignored, and which make the whole file fail. The results are in
[format.md](format.md).

## 3. The editor's code

The frontend bundles (`https://europa.eu/europass/eportfolio/*.js`) provide:

- the endpoint and form field above (`WIZARD_API_EUROPASS_CV`, `buildFormData`);
- the section names used in `SectionsOrder` and in `profile.preference.profileStructure`
  (`personal-information`, `work-experience`, `education-training`, `language`,
  `profile-skills`, `driving-licence`, `publication`, `membership`,
  `social-or-political-activity`, `conference-seminar`, `recommendation`,
  `projects`, `skills-assessment`, `honour-award`, `hobbies-interests`,
  `creative-works`, `volunteering`, `certifications`, `custom-section`);
- the rule that decides what is displayed after an import: only the sections
  listed in `profileStructure` (and non-empty), plus custom sections. This is
  why a file without `RenderingInformation/Design/SectionsOrder` imports "only
  personal data" as far as the user can see.

## 4. The codification lists

The dropdown values are served by
`GET https://europa.eu/europass/eportfolio/api/codifications?types=<type>`
(`socialMediaTypes`, `telephoneTypes`, `drivingLicences`, `naceTopLevels`,
`cefrLevels`, `eqfs`, `sexes`, `countries`, `profileLanguages`,
`instantMessengerTypes`, `legalDocumentTypes`). They are copied in
[codifications.md](codifications.md).

## What the format is, historically

`Candidate`, `CandidateSupplier`, `CandidatePerson`, `CandidateProfile`,
`EmploymentHistory/EmployerHistory/PositionHistory`,
`EducationHistory/EducationOrganizationAttendance`, `PersonQualifications/PersonCompetency`
and the `hr:`/`oa:` prefixes are the HR-XML 3 (HR Open Standards) *Candidate*
noun built on OAGIS 9. Europass adds its own namespace for the container
elements and an `eures:` namespace (EURES, the European job mobility network)
for periods, licences, competency dimensions and attachments. The predecessor
format, the Cedefop "SkillsPassport" XML v3 (namespace
`http://europass.cedefop.europa.eu/Europass`, 2013 to 2020), is rejected by the
current editor as an old format; most open-source Europass tooling still
targets it.

## Trademarks and affiliation

Europass is a service of the European Commission. This project is not
affiliated with, endorsed by or supported by the European Commission, Cedefop
or EURES. The endpoint documented here is the one the public editor uses; it
may change without notice.
