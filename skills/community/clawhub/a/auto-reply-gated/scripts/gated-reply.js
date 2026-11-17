#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

function value(flag) {
  const i = process.argv.indexOf(flag);
  return i >= 0 ? process.argv[i + 1] : undefined;
}
function fail(message) {
  process.stderr.write(message + "\n");
  process.exit(1);
}
const command = process.argv[2];
if (command === "draft") {
  const recipient = value("--recipient");
  const message = value("--message");
  if (!recipient || !message) fail("recipient and message are required");
  const draft = {
    id: crypto.randomUUID(),
    recipient,
    message,
    status: "pending_human_approval",
    approvedBy: null,
    approvedAt: null,
    createdAt: new Date().toISOString()
  };
  const dir = path.resolve(process.cwd(), "drafts");
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, draft.id + ".json");
  fs.writeFileSync(file, JSON.stringify(draft, null, 2), { mode: 0o600 });
  process.stdout.write(JSON.stringify({ file, draft }, null, 2) + "\n");
} else if (command === "approve") {
  const file = value("--file");
  const approvedBy = value("--approved-by");
  if (!file || !approvedBy) fail("file and approved-by are required");
  const draft = JSON.parse(fs.readFileSync(path.resolve(file), "utf8"));
  if (draft.status !== "pending_human_approval") fail("draft is not pending approval");
  draft.status = "approved_for_manual_send";
  draft.approvedBy = approvedBy;
  draft.approvedAt = new Date().toISOString();
  fs.writeFileSync(path.resolve(file), JSON.stringify(draft, null, 2), { mode: 0o600 });
  process.stdout.write(JSON.stringify(draft, null, 2) + "\n");
} else if (command === "export") {
  const file = value("--file");
  if (!file) fail("file is required");
  const draft = JSON.parse(fs.readFileSync(path.resolve(file), "utf8"));
  if (draft.status !== "approved_for_manual_send" || !draft.approvedBy) fail("explicit human approval is required");
  process.stdout.write(JSON.stringify({
    action: "manual_send_required",
    recipient: draft.recipient,
    message: draft.message,
    approvedBy: draft.approvedBy,
    approvedAt: draft.approvedAt
  }, null, 2) + "\n");
} else {
  fail("usage: gated-reply.js draft|approve|export");
}
