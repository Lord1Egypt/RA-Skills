const fs = require("fs");
const path = require("path");
const os = require("os");
const utils = require("./utils");

function localDateStr() {
  const d = new Date();
  return (
    d.getFullYear() +
    "-" +
    String(d.getMonth() + 1).padStart(2, "0") +
    "-" +
    String(d.getDate()).padStart(2, "0")
  );
}

/**
 * @param {boolean} [saveFromCli]
 * @returns {boolean}
 */
function isLogEnabled(saveFromCli) {
  if (saveFromCli === true) return true;
  return process.env.GUAIKEI_ENABLE_LOG === "1";
}

/**
 * @param {string} filename
 * @param {string} content
 * @param {boolean} [saveFromCli]
 */
async function writeResultLog(filename, content, saveFromCli) {
  if (!isLogEnabled(saveFromCli)) return;
  if (!filename || typeof filename !== "string") {
    utils.printError("日志文件名必须是非空字符串");
    return;
  }
  if (!content || typeof content !== "string") {
    utils.printError("日志内容必须是非空字符串");
    return;
  }
  let safeFilename = `${process.pid}_${filename}`
    .replace(/[\\/:*?"<>|]/g, "_")
    .replace(/\.\.+/g, "_")
    .replace(/^\.+|\.+$/g, "");
  const ext = path.extname(safeFilename);
  const stem = ext ? safeFilename.slice(0, -ext.length) : safeFilename;
  if (safeFilename.length > 200) {
    safeFilename = stem.slice(0, Math.max(1, 200 - ext.length)) + ext;
  }
  if (!safeFilename) {
    safeFilename = `log_${Date.now()}`;
  }

  const outputDir = path.join(
    os.tmpdir(),
    "douyin-guaikei",
    "logs",
    localDateStr(),
  );
  const outputFilename = path.join(outputDir, safeFilename);

  try {
    await fs.promises.mkdir(outputDir, { recursive: true, mode: 0o700 });
    await fs.promises.writeFile(outputFilename, content, { mode: 0o600 });
    utils.printSuccess(`  → 已保存到 ${outputFilename}`);
  } catch (error) {
    utils.printError(`日志写入失败: ${error.message}`);
  }
}

function resourceId(url) {
  const s = String(url || "");
  const user = s.match(/\/user\/([^/?#]+)/i);
  if (user) return user[1];
  const media = s.match(/\/(?:video|note)\/([^/?#]+)/i);
  if (media) return media[1];
  const share = s.match(/\/share\/(?:video|note)\/([^/?#]+)/i);
  if (share) return share[1];
  const short = s.match(/v\.douyin\.com\/([^/?#]+)/i);
  if (short) return short[1];
  const plain = s.replace(/[^a-zA-Z0-9_-]/g, "");
  return plain.slice(0, 80) || "unknown";
}
module.exports = {
  isLogEnabled,
  writeResultLog,
  resourceId,
};
