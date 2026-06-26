# 阶段一执行指南：数据获取

> 本文档描述如何通过 sessions_spawn 启动子Agent，逐个抓取15个F10模块数据。

---

## 一、工作目录

```
C:\Users\pd\.openclaw\workspace-analysts\data\{股票代码}\
```

示例：`C:\Users\pd\.openclaw\workspace-analysts\data\002792\`

所有15个 `.md` 数据文件都保存到该目录下。

---

## 二、市场标识判断规则

| 股票代码前缀 | 市场 | URL示例 |
|-------------|------|--------|
| 6开头 | SH（上海） | code=SZ002792 → SH600519 |
| 0、3开头 | SZ（深圳） | code=SZ002792 |
| 4、8开头 | 北交所 | 待扩展 |

**东财F10 URL格式：**
```
https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={市场}{代码}&color=b#/{hash}
```

---

## 三、15个模块任务队列

| 序号 | 模块名 | Hash | 文件名 | 路由类型 |
|-----|--------|------|--------|---------|
| 1 | 公司概况 | gsgk | gsgk.md | ✅ 单路由（含3个内嵌Tab） |
| 2 | 经营分析 | jyfx | jyfx.md | ✅ 单路由 |
| 3 | 财务分析 | cwfx | cwfx.md | ✅ 单路由 |
| 4 | 核心题材 | hxtc | hxtc.md | ✅ 单路由（含3个内嵌Tab） |
| 5 | 操盘必读 | cpbd | cpbd.md | ✅ 单路由（超级聚合页） |
| 6 | 同行比较 | thbj | thbj.md | ✅ 单路由 |
| 7 | 股东研究 | gdyj | gdyj.md | ✅ 单路由 |
| 8 | 分红融资 | fhfx | fhfx.md | ✅ 单路由 |
| 9 | 公司高管 | gsgg | gsgg.md | ✅ 单路由（含3个内嵌Tab） |
| 10 | 资本运作 | zbyz | zbyz.md | ✅ 单路由 |
| 11 | 公司大事 | gsds | gsds.md | ✅ 单路由 |
| 12 | 资讯公告 | zxgg | zxgg.md | ✅ 单路由 |
| 13 | 股本结构 | gbjg | gbjg.md | ✅ 单路由 |
| 14 | 关联个股 | glgg/tdyggpm + glgg/tgnggpm + glgg/thyggpm | glgg.md | 🔴 强制多子URL |
| 15 | 龙虎榜单 | lhbd | lhbd.md | ✅ 单路由 |

> **路由类型说明：**
> - ✅ **单路由**：直接访问 `#/hash` 稳定可用，内嵌Tab在页面内自动加载
> - 🔴 **强制多子URL**：直接访问 `#/hash` 会卡住，**必须**使用完整子URL（仅 glgg）
>
> **glgg（关联个股）** 是唯一一个必须用多个子URL的模块，包含3个子URL：
> - `glgg/tdyggpm` = 同地域个股排名
> - `glgg/tgnggpm` = 同概念个股排名
> - `glgg/thyggpm` = 同行业个股排名
> 三个子URL的数据都需要获取，最终合并写入同一个 glgg.md 文件。
>
> **cpbd（操盘必读）** 是超级聚合页，在一个页面内嵌了全量摘要数据（最新指标、大事提醒、资讯公告、核心题材、股东分析、龙虎榜单等），可直接作为全量数据的兜底来源。
>
> **gsgk / hxtc / gsgg** 虽包含多个内嵌Tab，但这些Tab都在同一页面内加载，**不需要**切换子URL，直接访问 `#/hash` 即可获取全部内容。

---

## 四、启动4个Worker子Agent

### 4条 sessions_spawn 命令（一次性发出）

```json
// Worker-1
sessions_spawn:
  task: "数据获取Worker-1初始化 - 等待派发任务"
  runtime: "subagent"
  mode: "session"          // 关键：持久会话，不退出
  runTimeoutSeconds: 0     // 无超时

// Worker-2
sessions_spawn:
  task: "数据获取Worker-2初始化 - 等待派发任务"
  runtime: "subagent"
  mode: "session"
  runTimeoutSeconds: 0

// Worker-3
sessions_spawn:
  task: "数据获取Worker-3初始化 - 等待派发任务"
  runtime: "subagent"
  mode: "session"
  runTimeoutSeconds: 0

// Worker-4
sessions_spawn:
  task: "数据获取Worker-4初始化 - 等待派发任务"
  runtime: "subagent"
  mode: "session"
  runTimeoutSeconds: 0
```

### 派发顺序（负载均衡）

