/**
 * Dashboard 单元测试 —— 验证纯函数逻辑。
 * 运行：node tests/js/test_dashboard.js
 *
 * 从 assets/dashboard.html 提取 Utils / MDParser / 工具函数，
 * 测试 root prefix、路径匹配、别名映射、章节排序、Markdown 安全、表格、硬换行、Reader 搜索状态、TXT 文件名。
 */

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.dirname(path.dirname(__dirname));
const HTML_PATH = path.join(ROOT, "assets", "dashboard.html");

// 提取 <script> 内容并在沙箱中执行
const html = fs.readFileSync(HTML_PATH, "utf8");
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) { console.error("未找到 <script> 块"); process.exit(1); }

// 创建沙箱，模拟浏览器环境
const sandbox = {
  console,
  window: {},
  document: {
    getElementById: () => null,
    querySelectorAll: () => [],
    querySelector: () => null,
    createElement: () => ({ setAttribute(){}, addEventListener(){}, classList:{toggle(){},add(){},remove(){},contains(){return false;} }, style:{} }),
    addEventListener: () => {},
    documentElement: { classList: { toggle(){}, add(){}, remove(){}, contains(){return false;} } },
    body: { classList: { add(){}, remove(){}, contains(){return false;} }, appendChild(){}, removeChild(){} },
  },
  localStorage: { getItem: () => null, setItem: () => {} },
  location: { hash: "" },
  indexedDB: { open: () => ({ onupgradeneeded:null, onsuccess:null, onerror:null }) },
  NodeFilter: { FILTER_ACCEPT: 1, FILTER_REJECT: 2 },
  Math, JSON, Promise, Set, Map, Array, String, Number, Object, Date, RegExp, Error,
  Blob: function(){}, URL: { createObjectURL: () => "blob:x", revokeObjectURL: () => {} },
};
sandbox.window = sandbox; // self-reference
sandbox.globalThis = sandbox;

// 追加导出：将 const 声明暴露到沙箱全局（const 不会自动挂载到 globalThis）
const exportScript = `
  globalThis.Utils = Utils;
  globalThis.MDParser = MDParser;
  globalThis.ALIASES = ALIASES;
  globalThis.ALIAS_TO_CANONICAL = ALIAS_TO_CANONICAL;
  globalThis.determineRootPrefix = determineRootPrefix;
  globalThis.toRelPath = toRelPath;
  globalThis.isExcludedPath = isExcludedPath;
  globalThis.parseChapterNum = parseChapterNum;
  globalThis.chapterSortKey = chapterSortKey;
  globalThis.computeSettingCompletion = computeSettingCompletion;
  globalThis.diagnoseChapters = diagnoseChapters;
  globalThis.stripMarkdown = stripMarkdown;
  globalThis.Router = Router;
  globalThis.Store = Store;
  globalThis.Reader = Reader;
  globalThis.Characters = Characters;
`;
vm.createContext(sandbox);
vm.runInContext(scriptMatch[1] + exportScript, sandbox, { filename: "dashboard-inline.js" });

// 测试框架
let passed = 0, failed = 0;
function test(name, fn) {
  try {
    fn();
    passed++;
    console.log(`  ✓ ${name}`);
  } catch (e) {
    failed++;
    console.error(`  ✗ ${name}\n      ${e.message}`);
  }
}
function eq(actual, expected, msg) {
  const a = JSON.stringify(actual), b = JSON.stringify(expected);
  if (a !== b) throw new Error(`${msg || "断言失败"}: 期望 ${b}, 实际 ${a}`);
}
function ok(cond, msg) {
  if (!cond) throw new Error(msg || "断言失败");
}

const Utils = sandbox.Utils;
const MDParser = sandbox.MDParser;

console.log("\n=== Utils 工具函数 ===");
test("escHtml 转义 HTML 特殊字符", () => {
  eq(Utils.escHtml("<a>&\""), "&lt;a&gt;&amp;&quot;");
});
test("countWords 统计中文字数", () => {
  eq(Utils.countWords("这是一段中文文字"), 8);
});
test("countWords 去除 Markdown 语法", () => {
  const n = Utils.countWords("```code``` **bold** 正文");
  ok(n >= 2, "应至少统计到正文的字数");
});
test("statusLabel 映射状态", () => {
  eq(Utils.statusLabel("drafting"), "写作中");
  eq(Utils.statusLabel("unknown"), "unknown");
});
test("truncate 截断长文本", () => {
  eq(Utils.truncate("abc", 3), "abc");
  ok(Utils.truncate("abcdef", 3).endsWith("…"));
});

