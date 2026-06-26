function getFetchImpl(context = {}) {
  if (typeof context.fetch === "function") {
    return context.fetch;
  }

  if (typeof fetch === "function") {
    return fetch.bind(globalThis);
  }

  throw new Error("No fetch implementation is available in the current runtime.");
}

function extractCaptionTracks(html) {
  const match = String(html || "").match(/"captionTracks"\s*:\s*(\[[\s\S]*?\])/);
  if (!match) {
    return [];
  }

  try {
    return JSON.parse(match[1]);
  } catch {
    return [];
  }
}

function pickBestTrack(tracks) {
  if (!Array.isArray(tracks) || tracks.length === 0) {
    return null;
  }

  const zhTrack = tracks.find(
    (t) => t.languageCode && /^zh/i.test(t.languageCode),
  );
  if (zhTrack) {
    return zhTrack;
  }

  const enTrack = tracks.find(
    (t) => t.languageCode && /^en/i.test(t.languageCode),
  );
  if (enTrack) {
    return enTrack;
  }

  return tracks[0];
}

function parseTranscriptXml(xml) {
  const texts = [];
  const regex = /<text\b[^>]*>([\s\S]*?)<\/text>/gi;
  let match;

  while ((match = regex.exec(xml)) !== null) {
    const decoded = match[1]
      .replace(/&amp;/g, "&")
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&#x27;/g, "'")
      .replace(/\n/g, " ")
      .trim();

    if (decoded) {
      texts.push(decoded);
    }
  }

  return texts.join(" ");
}

async function fetchTranscript(videoUrl, context = {}) {
  const fetchImpl = getFetchImpl(context);

  const videoIdMatch = String(videoUrl || "").match(
    /(?:v=|youtu\.be\/)([A-Za-z0-9_-]{11})/,
  );
  if (!videoIdMatch) {
    return { ok: false, reason: "invalid_video_url" };
  }

  const watchUrl = `https://www.youtube.com/watch?v=${videoIdMatch[1]}`;

  let html;
  try {
    const response = await fetchImpl(watchUrl, {
      headers: {
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        accept: "text/html",
      },
    });
    html = await response.text();
  } catch {
    return { ok: false, reason: "fetch_page_failed" };
  }

  const tracks = extractCaptionTracks(html);
  if (tracks.length === 0) {
    return { ok: false, reason: "no_captions_available" };
  }

  const track = pickBestTrack(tracks);
  if (!track || !track.baseUrl) {
    return { ok: false, reason: "no_suitable_caption_track" };
  }

  let xml;
  try {
    const response = await fetchImpl(track.baseUrl, {
      headers: { accept: "application/xml, text/xml" },
    });
    xml = await response.text();
  } catch {
    return { ok: false, reason: "fetch_captions_failed" };
  }

  const text = parseTranscriptXml(xml);
  if (!text) {
    return { ok: false, reason: "empty_captions" };
  }

  return {
    ok: true,
    text,
    language: track.languageCode || null,
    source: "caption_track",
  };
}

module.exports = {
  fetchTranscript,
  extractCaptionTracks,
  pickBestTrack,
  parseTranscriptXml,
};
