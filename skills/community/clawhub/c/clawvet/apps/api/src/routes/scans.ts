import type { FastifyInstance } from "fastify";
import { scanSkill } from "../services/scanner.js";
import { resolveUser } from "../services/resolve-user.js";
import { getPlanLimits, getCurrentPeriodStart } from "../services/tiers.js";
import { eq, and, gte, count as drizzleCount } from "drizzle-orm";
import { desc } from "drizzle-orm";

interface ScanBody {
  content: string;
  semantic?: boolean;
  skillName?: string;
}

async function getUserScanCount(userId: string): Promise<number> {
  try {
    const { db, schema } = await import("../db/index.js");
    const periodStart = getCurrentPeriodStart();
    const [result] = await db
      .select({ count: drizzleCount(schema.scans.id) })
      .from(schema.scans)
      .where(
        and(
          eq(schema.scans.userId, userId),
          gte(schema.scans.createdAt, periodStart)
        )
      );
    return Number(result?.count || 0);
  } catch {
    return 0;
  }
}

export async function scanRoutes(app: FastifyInstance) {
  app.post<{ Body: ScanBody }>("/api/v1/scans", async (request, reply) => {
    const { content, semantic, skillName } = request.body;

    if (!content) {
      return reply.status(400).send({ error: "content is required" });
    }

    const user = await resolveUser(request);
    const plan = user ? getPlanLimits(user.plan) : getPlanLimits("free");

    if (user && plan.apiScansPerMonth !== Infinity) {
      const used = await getUserScanCount(user.id);
      if (used >= plan.apiScansPerMonth) {
        return reply.status(429).send({
          error: "Monthly scan limit reached",
          limit: plan.apiScansPerMonth,
          used,
          upgrade: "Upgrade to Pro for unlimited scans: https://clawvet.dev/pricing",
        });
      }
    }

    let semanticEnabled = false;
    let semanticPreviewed = false;

    if (semantic) {
      if (plan.semanticScans) {
        semanticEnabled = true;
      } else if (plan.semanticPreview) {
        semanticEnabled = true;
        semanticPreviewed = true;
      }
    }

    const result = await scanSkill(content, { semantic: semanticEnabled });
    if (skillName) {
      result.skillName = skillName;
    }

    if (semanticPreviewed && result.findings.length > 0) {
      const semanticFindings = result.findings.filter(
        (f) => f.analysisPass === "semantic-analysis"
      );
      const otherFindings = result.findings.filter(
        (f) => f.analysisPass !== "semantic-analysis"
      );

      const previewCount = plan.semanticPreviewCount as number;
      const visibleSemantic = semanticFindings.slice(0, previewCount);
      const hiddenCount = semanticFindings.length - visibleSemantic.length;

      const redactedSemantic = visibleSemantic.map((f) => ({
        ...f,
        _preview: true,
      }));

      result.findings = [...otherFindings, ...redactedSemantic];

      (result as any).semanticPreview = {
        shown: visibleSemantic.length,
        hidden: hiddenCount,
        total: semanticFindings.length,
        message:
          hiddenCount > 0
            ? `${hiddenCount} more AI finding${hiddenCount > 1 ? "s" : ""} hidden. Upgrade to Pro to see all semantic analysis results.`
            : "Upgrade to Pro for unlimited AI-powered semantic analysis.",
        upgrade: "https://clawvet.dev/pricing",
      };
    }

    if (user) {
      (result as any).tier = {
        plan: user.plan,
        semanticEnabled: plan.semanticScans,
        apiScansLimit: plan.apiScansPerMonth === Infinity ? "unlimited" : plan.apiScansPerMonth,
      };
    } else {
      (result as any).tier = {
        plan: "anonymous",
        semanticEnabled: false,
        apiScansLimit: "unlimited",
        note: "Sign in with GitHub to track usage and access premium features",
      };
    }

    try {
      const { db, schema } = await import("../db/index.js");
      const [scan] = await db
        .insert(schema.scans)
        .values({
          skillName: result.skillName,
          skillVersion: result.skillVersion || null,
          skillSource: result.skillSource,
          status: "complete",
          riskScore: result.riskScore,
          riskGrade: result.riskGrade,
          findingsCount: result.findingsCount,
          userId: user?.id || null,
          completedAt: new Date(),
        })
        .returning();

      result.id = scan.id;

      if (result.findings.length > 0) {
        await db.insert(schema.findings).values(
          result.findings.map((f) => ({
            scanId: scan.id,
            category: f.category,
            severity: f.severity,
            title: f.title,
            description: f.description,
            evidence: f.evidence || null,
            lineNumber: f.lineNumber ?? null,
            analysisPass: f.analysisPass,
          }))
        );
      }
    } catch {
      // DB not available — return result without persistence
    }

    return reply.status(200).send(result);
  });

  app.get<{ Params: { id: string } }>(
    "/api/v1/scans/:id",
    async (request, reply) => {
      try {
        const { db, schema } = await import("../db/index.js");
        const scan = await db.query.scans.findFirst({
          where: eq(schema.scans.id, request.params.id),
        });

        if (!scan) {
          return reply.status(404).send({ error: "Scan not found" });
        }

        const scanFindings = await db.query.findings.findMany({
          where: eq(schema.findings.scanId, scan.id),
        });

        return reply.send({
          ...scan,
          findings: scanFindings.map((f) => ({
            category: f.category,
            severity: f.severity,
            title: f.title,
            description: f.description,
            evidence: f.evidence,
            lineNumber: f.lineNumber,
            analysisPass: f.analysisPass,
          })),
        });
      } catch {
        return reply
          .status(503)
          .send({ error: "Database not available" });
      }
    }
  );

  app.get<{ Querystring: { limit?: string; offset?: string } }>(
    "/api/v1/scans",
    async (request, reply) => {
      try {
        const { db, schema } = await import("../db/index.js");
        const limit = Math.min(parseInt(request.query.limit || "20"), 100);
        const offset = parseInt(request.query.offset || "0");

        const results = await db.query.scans.findMany({
          orderBy: desc(schema.scans.createdAt),
          limit,
          offset,
        });

        return reply.send({ scans: results, limit, offset });
      } catch {
        return reply
          .status(503)
          .send({ error: "Database not available" });
      }
    }
  );

  app.get("/api/v1/stats", async (request, reply) => {
    try {
      const { db, schema } = await import("../db/index.js");
      const { count, avg } = await import("drizzle-orm");

      const [stats] = await db
        .select({
          skillsScanned: count(schema.scans.id),
          avgRiskScore: avg(schema.scans.riskScore),
        })
        .from(schema.scans)
        .where(eq(schema.scans.status, "complete"));

      const [threatStats] = await db
        .select({ threatsFound: count(schema.findings.id) })
        .from(schema.findings);

      return reply.send({
        skillsScanned: Number(stats.skillsScanned),
        threatsFound: Number(threatStats.threatsFound),
        avgRiskScore: Math.round(Number(stats.avgRiskScore) || 0),
      });
    } catch {
      return reply.send({
        skillsScanned: 0,
        threatsFound: 0,
        avgRiskScore: 0,
      });
    }
  });
}
