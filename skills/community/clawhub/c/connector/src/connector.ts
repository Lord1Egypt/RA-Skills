import { mkdir, readFile, writeFile } from "node:fs/promises";
import { createHmac } from "node:crypto";
import { homedir } from "node:os";
import { dirname } from "node:path";
import { join } from "node:path";
import { setTimeout as delay } from "node:timers/promises";
import { z } from "zod";

const eventSchema = z.object({
  eventId: z.string(),
  eventType: z.enum([
    "agent_status_changed",
    "agent_moved_room",
    "task_started",
    "task_completed",
    "room_updated",
  ]),
  occurredAt: z.number().int(),
  idempotencyKey: z.string().optional(),
  agent: z
    .object({
      agentId: z.string(),
      name: z.string(),
      role: z.string().optional(),
      status: z.enum(["active", "idle", "meeting"]).optional(),
      roomId: z.string().optional(),
    })
    .optional(),
  room: z
    .object({
      roomId: z.string(),
      name: z.string(),
      occupancyCount: z.number().int().optional(),
    })
    .optional(),
  task: z
    .object({
      taskId: z.string(),
      title: z.string(),
      status: z.enum(["started", "completed"]).optional(),
    })
    .optional(),
  metadata: z.record(z.string(), z.string()).optional(),
});

export type ConnectorEvent = z.infer<typeof eventSchema>;

const connectorConfigSchema = z.object({
  launchThatBaseUrl: z.string().url(),
  workspaceId: z.string().min(1),
  instanceId: z.string().min(1),
  ingestToken: z.string().min(1),
  signingSecret: z.string().min(16).optional(),
  heartbeatIntervalMs: z.number().int().min(5_000).default(30_000),
  queueFilePath: z
    .string()
    .default(join(homedir(), ".config", "launchthat-openclaw", "queue.json")),
  persistQueue: z.boolean().default(true),
});

export type ConnectorConfig = z.input<typeof connectorConfigSchema>;

type PersistedQueue = {
  events: ConnectorEvent[];
};

export class LaunchThatOpenClawConnector {
  private readonly config: z.output<typeof connectorConfigSchema>;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private readonly queue: ConnectorEvent[] = [];
  private isFlushing = false;

  public constructor(config: ConnectorConfig) {
    this.config = connectorConfigSchema.parse(config);
  }

  public static async createAuthLink(params: {
    launchThatBaseUrl: string;
    workspaceId: string;
    instanceName: string;
  }): Promise<{ authUrl: string; challengeId: string; expiresAt: number }> {
    const response = await fetch(
      `${params.launchThatBaseUrl.replace(/\/$/, "")}/api/openclaw/connect/start`,
      {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          workspaceId: params.workspaceId,
          instanceName: params.instanceName,
        }),
      },
    );

    if (!response.ok) {
      throw new Error(`Connect start failed (${response.status})`);
    }

    return (await response.json()) as {
      authUrl: string;
      challengeId: string;
      expiresAt: number;
    };
  }

  public async start(): Promise<void> {
    await this.loadQueueFromDisk();
    this.startHeartbeat();
    await this.flushQueue();
  }

  public async stop(): Promise<void> {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
    await this.persistQueue();
  }

  public async trackEvent(event: ConnectorEvent): Promise<void> {
    const normalized = eventSchema.parse(event);
    this.queue.push({
      ...normalized,
      idempotencyKey:
        normalized.idempotencyKey ??
        `${normalized.eventType}:${normalized.eventId}:${normalized.occurredAt}`,
      metadata: normalized.metadata ?? {},
    });
    await this.persistQueue();
    await this.flushQueue();
  }

  private startHeartbeat(): void {
    if (this.heartbeatTimer) return;
    this.heartbeatTimer = setInterval(() => {
      void this.sendHeartbeat();
    }, this.config.heartbeatIntervalMs);
    void this.sendHeartbeat();
  }

  private async sendHeartbeat(): Promise<void> {
    const url = `${this.config.launchThatBaseUrl.replace(/\/$/, "")}/api/openclaw/instances/${this.config.instanceId}/heartbeat`;
    const signedHeaders = this.createSignedHeaders("");
    await this.retry(async () => {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          authorization: `Bearer ${this.config.ingestToken}`,
          ...signedHeaders,
        },
      });
      if (!response.ok) {
        throw new Error(`Heartbeat failed (${response.status})`);
      }
    });
  }

  private async flushQueue(): Promise<void> {
    if (this.isFlushing || this.queue.length === 0) return;
    this.isFlushing = true;
    try {
      while (this.queue.length > 0) {
        const batch = this.queue.slice(0, 100);
        const url = `${this.config.launchThatBaseUrl.replace(/\/$/, "")}/api/openclaw/ingest/events`;
        const requestBody = JSON.stringify({
          instanceId: this.config.instanceId,
          events: batch,
        });
        const signedHeaders = this.createSignedHeaders(requestBody);
        await this.retry(async () => {
          const response = await fetch(url, {
            method: "POST",
            headers: {
              "content-type": "application/json",
              authorization: `Bearer ${this.config.ingestToken}`,
              ...signedHeaders,
            },
            body: requestBody,
          });
          if (!response.ok) {
            throw new Error(`Ingest failed (${response.status})`);
          }
        });

        this.queue.splice(0, batch.length);
        await this.persistQueue();
      }
    } finally {
      this.isFlushing = false;
    }
  }

  private async retry(
    task: () => Promise<void>,
    maxAttempts = 5,
    baseDelayMs = 500,
  ): Promise<void> {
    for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
      try {
        await task();
        return;
      } catch (error) {
        if (attempt === maxAttempts) throw error;
        const waitMs = baseDelayMs * 2 ** (attempt - 1);
        await delay(waitMs);
      }
    }
  }

  private async persistQueue(): Promise<void> {
    if (!this.config.persistQueue) return;
    const payload: PersistedQueue = { events: this.queue };
    const path = this.config.queueFilePath;
    await mkdir(dirname(path), { recursive: true, mode: 0o700 });
    await writeFile(path, JSON.stringify(payload, null, 2), {
      encoding: "utf-8",
      mode: 0o600,
    });
  }

  private async loadQueueFromDisk(): Promise<void> {
    if (!this.config.persistQueue) return;
    try {
      const file = await readFile(this.config.queueFilePath, "utf-8");
      const parsed = JSON.parse(file) as PersistedQueue;
      const events = z.array(eventSchema).parse(parsed.events ?? []);
      this.queue.push(...events);
    } catch {
      // No persisted queue yet.
    }
  }

  private createSignedHeaders(body: string): Record<string, string> {
    if (!this.config.signingSecret) return {};
    const timestamp = `${Date.now()}`;
    const signature = createHmac("sha256", this.config.signingSecret)
      .update(`${timestamp}.${body}`)
      .digest("hex");
    return {
      "x-openclaw-timestamp": timestamp,
      "x-openclaw-signature": signature,
    };
  }
}
