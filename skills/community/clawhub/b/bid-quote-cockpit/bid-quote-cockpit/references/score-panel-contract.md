# 评分类看板固化契约（score_config.json / render_rules.json）

> 适用范围：看板里含「**评委打分 → 有效平均 → 综合评分 → 定标建议**」这条链路的项目。
> 本文件是这条链路的**唯一数据契约**。换门店、换供应商、换评委、换维度，只改 JSON，不改渲染代码。
> 若项目只有「纯价格比价」、没有评委打分类环节，**整套跳过**，看板不体现任何评分节。

---

## 0. 为什么需要「固化」

评委打分的原始做法是存在浏览器 `localStorage`。这条链路有**三个必踩的坑**：

| 坑 | 现象 | 根因 |
|---|---|---|
| origin 隔离 | 本地打开有分数，上传云端打开全空 | `file://` 与 `https://` 是不同 origin，localStorage 互不相通 |
| iframe 沙箱 | 云文档/嵌入式页面里 localStorage 被禁 | 第三方 Cookie/存储策略，`setItem` 直接抛异常 |
| 静态基线回退 | 别人电脑打开显示的是**另一套分数**（如「无人打分的静态评估基线」） | 页面探测不到打分数据 → 静默切回默认值 |

第三坑最危险：**不报错、不空白，只是显示一个看起来合理却错误的分数**。
所以定稿版一律把分数**烘焙进 HTML 字节**（`window.__SCORE_SEED__`），页面只读，任何设备一致。

---

## 1. `score_config.json`

```jsonc
{
  // —— 分数区块标题（用于面板文案，不要写具体门店/公司名）——
  "score_label": "评委最终打分",

  // —— 参与打分的单位（看板里的供应商；数量决定表格列数）——
  "vendors": [
    {"name": "供应商A", "code": "a", "short": "A"},   // short = 表头简称
    {"name": "供应商B", "code": "b", "short": "B"}
  ],

  // —— 打分维度：max 决定表头上限与校验范围；weight 用于加权（不需要加权时 = max）——
  "dims": [
    {"key": "履约能力", "code": "lvyue",   "max": 6, "weight": 6},
    {"key": "售后服务", "code": "shouhou", "max": 5, "weight": 5},
    {"key": "产品品质", "code": "pinzhi",  "max": 5, "weight": 5},
    {"key": "垫资能力", "code": "dianzi",  "max": 4, "weight": 4}
  ],

  // —— 评委岗位顺序（只影响默认岗位与表内顺序）——
  "roles": ["采购", "设计", "零售", "零售", "销售"],
  "max_judges": 5,

  // —— 打分时间（可空；仅作留痕，不显示为「会议日期」类措辞）——
  "scored_at": "2026-09-17T10:25:16.961Z",

  // —— 评委打分：字段名 = "<vendor.code>_<dim.code>"，值必须是 0~max 的整数 ——
  "judges": [
    {"role": "销售", "name": "评委甲", "a_lvyue": 5, "a_shouhou": 4, "a_pinzhi": 4, "a_dianzi": 4,
                                       "b_lvyue": 6, "b_shouhou": 5, "b_pinzhi": 5, "b_dianzi": 5},
    {"role": "采购", "name": "评委乙", "a_lvyue": 5, "a_shouhou": 4, "a_pinzhi": 5, "a_dianzi": 4,
                                       "b_lvyue": 5, "b_shouhou": 4, "b_pinzhi": 4, "b_dianzi": 4}
  ],

  // —— 综合分：价格分（业务侧算好，通常 = 满分 × 最低采用价 / 本单位采用价）——
  "price_score": {"供应商A": 60.00, "供应商B": 59.00},

  // —— 固定分项（经验 / 及时性 / 完整性 等**不打分**的项，直接给固定值）——
  //     其他分 = 固定分项 + 各打分维度的有效平均之和
  "other_fixed": {"供应商A": 17.5, "供应商B": 16.5}
}
```

### 校验规则（脚本启动即校验，不通过直接退出码 2）

