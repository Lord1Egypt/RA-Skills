const { CHANNEL_ID_RE, normalizeYouTubeInput } = require("./youtube");

const YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3";
const YOUTUBE_FEED_BASE = "https://www.youtube.com/feeds/videos.xml";

function getFetchImpl(context = {}) {
  if (typeof context.fetch === "function") {
    return context.fetch;
  }

  if (typeof fetch === "function") {
    return fetch.bind(globalThis);
  }

  throw new Error("No fetch implementation is available in the current runtime.");
}

function getApiKey(context = {}) {
  const configuredKey = String(
    context.config?.youtube_api_key || process.env.YOUTUBE_API_KEY || "",
  ).trim();

  if (!configuredKey) {
    throw new Error(
      "Missing YouTube API key. Set config.youtube_api_key or the YOUTUBE_API_KEY environment variable.",
    );
  }

  return configuredKey;
}

function hasApiKey(context = {}) {
  return Boolean(
    String(context.config?.youtube_api_key || process.env.YOUTUBE_API_KEY || "").trim(),
  );
}

function buildUrl(path, params) {
  const url = new URL(`${YOUTUBE_API_BASE}/${path}`);

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === "") {
      return;
    }
    url.searchParams.set(key, String(value));
  });

  return url;
}

async function fetchYouTubeJson(path, params, context = {}) {
  const fetchImpl = getFetchImpl(context);
  const apiKey = getApiKey(context);
  const url = buildUrl(path, {
    ...params,
    key: apiKey,
  });

  const response = await fetchImpl(url.toString(), {
    headers: {
      accept: "application/json",
    },
  });

  const rawBody = await response.text();
  let body;

  try {
    body = rawBody ? JSON.parse(rawBody) : {};
  } catch {
    body = { raw: rawBody };
  }

  if (!response.ok) {
    const apiMessage =
      body?.error?.message || body?.message || `YouTube API request failed with status ${response.status}.`;
    throw new Error(apiMessage);
  }

  return body;
}

async function fetchText(url, context = {}) {
  const fetchImpl = getFetchImpl(context);
  const response = await fetchImpl(url, {
    headers: {
      accept: "application/xml, text/xml, text/html, application/json;q=0.9, */*;q=0.8",
    },
  });

  const body = await response.text();
  if (!response.ok) {
    throw new Error(`Request failed for ${url} with status ${response.status}.`);
  }

  return body;
}

function ensureSingleItem(payload, errorMessage) {
  if (!Array.isArray(payload?.items) || payload.items.length === 0) {
    throw new Error(errorMessage);
  }

  return payload.items[0];
}

function mapChannelResource(channel) {
  return {
    kind: "channel",
    channel_id: channel.id,
    title: channel.snippet?.title,
    description: channel.snippet?.description || "",
    custom_url: channel.snippet?.customUrl,
    published_at: channel.snippet?.publishedAt,
    thumbnails: channel.snippet?.thumbnails || {},
    uploads_playlist_id: channel.contentDetails?.relatedPlaylists?.uploads,
    canonical_url: channel.id ? `https://www.youtube.com/channel/${channel.id}` : undefined,
    follow_ready: Boolean(channel.id && channel.contentDetails?.relatedPlaylists?.uploads),
    unresolved: false,
  };
}

function mapUploadItem(item) {
  const videoId = item.contentDetails?.videoId || item.snippet?.resourceId?.videoId;
  const publishedAt = item.contentDetails?.videoPublishedAt || item.snippet?.publishedAt;

  return {
    video_id: videoId,
    video_url: videoId ? `https://www.youtube.com/watch?v=${videoId}` : undefined,
    title: item.snippet?.title || "Untitled video",
    description: item.snippet?.description || "",
    published_at: publishedAt,
    channel_id: item.snippet?.channelId,
    channel_title: item.snippet?.channelTitle,
    thumbnails: item.snippet?.thumbnails || {},
    playlist_item_id: item.id,
    position: item.snippet?.position,
  };
}

async function getChannelById(channelId, context = {}) {
  const payload = await fetchYouTubeJson(
    "channels",
    {
      part: "snippet,contentDetails",
      id: channelId,
      maxResults: 1,
    },
    context,
  );

  return mapChannelResource(
    ensureSingleItem(payload, `Could not find a YouTube channel for channel ID ${channelId}.`),
  );
}

async function getChannelByHandle(handle, context = {}) {
  const normalizedHandle = String(handle || "").replace(/^@/, "");
  const payload = await fetchYouTubeJson(
    "channels",
    {
      part: "snippet,contentDetails",
      forHandle: normalizedHandle,
      maxResults: 1,
    },
    context,
  );

  const channel = mapChannelResource(
    ensureSingleItem(payload, `Could not find a YouTube channel for handle @${normalizedHandle}.`),
  );

  channel.handle = `@${normalizedHandle}`;
  return channel;
}

async function getChannelByUsername(username, context = {}) {
  const payload = await fetchYouTubeJson(
    "channels",
    {
      part: "snippet,contentDetails",
      forUsername: username,
      maxResults: 1,
    },
    context,
  );

  const channel = mapChannelResource(
    ensureSingleItem(payload, `Could not find a YouTube channel for username ${username}.`),
  );

  channel.username = username;
  return channel;
}

