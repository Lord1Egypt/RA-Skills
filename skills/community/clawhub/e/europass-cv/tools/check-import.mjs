#!/usr/bin/env node
/**
 * Ask the real Europass importer what it understands of a Candidate XML (or a PDF with the XML embedded).
 *
 *   node tools/check-import.mjs examples/full.xml
 *   node tools/check-import.mjs my-cv.pdf --json > profile.json
 *
 * This calls POST https://europa.eu/europass/eportfolio/api/eprofile/europass-cv, the same endpoint the
 * editor at europass.europa.eu calls when you upload a file. It needs no account: the anonymous session
 * cookie and the XSRF token come from loading the editor page first.
 *
 * THE FILE IS SENT TO A EUROPEAN COMMISSION SERVER. Use it with your own CV or with fictional data only.
 *
 * Output: HTTP status, the importer's error (if the file is rejected outright), per-field validation
 * errors, the sections the editor will display (profileStructure) and a count per section. With --json
 * the full parsed profile is printed instead.
 */
import { readFile } from "node:fs/promises";
import { basename, extname } from "node:path";

const EDITOR = "https://europa.eu/europass/eportfolio/screen/cv-editor?lang=en";
const IMPORTER = "https://europa.eu/europass/eportfolio/api/eprofile/europass-cv";
const UA = "Mozilla/5.0 (europass-cv check-import)";

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith("--"));
const asJson = args.includes("--json");
const lang = (args.find((a) => a.startsWith("--lang=")) ?? "--lang=en").slice(7);
if (!file) {
  console.error("usage: node tools/check-import.mjs <file.xml|file.pdf> [--json] [--lang=en]");
  process.exit(2);
}

const bytes = await readFile(file);
const type = extname(file).toLowerCase() === ".pdf" ? "application/pdf" : "text/xml";

// Session cookie + XSRF token, exactly as the browser gets them.
const jar = new Map();
const collect = (res) => {
  for (const c of res.headers.getSetCookie()) {
    const [pair] = c.split(";");
    const i = pair.indexOf("=");
    if (i > 0) jar.set(pair.slice(0, i).trim(), pair.slice(i + 1));
  }
};
const cookie = () => Array.from(jar, ([k, v]) => `${k}=${v}`).join("; ");
collect(await fetch(EDITOR, { headers: { "user-agent": UA } }));
collect(
  await fetch(new URL("/europass/eportfolio/api/user-details", EDITOR), {
    headers: { "user-agent": UA, cookie: cookie() },
  }),
);
const token = jar.get("XSRF-TOKEN");
if (!token) {
  console.error("No XSRF-TOKEN cookie received: the editor site has changed. Please open an issue.");
  process.exit(1);
}

const form = new FormData();
form.append("file", new Blob([bytes], { type }), basename(file));
const res = await fetch(IMPORTER, {
  method: "POST",
  headers: {
    "user-agent": UA,
    cookie: cookie(),
    "x-xsrf-token": token,
    accept: "application/json",
    "accept-language": lang,
  },
  body: form,
});
const text = await res.text();
let body;
try {
  body = JSON.parse(text);
} catch {
  console.log(`HTTP ${res.status}\n${text.slice(0, 500)}`);
  process.exit(1);
}

if (asJson) {
  console.log(JSON.stringify(body, null, 2));
  process.exit(body.errorCode ? 1 : 0);
}

console.log(`HTTP ${res.status}`);
if (body.errorCode) {
  // The whole file was rejected. Known causes: old SkillsPassport v3 format ("not-compliant"),
  // a Telephone communication without CountryDialing, a missing PersonName.
  console.log(`REJECTED: ${body.errorCode}: ${body.errorMessage}`);
  process.exit(1);
}

const p = body.profile ?? {};
const errors = body.errors && Object.keys(body.errors).length ? body.errors : null;
console.log(`Field errors: ${errors ? JSON.stringify(errors, null, 1) : "none"}`);
console.log(`Sections the editor will show: ${(p.preference?.profileStructure ?? []).join(", ") || "(none: add RenderingInformation/Design/SectionsOrder)"}`);
const pi = p.personalInformation ?? {};
const count = (v) => (Array.isArray(v) ? v.length : 0);
const rows = [
  ["personalInformation.emails", count(pi.emails)],
  ["personalInformation.phones", count(pi.phones)],
  ["personalInformation.addresses", count(pi.addresses)],
  ["personalInformation.socialMediaWebsites", count(pi.socialMediaWebsites)],
  ["personalInformation.websites", count(pi.websites)],
  ["personalInformation.nationalities", count(pi.nationalities)],
  ["personalInformation.personalDescription", pi.personalDescription ? "yes" : "no"],
  ["personalInformation.dateOfBirth", pi.dateOfBirth?.date ?? "no"],
  ["workExperiences", count(p.workExperiences?.solidWorkExperiences)],
  ["educationTrainings", count(p.educationTrainings)],
  ["languageSkills.nativeLanguages", count(p.languageSkills?.nativeLanguages)],
  ["languageSkills.otherLanguages", count(p.languageSkills?.otherLanguages)],
  ["profileSkills.other (digital skills)", count(p.profileSkills?.other)],
  ["profileSkills.groups", count(p.profileSkills?.groups)],
  ["drivingLicence.licences", count(p.drivingLicence?.licences)],
  ["publications", count(p.publications)],
  ["customSections", count(p.customSections)],
  ["profile picture", body.userPicture ? "yes" : "no"],
  ["template", p.template?.templateName ?? body.template?.templateName ?? "-"],
];
for (const [k, v] of rows) console.log(`  ${k.padEnd(44)} ${v}`);
process.exit(errors ? 1 : 0);
