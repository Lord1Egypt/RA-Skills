/**
 * MDParser 单元测试 —— 验证 Markdown 解析正确性。
 * 运行：node tests/js/test_mdparser.js
 */

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.dirname(path.dirname(__dirname));
const HTML_PATH = path.join(ROOT, "assets", "dashboard.html");

const html = fs.readFileSync(HTML_PATH, "utf8");
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);

// 沙箱中只暴露 MDParser 需要的纯函数依赖
const sandbox = {
  console,
  Math, JSON, Set, Map, Array, String, Number, Object, Boolean,
  Date, RegExp, Error, Promise, parseInt, parseFloat, isNaN, isFinite,
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;

vm.createContext(sandbox);
vm.runInContext(
  scriptMatch[1] + "\nglobalThis.MDParser = MDParser;",
  sandbox,
  { filename: "dashboard-inline.js" }
);

const MDParser = sandbox.MDParser;

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log(`  ✓ ${name}`); }
  catch (e) { failed++; console.error(`  ✗ ${name}\n      ${e.message}`); }
}
function eq(actual, expected, msg) {
  if (actual !== expected) {
    throw new Error(`${msg || "断言失败"}:\n     期望: ${JSON.stringify(expected)}\n     实际: ${JSON.stringify(actual)}`);
  }
}
function contains(str, sub, msg) {
  if (!str.includes(sub)) throw new Error(`${msg || "应包含"}: ${sub}\n     实际: ${str}`);
}
function notContains(str, sub, msg) {
  if (str.includes(sub)) throw new Error(`${msg || "不应包含"}: ${sub}\n     实际: ${str}`);
}

console.log("\n=== 标题 ===");
test("ATX 标题 h1-h6", () => {
  eq(MDParser.parse("# H1"), "<h1>H1</h1>");
  eq(MDParser.parse("## H2"), "<h2>H2</h2>");
  eq(MDParser.parse("###### H6"), "<h6>H6</h6>");
});
test("Setext 标题 h1", () => {
  eq(MDParser.parse("Title\n====="), "<h1>Title</h1>");
});
test("Setext 标题 h2", () => {
  eq(MDParser.parse("Title\n-----"), "<h2>Title</h2>");
});
test("标题含行内格式", () => {
  eq(MDParser.parse("## **粗体** 标题"), "<h2><strong>粗体</strong> 标题</h2>");
});

console.log("\n=== 段落 ===");
test("单行段落", () => {
  eq(MDParser.parse("Hello world"), "<p>Hello world</p>");
});
test("多行段落用空格连接", () => {
  eq(MDParser.parse("第一行\n第二行\n第三行"), "<p>第一行 第二行 第三行</p>");
});
test("双空格硬换行", () => {
  const r = MDParser.parse("第一行  \n第二行");
  contains(r, "<br>", "应包含 <br>");
  contains(r, "第一行", "应包含 第一行");
  contains(r, "第二行", "应包含 第二行");
});
test("反斜杠硬换行", () => {
  const r = MDParser.parse("第一行\\\n第二行");
  contains(r, "<br>", "应包含 <br>");
});
test("空行分隔段落", () => {
  const r = MDParser.parse("段落一\n\n段落二");
  contains(r, "<p>段落一</p>", "应包含段落一");
  contains(r, "<p>段落二</p>", "应包含段落二");
});

console.log("\n=== 强调 ===");
test("粗体 **", () => {
  eq(MDParser.parse("**bold**"), "<p><strong>bold</strong></p>");
});
test("粗体 __", () => {
  eq(MDParser.parse("__bold__"), "<p><strong>bold</strong></p>");
});
test("斜体 *", () => {
  eq(MDParser.parse("*italic*"), "<p><em>italic</em></p>");
});
test("斜体 _", () => {
  eq(MDParser.parse("_italic_"), "<p><em>italic</em></p>");
});
test("粗斜体 ***", () => {
  eq(MDParser.parse("***both***"), "<p><strong><em>both</em></strong></p>");
});
test("粗体含斜体", () => {
  const r = MDParser.parse("**bold *italic* text**");
  contains(r, "<strong>", "应包含 <strong>");
  contains(r, "<em>italic</em>", "应包含 <em>italic</em>");
});
test("斜体含粗体", () => {
  const r = MDParser.parse("*italic **bold** text*");
  contains(r, "<em>", "应包含 <em>");
  contains(r, "<strong>bold</strong>", "应包含 <strong>bold</strong>");
});

console.log("\n=== 删除线 ===");
test("删除线 ~~text~~", () => {
  eq(MDParser.parse("~~deleted~~"), "<p><del>deleted</del></p>");
});

console.log("\n=== 代码 ===");
test("行内代码", () => {
  eq(MDParser.parse("`code`"), "<p><code>code</code></p>");
});
test("行内代码不解析内部 Markdown", () => {
  const r = MDParser.parse("`**not bold**`");
  contains(r, "<code>**not bold**</code>", "代码内不应解析");
  notContains(r, "<strong>", "不应生成 strong");
});
test("围栏代码块", () => {
  const r = MDParser.parse("```\ncode line\n```");
  contains(r, "<pre><code>", "应包含 <pre><code>");
  contains(r, "code line", "应包含代码内容");
  notContains(r, "```", "不应包含围栏标记");
});
test("围栏代码块带语言", () => {
  const r = MDParser.parse("```python\nprint(1)\n```");
  contains(r, 'class="lang-python"', "应包含语言类");
  contains(r, "print(1)", "应包含代码");
});
test("围栏代码块(~~~)", () => {
  const r = MDParser.parse("~~~\ncode\n~~~");
  contains(r, "<pre><code>", "应包含 <pre><code>");
});
test("代码块保留 HTML 实体", () => {
  const r = MDParser.parse("```\n<div>\n```");
  contains(r, "&lt;div&gt;", "应转义 HTML");
});

