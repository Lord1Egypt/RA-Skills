const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs/promises");
const os = require("node:os");
const path = require("node:path");

const handler = require("../src/index");
const { extractCaptionTracks, pickBestTrack, parseTranscriptXml } = require("../src/transcript");

async function makeContext(overrides = {}) {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "creator-feed-watch-"));
  return {
    config: {
      watchlist_path: path.join(tempDir, "watchlist.json"),
      ...overrides.config,
    },
    fetch: overrides.fetch,
  };
}

function jsonResponse(payload, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    text: async () => JSON.stringify(payload),
  };
}

function textResponse(payload, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    text: async () => String(payload),
  };
}

test("normalizes a YouTube handle", async () => {
  const result = await handler({
    action: "normalize_target",
    source: "@OpenAI",
  });

  assert.equal(result.ok, true);
  assert.equal(result.normalized.kind, "handle");
  assert.equal(result.normalized.handle, "@OpenAI");
});

test("normalizes a channel URL with channel id", async () => {
  const result = await handler({
    action: "normalize_target",
    source: "https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw",
  });

  assert.equal(result.ok, true);
  assert.equal(result.normalized.kind, "channel");
  assert.equal(result.normalized.follow_ready, true);
});

test("normalizes a watch URL", async () => {
  const result = await handler({
    action: "normalize_target",
    source: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  });

  assert.equal(result.ok, true);
  assert.equal(result.normalized.kind, "video");
  assert.equal(result.normalized.video_id, "dQw4w9WgXcQ");
});

test("prepares an update card", async () => {
  const result = await handler({
    action: "prepare_update",
    channel_name: "OpenAI",
    video_title: "How we built the next demo",
    video_description:
      "A short behind-the-scenes walkthrough.\nWhat changed in the stack.\nWhy the demo matters.",
    video_url: "https://www.youtube.com/watch?v=abc123def45",
    published_at: "2026-03-20T12:00:00Z",
  });

  assert.equal(result.ok, true);
  assert.equal(result.update.headline, "OpenAI: How we built the next demo");
  assert.equal(result.update.bullets.length, 3);
  assert.match(
    result.update.markdown,
    /Watch: https:\/\/www\.youtube\.com\/watch\?v=abc123def45/,
  );
});

