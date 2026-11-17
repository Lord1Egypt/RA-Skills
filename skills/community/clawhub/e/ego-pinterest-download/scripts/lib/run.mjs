import {
  BASE,
  acceptMedia,
  assertPinimg,
  attachLoginCopy,
  EXT,
  foldDomUrls,
  interpretSession,
  isVideoUrl,
  loginRequiredSummary,
  meetsMinResolution,
  normalizePin,
  outputName,
  parseBoard,
  parseResourceResponse,
  pinIdFromInput,
  pinRequest,
  previewCandidates,
  previewPayload,
  relatedRequest,
  resourcePath,
  searchRequest,
  sizeCandidates,
  sniffImage,
  sniffVideo,
  videoTryUrls,
  boardFeedRequest,
  boardRequest,
} from "./pure.mjs";

async function publish(summary, fs, path) {
  if (!summary.outDir) return;
  await fs.mkdir(summary.outDir, { recursive: true });
  const manifest = path.join(summary.outDir, "manifest.json");
  summary.manifest = manifest;
  await fs.writeFile(manifest, JSON.stringify(summary, null, 2));
}

function rejectResolution(pin, config, skipped) {
  if (!config || config.command === "download" || config.command === "preview") return false;
  const minWidth = Number(config.minWidth) || 0;
  const minHeight = Number(config.minHeight) || 0;
  if (minWidth <= 0 && minHeight <= 0) return false;
  const kind = config.media === "video" ? "video" : "image";
  const gate = meetsMinResolution(pin, minWidth, minHeight, kind);
  if (gate.ok) return false;
  skipped?.push({
    url: pin.pin_url || pin.video_url || pin.image_url,
    image_url: pin.image_url,
    pin_id: pin.id,
    width: gate.width,
    height: gate.height,
    reason: gate.reason,
  });
  return true;
}

async function loadPins(session, build, { limit, media, bookmark, maxPages, now, minWidth, minHeight, command, skipped }) {
  const pins = [];
  const seen = new Set();
  let next = bookmark || undefined;
  for (let pageNo = 0; pageNo < maxPages && pins.length < limit; pageNo++) {
    const request = build(next);
    const response = await session.fetchJson(resourcePath(request, now()), {
      "X-Pinterest-PWS-Handler": request.handler,
    });
    const parsed = parseResourceResponse(response);
    if (parsed.error) throw new Error(parsed.error);
    for (const raw of parsed.items) {
      if (pins.length >= limit) break;
      const pin = normalizePin(raw);
      if (!pin?.image_url || seen.has(pin.image_url)) continue;
      seen.add(pin.image_url);
      if (!acceptMedia(pin, media)) continue;
      if (rejectResolution(pin, { command, media, minWidth, minHeight }, skipped)) continue;
      pins.push(pin);
    }
    if (!parsed.bookmark || parsed.items.length === 0) break;
    next = parsed.bookmark;
  }
  return pins;
}

async function firstGood(session, urls, accept, maxBytes) {
  let last = "no candidate";
  for (const url of urls) {
    let got;
    try {
      got = await session.fetchBytes(url, { maxBytes });
    } catch (error) {
      last = String(error.message || error);
      continue;
    }
    if (accept(got, maxBytes)) return { ...got, url };
    if (got?.error) last = got.error;
    else if (got?.buf && maxBytes && got.buf.length > maxBytes) last = `larger than ${maxBytes} bytes`;
    else last = `HTTP ${got?.status || "error"}`;
  }
  throw new Error(last);
}

function acceptImage(got) {
  return Boolean(got?.ok && sniffImage(got.buf));
}

function acceptVideo(got, maxBytes) {
  if (!got?.ok || !got.buf || got.buf.length < 100 || got.buf.length > maxBytes) return false;
  return String(got.type || "").startsWith("video/") || sniffVideo(got.buf);
}

async function saveImage(session, fs, path, imageUrl, destDir, index, size) {
  assertPinimg(imageUrl);
  const got = await firstGood(session, sizeCandidates(imageUrl, size), acceptImage, 20_000_000);
  const type = sniffImage(got.buf);
  const file = path.join(destDir, outputName(index, got.url, EXT[type] || "jpg"));
  await fs.writeFile(file, got.buf);
  return {
    n: String(index + 1).padStart(2, "0"),
    path: file,
    url: got.url,
    bytes: got.buf.length,
    contentType: type,
    kind: "image",
  };
}

async function saveVideo(session, fs, path, videoUrl, destDir, index, maxVideoBytes) {
  assertPinimg(videoUrl);
  const tries = videoTryUrls(videoUrl);
  if (!tries.length) throw new Error("HLS stream has no MP4 rendition");
  const got = await firstGood(session, tries, (item) => acceptVideo(item, maxVideoBytes), maxVideoBytes);
  const file = path.join(destDir, outputName(index, got.url, "mp4"));
  await fs.writeFile(file, got.buf);
  return {
    n: String(index + 1).padStart(2, "0"),
    path: file,
    url: got.url,
    bytes: got.buf.length,
    contentType: got.type || "video/mp4",
    kind: "video",
  };
}

