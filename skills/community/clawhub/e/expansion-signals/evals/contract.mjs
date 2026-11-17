import assert from "node:assert/strict";
import { resetRegistry, resources } from "@cargo-ai/cdk";

// The boundaries schema validation cannot express, checked against the
// compiled registry. Run it from the skill folder after every adaptation:
//   node --import tsx evals/contract.mjs
resetRegistry();
const stamp = Date.now();
await import(`../infra/plays/flag-expansion.ts?contract=${stamp}`);
await import(`../infra/agents/digest.ts?contract=${stamp}`);

const byId = new Map(resources().map((resource) => [resource.id, resource]));

const findOne = (nodes, predicate, message) => {
  const matches = nodes.filter(predicate);
  assert.equal(matches.length, 1, message);
  return matches[0];
};

// No CRM in the worked example: native models only, so it deploys with no
// connector key. A CRM swap is the `crm-backed` variation, not the default.
assert.equal(byId.has("connector:hubspot"), false, "the worked example has no HubSpot connector");
for (const [id, extractor] of [
  ["model:gtm_accounts", "defineAccount"],
  ["model:gtm_opportunities", "defineDeal"],
]) {
  const model = byId.get(id);
  assert.ok(model, `${id} must exist`);
  assert.equal(model.spec.datasetUuid, "native", `${id} is a native model`);
  assert.equal(model.spec.extractorSlug, extractor, `${id} uses ${extractor}`);
}

// The play: one agent judgment, one write onto the account record by id, the
// three expansion columns, and nothing else written anywhere.
const play = byId.get("play:flag_expansion");
assert.ok(play, "play:flag_expansion must exist");
assert.equal(play.spec.isEnabled, false, "the play ships disabled until the pilot is approved");
const nodes = play.spec.nodes;
findOne(
  nodes,
  (node) => node.kind === "agent" && node.agentUuid?.resourceId === "agent:expansion_analyst",
  "flag_expansion must call the analyst once",
);
assert.equal(
  nodes.filter((node) => node.kind === "connector").length,
  0,
  "flag_expansion calls no connector: no CRM write, no unify",
);
const writes = nodes.filter(
  (node) => node.kind === "native" && /^model/.test(node.actionSlug ?? ""),
);
assert.equal(writes.length, 1, "flag_expansion must own exactly one model write");
const [write] = writes;
assert.equal(write.actionSlug, "modelCustomColumn", "the write sets custom columns on one record by id");
assert.equal(
  write.config.modelUuid?.resourceId,
  "model:gtm_accounts",
  "only the account is written, never a deal or a contact",
);
assert.match(write.config.id?.expression ?? "", /account_id/, "the write targets the deal's account id");
assert.deepEqual(
  new Set(write.config.mappings.map((mapping) => mapping.columnSlug)),
  new Set(["expansion_signal", "expansion_reason", "expansion_signal_at"]),
  "the play writes only the three expansion columns, by bare slug",
);

// The analyst reads, never writes.
const analyst = byId.get("agent:expansion_analyst");
assert.ok(analyst, "agent:expansion_analyst must exist");
assert.equal((analyst.spec.connectorActions ?? []).length, 0, "the analyst has no connector action: the play writes");
for (const model of analyst.spec.models ?? []) {
  assert.equal(model.readOnly, true, "every model on the analyst is read-only");
}
const analystCaps = JSON.stringify(analyst.spec.capabilities ?? []);
assert.ok(analystCaps.includes("context"), "the analyst reads the expansion plays from the workspace context");
assert.ok(/"isReadOnly":\s*true/.test(analystCaps), "the context capability is read-only");
assert.equal(analyst.spec.output?.type, "jsonSchema", "the analyst answers in the JSON shape the play maps");

// The digest: one locked Slack post, a ledger it writes, the CRM read-only.
const digest = byId.get("agent:expansion_digest");
assert.ok(digest, "agent:expansion_digest must exist");
const digestActions = digest.spec.connectorActions ?? [];
const post = findOne(
  digestActions,
  (action) => action.integration === "slack" && action.actionSlug === "postMessage",
  "the digest must use slack.postMessage",
);
assert.equal(typeof post.config?.channelId, "string", "channelId must be locked on postMessage");
assert.notEqual(post.config.channelId, "", "channelId must not be empty");
assert.equal(
  digestActions.length,
  1,
  "the digest has no other action and no Slack read: the ledger is the dedupe",
);
const digestModels = digest.spec.models ?? [];
assert.equal(
  findOne(digestModels, (m) => m.uuid?.resourceId === "model:expansion_digests", "the digest writes its ledger").readOnly,
  false,
);
assert.equal(
  findOne(digestModels, (m) => m.uuid?.resourceId === "model:gtm_accounts", "the digest reads accounts").readOnly,
  true,
);
findOne(
  digest.spec.triggers ?? [],
  (trigger) => trigger.type === "cron",
  "the digest must have one cron trigger",
);

console.log("ok: expansion-signals contract");