console.log("\n=== 链接和图片 ===");
test("链接", () => {
  const r = MDParser.parse("[text](https://example.com)");
  contains(r, '<a href="https://example.com"', "应包含链接");
  contains(r, 'rel="noopener noreferrer"', "应包含安全 rel");
  contains(r, ">text</a>", "应包含链接文字");
});
test("链接含 title", () => {
  const r = MDParser.parse('[text](https://example.com "Title")');
  contains(r, 'title="Title"', "应包含 title");
});
test("链接含行内格式", () => {
  const r = MDParser.parse("[**bold**](https://example.com)");
  contains(r, "<strong>bold</strong>", "链接文字应解析格式");
});
test("图片", () => {
  const r = MDParser.parse("![alt](https://example.com/img.png)");
  contains(r, '<img src="https://example.com/img.png"', "应包含 img");
  contains(r, 'alt="alt"', "应包含 alt");
});
test("危险链接被过滤", () => {
  const r = MDParser.parse("[x](javascript:alert(1))");
  notContains(r, "javascript:", "不应包含危险协议");
  contains(r, "x", "应保留链接文字");
});

console.log("\n=== 列表 ===");
test("无序列表", () => {
  const r = MDParser.parse("- a\n- b\n- c");
  contains(r, "<ul>", "应包含 <ul>");
  contains(r, "<li>a</li>", "应包含列表项");
});
test("有序列表", () => {
  const r = MDParser.parse("1. a\n2. b\n3. c");
  contains(r, "<ol>", "应包含 <ol>");
  contains(r, "<li>a</li>", "应包含列表项");
});
test("任务列表", () => {
  const r = MDParser.parse("- [x] done\n- [ ] todo");
  contains(r, 'type="checkbox"', "应包含 checkbox");
  contains(r, "checked", "应包含 checked");
});
test("嵌套列表", () => {
  const r = MDParser.parse("- item1\n  - sub1\n  - sub2\n- item2");
  contains(r, "<ul>", "应包含外层 ul");
  // 嵌套列表项应包含内层 ul
  const nestedCount = (r.match(/<ul>/g) || []).length;
  if (nestedCount < 2) throw new Error(`嵌套列表应包含至少 2 个 <ul>，实际 ${nestedCount}`);
});

console.log("\n=== 引用块 ===");
test("简单引用", () => {
  const r = MDParser.parse("> quote");
  contains(r, "<blockquote>", "应包含 <blockquote>");
  contains(r, "quote", "应包含引用内容");
});
test("多行引用", () => {
  const r = MDParser.parse("> line1\n> line2");
  contains(r, "<blockquote>", "应包含 <blockquote>");
  contains(r, "line1", "应包含 line1");
  contains(r, "line2", "应包含 line2");
});
test("引用含段落", () => {
  const r = MDParser.parse("> para1\n>\n> para2");
  contains(r, "<blockquote>", "应包含 <blockquote>");
  contains(r, "para1", "应包含 para1");
  contains(r, "para2", "应包含 para2");
});

console.log("\n=== 表格 ===");
test("简单表格", () => {
  const r = MDParser.parse("| A | B |\n|---|---|\n| 1 | 2 |");
  contains(r, "<table>", "应包含 <table>");
  contains(r, "<th>A</th>", "应包含表头");
  contains(r, "<td>1</td>", "应包含单元格");
});
test("表格含对齐", () => {
  const r = MDParser.parse("| 左 | 中 | 右 |\n|:---|:---:|---:|\n| a | b | c |");
  contains(r, 'style="text-align:center"', "应包含居中样式");
  contains(r, 'style="text-align:right"', "应包含右对齐样式");
});
test("表格含行内格式", () => {
  const r = MDParser.parse("| **粗体** | *斜体* |\n|---|---|\n| a | b |");
  contains(r, "<th><strong>粗体</strong></th>", "表头应解析格式");
});

console.log("\n=== 水平线 ===");
test("水平线 ---", () => {
  eq(MDParser.parse("---"), "<hr>");
});
test("水平线 ***", () => {
  eq(MDParser.parse("***"), "<hr>");
});

console.log("\n=== HTML 安全 ===");
test("HTML 实体转义", () => {
  const r = MDParser.parse("<script>alert(1)</script>");
  notContains(r, "<script>", "不应包含原始 script 标签");
  contains(r, "&lt;script&gt;", "应转义 HTML");
});
test("行内 HTML 转义", () => {
  const r = MDParser.parse("a < b > c");
  contains(r, "&lt;", "应转义 <");
});

console.log("\n=== 综合场景 ===");
test("混合文档", () => {
  const md = `# 标题

这是**粗体**和*斜体*的段落。

- 列表项1
- 列表项2

> 引用块

\`\`\`js
console.log("hi");
\`\`\`
`;
  const r = MDParser.parse(md);
  contains(r, "<h1>标题</h1>", "应包含标题");
  contains(r, "<strong>粗体</strong>", "应包含粗体");
  contains(r, "<em>斜体</em>", "应包含斜体");
  contains(r, "<li>列表项1</li>", "应包含列表");
  contains(r, "<blockquote>", "应包含引用");
  contains(r, "<pre><code", "应包含代码块");
});

console.log(`\n=== 结果：${passed} 通过，${failed} 失败 ===\n`);
process.exit(failed > 0 ? 1 : 0);
