export const ALLOWED_MODELS = ["t2v", "i2v", "lv", "t2v_v3", "i2v_v3"];

export const ACTIONS = {
  createGeneration: "createGeneration",
  getTask: "getTask",
  getStatus: "getStatus",
  cancelTask: "cancelTask",
};

const ASPECT_RATIOS = ["16:9", "9:16", "1:1"];
const DURATIONS_V1 = ["5", "8"];
const DURATIONS_V3 = ["5", "10", "15", "20"];

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isNullableString(value) {
  return value === null || typeof value === "string";
}

function isImageDataUri(value) {
  return (
    typeof value === "string" &&
    value.startsWith("data:image/") &&
    value.includes(";base64,") &&
    value.split("base64,")[1]?.trim().length > 0
  );
}

function isHttpImageUrl(value) {
  return typeof value === "string" && (value.startsWith("http://") || value.startsWith("https://"));
}

function isImageSource(value) {
  return isImageDataUri(value) || isHttpImageUrl(value);
}

function ensure(value, rule, field, expected, errors) {
  if (!rule(value)) {
    errors.push({
      field,
      expected,
      actual: value,
    });
  }
}

function validateT2V(payload, errors) {
  ensure(payload.prompt, isNonEmptyString, "prompt", "non-empty string", errors);
  ensure(
    payload.aspectRatio,
    (v) => ASPECT_RATIOS.includes(v),
    "aspectRatio",
    `one of ${ASPECT_RATIOS.join(", ")}`,
    errors,
  );
  ensure(
    payload.duration,
    (v) => DURATIONS_V1.includes(v),
    "duration",
    `one of ${DURATIONS_V1.join(", ")}`,
    errors,
  );
}

function validateI2V(payload, errors) {
  ensure(
    payload.image,
    isImageSource,
    "image",
    "public image URL or image data URI (prefer data URI: data:image/...;base64,...)",
    errors
  );
  ensure(payload.prompt, isNullableString, "prompt", "string or null", errors);
  ensure(
    payload.duration,
    (v) => DURATIONS_V1.includes(v),
    "duration",
    `one of ${DURATIONS_V1.join(", ")}`,
    errors,
  );
}

function validateLV(payload, errors) {
  ensure(
    payload.image,
    isImageSource,
    "image",
    "public image URL or image data URI (prefer data URI: data:image/...;base64,...)",
    errors
  );
  ensure(
    payload.prompt,
    (v) =>
      Array.isArray(v) &&
      v.length > 0 &&
      v.length <= 6 &&
      v.every((item) => typeof item === "string" && item.trim().length > 0),
    "prompt",
    "string[] with 1-6 non-empty items",
    errors,
  );
}

function validateT2VV3(payload, errors) {
  ensure(payload.prompt, isNonEmptyString, "prompt", "non-empty string", errors);
  ensure(
    payload.aspectRatio,
    (v) => ASPECT_RATIOS.includes(v),
    "aspectRatio",
    `one of ${ASPECT_RATIOS.join(", ")}`,
    errors,
  );
  ensure(
    payload.duration,
    (v) => DURATIONS_V3.includes(v),
    "duration",
    `one of ${DURATIONS_V3.join(", ")}`,
    errors,
  );
}

function validateI2VV3(payload, errors) {
  ensure(
    payload.image,
    isImageSource,
    "image",
    "public image URL or image data URI (prefer data URI: data:image/...;base64,...)",
    errors
  );
  ensure(payload.prompt, isNullableString, "prompt", "string or null", errors);
  ensure(
    payload.duration,
    (v) => DURATIONS_V3.includes(v),
    "duration",
    `one of ${DURATIONS_V3.join(", ")}`,
    errors,
  );
}

export function validateCreatePayload(model, payload) {
  const errors = [];

  if (!ALLOWED_MODELS.includes(model)) {
    return {
      ok: false,
      errorCode: "INVALID_MODEL",
      errorMessage: `model must be one of: ${ALLOWED_MODELS.join(", ")}`,
      details: [{ field: "model", expected: ALLOWED_MODELS.join("|"), actual: model }],
    };
  }

  if (!payload || typeof payload !== "object") {
    return {
      ok: false,
      errorCode: "INVALID_PAYLOAD",
      errorMessage: "payload must be an object",
      details: [{ field: "payload", expected: "object", actual: payload }],
    };
  }

  if (model === "t2v") validateT2V(payload, errors);
  if (model === "i2v") validateI2V(payload, errors);
  if (model === "lv") validateLV(payload, errors);
  if (model === "t2v_v3") validateT2VV3(payload, errors);
  if (model === "i2v_v3") validateI2VV3(payload, errors);

  if (errors.length > 0) {
    return {
      ok: false,
      errorCode: "INVALID_PAYLOAD",
      errorMessage: "payload validation failed",
      details: errors,
    };
  }

  return { ok: true };
}

export function normalizeResult({
  ok,
  status = "UNKNOWN",
  taskId = null,
  data = null,
  errorCode = null,
  errorMessage = null,
  retryAfter = null,
  httpStatus = null,
}) {
  return {
    ok: Boolean(ok),
    status,
    taskId,
    data,
    errorCode,
    errorMessage,
    retryAfter,
    httpStatus,
    timestamp: new Date().toISOString(),
  };
}
