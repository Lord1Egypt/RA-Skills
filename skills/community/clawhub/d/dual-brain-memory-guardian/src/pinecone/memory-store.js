import crypto from "node:crypto";
import { bootstrapPinecone } from "./client.js";
import { namespaceForTenant, normalizeTenantId } from "./config.js";
import {
  assertVectorPayloadSafe,
  sanitizeForVectorStorage,
  sanitizeMetadata
} from "./gatekeeper.js";

const RESERVED_KEYS = new Set([
  "id",
  "_id",
  "event_type",
  "domain",
  "project",
  "tenant_id",
  "task_context",
  "resolution",
  "created_at",
  "promoted_at",
  "promoted_to_markdown",
  "tags",
  "content"
]);

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function normalizedTags(tags) {
  if (!tags) {
    return [];
  }

  if (Array.isArray(tags)) {
    return tags
      .map((item) => sanitizeForVectorStorage(String(item)).toLowerCase())
      .filter(Boolean)
      .slice(0, 64);
  }

  return String(tags)
    .split(",")
    .map((item) => sanitizeForVectorStorage(item).toLowerCase())
    .filter(Boolean)
    .slice(0, 64);
}

function normalizedTaskContext(taskContext) {
  const value = sanitizeForVectorStorage(taskContext || "");
  return value ? value.toLowerCase() : "";
}

function buildRecordId(tenantId, eventType, createdAt) {
  const ts = createdAt.replace(/[-:.TZ]/g, "");
  return `${tenantId}#${eventType}#${ts}#${crypto.randomUUID().slice(0, 8)}`;
}

function buildEventText({ eventType, domain, project, taskContext, content, resolution }) {
  const parts = [
    `event_type: ${eventType}`,
    `domain: ${domain}`,
    `project: ${project}`,
    taskContext ? `task_context: ${taskContext}` : "",
    `content: ${content}`,
    resolution ? `resolution: ${resolution}` : ""
  ];

  return parts.filter(Boolean).join("\n");
}

function buildFilter({ eventType, domain, project, taskContext, tags, promotedToMarkdown }) {
  const clauses = [];

  if (eventType) {
    clauses.push({ event_type: { $eq: eventType } });
  }

  if (domain) {
    clauses.push({ domain: { $eq: domain } });
  }

  if (project) {
    clauses.push({ project: { $eq: project } });
  }

  if (taskContext) {
    clauses.push({ task_context: { $eq: taskContext } });
  }

  if (tags?.length) {
    clauses.push({ tags: { $in: tags } });
  }

  if (typeof promotedToMarkdown === "boolean") {
    clauses.push({ promoted_to_markdown: { $eq: promotedToMarkdown } });
  }

  if (clauses.length === 0) {
    return undefined;
  }

  if (clauses.length === 1) {
    return clauses[0];
  }

  return { $and: clauses };
}

export class DualBrainMemoryStore {
  constructor(overrides = {}) {
    this.overrides = overrides;
    this.bootstrapPromise = null;
    this.context = null;
  }

  async init() {
    if (!this.bootstrapPromise) {
      this.bootstrapPromise = bootstrapPinecone(this.overrides).then((ctx) => {
        this.context = ctx;
        return ctx;
      });
    }

    return this.bootstrapPromise;
  }

  get config() {
    if (!this.context) {
      throw new Error("DualBrainMemoryStore is not initialized.");
    }

    return this.context.config;
  }

  get index() {
    if (!this.context) {
      throw new Error("DualBrainMemoryStore is not initialized.");
    }

    return this.context.index;
  }

  namespace(tenantId) {
    return namespaceForTenant(this.config.namespacePrefix, tenantId || this.config.defaultTenant);
  }

