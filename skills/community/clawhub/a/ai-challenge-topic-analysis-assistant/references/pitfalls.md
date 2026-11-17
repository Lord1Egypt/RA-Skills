# 实战踩过的坑

## 坑 1 · Workspace 不可用时不要卡住

某些 Windows 环境下 mcp workspace / bash 会 VHDX 启动失败。别反复重试——直接用 `Write` 工具写目标绝对路径即可（Write 会自动建父目录，不需要 mkdir）。

## 坑 2 · file:// 下剪贴板会失败

双击打开 HTML 时 `navigator.clipboard.writeText` 在多数浏览器下被拒。做三级降级：

```js
if (navigator.clipboard && window.isSecureContext) {
  navigator.clipboard.writeText(t).then(done).catch(fallback);
} else {
  fallback();  // execCommand('copy')
}
```

## 坑 3 · 演示模式切换感不够

只隐藏按钮 + 放大字号，评委会觉得"切了跟没切一样"。建议：

- 背景反色/深色渐变
- 关键数字用 `stat-big` 类放大到 2.4rem
- 一处显眼的大数字看板（如 60→22、100%）
- 200ms fade 过渡动画

## 坑 4 · AI 按钮重复输出穿帮

评委至少会点 2–3 次同一个 AI 按钮验证真实性。用 `DRAFT_VARIANTS` 数组按点击次数轮询，附随机置信度徽章（0.79 / 0.82 / 0.86 轮播）。

反例：

```js
const roleMap = { business: '固定文案A', dev: '固定文案B' };
r.opinions.push({ content: roleMap[r.role], isAiDraft: true });
```

正例：

```js
const DRAFT_VARIANTS = {
  business: ['文案A1', '文案A2', '文案A3'],
  dev: ['文案B1', '文案B2', '文案B3']
};
const usedCount = r.opinions.filter(o=>o.isAiDraft).length;
const content = DRAFT_VARIANTS[r.role][usedCount % 3];
const confidence = [0.86, 0.79, 0.82][usedCount % 3];
```

## 坑 5 · 默认停在模块 A 视觉冲击弱

页面首次打开应停在**最有视觉冲击的模块**（如 AI 诊断满屏彩色卡片），配合欢迎横幅点破"这是 AI 已完成的状态"。

## 坑 6 · 时间戳用相对时间

JSON 里用"下周""明天"会被评委追问"哪一天"。全部改绝对日期（如 `2026-08-01`）。

## 坑 7 · 路演稿只有逐字稿不够

只有 3'30" 逐字稿不够。必须补：

- 90 秒速演版（时间被压缩时）
- 演示动线一览表（A4 打印）
- Q&A 逐字答案（≥3 个）
- 万一崩溃预案（页面卡死、按钮不响应、忘词）

## 坑 8 · 语义/关键词断言用"字符串手术"

写实体命中断言时，容易出现下面这种即兴 `.replace` 操作，看起来是在处理格式变体，实际上是给自己挖坑：

反例（真实项目里发生过）：

```js
// 想同时接受 "7天" 和 "7 天"，就随手 replace
const hits = ["7天", "无理由", "退换货", "客服"]
  .filter(k => text.includes(k.replace("7天", "7")));
// bug: "7天" 被替成 "7"，任何含数字 7 的响应都会命中
```

正确姿势——把每个实体写成**同义候选数组**，任一命中即算命中：

```js
const ENTITIES = {
  "7天无理由": ["7天", "7 天", "七天", "seven day"],
  "退换货":    ["退换货", "退货", "换货", "return"],
  "客服":      ["客服", "客户服务", "在线咨询"],
};
const hits = Object.entries(ENTITIES).filter(
  ([_, aliases]) => aliases.some(a => text.includes(a))
);
```

**为什么**：LLM 输出的措辞天然多样，靠单串关键词永远漏；字符串手术又会引入长得像"技术处理"的假通过。同义候选数组是**唯一让评委追问时你能自圆其说**的姿势。

## 坑 9 · 多规则语义判定的 verdict 被后写覆盖

语义 Judge 里常见的写法是"命中一条规则就 `verdict = 'fail'`"，多条规则依次 if/else 时，**后写的会覆盖前写的**：一条 fail 规则先命中，紧接着一条 pass 规则也命中，最终结果反而是 pass。

反例：

```js
if (isHallucination(...))  { verdict = "fail"; score = 15; }
if (isEntityHit(...))      { verdict = "pass"; score = 90; }  // 覆盖了 fail
```

正确姿势——用**取最差**累加器：每条规则只 push 自己的判定，最后 reduce：

```js
const RANK = { pass: 0, warn: 1, fail: 2 };
const results = [];
if (isHallucination(...)) results.push({ v: "fail", s: 15, reason: "..." });
if (isEntityMiss(...))    results.push({ v: "fail", s: 25, reason: "..." });
if (isPromptInject(...))  results.push({ v: "pass", s: 95, reason: "..." });

const worst = results.reduce((a, b) => RANK[b.v] > RANK[a.v] ? b : a);
const finalScore = Math.min(...results.map(r => r.s));
```

**为什么**：多规则 Judge 天然是"任一规则否决则整体否决"的语义，本质是 `reduce(worst)` 而不是 `last-write-wins`。写反了评委不一定发现，但同一条 case 多点几次输出会飘忽（原则 4 的负面表现）。

## 坑 10 · Case 名与 payload 不一致（demo-data 一致性）

生成演示数据时容易出现名字和数据对不上：

```json
{ "name": "边界 · 极大订单号", "request": { "path": { "id": "O" } } }
// 名字说"极大"，payload 却是最短的 "O"
```

评委扫过 case 列表时会一眼看出，直接扣完成度。**提交前跑一次自检**：

```js
// 简单一致性 lint（写在生成脚本或 boot 时执行一次）
cases.forEach(c => {
  const id = c.request?.path?.id || "";
  if (/极大|超长|最大/.test(c.name) && id.length < 20)
    console.warn(`[LINT] ${c.case_id} 名字含"极大"但 id 只有 ${id.length} 字符`);
  if (/极小|最短/.test(c.name) && id.length > 5)
    console.warn(`[LINT] ${c.case_id} 名字含"极小"但 id 有 ${id.length} 字符`);
});
```

**为什么**：demo-data 的每条数据都是评委的"证据"，名与数据对不上会让整套 AI 生成显得不可信。花 30 秒加一段 lint，防止一整套评分被单条低级错误拖累。
