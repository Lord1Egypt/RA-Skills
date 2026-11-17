// The deduplication graph's executable contract: the boundaries schema
// validation cannot express, checked against the compiled resources.
//
// It loads through `loadResources`, the same loader `cargo-ai project check`,
// `plan`, and `deploy` use, so what is asserted here is what would deploy.
import assert from "node:assert/strict";
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { loadResources } from "@cargo-ai/cdk";

import { deriveEvidence } from "../infra/scripts/accounts/evidence.ts";
import { deriveContactEvidence } from "../infra/scripts/contacts/evidence.ts";
import {
  normalizeEmail,
  normalizeLinkedinProfile,
  normalizePhone,
  phoneMatchKeys,
} from "../infra/scripts/contacts/identity.ts";
import { prepareContactSearch } from "../infra/scripts/contacts/search.ts";

const infraDir = new URL("../infra", import.meta.url).pathname;
const byId = new Map(
  (await loadResources(infraDir)).map((resource) => [resource.id, resource]),
);

// Each object path owns its own folder and shares `common/`. A path that reads
// the other's modules makes one path's local decision the other's contract, so
// adapting or removing a path stops being independent.
const scriptsDir = join(infraDir, "scripts");
const sourcesIn = (folder) =>
  readdirSync(join(scriptsDir, folder)).map((file) => ({
    path: `${folder}/${file}`,
    source: readFileSync(join(scriptsDir, folder, file), "utf8"),
  }));
for (const [folder, other] of [
  ["accounts", "contacts"],
  ["contacts", "accounts"],
]) {
  for (const { path, source } of sourcesIn(folder)) {
    assert.equal(
      source.includes(`from "../${other}/`),
      false,
      `${path} must not import the ${other} path: shared code belongs in scripts/common/`,
    );
  }
}
for (const { path, source } of sourcesIn("common")) {
  assert.equal(
    source.includes('from "../'),
    false,
    `${path} must not depend on an object path: common code is what both paths read`,
  );
}

assert.deepEqual(
  new Set(byId.keys()),
  new Set([
    "connector:crm",
    "connector:slack",
    "folder:crm_deduplication_models",
    "folder:crm_deduplication_plays",
    "model:crm_accounts",
    "model:crm_contacts",
    "play:deduplicate_accounts",
    "play:deduplicate_contacts",
  ]),
  "crm-deduplication must deploy only its CRM models, connectors, and deduplication plays",
);
assert.equal(
  byId.has("model:account_duplicate_candidates"),
  false,
  "deduplication must not deploy a duplicate-candidate staging model",
);
assert.equal(
  byId.has("model:contact_duplicate_candidates"),
  false,
  "deduplication must not deploy a contact-candidate staging model",
);
// Every merge decision rests on what the CRM returns during the run. A cached
// connector could serve `findRecords` a stale cluster, which is the one thing
// the fresh-source guard cannot catch.
for (const connectorId of ["connector:crm", "connector:slack"]) {
  assert.equal(
    byId.get(connectorId).spec.cacheTtlMilliseconds,
    undefined,
    `${connectorId} must not cache: a merge acts on what the CRM returns now`,
  );
}
for (const modelId of ["model:crm_accounts", "model:crm_contacts"]) {
  assert.equal(
    byId.get(modelId).spec.folderUuid.resourceId,
    "folder:crm_deduplication_models",
    `${modelId} must belong to the skill's model folder`,
  );
}
for (const playId of ["play:deduplicate_accounts", "play:deduplicate_contacts"]) {
  assert.equal(
    byId.get(playId).spec.folderUuid.resourceId,
    "folder:crm_deduplication_plays",
    `${playId} must belong to the skill's play folder`,
  );
}

const play = byId.get("play:deduplicate_accounts");
assert.equal(
  play.spec.modelUuid.resourceId,
  "model:crm_accounts",
  "deduplicate_accounts must run directly on the CRM account model",
);
assert.equal(play.spec.isEnabled, false, "the dedup play must be disabled");
assert.equal(play.spec.limit, 15, "the dedup pilot must be limited to 15 rows");
assert.equal(
  play.spec.runCreationRule,
  "noConcurrency",
  "the dedup play must run serially",
);

