# 数据可信度陷阱（报价抽取与统计阶段）

> 与 `bid-quote-clarification-sync` §7.2 互补：那份聚焦**澄清/多轮回灌**，本文聚焦**首次抽取与统计**。两者共用一条铁律：**中间产物的统计字段不可直接采信**。

---

## 1. 统计字段必须逐条重算（最高频踩坑）

**现象**：抽取脚本产出的 `zero_count` / `zero_by_cat` / `item_count` 一类汇总字段可能是错的。
**实例**：某项目抽取脚本产出的 JSON 报供应商 C 零单价 98 条、另两家各 2 条；从 `items` 逐条重算真值是 **125 / 0 / 0**。

**铁律**：凡零单价、条目数、完整性占比一类统计，**一律回到 `items` 逐条重算**。
```python
# 零单价判定
is_zero = (item.get('unit_price') in (None, 0)) or (item.get('unit_price') == '')
```

**小计/合计行必须先剔除**，否则"小计 0"被误计入零单价（某项目因此多算 19 条）：
```python
if any(k in desc for k in ("小计","合计","TOTAL","Subtotal","Grand Total")): 
    continue
```

---

## 2. 描述级匹配：先剥离中文再归一化

多轮报价对照（或两表对照）**不能按原序号对应**——BOQ 结构常大改（条目数变化、子组拆分、序号重置）。

标准归一化：
```python
def norm(s):
    s = str(s or '').split('\n')[0]          # ① 只取首行
    s = re.sub(r'[\u4e00-\u9fff]+', '', s)   # ② 剥离中文译文
    return re.sub(r'[^A-Za-z0-9]+', '', s).lower()   # ③ 去符号+小写
```

- **第②步不能省**：新版报价常在描述里补中文译文（`"Surface mounted spotlight 明装射灯"`），保留中文会与旧版失配（实测匹配数 130 → 129，凭空多出 gone/new 各 1 条）。
- 匹配输出三类：`matched`（两轮都有）/ `gone`（仅上轮有）/ `new`（仅本轮有）。
- **匹配率 100% 属巧合**，通常 90% 上下。匹配不上的逐条核对，不要静默丢弃。
- 自校验：同一供应商"文件字节未变"的两个版本，用该键对照应 **100% 一致**；出现差异说明归一化还有问题。

---

## 3. 同一轮次可能有多个文件版本

**现象**：v2 / v3 两个文件**总价相同但逐条不同**（某项目唯一变化是某一条目 €13,999 → €7,890，Option 1 合计均不变）。

**规则**：凡引用明细，必须注明是**哪个文件版本**；若有版本差异，在看板/报告里单列"文件内部版本变化"。

---

## 4. "二选一"方案：只有计入基础合计的那个参与求和

外立面门头之类常出 Option 1 / Option 2（如洗墙灯 vs 格栅），原文自带两行 Total。

- **只有计入基础报价合计的那个 Option 参与分项求和**，另一个方案单独成行、不计入。
- **勾稽时必须先剔除"方案二"条目金额**再与原文总价比对，否则恒多出该笔。

采用价取值顺序：**`promo（优惠价，若有）→ 否则 Option 1 基础报价合计`**。

---

## 5. 名义最低价 ≠ 中标候选

某家数字最低但完整性存疑（大量零单价 / 缺项 / 空表）时：
- 排序一律加 **「名义·不完整」** 标签
- 同时给出 **有效可比排名**（只含完整报价单位）
- **绝不为了给老板一个"最低价"而隐去完整性问题**

**空表判定**：某家某轮多数分项为 0、合计远小于上轮 → 判定未填完，**不采用**，该轮标"不采用"，不进比价。

---

## 6. 优惠额未分摊是"已知差异"，不是差错

分项合计（基础价）≠ 优惠后总价 时：
- **不做分摊推算**（红线：禁止估算）
- 分项表加注说明"优惠额未分摊"
- 排名用优惠后价
- **勾稽基准用「原文报价」，不要用「采用价」**——否则把优惠额误判成差错

---

## 7. 无本轮报价的单位要补位，不能静默剔除

