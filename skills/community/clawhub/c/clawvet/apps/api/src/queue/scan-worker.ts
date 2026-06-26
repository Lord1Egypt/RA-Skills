import { Worker } from "bullmq";
import { eq } from "drizzle-orm";
import { scanSkill } from "../services/scanner.js";
import { db, schema } from "../db/index.js";

const redisUrl = new URL(process.env.REDIS_URL || "redis://localhost:6379");

const connection = {
  host: redisUrl.hostname,
  port: Number(redisUrl.port || 6379),
  username: redisUrl.username || undefined,
  password: redisUrl.password || undefined,
  db: redisUrl.pathname ? Number(redisUrl.pathname.replace("/", "") || 0) : 0,
  maxRetriesPerRequest: null,
  ...(redisUrl.protocol === "rediss:" && { tls: {} }),
};

const worker = new Worker(
  "scans",
  async (job) => {
    const { scanId, content, semantic } = job.data;
    console.log(`Processing scan ${scanId}`);

    // Mark as scanning
    await db
      .update(schema.scans)
      .set({ status: "scanning" })
      .where(eq(schema.scans.id, scanId));

    try {
      const result = await scanSkill(content, { semantic });

      // Update scan record
      await db
        .update(schema.scans)
        .set({
          status: "complete",
          riskScore: result.riskScore,
          riskGrade: result.riskGrade,
          findingsCount: result.findingsCount,
          skillName: result.skillName,
          skillVersion: result.skillVersion || null,
          completedAt: new Date(),
        })
        .where(eq(schema.scans.id, scanId));

      // Insert findings
      if (result.findings.length > 0) {
        await db.insert(schema.findings).values(
          result.findings.map((f) => ({
            scanId,
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

      // Fire webhooks for this user's scan
      const scan = await db.query.scans.findFirst({
        where: eq(schema.scans.id, scanId),
      });

      if (scan?.userId) {
        await fireWebhooks(scan.userId, scanId, result);
      }

      console.log(
        `Scan ${scanId} complete: score=${result.riskScore} grade=${result.riskGrade}`
      );
      return result;
    } catch (err) {
      await db
        .update(schema.scans)
        .set({ status: "failed" })
        .where(eq(schema.scans.id, scanId));
      throw err;
    }
  },
  { connection, concurrency: 5 }
);

async function fireWebhooks(
  userId: string,
  scanId: string,
  result: Awaited<ReturnType<typeof scanSkill>>
) {
  const hooks = await db.query.webhooks.findMany({
    where: eq(schema.webhooks.userId, userId),
  });

  for (const hook of hooks) {
    if (!hook.active) continue;

    const events = hook.events as string[];
    const shouldFire =
      events.includes("scan.complete") ||
      (events.includes("scan.critical") &&
        result.findingsCount.critical > 0);

    if (!shouldFire) continue;

    try {
      await fetch(hook.url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          event: result.findingsCount.critical > 0
            ? "scan.critical"
            : "scan.complete",
          scanId,
          skillName: result.skillName,
          riskScore: result.riskScore,
          riskGrade: result.riskGrade,
          findingsCount: result.findingsCount,
          recommendation: result.recommendation,
        }),
        signal: AbortSignal.timeout(10000),
      });
    } catch (err) {
      console.error(`Webhook delivery to ${hook.url} failed:`, err);
    }
  }
}

worker.on("completed", (job) => {
  console.log(`Job ${job.id} completed`);
});

worker.on("failed", (job, err) => {
  console.error(`Job ${job?.id} failed:`, err);
});

export { worker };
