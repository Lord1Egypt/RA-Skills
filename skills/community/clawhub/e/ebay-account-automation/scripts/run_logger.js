/**
 * 运行日志
 */

const fs = require('fs');
const path = require('path');

const LOG_DIR = path.join(__dirname, 'logs');
const MAX_LINES = 500;

function ensureLogDir() {
  if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
}

function todayStr() {
  const d = new Date();
  return `${d.getFullYear()}${String(d.getMonth()+1).padStart(2,'0')}${String(d.getDate()).padStart(2,'0')}`;
}

function nowStr() {
  const d = new Date();
  return `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}:${String(d.getSeconds()).padStart(2,'0')}`;
}

function log(level, msg) {
  ensureLogDir();
  const logFile = path.join(LOG_DIR, `run_${todayStr()}.log`);
  const line = `[${nowStr()}] [${level}] ${msg}`;
  try {
    fs.appendFileSync(logFile, line + '\n', 'utf-8');
    const content = fs.readFileSync(logFile, 'utf-8');
    const lines = content.split('\n').filter(l => l.trim());
    if (lines.length > MAX_LINES) {
      fs.writeFileSync(logFile, lines.slice(-Math.floor(MAX_LINES * 0.7)).join('\n') + '\n', 'utf-8');
    }
  } catch(e) {
    console.warn('日志写入失败:', e.message);
  }
  console.log(line);
}

function logRunStart(accountName, accountNum, totalAccounts) {
  log('INFO', `========== 开始账号 ${accountNum}/${totalAccounts} [${accountName}] ==========`);
}

function logRunEnd(accountName, result) {
  const { searchesDone, totalFavorited, totalAddedToCart, durationSec } = result;
  log('INFO', `账号 [${accountName}] 完成: ${searchesDone}轮搜索, 收藏${totalFavorited}个, 加购${totalAddedToCart}个, 耗时${durationSec}秒`);
}

function logError(accountName, errMsg) {
  log('ERROR', `账号 [${accountName}] 出错: ${errMsg}`);
}

module.exports = { logRunStart, logRunEnd, logError, log };
