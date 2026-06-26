function isObject(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function compareUtf16CodeUnits(left, right) {
  const minLength = Math.min(left.length, right.length);
  for (let i = 0; i < minLength; i += 1) {
    const diff = left.charCodeAt(i) - right.charCodeAt(i);
    if (diff !== 0) {
      return diff;
    }
  }
  return left.length - right.length;
}

function assertValidUnicodeString(value) {
  for (let i = 0; i < value.length; i += 1) {
    const code = value.charCodeAt(i);
    if (code >= 0xd800 && code <= 0xdbff) {
      const next = value.charCodeAt(i + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) {
        throw new Error("RFC8785: invalid unicode string (unpaired high surrogate)");
      }
      i += 1;
      continue;
    }
    if (code >= 0xdc00 && code <= 0xdfff) {
      throw new Error("RFC8785: invalid unicode string (unpaired low surrogate)");
    }
  }
}

function serializeNumber(value) {
  if (!Number.isFinite(value)) {
    throw new Error("RFC8785: non-finite numbers are not allowed");
  }
  if (Object.is(value, -0)) {
    return "0";
  }
  return JSON.stringify(value);
}

function toJsonValue(value) {
  if (value === null || typeof value === "boolean" || typeof value === "string") {
    return value;
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) {
      throw new Error("RFC8785: non-finite numbers are not allowed");
    }
    return value;
  }
  if (Array.isArray(value)) {
    return value.map((item) => {
      if (item === undefined || typeof item === "function" || typeof item === "symbol") {
        return null;
      }
      if (typeof item === "bigint") {
        throw new Error("RFC8785: bigint is not valid JSON");
      }
      return toJsonValue(item);
    });
  }
  if (isObject(value)) {
    if (typeof value.toJSON === "function") {
      return toJsonValue(value.toJSON());
    }
    const result = Object.create(null);
    for (const key of Object.keys(value)) {
      const item = value[key];
      if (item === undefined || typeof item === "function" || typeof item === "symbol") {
        continue;
      }
      if (typeof item === "bigint") {
        throw new Error("RFC8785: bigint is not valid JSON");
      }
      result[key] = toJsonValue(item);
    }
    return result;
  }
  if (typeof value === "bigint") {
    throw new Error("RFC8785: bigint is not valid JSON");
  }
  throw new Error("RFC8785: unsupported value type");
}

function canonicalizeInternal(value, stack) {
  if (value === null) {
    return "null";
  }
  const type = typeof value;
  if (type === "string") {
    assertValidUnicodeString(value);
    return JSON.stringify(value);
  }
  if (type === "boolean") {
    return value ? "true" : "false";
  }
  if (type === "number") {
    return serializeNumber(value);
  }
  if (Array.isArray(value)) {
    const entries = value.map((item) => canonicalizeInternal(item, stack));
    return `[${entries.join(",")}]`;
  }

  if (stack.has(value)) {
    throw new Error("RFC8785: circular structure is not allowed");
  }
  stack.add(value);
  try {
    const keys = Object.keys(value).sort(compareUtf16CodeUnits);
    const entries = [];
    for (const key of keys) {
      assertValidUnicodeString(key);
      entries.push(`${JSON.stringify(key)}:${canonicalizeInternal(value[key], stack)}`);
    }
    return `{${entries.join(",")}}`;
  } finally {
    stack.delete(value);
  }
}

export function canonicalizeJson(value) {
  return canonicalizeInternal(toJsonValue(value), new Set());
}
