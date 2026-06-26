/**
 * EVA Soul - 结构化日志模块
 * 统一日志级别、上下文、时间戳，支持控制台+文件双输出
 */

const fs = require('fs');
const path = require('path');
const i18n = require('../i18n');

// 日志级别
const LEVELS = {
  DEBUG: 0,
  INFO:  1,
  WARN:  2,
  ERROR: 3
};

const LEVEL_NAMES = ['DEBUG', 'INFO', 'WARN', 'ERROR'];

// 颜色码（控制台彩色输出）
const COLORS = {
  RESET:   '\x1b[0m',
  GRAY:    '\x1b[90m',
  BLUE:    '\x1b[34m',
  GREEN:   '\x1b[32m',
  YELLOW:  '\x1b[33m',
  RED:     '\x1b[31m',
  MAGENTA: '\x1b[35m'
};

const LEVEL_COLORS = {
  DEBUG: COLORS.GRAY,
  INFO:  COLORS.BLUE,
  WARN:  COLORS.YELLOW,
  ERROR: COLORS.RED,
  SUCC:  COLORS.GREEN,   // 自定义成功级别
  HDR:   COLORS.MAGENTA  // 自定义标题级别
};

/**
 * Logger 配置
 */
let _config = {
  level: LEVELS.INFO,         // 最低输出级别
  enableConsole: true,        // 控制台输出
  enableFile: false,          // 文件输出（默认关闭）
  logDir: null,               // 日志目录（需手动开启）
  maxFileSize: 5 * 1024 * 1024, // 单文件最大 5MB
  maxFiles: 3,                // 保留文件数
  showTimestamp: true,        // 显示时间戳
  showContext: true,          // 显示上下文标签
  emoji: true                 // 显示 emoji
};

/**
 * 配置 Logger
 * @param {object} options
 */
/**
 * 设置当前语言
 * @param {string} locale - 语言代码：zh / en / ja / zh-TW
 */
function setLocale(locale) {
  _config.locale = locale;
}

/**
 * 获取当前语言
 */
function getLocale() {
  return _config.locale || 'zh';
}

/**
 * 配置 Logger
 */
function configure(options = {}) {
  _config = { ..._config, ...options };
  if (options.locale) _config.locale = options.locale;
}

/**
 * 格式化时间戳
 */