const nodes = play.spec.nodes;
const only = (predicate, message) => {
  const matches = nodes.filter(predicate);
  assert.equal(matches.length, 1, message);
  return matches[0];
};
const byUuid = (uuid) => nodes.find((node) => node.uuid === uuid);
const childrenOf = (node) => node.childrenUuids.map(byUuid);
const reachableFrom = (uuid, seen = new Set()) => {
  const node = byUuid(uuid);
  if (node === undefined || seen.has(node.uuid)) return seen;
  seen.add(node.uuid);
  for (const child of node.childrenUuids) reachableFrom(child, seen);
  return seen;
};
const isCrmAction = (actionSlug) => (node) =>
  node.kind === "connector" &&
  node.connectorUuid?.resourceId === "connector:crm" &&
  node.actionSlug === actionSlug;

// Search live, then reason about what came back. An audit snapshot can be
// stale by the time the row is dequeued.
const search = only(
  isCrmAction("findRecords"),
  "deduplicate_accounts must search the CRM with exactly one findRecords node",
);
const evidenceNode = childrenOf(search)[0];
assert.equal(
  evidenceNode.actionSlug,
  "script",
  "the CRM search must continue into deterministic evidence preparation",
);

const scoreNode = only(
  (node) => node.kind === "native" && node.actionSlug === "scoring",
  "duplicate evidence must be scored by exactly one native Scoring node",
);
assert.deepEqual(
  scoreNode.config.criterias.map(({ name, score }) => [
    name,
    score.expression,
  ]),
  [
    ["Exact LinkedIn company ID", "{{ 60 }}"],
    ["Exact LinkedIn company URL", "{{ 25 }}"],
    ["Exact non-generic domain", "{{ 15 }}"],
  ],
  "the native duplicate score must preserve the approved 60/25/15 policy",
);
// Survivor selection rides in the evidence script, so no script reads another
// script's output. That coupling is invisible in TypeScript and breaks the
// moment a node is inserted ahead of the one being read, so forbid it outright
// rather than test around it.
for (const node of nodes.filter((node) => node.actionSlug === "script")) {
  assert.doesNotMatch(
    node.config.script,
    /nodes\.script\b/,
    "no script may read another script through its compiler-assigned slug",
  );
}

// The evidence node must carry the bundle, not a hand-written body: that is
// what keeps the module this file imports and the code a run executes identical.
assert.match(
  evidenceNode.config.script,
  /Generated from evidence\.ts/,
  "the evidence node must be bundled from infra/scripts/accounts/evidence.ts",
);
// The script takes the search and the record ID as values; the SDK writes where
// each lives. Checked here because it is the one place the wiring is visible:
// the fresh search, not the enrolled extract, and the enrolled row's own ID.
assert.match(
  evidenceNode.config.script,
  new RegExp(
    `\\(\\{ records: nodes\\.${search.slug}, accountId: nodes\\.start\\.hs_object_id \\}`,
  ),
  "the evidence script must receive the live CRM search and the enrolled record ID",
);

// Automatic merge needs BOTH the score threshold and the exact-identity guard.
const gate = childrenOf(scoreNode)[0];
assert.equal(
  gate.actionSlug,
  "branch",
  "scoring must feed the guarded automatic-merge branch",
);
assert.match(
  gate.config.condition.expression,
  /scoring\.score >= 60.*autoEligible/,
  "automatic merge must require both the score threshold and the conflict guard",
);

const merges = nodes.filter(isCrmAction("mergeRecords"));
const mergeUuids = new Set(merges.map((merge) => merge.uuid));
assert.equal(
  merges.length,
  2,
  "deduplicate_accounts must expose exactly the automatic and human-approved merge paths",
);
for (const merge of merges) {
  assert.match(
    merge.config.primaryId.expression,
    /result\.primaryId/,
    "every CRM merge must use the selected survivor",
  );
  assert.match(
    merge.config.idsToMerge.expression,
    /result\.idsToMerge/,
    "every CRM merge must use the selected non-survivor IDs",
  );
}
assert.equal(
  mergeUuids.has(gate.childrenUuids[0]),
  true,
  "the guarded yes path must merge automatically",
);