async function savePinMedia(session, fs, path, pin, destDir, index, config) {
  const videoUrl = pin.video_url || (isVideoUrl(pin.image_url) ? pin.image_url : "");
  const wantVideo = config.media === "video" || (config.command === "download" && Boolean(videoUrl));
  if (wantVideo) {
    if (!videoUrl) throw new Error("pin has no video_url");
    return saveVideo(session, fs, path, videoUrl, destDir, index, config.maxVideoBytes);
  }
  return saveImage(session, fs, path, pin.image_url, destDir, index, config.size);
}

async function addPreviews(session, summary, urls, config) {
  const wanted = Math.min(config.previews || 0, urls.length);
  summary.previews = [];
  for (let index = 0; index < wanted; index++) {
    try {
      assertPinimg(urls[index]);
      const got = await firstGood(session, previewCandidates(urls[index]), acceptImage, config.maxVideoBytes);
      const preview = previewPayload(got.buf);
      summary.previews.push({ url: got.url, source: urls[index], ...preview });
    } catch (error) {
      summary.failures.push({ stage: "preview", url: urls[index], error: String(error.message || error) });
    }
  }
}

function startUrlFor(config, id, board) {
  if (config.command === "search") return `${BASE}/search/pins/?q=${encodeURIComponent(config.query)}&rs=typed`;
  if ((config.command === "related" || config.command === "pin") && id) return `${BASE}/pin/${id}/`;
  if (config.command === "board" && board) return `${BASE}${board.path}`;
  return `${BASE}/`;
}

async function resolvePin(config, session) {
  const parsed = pinIdFromInput(config.pin);
  if (parsed.error) {
    const error = new Error(parsed.error);
    error.usage = true;
    throw error;
  }
  if (parsed.id) return parsed.id;
  await session.goto(parsed.redirect);
  const finalUrl = await session.url();
  const again = pinIdFromInput(finalUrl);
  if (!again.id) throw new Error(again.error || "Could not resolve pin.it link");
  return again.id;
}

