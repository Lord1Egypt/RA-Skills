function cleanLine(line) {
  return String(line || "")
    .replace(/\s+/g, " ")
    .trim();
}

function collectBulletCandidates(description) {
  const rawLines = String(description || "")
    .split("\n")
    .map(cleanLine)
    .filter(Boolean);

  const filteredLines = rawLines.filter((line) => {
    if (/^https?:\/\//i.test(line)) {
      return false;
    }
    if (/^(#|@)/.test(line)) {
      return false;
    }
    return true;
  });

  if (filteredLines.length > 0) {
    return filteredLines;
  }

  return String(description || "")
    .split(/[.!?]\s+/)
    .map(cleanLine)
    .filter(Boolean);
}

function truncate(text, maxLength) {
  if (!text || text.length <= maxLength) {
    return text;
  }
  return `${text.slice(0, maxLength - 1).trim()}…`;
}

function summarizeVideoMetadata(input) {
  const channelName = cleanLine(input.channel_name || input.channelName || "Creator");
  const title = cleanLine(input.video_title || input.videoTitle || "Untitled video");
  const description = String(input.video_description || input.videoDescription || "");
  const videoUrl = cleanLine(input.video_url || input.videoUrl || "");
  const publishedAt = cleanLine(input.published_at || input.publishedAt || "");

  const bulletCandidates = collectBulletCandidates(description)
    .slice(0, 3)
    .map((line) => truncate(line, 140));

  const summarySource = bulletCandidates[0] || title;
  const summary = truncate(`${channelName} published "${title}". ${summarySource}`, 220);
  const headline = `${channelName}: ${title}`;

  const markdownLines = [
    `**${headline}**`,
    publishedAt ? `Published: ${publishedAt}` : null,
    "",
    summary,
    "",
    ...bulletCandidates.map((line) => `- ${line}`),
    videoUrl ? "" : null,
    videoUrl ? `Watch: ${videoUrl}` : null,
  ].filter(Boolean);

  return {
    headline,
    summary,
    bullets: bulletCandidates,
    markdown: markdownLines.join("\n"),
  };
}

module.exports = {
  summarizeVideoMetadata,
};