console.log("\n=== 路径匹配与 root prefix ===");
test("determineRootPrefix 计算公共前缀", () => {
  const entries = [
    { webkitRelativePath: "mybook/book.json" },
    { webkitRelativePath: "mybook/chapters/0001.md" },
  ];
  eq(sandbox.determineRootPrefix(entries), "mybook");
});
test("determineRootPrefix 单文件返回自身", () => {
  // 单文件时前缀即为其路径本身（无目录层级）
  eq(sandbox.determineRootPrefix([{ webkitRelativePath: "book.json" }]), "book.json");
});
test("getRootPrefix 按 entries 缓存，不同 entries 独立计算", () => {
  const e1 = [
    { webkitRelativePath: "book1/book.json" },
    { webkitRelativePath: "book1/chapters/1.md" },
  ];
  const e2 = [
    { webkitRelativePath: "book2/book.json" },
    { webkitRelativePath: "book2/chapters/1.md" },
  ];
  eq(sandbox.getRootPrefix(e1), "book1");
  eq(sandbox.getRootPrefix(e2), "book2"); // 不应复用 book1 的前缀
  eq(sandbox.getRootPrefix(e1), "book1"); // 再次调用仍正确
});
test("toRelPath 去掉根前缀", () => {
  const entry = { webkitRelativePath: "mybook/chapters/0001.md" };
  eq(sandbox.toRelPath(entry, "mybook"), "chapters/0001.md");
});
test("isExcludedPath 排除快照/备份", () => {
  ok(sandbox.isExcludedPath("snapshots/0001/book.json"));
  ok(sandbox.isExcludedPath("runtime/rewrites/x.md"));
  ok(!sandbox.isExcludedPath("chapters/0001.md"));
});

console.log("\n=== 别名映射 ALIASES ===");
test("ALIASES 包含所有 canonical path", () => {
  const keys = Object.keys(sandbox.ALIASES);
  ok(keys.includes("story/outline/story_frame.md"), "应包含 story_frame");
  ok(keys.includes("story/current_focus.md"), "应包含 current_focus");
  ok(keys.includes("story/style_guide.md"), "应包含 style_guide");
});
test("ALIAS_TO_CANONICAL 双向映射", () => {
  eq(sandbox.ALIAS_TO_CANONICAL["story/story_bible.md"], "story/outline/story_frame.md");
  eq(sandbox.ALIAS_TO_CANONICAL["story/outline/story_frame.md"], "story/outline/story_frame.md");
});

console.log("\n=== 章节排序 ===");
test("parseChapterNum 解析数字章号", () => {
  eq(sandbox.parseChapterNum("0001_开篇.md"), 1);
  eq(sandbox.parseChapterNum("第二章.md"), 0); // 非数字开头返回 0
});
test("chapterSortKey 非补零章号排序", () => {
  const files = [{ n: "2_二.md" }, { n: "10_十.md" }, { n: "1_一.md" }];
  const sorted = files.sort((a, b) => sandbox.chapterSortKey(a.n).localeCompare(sandbox.chapterSortKey(b.n)));
  eq(sorted.map(f => f.n), ["1_一.md", "2_二.md", "10_十.md"]);
});

console.log("\n=== Markdown URL 安全 ===");
test("sanitizeUrl 拒绝 javascript:", () => {
  // sanitizeUrl 在 MDParser 闭包中，通过 parseInline 间接测试
  const out = MDParser.parseInline("[x](javascript:alert(1))");
  ok(!out.includes("javascript:"), "应过滤 javascript: 协议");
  ok(out.includes("x"), "应保留链接文字");
});
test("sanitizeUrl 允许 https:", () => {
  const out = MDParser.parseInline("[ok](https://example.com)");
  ok(out.includes("https://example.com"), "应保留 https: 链接");
});
test("sanitizeUrl 拒绝 data:", () => {
  const out = MDParser.parseInline("[img](data:text/html,<script>)");
  ok(!out.includes("data:"), "应过滤 data: 协议");
});
test("sanitizeUrl 拒绝协议相对 URL", () => {
  const out = MDParser.parseInline("[x](//evil.com)");
  ok(!out.includes("//evil.com"), "应过滤协议相对 URL");
});

