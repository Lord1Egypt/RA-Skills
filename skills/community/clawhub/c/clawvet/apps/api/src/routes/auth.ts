import type { FastifyInstance } from "fastify";
import { eq } from "drizzle-orm";
import { randomBytes, createHmac } from "node:crypto";

const GITHUB_CLIENT_ID = process.env.GITHUB_CLIENT_ID || "";
const GITHUB_CLIENT_SECRET = process.env.GITHUB_CLIENT_SECRET || "";
const GITHUB_REDIRECT_URI =
  process.env.GITHUB_REDIRECT_URI ||
  "http://localhost:3001/api/v1/auth/github/callback";
const JWT_SECRET = process.env.JWT_SECRET || "clawvet-dev-secret-change-me";
const WEB_URL = process.env.WEB_URL || "http://localhost:3000";

function signJwt(payload: Record<string, unknown>, expiresInHours = 168): string {
  const header = { alg: "HS256", typ: "JWT" };
  const now = Math.floor(Date.now() / 1000);
  const claims = { ...payload, iat: now, exp: now + expiresInHours * 3600 };

  const b64 = (obj: unknown) =>
    Buffer.from(JSON.stringify(obj)).toString("base64url");

  const unsigned = `${b64(header)}.${b64(claims)}`;
  const sig = createHmac("sha256", JWT_SECRET)
    .update(unsigned)
    .digest("base64url");
  return `${unsigned}.${sig}`;
}

function verifyJwt(token: string): Record<string, unknown> | null {
  try {
    const [headerB64, claimsB64, sig] = token.split(".");
    if (!headerB64 || !claimsB64 || !sig) return null;

    const expected = createHmac("sha256", JWT_SECRET)
      .update(`${headerB64}.${claimsB64}`)
      .digest("base64url");

    if (sig !== expected) return null;

    const claims = JSON.parse(Buffer.from(claimsB64, "base64url").toString());
    if (claims.exp && claims.exp < Math.floor(Date.now() / 1000)) return null;

    return claims;
  } catch {
    return null;
  }
}

export async function authRoutes(app: FastifyInstance) {
  app.get("/api/v1/auth/github", async (request, reply) => {
    if (!GITHUB_CLIENT_ID) {
      return reply
        .status(503)
        .send({ error: "GitHub OAuth not configured. Set GITHUB_CLIENT_ID." });
    }

    const params = new URLSearchParams({
      client_id: GITHUB_CLIENT_ID,
      redirect_uri: GITHUB_REDIRECT_URI,
      scope: "read:user user:email",
    });

    return reply.redirect(
      `https://github.com/login/oauth/authorize?${params}`
    );
  });

  app.get<{ Querystring: { code?: string } }>(
    "/api/v1/auth/github/callback",
    async (request, reply) => {
      const { code } = request.query;
      if (!code) {
        return reply.status(400).send({ error: "Missing code parameter" });
      }

      if (!GITHUB_CLIENT_ID || !GITHUB_CLIENT_SECRET) {
        return reply
          .status(503)
          .send({ error: "GitHub OAuth not configured" });
      }

      const tokenRes = await fetch(
        "https://github.com/login/oauth/access_token",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({
            client_id: GITHUB_CLIENT_ID,
            client_secret: GITHUB_CLIENT_SECRET,
            code,
            redirect_uri: GITHUB_REDIRECT_URI,
          }),
        }
      );

      const tokenData = (await tokenRes.json()) as {
        access_token?: string;
        error?: string;
      };
      if (!tokenData.access_token) {
        return reply
          .status(400)
          .send({ error: tokenData.error || "Failed to get access token" });
      }

      const userRes = await fetch("https://api.github.com/user", {
        headers: { Authorization: `Bearer ${tokenData.access_token}` },
      });
      const ghUser = (await userRes.json()) as {
        id: number;
        login: string;
        email?: string;
      };

      try {
        const { db, schema } = await import("../db/index.js");

        let user = await db.query.users.findFirst({
          where: eq(schema.users.githubId, String(ghUser.id)),
        });

        if (!user) {
          const apiKey = `cg_${randomBytes(24).toString("hex")}`;
          const [newUser] = await db
            .insert(schema.users)
            .values({
              githubId: String(ghUser.id),
              githubUsername: ghUser.login,
              email: ghUser.email || null,
              apiKey,
            })
            .returning();
          user = newUser;
        }

        const jwt = signJwt({
          sub: user.id,
          username: user.githubUsername,
          plan: user.plan,
        });

        reply.header(
          "Set-Cookie",
          `cg_session=${jwt}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${7 * 86400}${
            process.env.NODE_ENV === "production" ? "; Secure" : ""
          }`
        );

        return reply.redirect(`${WEB_URL}/dashboard`);
      } catch {
        return reply.status(503).send({ error: "Database not available" });
      }
    }
  );

  app.get("/api/v1/auth/me", async (request, reply) => {
    const cookie = (request.headers.cookie || "")
      .split(";")
      .map((c) => c.trim())
      .find((c) => c.startsWith("cg_session="));
    const jwtToken = cookie?.split("=")[1];

    const authHeader = request.headers.authorization;
    const apiKey = authHeader?.startsWith("Bearer cg_")
      ? authHeader.slice(7)
      : null;

    if (!jwtToken && !apiKey) {
      return reply.status(401).send({ error: "Missing or invalid API key" });
    }

    try {
      const { db, schema } = await import("../db/index.js");

      if (jwtToken) {
        const claims = verifyJwt(jwtToken);
        if (!claims?.sub) {
          return reply.status(401).send({ error: "Invalid or expired session" });
        }
        const user = await db.query.users.findFirst({
          where: eq(schema.users.id, claims.sub as string),
        });
        if (!user) {
          return reply.status(401).send({ error: "User not found" });
        }
        return reply.send({
          id: user.id,
          githubUsername: user.githubUsername,
          email: user.email,
          plan: user.plan,
          apiKey: user.apiKey,
          createdAt: user.createdAt,
        });
      }

      const user = await db.query.users.findFirst({
        where: eq(schema.users.apiKey, apiKey!),
      });

      if (!user) {
        return reply.status(401).send({ error: "Invalid API key" });
      }

      return reply.send({
        id: user.id,
        githubUsername: user.githubUsername,
        email: user.email,
        plan: user.plan,
        apiKey: user.apiKey,
        createdAt: user.createdAt,
      });
    } catch {
      return reply.status(503).send({ error: "Database not available" });
    }
  });

  app.post("/api/v1/auth/logout", async (request, reply) => {
    reply.header(
      "Set-Cookie",
      "cg_session=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0"
    );
    return reply.send({ ok: true });
  });
}
