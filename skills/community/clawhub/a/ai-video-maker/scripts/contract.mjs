export const ALLOWED_MODELS = [
  "t2v",
  "i2v",
  "minimax",
  "t2v_v3",
  "i2v_v3",
  "seedance20",
  "wan30",
  "happyhorse",
];

export const ACTIONS = {
  createGeneration: "createGeneration",
  getTask: "getTask",
  getStatus: "getStatus",
  cancelTask: "cancelTask",
};

const ASPECT_RATIOS = ["16:9", "9:16", "1:1"];
const DURATIONS_V1 = ["5", "8"];
const DURATIONS_V3 = ["5", "10", "15", "20"];
const MINIMAX_ASPECT_RATIOS = ["auto", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"];
const MINIMAX_RESOLUTIONS = ["720p", "1080p"];
const MINIMAX_TIERS = ["turbo", "base"];
const SEEDANCE_RATIOS = ["16:9", "9:16", "1:1"];
const WAN_RATIOS = ["16:9", "9:16", "1:1", "4:3", "3:4"];
const WAN_DURATIONS = ["5", "10", "15"];
const WAN_RESOLUTIONS = ["480P", "720P", "1080P"];
const HAPPYHORSE_RESOLUTIONS = ["720P", "1080P"];
const HAPPYHORSE_RATIOS = ["16:9", "9:16", "3:4", "4:3", "1:1"];

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isNullableString(value) {
  return value === undefined || value === null || typeof value === "string";
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

function isHttpUrl(value) {
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
    errors,
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

function validateMinimax(payload, errors) {
  ensure(payload.content, (v) => typeof v === "string", "content", "string", errors);
  ensure(
    payload.imageUrl,
    (v) => v === undefined || v === null || isImageSource(v),
    "imageUrl",
    "public image URL, image data URI, or null",
    errors,
  );
  ensure(
    payload.lastFrameUrl,
    (v) => v === undefined || v === null || isImageSource(v),
    "lastFrameUrl",
    "public image URL, image data URI, or null",
    errors,
  );
  ensure(
    payload.referenceImageUrls,
    (v) =>
      v === undefined ||
      (Array.isArray(v) && v.length <= 4 && v.every((item) => isImageSource(item))),
    "referenceImageUrls",
    "an array of up to 4 public image URLs or image data URIs",
    errors,
  );
  ensure(
    payload.referenceVideoUrl,
    (v) =>
      v === undefined ||
      v === null ||
      (typeof v === "string" && (v.startsWith("http://") || v.startsWith("https://"))),
    "referenceVideoUrl",
    "public video URL or null",
    errors,
  );
  ensure(
    payload.referenceAudioUrls,
    (v) =>
      v === undefined ||
      (Array.isArray(v) &&
        v.length <= 2 &&
        v.every(
          (item) =>
            typeof item === "string" && (item.startsWith("http://") || item.startsWith("https://")),
        )),
    "referenceAudioUrls",
    "an array of up to 2 public audio URLs",
    errors,
  );
  ensure(
    payload.aspectRatio,
    (v) => v === undefined || MINIMAX_ASPECT_RATIOS.includes(v),
    "aspectRatio",
    `one of ${MINIMAX_ASPECT_RATIOS.join(", ")}`,
    errors,
  );
  ensure(
    payload.duration,
    (v) => v === undefined || (typeof v === "number" && Number.isInteger(v) && v >= 5 && v <= 20),
    "duration",
    "an integer from 5 to 20",
    errors,
  );
  ensure(
    payload.resolution,
    (v) => v === undefined || MINIMAX_RESOLUTIONS.includes(v),
    "resolution",
    `one of ${MINIMAX_RESOLUTIONS.join(", ")}`,
    errors,
  );
  ensure(
    payload.tier,
    (v) => v === undefined || MINIMAX_TIERS.includes(v),
    "tier",
    `one of ${MINIMAX_TIERS.join(", ")}`,
    errors,
  );

  const hasFrames = Boolean(payload.imageUrl || payload.lastFrameUrl);
  const hasReference =
    (Array.isArray(payload.referenceImageUrls) && payload.referenceImageUrls.length > 0) ||
    Boolean(payload.referenceVideoUrl) ||
    (Array.isArray(payload.referenceAudioUrls) && payload.referenceAudioUrls.length > 0);
  if (hasFrames && hasReference) {
    errors.push({
      field: "media",
      expected: "frame inputs or reference assets, not both",
      actual: "mixed frame and reference inputs",
    });
  }
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
    errors,
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

function validateSeedance20(payload, errors) {
  ensure(
    payload.prompt,
    (v) => v === undefined || v === null || isNonEmptyString(v),
    "prompt",
    "non-empty string or null",
    errors,
  );
  ensure(
    payload.image,
    (v) => v === undefined || v === null || isImageSource(v),
    "image",
    "public image URL, image data URI, or null",
    errors,
  );
  ensure(
    payload.video,
    (v) => v === undefined || v === null || isHttpUrl(v),
    "video",
    "public HTTP(S) video URL or null",
    errors,
  );
  ensure(
    payload.audio,
    (v) => v === undefined || v === null || isHttpUrl(v),
    "audio",
    "public HTTP(S) audio URL or null",
    errors,
  );
  ensure(
    payload.duration,
    (v) => typeof v === "number" && Number.isInteger(v) && v >= 4 && v <= 15,
    "duration",
    "an integer from 4 to 15",
    errors,
  );
  ensure(
    payload.resolution,
    (v) => v === 480 || v === 720,
    "resolution",
    "480 or 720 as a number",
    errors,
  );
  ensure(
    payload.ratio,
    (v) => SEEDANCE_RATIOS.includes(v),
    "ratio",
    `one of ${SEEDANCE_RATIOS.join(", ")}`,
    errors,
  );

  const hasPrimaryInput =
    isNonEmptyString(payload.prompt) || isImageSource(payload.image) || isHttpUrl(payload.video);
  if (!hasPrimaryInput) {
    errors.push({
      field: "input",
      expected: "at least one of prompt, image, or video",
      actual: payload.audio ? "audio only" : "no usable input",
    });
  }
}

function validateWan30(payload, errors) {
  ensure(payload.prompt, isNonEmptyString, "prompt", "non-empty string", errors);
  ensure(
    payload.image,
    (v) => v === undefined || v === null || isImageSource(v),
    "image",
    "public image URL, image data URI, or null",
    errors,
  );
  ensure(
    payload.duration,
    (v) => WAN_DURATIONS.includes(v),
    "duration",
    `one of ${WAN_DURATIONS.join(", ")} as a string`,
    errors,
  );
  ensure(
    payload.resolution,
    (v) => WAN_RESOLUTIONS.includes(v),
    "resolution",
    `one of ${WAN_RESOLUTIONS.join(", ")}`,
    errors,
  );
  ensure(
    payload.ratio,
    (v) => WAN_RATIOS.includes(v),
    "ratio",
    `one of ${WAN_RATIOS.join(", ")}`,
    errors,
  );
  ensure(
    payload.promptExtend,
    (v) => v === undefined || typeof v === "boolean",
    "promptExtend",
    "boolean",
    errors,
  );
}

function validateHappyhorse(payload, errors) {
  ensure(payload.prompt, isNonEmptyString, "prompt", "non-empty string", errors);
  ensure(
    payload.image,
    (v) =>
      v === undefined ||
      v === null ||
      isImageSource(v) ||
      (Array.isArray(v) && v.length > 0 && v.every((item) => isImageSource(item))),
    "image",
    "public image URL, image data URI, non-empty array of image sources, or null",
    errors,
  );
  ensure(
    payload.duration,
    (v) => typeof v === "number" && Number.isInteger(v) && v >= 3 && v <= 15,
    "duration",
    "an integer from 3 to 15",
    errors,
  );
  ensure(
    payload.resolution,
    (v) => HAPPYHORSE_RESOLUTIONS.includes(v),
    "resolution",
    `one of ${HAPPYHORSE_RESOLUTIONS.join(", ")}`,
    errors,
  );
  ensure(
    payload.ratio,
    (v) => v === undefined || v === null || HAPPYHORSE_RATIOS.includes(v),
    "ratio",
    `one of ${HAPPYHORSE_RATIOS.join(", ")} or null`,
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
  if (model === "minimax") validateMinimax(payload, errors);
  if (model === "t2v_v3") validateT2VV3(payload, errors);
  if (model === "i2v_v3") validateI2VV3(payload, errors);
  if (model === "seedance20") validateSeedance20(payload, errors);
  if (model === "wan30") validateWan30(payload, errors);
  if (model === "happyhorse") validateHappyhorse(payload, errors);

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