  async saveExperience({
    tenantId,
    eventType,
    domain = "general",
    project = "global",
    taskContext = "",
    content,
    resolution = "",
    tags = [],
    metadata = {}
  }) {
    await this.init();

    const safeEventType = sanitizeForVectorStorage(eventType || "correction").toLowerCase();
    const safeTenantId = normalizeTenantId(tenantId || this.config.defaultTenant);
    const safeDomain = sanitizeForVectorStorage(domain || "general").toLowerCase();
    const safeProject = sanitizeForVectorStorage(project || "global").toLowerCase();
    const safeTaskContext = normalizedTaskContext(taskContext);
    const safeContent = sanitizeForVectorStorage(content || "");
    const safeResolution = sanitizeForVectorStorage(resolution || "");
    const safeTags = normalizedTags(tags);

    if (!safeContent) {
      throw new Error("content is required.");
    }

    const createdAt = new Date().toISOString();
    const id = buildRecordId(safeTenantId, safeEventType, createdAt);
    const vectorText = buildEventText({
      eventType: safeEventType,
      domain: safeDomain,
      project: safeProject,
      taskContext: safeTaskContext,
      content: safeContent,
      resolution: safeResolution
    });

    assertVectorPayloadSafe(vectorText);

    const additionalMetadata = sanitizeMetadata(metadata);
    for (const key of Object.keys(additionalMetadata)) {
      if (RESERVED_KEYS.has(key)) {
        delete additionalMetadata[key];
      }
    }

    const record = {
      id,
      [this.config.textField]: vectorText,
      event_type: safeEventType,
      domain: safeDomain,
      project: safeProject,
      tenant_id: safeTenantId,
      task_context: safeTaskContext,
      resolution: safeResolution,
      created_at: createdAt,
      promoted_to_markdown: false,
      promoted_at: "",
      tags: safeTags,
      ...additionalMetadata
    };

    const namespace = this.namespace(safeTenantId);
    await this.index.upsertRecords({
      namespace,
      records: [record]
    });

    return { id, namespace, createdAt };
  }

  async searchExperiences({
    tenantId,
    query,
    topK = 3,
    eventType,
    domain,
    project,
    taskContext,
    tags = [],
    promotedToMarkdown,
    fields
  }) {
    await this.init();

    const safeQuery = sanitizeForVectorStorage(query || "");
    if (!safeQuery) {
      throw new Error("query is required.");
    }

    const safeTopK = Number.isFinite(Number(topK)) ? Math.max(1, Number(topK)) : 3;
    const safeTags = normalizedTags(tags);
    const filter = buildFilter({
      eventType: eventType ? sanitizeForVectorStorage(eventType).toLowerCase() : undefined,
      domain: domain ? sanitizeForVectorStorage(domain).toLowerCase() : undefined,
      project: project ? sanitizeForVectorStorage(project).toLowerCase() : undefined,
      taskContext: normalizedTaskContext(taskContext) || undefined,
      tags: safeTags,
      promotedToMarkdown:
        typeof promotedToMarkdown === "boolean" ? promotedToMarkdown : undefined
    });

    const namespace = this.namespace(tenantId || this.config.defaultTenant);

    const response = await this.index.searchRecords({
      namespace,
      query: {
        inputs: { text: safeQuery },
        topK: safeTopK,
        ...(filter ? { filter } : {})
      },
      fields:
        fields ||
        [
          this.config.textField,
          "event_type",
          "domain",
          "project",
          "task_context",
          "resolution",
          "created_at",
          "tags"
        ]
    });

    return {
      namespace,
      hits: response.result?.hits ?? []
    };
  }

  async startImport({ uri, integration, integrationId, errorMode = "continue" }) {
    await this.init();

    const finalUri = String(uri || "").trim();
    if (!finalUri) {
      throw new Error("uri is required.");
    }

    const safeErrorMode = String(errorMode || "").toLowerCase() === "abort" ? "abort" : "continue";
    const finalIntegration = String(
      integration || integrationId || this.config.importIntegrationId || ""
    ).trim();

    const options = {
      uri: finalUri,
      errorMode: safeErrorMode
    };

    if (finalIntegration) {
      options.integration = finalIntegration;
    }

    return this.index.startImport(options);
  }

  async describeImport(id) {
    await this.init();
    return this.index.describeImport(String(id));
  }

  async listImports(limit = 20, paginationToken) {
    await this.init();
    return this.index.listImports(limit, paginationToken);
  }

  async cancelImport(id) {
    await this.init();
    return this.index.cancelImport(String(id));
  }

  async describeFreshness({ tenantId } = {}) {
    await this.init();

    const stats = await this.index.describeIndexStats();
    const namespace = this.namespace(tenantId || this.config.defaultTenant);
    const namespaceSummary = stats.namespaces?.[namespace] || null;

    return {
      namespace,
      namespaceRecordCount:
        namespaceSummary?.recordCount ?? namespaceSummary?.vectorCount ?? 0,
      totalRecordCount: stats.totalRecordCount ?? stats.totalVectorCount ?? 0,
      dimension: stats.dimension,
      indexFullness: stats.indexFullness ?? 0,
      raw: stats
    };
  }

