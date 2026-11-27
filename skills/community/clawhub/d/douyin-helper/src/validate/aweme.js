const { extractDouyinUrl } = require("./url");

function parseDouyinAweme(url) {
  const extracted = extractDouyinUrl(url);
  if (extracted) {
    if (
      /\/(video|note)\//i.test(extracted) ||
      /v\.douyin\.com\//i.test(extracted)
    ) {
      return extracted;
    }
    return null;
  }

  const s = String(url ?? "")
    .trim()
    .replace(/[^0-9a-zA-Z_-]/g, "");
  if (!s || !/^\d+$/.test(s)) {
    return null;
  }
  return s;
}

module.exports = {
  parseDouyinAweme,
};
