# The JSON input of `tools/build-cv.mjs`

A plain description of a CV that the generator turns into a valid Candidate
document, applying the import rules (section order, one `Others` per entry,
telephone with dialing code, escaped HTML, date checks). All fields are
optional except `person.givenName` and `person.familyName`. See
[examples/cv.json](../examples/cv.json).

```jsonc
{
  "language": "en",                    // CandidateProfile/@languageCode: two letters
  "id": "my-cv-001",                    // hr:ID value (optional)
  "person": {
    "givenName": "Giulia",
    "familyName": "Rossi",
    "email": "giulia@example.com",      // or "emails": [...]
    "phones": ["+39 333 0000000"],      // E.164 string, or {"dialing":"39","number":"3330000000","country":"it","type":"mobile"}
    "address": { "line": "Via di Prova 1", "city": "Bologna", "postalCode": "40100", "country": "it" },
    "nationality": "it",                // ISO 3166-1 alpha-2, lower case
    "birthDate": "1990-05-12",          // YYYY, YYYY-MM or YYYY-MM-DD
    "gender": "female",                 // male | female | other | do_not_indicate
    "socialMedia": [{ "type": "linkedin", "url": "https://www.linkedin.com/in/giulia-rossi-test" }],
    "websites": ["https://github.com/giulia-test"],
    "motherTongues": ["ita"]            // ISO 639-2 codes, or a label for FREE_TEXT
  },
  "summary": "About me. Plain text (paragraphs become <p>) or HTML.",
  "workExperience": [
    {
      "title": "Accounting clerk",
      "employer": "Meccanica Padana Srl",
      "city": "Bologna", "country": "it",
      "sector": "C",                    // NACE section letter, optional
      "start": "2019-09", "end": null, "current": true,
      "activities": ["Bookkeeping.", "Bank reconciliations."],   // or "description": "<ul><li>...</li></ul>"
      "website": "https://example.org"  // organisation website, optional
    }
  ],
  "education": [
    {
      "qualification": "Bachelor in Business Administration",
      "institution": "Università di Bologna",
      "city": "Bologna", "country": "it",
      "start": "2010", "end": "2014", "ongoing": false,
      "eqf": 6,                         // 1..8
      "grade": "105/110", "thesis": "Management control in SMEs",
      "description": "Main subjects...",
      "fieldOfStudy": "0411",           // ISCED-F code, optional
      "credits": 180, "creditType": "ECTS",
      "link": "https://www.unibo.it"
    }
  ],
  "languages": [
    { "code": "eng", "listening": "B2", "reading": "B2", "spokenInteraction": "B1", "spokenProduction": "B1", "writing": "B2" },
    { "label": "Swahili", "listening": "A1" }   // label -> FREE_TEXT
  ],
  "digitalSkills": ["Excel", "SAP FI", { "title": "Tools", "skills": ["Git", "Docker"] }],
  "drivingLicences": ["B"],
  "publications": [{ "title": "...", "year": 2025, "authors": "...", "journal": "...", "doi": "https://doi.org/..." }],
  "customSections": [
    { "title": "Personal skills",
      "entries": [{ "title": "Communication", "description": "...", "start": "2020", "end": "2021", "links": [] }] }
  ],
  "sectionsOrder": ["work-experience", "education-training"],   // optional; derived from content when omitted
  "template": { "name": "Template1", "color": "Default", "fontSize": "Medium", "logo": "FirstPage", "pageNumbers": true }
}
```

Values outside the codified lists (social media types, telephone types,
driving licence categories, NACE letters, CEFR levels, EQF levels) produce a
warning on stderr: the file still imports, but the editor flags the field.
Impossible dates and blank custom entry titles are errors, because the
importer rejects or flags them.