test("fetches latest uploads for a handle", async () => {
  const fetchStub = async (url) => {
    const parsed = new URL(url);
    const pathName = parsed.pathname;

    if (pathName.endsWith("/channels") && parsed.searchParams.get("forHandle") === "OpenAI") {
      return jsonResponse({
        items: [
          {
            id: "UC1234567890123456789012",
            snippet: {
              title: "OpenAI",
              description: "AI research and products.",
              customUrl: "@OpenAI",
              publishedAt: "2015-01-01T00:00:00Z",
              thumbnails: {
                default: { url: "https://img.example.com/channel-default.jpg" },
              },
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF1234567890123456789012",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/playlistItems") &&
      parsed.searchParams.get("playlistId") === "UULF1234567890123456789012"
    ) {
      return jsonResponse({
        items: [
          {
            id: "playlist-item-1",
            snippet: {
              title: "New Demo Walkthrough",
              description: "A short breakdown.\nMain takeaways.\nWhat ships next.",
              publishedAt: "2026-03-20T12:00:00Z",
              channelId: "UC1234567890123456789012",
              channelTitle: "OpenAI",
              position: 0,
              resourceId: {
                videoId: "abc123def45",
              },
              thumbnails: {
                medium: { url: "https://img.example.com/video-medium.jpg" },
              },
            },
            contentDetails: {
              videoId: "abc123def45",
              videoPublishedAt: "2026-03-20T12:00:00Z",
            },
          },
          {
            id: "playlist-item-2",
            snippet: {
              title: "Previous Update",
              description: "Last week's recap.",
              publishedAt: "2026-03-18T12:00:00Z",
              channelId: "UC1234567890123456789012",
              channelTitle: "OpenAI",
              position: 1,
              resourceId: {
                videoId: "xyz987uvw65",
              },
              thumbnails: {},
            },
            contentDetails: {
              videoId: "xyz987uvw65",
              videoPublishedAt: "2026-03-18T12:00:00Z",
            },
          },
        ],
      });
    }

    return jsonResponse(
      {
        error: {
          message: `Unexpected request: ${url}`,
        },
      },
      404,
    );
  };

  const context = await makeContext({
    config: {
      youtube_api_key: "test-key",
    },
    fetch: fetchStub,
  });

  const result = await handler(
    {
      action: "fetch_latest_uploads",
      source: "@OpenAI",
      limit: 2,
    },
    context,
  );

  assert.equal(result.ok, true);
  assert.equal(result.target.channel_id, "UC1234567890123456789012");
  assert.equal(result.uploads.length, 2);
  assert.equal(result.latest_upload.video_id, "abc123def45");
  assert.match(result.latest_update.markdown, /New Demo Walkthrough/);
});

test("fetches latest uploads without an API key by using the public page and feed fallback", async () => {
  const feedXml = `<?xml version="1.0" encoding="UTF-8"?>
  <feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns:media="http://search.yahoo.com/mrss/">
    <title>OpenAI</title>
    <author><name>OpenAI</name></author>
    <yt:channelId>UC1234567890123456789012</yt:channelId>
    <entry>
      <yt:videoId>abc123def45</yt:videoId>
      <yt:channelId>UC1234567890123456789012</yt:channelId>
      <title>New Demo Walkthrough</title>
      <link rel="alternate" href="https://www.youtube.com/watch?v=abc123def45"/>
      <author><name>OpenAI</name></author>
      <published>2026-03-20T12:00:00Z</published>
      <media:group>
        <media:title>New Demo Walkthrough</media:title>
        <media:description>A short breakdown.</media:description>
      </media:group>
    </entry>
  </feed>`;

  const fetchStub = async (url) => {
    if (url === "https://www.youtube.com/@OpenAI") {
      return textResponse(
        `<html><head>
          <meta property="og:title" content="OpenAI">
          <link rel="alternate" type="application/rss+xml" title="RSS" href="https://www.youtube.com/feeds/videos.xml?channel_id=UC1234567890123456789012">
          <link rel="canonical" href="https://www.youtube.com/@OpenAI">
        </head></html>`,
      );
    }

    if (url === "https://www.youtube.com/feeds/videos.xml?channel_id=UC1234567890123456789012") {
      return textResponse(feedXml);
    }

    return jsonResponse({ error: { message: `Unexpected request: ${url}` } }, 404);
  };

  const context = await makeContext({
    fetch: fetchStub,
  });

  const result = await handler(
    {
      action: "fetch_latest_uploads",
      source: "@OpenAI",
    },
    context,
  );

  assert.equal(result.ok, true);
  assert.equal(result.target.channel_id, "UC1234567890123456789012");
  assert.equal(result.latest_upload.video_id, "abc123def45");
});

test("resolves a pasted video URL back to its channel before fetching uploads", async () => {
  const fetchStub = async (url) => {
    const parsed = new URL(url);
    const pathName = parsed.pathname;

    if (pathName.endsWith("/videos") && parsed.searchParams.get("id") === "dQw4w9WgXcQ") {
      return jsonResponse({
        items: [
          {
            id: "dQw4w9WgXcQ",
            snippet: {
              channelId: "UC9999999999999999999999",
              channelTitle: "Example Creator",
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/channels") &&
      parsed.searchParams.get("id") === "UC9999999999999999999999"
    ) {
      return jsonResponse({
        items: [
          {
            id: "UC9999999999999999999999",
            snippet: {
              title: "Example Creator",
              description: "Example channel.",
              publishedAt: "2024-01-01T00:00:00Z",
              thumbnails: {},
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF9999999999999999999999",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/playlistItems") &&
      parsed.searchParams.get("playlistId") === "UULF9999999999999999999999"
    ) {
      return jsonResponse({
        items: [
          {
            id: "playlist-item-video-resolution",
            snippet: {
              title: "Fresh Upload",
              description: "A quick update.",
              publishedAt: "2026-03-21T09:00:00Z",
              channelId: "UC9999999999999999999999",
              channelTitle: "Example Creator",
              position: 0,
              resourceId: {
                videoId: "newvideo1234",
              },
              thumbnails: {},
            },
            contentDetails: {
              videoId: "newvideo1234",
              videoPublishedAt: "2026-03-21T09:00:00Z",
            },
          },
        ],
      });
    }

    return jsonResponse({ error: { message: `Unexpected request: ${url}` } }, 404);
  };

  const context = await makeContext({
    config: {
      youtube_api_key: "test-key",
    },
    fetch: fetchStub,
  });

  const result = await handler(
    {
      action: "fetch_latest_uploads",
      source: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    context,
  );

  assert.equal(result.ok, true);
  assert.equal(result.target.resolved_from_video_id, "dQw4w9WgXcQ");
  assert.equal(result.latest_upload.video_id, "newvideo1234");
});

test("adds a follow and lists it from the persisted watchlist", async () => {
  const fetchStub = async (url) => {
    const parsed = new URL(url);
    const pathName = parsed.pathname;

    if (pathName.endsWith("/channels") && parsed.searchParams.get("forHandle") === "OpenAI") {
      return jsonResponse({
        items: [
          {
            id: "UC1234567890123456789012",
            snippet: {
              title: "OpenAI",
              description: "AI research and products.",
              customUrl: "@OpenAI",
              publishedAt: "2015-01-01T00:00:00Z",
              thumbnails: {},
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF1234567890123456789012",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/playlistItems") &&
      parsed.searchParams.get("playlistId") === "UULF1234567890123456789012"
    ) {
      return jsonResponse({
        items: [
          {
            id: "playlist-item-1",
            snippet: {
              title: "New Demo Walkthrough",
              description: "A short breakdown.",
              publishedAt: "2026-03-20T12:00:00Z",
              channelId: "UC1234567890123456789012",
              channelTitle: "OpenAI",
              position: 0,
              resourceId: {
                videoId: "abc123def45",
              },
              thumbnails: {},
            },
            contentDetails: {
              videoId: "abc123def45",
              videoPublishedAt: "2026-03-20T12:00:00Z",
            },
          },
        ],
      });
    }

    return jsonResponse({ error: { message: `Unexpected request: ${url}` } }, 404);
  };

  const context = await makeContext({
    config: {
      youtube_api_key: "test-key",
    },
    fetch: fetchStub,
  });

  const added = await handler(
    {
      action: "add_follow",
      source: "@OpenAI",
    },
    context,
  );

  assert.equal(added.ok, true);
  assert.equal(added.created, true);
  assert.equal(added.follow.channel_id, "UC1234567890123456789012");
  assert.equal(added.follow.last_seen_video_id, "abc123def45");

  const listed = await handler(
    {
      action: "list_follows",
    },
    context,
  );

  assert.equal(listed.ok, true);
  assert.equal(listed.count, 1);
  assert.equal(listed.follows[0].title, "OpenAI");
});

test("adds a follow without an API key by using the public fallback", async () => {
  const feedXml = `<?xml version="1.0" encoding="UTF-8"?>
  <feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns:media="http://search.yahoo.com/mrss/">
    <title>OpenAI</title>
    <author><name>OpenAI</name></author>
    <yt:channelId>UC1234567890123456789012</yt:channelId>
    <entry>
      <yt:videoId>abc123def45</yt:videoId>
      <yt:channelId>UC1234567890123456789012</yt:channelId>
      <title>New Demo Walkthrough</title>
      <link rel="alternate" href="https://www.youtube.com/watch?v=abc123def45"/>
      <author><name>OpenAI</name></author>
      <published>2026-03-20T12:00:00Z</published>
      <media:group>
        <media:description>A short breakdown.</media:description>
      </media:group>
    </entry>
  </feed>`;

  const fetchStub = async (url) => {
    if (url === "https://www.youtube.com/@OpenAI") {
      return textResponse(
        `<html><head>
          <meta property="og:title" content="OpenAI">
          <link rel="alternate" type="application/rss+xml" title="RSS" href="https://www.youtube.com/feeds/videos.xml?channel_id=UC1234567890123456789012">
          <link rel="canonical" href="https://www.youtube.com/@OpenAI">
        </head></html>`,
      );
    }

    if (url === "https://www.youtube.com/feeds/videos.xml?channel_id=UC1234567890123456789012") {
      return textResponse(feedXml);
    }

    return jsonResponse({ error: { message: `Unexpected request: ${url}` } }, 404);
  };

  const context = await makeContext({
    fetch: fetchStub,
  });

  const added = await handler(
    {
      action: "add_follow",
      source: "@OpenAI",
    },
    context,
  );

  assert.equal(added.ok, true);
  assert.equal(added.follow.channel_id, "UC1234567890123456789012");
  assert.equal(added.follow.last_seen_video_id, "abc123def45");
});

test("detects new uploads in the watchlist and marks them seen by default", async () => {
  let playlistCall = 0;
  const fetchStub = async (url) => {
    const parsed = new URL(url);
    const pathName = parsed.pathname;

    if (pathName.endsWith("/channels") && parsed.searchParams.get("forHandle") === "OpenAI") {
      return jsonResponse({
        items: [
          {
            id: "UC1234567890123456789012",
            snippet: {
              title: "OpenAI",
              description: "AI research and products.",
              customUrl: "@OpenAI",
              publishedAt: "2015-01-01T00:00:00Z",
              thumbnails: {},
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF1234567890123456789012",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/channels") &&
      parsed.searchParams.get("id") === "UC1234567890123456789012"
    ) {
      return jsonResponse({
        items: [
          {
            id: "UC1234567890123456789012",
            snippet: {
              title: "OpenAI",
              description: "AI research and products.",
              customUrl: "@OpenAI",
              publishedAt: "2015-01-01T00:00:00Z",
              thumbnails: {},
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF1234567890123456789012",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/playlistItems") &&
      parsed.searchParams.get("playlistId") === "UULF1234567890123456789012"
    ) {
      playlistCall += 1;
      const latestVideoId = playlistCall === 1 ? "seedvideo001" : "freshvideo02";
      const latestTitle = playlistCall === 1 ? "Seed Upload" : "Fresh Upload";

      return jsonResponse({
        items: [
          {
            id: `playlist-item-${playlistCall}`,
            snippet: {
              title: latestTitle,
              description: "New details.",
              publishedAt: "2026-03-20T12:00:00Z",
              channelId: "UC1234567890123456789012",
              channelTitle: "OpenAI",
              position: 0,
              resourceId: {
                videoId: latestVideoId,
              },
              thumbnails: {},
            },
            contentDetails: {
              videoId: latestVideoId,
              videoPublishedAt: "2026-03-20T12:00:00Z",
            },
          },
        ],
      });
    }

    return jsonResponse({ error: { message: `Unexpected request: ${url}` } }, 404);
  };

  const context = await makeContext({
    config: {
      youtube_api_key: "test-key",
    },
    fetch: fetchStub,
  });

  const added = await handler(
    {
      action: "add_follow",
      source: "@OpenAI",
    },
    context,
  );

  assert.equal(added.ok, true);
  assert.equal(added.follow.last_seen_video_id, "seedvideo001");

  const checked = await handler(
    {
      action: "check_watchlist_updates",
    },
    context,
  );

  assert.equal(checked.ok, true);
  assert.equal(checked.update_count, 1);
  assert.equal(checked.updates[0].latest_upload.video_id, "freshvideo02");

  const listed = await handler(
    {
      action: "list_follows",
    },
    context,
  );

  assert.equal(listed.follows[0].last_seen_video_id, "freshvideo02");
});

test("removes a follow from the persisted watchlist", async () => {
  const fetchStub = async (url) => {
    const parsed = new URL(url);
    const pathName = parsed.pathname;

    if (pathName.endsWith("/channels") && parsed.searchParams.get("forHandle") === "OpenAI") {
      return jsonResponse({
        items: [
          {
            id: "UC1234567890123456789012",
            snippet: {
              title: "OpenAI",
              description: "AI research and products.",
              customUrl: "@OpenAI",
              publishedAt: "2015-01-01T00:00:00Z",
              thumbnails: {},
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF1234567890123456789012",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/playlistItems") &&
      parsed.searchParams.get("playlistId") === "UULF1234567890123456789012"
    ) {
      return jsonResponse({
        items: [
          {
            id: "playlist-item-1",
            snippet: {
              title: "Seed Upload",
              description: "Initial item.",
              publishedAt: "2026-03-20T12:00:00Z",
              channelId: "UC1234567890123456789012",
              channelTitle: "OpenAI",
              position: 0,
              resourceId: {
                videoId: "seedvideo001",
              },
              thumbnails: {},
            },
            contentDetails: {
              videoId: "seedvideo001",
              videoPublishedAt: "2026-03-20T12:00:00Z",
            },
          },
        ],
      });
    }

    return jsonResponse({ error: { message: `Unexpected request: ${url}` } }, 404);
  };

  const context = await makeContext({
    config: {
      youtube_api_key: "test-key",
    },
    fetch: fetchStub,
  });

  await handler(
    {
      action: "add_follow",
      source: "@OpenAI",
    },
    context,
  );

  const removed = await handler(
    {
      action: "remove_follow",
      source: "@OpenAI",
    },
    context,
  );

  assert.equal(removed.ok, true);
  assert.equal(removed.count, 0);

  const listed = await handler(
    {
      action: "list_follows",
    },
    context,
  );

  assert.equal(listed.count, 0);
});

test("notifies new watchlist updates through a runtime delivery adapter", async () => {
  let playlistCall = 0;
  const delivered = [];
  const fetchStub = async (url) => {
    const parsed = new URL(url);
    const pathName = parsed.pathname;

    if (pathName.endsWith("/channels") && parsed.searchParams.get("forHandle") === "OpenAI") {
      return jsonResponse({
        items: [
          {
            id: "UC1234567890123456789012",
            snippet: {
              title: "OpenAI",
              description: "AI research and products.",
              customUrl: "@OpenAI",
              publishedAt: "2015-01-01T00:00:00Z",
              thumbnails: {},
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF1234567890123456789012",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/channels") &&
      parsed.searchParams.get("id") === "UC1234567890123456789012"
    ) {
      return jsonResponse({
        items: [
          {
            id: "UC1234567890123456789012",
            snippet: {
              title: "OpenAI",
              description: "AI research and products.",
              customUrl: "@OpenAI",
              publishedAt: "2015-01-01T00:00:00Z",
              thumbnails: {},
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF1234567890123456789012",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/playlistItems") &&
      parsed.searchParams.get("playlistId") === "UULF1234567890123456789012"
    ) {
      playlistCall += 1;
      const latestVideoId = playlistCall === 1 ? "seedvideo001" : "freshvideo02";
      const latestTitle = playlistCall === 1 ? "Seed Upload" : "Fresh Upload";

      return jsonResponse({
        items: [
          {
            id: `playlist-item-${playlistCall}`,
            snippet: {
              title: latestTitle,
              description: "New details.",
              publishedAt: "2026-03-20T12:00:00Z",
              channelId: "UC1234567890123456789012",
              channelTitle: "OpenAI",
              position: 0,
              resourceId: {
                videoId: latestVideoId,
              },
              thumbnails: {},
            },
            contentDetails: {
              videoId: latestVideoId,
              videoPublishedAt: "2026-03-20T12:00:00Z",
            },
          },
        ],
      });
    }

    return jsonResponse({ error: { message: `Unexpected request: ${url}` } }, 404);
  };

  const context = await makeContext({
    config: {
      youtube_api_key: "test-key",
      delivery_target: "telegram:test-room",
    },
    fetch: fetchStub,
  });
  context.deliver = async (notification) => {
    delivered.push(notification);
    return { accepted: true };
  };

  await handler(
    {
      action: "add_follow",
      source: "@OpenAI",
    },
    context,
  );

  const notified = await handler(
    {
      action: "notify_watchlist_updates",
    },
    context,
  );

  assert.equal(notified.ok, true);
  assert.equal(notified.delivered_count, 1);
  assert.equal(delivered.length, 1);
  assert.equal(delivered[0].delivery_target, "telegram:test-room");
  assert.match(delivered[0].markdown, /Fresh Upload/);

  const listed = await handler(
    {
      action: "list_follows",
    },
    context,
  );

  assert.equal(listed.follows[0].last_seen_video_id, "freshvideo02");
});

test("returns prepared notifications when no runtime delivery adapter exists", async () => {
  let playlistCall = 0;
  const fetchStub = async (url) => {
    const parsed = new URL(url);
    const pathName = parsed.pathname;

    if (pathName.endsWith("/channels") && parsed.searchParams.get("forHandle") === "OpenAI") {
      return jsonResponse({
        items: [
          {
            id: "UC1234567890123456789012",
            snippet: {
              title: "OpenAI",
              description: "AI research and products.",
              customUrl: "@OpenAI",
              publishedAt: "2015-01-01T00:00:00Z",
              thumbnails: {},
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF1234567890123456789012",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/channels") &&
      parsed.searchParams.get("id") === "UC1234567890123456789012"
    ) {
      return jsonResponse({
        items: [
          {
            id: "UC1234567890123456789012",
            snippet: {
              title: "OpenAI",
              description: "AI research and products.",
              customUrl: "@OpenAI",
              publishedAt: "2015-01-01T00:00:00Z",
              thumbnails: {},
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF1234567890123456789012",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/playlistItems") &&
      parsed.searchParams.get("playlistId") === "UULF1234567890123456789012"
    ) {
      playlistCall += 1;
      const latestVideoId = playlistCall === 1 ? "seedvideo001" : "freshvideo02";

      return jsonResponse({
        items: [
          {
            id: `playlist-item-${playlistCall}`,
            snippet: {
              title: playlistCall === 1 ? "Seed Upload" : "Fresh Upload",
              description: "New details.",
              publishedAt: "2026-03-20T12:00:00Z",
              channelId: "UC1234567890123456789012",
              channelTitle: "OpenAI",
              position: 0,
              resourceId: {
                videoId: latestVideoId,
              },
              thumbnails: {},
            },
            contentDetails: {
              videoId: latestVideoId,
              videoPublishedAt: "2026-03-20T12:00:00Z",
            },
          },
        ],
      });
    }

    return jsonResponse({ error: { message: `Unexpected request: ${url}` } }, 404);
  };

  const context = await makeContext({
    config: {
      youtube_api_key: "test-key",
    },
    fetch: fetchStub,
  });

  await handler(
    {
      action: "add_follow",
      source: "@OpenAI",
    },
    context,
  );

  const notified = await handler(
    {
      action: "notify_watchlist_updates",
    },
    context,
  );

  assert.equal(notified.ok, false);
  assert.equal(notified.delivered_count, 0);
  assert.equal(notified.notifications.length, 1);

  const listed = await handler(
    {
      action: "list_follows",
    },
    context,
  );

  assert.equal(listed.follows[0].last_seen_video_id, "seedvideo001");
});

// --- Transcript tests ---

test("extractCaptionTracks parses caption tracks from YouTube page HTML", () => {
  const html = `var ytInitialPlayerResponse = {"captions":{"playerCaptionsTracklistRenderer":{"captionTracks":[{"baseUrl":"https://example.com/timedtext?lang=zh-Hans","languageCode":"zh-Hans"},{"baseUrl":"https://example.com/timedtext?lang=en","languageCode":"en"}]}}};`;

  const tracks = extractCaptionTracks(html);
  assert.equal(tracks.length, 2);
  assert.equal(tracks[0].languageCode, "zh-Hans");
  assert.equal(tracks[1].languageCode, "en");
});

test("extractCaptionTracks returns empty array when no captions exist", () => {
  const html = `<html><body>No captions here</body></html>`;
  const tracks = extractCaptionTracks(html);
  assert.deepEqual(tracks, []);
});

test("pickBestTrack prefers Chinese over English", () => {
  const tracks = [
    { languageCode: "en", baseUrl: "https://example.com/en" },
    { languageCode: "zh-Hans", baseUrl: "https://example.com/zh" },
  ];
  const best = pickBestTrack(tracks);
  assert.equal(best.languageCode, "zh-Hans");
});

test("pickBestTrack falls back to English when no Chinese", () => {
  const tracks = [
    { languageCode: "fr", baseUrl: "https://example.com/fr" },
    { languageCode: "en", baseUrl: "https://example.com/en" },
  ];
  const best = pickBestTrack(tracks);
  assert.equal(best.languageCode, "en");
});

test("pickBestTrack falls back to first track when no zh or en", () => {
  const tracks = [
    { languageCode: "ja", baseUrl: "https://example.com/ja" },
    { languageCode: "ko", baseUrl: "https://example.com/ko" },
  ];
  const best = pickBestTrack(tracks);
  assert.equal(best.languageCode, "ja");
});

test("parseTranscriptXml extracts text from XML captions", () => {
  const xml = `<?xml version="1.0" encoding="utf-8"?>
<transcript>
  <text start="0" dur="5.2">Hello world</text>
  <text start="5.2" dur="3.1">This is a test &amp; demo</text>
  <text start="8.3" dur="4.0">Final segment</text>
</transcript>`;

  const text = parseTranscriptXml(xml);
  assert.equal(text, "Hello world This is a test & demo Final segment");
});

// --- Analyze video tests ---

test("analyzes a video URL with transcript (API-backed)", async () => {
  const captionXml = `<?xml version="1.0" encoding="utf-8"?>
<transcript>
  <text start="0" dur="5">Welcome to this podcast about AI agents</text>
  <text start="5" dur="5">Today we discuss the future of autonomous systems</text>
</transcript>`;

  const pageHtml = `<html><head>
    <script>var ytInitialPlayerResponse = {"captions":{"playerCaptionsTracklistRenderer":{"captionTracks":[{"baseUrl":"https://example.com/timedtext?lang=en","languageCode":"en"}]}}};</script>
  </head></html>`;

  const fetchStub = async (url) => {
    const parsed = typeof url === "string" ? new URL(url) : url;
    const urlStr = parsed.toString();
    const pathName = parsed.pathname;

    if (urlStr.startsWith("https://www.youtube.com/watch?v=testvid1234")) {
      return textResponse(pageHtml);
    }

    if (urlStr.startsWith("https://example.com/timedtext")) {
      return textResponse(captionXml);
    }

    if (pathName.endsWith("/videos") && parsed.searchParams.get("id") === "testvid1234") {
      return jsonResponse({
        items: [
          {
            id: "testvid1234",
            snippet: {
              channelId: "UC1234567890123456789012",
              channelTitle: "AI Podcast",
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/channels") &&
      parsed.searchParams.get("id") === "UC1234567890123456789012"
    ) {
      return jsonResponse({
        items: [
          {
            id: "UC1234567890123456789012",
            snippet: {
              title: "AI Podcast",
              description: "A podcast about AI.",
              publishedAt: "2024-01-01T00:00:00Z",
              thumbnails: {},
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF1234567890123456789012",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/playlistItems") &&
      parsed.searchParams.get("playlistId") === "UULF1234567890123456789012"
    ) {
      return jsonResponse({
        items: [
          {
            id: "playlist-item-1",
            snippet: {
              title: "AI Agents Deep Dive",
              description: "A comprehensive look at AI agents and their future.",
              publishedAt: "2026-03-20T12:00:00Z",
              channelId: "UC1234567890123456789012",
              channelTitle: "AI Podcast",
              position: 0,
              resourceId: { videoId: "testvid1234" },
              thumbnails: {},
            },
            contentDetails: {
              videoId: "testvid1234",
              videoPublishedAt: "2026-03-20T12:00:00Z",
            },
          },
        ],
      });
    }

    return jsonResponse({ error: { message: `Unexpected request: ${urlStr}` } }, 404);
  };

  const context = await makeContext({
    config: { youtube_api_key: "test-key" },
    fetch: fetchStub,
  });

  const result = await handler(
    {
      action: "analyze_video",
      source: "https://www.youtube.com/watch?v=testvid1234",
    },
    context,
  );

  assert.equal(result.ok, true);
  assert.equal(result.action, "analyze_video");
  assert.equal(result.video_id, "testvid1234");
  assert.equal(result.channel_name, "AI Podcast");
  assert.equal(result.has_transcript, true);
  assert.equal(result.transcript_language, "en");
  assert.match(result.transcript_text, /AI agents/);
  assert.match(result.message, /with transcript/);
});

test("analyzes a video URL without transcript available", async () => {
  const pageHtml = `<html><head><title>No captions video</title></head></html>`;

  const fetchStub = async (url) => {
    const parsed = typeof url === "string" ? new URL(url) : url;
    const urlStr = parsed.toString();
    const pathName = parsed.pathname;

    if (urlStr.startsWith("https://www.youtube.com/watch?v=nocaption12")) {
      return textResponse(pageHtml);
    }

    if (pathName.endsWith("/videos") && parsed.searchParams.get("id") === "nocaption12") {
      return jsonResponse({
        items: [
          {
            id: "nocaption12",
            snippet: {
              channelId: "UC9999999999999999999999",
              channelTitle: "No Caption Channel",
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/channels") &&
      parsed.searchParams.get("id") === "UC9999999999999999999999"
    ) {
      return jsonResponse({
        items: [
          {
            id: "UC9999999999999999999999",
            snippet: {
              title: "No Caption Channel",
              description: "",
              publishedAt: "2024-01-01T00:00:00Z",
              thumbnails: {},
            },
            contentDetails: {
              relatedPlaylists: {
                uploads: "UULF9999999999999999999999",
              },
            },
          },
        ],
      });
    }

    if (
      pathName.endsWith("/playlistItems") &&
      parsed.searchParams.get("playlistId") === "UULF9999999999999999999999"
    ) {
      return jsonResponse({
        items: [
          {
            id: "playlist-item-1",
            snippet: {
              title: "Video Without Captions",
              description: "This video has no subtitles.",
              publishedAt: "2026-03-20T12:00:00Z",
              channelId: "UC9999999999999999999999",
              channelTitle: "No Caption Channel",
              position: 0,
              resourceId: { videoId: "nocaption12" },
              thumbnails: {},
            },
            contentDetails: {
              videoId: "nocaption12",
              videoPublishedAt: "2026-03-20T12:00:00Z",
            },
          },
        ],
      });
    }

    return jsonResponse({ error: { message: `Unexpected request: ${urlStr}` } }, 404);
  };

  const context = await makeContext({
    config: { youtube_api_key: "test-key" },
    fetch: fetchStub,
  });

  const result = await handler(
    {
      action: "analyze_video",
      source: "https://www.youtube.com/watch?v=nocaption12",
    },
    context,
  );

  assert.equal(result.ok, true);
  assert.equal(result.video_id, "nocaption12");
  assert.equal(result.has_transcript, false);
  assert.equal(result.transcript_text, null);
  assert.match(result.message, /without transcript/);
});

test("analyze_video returns error for missing source", async () => {
  const result = await handler({
    action: "analyze_video",
  });

  assert.equal(result.ok, false);
  assert.match(result.message, /Missing required input/);
});
