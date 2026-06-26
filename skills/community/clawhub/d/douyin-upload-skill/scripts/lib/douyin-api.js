const path = require("path");
const fs = require("fs");

const { DOUYIN_BASE_URL } = require("./constants");

class DouyinApiError extends Error {
  constructor(message, options = {}) {
    super(message);
    this.name = "DouyinApiError";
    this.code = options.code || null;
    this.status = options.status || null;
    this.details = options.details || null;
    this.response = options.response || null;
  }
}

function buildAuthUrl({ clientKey, redirectUri, scope, state }) {
  const params = new URLSearchParams({
    client_key: clientKey,
    response_type: "code",
    redirect_uri: redirectUri,
    scope,
    state,
  });
  return `${DOUYIN_BASE_URL}/platform/oauth/connect/?${params.toString()}`;
}

async function parseJsonResponse(response) {
  const text = await response.text();
  let json = null;
  if (text) {
    try {
      json = JSON.parse(text);
    } catch (_) {
      json = { raw: text };
    }
  }

  return {
    text,
    json,
  };
}

function extractErrorFromPayload(payload, statusCode) {
  if (!payload || typeof payload !== "object") {
    return null;
  }

  const candidates = [
    {
      code: payload.error_code,
      message: payload.description || payload.error_description || payload.message,
    },
    {
      code: payload.err_no,
      message: payload.err_tips || payload.message,
    },
    {
      code: payload.code,
      message: payload.msg || payload.message,
    },
    {
      code: payload?.extra?.error_code,
      message: payload?.extra?.description || payload?.extra?.error_msg,
    },
  ];

  for (const item of candidates) {
    if (item.code === undefined || item.code === null) {
      continue;
    }

    const numeric = Number(item.code);
    if (!Number.isNaN(numeric) && numeric === 0) {
      continue;
    }

    if (String(item.code) === "0") {
      continue;
    }

    return new DouyinApiError(item.message || "Douyin API returned an error", {
      code: String(item.code),
      status: statusCode,
      details: payload,
      response: payload,
    });
  }

  return null;
}

function unwrapData(payload) {
  if (payload && typeof payload === "object" && payload.data && typeof payload.data === "object") {
    return payload.data;
  }
  return payload;
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const parsed = await parseJsonResponse(response);

  if (!response.ok) {
    const payloadError = extractErrorFromPayload(parsed.json, response.status);
    if (payloadError) {
      throw payloadError;
    }

    throw new DouyinApiError(
      (parsed.json && (parsed.json.message || parsed.json.description || parsed.json.error_description))
      || `Douyin API HTTP ${response.status}`,
      {
        code: `HTTP_${response.status}`,
        status: response.status,
        details: parsed.json || parsed.text,
        response: parsed.json,
      }
    );
  }

  const apiError = extractErrorFromPayload(parsed.json, response.status);
  if (apiError) {
    throw apiError;
  }

  return unwrapData(parsed.json);
}

function extractTokenData(data) {
  if (!data || typeof data !== "object") {
    throw new DouyinApiError("Invalid token payload format.", {
      code: "TOKEN_PAYLOAD_INVALID",
      details: data,
    });
  }

  return {
    access_token: data.access_token,
    refresh_token: data.refresh_token,
    expires_in: data.expires_in,
    refresh_expires_in: data.refresh_expires_in,
    open_id: data.open_id,
    scope: data.scope,
  };
}

async function exchangeCodeForToken({ clientKey, clientSecret, redirectUri, code }) {
  const body = new URLSearchParams({
    client_key: clientKey,
    client_secret: clientSecret,
    grant_type: "authorization_code",
    code,
    redirect_uri: redirectUri,
  });

  const data = await requestJson(`${DOUYIN_BASE_URL}/oauth/access_token/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  return extractTokenData(data);
}

async function refreshAccessToken({ clientKey, clientSecret, refreshToken }) {
  const body = new URLSearchParams({
    client_key: clientKey,
    client_secret: clientSecret,
    grant_type: "refresh_token",
    refresh_token: refreshToken,
  });

  const data = await requestJson(`${DOUYIN_BASE_URL}/oauth/refresh_token/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  return extractTokenData(data);
}

function detectVideoId(payload) {
  const candidates = [
    payload?.video_id,
    payload?.video?.video_id,
    payload?.video?.id,
    payload?.data?.video_id,
    payload?.data?.video?.video_id,
  ];

  for (const item of candidates) {
    if (item) {
      return String(item);
    }
  }

  return null;
}

async function uploadVideoSmall({ accessToken, videoPath }) {
  const buffer = await fs.promises.readFile(videoPath);
  const fileName = path.basename(videoPath);

  const form = new FormData();
  form.append("access_token", accessToken);
  form.append("video", new File([buffer], fileName));

  const payload = await requestJson(`${DOUYIN_BASE_URL}/api/douyin/v1/video/upload_video/`, {
    method: "POST",
    body: form,
  });

  const videoId = detectVideoId(payload);
  if (!videoId) {
    throw new DouyinApiError("Cannot find video_id from upload response.", {
      code: "UPLOAD_VIDEO_ID_MISSING",
      details: payload,
    });
  }

  return {
    videoId,
    raw: payload,
  };
}

function detectCreateResult(payload) {
  const itemId = payload?.item_id || payload?.item?.item_id || payload?.aweme_id || null;
  const videoId = payload?.video_id || payload?.video?.video_id || null;
  return {
    itemId: itemId ? String(itemId) : null,
    videoId: videoId ? String(videoId) : null,
    raw: payload,
  };
}

async function createVideo({ accessToken, videoId, text, privateStatus }) {
  const url = `${DOUYIN_BASE_URL}/api/douyin/v1/video/create_video/?access_token=${encodeURIComponent(accessToken)}`;
  const body = {
    text,
    video_id: videoId,
    private_status: Number(privateStatus),
  };

  const payload = await requestJson(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  return detectCreateResult(payload);
}

function isPermissionLikeError(error) {
  const text = `${error?.message || ""} ${error?.code || ""}`.toLowerCase();
  const status = Number(error?.status || 0);
  if (status === 401 || status === 403) {
    return true;
  }

  return (
    text.includes("permission") ||
    text.includes("scope") ||
    text.includes("video.create.bind") ||
    text.includes("能力") ||
    text.includes("权限") ||
    text.includes("auth")
  );
}

module.exports = {
  DouyinApiError,
  buildAuthUrl,
  createVideo,
  exchangeCodeForToken,
  isPermissionLikeError,
  refreshAccessToken,
  uploadVideoSmall,
};
