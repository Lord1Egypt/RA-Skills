/**
 * 后端数字 errcode → Skill 稳定 error_code（封闭枚举，不把裸数字透出给信封）。
 * 顺序：包月文案 → 余额（15 / 文案；详情 14=余额靠文案先命中）→ 裸 14 作 PLAN_LIMIT → 频控 → 日限
 * → 鉴权态（410 停用 / 405 未开通 / 77 过期）→ 未知码兜底 API_ERROR。
 * 同码异义：搜索/用户搜索/作品/评论的 14 为包月条数；详情的 14 为余额（须带余额文案）。
 * 注意：业务 errcode 410 = TOKEN 状态异常，不是「接口下线 / 任务过期」。
 */
const { ApiError, AuthError } = require("./errors");

const PLAN_LIMIT_RE = /包月TOKEN|搜索量受限|作品量受限|评论量受限|最多支持\d+条/;
const BALANCE_RE = /余额可能不足|TOKEN余额|请通过www\.guaikei\.com充值/;
const RATE_RE = /短时间内请勿提交过多/;
const DAY_LIMIT_RE = /今日消费已达每日上限|每日消费限额|每日上限/;
const TOKEN_DISABLED_RE = /^Gone$/i;
const TOKEN_EXPIRED_RE = /TOKEN已过期|请通过www\.guaikei\.com延期/;
const FEATURE_CLOSED_RE = /^Method Not Allowed$/i;

const PLAN_LIMIT_FALLBACK =
  "当前 TOKEN 套餐单次条数超限（包月：视频搜索/用户搜索/作品最多 30，评论最多 50）。请降低 --limit，或到 www.guaikei.com 升级按量套餐";

const TOKEN_DISABLED_MSG =
  "GUAIKEI_API_TOKEN 已停用或状态异常，请到 www.guaikei.com 检查 TOKEN 或联系客服（不是搜索接口下线）";
const FEATURE_CLOSED_MSG =
  "当前 TOKEN 未开通该接口权限，请到 www.guaikei.com 开通对应能力后重试";
const TOKEN_EXPIRED_MSG =
  "TOKEN 已过期，请通过 www.guaikei.com 延期后重试";

/**
 * @param {number} errcode
 * @param {string} [errmsg]
 * @returns {ApiError|AuthError}
 */
function mapBackendApiError(errcode, errmsg) {
  const msg = (errmsg && String(errmsg).trim()) || "";

  if (PLAN_LIMIT_RE.test(msg)) {
    return new ApiError("PLAN_LIMIT", msg || PLAN_LIMIT_FALLBACK, true);
  }

  if (errcode === 15 || BALANCE_RE.test(msg)) {
    return new ApiError(
      "INSUFFICIENT_BALANCE",
      msg ||
        "TOKEN 余额可能不足，请通过 www.guaikei.com 充值后重试",
      true,
    );
  }

  // 包月条数官方码；详情余额须已由上方 BALANCE_RE 吃掉
  if (errcode === 14) {
    return new ApiError("PLAN_LIMIT", msg || PLAN_LIMIT_FALLBACK, true);
  }

  if (errcode === 2 || RATE_RE.test(msg)) {
    return new ApiError(
      "RATE_LIMITED",
      msg || "短时间内请勿提交过多任务，请稍后重试",
      true,
    );
  }

  if (errcode === 18 || DAY_LIMIT_RE.test(msg)) {
    return new ApiError(
      "DAILY_LIMIT",
      msg ||
        "今日消费已达每日上限，请明日再试，或登录 www.guaikei.com 调整每日消费限额",
      true,
    );
  }

  // 与 request.js 对齐；若走到此处仍按鉴权处理
  if (errcode === 401 || errcode === 403) {
    const e = new AuthError(
      "GUAIKEI_API_TOKEN 无效, 请检查环境变量 或 通过 www.guaikei.com 联系客服获取解决方案",
    );
    e.noRetry = true;
    return e;
  }

  // TOKEN status != 1（业务码 410 + Gone）；禁止当成接口退役或任务过期
  if (errcode === 410 || TOKEN_DISABLED_RE.test(msg)) {
    const e = new AuthError(TOKEN_DISABLED_MSG);
    e.noRetry = true;
    return e;
  }

  // 包月/能力未对 TOKEN 开通该 path（业务码 405）
  if (errcode === 405 || FEATURE_CLOSED_RE.test(msg)) {
    const e = new AuthError(FEATURE_CLOSED_MSG);
    e.noRetry = true;
    return e;
  }

  // 77：过期文案；余额文案已在上方 BALANCE_RE 处理
  if (errcode === 77 || TOKEN_EXPIRED_RE.test(msg)) {
    const e = new AuthError(msg || TOKEN_EXPIRED_MSG);
    e.noRetry = true;
    return e;
  }

  const detail = msg
    ? `${msg}（上游 errcode=${errcode}）`
    : `上游返回未映射业务码 errcode=${errcode}`;
  return new ApiError("API_ERROR", detail, errcode >= 10);
}

module.exports = {
  mapBackendApiError,
  PLAN_LIMIT_RE,
  BALANCE_RE,
  RATE_RE,
  DAY_LIMIT_RE,
};