某家没提交本轮报价时：
- **沿用上轮价参与本轮排名**（保证各家完整对比），并标注「沿用首轮·无更新」
- **排名变化必须用计算值**，不能只看有本轮报价的那几家
- 注意补位会改变他人名次（某家沿用价可能低于另一家的新报价）

---

## 8. 单方造价的口径

- 单方 = `采用价 / 面积`，必须在页面上**标注公式**（透明算术）。
- 各家面积原则上相同（同一项目）；**历史门店各用各的面积**，不要统一除以本项目面积。
- 历史门店若只给了现成单方值而无总额/面积，直接用；若给了总额和面积，**优先用 `total / area` 自算**，避免手填错误。

---

## 9. 抽取阶段的"三不"

1. **不改写描述原文**（保留多行、外文、中文译文），归一化在后续单独做。
2. **不补全缺项**（缺单价就是缺单价，标"待确认"，不猜）。
3. **不换算币种/税率**（原文是含税就标含税，需要不含税对比时请使用者提供或确认税率，不自行折算）。

---

## 10. 版式溢出：`nowrap` 会把长文本表撑出页面（交付后被退回的高频 bug）

**现象**（使用者原话："显示出现重大失误，已经超出页面范围"）：附录 A 的逐项核查表里，「法规依据」列放了整段西班牙法规原文，整张表横向撑破卡片边界，页面右侧出现大片空白/横向滚动条，最后一列被切掉看不到。

**根因**：模板全局有 `td{white-space:nowrap}`（专为数字列不被折行而设），但**长文本列继承了它**——单元格拒绝换行 → 单元格 min-content 宽度 = 整段文字宽度 → 表格 min-content 撑爆卡片。

**修复**（`build_dashboard.py` 已内置，新增长文本表直接套用）：

```css
.tblscroll{overflow-x:auto;margin-bottom:4px}          /* 兜底：极端窄屏可局部横滚，不撑破页面 */
table.fixed{table-layout:fixed}                        /* 列宽由 colgroup 定，不被内容反推 */
table.fixed th,table.fixed td{white-space:normal;word-break:break-word;overflow-wrap:anywhere}
table.fixed td.lft,table.fixed th.lft{text-align:left}
```

```html
<div class="tblscroll">
  <table class="fixed">
    <colgroup>
      <col style="width:5%"><col style="width:22%"><col style="width:10%">
      <col style="width:9%"><col style="width:28%"><col style="width:26%">
    </colgroup>
    <thead><tr><th>序号</th><th class="lft">项目</th>…</tr></thead>
    <tbody><tr><td class="mono">1</td><td class="lft">…</td></tr></tbody>
  </table>
</div>
```

- **凡「表格里有整句/整段文字」的列，一律走 `table.fixed` + `<colgroup>` + `.lft`**，不要用裸 `<table>`。数字列保留 `.mono`，长文本列加 `.lft` 左对齐。
- `<colgroup>` 各列百分比之和必须 **= 100%**；序号列别低于 5%、徽章列别低于 9%，否则窄屏下表头会折行。
- 数据里若含 `**强调**` 标记，用 `rich()`（`esc()` + 把 `**x**` 转 `<b>`）渲染，避免页面上出现字面星号。

**验证方式（不要靠目视，一定要浏览器实测）**：
```bash
python scripts/check_overflow.py ./报价分析看板.html 1500,1280,1100
# 正对照：把「裁剪兜底」与「长文本换行」两条规则一齐置空，应能复现页面级溢出，自证检测有效
python scripts/check_overflow.py ./报价分析看板.html 1500,1280 \
  --before ".tblscroll{overflow-x:auto;margin-bottom:4px}" \
  --before "table.fixed th,table.fixed td{white-space:normal;word-break:break-word;overflow-wrap:anywhere}"
```
判读标准（三个指标语义不同，别混用）：

| 指标 | 含义 | 是否致命 |
|---|---|---|
| `PAGE_SCROLL` | 页面级横向滚动（`doc.scrollWidth - doc.clientWidth`）——「超出页面范围」最直接的判据 | ✅ 必须为 0 |
| `BEYOND_WRAP` | 内容视觉上超出 `.wrap` 右边界（已按祖先 overflow 裁切折算）——捕获"页面不滚但内容被切掉" | ✅ 必须为 0 |
| `SCROLLABLE` | 某容器内部横向滚动（`scrollWidth > clientWidth`） | ⚠️ 信息项，`--strict` 可升级为失败 |