```
Worker-1 → Task1(gsgk) → 完成 → Task5(thbj) → 完成 → Task9(gsgg) → 完成 → Task13(zxgg)
Worker-2 → Task2(jyfx) → 完成 → Task6(fhfx) → 完成 → Task10(zbyz) → 完成 → Task14(glgg)
Worker-3 → Task3(cwfx) → 完成 → Task7(gdyj) → 完成 → Task11(zbyz) → 完成 → Task15(glgg)
Worker-4 → Task4(hxtc) → 完成 → Task8(cpbd) → 完成 → Task12(gbjg) → 完成 → Task15(lhbd)
```

---

## 五、发送给子Agent的任务消息格式

### 第一条消息（初始化后立即发送）

```
请抓取以下F10数据模块：

股票代码：{代码}
市场标识：{SZ或SH}
模块名称：{模块中文名}
目标Hash：{hash}
URL：https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={市场}{代码}&color=b#/{hash}
输出文件：C:\Users\pd\.openclaw\workspace-analysts\data\{代码}\{hash}.md

执行步骤：
1. browser.start()                        ← 启动浏览器（如果未启动）
2. browser.open(url)                      ← 打开目标URL
3. 等待10秒让页面完全加载（等待 browser.snapshot 前 AJAX 数据返回）
4. browser.snapshot(compact=true)          ← 获取页面内容
5. 提炼所有有用的数据，整理为结构化Markdown格式（见下方数据结构化要求）
6. write/写入输出文件
7. 回复："Task{序号} {hash}.md 已完成"

**数据结构化要求（非常重要）：**
- 将页面内容整理为 Markdown 格式，包含以下结构：
  - H2 标题：模块名称（如 "## 公司概况"）
  - 数据项用表格呈现（表格优先于纯文本）
  - 包含数值、单位、时间等关键指标
  - 标注数据来源和时间（如"数据来源：2024年年报"）
- 提取原则：宁可多提取，不要遗漏。即使某些数据暂时判断为无用，也先提取保留
- 过滤内容：不提取导航栏、顶部Banner、悬浮广告、页面Footer中的免责声明
- 表格优先：对财务数据、股东数据、指标数据等优先提取为 Markdown 表格
- 完整优先：不要省略任何数据行，即使某些单元格为空也要保留表格结构
- 子Tab数据：gsgk/hxtc/gsgg 等含内嵌Tab的模块，将所有Tab内容都保留在同一个md文件中，用H3标题区分各Tab
```

### 后续消息（上一个任务完成后发送）

```
继续抓取下一个模块：

股票代码：{代码}
市场标识：{SZ或SH}
模块名称：{模块中文名}
目标Hash：{hash}
URL：https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={市场}{代码}&color=b#/{hash}
输出文件：C:\Users\pd\.openclaw\workspace-analysts\data\{代码}\{hash}.md

执行步骤：
1. browser.open(url)
2. 等待10秒让页面完全加载
3. browser.snapshot(compact=true)
4. 提炼所有有用数据，整理为结构化Markdown（表格优先，数据完整，宁多勿缺）
5. write/写入输出文件
6. 回复："Task{序号} {hash}.md 已完成"

**数据结构化要求：**
- 将页面内容整理为 Markdown 格式，包含以下结构：
  - H2 标题：模块名称（如 "## 公司概况"）
  - 数据项用表格呈现（表格优先于纯文本）
  - 包含数值、单位、时间等关键指标
  - 标注数据来源和时间
- 提取原则：宁可多提取，不要遗漏。即使某些数据暂时判断为无用，也先提取保留
- 过滤内容：不提取导航栏、Banner广告、悬浮广告、页面Footer免责声明
- 表格优先：财务数据、股东数据、指标数据等优先提取为 Markdown 表格
- 完整优先：不要省略任何数据行，即使某些单元格为空也要保留表格结构
- 子Tab数据：gsgk/hxtc/gsgg 等含内嵌Tab的模块，将所有Tab内容都保留在同一个md文件中，用H3标题区分各Tab
```

### 关联个股(glgg)专项处理

glgg 模块是唯一一个**必须**用多个子URL的模块。直接访问 `#/glgg` 会永远卡在"加载中"，必须使用完整子URL：