| 规则 | 说明 |
|---|---|
| `vendors[].code` | 仅 `[A-Za-z][A-Za-z0-9_]*`，且互不重复 —— 它要拼进 JS 字段名 |
| `dims[].code` | 同上；`dims[].key` 互不重复 |
| `dims[].max` | 正数；打分值超出范围 → **该格置空并告警**，绝不截断成 max |
| 打分值 | 必须**整数**。小数（如 4.5）→ 置空 + 告警（宁可缺格，不可篡改） |
| 评委人数 | 偶数时告警（多数评审规则要求奇数）；但**不阻断**，仍按算术平均 |
| 缺格 | 某评委某格缺失 → 置空 + 告警；该格**不计入**有效平均的分母 |

> ⚠️ **不许"补齐"**：缺失/越界/小数的打分一律置空并列出告警，由人决定要不要补，
> 绝不自动填 max、填 0 或四舍五入。这是「只用原文数字」红线在打分场景的体现。

---

## 2. 有效平均与综合分的算法（唯一口径）

```
有效平均(单位, 维度) = 均值( 该格打分为 0~max 整数的评委，且该评委姓名非空 )
      · 无任何有效打分     → null（显示「—」，**不计入**分母，也不当 0 用）
      · 姓名空白的评委行    → 整行不参与（防止空行拉低均值）

其他分(单位) = 固定分项 + Σ 各打分维度的有效平均（null 视为 0，但**必须记录到 missing_dims**）
综合分(单位) = 价格分 + 其他分
名次         = 按综合分降序，1..N
```

**必须同时输出** `missing_dims`（哪些维度没有有效打分）。理由：某维度全缺时，
若静默按 0 计，该单位综合分会被压低却不留痕 —— 老板会以为它真的差。脚本把缺项写进
`score_panel.meta.json`，生成器据此在页面上给出提示。

---

## 3. 产物

| 文件 | 内容 |
|---|---|
| `score_panel.html` | 可直接插入看板的区块：CSS + 只读表 + 有效平均行 + 内联 seed JS |
| `score_panel.meta.json` | 评委数 / 各格有效平均 / 固定分项 / 综合分 / 名次 / 告警清单 |

`meta.json` 是给**主看板生成器**读的：9.3 综合评分表与首屏推荐卡不再自己算分，
而是直接取 meta 里的 `composite` / `rank_order`，避免两处算法跑偏。

---

## 4. 与主看板集成（**一步装配，不要事后注入**）

```bash
# 1) 先生成评分片段
python scripts/gen_score_panel.py --config ./score_config.json --out ./score_panel.html --report

# 2) 用 --score-panel 把片段交给主生成器装配（生成器内部完成 CSS/DOM/JS 三处嵌入）
python scripts/build_dashboard.py --config ./config.json --score-panel ./score_panel.html --out ./看板.html
```

`--score-panel` 的路径按 **`config.json` 所在目录**解析（与 `quotes` / `history` 同口径），
`--out` 也同理。拿不准就用绝对路径。

生成器内部完成三处触点装配：

| 触点 | 做法 |
|---|---|
| `<style>` | 片段 CSS 段（`.sp-*`）插在主 CSS 之后 |
| 9.3 综合评分表 + 首屏卡 | 分数/名次取 `meta.composite` / `meta.rank_order`；维度值取 `meta.effective_avg` |
| `<body>` 末尾 | 面板 DOM + seed 注入段；页面加载后分数即来自 `window.__SCORE_SEED__`，**不读不写 localStorage** |

### ⚠️ 绝对不要「事后再往 HTML 里塞片段」

想手动拼装的人一定会写类似 `re.search(r"<style[^>]*>", html)` 或 `html.find("</body>")` 去找锚点 ——
**这会静默失败**。原因是产物里**内联了压缩版 ECharts**，而 ECharts 的工具箱代码里有
`saveAsImage` 干函数，其字符串字面量中包含完整的 `</body>`、`<style>` 片段：

```js
// ECharts 源码里的字面量（示意）——它就是那个假锚点
w = '<body style="margin:0;"><img src="' + s + '" ... />'
          + '...</body>', S = window.open(); S.document.write(w)
```