  async waitForWrite({ tenantId, id, timeoutMs = 15000, pollIntervalMs = 750 }) {
    await this.init();

    const namespace = this.namespace(tenantId || this.config.defaultTenant);
    const startedAt = Date.now();

    while (Date.now() - startedAt < timeoutMs) {
      const fetched = await this.index.fetch({ ids: [id], namespace });
      const records = fetched.records || fetched.vectors || {};

      if (records[id]) {
        return { visible: true, namespace, waitedMs: Date.now() - startedAt };
      }

      await sleep(pollIntervalMs);
    }

    return {
      visible: false,
      namespace,
      waitedMs: Date.now() - startedAt,
      note:
        "Write not visible yet. Pinecone is eventually consistent; retry search or fetch shortly."
    };
  }

  async clearTenantMemory({ tenantId } = {}) {
    await this.init();

    const namespace = this.namespace(tenantId || this.config.defaultTenant);
    await this.index.deleteAll({ namespace });

    return {
      namespace,
      status: "cleared"
    };
  }

  async forgetExperience({
    tenantId,
    ids = [],
    eventType,
    domain,
    project,
    taskContext,
    tags = [],
    promotedToMarkdown
  } = {}) {
    await this.init();

    const namespace = this.namespace(tenantId || this.config.defaultTenant);
    const normalizedIds = Array.isArray(ids)
      ? ids.map((item) => String(item).trim()).filter(Boolean)
      : [];

    if (normalizedIds.length > 0) {
      await this.index.deleteMany({
        namespace,
        ids: normalizedIds
      });

      return {
        namespace,
        mode: "ids",
        deletedIds: normalizedIds
      };
    }

    const filter = buildFilter({
      eventType: eventType ? sanitizeForVectorStorage(eventType).toLowerCase() : undefined,
      domain: domain ? sanitizeForVectorStorage(domain).toLowerCase() : undefined,
      project: project ? sanitizeForVectorStorage(project).toLowerCase() : undefined,
      taskContext: normalizedTaskContext(taskContext) || undefined,
      tags: normalizedTags(tags),
      promotedToMarkdown:
        typeof promotedToMarkdown === "boolean" ? promotedToMarkdown : undefined
    });

    if (!filter) {
      throw new Error(
        "forget requires either --id or at least one filter (--type/--domain/--project/--task/--tags)."
      );
    }

    await this.index.deleteMany({
      namespace,
      filter
    });

    return {
      namespace,
      mode: "filter",
      filter
    };
  }

  async markExperiencePromoted({
    tenantId,
    id,
    promoted = true,
    promotedAt,
    metadata = {}
  } = {}) {
    await this.init();

    const safeId = String(id || "").trim();
    if (!safeId) {
      throw new Error("id is required for markExperiencePromoted.");
    }

    const namespace = this.namespace(tenantId || this.config.defaultTenant);
    const safePromoted = Boolean(promoted);
    const safePromotedAt = safePromoted ? String(promotedAt || new Date().toISOString()) : "";

    const additionalMetadata = sanitizeMetadata(metadata);
    for (const key of Object.keys(additionalMetadata)) {
      if (RESERVED_KEYS.has(key)) {
        delete additionalMetadata[key];
      }
    }

    const patch = {
      promoted_to_markdown: safePromoted,
      promoted_at: safePromotedAt,
      ...additionalMetadata
    };

    const attempts = [];

    if (typeof this.index.update === "function") {
      const payloads = [
        { namespace, id: safeId, setMetadata: patch },
        { namespace, id: safeId, metadata: patch }
      ];

      for (const payload of payloads) {
        try {
          await this.index.update(payload);
          return {
            id: safeId,
            namespace,
            promoted_to_markdown: safePromoted,
            promoted_at: safePromotedAt,
            method: "update"
          };
        } catch (error) {
          attempts.push(error?.message || String(error));
        }
      }
    }

    if (typeof this.index.updateRecord === "function") {
      const payloads = [
        { namespace, id: safeId, metadata: patch },
        { namespace, id: safeId, setMetadata: patch },
        { namespace, id: safeId, record: patch }
      ];

      for (const payload of payloads) {
        try {
          await this.index.updateRecord(payload);
          return {
            id: safeId,
            namespace,
            promoted_to_markdown: safePromoted,
            promoted_at: safePromotedAt,
            method: "updateRecord"
          };
        } catch (error) {
          attempts.push(error?.message || String(error));
        }
      }
    }

    throw new Error(
      `Unable to update promoted_to_markdown metadata for id ${safeId}. ${
        attempts.length ? `Tried SDK update/updateRecord payloads: ${attempts.join(" | ")}` : ""
      }`
    );
  }
}
