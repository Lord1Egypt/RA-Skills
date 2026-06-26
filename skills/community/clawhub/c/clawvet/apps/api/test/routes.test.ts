import { describe, it, expect, beforeAll, afterAll } from "vitest";
import Fastify from "fastify";
import { scanRoutes } from "../src/routes/scans.js";
import { authRoutes } from "../src/routes/auth.js";
import { webhookRoutes } from "../src/routes/webhooks.js";
import { skillRoutes } from "../src/routes/skills.js";

describe("auth routes", () => {
  const app = Fastify();
  beforeAll(async () => {
    await app.register(authRoutes);
    await app.ready();
  });
  afterAll(() => app.close());

  it("GET /api/v1/auth/github returns 503 when not configured", async () => {
    const res = await app.inject({ method: "GET", url: "/api/v1/auth/github" });
    expect(res.statusCode).toBe(503);
    expect(JSON.parse(res.payload).error).toContain("not configured");
  });

  it("GET /api/v1/auth/github/callback returns 400 without code", async () => {
    const res = await app.inject({
      method: "GET",
      url: "/api/v1/auth/github/callback",
    });
    expect(res.statusCode).toBe(400);
  });

  it("GET /api/v1/auth/me returns 401 without auth header", async () => {
    const res = await app.inject({ method: "GET", url: "/api/v1/auth/me" });
    expect(res.statusCode).toBe(401);
  });

  it("GET /api/v1/auth/me returns 401 with bad key", async () => {
    const res = await app.inject({
      method: "GET",
      url: "/api/v1/auth/me",
      headers: { authorization: "Bearer cg_invalid" },
    });
    // 503 (db unavailable) or 401 — both acceptable without DB
    expect([401, 503]).toContain(res.statusCode);
  });
});

describe("webhook routes", () => {
  const app = Fastify();
  beforeAll(async () => {
    await app.register(webhookRoutes);
    await app.ready();
  });
  afterAll(() => app.close());

  it("POST /api/v1/webhooks returns 401 without auth", async () => {
    const res = await app.inject({
      method: "POST",
      url: "/api/v1/webhooks",
      payload: { url: "https://example.com/hook", events: ["scan.complete"] },
    });
    expect(res.statusCode).toBe(401);
  });

  it("GET /api/v1/webhooks returns 401 without auth", async () => {
    const res = await app.inject({ method: "GET", url: "/api/v1/webhooks" });
    expect(res.statusCode).toBe(401);
  });

  it("DELETE /api/v1/webhooks/:id returns 401 without auth", async () => {
    const res = await app.inject({
      method: "DELETE",
      url: "/api/v1/webhooks/some-id",
    });
    expect(res.statusCode).toBe(401);
  });
});

describe("skill routes", () => {
  const app = Fastify();
  beforeAll(async () => {
    await app.register(skillRoutes);
    await app.ready();
  });
  afterAll(() => app.close());

  it("GET /api/v1/skills/:slug returns 404 for unknown skill", { timeout: 25000 }, async () => {
    const res = await app.inject({
      method: "GET",
      url: "/api/v1/skills/nonexistent-skill-xyz-99999",
    });
    expect(res.statusCode).toBe(404);
    expect(JSON.parse(res.payload).error).toContain("not found");
  });
});

describe("scan routes — input validation", () => {
  const app = Fastify();
  beforeAll(async () => {
    await app.register(scanRoutes);
    await app.ready();
  });
  afterAll(() => app.close());

  it("POST /api/v1/scans with empty string content returns 400", async () => {
    const res = await app.inject({
      method: "POST",
      url: "/api/v1/scans",
      payload: { content: "" },
    });
    // Empty string is falsy, should be rejected
    expect(res.statusCode).toBe(400);
  });

  it("POST /api/v1/scans with huge content still works", async () => {
    const content = `---\nname: big\n---\n${"x".repeat(100000)}`;
    const res = await app.inject({
      method: "POST",
      url: "/api/v1/scans",
      payload: { content },
    });
    expect(res.statusCode).toBe(200);
    const body = JSON.parse(res.payload);
    expect(body.status).toBe("complete");
  });

  it("POST /api/v1/scans allows overriding skillName", async () => {
    const res = await app.inject({
      method: "POST",
      url: "/api/v1/scans",
      payload: {
        content: "---\nname: original\n---\nHello",
        skillName: "override-name",
      },
    });
    expect(res.statusCode).toBe(200);
    const body = JSON.parse(res.payload);
    expect(body.skillName).toBe("override-name");
  });

  it("GET /api/v1/scans returns 503 without DB", async () => {
    const res = await app.inject({ method: "GET", url: "/api/v1/scans" });
    expect(res.statusCode).toBe(503);
  });

  it("GET /api/v1/stats returns zeros without DB", async () => {
    const res = await app.inject({ method: "GET", url: "/api/v1/stats" });
    expect(res.statusCode).toBe(200);
    const body = JSON.parse(res.payload);
    expect(body.skillsScanned).toBe(0);
  });
});
