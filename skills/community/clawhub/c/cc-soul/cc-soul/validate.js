function validate(body, schema) {
  if (!body || typeof body !== "object") {
    return { ok: false, error: "request body must be a JSON object" };
  }
  const data = {};
  for (const [key, rule] of Object.entries(schema)) {
    const val = body[key];
    if (rule.required && (val === void 0 || val === null || val === "")) {
      return { ok: false, error: `"${key}" is required` };
    }
    if (val === void 0 || val === null) continue;
    if (rule.type && typeof val !== rule.type) {
      return { ok: false, error: `"${key}" must be ${rule.type}, got ${typeof val}` };
    }
    if (rule.type === "string") {
      if (rule.min !== void 0 && val.length < rule.min) {
        return { ok: false, error: `"${key}" must be at least ${rule.min} characters` };
      }
      if (rule.max !== void 0 && val.length > rule.max) {
        return { ok: false, error: `"${key}" must be at most ${rule.max} characters` };
      }
    }
    if (rule.type === "number") {
      if (rule.min !== void 0 && val < rule.min) {
        return { ok: false, error: `"${key}" must be >= ${rule.min}` };
      }
      if (rule.max !== void 0 && val > rule.max) {
        return { ok: false, error: `"${key}" must be <= ${rule.max}` };
      }
    }
    if (rule.enum && !rule.enum.includes(val)) {
      return { ok: false, error: `"${key}" must be one of: ${rule.enum.join(", ")}` };
    }
    data[key] = val;
  }
  for (const key of Object.keys(body)) {
    if (!(key in schema)) data[key] = body[key];
  }
  return { ok: true, data };
}
export {
  validate
};
