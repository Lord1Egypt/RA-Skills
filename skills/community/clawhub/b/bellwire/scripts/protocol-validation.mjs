// SPDX-License-Identifier: MIT-0

const FIELD_TYPES = new Set(["string", "number", "boolean", "datetime", "url", "enum"]);
const SURFACE_TYPES = new Set([
  "stats", "metrics", "segmented_progress", "progress", "alert", "timer",
  "status", "checklist", "trend",
]);
const SURFACE_COLORS = new Set([
  "lime", "green", "cyan", "blue", "purple", "magenta", "red", "orange",
  "yellow", "gray",
]);
const STATUS_STATES = ["neutral", "running", "success", "warning", "critical", "paused"];
const CHECKLIST_STATES = ["pending", "running", "completed", "failed", "skipped"];
const TREND_GOALS = ["up", "down", "neutral"];
const TEMPLATE_PATTERN = /\{\{\s*([A-Za-z][A-Za-z0-9_]*)(?:\s*\|\s*default:\s*(['"])(.*?)\2)?\s*\}\}/gu;
const STABLE_KEY_PATTERN = /^[a-z0-9]+(?:[._-][a-z0-9]+)*$/u;
const SYMBOL_PATTERN = /^[A-Za-z0-9]+(?:[._-][A-Za-z0-9]+)*$/u;
const REFERENCE_PATTERN = /^[A-Za-z0-9_-]{22,200}$/u;
const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/iu;

export function validateEventSpec(value) {
  if (!isRecord(value)) throw new Error("Event Spec must be a JSON object");
  if (typeof value.eventType !== "string" || !/^[a-z0-9]+(?:\.[a-z0-9]+)*$/u.test(value.eventType)) {
    throw new Error("eventType must be a lowercase dotted name such as payment.success");
  }
  if (!isRecord(value.fields) || Object.keys(value.fields).length === 0) {
    throw new Error("fields must contain at least one field definition");
  }
  for (const [name, rawDefinition] of Object.entries(value.fields)) {
    if (!/^[A-Za-z][A-Za-z0-9_]*$/u.test(name)) throw new Error(`Invalid field name: ${name}`);
    if (!isRecord(rawDefinition) || !FIELD_TYPES.has(rawDefinition.type)) {
      throw new Error(`Unsupported type for field ${name}`);
    }
    if (rawDefinition.required !== undefined && typeof rawDefinition.required !== "boolean") {
      throw new Error(`required must be boolean for field ${name}`);
    }
    if (rawDefinition.sensitive !== undefined && typeof rawDefinition.sensitive !== "boolean") {
      throw new Error(`sensitive must be boolean for field ${name}`);
    }
    if (
      rawDefinition.type === "enum"
      && (!Array.isArray(rawDefinition.values) || rawDefinition.values.length === 0
        || rawDefinition.values.some((item) => !nonEmpty(item)))
    ) {
      throw new Error(`Enum field ${name} requires values`);
    }
  }
  if (value.notification !== undefined) validateNotification(value.notification, value.fields);
}

export function validateTestEvent(value) {
  if (!isRecord(value) || !nonEmpty(value.type) || !isRecord(value.data) || !nonEmpty(value.occurredAt)) {
    throw new Error("Test event requires type, data, and occurredAt");
  }
  if (Number.isNaN(Date.parse(value.occurredAt))) throw new Error("occurredAt must be an ISO datetime");
}

export function validateDirectConnectionManifest(value) {
  if (!isRecord(value) || value.version !== 2) {
    throw new Error("Direct connection manifest version must be 2");
  }
  bounded(value.connectionId, "connectionId", 120, true);
  validateHttpsUrl(value.baseUrl, "baseUrl");
  if (!isRecord(value.endpoints)) throw new Error("endpoints is required");
  for (const name of ["notification", "inbox", "surfaces"]) {
    validateEndpointPath(value.endpoints[name], `endpoints.${name}`);
  }
  if (
    !Array.isArray(value.capabilities)
    || value.capabilities.length !== 3
    || new Set(value.capabilities).size !== value.capabilities.length
    || value.capabilities.some((item) => !["notification_detail", "inbox", "surfaces"].includes(item))
  ) {
    throw new Error("capabilities must contain notification_detail, inbox, and surfaces exactly once");
  }
  if (!isRecord(value.project)) throw new Error("project is required");
  if (!isUUID(value.project.id)) throw new Error("project.id must be a UUID");
  bounded(value.project.name, "project.name", 120, true);
  bounded(value.project.icon, "project.icon", 120, true);
  if (!SYMBOL_PATTERN.test(value.project.icon)) throw new Error("project.icon must be an SF Symbol name");
  bounded(value.project.category, "project.category", 80, true);
  if (value.project.logoUrl !== undefined && value.project.logoUrl !== null) {
    validateHttpsUrl(value.project.logoUrl, "project.logoUrl");
  }
  validateDisplayOrder(value.project.displayOrder, "project.displayOrder");
}

export function validateOpaqueReference(value) {
  if (typeof value !== "string" || !REFERENCE_PATTERN.test(value)) {
    throw new Error("reference must be a 22-200 character URL-safe opaque value");
  }
}

export function validateSurfaceInput(value) {
  if (!isRecord(value) || !SURFACE_TYPES.has(value.type)) {
    throw new Error(`Surface type must be one of: ${[...SURFACE_TYPES].join(", ")}`);
  }
  bounded(value.title, "title", 80, true);
  bounded(value.subtitle, "subtitle", 120, false);
  validateAction(value.action);
  validateLiveActivity(value.liveActivity);
  validateSurfaceContent(value.type, value);
}

export function validatePrivateEvent(value, expectedReference) {
  if (!isRecord(value)) throw new Error("Private event must be a JSON object");
  validateOpaqueReference(value.reference);
  if (expectedReference && value.reference !== expectedReference) {
    throw new Error("Notification response reference does not match the request");
  }
  bounded(value.eventType, "eventType", 120, true);
  bounded(value.title, "title", 240, true);
  bounded(value.body, "body", 1_000, true);
  bounded(value.subtitle, "subtitle", 240, false);
  validateDate(value.occurredAt, "occurredAt");
  if (!isRecord(value.data)) throw new Error("data must be a JSON object");
  if (value.deepLink !== undefined && value.deepLink !== null) {
    bounded(value.deepLink, "deepLink", 2_048, true);
    const deepLink = parseUrl(value.deepLink, "deepLink");
    if (!["https:", "bellwire:"].includes(deepLink.protocol) || deepLink.username || deepLink.password) {
      throw new Error("deepLink must be an HTTPS or bellwire URL without credentials");
    }
  }
  if (value.logoUrl !== undefined && value.logoUrl !== null) {
    validateHttpsUrl(value.logoUrl, "logoUrl");
  }
}

export function validateDirectInboxResponse(value) {
  if (!isRecord(value) || !Array.isArray(value.events) || value.events.length > 50) {
    throw new Error("Inbox response must contain at most 50 events");
  }
  for (const event of value.events) validatePrivateEvent(event);
  if (value.nextCursor !== null && value.nextCursor !== undefined) {
    bounded(value.nextCursor, "nextCursor", 512, true);
  }
}

export function validateDirectSurfacesResponse(value, expectedProjectId) {
  if (!isRecord(value) || !Array.isArray(value.surfaces)) {
    throw new Error("Surfaces response must contain a surfaces array");
  }
  for (const surface of value.surfaces) validateDirectSurfaceRecord(surface, expectedProjectId);
}

export function isUUID(value) {
  return typeof value === "string" && UUID_PATTERN.test(value);
}

function validateNotification(value, fields) {
  if (!isRecord(value)) throw new Error("notification must be an object");
  for (const name of ["title", "body"]) {
    if (!nonEmpty(value[name])) throw new Error("notification.title and notification.body are required");
    validateTemplate(value[name], fields, `notification.${name}`);
  }
  if (value.subtitle !== undefined && value.subtitle !== null && value.subtitle !== "") {
    if (!nonEmpty(value.subtitle)) throw new Error("notification.subtitle must be a string");
    validateTemplate(value.subtitle, fields, "notification.subtitle");
  }
  if (value.priority !== undefined && !["normal", "high"].includes(value.priority)) {
    throw new Error("notification.priority must be normal or high");
  }
}

function validateTemplate(template, fields, name) {
  if (template.length > 240) throw new Error(`${name} must be at most 240 characters`);
  const matches = [...template.matchAll(TEMPLATE_PATTERN)];
  const remainder = template.replace(TEMPLATE_PATTERN, "");
  if (remainder.includes("{{") || remainder.includes("}}")) {
    throw new Error(`${name} contains unsupported template syntax`);
  }
  for (const match of matches) {
    const field = match[1];
    if (!fields[field]) throw new Error(`${name} references unknown field ${field}`);
    if (fields[field].sensitive === true) throw new Error(`${name} references sensitive field ${field}`);
  }
}

function validateDirectSurfaceRecord(value, expectedProjectId) {
  if (!isRecord(value)) throw new Error("Each Surface must be a JSON object");
  bounded(value.id, "surface.id", 120, true);
  bounded(value.projectId, "surface.projectId", 120, true);
  if (expectedProjectId && value.projectId !== expectedProjectId) {
    throw new Error("Surface projectId must match manifest.project.id");
  }
  bounded(value.surfaceKey, "surface.surfaceKey", 80, true);
  if (!STABLE_KEY_PATTERN.test(value.surfaceKey)) throw new Error("surface.surfaceKey must be a stable lowercase key");
  if (!isRecord(value.content)) throw new Error("surface.content must be a JSON object");
  validateSurfaceInput({
    type: value.type,
    title: value.title,
    ...(value.subtitle === undefined || value.subtitle === null ? {} : { subtitle: value.subtitle }),
    ...value.content,
    ...(value.action === undefined || value.action === null ? {} : { action: value.action }),
    ...(value.liveActivity === undefined || value.liveActivity === null ? {} : { liveActivity: value.liveActivity }),
  });
  validateDisplayOrder(value.displayOrder, "surface.displayOrder");
  if (!Number.isInteger(value.version) || value.version < 1) {
    throw new Error("surface.version must be a positive integer");
  }
  validateDate(value.createdAt, "surface.createdAt");
  validateDate(value.updatedAt, "surface.updatedAt");
  if (value.project !== undefined && value.project !== null) {
    if (!isRecord(value.project)) throw new Error("surface.project must be a JSON object");
    if (value.project.id !== value.projectId) throw new Error("surface.project.id must match surface.projectId");
    bounded(value.project.name, "surface.project.name", 120, true);
    bounded(value.project.icon, "surface.project.icon", 120, true);
    if (value.project.logoUrl !== undefined && value.project.logoUrl !== null) {
      validateHttpsUrl(value.project.logoUrl, "surface.project.logoUrl");
    }
  }
}

function validateSurfaceContent(type, value) {
  switch (type) {
    case "stats": validateMetrics(value.metrics, 8, false); break;
    case "metrics": validateMetrics(value.metrics, 4, true); break;
    case "progress": {
      if (finite(value.percentage)) {
        if (value.percentage < 0 || value.percentage > 100) throw new Error("percentage must be between 0 and 100");
      } else if (!finite(value.value) || !finite(value.upperLimit) || value.upperLimit <= 0 || value.value < 0 || value.value > value.upperLimit) {
        throw new Error("progress requires percentage or value with a positive upperLimit");
      }
      break;
    }
    case "segmented_progress":
      if (!Number.isInteger(value.numberOfSteps) || value.numberOfSteps < 1 || value.numberOfSteps > 12) {
        throw new Error("numberOfSteps must be between 1 and 12");
      }
      if (!Number.isInteger(value.currentStep) || value.currentStep < 0 || value.currentStep > value.numberOfSteps) {
        throw new Error("currentStep must be between 0 and numberOfSteps");
      }
      bounded(value.stepLabel, "stepLabel", 80, false);
      break;
    case "alert":
      bounded(value.message, "message", 240, true);
      validateAdornment(value.icon, "icon", "symbol", 80);
      validateAdornment(value.badge, "badge", "title", 24);
      break;
    case "timer":
      if (!Number.isInteger(value.durationSeconds) || value.durationSeconds < 1 || value.durationSeconds > 604_800) {
        throw new Error("durationSeconds must be between 1 and 604800");
      }
      if (value.countsDown !== undefined && typeof value.countsDown !== "boolean") {
        throw new Error("countsDown must be boolean");
      }
      break;
    case "status":
      oneOf(value.state, "state", STATUS_STATES);
      bounded(value.label, "label", 32, false);
      break;
    case "checklist": validateChecklist(value.items); break;
    case "trend": validateTrend(value); break;
  }
}

function validateChecklist(items) {
  if (!Array.isArray(items) || items.length < 1 || items.length > 8) {
    throw new Error("items must contain between 1 and 8 checklist entries");
  }
  const ids = new Set();
  items.forEach((item, index) => {
    if (!isRecord(item)) throw new Error(`items[${index}] must be an object`);
    bounded(item.id, `items[${index}].id`, 64, true);
    if (!STABLE_KEY_PATTERN.test(item.id)) throw new Error(`items[${index}].id must be a stable lowercase key`);
    if (ids.has(item.id)) throw new Error("Checklist item IDs must be unique");
    ids.add(item.id);
    bounded(item.title, `items[${index}].title`, 80, true);
    bounded(item.detail, `items[${index}].detail`, 120, false);
    oneOf(item.state, `items[${index}].state`, CHECKLIST_STATES);
  });
}

function validateTrend(value) {
  if (!Array.isArray(value.points) || value.points.length < 2 || value.points.length > 30) {
    throw new Error("points must contain between 2 and 30 trend points");
  }
  value.points.forEach((point, index) => {
    if (!isRecord(point)) throw new Error(`points[${index}] must be an object`);
    bounded(point.label, `points[${index}].label`, 24, true);
    if (!finite(point.value)) throw new Error(`points[${index}].value must be a finite number`);
  });
  oneOf(value.goal, "goal", TREND_GOALS);
  bounded(value.displayValue, "displayValue", 64, false);
  bounded(value.unit, "unit", 16, false);
}

function validateMetrics(value, maximum, numeric) {
  if (!Array.isArray(value) || value.length < 1 || value.length > maximum) {
    throw new Error(`metrics must contain between 1 and ${maximum} items`);
  }
  value.forEach((metric, index) => {
    if (!isRecord(metric)) throw new Error(`metrics[${index}] must be an object`);
    bounded(metric.label, `metrics[${index}].label`, 40, true);
    if (numeric) {
      if (!finite(metric.value)) throw new Error(`metrics[${index}].value must be a finite number`);
    } else if (finite(metric.value)) {
      // Numeric display values are valid without an additional string bound.
    } else {
      bounded(metric.value, `metrics[${index}].value`, 64, true);
    }
    bounded(metric.unit, `metrics[${index}].unit`, 16, false);
    validateColor(metric.color, `metrics[${index}].color`);
  });
}

function validateAdornment(value, name, key, maximum) {
  if (value === undefined || value === null) return;
  if (!isRecord(value)) throw new Error(`${name} must be an object`);
  bounded(value[key], `${name}.${key}`, maximum, true);
  if (key === "symbol" && !SYMBOL_PATTERN.test(value[key])) {
    throw new Error(`${name}.${key} must be an SF Symbol name`);
  }
  validateColor(value.color, `${name}.color`);
}

function validateAction(value) {
  if (value === undefined || value === null) return;
  if (!isRecord(value) || value.type !== "open_url") throw new Error("action.type must be open_url");
  bounded(value.title, "action.title", 40, true);
  bounded(value.url, "action.url", 2_048, true);
  const url = parseUrl(value.url, "action.url");
  if (!["http:", "https:"].includes(url.protocol)) throw new Error("action.url must use http or https");
}

function validateLiveActivity(value) {
  if (value === undefined || value === null) return;
  if (!isRecord(value)) throw new Error("liveActivity must be an object");
  bounded(value.sessionId, "liveActivity.sessionId", 80, true);
  if (!SYMBOL_PATTERN.test(value.sessionId)) throw new Error("liveActivity.sessionId must be a stable key");
  oneOf(value.state, "liveActivity.state", ["active", "ended"]);
}

function validateEndpointPath(value, name) {
  if (!nonEmpty(value) || !value.startsWith("/") || value.startsWith("//")) {
    throw new Error(`${name} must be an absolute URL path`);
  }
  const parsed = parseUrl(value, name, "https://bellwire.invalid");
  if (parsed.origin !== "https://bellwire.invalid") throw new Error(`${name} must remain on baseUrl`);
}

function validateHttpsUrl(value, name) {
  bounded(value, name, 2_048, true);
  const url = parseUrl(value, name);
  if (url.protocol !== "https:" || url.username || url.password || !url.hostname) {
    throw new Error(`${name} must be an HTTPS URL without embedded credentials`);
  }
}

function parseUrl(value, name, base) {
  try {
    return base ? new URL(value, base) : new URL(value);
  } catch {
    throw new Error(`${name} must be a valid URL`);
  }
}

function validateDisplayOrder(value, name) {
  if (!Number.isInteger(value) || value < 0 || value > 1_000_000) {
    throw new Error(`${name} must be an integer between 0 and 1000000`);
  }
}

function validateDate(value, name) {
  if (!nonEmpty(value) || Number.isNaN(Date.parse(value))) throw new Error(`${name} must be an ISO datetime`);
}

function validateColor(value, name) {
  if (value !== undefined && value !== null && value !== "" && !SURFACE_COLORS.has(value)) {
    throw new Error(`${name} is not a supported color`);
  }
}

function oneOf(value, name, allowed) {
  if (!allowed.includes(value)) throw new Error(`${name} must be one of: ${allowed.join(", ")}`);
}

function bounded(value, name, maximum, requiredValue) {
  if ((value === undefined || value === null || value === "") && !requiredValue) return;
  if (!nonEmpty(value)) throw new Error(`${name} is required`);
  if (value.length > maximum) throw new Error(`${name} must be at most ${maximum} characters`);
}

function finite(value) {
  return typeof value === "number" && Number.isFinite(value);
}

function nonEmpty(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isRecord(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
