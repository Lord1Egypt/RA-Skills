const fs = require("node:fs/promises");
const path = require("node:path");

const STORE_VERSION = 1;

function getWatchlistPath(context = {}) {
  const configured = String(context.config?.watchlist_path || "").trim();
  if (configured) {
    return path.resolve(configured);
  }

  return path.resolve(process.cwd(), "data", "watchlist.json");
}

async function ensureParentDir(filePath) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
}

function normalizeStore(data) {
  if (!data || typeof data !== "object") {
    return {
      version: STORE_VERSION,
      follows: [],
    };
  }

  return {
    version: Number(data.version) || STORE_VERSION,
    follows: Array.isArray(data.follows) ? data.follows : [],
  };
}

async function loadStore(context = {}) {
  const filePath = getWatchlistPath(context);

  try {
    const raw = await fs.readFile(filePath, "utf8");
    return {
      path: filePath,
      data: normalizeStore(JSON.parse(raw)),
    };
  } catch (error) {
    if (error.code === "ENOENT") {
      return {
        path: filePath,
        data: normalizeStore(null),
      };
    }
    throw error;
  }
}

async function saveStore(context = {}, data) {
  const filePath = getWatchlistPath(context);
  await ensureParentDir(filePath);
  await fs.writeFile(filePath, JSON.stringify(normalizeStore(data), null, 2) + "\n", "utf8");
  return filePath;
}

function toFollowRecord(target, options = {}) {
  const now = new Date().toISOString();
  return {
    channel_id: target.channel_id,
    title: target.title || "",
    description: target.description || "",
    canonical_url: target.canonical_url || "",
    custom_url: target.custom_url || "",
    handle: target.handle || "",
    username: target.username || "",
    uploads_playlist_id: target.uploads_playlist_id || "",
    source_input: options.source_input || "",
    source_kind: options.source_kind || "",
    followed_at: options.followed_at || now,
    updated_at: now,
    last_checked_at: options.last_checked_at || null,
    last_seen_video_id: options.last_seen_video_id || null,
    last_seen_published_at: options.last_seen_published_at || null,
    last_seen_title: options.last_seen_title || null,
  };
}

function canonicalMatchValue(value) {
  return String(value || "").trim().toLowerCase();
}

function matchFollowBySource(follow, source) {
  const needle = canonicalMatchValue(source);
  if (!needle) {
    return false;
  }

  return [
    follow.channel_id,
    follow.canonical_url,
    follow.custom_url,
    follow.handle,
    follow.username,
    follow.source_input,
  ]
    .map(canonicalMatchValue)
    .some((value) => value && value === needle);
}

async function listFollows(context = {}) {
  const store = await loadStore(context);
  return {
    path: store.path,
    follows: store.data.follows,
  };
}

async function upsertFollow(target, options = {}, context = {}) {
  const store = await loadStore(context);
  const follows = [...store.data.follows];
  const index = follows.findIndex((follow) => follow.channel_id === target.channel_id);
  const existing = index >= 0 ? follows[index] : null;

  const nextRecord = toFollowRecord(target, {
    source_input: options.source_input,
    source_kind: options.source_kind,
    followed_at: existing?.followed_at,
    last_checked_at: options.last_checked_at ?? existing?.last_checked_at,
    last_seen_video_id: options.last_seen_video_id ?? existing?.last_seen_video_id,
    last_seen_published_at:
      options.last_seen_published_at ?? existing?.last_seen_published_at,
    last_seen_title: options.last_seen_title ?? existing?.last_seen_title,
  });

  if (index >= 0) {
    follows[index] = nextRecord;
  } else {
    follows.push(nextRecord);
  }

  await saveStore(context, {
    version: STORE_VERSION,
    follows,
  });

  return {
    created: index === -1,
    follow: nextRecord,
    count: follows.length,
  };
}

async function removeFollow(source, context = {}) {
  const store = await loadStore(context);
  const follows = [...store.data.follows];
  const index = follows.findIndex((follow) => matchFollowBySource(follow, source));

  if (index === -1) {
    return {
      removed: false,
      count: follows.length,
      follow: null,
    };
  }

  const [removedFollow] = follows.splice(index, 1);
  await saveStore(context, {
    version: STORE_VERSION,
    follows,
  });

  return {
    removed: true,
    count: follows.length,
    follow: removedFollow,
  };
}

module.exports = {
  getWatchlistPath,
  listFollows,
  loadStore,
  matchFollowBySource,
  removeFollow,
  saveStore,
  upsertFollow,
};
