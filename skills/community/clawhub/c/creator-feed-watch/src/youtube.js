const CHANNEL_ID_RE = /^UC[A-Za-z0-9_-]{22}$/;
const VIDEO_ID_RE = /^[A-Za-z0-9_-]{11}$/;

function maybeUrl(raw) {
  if (!raw) {
    return null;
  }

  const trimmed = String(raw).trim();
  const withProtocol =
    trimmed.startsWith("http://") ||
    trimmed.startsWith("https://") ||
    trimmed.startsWith("@") ||
    CHANNEL_ID_RE.test(trimmed)
      ? trimmed
      : trimmed.startsWith("youtube.com/") ||
          trimmed.startsWith("www.youtube.com/") ||
          trimmed.startsWith("m.youtube.com/") ||
          trimmed.startsWith("youtu.be/")
        ? `https://${trimmed}`
        : trimmed;

  try {
    return new URL(withProtocol);
  } catch {
    return null;
  }
}

function normalizeYouTubeInput(source) {
  const raw = String(source || "").trim();
  if (!raw) {
    return {
      ok: false,
      message: "Missing YouTube input.",
    };
  }

  if (CHANNEL_ID_RE.test(raw)) {
    return {
      ok: true,
      kind: "channel",
      raw,
      channel_id: raw,
      canonical_url: `https://www.youtube.com/channel/${raw}`,
      unresolved: false,
      follow_ready: true,
    };
  }

  if (raw.startsWith("@")) {
    return {
      ok: true,
      kind: "handle",
      raw,
      handle: raw,
      canonical_url: `https://www.youtube.com/${raw}`,
      unresolved: true,
      follow_ready: false,
      recommended_next_step: "Resolve this handle to a stable channel ID before persisting it.",
    };
  }

  const url = maybeUrl(raw);
  if (!url) {
    return {
      ok: false,
      raw,
      message: "Input is not a recognized YouTube URL, handle, or channel ID.",
    };
  }

  const host = url.hostname.replace(/^www\./, "").replace(/^m\./, "");

  if (host === "youtu.be") {
    const videoId = url.pathname.split("/").filter(Boolean)[0];
    return {
      ok: Boolean(videoId && VIDEO_ID_RE.test(videoId)),
      kind: "video",
      raw,
      video_id: videoId,
      canonical_url: `https://www.youtube.com/watch?v=${videoId}`,
      unresolved: true,
      follow_ready: false,
      recommended_next_step: "Resolve this video to its parent channel before adding it to a watchlist.",
    };
  }

  if (host !== "youtube.com") {
    return {
      ok: false,
      raw,
      message: "Only YouTube URLs are supported.",
    };
  }

  const parts = url.pathname.split("/").filter(Boolean);
  const first = parts[0] || "";
  const second = parts[1] || "";

  if (first === "channel" && CHANNEL_ID_RE.test(second)) {
    return {
      ok: true,
      kind: "channel",
      raw,
      channel_id: second,
      canonical_url: `https://www.youtube.com/channel/${second}`,
      unresolved: false,
      follow_ready: true,
    };
  }

  if (first.startsWith("@")) {
    return {
      ok: true,
      kind: "handle",
      raw,
      handle: first,
      canonical_url: `https://www.youtube.com/${first}`,
      unresolved: true,
      follow_ready: false,
      recommended_next_step: "Resolve this handle to a stable channel ID before persisting it.",
    };
  }

  if (first === "watch") {
    const videoId = url.searchParams.get("v");
    return {
      ok: Boolean(videoId && VIDEO_ID_RE.test(videoId)),
      kind: "video",
      raw,
      video_id: videoId,
      canonical_url: videoId ? `https://www.youtube.com/watch?v=${videoId}` : undefined,
      unresolved: true,
      follow_ready: false,
      recommended_next_step: "Resolve this video to its parent channel before adding it to a watchlist.",
    };
  }

  if (first === "shorts" || first === "live") {
    return {
      ok: Boolean(second && VIDEO_ID_RE.test(second)),
      kind: "video",
      raw,
      video_id: second,
      canonical_url: second ? `https://www.youtube.com/watch?v=${second}` : undefined,
      unresolved: true,
      follow_ready: false,
      recommended_next_step: "Resolve this video to its parent channel before adding it to a watchlist.",
    };
  }

  if (first === "playlist") {
    const playlistId = url.searchParams.get("list");
    return {
      ok: Boolean(playlistId),
      kind: "playlist",
      raw,
      playlist_id: playlistId,
      canonical_url: playlistId
        ? `https://www.youtube.com/playlist?list=${playlistId}`
        : undefined,
      unresolved: true,
      follow_ready: false,
      recommended_next_step: "Playlists are not stable creator watch targets yet.",
    };
  }

  if (first === "user") {
    return {
      ok: true,
      kind: "legacy_username",
      raw,
      username: second,
      canonical_url: `https://www.youtube.com/user/${second}`,
      unresolved: true,
      follow_ready: false,
      recommended_next_step: "Resolve this legacy username to a stable channel ID before persisting it.",
    };
  }

  if (first === "c") {
    return {
      ok: true,
      kind: "custom_channel_url",
      raw,
      custom_path: `c/${second}`.replace(/\/$/, ""),
      canonical_url: `https://www.youtube.com/${first}/${second}`,
      unresolved: true,
      follow_ready: false,
      recommended_next_step: "Resolve this custom channel URL to a stable channel ID before persisting it.",
    };
  }

  return {
    ok: false,
    raw,
    message: "YouTube input format is recognized, but this path is not handled yet.",
  };
}

module.exports = {
  CHANNEL_ID_RE,
  VIDEO_ID_RE,
  normalizeYouTubeInput,
};
