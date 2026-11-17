# The Candidate document, element by element

Namespaces:

| Prefix | Namespace | Origin |
| --- | --- | --- |
| (default) | `http://www.europass.eu/1.0` | Europass container elements |
| `hr:` | `http://www.hr-xml.org/3` | HR-XML 3 (HR Open Standards) |
| `oa:` | `http://www.openapplications.org/oagis/9` | OAGIS 9 |
| `eures:` | `http://www.europass_eures.eu/1.0` | EURES extensions |

The root carries `xsi:schemaLocation="http://www.europass.eu/1.0 Candidate.xsd"`;
the file it points to is not published. The XML declaration is
`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>`.

**HTML in text.** Long texts (`hr:ExecutiveSummary`, `oa:Description`,
`OccupationalSkillsCovered`, `Other/Description`, `hr:FormattedPublicationDescription`)
contain HTML (`p`, `strong`, `ul`, `li`, `br`, `span`) stored *escaped* inside
the text node: `&lt;p&gt;...&lt;/p&gt;`. The importer unescapes it once and
keeps it as rich text.

**Dates.** `hr:FormattedDateTime` and `hr:BirthDate` take `YYYY`, `YYYY-MM` or
`YYYY-MM-DD`; the importer keeps the precision (`dateType` YEAR, MONTH or DAY).
An impossible day rejects the whole file.

**Order.** Real exports disagree on child order inside several elements (for
instance `Communication`); the importer does not care. The XSD in this
repository uses repeatable choices for those.

## `Candidate`

```
hr:DocumentID  @schemeID @schemeName="DocumentIdentifier" @schemeAgencyName="EUROPASS" @schemeVersionID="4.0"
CandidateSupplier
CandidatePerson
CandidateProfile @languageCode
RenderingInformation
```

## `CandidateSupplier`

Who supplies the document. The editor writes the person themselves.

```
hr:PartyID @schemeID @schemeName="PartyID" @schemeAgencyName="EUROPASS" @schemeVersionID="1.0"
hr:PartyName            "Owner"
PersonContact
  PersonName            oa:GivenName, hr:FamilyName
  Communication*        the e-mail channel
hr:PrecedenceCode       1
```

## `CandidatePerson`

| Element | Editor field | Notes |
| --- | --- | --- |
| `PersonName/oa:GivenName`, `PersonName/hr:FamilyName` | First name, last name | Required: without `PersonName` the importer rejects the file |
| `Communication` (Email) | E-mail | `ChannelCode` Email, `oa:URI` |
| `Communication` (Telephone) | Phone | `ChannelCode` Telephone, `UseCode` home/work/mobile/other, `CountryDialing` (digits, no +), `oa:DialNumber`, `CountryCode`. **`CountryDialing` is mandatory.** An unknown prefix gives "Should be valid prefix" |
| `Communication` (Social Media) | Social media | `ChannelCode` Social Media, `UseCode` one of the codified types, `oa:URI` |
| `Communication` (Web) | Website | `ChannelCode` Web, `oa:URI` absolute URL |
| `Communication` (Address) | Address | `UseCode` home, `Address type="home"` with `oa:AddressLine`, `oa:CityName`, `CountryCode`, `oa:PostalCode` |
| `NationalityCode` | Nationality | ISO 3166-1 alpha-2, lower case |
| `hr:BirthDate` | Date of birth | `YYYY-MM-DD`, `YYYY-MM` or `YYYY` |
| `GenderCode` | Sex | male, female, other, do_not_indicate |
| `PrimaryLanguageCode @name` | Mother tongue(s) | Repeatable. `name="NORMAL"` with an ISO 639-2 code, or `name="FREE_TEXT"` with a label |

Not importable (tried, no element fills them): the personal title or motto
(`personalMottoLine`), instant messengers, legal documents.

## `CandidateProfile`

Attribute `languageCode`: the CV language (two letters); missing, the profile
language is flagged.

| Element | Editor section | Notes |
| --- | --- | --- |
| `hr:ID` | (internal) | May be empty or absent |
| `hr:ExecutiveSummary` | About me | Escaped HTML |
| `EmploymentHistory/EmployerHistory` | Work experience | One `EmployerHistory` per position (see below) |
| `EducationHistory/EducationOrganizationAttendance` | Education and training | See below |
| `eures:Licenses/eures:License/hr:LicenseTypeCode` | Driving licence | One `eures:License` per category |
| `Certifications` | Certifications | Only observed empty; `Certification` children are ignored |
| `PublicationHistory/Publication` | Publications | See below |
| `PersonQualifications/PersonCompetency` | Language skills | See below |
| `EmploymentReferences` | Recommendations | Only observed empty |
| `eures:Attachment` | Profile picture | `oa:EmbeddedData` (base64 of a `data:image/...;base64,...` URI), `oa:FileType` photo, `hr:Instructions` ProfilePicture |
| `CreativeWorks`, `Projects`, `SocialAndPoliticalActivities`, `NetworksAndMemberships`, `ConferencesAndSeminars`, `VoluntaryWorks`, `CourseCertifications` | Other sections | Only observed empty |
| `Skills` | Digital skills | See below |
| `Others` | Custom sections | See below |
| `CommunicationAndInterpersonalSkills`, `OrganisationalSkills`, `DigitalSkills` | (legacy) | Written by older editor versions; ignored today |

