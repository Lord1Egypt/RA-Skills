import { Queue } from "bullmq";
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

export const scanQueue = new Queue("scans", { connection });

export async function enqueueScan(data: {
  scanId: string;
  content: string;
  semantic?: boolean;
}) {
  return scanQueue.add("scan-skill", data, {
    attempts: 3,
    backoff: { type: "exponential", delay: 1000 },
  });
}
