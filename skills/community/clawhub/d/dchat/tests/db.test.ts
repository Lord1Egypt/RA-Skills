import { describe, it, expect, beforeEach, afterEach } from "vitest";
import fs from "fs";
import os from "os";
import path from "path";
import { MessageDb } from "../src/db.js";

describe("MessageDb", () => {
  let db: MessageDb;
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "dchat-test-"));
    db = new MessageDb(tmpDir);
  });

  afterEach(() => {
    db.close();
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it("inserts and retrieves messages", () => {
    db.insertMessage({
      id: "msg-1",
      sender: "alice",
      receiver: "bob",
      contentType: "text",
      content: "hello",
      status: "sent",
      isOutbound: true,
      createdAt: 1000,
    });

    const msgs = db.getMessages("alice", 10);
    expect(msgs).toHaveLength(1);
    expect(msgs[0].content).toBe("hello");
    expect(msgs[0].isOutbound).toBe(true);
  });

  it("deduplicates by message id", () => {
    const msg = {
      id: "msg-dup",
      sender: "alice",
      receiver: "bob",
      contentType: "text" as const,
      content: "hello",
      status: "sent" as const,
      isOutbound: true,
      createdAt: 1000,
    };
    db.insertMessage(msg);
    db.insertMessage(msg); // duplicate
    expect(db.getMessages("alice", 10)).toHaveLength(1);
  });

  it("hasMessage works", () => {
    expect(db.hasMessage("nonexistent")).toBe(false);
    db.insertMessage({
      id: "exists",
      sender: "a",
      receiver: "b",
      contentType: "text",
      content: "",
      status: "sent",
      isOutbound: true,
      createdAt: 1000,
    });
    expect(db.hasMessage("exists")).toBe(true);
  });

  it("updates status", () => {
    db.insertMessage({
      id: "msg-status",
      sender: "a",
      receiver: "b",
      contentType: "text",
      content: "hi",
      status: "sending",
      isOutbound: true,
      createdAt: 1000,
    });
    db.updateStatus("msg-status", "delivered");
    const msgs = db.getMessages("a", 10);
    expect(msgs[0].status).toBe("delivered");
  });

  it("burns expired messages", () => {
    db.insertMessage({
      id: "burn-me",
      sender: "a",
      receiver: "b",
      contentType: "text",
      content: "secret",
      status: "delivered",
      isOutbound: false,
      deleteAt: Date.now() - 1000, // already expired
      createdAt: 1000,
    });

    const burned = db.burnExpired();
    expect(burned).toEqual(["burn-me"]);

    // Should not appear in messages
    const msgs = db.getMessages("a", 10);
    expect(msgs).toHaveLength(0);
  });

  it("upserts peers", () => {
    db.upsertPeer("alice.nkn", "Alice");
    db.upsertPeer("alice.nkn", "Alice Bot"); // update name
    // No error = success (we don't expose peer reads yet)
  });
});
