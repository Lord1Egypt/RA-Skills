import assert from "node:assert/strict";
import { resetRegistry, resources } from "@cargo-ai/cdk";

resetRegistry();
await import(`../infra/agents/engager.ts?contract=${Date.now()}`);

const byId = new Map(resources().map((resource) => [resource.id, resource]));

const findOne = (nodes, predicate, message) => {
  const matches = nodes.filter(predicate);
  assert.equal(matches.length, 1, message);
  return matches[0];
};

assert.ok(byId.get("domain:example-outreach.com"), "defineDomain must exist");
assert.ok(byId.get("mailbox:rep"), "defineMailbox(rep) must exist");
assert.equal(
  byId.has("tool:send-email"),
  false,
  "sendEmail must be a native action on the agent, not a wrapped tool",
);
assert.equal(
  byId.has("folder:agentic-engagement-tools"),
  false,
  "the tools folder must not exist once the send wrapper is gone",
);

const agent = byId.get("agent:engager");
assert.ok(agent, "defineAgent(engager) must exist");

const nativeActions = agent.spec.nativeActions ?? [];
const send = findOne(
  nativeActions,
  (action) => action.actionSlug === "sendEmail",
  "engager must use native sendEmail",
);
assert.ok(
  send.config?.mailboxUuid,
  "mailboxUuid must be locked on the sendEmail use, not left for the agent to pick",
);
findOne(
  nativeActions,
  (action) => action.actionSlug === "listEmailEvents",
  "engager must use native listEmailEvents so a heartbeat can read thread status",
);
assert.equal(
  (agent.spec.tools ?? []).length,
  0,
  "engager must not wrap sendEmail in a tool",
);

const nativeEmail = findOne(
  agent.spec.triggers,
  (trigger) => trigger.type === "native" && trigger.agentSlug === "email",
  "engager must have exactly one native email trigger",
);
assert.deepEqual(
  nativeEmail.config?.kinds,
  ["replied", "unsubscribed"],
  "the native email trigger must wake on replied and unsubscribed, not opens",
);
assert.equal(
  nativeEmail.config.kinds.includes("opened"),
  false,
  "opened must not be a trigger kind",
);
assert.equal(
  nativeEmail.config.kinds.includes("interacted"),
  false,
  "interacted must not be a trigger kind",
);

const heartbeat = agent.spec.heartbeat;
assert.ok(heartbeat, "engager must declare a heartbeat — silence has no event");
assert.equal(typeof heartbeat.intervalMinutes, "number");
assert.ok(
  heartbeat.intervalMinutes >= 60,
  "heartbeat interval must be at least an hour, not a poll loop",
);
assert.ok(
  heartbeat.maxMessages >= 4,
  "heartbeat maxMessages must allow a first send plus a short thread",
);
assert.equal(typeof heartbeat.prompt, "string");
assert.match(
  heartbeat.prompt,
  /listEmailEvents/i,
  "heartbeat prompt must tell the agent to list thread events",
);

console.log("ok: agentic-engagement contract");