async function resolveChannelFromVideoId(videoId, context = {}) {
  const payload = await fetchYouTubeJson(
    "videos",
    {
      part: "snippet",
      id: videoId,
      maxResults: 1,
    },
    context,
  );

  const video = ensureSingleItem(payload, `Could not find a YouTube video for ID ${videoId}.`);
  const channelId = video.snippet?.channelId;

  if (!channelId) {
    throw new Error(`The video ${videoId} does not expose a parent channel ID.`);
  }

  const channel = await getChannelById(channelId, context);
  channel.resolved_from_video_id = videoId;
  return channel;
}

async function resolveYouTubeTarget(source, context = {}) {
  if (hasApiKey(context)) {
    return resolveYouTubeTargetWithApi(source, context);
  }

  return resolveYouTubeTargetFromPublicSource(source, context);
}

async function resolveYouTubeTargetWithApi(source, context = {}) {
  const normalized = normalizeYouTubeInput(source);

  if (!normalized.ok) {
    throw new Error(normalized.message || "Unable to normalize YouTube input.");
  }

  if (normalized.kind === "channel") {
    const channel = await getChannelById(normalized.channel_id, context);
    return {
      normalized,
      target: channel,
    };
  }

  if (normalized.kind === "handle") {
    const channel = await getChannelByHandle(normalized.handle, context);
    return {
      normalized,
      target: channel,
    };
  }

  if (normalized.kind === "legacy_username") {
    const channel = await getChannelByUsername(normalized.username, context);
    return {
      normalized,
      target: channel,
    };
  }

  if (normalized.kind === "video") {
    const channel = await resolveChannelFromVideoId(normalized.video_id, context);
    return {
      normalized,
      target: channel,
    };
  }

  if (normalized.kind === "custom_channel_url") {
    throw new Error(
      "Custom /c/ YouTube URLs are not resolved yet. Use a channel URL, @handle, username URL, or a video URL instead.",
    );
  }

  throw new Error(`Unsupported YouTube target kind: ${normalized.kind}`);
}

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function decodeHtmlEntities(text) {
  return String(text || "")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'");
}

function extractFirstMatch(text, regex) {
  const match = String(text || "").match(regex);
  return match ? decodeHtmlEntities(match[1]) : null;
}

function extractXmlTag(block, tag) {
  const safeTag = escapeRegex(tag);
  return extractFirstMatch(
    block,
    new RegExp(`<${safeTag}(?:\\s[^>]*)?>([\\s\\S]*?)<\\/${safeTag}>`, "i"),
  );
}