```
模块名称：关联个股
输出文件：C:\Users\pd\.openclaw\workspace-analysts\data\{代码}\glgg.md

需要抓取的3个URL：
1. https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={市场}{代码}&color=b#/glgg/tdyggpm   → 同地域个股排名
2. https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={市场}{代码}&color=b#/glgg/tgnggpm   → 同概念个股排名
3. https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={市场}{代码}&color=b#/glgg/thyggpm   → 同行业个股排名

执行步骤：
1. browser.start()
2. browser.open(URL1)
3. 等待10秒让页面完全加载
4. browser.snapshot(compact=true)
5. 提炼所有有用数据（表格、排名、涨跌幅、相关性等），整理为结构化Markdown
6. browser.open(URL2)，重复步骤3-5
7. browser.open(URL3)，重复步骤3-5
8. 将3个URL的数据合并整理为Markdown格式（每个子Tab用H3标题区分）
9. write/写入 glgg.md（包含3个子Tab的完整数据）
10. 回复："glgg.md已完成（3个tab）"

**数据结构化要求（与普通模块一致）：**
- 将每个子Tab的数据整理为 Markdown 表格格式
- 包含：排名、股票代码、名称、总市值、涨跌幅、相关性等指标
- 三个子Tab数据都要保留，宁可多抓不要遗漏
- 不要提取广告、Banner、免责条款
```

### 结束消息（所有任务完成后发送）

```
所有15个模块已抓取完毕。感谢你的工作，请结束当前会话。
```

---

## 六、主Agent派发逻辑（伪代码）

```
1. 创建数据目录
   mkdir -p C:\Users\pd\.openclaw\workspace-analysts\data\{代码}

2. 启动4个Worker子Agent，获得sessionKey列表
   [worker1, worker2, worker3, worker4]

3. 初始化任务队列
   队列 = [
     {序号:1, hash:"gsgk", 市场:"SZ", 代码:"002792"},
     {序号:2, hash:"jyfx", 市场:"SZ", 代码:"002792"},
     ... (共15项)
   ]
   当前索引 = 0

4. 立即向各Worker发送第一个任务
   sessions_send(worker1, "Task1消息")
   sessions_send(worker2, "Task2消息")
   sessions_send(worker3, "Task3消息")
   sessions_send(worker4, "Task4消息")
   当前索引 = 4

5. 循环等待子Agent完成回报（通过subagent完成事件感知）

6. 每收到一个完成信号，立即派发下一个
   sessions_send(对应worker, "Task{N+4}消息")
   当前索引++

7. 当 当前索引 >= 15
   向所有Worker发送结束消息

8. 等待所有子Agent确认退出
```

---

## 七、浏览器操作规范

### 每个子Agent独立浏览器

```
browser.start() 时使用默认 profile="openclaw"
每个子Agent维护自己的浏览器实例和Tab
不共享、不混用
```

### 页面加载判断

```
browser.open(url) 后等待页面稳定
如果 snapshot 返回内容为空或仅标题，等待2秒后重试
最多重试3次

注意：东方财富F10是重型SPA（单页应用），页面首次加载和Tab切换时需要等待AJAX数据返回：
- 普通模块（gsgk、cwfx、thbj等）：等待10秒
- 数据量大的模块（zjlx资金流向）：等待15秒
- glgg 关联个股（每个子URL）：等待10秒
- 超时重试：zjlx 建议 runTimeoutSeconds 不低于 240 秒
```

### 数据提炼标准

**保留：**
- 表格数据（数值、指标名称）
- 结构化文字（公司简介、主营构成）
- 关键结论（行业地位、核心业务）
- 时间节点（上市日期、分红日期）

**剔除：**
- 东方财富导航栏、股吧链接
- "郑重声明"段落
- 广告浮窗
- 页脚版权信息

---

## 八、异常处理

| 情况 | 处理方式 |
|------|---------|
| 浏览器打开失败 | 重试3次，每次间隔5秒 |
| 页面内容为空 | 等待2秒后重新 snapshot |
| 写入文件失败 | 检查目录是否存在，报告错误 |
| 子Agent无响应 | 30秒后发送 ping，仍无响应则跳过该任务 |
| 网络超时 | 任务重新入队，稍后重试 |
| glgg 直接访问 #/glgg 页面卡住 | 必须使用完整子URL：glgg/tdyggpm 或 glgg/tgnggpm 或 glgg/thyggpm |
| glgg 某子URL超时 | 重试该子URL最多3次（不影响其他已完成的子URL数据） |
| zjlx 加载慢 | 等待时间延长至15秒，超时提高至240秒 |

---

## 九、进度追踪

主Agent维护任务状态：

```
TaskState = {
  total: 16,
  completed: 0,
  failed: [],
  results: {}  // hash → "已完成" / "失败"
}
```

每次子Agent回报时更新状态，并在所有任务完成时汇总报告。

---

## 十、阶段一完成标准

```
✓ 16个 .md 文件全部存在于 data/{代码}/ 目录
✓ 每个文件非空（>500字节）
✓ 关键模块（gsgk、cwfx、jyfx）必须包含可读数据
```

阶段一完成后，主Agent进入阶段二：分析生成。