修前该看板 `--before` 对照态在 1500/1280px 分别报 `PAGE_SCROLL=384/500`（`docScrollW=1862/1758 > docClientW=1478/1258`），修后均为 0。

> ⚠️ **写测量脚本的四个坑**：
> ① 注入点必须取**最后一个** `</body>`（`html.rfind("</body>")`）——echarts 压缩代码里含字面量 `</body>`，用 `replace` 会把脚本注入进 JS 字符串，永不执行、报 `NO_RESULT`；
> ② 抓结果的正则要写成 `<pre id="__measure"[^>]*>`——注入的 `<pre>` 带 `style` 属性，写死无属性匹配不上；
> ③ **算 `BEYOND_WRAP` 必须折算祖先 overflow**：`getBoundingClientRect()` 返回布局盒、不理会祖先 `overflow`，直接比 `wrapRight` 会把正常的 `overflow-x:auto` 宽表误判为溢出（**假阳性**，某项目曾据此误报）；
> ④ **只靠 `BEYOND_WRAP` 会漏报**：沿途若有 `overflow:hidden` 祖先把内容裁掉，它会折算成 0，而文档其实已经横向滚动了（**假阴性**）——所以必须同时看 `PAGE_SCROLL`。两者互补，缺一不可。
>
> `verify_dashboard.js` 查的是"JS 能不能跑、图能不能画"，**查不出溢出**，两个校验都要跑。

---

## 11. ECharts 标签重叠与层级：均值线 label 被 bar 压字 / 多组数据 label 堆叠

**现象**（使用者原话："字体要在均值线上层图层，显示才会清晰；多组数据堆在一起相互遮盖"）：
第七节「全门店单方造价对比」里，过往项目单方均值线的标签与 bar 顶部数值重叠，彼此遮盖；历史门店 bar 数量多，顶部数值全挤在一起。

**根因**：
1. 均值线 series 默认 `z` 与 bar 同级或更低，其 `markLine.label` 会被 bar 或 bar label 盖住。
2. 同一张图上有 bar 顶部 label + 均值线 label + `endLabel`，多个文本在相近位置堆叠。
3. 历史门店有 8 家，每家都显示顶部数值，与当前项目 4 家数值+均值线标签挤成一团。

**修复**（`build_dashboard.py` 已内置）：
- 均值线/辅助线统一 `z: 10`（高于 bar 的 `z: 2`）；`markLine.label` 再设 `z: 11`。
- 标签加 **半透明白底 + padding + borderRadius**，确保压在线/柱之上仍清晰可读：
  ```json
  "backgroundColor": "rgba(255,255,255,0.85)", "padding": [2, 4], "borderRadius": 3
  ```
- bar 系列加 `"labelLayout": {"hideOverlap": True}`，重叠时自动隐藏部分 label。
- **历史门店柱不显示顶部数值**（精确值进 tooltip），只保留当前项目单位柱的顶部数值，避免 12 个 label 堆叠。
- 均值线只保留 `markLine.label`，**去掉冗余的 `endLabel`**，避免同一数值出现两个标签。

**验证**：Chrome headless 截图第七节 + 第四节，均值线标签清晰、无压字、无堆叠。`check_overflow.py` 同时通过（这些调整不影响溢出）。

---

## 12. Python 常量名泄漏进 JS：语法检查查不出，运行时静默中断后续全部渲染

**现象**：改完生成器重建看板，页面不白屏、也不报错，但**某一段之后的内容全空** ——
表格没有行、图表不画、按钮无反应。`node --check` 通过，`verify_dashboard.js` 的
「内容为空的容器」却列出一长串 id（且它们**恰好都在某一处之后**）。