### Work experience

```
EmployerHistory
  hr:OrganizationName                        employer
  OrganizationContact/Communication/Address  oa:CityName, CountryCode  (also Web/Email channels: organisation website, contact e-mail)
  hr:IndustryCode                            NACE section letter (organisationBusinessSector)
  Link                                       organisation link (observed in exports)
  PositionHistory
    PositionTitle @typeCode="FREETEXT"       occupation label
    eures:EmploymentPeriod
      eures:StartDate/hr:FormattedDateTime
      eures:EndDate/hr:FormattedDateTime     omit when current
      hr:CurrentIndicator                    true | false
    oa:Description                           main activities, escaped HTML
    City
    Country                                  lower-case ISO code
```

### Education and training

```
EducationOrganizationAttendance
  hr:OrganizationName                        institution
  OrganizationContact/Communication          Address (city, country) and/or Web channel (website)
  AttendancePeriod
    StartDate/hr:FormattedDateTime
    EndDate/hr:FormattedDateTime
    Ongoing                                  true | false
  EducationDegree
    hr:DegreeName                            qualification
    OccupationalSkillsCovered                description (escaped HTML)
    FieldOfStudy @typeCode="URI"             MainFieldOfStudy/ProgramConcentration, SpecificFieldOfStudy/ProgramConcentration (ISCED-F codes)
    FinalGrade/hr:ScoreText                  final grade, free text
    Thesis                                   thesis title
    NationalClassification
    CreditType                               ECTS
    NumberOfCredit
  EducationLevelCode                         EQF level 1..8  (sibling of EducationDegree, not inside it)
  Link
```

### Language skills

```
PersonCompetency
  CompetencyID @schemeName="NORMAL"|"FREE_TEXT"   ISO 639-2 code, or a label
  hr:TaxonomyID                                   language
  eures:CompetencyDimension*                      one per skill
    hr:CompetencyDimensionTypeCode                CEF-Understanding-Listening | CEF-Understanding-Reading | CEF-Speaking-Interaction | CEF-Speaking-Production | CEF-Writing-Production
    eures:Score/hr:ScoreText                      A1 .. C2
```

### Digital skills

```
Skills
  PersonCompetency*                 loose skills: hr:TaxonomyID Digital_Skill, hr:CompetencyName
  SkillsGroup*                      named group: Title, then PersonCompetency*
```

Two identical `hr:CompetencyName` values give a "Should contain distinct values" error.

### Custom sections

```
Others
  Title                 section title
  Other                 ONE entry
    Title               entry title, required (non-blank)
    Date                StartDate/hr:FormattedDateTime, EndDate/hr:FormattedDateTime  (optional)
    Description         escaped HTML
    Link*               optional links
```

**The importer keeps only the last `Other` of an `Others`.** To have several
entries in one section, write one `Others` per entry, all with the same
`Title`: the importer merges them into a single section with all the entries.
Custom sections are added to the displayed sections automatically; they do not
need to appear in `SectionsOrder`.

### Publications

```
Publication
  hr:FormattedPublicationDescription   escaped HTML
  Title
  Year
  Reference
  DOI/Link
  Authors, Journal, Publisher, Volume
```

## `RenderingInformation`

```
Design
  Template        Template1 | Template2 | Template3 ...
  Color           Default ...
  FontSize        Medium ...
  Logo            FirstPage ...
  PageNumbers     true | false
  SectionsOrder
    Section
      Title       section name (see codifications.md)
      Custom      true for a custom section (observed in some exports)
```

`SectionsOrder` becomes `profile.preference.profileStructure`, and the editor
displays exactly the listed sections that have content (plus personal
information, always, and custom sections). Leave it out and everything but the
personal information is hidden.

## PDF embedding

The editor's PDFs carry the document as an embedded file named
`attachment.xml`, `/Subtype /text/xml`, with `/Desc`, `/UF` and an `/AF`
array on the catalog (produced with pdf-lib). The importer accepts such PDFs
exactly like the bare XML. `application/xml` as subtype also works.

## Importer responses worth knowing

| Response | Cause |
| --- | --- |
| `not-compliant`, "Documento non valido, vecchio formato" | SkillsPassport v3 XML |
| `not-compliant`, "map XML to model: null" | Telephone without `CountryDialing`; other missing mandatory sub-elements |
| `not-compliant`, "map XML to model: Cannot invoke ...PersonName" | Missing `PersonName` |
| `not-compliant`, "Invalid date 'FEBRUARY 31'" | Impossible date |
| `errors.personalInformation[...].mediaType` ValidCodification | Social media `UseCode` not in the list |
| `errors.personalInformation[...].phonePrefix` "Should be valid prefix" | Unknown `CountryDialing` |
| `errors.customSections[...].records[...].title` NotBlank | `Other` without `Title` |
| `errors.profileSkills.other` Distinct | Duplicate digital skills |
| `errors.language` ValidCodification | Missing `CandidateProfile/@languageCode` |
| Sections missing on screen, data present in the response | No `SectionsOrder` |