一旦按字符串找锚点，就会命中这个**假锚点**，把面板 DOM 塞进 JS 字符串里 —— 结果：

- 文件字节数正常变大 ✅
- 页面完全不报错 ✅
- 搜索 `scorePanel` 也能搜到 ✅（在 JS 源码里）
- **但浏览器渲染出来根本没有评分节** ❌ → 校验器 10 项全 FAIL，且原因极难定位

所以**唯一正确路径是 `--score-panel`**。若确实需要脚本级拼装（例如为别的渲染链路做适配），
锚点必须建立在**已知唯一的结构标记**上，例如 `re.search(r"</title>\s*<style", html)`
（`</title>` 在 head 里只出现一次、且一定在真实 CSS 之前），并在装配后断言
「`id="scorePanel"` 的位置不在任何 `<script>…</script>` 区间内、且早于 `</body>`」。

### 页面必须满足的只读约束

1. 打分面板内**不得存在** `input` / `select` / `button` / `textarea`（校验器按数量 == 0 断言）。
2. 页面**不得写入**评分类 `localStorage` key（校验器扫描所有 key，含 `score|team|judge|rate` 即失败）。
3. 不得出现「保存打分」「导出打分码」「清空打分」等入口。
4. 文案必须写明「任何设备打开结果一致」，以及改分的正确路径（更新构建种子 → 重新生成 → 重新发布）。

---

## 5. 校验

```bash
# 生成
python scripts/gen_score_panel.py --config ./score_config.json --out ./score_panel.html --report

# 本地真机一致性（两个全新 user-data-dir = 两台电脑）
python scripts/verify_score_frozen.py ./看板.html --config ./score_config.json --log ./verify_score.log

# 线上产物一致性：先把线上**静态字节**下载成文件，再校验
curl -sL "<静态产物地址>" -o ./online_static.html
python scripts/verify_score_frozen.py ./online_static.html --config ./score_config.json --online
```

⚠️ **不要拿发布分享页的 URL 当产物**：分享页通常只是几 KB 的引导壳（含
`__PUBLISH_BOOTSTRAP__`），真实 HTML 在另一个静态域名下。校验脚本要在**真字节**上跑，
否则断言的是壳页、不是看板。

`--log` 里每一项都是「OK / FAIL + 实测值」，失败项集中列在末行。
退出码 0 才可交付。

### 关于「看板内没有评分节」

若被校验的看板是**纯价格比价版**（没有综合评分表、也没有首屏推荐卡容器），
脚本会打印一条 `--` 级说明并**跳过**综合分/名次断言 —— 这不是失败，
因为评分节本就是可选模块（见 `module-spec.md` 的条件模块说明）。

但要注意：**跳过 ≠ 通过**。若这个看板本应含评分节，说明
`render_rules.json` 的 `_selectors` 没指到正确的容器 id，或评分节根本没被渲染出来 ——
此时应检查选择器，而不是接受"通过"。

`_selectors` 可覆盖的键（默认值见脚本 `SEL_DEFAULT`）：

```json
{
  "_selectors": {
    "panel":      "#scorePanel, #teamPanel",
    "scoreTable": "#tScore, #scoreTable",
    "hero":       "#heroReco, #heroCards",
    "rulesBox":   "#scoreRulesBox, #rulesBox"
  }
}
```

写法：**逗号分隔的多个候选选择器**，脚本取第一个命中的 —— 这样同一套脚本
既能校验不同命名的看板，又不需要为每个项目改代码。

---

## 6. 改分流程（交付后）

```
1. 编辑 score_config.json 里对应评委的那一格
2. 重新跑 gen_score_panel.py（--report 核对综合分与名次变化）
3. 重新生成主看板 HTML（带 --score-panel 一起重跑）
4. 重新发布
5. 跑 verify_score_frozen.py --online 确认线上字节已更新
```

**不要**在页面上留任何后门去改分 —— 一旦开了口子，「任何设备一致」这个保证就没了。