**根因**：生成器把 **Python 侧的常量名**当 JS 变量写了：
```python
# Python 侧
FACADE_IDX = 4
DATA = {"facade_idx": FACADE_IDX, ...}
```
```js
// JS 侧（错）：FACADE_IDX 在 JS 里根本不存在
+'<td>'+fmt(DATA.r2[v].cats[FACADE_IDX],2)+'</td>'
// JS 侧（对）：用注入的 DATA 字段
var FAC = DATA.facade_idx;   // 或直接 DATA.facade_idx
```
`FACADE_IDX` 是**合法标识符**，所以语法检查必然放过；只有浏览器执行到那一行才抛
`ReferenceError`。因为整段 JS 在一个 IIFE 里，**抛出点之后的所有 `innerHTML=` 都不再执行** ——
于是「定标建议 → 评分表 → 评委打分 → 飞书记录」整片空白，而前面的表格一切正常。
「空容器清单恰好是抛出点之后的所有 id」就是最典型的指纹。

**修法**：JS 取数一律走 `DATA.*` 或 JS 自己 `var` 的变量。生成器里**不要**把 Python 常量名
拼进 JS 字符串。

**交付前必跑（新增第 3 道静态检查）**：
```bash
python scripts/lint_py_const_leak.py ./build_dashboard.py ./报价分析看板.html
# 退出码 0 = 无泄漏（可交付）；1 = 有泄漏（不可交付）
```
规则：取生成器里所有顶格大写常量名 → 剥掉 JS 注释后扫描产物 script 块 →
命中且不是 JS 自己 `var` 的同名变量即判泄漏。

**为什么 `verify_dashboard.js` 挡不住**：它只在**脚本能跑完**的前提下检查渲染产出。
一旦某行抛异常，它报的是「一堆容器为空」，不告诉你**是哪一行**抛的 —— 需要靠
「空容器清单的边界位置」+ 本 lint 才能秒级定位。

---

## 13. 看板内的「评委打分 / 人工评分」持久化：保存按钮 + 关闭重开自动带出

**需求原型**：评委在页面上填姓名与打分，要求**保存后下次打开链接自动带出上次结果**，
除非点「清空/重新打分」。

**正确做法**（纯前端、零依赖）：
1. 输入即自动 `localStorage.setItem(KEY, JSON.stringify({scores, savedAt}))` —— F5 不丢数据；
2. **另设**一个显式「✔ 保存打分」按钮，点击时写入并刷新状态文案
   （`✔ 已保存 9月16日 13:33 · 本机浏览器，下次打开自动带出（当前 3 位评委）`）；
3. **`loadTeam()` 必须在页面加载时从 localStorage 恢复**，绝不能在打开时
   `localStorage.removeItem()` —— 那等于把「保存」功能作废；
4. 恢复后要**归一化校验**每个字段（类型/范围/整数），非法值一律置空，
   兼容旧版本存储结构；
5. 「清空所有评委打分」要同时覆盖 localStorage，并 `confirm()` 二次确认。

**表格初始值 vs 打分值**（易错）：
- 若**尚无任何评委打分**，团队维度显示静态评估基线（否则打开就是一张全 0 的空表，
  与结论文案里的分数对不上）；
- 一旦**有任何评委开始打分**，即全面切换为「有效平均」口径，未被打分的
  「供应商 × 维度」计 0。
- 实现上：初始只在 `hasJudge` 为真时才调用刷新函数，否则保留静态渲染。
- ⚠️ 渲染顺序陷阱：表体 `innerHTML` 是在初始化**之后**才写入的，
  若把 `updateScoreTable()` 写在表体渲染之前，首屏永远只有静态值。
  应放在表体渲染**之后**（或用 `hasJudge` 门控）。

**跨进程验证（真机验证，别只用桩）**：桩化 DOM 无法覆盖 localStorage 与复合选择器
（`#tbl tr.subrow td[data-v="X"] .cv`）。用两次 headless Chrome、共用同一个
`--user-data-dir`，即「关掉再打开」的真实语义：
```bash
# 阶段一：注入脚本填分 + 点保存
chrome --headless=new --user-data-dir=./prof --virtual-time-budget=12000 \
       --dump-dom "file:///.../副本_fill.html"
# 阶段二：同一 profile 再开一次，读回输入框与两张评分表的文本
chrome --headless=new --user-data-dir=./prof --virtual-time-budget=12000 \
       --dump-dom "file:///.../副本_check.html"
```
注入点用 `html.rfind("</body>")`；结果写进 `<pre id="__test">` 再正则取回
（与 `check_overflow.py` 的 `__measure` 同源）。注意：
- 副本必须**以二进制/`newline=''` 读写**，否则文本模式会把 CRLF 来回翻译，体积对不上；
- 注入锚点要**唯一**：`renderTeamPanel();` 在主流程缩进 2 空格、在事件处理函数里缩进 8 空格，
  用 `^ {2}renderTeamPanel\(\);` 才不会注错地方；
