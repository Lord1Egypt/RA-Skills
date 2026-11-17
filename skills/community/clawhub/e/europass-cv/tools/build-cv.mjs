#!/usr/bin/env node
/**
 * Build a Europass Candidate XML from a plain JSON description of a CV.
 *
 *   node tools/build-cv.mjs cv.json > cv.xml
 *
 * The JSON shape is documented in docs/cv-json.md (see examples/cv.json). This script applies every
 * rule we know the importer enforces: SectionsOrder derived from the content, one Others per custom
 * entry, telephone with CountryDialing, codified social media types, HTML escaped inside text nodes,
 * dates with the precision you give (YYYY, YYYY-MM, YYYY-MM-DD) and rejected when impossible.
 * Warnings for values outside the codification lists go to stderr; the XML goes to stdout.
 *
 * No dependencies. Node 20 or later.
 */
import { readFileSync } from "node:fs";

const SOCIAL = ["facebook", "twitter", "instagram", "linkedin", "youtube", "pinterest", "tumblr"];
const PHONE_TYPES = ["home", "work", "mobile", "other"];
const LICENCES = ["AM", "A1", "A2", "A", "B1", "B", "BE", "C1", "C1E", "C", "CE", "D1", "D1E", "D", "DE"];
const NACE = [..."ABCDEFGHIJKLMNOPQRSTU", "NS"];
const CEFR = ["A1", "A2", "B1", "B2", "C1", "C2"];
const CEF_DIMENSIONS = [
  ["listening", "CEF-Understanding-Listening"],
  ["reading", "CEF-Understanding-Reading"],
  ["spokenInteraction", "CEF-Speaking-Interaction"],
  ["spokenProduction", "CEF-Speaking-Production"],
  ["writing", "CEF-Writing-Production"],
];
// Country calling codes, longest first, for phone strings like "+39 333 0000000".
const DIALING = [
  ["351", "pt"], ["352", "lu"], ["353", "ie"], ["354", "is"], ["355", "al"], ["356", "mt"], ["357", "cy"],
  ["358", "fi"], ["359", "bg"], ["370", "lt"], ["371", "lv"], ["372", "ee"], ["373", "md"], ["380", "ua"],
  ["381", "rs"], ["385", "hr"], ["386", "si"], ["387", "ba"], ["389", "mk"], ["420", "cz"], ["421", "sk"],
  ["30", "gr"], ["31", "nl"], ["32", "be"], ["33", "fr"], ["34", "es"], ["36", "hu"], ["39", "it"], ["40", "ro"],
  ["41", "ch"], ["43", "at"], ["44", "gb"], ["45", "dk"], ["46", "se"], ["47", "no"], ["48", "pl"], ["49", "de"],
  ["90", "tr"], ["1", "us"],
];

const warnings = [];
const warn = (m) => warnings.push(m);

/* ---------- tiny XML builder ---------- */
const CONTROL = /[\x00-\x08\x0B\x0C\x0E-\x1F]/g;
const esc = (v) => String(v).replace(CONTROL, "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const escAttr = (v) => esc(v).replace(/"/g, "&quot;");
/** el(name, attrs?, ...children); falsy children are skipped; strings are text. */
function el(name, ...rest) {
  let attrs = {};
  if (rest.length && rest[0] && typeof rest[0] === "object" && !rest[0].__el && !Array.isArray(rest[0])) attrs = rest.shift();
  const children = rest.flat(Infinity).filter((c) => c !== false && c !== null && c !== undefined && c !== "");
  return { __el: true, name, attrs, children };
}
function write(n) {
  if (typeof n === "string") return esc(n);
  const a = Object.entries(n.attrs).filter(([, v]) => v !== undefined && v !== null).map(([k, v]) => ` ${k}="${escAttr(v)}"`).join("");
  return n.children.length ? `<${n.name}${a}>${n.children.map(write).join("")}</${n.name}>` : `<${n.name}${a}/>`;
}
/** Plain text or HTML -> the escaped HTML the editor stores. Plain text becomes <p> per paragraph. */
const html = (text) => {
  if (!text) return "";
  const t = String(text).trim();
  if (/<\/?(p|ul|ol|li|strong|em|br|b|i|span)\b/i.test(t)) return t;
  return t.split(/\n{2,}|\r?\n/).map((p) => p.trim()).filter(Boolean).map((p) => `<p>${esc(p)}</p>`).join("");
};
const list = (items) => (items?.length ? `<ul>${items.map((i) => `<li>${esc(i)}</li>`).join("")}</ul>` : "");

