const REDACTION_RULES = [
  {
    name: "openai-secret-token",
    regex: /\bsk-[A-Za-z0-9]{20,}\b/g,
    replacement: "<REDACTED_TOKEN>"
  },
  {
    name: "public-or-publishable-token",
    regex: /\bpk_(?:live|test)_[A-Za-z0-9]{16,}\b/gi,
    replacement: "<REDACTED_TOKEN>"
  },
  {
    name: "jwt",
    regex: /\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b/g,
    replacement: "<REDACTED_JWT>"
  },
  {
    name: "bearer-token",
    regex: /\bBearer\s+[A-Za-z0-9._-]+\b/gi,
    replacement: "Bearer <REDACTED_TOKEN>"
  },
  {
    name: "aws-access-key",
    regex: /\bAKIA[0-9A-Z]{16}\b/g,
    replacement: "<REDACTED_AWS_KEY>"
  },
  {
    name: "private-key-header",
    regex: /-----BEGIN [A-Z ]+PRIVATE KEY-----/g,
    replacement: "<REDACTED_PRIVATE_KEY_HEADER>"
  },
  {
    name: "ipv4",
    regex: /\b(?:\d{1,3}\.){3}\d{1,3}\b/g,
    replacement: "<REDACTED_IP>"
  },
  {
    name: "email",
    regex: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g,
    replacement: "<REDACTED_EMAIL>"
  },
  {
    name: "api-key-like",
    regex: /\b[a-f0-9]{8}-[a-f0-9]{4}-[1-5][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}\b/gi,
    replacement: "<REDACTED_KEY>"
  },
  {
    name: "person-handle",
    regex: /@[A-Za-z0-9_]{2,32}\b/g,
    replacement: "<REDACTED_PERSON>"
  }
];

const BLOCKLIST = [
  /-----BEGIN [A-Z ]+PRIVATE KEY-----/i,
  /\bSECRET_ACCESS_KEY\b/i,
  /\bsk-[A-Za-z0-9]{20,}\b/i,
  /\bpk_(?:live|test)_[A-Za-z0-9]{16,}\b/i,
  /\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b/i
];

const CONTEXT_LABEL_REDACTIONS = [
  {
    regex: /((?:project|repo|repository|workspace|项目|工程)\s*[:：]\s*)([^\s,，;；]+)/gi,
    replacement: "$1<REDACTED_PROJECT>"
  },
  {
    regex: /((?:name|owner|assignee|user|联系人|姓名|客户)\s*[:：]\s*)([^\s,，;；]+)/gi,
    replacement: "$1<REDACTED_PERSON>"
  }
];

const PERSON_LIKE_KEY = /(name|owner|assignee|user|contact|person|姓名|联系人|客户)/i;
const PROJECT_LIKE_KEY = /(project|repo|repository|workspace|项目|工程)/i;

function compactWhitespace(text) {
  return text.replace(/[\t\r]+/g, " ").replace(/\s{2,}/g, " ").trim();
}

function truncate(value, max) {
  if (value.length <= max) {
    return value;
  }

  return `${value.slice(0, max)}...[truncated]`;
}

export function sanitizeForVectorStorage(input) {
  let value = String(input ?? "");

  for (const rule of REDACTION_RULES) {
    value = value.replace(rule.regex, rule.replacement);
  }

  for (const rule of CONTEXT_LABEL_REDACTIONS) {
    value = value.replace(rule.regex, rule.replacement);
  }

  return compactWhitespace(value);
}

export function assertVectorPayloadSafe(input) {
  const value = String(input ?? "");
  for (const pattern of BLOCKLIST) {
    if (pattern.test(value)) {
      throw new Error("Blocked sensitive payload: private key material detected.");
    }
  }
}

function coerceMetadataValue(value) {
  if (typeof value === "string") {
    return truncate(sanitizeForVectorStorage(value), 1000);
  }

  if (typeof value === "number" && Number.isFinite(value)) {
    return value;
  }

  if (typeof value === "boolean") {
    return value;
  }

  if (Array.isArray(value)) {
    return value
      .map((item) => truncate(sanitizeForVectorStorage(String(item)), 120))
      .filter(Boolean)
      .slice(0, 64);
  }

  return truncate(sanitizeForVectorStorage(JSON.stringify(value)), 1000);
}

export function sanitizeMetadata(metadata) {
  if (!metadata || typeof metadata !== "object") {
    return {};
  }

  const result = {};
  for (const [key, value] of Object.entries(metadata)) {
    if (value === undefined || value === null) {
      continue;
    }

    const safeKey = String(key);

    if (PERSON_LIKE_KEY.test(safeKey)) {
      result[safeKey] = "<REDACTED_PERSON>";
      continue;
    }

    if (PROJECT_LIKE_KEY.test(safeKey)) {
      result[safeKey] = "<REDACTED_PROJECT>";
      continue;
    }

    result[safeKey] = coerceMetadataValue(value);
  }

  return result;
}
