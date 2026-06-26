const { normalizeYouTubeInput } = require("./youtube");
const { fetchLatestUploads, resolveYouTubeTarget } = require("./youtube-api");
const { fetchTranscript } = require("./transcript");

async function analyzeVideo(source, context = {}) {
  const normalized = normalizeYouTubeInput(source);

  if (!normalized.ok) {
    throw new Error(normalized.message || "Unable to normalize YouTube input.");
  }

  let videoId = null;
  let videoTitle = null;
  let videoDescription = null;
  let videoUrl = null;
  let publishedAt = null;
  let channelName = null;
  let channelId = null;

  if (normalized.kind === "video") {
    videoId = normalized.video_id;
    videoUrl = normalized.canonical_url;

    const resolved = await resolveYouTubeTarget(source, context);
    channelId = resolved.target.channel_id;
    channelName = resolved.target.title;

    const uploads = await fetchLatestUploads(resolved.target.channel_id, { limit: 10 }, context);
    const match = uploads.uploads.find((u) => u.video_id === videoId);

    if (match) {
      videoTitle = match.title;
      videoDescription = match.description;
      publishedAt = match.published_at;
      channelName = channelName || match.channel_title;
    }
  } else {
    const resolved = await resolveYouTubeTarget(source, context);
    channelId = resolved.target.channel_id;
    channelName = resolved.target.title;

    const uploads = await fetchLatestUploads(source, { limit: 1 }, context);
    const latest = uploads.latest_upload;

    if (latest) {
      videoId = latest.video_id;
      videoTitle = latest.title;
      videoDescription = latest.description;
      videoUrl = latest.video_url;
      publishedAt = latest.published_at;
      channelName = channelName || latest.channel_title;
    }
  }

  if (!videoId) {
    throw new Error("Could not find a video to analyze for this input.");
  }

  const transcriptUrl = videoUrl || `https://www.youtube.com/watch?v=${videoId}`;
  const transcript = await fetchTranscript(transcriptUrl, context);

  return {
    video_id: videoId,
    video_url: videoUrl || `https://www.youtube.com/watch?v=${videoId}`,
    title: videoTitle || "Untitled video",
    description: videoDescription || "",
    published_at: publishedAt || null,
    channel_id: channelId,
    channel_name: channelName || "Unknown",
    has_transcript: transcript.ok,
    transcript_language: transcript.ok ? transcript.language : null,
    transcript_text: transcript.ok ? transcript.text : null,
  };
}

module.exports = {
  analyzeVideo,
};