const review = only(
  (node) => node.kind === "native" && node.actionSlug === "humanReview",
  "every other cluster must reach exactly one native Human review node",
);
assert.equal(
  gate.childrenUuids[1],
  review.uuid,
  "the guarded no path must request human review",
);
assert.equal(
  review.config.connectorUuid.resourceId,
  "connector:slack",
  "human review must post through the declared Slack review connector",
);
assert.match(
  review.config.content.expression,
  /Identity conflict:[\s\S]*Protected ID conflict:[\s\S]*Parent\/subsidiary warning:[\s\S]*Evidence:/,
  "the review message must show the score, every conflict, and the evidence",
);

const [approvedUuid, declinedUuid] = review.childrenUuids;
assert.equal(
  [...reachableFrom(approvedUuid)].some((uuid) => mergeUuids.has(uuid)),
  true,
  "approval must reach the reviewed merge",
);
assert.equal(
  [...reachableFrom(declinedUuid)].some((uuid) => mergeUuids.has(uuid)),
  false,
  "decline and timeout must never reach a CRM merge",
);

// The evidence module runs for real. Imported rather than reconstructed from
// the compiled node: calling `deriveEvidence(…)` bundles this exact module, so
// calling it here and calling it in a run are the same code — and because it
// takes values rather than reading `nodes.<slug>`, the test hands it values too.
const record = (id, properties = {}) => ({
  id,
  properties: {
    linkedin_company_id: "123",
    linkedin_company_page: "https://www.linkedin.com/company/acme",
    domain: "acme.com",
    lifecyclestage: "lead",
    hs_num_open_deals: 0,
    num_associated_contacts: 0,
    hs_num_engagements: 0,
    createdate: "2024-01-01T00:00:00.000Z",
    ...properties,
  },
});
const evidenceFor = (accountId, records) =>
  deriveEvidence({ records, accountId });

const exact = evidenceFor("account", [
  record("account"),
  record("customer", { lifecyclestage: "customer" }),
]);
assert.equal(exact.accountFound, true, "the account must be found in the fresh search");
assert.equal(exact.duplicateCount, 1, "the duplicate candidate must be kept");
assert.equal(
  exact.autoEligible,
  true,
  "an exact shared LinkedIn ID without conflicts must reach the automatic gate",
);

assert.equal(
  exact.primaryId,
  "customer",
  "survivor selection must apply the deterministic precedence",
);
assert.deepEqual(
  exact.idsToMerge,
  ["account"],
  "survivor selection must return every non-survivor ID",
);

const conflicting = evidenceFor("account", [
  record("account"),
  record("conflict", { domain: "other.example" }),
]);
assert.equal(
  conflicting.identityConflict,
  true,
  "conflicting non-null identity must be visible to the merge gate",
);
assert.equal(
  conflicting.autoEligible,
  false,
  "an identity conflict must require human review",
);

// One company page, written the ways a CRM ends up holding it. Each variant must
// read as the same page: a false conflict here sends a merge that should be
// automatic to review, and shows the reviewer a disagreement that is not real.
const samePage = evidenceFor("account", [
  record("account"),
  record("regional", {
    linkedin_company_page: "https://uk.linkedin.com/company/acme/about/",
  }),
  record("mobile", {
    linkedin_company_page: "https://m.linkedin.com/company/Acme?trk=feed",
  }),
]);
assert.equal(
  samePage.identityConflict,
  false,
  "a regional, mobile, or sub-page LinkedIn URL is the same company page",
);
assert.equal(
  samePage.exactLinkedinUrl,
  true,
  "every variant of one company page must agree",
);