- 断言前先算准 DOM 顺序：评委表单行的 16 个 number input 顺序是
  **维度外层 × 供应商内层**，所以前 4 个是「履约能力」下的 4 家，不是某一家 4 个维度。


---

## 14. 文案里的「单位 × 金额」错配：排序序位 ≠ 指标归属（2026-09-16 实盘踩坑）

**症状**：看板渲染出来写「最低为 **甲公司** €269,414.14」——单位名与金额**张冠李戴**。
数字全对、表也全对，只有这句**文案**错了，所以数值自检、语法检查、溢出体检**三关全过**。

**根因**：同一次渲染里有两条互不相干的排序，代码图省事复用了同一个数组的下标 0：

```js
// nfOrder = 按【综合分】降序 —— 用于列顺序与名次
var nfOrder = TEAM_VENS.slice().sort(function(a,b){return rec.composite_nofac[b]-rec.composite_nofac[a];});
//         ^ 下标 0 是「综合分最高」= 甲公司，不是「价格最低」= 丁公司
...
+'最低为 <b>'+esc(VN[nfOrder[0]])+' €'+fmt(rec.min_nofac,2)+'</b>'
```

`rec.min_nofac`（= 269,414.14）取自**另一套口径**（nocat 金额升序）的第 0 名 丁公司，
却配上 `nfOrder[0]` 的单位名 甲公司 → 错配。

**规则（硬性）**：
> 每个数组只服务一个指标。**「取某指标的第一名」必须就地为该指标单独排序**，
> 严禁拿「另一个指标的排序结果」的下标去索引这个指标的值。

**修法**：
```js
var nfOrder = TEAM_VENS.slice().sort(function(a,b){return rec.composite_nofac[b]-rec.composite_nofac[a];}); // 综合分 → 列顺序
var nfLowV  = TEAM_VENS.slice().sort(function(a,b){return (DATA.nofac_r2[a]||Infinity)-(DATA.nofac_r2[b]||Infinity);})[0]; // 金额 → 最低单位
```

**为什么三道校验都拦不住**：
- `node --check` / `verify_dashboard.js` 只看**能不能跑、有没有 NaN** —— 这句文案字符串拼接完全合法；
- `check_overflow.py` 只看**版式** —— 错配的文案跟溢出无关；
- `lint_py_const_leak.py` 只看**常量泄漏** —— 与标识符来源无关。

**必须补第 4 道：渲染级「单位↔金额」配对断言。**
`grep` 静态源码查不到 —— 千分位是客户端 `fmt()` 生成的，源码里只有裸数字 `269414.14`。
做法：`--dump-dom` 渲染后取容器 `innerText`，断言目标句同时含**正确单位名**且
**不含**「错误单位名 + 该金额」的组合：

```python
snote = rendered('scoreNoFacNote')
assert '丁公司' in snote and '269,414.14' in snote
assert not re.search(r'最低为\s*甲公司\s*€?\s*269,414', snote)
```

**通用自检口径**：任何「<单位> 为 … €<金额>」句式，都要能被一条
「该单位确实持有该金额」的断言覆盖（金额 → 单位 是**函数关系**，不是装饰）。

**已固化为可复用脚本**：`scripts/dump_rendered.py` —— 渲染后取容器 `innerText`／表格逐行文本，按 JSON 规则做 `must_contain` / `must_not_contain` / `must_match` / `must_not_match` 断言。

```bash
# 排错：看渲染文本
python scripts/dump_rendered.py 看板.html --ids tScore,scoreNote
# 闸门：exit 0 才可交付（--log 落 UTF-8 报告，绕开 Windows 控制台 GBK 乱码）
python scripts/dump_rendered.py 看板.html --rules render_rules.json --log gate.log
```

⚠️ **脚本自身坑**：`--rules` 里出现的容器 id 会被自动并入渲染清单 —— 首版没做这件事，导致「规则里写了、`--ids` 里没写」的容器一律误报 `__MISSING__`（假失败）。