/* ---------- dates ---------- */
function date(v, what) {
  if (v === undefined || v === null || v === "") return null;
  const s = String(v).trim();
  const m = s.match(/^(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?$/);
  if (!m) throw new Error(`${what}: date "${s}" must be YYYY, YYYY-MM or YYYY-MM-DD`);
  const [, y, mo, d] = m;
  if (mo && (Number(mo) < 1 || Number(mo) > 12)) throw new Error(`${what}: month out of range in "${s}"`);
  if (d && new Date(Date.UTC(Number(y), Number(mo) - 1, Number(d))).getUTCDate() !== Number(d)) {
    throw new Error(`${what}: "${s}" is not a real date (the importer rejects the whole file)`);
  }
  return s;
}
const dated = (wrapper, v) => el(wrapper, el("hr:FormattedDateTime", v));

/* ---------- phone ---------- */
function phone(p, i) {
  if (!p) return null;
  if (typeof p === "object") {
    if (!p.dialing || !p.number) throw new Error(`person.phones[${i}]: needs dialing and number`);
    return { dialing: String(p.dialing).replace(/^\+/, ""), number: String(p.number).replace(/\D/g, ""), country: p.country ?? "", type: p.type ?? "mobile" };
  }
  const digits = String(p).replace(/[^\d+]/g, "");
  const intl = digits.match(/^(?:\+|00)(\d+)$/);
  if (!intl) throw new Error(`person.phones[${i}]: give an international number (+39 ...) or {dialing, number, country}`);
  const hit = DIALING.find(([c]) => intl[1].startsWith(c));
  if (!hit) throw new Error(`person.phones[${i}]: unknown country code in "${p}", use {dialing, number, country}`);
  return { dialing: hit[0], number: intl[1].slice(hit[0].length), country: hit[1], type: "mobile" };
}

/* ---------- sections ---------- */
function person(cv) {
  const p = cv.person ?? {};
  if (!p.givenName || !p.familyName) throw new Error("person.givenName and person.familyName are required");
  const emails = [].concat(p.email ?? p.emails ?? []);
  const phones = [].concat(p.phones ?? p.phone ?? []).map(phone).filter(Boolean);
  const socials = (p.socialMedia ?? []).map((s) => {
    if (!SOCIAL.includes(s.type)) warn(`socialMedia type "${s.type}" is not codified (${SOCIAL.join(", ")}): it will be flagged; use "websites" instead`);
    return s;
  });
  phones.forEach((ph) => { if (!PHONE_TYPES.includes(ph.type)) warn(`phone type "${ph.type}" not codified (${PHONE_TYPES.join(", ")})`); });
  const a = p.address;
  const tongues = [].concat(p.motherTongues ?? p.motherTongue ?? []);
  return el("CandidatePerson",
    el("PersonName", el("oa:GivenName", p.givenName), el("hr:FamilyName", p.familyName)),
    emails.map((e) => el("Communication", el("ChannelCode", "Email"), el("oa:URI", e))),
    socials.map((s) => el("Communication", el("ChannelCode", "Social Media"), el("UseCode", s.type), el("oa:URI", s.url))),
    (p.websites ?? []).map((u) => el("Communication", el("ChannelCode", "Web"), el("oa:URI", u))),
    phones.map((ph) => el("Communication", el("ChannelCode", "Telephone"), el("UseCode", ph.type), el("CountryDialing", ph.dialing), el("oa:DialNumber", ph.number), ph.country && el("CountryCode", ph.country))),
    a && el("Communication", el("UseCode", "home"), el("Address", { type: "home" }, a.line && el("oa:AddressLine", a.line), a.city && el("oa:CityName", a.city), a.country && el("CountryCode", a.country), a.postalCode && el("oa:PostalCode", a.postalCode))),
    p.nationality && el("NationalityCode", p.nationality),
    date(p.birthDate, "person.birthDate") && el("hr:BirthDate", date(p.birthDate, "person.birthDate")),
    p.gender && el("GenderCode", p.gender),
    tongues.map((t) => (typeof t === "string" && /^[a-z]{3}$/.test(t) ? el("PrimaryLanguageCode", { name: "NORMAL" }, t) : el("PrimaryLanguageCode", { name: "FREE_TEXT" }, typeof t === "string" ? t : t.label))),
  );
}

const orgContact = (x) => el("OrganizationContact",
  el("Communication", el("Address", x.city && el("oa:CityName", x.city), x.country && el("CountryCode", x.country))),
  x.website && el("Communication", el("ChannelCode", "Web"), el("oa:URI", x.website)),
);

function work(cv) {
  return el("EmploymentHistory", (cv.workExperience ?? []).map((w, i) => {
    if (w.sector && !NACE.includes(w.sector)) warn(`workExperience[${i}].sector "${w.sector}" is not a NACE section letter`);
    const start = date(w.start, `workExperience[${i}].start`);
    const end = w.current ? null : date(w.end, `workExperience[${i}].end`);
    const current = w.current === true || (!end && w.current !== false && !w.end);
    return el("EmployerHistory",
      el("hr:OrganizationName", w.employer ?? ""),
      orgContact(w),
      w.sector && el("hr:IndustryCode", w.sector),
      el("PositionHistory",
        el("PositionTitle", { typeCode: "FREETEXT" }, w.title ?? ""),
        el("eures:EmploymentPeriod", start && dated("eures:StartDate", start), end && dated("eures:EndDate", end), el("hr:CurrentIndicator", current ? "true" : "false")),
        (w.description || w.activities?.length) && el("oa:Description", w.description ? html(w.description) : list(w.activities)),
        w.city && el("City", w.city),
        w.country && el("Country", w.country),
      ),
    );
  }));
}

function education(cv) {
  return el("EducationHistory", (cv.education ?? []).map((e, i) => {
    const start = date(e.start, `education[${i}].start`);
    const end = date(e.end, `education[${i}].end`);
    if (e.eqf !== undefined && e.eqf !== null && !(Number(e.eqf) >= 1 && Number(e.eqf) <= 8)) warn(`education[${i}].eqf must be 1..8`);
    return el("EducationOrganizationAttendance",
      el("hr:OrganizationName", e.institution ?? ""),
      orgContact(e),
      el("AttendancePeriod", start && dated("StartDate", start), end && dated("EndDate", end), el("Ongoing", e.ongoing === true ? "true" : "false")),
      el("EducationDegree",
        el("hr:DegreeName", e.qualification ?? ""),
        e.description && el("OccupationalSkillsCovered", html(e.description)),
        e.fieldOfStudy && el("FieldOfStudy", { typeCode: "URI" }, el("MainFieldOfStudy", el("ProgramConcentration", e.fieldOfStudy))),
        e.grade && el("FinalGrade", el("hr:ScoreText", e.grade)),
        e.thesis && el("Thesis", e.thesis),
        e.credits && el("CreditType", e.creditType ?? "ECTS"),
        e.credits && el("NumberOfCredit", String(e.credits)),
      ),
      e.eqf !== undefined && e.eqf !== null && el("EducationLevelCode", String(e.eqf)),
      e.link && el("Link", e.link),
    );
  }));
}

function languages(cv) {
  return el("PersonQualifications", (cv.languages ?? []).map((l, i) => {
    const code = l.code ? { scheme: "NORMAL", value: l.code } : { scheme: "FREE_TEXT", value: l.label ?? "" };
    if (!code.value) throw new Error(`languages[${i}]: needs code (ISO 639-2) or label`);
    return el("PersonCompetency",
      el("CompetencyID", { schemeName: code.scheme }, code.value),
      el("hr:TaxonomyID", "language"),
      CEF_DIMENSIONS.map(([key, dim]) => {
        const level = l[key];
        if (!level) return null;
        if (!CEFR.includes(level)) warn(`languages[${i}].${key} "${level}" is not a CEFR level`);
        return el("eures:CompetencyDimension", el("hr:CompetencyDimensionTypeCode", dim), el("eures:Score", el("hr:ScoreText", level)));
      }),
    );
  }));
}

function skills(cv) {
  const seen = new Set();
  const one = (s) => {
    const k = String(s).trim().toLowerCase();
    if (!k || seen.has(k)) { if (k) warn(`digital skill "${s}" repeated: dropped (the importer requires distinct values)`); return null; }
    seen.add(k);
    return el("PersonCompetency", el("hr:TaxonomyID", "Digital_Skill"), el("hr:CompetencyName", String(s).trim()));
  };
  const flat = (cv.digitalSkills ?? []).filter((s) => typeof s === "string").map(one);
  const groups = (cv.digitalSkills ?? []).filter((s) => typeof s === "object").map((g) => el("SkillsGroup", el("Title", g.title), (g.skills ?? []).map(one)));
  return el("Skills", flat, groups);
}

function licences(cv) {
  return el("eures:Licenses", (cv.drivingLicences ?? []).map((c) => {
    if (!LICENCES.includes(c)) warn(`driving licence "${c}" is not a codified category (${LICENCES.join(", ")})`);
    return el("eures:License", el("hr:LicenseTypeCode", c));
  }));
}

/** One <Others> per entry, same title: the importer keeps only the last Other of an Others and merges same-titled Others. */
function custom(cv) {
  return (cv.customSections ?? []).flatMap((s, i) => (s.entries ?? []).map((e, j) => {
    if (!e.title || !String(e.title).trim()) throw new Error(`customSections[${i}].entries[${j}]: title is required (the editor flags blank titles)`);
    return el("Others", el("Title", s.title),
      el("Other", el("Title", e.title),
        (e.start || e.end) && el("Date", e.start && dated("StartDate", date(e.start, "custom entry start")), e.end && dated("EndDate", date(e.end, "custom entry end"))),
        e.description && el("Description", html(e.description)),
        (e.links ?? []).map((l) => el("Link", l)),
      ));
  }));
}

function publications(cv) {
  return el("PublicationHistory", (cv.publications ?? []).map((p) => el("Publication",
    p.description && el("hr:FormattedPublicationDescription", html(p.description)),
    el("Title", p.title ?? ""), p.year && el("Year", String(p.year)), p.reference && el("Reference", p.reference),
    p.doi && el("DOI", el("Link", p.doi)), p.authors && el("Authors", p.authors), p.journal && el("Journal", p.journal),
    p.publisher && el("Publisher", p.publisher), p.volume && el("Volume", String(p.volume)),
  )));
}

function sectionsOrder(cv) {
  const s = [];
  if (cv.workExperience?.length) s.push("work-experience");
  if (cv.education?.length) s.push("education-training");
  if (cv.languages?.length || cv.person?.motherTongues?.length || cv.person?.motherTongue) s.push("language");
  if (cv.digitalSkills?.length) s.push("profile-skills");
  if (cv.drivingLicences?.length) s.push("driving-licence");
  if (cv.publications?.length) s.push("publication");
  return (cv.sectionsOrder ?? s);
}

export function buildCandidate(cv) {
  const scheme = cv.schemeId ?? "europass-cv";
  const lang = cv.language ?? "en";
  const p = cv.person ?? {};
  const t = cv.template ?? {};
  const doc = el("Candidate", {
    "xsi:schemaLocation": "http://www.europass.eu/1.0 Candidate.xsd",
    xmlns: "http://www.europass.eu/1.0",
    "xmlns:oa": "http://www.openapplications.org/oagis/9",
    "xmlns:eures": "http://www.europass_eures.eu/1.0",
    "xmlns:hr": "http://www.hr-xml.org/3",
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
  },
    el("hr:DocumentID", { schemeID: scheme, schemeName: "DocumentIdentifier", schemeAgencyName: "EUROPASS", schemeVersionID: "4.0" }),
    el("CandidateSupplier",
      el("hr:PartyID", { schemeID: scheme, schemeName: "PartyID", schemeAgencyName: "EUROPASS", schemeVersionID: "1.0" }),
      el("hr:PartyName", "Owner"),
      el("PersonContact", el("PersonName", el("oa:GivenName", p.givenName ?? ""), el("hr:FamilyName", p.familyName ?? "")),
        [].concat(p.email ?? p.emails ?? []).slice(0, 1).map((e) => el("Communication", el("ChannelCode", "Email"), el("oa:URI", e)))),
      el("hr:PrecedenceCode", "1"),
    ),
    person(cv),
    el("CandidateProfile", { languageCode: lang },
      el("hr:ID", { schemeID: scheme, schemeName: "CandidateProfileID", schemeAgencyName: "EUROPASS", schemeVersionID: "1.0" }, cv.id ?? ""),
      cv.summary && el("hr:ExecutiveSummary", html(cv.summary)),
      work(cv), education(cv), licences(cv), el("Certifications"), publications(cv), languages(cv),
      el("EmploymentReferences"), el("CreativeWorks"), el("Projects"), el("SocialAndPoliticalActivities"), skills(cv),
      el("NetworksAndMemberships"), el("ConferencesAndSeminars"), el("VoluntaryWorks"), el("CourseCertifications"),
      custom(cv),
    ),
    el("RenderingInformation", el("Design",
      el("Template", t.name ?? "Template1"), el("Color", t.color ?? "Default"), el("FontSize", t.fontSize ?? "Medium"),
      el("Logo", t.logo ?? "FirstPage"), el("PageNumbers", t.pageNumbers === false ? "false" : "true"),
      el("SectionsOrder", sectionsOrder(cv).map((s) => el("Section", el("Title", s)))),
    )),
  );
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` + write(doc);
}

const isMain = process.argv[1] && import.meta.url === new URL(`file://${process.argv[1]}`).href;
if (isMain) {
  const file = process.argv[2];
  if (!file) { console.error("usage: node tools/build-cv.mjs cv.json > cv.xml"); process.exit(2); }
  try {
    const xml = buildCandidate(JSON.parse(readFileSync(file, "utf8")));
    for (const w of warnings) console.error(`warning: ${w}`);
    process.stdout.write(xml + "\n");
  } catch (e) {
    console.error(`error: ${e.message}`);
    process.exit(1);
  }
}