const encodedPage = evidenceFor("account", [
  record("account", {
    linkedin_company_page:
      "https://www.linkedin.com/company/soci%C3%A9t%C3%A9-g%C3%A9n%C3%A9rale",
  }),
  record("decoded", {
    linkedin_company_page: "linkedin.com/company/Société-Générale",
  }),
]);
assert.equal(
  encodedPage.exactLinkedinUrl,
  true,
  "a percent-encoded company page must match its decoded form",
);

// A numeric page is LinkedIn's company ID, not a vanity handle: it agrees with
// the ID property rather than conflicting with the handle.
const numericPage = evidenceFor("account", [
  record("account"),
  record("by-id", {
    linkedin_company_id: undefined,
    linkedin_company_page: "https://www.linkedin.com/company/123",
  }),
]);
assert.equal(
  numericPage.identityConflict,
  false,
  "a numeric company page must not conflict with a vanity handle",
);
assert.equal(
  numericPage.exactLinkedinId,
  true,
  "a numeric company page must count as the company's LinkedIn ID",
);

const differentPages = evidenceFor("account", [
  record("account"),
  record("other", {
    linkedin_company_page: "https://www.linkedin.com/company/globex",
  }),
]);
assert.equal(
  differentPages.identityConflict,
  true,
  "two different company pages must still conflict",
);

const noLinkedin = { linkedin_company_id: "", linkedin_company_page: "" };
const genericDomain = evidenceFor("account", [
  record("account", { ...noLinkedin, domain: "google.com" }),
  record("other", { ...noLinkedin, domain: "google.com" }),
]);
assert.equal(
  genericDomain.duplicateCount,
  0,
  "a generic domain alone must never create a duplicate candidate",
);

const absorbed = evidenceFor("already-merged", [record("survivor")]);
assert.equal(
  absorbed.accountFound,
  false,
  "an account already absorbed by an earlier merge must stop before scoring",
);
// What "stop before scoring" has to mean downstream. The cluster itself is no
// longer in the payload — nothing at runtime read it — so assert the guarantee
// it stood for: an account the search no longer returns names nothing to merge.
assert.equal(
  absorbed.primaryId,
  undefined,
  "an account missing from the fresh search must never name a survivor",
);
assert.deepEqual(
  absorbed.idsToMerge,
  [],
  "an account missing from the fresh search must never emit a merge ID",
);

const contactPlay = byId.get("play:deduplicate_contacts");
assert.equal(
  contactPlay.spec.modelUuid.resourceId,
  "model:crm_contacts",
  "deduplicate_contacts must run directly on the CRM contact model",
);
assert.equal(contactPlay.spec.isEnabled, false, "the contact play must be disabled");
assert.equal(contactPlay.spec.limit, 15, "the contact pilot must be limited to 15 rows");
assert.equal(
  contactPlay.spec.runCreationRule,
  "noConcurrency",
  "the contact play must run serially",
);

const contactNodes = contactPlay.spec.nodes;
const contactOnly = (predicate, message) => {
  const matches = contactNodes.filter(predicate);
  assert.equal(matches.length, 1, message);
  return matches[0];
};
const contactByUuid = (uuid) =>
  contactNodes.find((node) => node.uuid === uuid);
const contactChildrenOf = (node) =>
  node.childrenUuids.map(contactByUuid).filter(Boolean);
const contactCrmAction = (actionSlug) => (node) =>
  node.kind === "connector" &&
  node.connectorUuid?.resourceId === "connector:crm" &&
  node.actionSlug === actionSlug;

const contactSearches = contactNodes.filter(contactCrmAction("findRecords"));
assert.equal(
  contactSearches.length,
  2,
  "contact deduplication must perform direct and transitive live CRM searches",
);
assert.equal(
  contactSearches.every((node) => node.config.objectType === "contacts"),
  true,
  "both contact searches must read live CRM contacts",
);

