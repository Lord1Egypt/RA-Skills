/**
 * 分享文案抽链：匹配在停止符处截断，再剥尾部装饰符。
 * 停止符须覆盖中文引号/书名号等（不在 \u4e00-\u9fff 内），避免尾部脏字符进后端。
 */
const URL_STOP_CLASS =
  '\\s"\'<>`' +
  '\\u4e00-\\u9fff' +
  '，。！？、；：（）【】' +
  '「」『』“”‘’《》〈〉' +
  '［］〔〕〖〗…—～·';

const DOUYIN_URL_RE = new RegExp(
  `(?:https?:\\/\\/)?(?:www\\.|v\\.)?(?:douyin\\.com|iesdouyin\\.com)\\/[^${URL_STOP_CLASS}]+`,
  'i',
);

const URL_TRAIL_STRIP_RE = new RegExp(
  `[\\/.,;:!?\"'，。！？；：、）】》「」『』“”‘’《》〈〉［］〔〕〖〗…—～·]+$`,
  'g',
);

function extractDouyinUrl(raw) {
  if (typeof raw !== "string") return null;
  const m = raw.match(DOUYIN_URL_RE);
  if (!m) return null;

  let url = m[0];
  url = url.split("?")[0].split("#")[0];
  url = url.replace(URL_TRAIL_STRIP_RE, "");
  return url || null;
}

module.exports = {
  extractDouyinUrl,
};