---

## 15. `.tblwrap{max-height:…}` 静默裁切：最关键的一行被藏起来（2026-09-16 实盘踩坑）

**症状**：表格渲染"看起来正常"，但**最后一行不见了** —— 而它恰好是「合计 / 综合总分」。
浏览器里手动往下滚一下能看到，**截图、打印、PDF 一律丢失**。
更迷惑的是：表格盒高 > 容器高，后随的 `.note` 会压在那片溢出区上，
看上去像"摘要文字和表格重叠了"，很容易被误判成 margin 或 z-index 问题。

**机制**：
```css
.tblwrap{overflow-x:auto; …; max-height:420px; overflow-y:auto}   /* 全局兜底 */
```
- 内容 489px > 上限 420px → 溢出部分进入**容器内部滚动区**；
- 表格自身 `getBoundingClientRect()` 仍报 489px（元素没被改尺寸，是祖先在裁），
  所以**它的盒底比容器的盒底还低 69px**；
- 紧随其后的 `.note`（static 流 + 10px margin）从容器底开始 → 正好压在那 69px 上。

**实测数据（某门店装修报价看板）**：
| 表 | 内容高 | 容器高 | 被藏 | 受害行 |
|---|---|---|---|---|
| `tScore`（10.3-A） | 489px | 420px | **71px** | 综合总分（100 分） |
| `tScoreNoFac`（10.3-B） | 489px | 420px | **71px** | 综合总分（100 分） |
| `tOverview`（1100px 视口） | 466px | 420px | **46px** | 尾行（窄视口列宽变窄、换行变多） |

⚠️ 注意第三行：**同一个表在 1500px 好好的，到 1100px 就被裁** ——
窄视口下单元格换行变多、行变高，很容易越过固定上限。
所以「宽带下没问题」不能作为放行理由，**必须多视口跑**。

**修法（推荐：反转默认）**：
```css
.tblwrap{max-height:none !important;overflow-y:visible}   /* 默认不裁 */
.tblwrap-scroll{max-height:420px;overflow-y:auto}          /* 确需内部竖滚时单项开启 */
```
理由：数据类看板里「页面变长」远好过「关键行消失」。不要再让兜底样式默认裁数据。

**检测（已固化进 `check_overflow.py` 的 `CLIPPED` 指标）**：
在每次测量里扫 `.wrap *`，命中条件 = **显式设了 `max-height`（≠ none）** 且
`scrollHeight - clientHeight > 8`。只看这两条，是因为要避开"设计上就该滚动"的容器 ——
例如靠 `min-width` 撑宽的宽表（`.tp-tablewrap`），它没有 max-height，不会误报。

判读：`CLIPPED=0` 才是通过；`CLIPPED>0` 直接 exit 1 不可交付，明细在 `CLIP:` 行。
正对照：把该 `` `.tblwrap{max-height:none !important}` `` 规则用 `--before` 传进去置空，
`CLIPPED` 应从 0 变回 2~3 —— 证明检测器真的抓得住，而不是碰巧为 0。

**为什么之前的校验全都没发现**：
- `node --check` / `verify_dashboard.js`：只查 JS 能否跑、有无 NaN —— **DOM 完全正常**；
- `check_overflow.py` 旧版：只有 `PAGE_SCROLL` / `BEYOND_WRAP` / `SCROLLABLE`
  三个**横向**指标 —— 这是**纵向**裁切，横向一道都命不中；
- 人工截图：截的是"当前 CSS"，而 max-height 让页面**看起来只是排版紧**，不细看发现不了。

**排查手法（判断"DOM 有但看不见"）**：取元素 `getBoundingClientRect()`，
再和它的**父容器** `getBoundingClientRect()` 比 ——
若 `el.bottom > parent.bottom`，就是被祖先裁了（而不是没渲染）。
配合 `document.elementFromPoint(中心点)` 看命中的是不是别人（被遮挡）。
注意 `elementFromPoint` 会跳过 `pointer-events:none`，**必须用几何区间相交做最终判定**，
否则会假阳性。

---

## 16. 「评委打分」的终局：从 localStorage 改为**构建期固化**（2026-09-17 实盘返工）

