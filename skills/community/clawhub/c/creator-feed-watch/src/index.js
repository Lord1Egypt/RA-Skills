const { normalizeYouTubeInput } = require("./youtube");
const { fetchLatestUploads, resolveYouTubeTarget } = require("./youtube-api");
const { buildNotification, dispatchNotifications } = require("./delivery");
const { summarizeVideoMetadata } = require("./summary");
const { listFollows, removeFollow, upsertFollow } = require("./watchlist-store");
const { analyzeVideo } = require("./analyze");
const { fetchTranscript } = require("./transcript");

function buildLatestUpdate(latestUpload, target) {
  if (!latestUpload) {
    return null;
  }

  return summarizeVideoMetadata({
    channel_name: latestUpload.channel_title || target?.title,
    video_title: latestUpload.title,
    video_description: latestUpload.description,
    video_url: latestUpload.video_url,
    published_at: latestUpload.published_at,
  });
}

async function scanWatchlistUpdates(context = {}, options = {}) {
  const watchlist = await listFollows(context);
  const markSeen = options.mark_seen !== false;
  const updates = [];
  const checked = [];

  for (const follow of watchlist.follows) {
    try {
      const latest = await fetchLatestUploads(follow.channel_id, { limit: 1 }, context);
      const latestUpload = latest.latest_upload;
      const hasUpdate = Boolean(
        latestUpload &&
          latestUpload.video_id &&
          latestUpload.video_id !== follow.last_seen_video_id,
      );

      let storedFollow = follow;
      if (latestUpload) {
        const stored = await upsertFollow(
          latest.target,
          {
            source_input: follow.source_input || follow.canonical_url || follow.channel_id,
            source_kind: follow.source_kind || "channel",
            last_checked_at: new Date().toISOString(),
            last_seen_video_id:
              hasUpdate && !markSeen ? follow.last_seen_video_id : latestUpload.video_id,
            last_seen_published_at:
              hasUpdate && !markSeen
                ? follow.last_seen_published_at
                : latestUpload.published_at,
            last_seen_title:
              hasUpdate && !markSeen ? follow.last_seen_title : latestUpload.title,
          },
          context,
        );
        storedFollow = stored.follow;
      }

      checked.push({
        follow: storedFollow,
        latest_upload: latestUpload,
        has_update: hasUpdate,
      });

      if (hasUpdate) {
        updates.push({
          follow: storedFollow,
          latest_upload: latestUpload,
          latest_update: buildLatestUpdate(latestUpload, latest.target),
        });
      }
    } catch (error) {
      checked.push({
        follow,
        has_update: false,
        error: error.message || "Failed to check follow target.",
      });
    }
  }

  return {
    count: watchlist.follows.length,
    update_count: updates.length,
    checked,
    updates,
  };
}

async function markUpdatesSeen(updates, context = {}) {
  for (const update of updates) {
    const follow = update.follow || {};
    const latestUpload = update.latest_upload || {};
    await upsertFollow(
      {
        channel_id: follow.channel_id,
        title: follow.title,
        description: follow.description,
        canonical_url: follow.canonical_url,
        custom_url: follow.custom_url,
        handle: follow.handle,
        username: follow.username,
        uploads_playlist_id: follow.uploads_playlist_id,
      },
      {
        source_input: follow.source_input || follow.canonical_url || follow.channel_id,
        source_kind: follow.source_kind || "channel",
        last_checked_at: new Date().toISOString(),
        last_seen_video_id: latestUpload.video_id || follow.last_seen_video_id,
        last_seen_published_at: latestUpload.published_at || follow.last_seen_published_at,
        last_seen_title: latestUpload.title || follow.last_seen_title,
      },
      context,
    );
  }
}

