# Codifications (closed value lists)

Copied from `https://europa.eu/europass/eportfolio/api/codifications?types=<type>`
on 18 September 2026. A value outside these lists does not make the import
fail: the file is imported and the field is shown with a validation error
("Should be valid Codification") that the person has to fix by hand.

## Section names (`SectionsOrder/Section/Title`, `profileStructure`)

From the editor's code, not from the codification API.

| Title | Section |
| --- | --- |
| `personal-information` | Personal information (always shown) |
| `work-experience` | Work experience |
| `education-training` | Education and training |
| `language` | Language skills |
| `profile-skills` | Digital skills |
| `driving-licence` | Driving licence |
| `publication` | Publications |
| `membership` | Networks and memberships |
| `social-or-political-activity` | Social and political activities |
| `conference-seminar` | Conferences and seminars |
| `recommendation` | Recommendations |
| `projects` | Projects |
| `skills-assessment` | Digital skills test results |
| `honour-award` | Honours and awards |
| `hobbies-interests` | Hobbies and interests |
| `creative-works` | Creative works |
| `volunteering` | Volunteering |
| `certifications` | Certifications |
| `custom-section` | Custom sections (added automatically for each `Others`) |

## `socialMediaTypes` (Communication/UseCode with ChannelCode "Social Media")

`facebook`, `twitter`, `instagram`, `linkedin`, `youtube`, `pinterest`, `tumblr`, `other`

Anything else (GitHub, a portfolio) goes to `ChannelCode Web`.

## `telephoneTypes` (Communication/UseCode with ChannelCode "Telephone")

`home`, `work`, `mobile`, `other`

## `drivingLicences` (hr:LicenseTypeCode)

| Group | Codes |
| --- | --- |
| motorbikes | `AM`, `A1`, `A2`, `A` |
| cars | `B1`, `B`, `BE` |
| trucks | `C1`, `C1E`, `C`, `CE` |
| others | `D1`, `D1E`, `D`, `DE` |

## `naceTopLevels` (hr:IndustryCode)

`A` to `U` (NACE Rev. 2 sections), plus `NS` (not specified).

## `cefrLevels` (hr:ScoreText under eures:Score)

`A1`, `A2`, `B1`, `B2`, `C1`, `C2`

Dimension codes (`hr:CompetencyDimensionTypeCode`): `CEF-Understanding-Listening`,
`CEF-Understanding-Reading`, `CEF-Speaking-Interaction`, `CEF-Speaking-Production`,
`CEF-Writing-Production`.

## `eqfs` (EducationLevelCode)

`1` to `8`.

## `sexes` (GenderCode)

`male`, `female`, `other`, `do_not_indicate`

## `profileLanguages` (CandidateProfile/@languageCode)

`en`, `bg`, `hr`, `cs`, `da`, `nl`, `et`, `fi`, `fr`, `de`, `el`, `hu`, `is`, `ga`,
`it`, `lv`, `lt`, `mk`, `mt`, `no`, `pl`, `pt`, `ro`, `sr`, `sk`, `sl`, `es`, `sv`,
`tr`, `uk`, `me`

## `instantMessengerTypes`

`skype`, `whatsapp`, `wechat`, `line`, `viber`, `other` (no XML element observed yet)

## `legalDocumentTypes`

`id`, `passport`, `residence-permit` (no XML element observed yet)

## `countries` (CountryCode, NationalityCode, Country)

ISO 3166-1 alpha-2 in lower case (`it`, `fr`, `de`...). The API returns each
code with flags (`eu`, `europe`, `europass`).

## Languages (CompetencyID and PrimaryLanguageCode with scheme NORMAL)

ISO 639-2 three-letter codes (`ita`, `eng`, `fra`, `deu`, `spa`...). A language
not in the editor's list can be written with `schemeName="FREE_TEXT"` (or
`name="FREE_TEXT"` for the mother tongue) and the label as value.