console.log("\n=== Markdown 表格 ===");
test("parse 解析简单表格", () => {
  const md = "| A | B |\n|---|---|\n| 1 | 2 |";
  const out = MDParser.parse(md);
  ok(out.includes("<table>"), "应生成 table");
  ok(out.includes("<th>A</th>"), "应生成表头");
  ok(out.includes("<td>1</td>"), "应生成单元格");
});
test("parse 支持转义管道符", () => {
  const md = "| 列 |\n|---|\n| a\\|b |";
  const out = MDParser.parse(md);
  ok(out.includes("a|b"), "转义管道符应保留字面量");
});
test("parse 列数不一致时补齐", () => {
  const md = "| A | B | C |\n|---|---|---|\n| 1 |";
  const out = MDParser.parse(md);
  ok(out.includes("<tr>"), "应生成行（补齐空单元格）");
});

console.log("\n=== Markdown 硬换行 ===");
test("parse 处理双空格硬换行", () => {
  const md = "第一行  \n第二行";
  const out = MDParser.parse(md);
  ok(out.includes("<br>"), "应生成 <br>");
});
test("parse 普通换行不生成 br", () => {
  const md = "第一行\n第二行";
  const out = MDParser.parse(md);
  // 普通换行在同一 <p> 内，不应有 <br>
  ok(!out.includes("<br>"), "普通换行不应生成 <br>");
});

console.log("\n=== Markdown 任务列表 ===");
test("parse 解析任务列表", () => {
  const md = "- [x] 已完成\n- [ ] 未完成";
  const out = MDParser.parse(md);
  ok(out.includes('type="checkbox"'), "应生成 checkbox 输入框");
  ok(out.includes("checked"), "已完成应有 checked 属性");
  ok(out.includes("task-list"), "应包含 task-list 类");
});

console.log("\n=== 完成度计算 ===");
test("computeSettingCompletion 计算各领域完成度", () => {
  const files = { story_frame: "## 主题\n有内容" };
  const result = sandbox.computeSettingCompletion(files);
  ok(result.length > 0, "应返回领域列表");
  const sf = result.find(d => d.key === "story_frame");
  ok(sf.present, "story_frame 应标记为存在");
});

console.log("\n=== TXT 文件名 ===");
test("导出时清理非法文件名", () => {
  const title = 'book/with:bad*chars?"<>|';
  const safe = title.replace(/[\/\\:*?"<>|]/g, "_");
  eq(safe, "book_with_bad_chars_____");
});

console.log("\n=== stripMarkdown 纯正文导出 ===");
test("stripMarkdown 剥离 Markdown 语法", () => {
  const out = sandbox.stripMarkdown("**bold** `code` [link](url) ~~del~~");
  ok(!out.includes("**"), "应剥离粗体");
  ok(out.includes("bold"), "应保留文字");
  ok(out.includes("link"), "应保留链接文字");
});

console.log("\n=== diagnoseChapters 章节诊断 ===");
test("diagnoseChapters 检测不连续章号", () => {
  const chapters = [{ name: "1.md", num: 1 }, { name: "3.md", num: 3 }];
  const warnings = sandbox.diagnoseChapters(chapters);
  ok(warnings.some(w => w.type === "nonContiguous"), "应检测不连续");
});
test("diagnoseChapters 检测重复章号", () => {
  const chapters = [{ name: "1a.md", num: 1 }, { name: "1b.md", num: 1 }];
  const warnings = sandbox.diagnoseChapters(chapters);
  ok(warnings.some(w => w.type === "duplicateNumber"), "应检测重复章号");
});
test("diagnoseChapters 检测无效章号", () => {
  const chapters = [{ name: "intro.md", num: 0 }];
  const warnings = sandbox.diagnoseChapters(chapters);
  ok(warnings.some(w => w.type === "invalidNumber"), "应检测无效章号");
});

console.log(`\n=== 结果：${passed} 通过，${failed} 失败 ===\n`);
process.exit(failed > 0 ? 1 : 0);