**§13 的 localStorage 方案适用于「同一台电脑反复打开」**。但只要看板要**发给别人看**
（云端链接、附件、iframe 嵌入），它就必然出事，而且**不报错**：

| 现象 | 根因 |
|---|---|
| 本地打开有分数，云端打开全空 | `file://` 与 `https://` 是不同 origin，localStorage 互不相通 |
| 嵌入式打开 storage 直接不可用 | 第三方存储策略 → `setItem` 抛异常，被 try/catch 吞掉 |
| 别人电脑显示的是**另一套分数** | 探不到分 → **静默回退到静态基线**，看起来合理却是错的（最危险） |
| 链接分享后别人看到的是旧分数 | 打分码要走 URL `#s=`，实际没人会用 |

**终局做法：构建期把分数烘焙进 HTML 字节**（`window.__SCORE_SEED__`），页面只读。

```
score_config.json（评委 × 维度 × 单位 的整数分）
      ↓ gen_score_panel.py
score_panel.html（只读表 + 内联 seed）+ score_panel.meta.json（有效平均/综合分/名次）
      ↓ 插入看板
任何设备打开 → 同一批分数（分数随字节走，不依赖任何本机状态）
```

**页面必须做到的 4 件事**（`verify_score_frozen.py` 逐条硬断言）：

1. 打分区块内 **0 个** `input/select/button/textarea`；
2. **不写入**任何评分类 `localStorage` key（扫描所有 key，含 `score|team|judge|rate` 即判失败）；
3. 不提供「保存 / 导出打分码 / 清空」入口；
4. 文案写明「任何设备打开结果一致」+ 改分路径（更新种子 → 重新生成 → 重新发布）。

**脏数据的唯一正确处理 = 置空 + 告警，不许补齐**：

| 输入 | 处理 |
|---|---|
| 打分缺失 | 置空，该格**不计入**有效平均分母（不是当 0 用），并告警 |
| 超出 `0~max` | 置空 + 告警（**绝不**截断成 max，那是篡改数据） |
| 非整数（如 4.5） | 置空 + 告警（**绝不**四舍五入） |
| 评委姓名为空 | **整行不参与**任何维度的平均（防止空行拉低均值） |

> 这一条是「只用原文数字」红线在打分场景的落地：**宁可缺一格并留痕，不可补一个数**。
> 另：某维度全无有效打分时按 0 计入综合分，但必须输出 `missing_dims` 并在页面提示，
> 否则等于静默压分，老板会以为该单位真的差。

**为什么必须用「两个全新 `--user-data-dir`」验证**：
同一 profile 跑两次只能证明「页面能渲染」，证明不了「换台电脑分数不变」。
两个全新临时目录 = 两台互不相通的电脑，结果一致才算固化成功。
`verify_score_frozen.py` 默认就跑双档案，并对**线上真字节**复用同一套断言。

**发布后别拿分享链接当产物**：分享 URL 常只是几 KB 的引导壳（含 `__PUBLISH_BOOTSTRAP__`），
真实 HTML 在另一个静态域名、**版本号递增**。核验要下载真字节，否则断言的是壳页。
详见 `references/publish-and-verify.md`。

---

## 17. 事后往 HTML 里注入片段：命中**假锚点**，塞进 JS 字符串还不报错（2026-09-23 实盘踩坑）

**场景**：把评分区块（`gen_score_panel.py` 的产物）拼进主看板。看着是"插一段 HTML"这么简单，
于是写脚本找锚点：`re.search(r"<style[^>]*>", html)` 或 `html.find("</body>")`，然后 insert。

**结果**：脚本全部"成功"，产物字节数正常变大，浏览器**完全不报错**，`grep scorePanel` 也搜得到 ——
但打开页面**根本没有评分节**。`verify_score_frozen.py` 10 项断言全 FAIL，而原因极难定位。

**根因**：产物内联了**压缩版 ECharts**，其 `saveAsImage` 干函数里有一个字符串字面量，
包含完整的 `</body>` 与 `<style>` 片段：

```js
// ECharts 源码里的字面量（示意）—— 这就是那个假锚点
w = '<body style="margin:0;"><img src="' + s + '" style="max-width:100%;" title="'
    + (b && b[0] || '') + '" />'
    + '...</body>', S = window.open(); S.document.write(w), S.document.title = i
```

