/**
 * 麻小安全策略 - 敏感信息脱敏脚本
 * sanitizer.js v1.2.2
 */
'use strict';

var _G = {
  IPv4: /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g,
  IPv6: /([0-9a-fA-F]{4}:){7}[0-9a-fA-F]{4}|([0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}/g,
  OpenAI: /sk-[A-Za-z0-9_-]{16,}/g,
  Aliyun: /AKLT[A-Za-z0-9]{16,}/g,
  WeChat: /wx[a-zA-Z0-9]{8,}/g,
  JWT: /eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*/g,
  RootPath: /\/root(?:\/[^\s'"]+)+/g,
  HomePath: /\/home\/[^\s\/]+/g,
  SysPath: /\/(?:etc|var|usr\/local)[^\s'"]*/g,
  WinPath: /[A-Za-z]:\\(?:[^\\/:*?"<>|\r\n]+)+/g,
  Hex32: /\b[A-Fa-f0-9]{32}\b/g,
};

var RULES = [
  { name: 'JWT Token',          pattern: _G.JWT,     replacement: '[JWT Token]' },
  { name: 'IPv6地址',           pattern: _G.IPv6,    replacement: '[IPv6地址]' },
  { name: 'OpenAI API Key',     pattern: _G.OpenAI,  replacement: 'sk-...[密钥]' },
  { name: '阿里云 AccessKey',   pattern: _G.Aliyun,  replacement: 'AKLT...[密钥]' },
  { name: '微信 AppID',         pattern: _G.WeChat,  replacement: 'wx...[AppID]' },
  { name: 'Linux 敏感路径',     pattern: /\/root[^\s'"]+/g, replacement: '/path/to/config.json' },
  { name: 'Linux 路径（home）', pattern: _G.HomePath, replacement: '/path/to/user' },
  { name: 'Linux 敏感目录',     pattern: _G.SysPath,  replacement: '/path/to/config' },
  { name: 'IPv4地址',           pattern: _G.IPv4,    replacement: 'x.x.x.x' },
  { name: 'Windows 路径',       pattern: /[A-Za-z]:(?:\\?[^\\/:*?"<>|\r\n]+)+/g, replacement: 'C:\\path\\to\\file' },
  { name: '通用 API Key',       pattern: _G.Hex32,   replacement: 'YOUR_API_KEY' },
];

function sanitize(text, opts) {
  opts = opts || {};
  var log = opts.log || false;
  var result = String(text);
  var applied = [];

  RULES.forEach(function(rule) {
    rule.pattern.lastIndex = 0;
    var count = (result.match(rule.pattern) || []).length;
    if (count > 0) {
      result = result.replace(rule.pattern, rule.replacement);
      applied.push({ name: rule.name, count: count });
    }
  });

  if (log && applied.length > 0) {
    console.log('\u2705 脱敏处理完成：');
    applied.forEach(function(c) {
      console.log('   [' + c.name + '] ' + c.count + '\u5904');
    });
  }
  return result;
}

// ---- P0/P1 危险指令检测 ----
var P0 = [
  /\bssh\s+/i, /\bscp\s+/i, /\btelnet\s+/i, /\brdp\s+/i,
  /rm\s+-rf\s+\//, /rm\s+-rf\s+\~\//, /rm\s+-rf\s+\x24HOME/,
  /del\s+\/f\s+\/s\s+\/q\s+c:\\*/i,
  /cat\s+.*\.env/, /cat\s+.*config.*\.json/,
];
var P1 = [
  /(api[_-]?key|app[_-]?secret|password|token|secret)/i,
  /(修改|更新|删除).*配置/i, /(修改|更新|删除).*技能/i,
  /重启.*gateway/i, /群发.*消息/, /发送到.*群/,
];

function checkCommand(cmd) {
  for (var i = 0; i < P0.length; i++) { if (P0[i].test(cmd)) return { level: 'P0', matched: P0[i].toString() }; }
  for (var j = 0; j < P1.length; j++) { if (P1[j].test(cmd)) return { level: 'P1', matched: P1[j].toString() }; }
  return { level: 'PASS', matched: null };
}

// ---- CLI ----
if (require.main === module) {
  var args = process.argv.slice(2);
  var isLog = args.indexOf('--log') !== -1 || args.indexOf('-l') !== -1;
  var isCheck = args.indexOf('--check') !== -1 || args.indexOf('-c') !== -1;

  var input;
  if (args.indexOf('--stdin') !== -1) {
    input = require('fs').readFileSync(0, 'utf-8').trim();
  } else if (args.indexOf('--file') !== -1) {
    var idx = args.indexOf('--file') + 1;
    var fp = args[idx];
    if (!fp) { console.error('\u274c 请指定文件路径'); process.exit(1); }
    input = require('fs').readFileSync(fp, 'utf-8');
  } else {
    input = args.filter(function(a) { return a.indexOf('--') !== 0; }).join(' ');
  }

  if (!input) { console.error('\u274c 请提供要处理的文本'); process.exit(1); }

  if (isCheck) {
    var r = checkCommand(input);
    console.log(r.level === 'PASS' ? '\u2705 无风险指令' : '\u26A0\uFE0F 风险等级: ' + r.level + '  规则: ' + r.matched);
  } else {
    console.log(sanitize(input, { log: isLog }));
  }
}

module.exports = { sanitize: sanitize, checkCommand: checkCommand };
