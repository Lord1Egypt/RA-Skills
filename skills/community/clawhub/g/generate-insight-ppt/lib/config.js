/**
 * lib/config.js - 共享配置
 * 
 * 配色方案（2026-04-04 更新）：
 * - 标题：深红色
 * - 正文：黑色为主
 * - 强调色：深红色
 * - 辅助色：淡灰色
 * - 页面背景：白色
 */
const path = require('path');

// 根目录
const ROOT_DIR = path.resolve(__dirname, '..');

// 报告输出根目录
const REPORTS_ROOT = 'D:\\techinsight\\reports';

// 临时文件夹命名格式
const SESSION_PREFIX = 'insight_';

// ========== 配色方案 ==========
const COLORS = {
  // 主色系
  primary: 'C00000',        // 深红色 - 用于标题、强调
  primaryLight: '8B0000',   // 深红偏暗 - 用于次级标题
  accent: 'C00000',         // 强调色 - 同深红色
  
  // 背景色
  background: 'FFFFFF',     // 页面背景 - 白色
  lightGray: 'F5F5F5',      // 浅灰背景 - 内容块背景
  mediumGray: 'E8E8E8',     // 中灰背景 - 分隔区域
  
  // 文字色
  titleColor: 'C00000',     // 标题色 - 深红色
  textColor: '000000',      // 正文色 - 黑色
  darkTextColor: '1A1A1A',  // 深色文字 - 近黑色
  mutedColor: '666666',     // 辅助文字 - 灰色
  
  // 功能色
  highlight: 'C00000',       // 高亮色 - 深红色
  warning: 'E65100',        // 警告色 - 橙色
  success: '2E7D32',        // 成功色 - 绿色
  info: '1565C0',           // 信息色 - 蓝色
  
  // 装饰色
  borderColor: 'D9D9D9',    // 边框色 - 淡灰
  dividerColor: 'E0E0E0',  // 分隔线色
  accentLine: 'C00000'      // 左侧强调线 - 深红色
};

// ========== 字体配置 ==========
const FONTS = {
  title: 'Microsoft YaHei',
  heading: 'Microsoft YaHei',
  body: 'Microsoft YaHei',
  data: 'Calibri'
};

// ========== 标题样式配置 ==========
const TITLE_STYLE = {
  fontSize: 28,             // 标题字号
  fontFace: 'Microsoft YaHei',
  color: 'C00000',          // 深红色标题
  bold: true,
  align: 'left',            // 居左对齐
  marginLeft: 0.5,
  marginTop: 0.3
};

// ========== 正文样式配置 ==========
const BODY_STYLE = {
  fontSize: 14,             // 正文字号
  fontFace: 'Microsoft YaHei',
  color: '000000',          // 黑色正文
  lineHeight: 1.5           // 行高
};

// ========== 幻灯片尺寸 ==========
const LAYOUT = {
  slideWidth: 10,
  slideHeight: 5.625,
  margin: 0.5,
  contentPadding: 0.3
};

// ========== 搜索来源配置 ==========
const SEARCH_SOURCES = [
  { name: 'GitHub', priority: 1, suffix: 'site:github.com' },
  { name: 'Hacker News', priority: 2, suffix: 'site:news.ycombinator.com' },
  { name: 'Stack Overflow', priority: 3, suffix: 'site:stackoverflow.com' },
  { name: '知乎', priority: 4, suffix: 'site:zhihu.com' },
  { name: 'ArXiv', priority: 5, suffix: 'site:arxiv.org' },
  { name: '新闻', priority: 6, suffix: '' },
  { name: '研究报告', priority: 7, suffix: 'filetype:pdf' }
];

// ========== PPT 页面类型 ==========
const SLIDE_TYPES = [
  'cover',              // 封面页
  'toc',                // 目录页
  'executive_summary',  // 执行摘要
  'tech_overview',      // 技术全景图
  'tech_point',         // 核心技术点展开（至少3页）
  'comparison',        // 对比分析
  'summary',            // 总结页
  'generic'             // 通用页面
];

// ========== 洞察类型 ==========
const INSIGHT_TYPES = [
  'fact',      // 事实洞察
  'trend',     // 趋势洞察
  'technical', // 技术洞察
  'comparison', // 对比洞察
  'causal',    // 因果洞察
  'recommendation' // 建议洞察
];

/**
 * 获取会话临时目录
 * @param {string} sessionId 
 * @returns {string}
 */
function getSessionDir(sessionId) {
  return path.join(REPORTS_ROOT, SESSION_PREFIX + sessionId);
}

/**
 * 获取会话子目录
 * @param {string} sessionId 
 * @param {string} subDir 
 * @returns {string}
 */
function getSessionSubDir(sessionId, subDir) {
  return path.join(getSessionDir(sessionId), subDir);
}

module.exports = {
  ROOT_DIR,
  REPORTS_ROOT,
  SESSION_PREFIX,
  COLORS,
  FONTS,
  TITLE_STYLE,
  BODY_STYLE,
  LAYOUT,
  SEARCH_SOURCES,
  SLIDE_TYPES,
  INSIGHT_TYPES,
  getSessionDir,
  getSessionSubDir
};