async function handler(input = {}, context = {}) {
  const action = input.action;

  if (!action) {
    return {
      ok: false,
      message: "Missing required input: action.",
    };
  }

  if (action === "healthcheck") {
    return {
      ok: true,
      action,
      message: "creator-feed-watch is ready.",
      config_present: Object.keys(context.config || {}).length > 0,
    };
  }

  if (action === "normalize_target") {
    if (!input.source) {
      return {
        ok: false,
        action,
        message: "Missing required input: source.",
      };
    }

    const normalized = normalizeYouTubeInput(input.source);
    return {
      ok: normalized.ok,
      action,
      normalized,
      message: normalized.ok
        ? "YouTube input normalized."
        : normalized.message || "Unable to normalize input.",
    };
  }

  if (action === "prepare_update") {
    const update = summarizeVideoMetadata(input);
    return {
      ok: true,
      action,
      update,
      message: "Prepared update card from video metadata.",
    };
  }

  if (action === "fetch_latest_uploads") {
    if (!input.source) {
      return {
        ok: false,
        action,
        message: "Missing required input: source.",
      };
    }

    try {
      const latest = await fetchLatestUploads(
        input.source,
        { limit: input.limit },
        context,
      );

      return {
        ok: true,
        action,
        target: latest.target,
        normalized: latest.normalized,
        uploads: latest.uploads,
        latest_upload: latest.latest_upload,
        latest_update: buildLatestUpdate(latest.latest_upload, latest.target),
        message: latest.uploads.length
          ? `Fetched ${latest.uploads.length} recent upload(s).`
          : "No uploads were returned for this channel.",
      };
    } catch (error) {
      return {
        ok: false,
        action,
        message: error.message || "Failed to fetch latest YouTube uploads.",
      };
    }
  }

  if (action === "list_follows") {
    const watchlist = await listFollows(context);
    return {
      ok: true,
      action,
      follows: watchlist.follows,
      count: watchlist.follows.length,
      storage_path: watchlist.path,
      message: watchlist.follows.length
        ? `Loaded ${watchlist.follows.length} follow target(s).`
        : "Watchlist is empty.",
    };
  }

  if (action === "add_follow") {
    if (!input.source) {
      return {
        ok: false,
        action,
        message: "Missing required input: source.",
      };
    }

    try {
      const resolved = await resolveYouTubeTarget(input.source, context);
      let latest = null;

      if (input.seed_latest !== false) {
        latest = await fetchLatestUploads(input.source, { limit: 1 }, context);
      }

      const stored = await upsertFollow(
        resolved.target,
        {
          source_input: input.source,
          source_kind: resolved.normalized.kind,
          last_checked_at: latest ? new Date().toISOString() : null,
          last_seen_video_id: latest?.latest_upload?.video_id || null,
          last_seen_published_at: latest?.latest_upload?.published_at || null,
          last_seen_title: latest?.latest_upload?.title || null,
        },
        context,
      );

      return {
        ok: true,
        action,
        created: stored.created,
        follow: stored.follow,
        latest_upload: latest?.latest_upload || null,
        latest_update: buildLatestUpdate(latest?.latest_upload || null, resolved.target),
        count: stored.count,
        message: stored.created
          ? "Added creator to watchlist."
          : "Updated existing creator in watchlist.",
      };
    } catch (error) {
      return {
        ok: false,
        action,
        message: error.message || "Failed to add follow target.",
      };
    }
  }

  if (action === "remove_follow") {
    if (!input.source) {
      return {
        ok: false,
        action,
        message: "Missing required input: source.",
      };
    }

    const removed = await removeFollow(input.source, context);
    return {
      ok: removed.removed,
      action,
      follow: removed.follow,
      count: removed.count,
      message: removed.removed
        ? "Removed creator from watchlist."
        : "No matching follow target was found.",
    };
  }

  if (action === "analyze_video") {
    if (!input.source) {
      return {
        ok: false,
        action,
        message: "Missing required input: source.",
      };
    }

    try {
      const analysis = await analyzeVideo(input.source, context);
      return {
        ok: true,
        action,
        video_id: analysis.video_id,
        video_url: analysis.video_url,
        title: analysis.title,
        description: analysis.description,
        published_at: analysis.published_at,
        channel_id: analysis.channel_id,
        channel_name: analysis.channel_name,
        has_transcript: analysis.has_transcript,
        transcript_language: analysis.transcript_language,
        transcript_text: analysis.transcript_text,
        message: analysis.has_transcript
          ? "Video materials collected with transcript."
          : "Video materials collected without transcript (captions unavailable).",
      };
    } catch (error) {
      return {
        ok: false,
        action,
        message: error.message || "Failed to analyze video.",
      };
    }
  }

  if (action === "check_watchlist_updates") {
    const scanned = await scanWatchlistUpdates(context, {
      mark_seen: input.mark_seen,
    });

    return {
      ok: true,
      action,
      count: scanned.count,
      update_count: scanned.update_count,
      checked: scanned.checked,
      updates: scanned.updates,
      message: scanned.update_count
        ? `Found ${scanned.update_count} follow target(s) with new uploads.`
        : "No new uploads found across the watchlist.",
    };
  }

  if (action === "notify_watchlist_updates") {
    const scanned = await scanWatchlistUpdates(context, {
      mark_seen: false,
    });

    if (scanned.update_count === 0) {
      return {
        ok: true,
        action,
        count: scanned.count,
        update_count: 0,
        notifications: [],
        deliveries: [],
        message: "No new uploads found across the watchlist.",
      };
    }

    const notifications = scanned.updates.map((update) =>
      buildNotification(update, {
        delivery_target: input.delivery_target || context.config?.delivery_target || null,
      }),
    );

    const delivery = await dispatchNotifications(
      notifications,
      {
        delivery_target: input.delivery_target || context.config?.delivery_target || null,
      },
      context,
    );

    if (delivery.ok && input.mark_seen !== false) {
      await markUpdatesSeen(scanned.updates, context);
    }

    return {
      ok: delivery.ok,
      action,
      count: scanned.count,
      update_count: scanned.update_count,
      notifications,
      deliveries: delivery.deliveries,
      delivered_count: delivery.delivered_count,
      failed_count: delivery.failed_count,
      adapter: delivery.adapter,
      message: delivery.message,
    };
  }

  return {
    ok: false,
    action,
    message: `Unsupported action: ${action}`,
  };
}

module.exports = handler;
module.exports._internal = {
  analyzeVideo,
  buildNotification,
  dispatchNotifications,
  fetchLatestUploads,
  fetchTranscript,
  listFollows,
  markUpdatesSeen,
  normalizeYouTubeInput,
  removeFollow,
  resolveYouTubeTarget,
  scanWatchlistUpdates,
  summarizeVideoMetadata,
  upsertFollow,
};