function extractEntryLink(entryBlock) {
  return (
    extractFirstMatch(
      entryBlock,
      /<link\b[^>]*rel=["']alternate["'][^>]*href=["']([^"']+)["'][^>]*\/?>/i,
    ) ||
    extractFirstMatch(
      entryBlock,
      /<link\b[^>]*href=["']([^"']+)["'][^>]*rel=["']alternate["'][^>]*\/?>/i,
    ) ||
    extractFirstMatch(entryBlock, /<link\b[^>]*href=["']([^"']+)["'][^>]*\/?>/i)
  );
}

function extractPageMetadata(html) {
  const feedUrl =
    extractFirstMatch(
      html,
      /<link\b[^>]*type=["']application\/rss\+xml["'][^>]*href=["']([^"']+)["'][^>]*>/i,
    ) ||
    extractFirstMatch(
      html,
      /<link\b[^>]*href=["']([^"']*feeds\/videos\.xml\?channel_id=[^"']+)["'][^>]*>/i,
    );

  const channelId =
    (feedUrl && extractFirstMatch(feedUrl, /channel_id=(UC[A-Za-z0-9_-]{22})/)) ||
    extractFirstMatch(html, /"channelId":"(UC[A-Za-z0-9_-]{22})"/) ||
    extractFirstMatch(html, /"externalId":"(UC[A-Za-z0-9_-]{22})"/) ||
    extractFirstMatch(html, /itemprop=["']channelId["'][^>]*content=["'](UC[A-Za-z0-9_-]{22})["']/i);

  const canonicalUrl =
    extractFirstMatch(html, /<link rel=["']canonical["'] href=["']([^"']+)["']/i) ||
    (channelId ? `https://www.youtube.com/channel/${channelId}` : null);

  const title =
    extractFirstMatch(html, /<meta property=["']og:title["'] content=["']([^"']+)["']/i) ||
    extractFirstMatch(html, /<title>([^<]+)<\/title>/i);

  return {
    channel_id: channelId,
    canonical_url: canonicalUrl,
    feed_url: feedUrl,
    title: title ? title.replace(/\s*-\s*YouTube\s*$/i, "").trim() : null,
  };
}

function parseYouTubeFeed(xml) {
  const feedChannelId =
    extractFirstMatch(xml, /<feed\b[\s\S]*?<yt:channelId>(UC[A-Za-z0-9_-]{22})<\/yt:channelId>/i) ||
    null;
  const feedTitle = extractFirstMatch(xml, /<feed\b[\s\S]*?<title>([\s\S]*?)<\/title>/i);
  const feedAuthor = extractFirstMatch(xml, /<feed\b[\s\S]*?<author>\s*<name>([\s\S]*?)<\/name>/i);
  const entries = Array.from(String(xml || "").matchAll(/<entry\b[\s\S]*?<\/entry>/gi)).map(
    (match) => {
      const entry = match[0];
      const videoId = extractXmlTag(entry, "yt:videoId");
      const channelId = extractXmlTag(entry, "yt:channelId") || feedChannelId;
      const title = extractXmlTag(entry, "title") || extractXmlTag(entry, "media:title");
      const description = extractXmlTag(entry, "media:description") || "";
      const publishedAt = extractXmlTag(entry, "published") || extractXmlTag(entry, "updated");
      const channelTitle = extractFirstMatch(
        entry,
        /<author>\s*<name>([\s\S]*?)<\/name>/i,
      ) || feedAuthor;

      return {
        video_id: videoId,
        video_url: extractEntryLink(entry) || (videoId ? `https://www.youtube.com/watch?v=${videoId}` : undefined),
        title: title || "Untitled video",
        description,
        published_at: publishedAt,
        channel_id: channelId,
        channel_title: channelTitle || feedTitle || null,
        thumbnails: {},
      };
    },
  );

  return {
    channel_id: feedChannelId,
    channel_title: feedAuthor || feedTitle || null,
    entries,
  };
}

async function resolveYouTubeTargetFromPublicSource(source, context = {}) {
  const normalized = normalizeYouTubeInput(source);

  if (!normalized.ok) {
    throw new Error(normalized.message || "Unable to normalize YouTube input.");
  }

  if (normalized.kind === "playlist") {
    throw new Error("Playlist inputs are not supported as creator watch targets.");
  }

  if (normalized.kind === "channel" && normalized.channel_id) {
    return {
      normalized,
      target: {
        kind: "channel",
        channel_id: normalized.channel_id,
        title: null,
        description: "",
        custom_url: "",
        published_at: null,
        thumbnails: {},
        uploads_playlist_id: null,
        canonical_url: normalized.canonical_url,
        follow_ready: true,
        unresolved: false,
      },
    };
  }

  const html = await fetchText(normalized.canonical_url, context);
  const metadata = extractPageMetadata(html);
  const channelId = metadata.channel_id;

  if (!channelId || !CHANNEL_ID_RE.test(channelId)) {
    throw new Error(
      "Could not resolve a stable YouTube channel ID without the API key. Try a channel URL, or configure youtube_api_key for stronger resolution.",
    );
  }

  return {
    normalized,
    target: {
      kind: "channel",
      channel_id: channelId,
      title: metadata.title || null,
      description: "",
      custom_url: normalized.kind === "handle" ? normalized.handle : "",
      published_at: null,
      thumbnails: {},
      uploads_playlist_id: null,
      canonical_url: metadata.canonical_url || `https://www.youtube.com/channel/${channelId}`,
      follow_ready: true,
      unresolved: false,
      resolved_from_video_id: normalized.kind === "video" ? normalized.video_id : undefined,
    },
  };
}

async function fetchLatestUploadsWithApi(source, options = {}, context = {}) {
  const limit = Math.max(1, Math.min(Number(options.limit) || 5, 10));
  const resolution = await resolveYouTubeTargetWithApi(source, context);

  if (!resolution.target.uploads_playlist_id) {
    throw new Error("The resolved YouTube channel does not expose an uploads playlist.");
  }

  const payload = await fetchYouTubeJson(
    "playlistItems",
    {
      part: "snippet,contentDetails",
      playlistId: resolution.target.uploads_playlist_id,
      maxResults: limit,
    },
    context,
  );

  const uploads = Array.isArray(payload.items) ? payload.items.map(mapUploadItem) : [];

  return {
    normalized: resolution.normalized,
    target: resolution.target,
    uploads,
    latest_upload: uploads[0] || null,
  };
}

async function fetchLatestUploadsFromPublicFeed(source, options = {}, context = {}) {
  const limit = Math.max(1, Math.min(Number(options.limit) || 5, 10));
  const resolution = await resolveYouTubeTargetFromPublicSource(source, context);
  const feedUrl = `${YOUTUBE_FEED_BASE}?channel_id=${resolution.target.channel_id}`;
  const xml = await fetchText(feedUrl, context);
  const parsed = parseYouTubeFeed(xml);
  const uploads = parsed.entries.slice(0, limit);

  return {
    normalized: resolution.normalized,
    target: {
      ...resolution.target,
      title: resolution.target.title || parsed.channel_title,
    },
    uploads,
    latest_upload: uploads[0] || null,
  };
}

async function fetchLatestUploads(source, options = {}, context = {}) {
  if (hasApiKey(context)) {
    return fetchLatestUploadsWithApi(source, options, context);
  }

  return fetchLatestUploadsFromPublicFeed(source, options, context);
}

module.exports = {
  fetchLatestUploads,
  hasApiKey,
  resolveYouTubeTarget,
  getApiKey,
};
