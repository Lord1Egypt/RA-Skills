import type { FastifyRequest } from "fastify";
import { eq } from "drizzle-orm";
import { createHmac } from "node:crypto";

const JWT_SECRET = process.env.JWT_SECRET || "clawvet-dev-secret-change-me";

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

export interface ResolvedUser {
  id: string;
  githubUsername: string;
  plan: string;
  apiKey: string | null;
}

export async function resolveUser(
  request: FastifyRequest
): Promise<ResolvedUser | null> {
  const cookie = (request.headers.cookie || "")
    .split(";")
    .map((c) => c.trim())
    .find((c) => c.startsWith("cg_session="));
  const jwtToken = cookie?.split("=")[1];

  const authHeader = request.headers.authorization;
  const apiKey = authHeader?.startsWith("Bearer cg_")
    ? authHeader.slice(7)
    : null;

  if (!jwtToken && !apiKey) return null;

  try {
    const { db, schema } = await import("../db/index.js");

    if (jwtToken) {
      const claims = verifyJwt(jwtToken);
      if (!claims?.sub) return null;
      const user = await db.query.users.findFirst({
        where: eq(schema.users.id, claims.sub as string),
      });
      if (!user) return null;
      return {
        id: user.id,
        githubUsername: user.githubUsername,
        plan: user.plan || "free",
        apiKey: user.apiKey,
      };
    }

    const user = await db.query.users.findFirst({
      where: eq(schema.users.apiKey, apiKey!),
    });
    if (!user) return null;
    return {
      id: user.id,
      githubUsername: user.githubUsername,
      plan: user.plan || "free",
      apiKey: user.apiKey,
    };
  } catch {
    return null;
  }
}