const contactScore = contactOnly(
  (node) => node.kind === "native" && node.actionSlug === "scoring",
  "contact evidence must be scored by one native Scoring node",
);
assert.deepEqual(
  contactScore.config.criterias.map(({ name, score }) => [
    name,
    score.expression,
  ]),
  [
    ["Exact LinkedIn person ID", "{{ 60 }}"],
    [
      "Exact LinkedIn person URL without person-ID conflict",
      "{{ 60 }}",
    ],
    [
      "Exact non-generic email without LinkedIn conflict",
      "{{ 60 }}",
    ],
    ["Transitive high-confidence chain", "{{ 60 }}"],
  ],
  "contact scoring must preserve the approved high-confidence classes",
);

const contactGate = contactChildrenOf(contactScore)[0];
assert.equal(
  contactGate.actionSlug,
  "branch",
  "contact scoring must feed the guarded automatic-merge branch",
);
assert.match(
  contactGate.config.condition.expression,
  /scoring\.score >= 60.*autoEligible/,
  "contact automatic merge must require both score and the global safety guard",
);

const contactMerges = contactNodes.filter(contactCrmAction("mergeRecords"));
const contactUpdates = contactNodes.filter(contactCrmAction("updateRecords"));
assert.equal(
  contactMerges.length,
  2,
  "contacts must merge only automatically or after approval",
);
assert.equal(
  contactUpdates.length,
  0,
  "contact merge paths must not create post-merge update nodes",
);

const contactReview = contactOnly(
  (node) => node.kind === "native" && node.actionSlug === "humanReview",
  "low-confidence contact clusters must reach one Human Review node when enabled",
);
assert.equal(
  contactReview.config.connectorUuid.resourceId,
  "connector:slack",
  "contact Human Review must use the declared Slack connector",
);
assert.match(
  contactReview.config.content.expression,
  /Conflicting LinkedIn person IDs:[\s\S]*Conflicting LinkedIn identity:[\s\S]*Generic or shared email:[\s\S]*Records:/,
  "contact review must show conflicts, generic-email risk, and formatted records",
);
assert.doesNotMatch(
  contactReview.config.content.expression,
  /\/100/,
  "contact score is additive and must not be displayed as a percentage",
);

const crmContact = (id, properties = {}) => ({
  id,
  properties: {
    email: "jack@example.com",
    phone: "(415) 555-0101",
    linkedin_url: "https://www.linkedin.com/in/jack-smith/",
    linkedin_person_id: "person-123",
    firstname: "Jack",
    lastname: "Smith",
    jobtitle: "VP Sales",
    associatedcompanyid: "company-1",
    num_associated_deals: 0,
    num_contacted_notes: 0,
    hs_sales_email_last_replied: 0,
    createdate: "2024-01-01T00:00:00.000Z",
    lastmodifieddate: "2024-01-01T00:00:00.000Z",
    ...properties,
  },
});
const contactEvidenceFor = (sourceId, directRecords, transitiveRecords = []) =>
  deriveContactEvidence({ sourceId, directRecords, transitiveRecords });

const exactContact = contactEvidenceFor("source", [
  crmContact("source", { email: "old@example.com" }),
  crmContact("history", {
    email: "new@example.com",
    num_associated_deals: 3,
    lastmodifieddate: "2024-02-01T00:00:00.000Z",
  }),
]);
assert.equal(
  exactContact.autoEligible,
  true,
  "an exact person ID without global conflicts must be automatic",
);
assert.equal(
  exactContact.primaryId,
  "history",
  "contact survivor selection must prefer commercial history",
);
assert.deepEqual(
  exactContact.idsToMerge,
  ["source"],
  "contact evidence must return every non-survivor ID",
);
assert.equal(
  Object.hasOwn(exactContact, "writeBackMappings"),
  false,
  "contact evidence must not prepare post-merge write-back mappings",
);

const genericEmailWithPersonId = contactEvidenceFor("source", [
  crmContact("source", { email: "INFO@example.com" }),
  crmContact("other", { email: "info@example.com" }),
]);
assert.equal(
  genericEmailWithPersonId.genericOrSharedEmail,
  true,
  "role-based email risk must be visible even when a person ID matches",
);
assert.equal(
  genericEmailWithPersonId.autoEligible,
  false,
  "the generic-email guard must apply to every automatic contact class",
);