文件里 `<style>` 只出现 1 次（真的那个），但 `</body>` 出现 **2 次** —— 前一个在 ECharts
字符串里，后一个才是真的结构收尾。按 `find` 找第一个命中，必然踩中假的。

**自证手法**（用来确认"注入点是否落在 script 内"）：
枚举所有 `<script>` / `</script>` 边界位置，看目标 DOM 的偏移是否落在某个 script 区间内：

```
16692 <script>      1045233 </script>      1045242 <script>   1203692 </script>
1203701 <script>    1205065 </script>      1209669 <script>   1212722 </script>
scorePanel @ 1205096  ← 落在 1203701~1205065 的 script 区间里 = 被塞进 JS，页面看不见
```

**正确做法：不要事后注入，用生成器的装配入口。**
`build_dashboard.py --score-panel ./score_panel.html` 在生成阶段就把 CSS / DOM / JS 三处按
结构顺序嵌入，不依赖任何字符串匹配：

```bash
python scripts/gen_score_panel.py --config ./score_config.json --out ./score_panel.html --report
python scripts/build_dashboard.py --config ./config.json --score-panel ./score_panel.html --out ./看板.html
```

**如果确实必须脚本级拼装**（适配别的渲染链路），锚点要有**唯一性依据**，并在装配后断言：

| 要求 | 做法 |
|---|---|
| 锚点唯一 | 用 `re.search(r"</title>\s*<style", html)` —— `</title>` 在 head 里只出现一次且必在真 CSS 前 |
| 装配后自检 | 断言目标 DOM 偏移**不在任何 `<script>…</script>` 区间内**，且早于 `</body>` 真位置 |
| 别信"搜到了" | `count("scorePanel") == 1` 在错误注入下**也是成立的** —— 它在 JS 字符串里 |

> 通用教训：**只要产物内联了第三方压缩库，就没有"安全的字符串锚点"**。
> 凡是要往产物里插东西，一律走生成器的显式参数，把装配变成构建期的一等公民。

### 附：装配路径的解析口径

`--score-panel` 与 `--out` 都按 **`config.json` 所在目录**解析（与 `quotes` / `history` 同口径）。
在 `examples/` 下跑时，写 `--score-panel examples/_t_panel.html` 会被解析成
`examples/examples/…` 而报 `FileNotFoundError`。拿不准就用绝对路径。

---

## 18. 校验脚本按**块序号**定位：多装配一个 script 就假失败（2026-09-23 同轮踩坑）

**场景**：`build_dashboard.py --score-panel` 装配成功后，`verify_dashboard.js` 立刻报：

```
❌ 运行时异常: DATA is not defined
DATA.js:17
  (DATA.staticCharts || []).forEach(function (id) {
```

**根因**：校验脚本原先按**数量倒推**定位块：

```js
const dataJs = blocks[blocks.length - 2];   // “约定 [n-2]=DATA  [n-1]=app”
const appJs  = blocks[blocks.length - 1];
```

这个约定只在"恰好 3 块（echarts / DATA / app）"时成立。装配评分注入段后变成 4 块，
于是 `blocks[n-2]` 取到的是 **DATA**、却被当成 app 执行 → DATA 还没定义 → 假失败。
**产物本身完全正常**（浏览器里 15 个图表全 setOption 成功），是校验器在误报。

**修复：按内容特征定位，不按序号。**

```js
const dataIdx = blocks.findIndex((b, i) => i > 0 && /(^|[\s;])var\s+DATA\s*=/.test(b));
const appIdx  = blocks.findIndex((b, i) => i > 0 && i !== dataIdx && /通用看板渲染器/.test(b));
```

同一次修复还加了**诊断输出**：找不到 DATA 块时直接打印各块开头的 40 字符，
下次块顺序再变也能一眼看出是哪一块。

> 通用教训：**校验脚本不许依赖"产物一定是 N 个块"**。
> 产物结构会随功能演进（本节就是被自己新增的装配功能打破的），
> 而校验器的定位逻辑必须比产物更稳。凡按 index/数量倒推的地方，都要换成特征匹配。