function timestamp() {
  const now = new Date();
  const pad = (n, w = 2) => String(n).padStart(w, '0');
  return `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())} ` +
         `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
}

/**
 * 写入文件
 */
function writeToFile(levelName, message, context) {
  if (!_config.enableFile || !_config.logDir) return;

  try {
    const logFile = path.join(_config.logDir, `eva-soul-${new Date().toISOString().slice(0,10)}.log`);
    const entry = {
      time: new Date().toISOString(),
      level: levelName,
      context,
      message
    };
    const line = JSON.stringify(entry) + '\n';
    fs.appendFileSync(logFile, line, 'utf8');
  } catch (e) {
    // 静默，避免日志写入失败导致崩溃
  }
}

/**
 * 滚动清理旧日志
 */
function rotateLogs() {
  if (!_config.enableFile || !_config.logDir) return;

  try {
    const files = fs.readdirSync(_config.logDir)
      .filter(f => f.startsWith('eva-soul-') && f.endsWith('.log'))
      .map(f => ({
        name: f,
        path: path.join(_config.logDir, f),
        mtime: fs.statSync(path.join(_config.logDir, f)).mtime.getTime()
      }))
      .sort((a, b) => b.mtime - a.mtime);

    if (files.length > _config.maxFiles) {
      files.slice(_config.maxFiles).forEach(f => {
        try { fs.unlinkSync(f.path); } catch (e) {}
      });
    }

    // 检查文件大小
    for (const f of files) {
      try {
        const stat = fs.statSync(f.path);
        if (stat.size > _config.maxFileSize) {
          const newPath = f.path + '.' + Date.now();
          fs.renameSync(f.path, newPath);
        }
      } catch (e) {}
    }
  } catch (e) {}
}

/**
 * 核心输出函数
 * @param {string} levelName 级别名
 * @param {string} message  消息
 * @param {string} context  上下文标签
 * @param {any}    data     附加数据（选填）
 */
function _log(levelName, message, context = 'EVA', data = null) {
  const level = LEVELS[levelName] ?? LEVELS.INFO;
  if (level < _config.level) return;

  const colorFn = LEVEL_COLORS[levelName] || COLORS.RESET;
  const parts = [];

  if (_config.showTimestamp) {
    parts.push(`${COLORS.GRAY}${timestamp()}${COLORS.RESET}`);
  }

  parts.push(`${colorFn}[${levelName.padEnd(5)}]${COLORS.RESET}`);

  if (_config.showContext && context) {
    parts.push(`${COLORS.MAGENTA}[${context}]${COLORS.RESET}`);
  }

  parts.push(message);

  if (data !== null) {
    const dataStr = typeof data === 'object'
      ? JSON.stringify(data)
      : String(data);
    parts.push(`${COLORS.GRAY}${dataStr}${COLORS.RESET}`);
  }

  const line = parts.join(' ');

  if (_config.enableConsole) {
    if (levelName === 'ERROR') {
      console.error(line);
    } else if (levelName === 'WARN') {
      console.warn(line);
    } else {
      console.log(line);
    }
  }

  writeToFile(levelName, message, context);
  rotateLogs();
}

// ============ 公开 API ============

function debug(message, context = 'EVA', data = null) {
  _log('DEBUG', message, context, data);
}

function info(message, context = 'EVA', data = null) {
  _log('INFO', message, context, data);
}

function warn(message, context = 'EVA', data = null) {
  _log('WARN', message, context, data);
}

function error(message, context = 'EVA', data = null) {
  _log('ERROR', message, context, data);
}

/**
 * 带 emoji 前缀的便捷日志（内部 hook 常用）
 */
function hook(message, context = 'EVA') {
  _log('INFO', message, context);
}

function hookWarn(message, context = 'EVA') {
  _log('WARN', message, context);
}

function hookError(message, context = 'EVA', err = null) {
  if (err) {
    _log('ERROR', message, context, { message: err.message, stack: err.stack });
  } else {
    _log('ERROR', message, context);
  }
}

/**
 * 带进度/状态展示的标题（plugin 注册时用）
 */
function section(title) {
  _log('INFO', title, 'EVA');
}

/**
 * 带成功标识的日志
 */
function success(message, context = 'EVA', data = null) {
  _log('INFO', `${COLORS.GREEN}✓ ${message}${COLORS.RESET}`, context, data);
}

/**
 * 带失败标识的日志
 */
function fail(message, context = 'EVA', data = null) {
  _log('ERROR', `${COLORS.RED}✗ ${message}${COLORS.RESET}`, context, data);
}

/**
 * 子项日志（带缩进）
 */
function item(message, context = 'EVA') {
  _log('INFO', `  ${message}`, context);
}

/**
 * 子项成功
 */
function itemOk(message, context = 'EVA') {
  _log('INFO', `  ${COLORS.GREEN}✓${COLORS.RESET} ${message}`, context);
}

/**
 * 子项失败
 */
function itemFail(message, context = 'EVA', err = null) {
  const msg = `  ${COLORS.RED}✗${COLORS.RESET} ${message}`;
  if (err) {
    _log('ERROR', msg, context, err.message);
  } else {
    _log('ERROR', msg, context);
  }
}

/**
 * 从老代码的 console.* 调用迁移过来时，
 * 用此函数做一个自动包装（向后兼容）
 *
 * 用法：
 *   const log = require('./hooks/logger').fromConsole('sessionStart');
 *   log.info('hello');   // => logger.info('hello', 'sessionStart')
 */
function fromConsole(context = 'APP') {
  return {
    log:   (...args) => info(args.join(' '), context),
    warn:  (...args) => warn(args.join(' '), context),
    error: (...args) => {
      const msg = args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ');
      error(msg, context);
    },
    debug: (...args) => debug(args.join(' '), context)
  };
}

/**
 * i18n 翻译快捷方法
 * 用法：logger.t('hooks.sessionStart.registering')
 * 用法：logger.t('hooks.preResponse.memories', { n: 5 })
 * @param {string} key 翻译键
 * @param {object} params 插值参数
 * @returns {string}
 */
function t(key, params = {}) {
  return i18n.t(getLocale(), key, params);
}

module.exports = {
  configure,
  debug, info, warn, error,
  hook, hookWarn, hookError, section,
  success, fail, item, itemOk, itemFail,
  fromConsole,
  setLocale, getLocale, t,
  LEVELS
};