const conflictingLinkedinWithPersonId = contactEvidenceFor("source", [
  crmContact("source"),
  crmContact("other", {
    linkedin_url: "https://linkedin.com/in/a-different-person",
  }),
]);
assert.equal(
  conflictingLinkedinWithPersonId.conflictingLinkedinIdentity,
  true,
  "conflicting LinkedIn URLs must be visible when person IDs match",
);
assert.equal(
  conflictingLinkedinWithPersonId.autoEligible,
  false,
  "the LinkedIn conflict guard must apply to every automatic contact class",
);

const transitiveContact = contactEvidenceFor(
  "a",
  [
    crmContact("a", {
      email: "",
      linkedin_url: "",
      linkedin_person_id: "person-1",
    }),
    crmContact("b", {
      email: "",
      linkedin_url: "https://linkedin.com/in/shared",
      linkedin_person_id: "person-1",
      num_associated_deals: 3,
    }),
  ],
  [
    crmContact("c", {
      email: "",
      linkedin_url: "https://www.linkedin.com/in/shared/",
      linkedin_person_id: "",
    }),
  ],
);
assert.equal(
  transitiveContact.transitiveHighConfidence,
  true,
  "pairwise high-confidence keys must form one transitive contact cluster",
);
assert.equal(
  transitiveContact.autoEligible,
  true,
  "a conflict-free transitive high-confidence cluster may merge automatically",
);
// The reviewer reads the enrolled contact first, then the records it gathered.
assert.equal(
  transitiveContact.reviewLines.length,
  3,
  "the review card must carry one line per record in the group",
);
assert.match(
  transitiveContact.reviewLines[0],
  /^a \|/,
  "the review card must lead with the enrolled contact",
);

const phoneOnlyContact = contactEvidenceFor("source", [
  crmContact("source", {
    email: "",
    linkedin_url: "",
    linkedin_person_id: "",
    phone: "06 12 34 56 78",
  }),
  crmContact("other", {
    email: "",
    linkedin_url: "",
    linkedin_person_id: "",
    phone: "+33 6 12 34 56 78",
  }),
]);
assert.equal(phoneOnlyContact.phoneOnly, true, "phone-only matches must be classified");
assert.equal(
  phoneOnlyContact.autoEligible,
  false,
  "phone-only matches must never merge automatically",
);

const staleContact = contactEvidenceFor("absorbed", [crmContact("survivor")]);
assert.equal(
  staleContact.sourceFound,
  false,
  "a contact missing from the fresh search must stop before scoring",
);
assert.deepEqual(
  staleContact.idsToMerge,
  [],
  "a missing contact must never emit merge IDs",
);

assert.deepEqual(
  prepareContactSearch({
    sourceId: "source",
    linkedinPersonId: undefined,
    linkedinUrl: "linkedin.com/in/Jack/",
    email: " JACK@Example.COM ",
    phone: undefined,
  }).linkedinUrlVariants,
  [
    "https://linkedin.com/in/jack",
    "https://linkedin.com/in/jack/",
    "https://www.linkedin.com/in/jack",
    "https://www.linkedin.com/in/jack/",
  ],
  "runtime search must enumerate normalized LinkedIn URL variants",
);
assert.equal(normalizeEmail(" JACK@Example.COM "), "jack@example.com");
assert.equal(
  normalizeLinkedinProfile(
    "https://www.linkedin.com/in/Jack-Smith/?trk=public",
  ),
  "jack-smith",
);
assert.equal(normalizePhone("(415) 555-0101"), "+14155550101");
assert.equal(phoneMatchKeys("06 12 34 56 78").includes("+33612345678"), true);
assert.equal(phoneMatchKeys("020 7946 0958").includes("+442079460958"), true);
assert.equal(phoneMatchKeys("0044 20 7946 0958").includes("+442079460958"), true);

console.log(
  "ok: crm-deduplication guards account and contact merges with live evidence",
);
