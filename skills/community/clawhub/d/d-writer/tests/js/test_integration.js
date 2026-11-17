/**
 * Dashboard 集成测试 —— 验证 HTML 结构与关键交互绑定。
 * 运行：node tests/js/test_integration.js
 *
 * 这类测试验证 DOM 结构、事件绑定、ARIA 属性等无法通过纯函数单元测试覆盖的场景。
 * 完整的浏览器交互测试（加载 fixture、键盘导航、搜索、导出）需要在真实浏览器中运行，
 * 见 tests/js/BROWSER_TESTS.md。
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.dirname(path.dirname(__dirname));
const HTML_PATH = path.join(ROOT, "assets", "dashboard.html");
const html = fs.readFileSync(HTML_PATH, "utf8");
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
const js = scriptMatch ? scriptMatch[1] : "";

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log(`  ✓ ${name}`); }
  catch (e) { failed++; console.error(`  ✗ ${name}\n      ${e.message}`); }
}
function ok(cond, msg) { if (!cond) throw new Error(msg || "断言失败"); }
function contains(str, sub, msg) { ok(str.includes(sub), `${msg || "应包含"}: ${sub}`); }

console.log("\n=== HTML 结构完整性 ===");
test("包含 CSP meta 标签", () => {
  contains(html, "Content-Security-Policy", "应有 CSP");
  contains(html, "connect-src 'none'", "CSP 应禁止网络连接");
});
test("包含 5 个标签页按钮", () => {
  const tabs = html.match(/role="tab"/g);
  ok(tabs && tabs.length >= 5, "应有至少 5 个 tab 角色");
});
test("包含 5 个面板", () => {
  const panels = html.match(/role="tabpanel"/g);
  ok(panels && panels.length >= 5, "应有至少 5 个 tabpanel");
});
test("落地页包含选择按钮和兼容模式", () => {
  contains(html, 'id="pickBtn"', "应有选择书架按钮");
  contains(html, 'id="fileInput"', "应有兼容模式文件输入");
  contains(html, "webkitdirectory", "应支持 webkitdirectory");
});
test("应用主体包含主题切换和刷新按钮", () => {
  contains(html, 'id="themeBtn"', "应有主题切换按钮");
  contains(html, 'id="refreshBtn"', "应有刷新按钮");
  contains(html, 'id="rePickBtn"', "应有切换书架按钮");
});

console.log("\n=== ARIA 可访问性 ===");
test("tablist 有 aria-label", () => {
  contains(html, 'role="tablist"', "应有 tablist");
  contains(html, 'aria-label="仪表盘视图"', "tablist 应有 aria-label");
});
test("tab 按钮有 aria-selected 和 aria-controls", () => {
  contains(html, 'aria-selected="true"', "应有选中的 tab");
  contains(html, "aria-controls=", "tab 应有 aria-controls");
});
test("canvas 有 role 和 aria-label", () => {
  contains(html, 'role="img"', "canvas 应有 img 角色");
  contains(html, "角色关系力导向图", "canvas 应有描述性 aria-label");
});
test("搜索按钮有 aria-label", () => {
  contains(html, 'aria-label="搜索当前章节内容"', "搜索输入应有 aria-label");
  contains(html, 'aria-label="关闭搜索（Esc）"', "关闭按钮应有 aria-label");
});
test("主题按钮有动态 aria-label", () => {
  contains(html, "当前主题", "主题按钮应有动态 aria-label");
});

console.log("\n=== 加载遮罩与阶段提示 ===");
test("包含 loadingOverlay（动态创建）", () => {
  contains(js, "loadingOverlay", "应有加载遮罩");
  contains(js, "aria-live=", "加载遮罩应有 aria-live");
});
test("Loading 支持 request ID 防并发", () => {
  contains(js, "requestId", "Loading 应有 requestId");
});

console.log("\n=== 无外部依赖（自包含离线） ===");
test("无外部 script src", () => {
  const extScripts = html.match(/<script[^>]+src\s*=\s*["']https?:\/\//g);
  ok(!extScripts, "不应有外部脚本");
});
test("无外部 link href", () => {
  const extLinks = html.match(/<link[^>]+href\s*=\s*["']https?:\/\//g);
  ok(!extLinks, "不应有外部样式");
});
test("无外部 img src", () => {
  const extImgs = html.match(/<img[^>]+src\s*=\s*["']https?:\/\//g);
  ok(!extImgs, "不应有外部图片");
});

console.log("\n=== 关键函数存在性 ===");
test("定义了 sanitizeUrl（URL 安全）", () => contains(js, "function sanitizeUrl"));
test("定义了 determineRootPrefix（路径匹配）", () => contains(js, "function determineRootPrefix"));
test("定义了 computeSettingCompletion（完成度计算）", () => contains(js, "function computeSettingCompletion"));
test("定义了 parseChapterNum（章节排序）", () => contains(js, "function parseChapterNum"));
test("定义了 diagnoseChapters（章节诊断）", () => contains(js, "function diagnoseChapters"));
test("定义了 stripMarkdown（TXT 导出）", () => contains(js, "function stripMarkdown"));
test("定义了 classifyError（错误分类）", () => contains(js, "function classifyError"));
test("Reader 使用 _marks/_currentMatch/_cleanHtml 属性（修复搜索状态）", () => {
  contains(js, "this._marks", "Reader 应有 _marks 属性");
  contains(js, "this._currentMatch", "Reader 应有 _currentMatch 属性");
  contains(js, "this._cleanHtml", "Reader 应有 _cleanHtml 属性");
});
test("GraphEngine.draw 有空值保护", () => {
  contains(js, "if (!ctx || !canvas || !W || !H) return", "draw 应有空值保护");
});
test("GraphEngine.pause/resume 有空值保护", () => {
  contains(js, "if (!ctx || !canvas) return", "pause/resume 应有空值保护");
});
test("validateBookDir 返回 chapterCount", () => {
  contains(js, "chapterCount", "validateBookDir 应返回 chapterCount");
});
test("SourceSession 收敛全局状态", () => {
  contains(js, "const SourceSession", "应定义 SourceSession");
});
test("Store 有 dataVersion", () => {
  contains(js, "dataVersion", "Store 应有 dataVersion");
});
test("shortcuts 支持 tab 参数", () => {
  contains(js, "register = (key, fn, tab)", "shortcuts.register 应支持 tab 参数");
});
test("Router.switchTab 处理 force 刷新", () => {
  contains(js, "onReload", "应支持 onReload 避免竞态");
});

console.log("\n=== Markdown 安全加固 ===");
test("sanitizeUrl 拒绝协议相对 URL", () => {
  contains(js, "/^\\/\\//", "应检测协议相对 URL");
});
test("sanitizeUrl 处理反斜线绕过", () => {
  contains(js, "replace(/\\\\/g", "应处理反斜线");
});
test("sanitizeUrl 处理 Unicode 冒号", () => {
  contains(js, "replace(/：/g", "应处理全角冒号");
});
test("sanitizeUrl 处理引号注入", () => {
  contains(js, '^["\']+', "应去除首尾引号注入");
});

console.log("\n=== 响应式与可访问性 CSS ===");
test("包含 reduced-motion 媒体查询", () => {
  contains(html, "prefers-reduced-motion", "应支持 reduced-motion");
});
test("包含 sr-only 类", () => {
  contains(html, ".sr-only", "应有屏幕阅读器专用类");
});
test("包含 focus-visible 样式", () => {
  contains(html, "focus-visible", "应有焦点可见样式");
});
test("包含移动端断点", () => {
  contains(html, "max-width:768px", "应有移动端断点");
  contains(html, "max-width:375px", "应有极小屏断点");
});

console.log(`\n=== 结果：${passed} 通过，${failed} 失败 ===\n`);
process.exit(failed > 0 ? 1 : 0);