export async function execute(config, deps) {
  const fs = deps.fs;
  const path = deps.path;
  const now = deps.now || (() => Date.now());
  const summary = attachLoginCopy({
    skill: "pinterest-download",
    command: config.command,
    ok: false,
    login_required: false,
    logged_in: false,
    anonymous: false,
    query: config.query || null,
    pin: config.pin || null,
    board: config.board || null,
    limit: config.limit,
    outDir: config.outDir,
    size: config.size,
    media: config.media,
    min_width: config.minWidth || 0,
    min_height: config.minHeight || 0,
    method: null,
    spaceId: null,
    pins: [],
    downloads: [],
    previews: [],
    skipped: [],
    failures: [],
    error: null,
    exitCode: 1,
  });
  let session = null;
  let dirReady = false;
  const ensureDir = async () => {
    if (dirReady || !config.outDir) return;
    await fs.mkdir(config.outDir, { recursive: true });
    dirReady = true;
  };
  try {
    let pinId = null;
    let board = null;
    if (config.command === "related" || config.command === "pin") {
      const early = pinIdFromInput(config.pin);
      if (early.error) throw Object.assign(new Error(early.error), { usage: true });
      pinId = early.id || null;
    }
    if (config.command === "board") {
      try {
        board = parseBoard(config.board);
      } catch (error) {
        error.usage = true;
        throw error;
      }
    }

    session = await deps.browser.open({
      taskName: config.taskName,
      startUrl: startUrlFor(config, pinId, board),
      keepBrowser: config.keepBrowser,
    });
    summary.spaceId = session.spaceId;
    if ((config.command === "related" || config.command === "pin") && !pinId) {
      pinId = await resolvePin(config, session);
    }
    const rawSession = await session.detect();
    const who = interpretSession(rawSession);
    summary.logged_in = who.loggedIn;
    summary.anonymous = !who.loggedIn;
    summary.signals = {
      unauth: who.unauth,
      profile: who.profile,
      auth_cookie: who.authCookie,
      login_url: who.loginUrl,
    };
    summary.page = { url: who.url, title: who.title };
    if (!who.loggedIn && !config.allowAnonymous) {
      loginRequiredSummary(summary);
      return summary;
    }
    await ensureDir();

    if (config.command === "search") {
      let pins = [];
      try {
        pins = await loadPins(session, (bookmark) => searchRequest(config.query, bookmark), {
          limit: config.limit,
          media: config.media,
          bookmark: config.bookmark,
          maxPages: config.maxPages,
          now,
          minWidth: config.minWidth,
          minHeight: config.minHeight,
          command: config.command,
          skipped: summary.skipped,
        });
        summary.method = "BaseSearchResource";
      } catch (error) {
        summary.failures.push({ stage: "BaseSearchResource", error: String(error.message || error) });
        pins = [];
        summary.method = null;
      }
      if (pins.length < config.limit) {
        const domPins = foldDomUrls(await session.domImages(config.limit), config.limit);
        const seen = new Set(pins.map((pin) => pin.image_url));
        for (const row of summary.skipped) if (row.image_url) seen.add(row.image_url);
        for (const pin of domPins) {
          if (pins.length >= config.limit) break;
          if (seen.has(pin.image_url)) continue;
          if (rejectResolution(pin, config, summary.skipped)) continue;
          seen.add(pin.image_url);
          pins.push(pin);
        }
        if (domPins.length) summary.method = summary.method ? `${summary.method}+dom` : "dom";
      }
      summary.pins = pins;
    } else if (config.command === "related") {
      summary.pins = await loadPins(session, (bookmark) => relatedRequest(pinId, bookmark), {
        limit: config.limit,
        media: config.media,
        bookmark: config.bookmark,
        maxPages: config.maxPages,
        now,
        minWidth: config.minWidth,
        minHeight: config.minHeight,
        command: config.command,
        skipped: summary.skipped,
      });
      summary.method = "RelatedModulesResource";
      summary.pin_id = pinId;
    } else if (config.command === "board") {
      const header = parseResourceResponse(
        await session.fetchJson(resourcePath(boardRequest(board.username, board.slug), now()), {
          "X-Pinterest-PWS-Handler": "www/[username]/[slug].js",
        }),
      );
      if (header.error) throw new Error(header.error);
      const data = header.data || {};
      if (!data.id) throw new Error("Board not found");
      summary.board_info = {
        id: String(data.id),
        name: data.name,
        url: `${BASE}${board.path}`,
        pin_count: data.pin_count,
        owner: data.owner?.username,
      };
      summary.pins = await loadPins(
        session,
        (bookmark) => boardFeedRequest(data.id, board.path, bookmark),
        {
          limit: config.limit,
          media: config.media,
          bookmark: config.bookmark,
          maxPages: config.maxPages,
          now,
          minWidth: config.minWidth,
          minHeight: config.minHeight,
          command: config.command,
          skipped: summary.skipped,
        },
      );
      summary.method = "BoardFeedResource";
    } else if (config.command === "pin") {
      const parsed = parseResourceResponse(
        await session.fetchJson(resourcePath(pinRequest(pinId), now()), {
          "X-Pinterest-PWS-Handler": "www/pin/[id].js",
        }),
      );
      if (parsed.error) throw new Error(parsed.error);
      const pin = normalizePin({ ...(parsed.data || {}), type: "pin", is_promoted: false });
      if (!pin) throw new Error("Pin has no image");
      summary.pins = [pin];
      summary.pin_id = pinId;
      summary.method = "PinResource";
    } else if (config.command === "download") {
      summary.method = "direct";
      summary.pins = config.urls.map((url) => (isVideoUrl(url) ? { video_url: url, image_url: url } : { image_url: url }));
    } else if (config.command === "preview") {
      summary.method = "preview";
      await addPreviews(session, summary, config.urls, { ...config, previews: config.urls.length });
    }

    if (config.command !== "preview") {
      const pins = config.command === "download" ? summary.pins : summary.pins.slice(0, config.limit);
      for (let index = 0; index < pins.length; index++) {
        const pin = pins[index];
        try {
          if (rejectResolution(pin, config, summary.skipped)) continue;
          const saved = await savePinMedia(session, fs, path, pin, config.outDir, index, config);
          saved.pin_id = pin.id;
          summary.downloads.push(saved);
        } catch (error) {
          summary.failures.push({ url: pin.video_url || pin.image_url, error: String(error.message || error) });
        }
      }
      if (config.previews > 0) {
        const sources = pins.map((pin) => pin.image_url).filter(Boolean);
        await addPreviews(session, summary, sources, config);
      }
    }

    summary.count = summary.downloads.length;
    const previewOk = config.command === "preview" && summary.previews.length > 0;
    const blockedByResolution = summary.skipped.length > 0 && summary.downloads.length === 0;
    const pinOk = config.command === "pin" && summary.pins.length > 0 && !blockedByResolution;
    summary.ok = summary.downloads.length > 0 || previewOk || pinOk;
    summary.exitCode = summary.ok ? 0 : 1;
    if (!summary.ok) {
      summary.error =
        summary.error ||
        (blockedByResolution
          ? "No media met the minimum resolution."
          : config.media === "video"
            ? "No videos were saved."
            : "No images were saved.");
    }
    return summary;
  } catch (error) {
    summary.ok = false;
    summary.error = String(error.message || error);
    summary.exitCode = error.usage ? 2 : 1;
    return summary;
  } finally {
    try {
      await publish(summary, fs, path);
    } catch {
      // stdout JSON remains the result when the directory cannot be written
    }
    if (session) {
      try {
        await session.finish();
      } catch (error) {
        summary.failures.push({ stage: "finish", error: String(error.message || error) });
      }
    }
  }
}
