---
name: bid-quote-cockpit
description: 通用投标报价对比分析驾驶舱。适用于新门店/新项目收到多家供应商报价（支持多轮回标/澄清后报价），需快速产出「总价排名 + 分部分项横向对比 + 单方造价 + 异常报价核查 + 勾稽校验 + 评分定标 + 行动清单」自包含交互式 HTML 看板的场景，并可直接上线发布（云端 Page / 公开链接）。支持条件模块：历史门店数据、评委打分与定标结论均由使用者**可选**提供（提供才渲染对应节）；评委打分一经提供即**固化进 HTML 字节**，任何人任何设备打开结果一致，页面只读不可改。
agent_created: true
---

# 投标报价对比分析驾驶舱（Bid Quote Cockpit）

把「一堆报价表」变成「一份可决策、可发布、可复用的看板」。本技能**不含任何具体门店或公司名称**，全部由使用者提供的配置驱动；换门店、换供应商、换货币、换分项结构、换评委都不需要改代码。

## 定位与边界

| 场景 | 用本技能 | 改用 |
|---|---|---|
| 多家供应商报价 → 横向比价 + 看板 | ✅ | |
| 多轮回标（首轮 / 二轮 / 澄清后）对比 | ✅ | |
| 评委打分 → 有效平均 → 综合评分 → 定标建议 | ✅ 见「评分与定标链路」 | |
| 看板要发给别人看 / 需固定在线链接 | ✅ 见 `references/publish-and-verify.md` | |
| 某家澄清后修订价回灌既有对比表 | ➖ 核心回灌流程 | `bid-quote-clarification-sync` |
| 填制「商务标分析表」/ 串标特征识别 | ➖ | `bid-price-analysis` |
| 两表逐项机械对比 | ➖ | `excel-quote-compare` |
| 同批供应商 × 多个子项目并置（不做跨项目合计） | ➖ | `multi-project-quote-board` |

> 本技能与 `bid-quote-clarification-sync` 互补：澄清回灌负责**修数据**，本技能负责**出看板**。两者共用同一套「只用原文数字」红线。

---

## 快速开始（3 步）

```bash
SK=~/.workbuddy/skills/bid-quote-cockpit

# 1. 复制配置模板，填入项目信息（门店/供应商/轮次/分项都在这里改）
cp $SK/scripts/config.example.json  ./config.json

# 2. 生成看板（读 config.json + quotes.json [+ history.json]）
#    out 为相对路径时，按 config.json 所在目录解析（不是 cwd），产物不会乱落
python $SK/scripts/build_dashboard.py --config ./config.json --report

# 3. 交付前必跑校验①：语法门禁 + 桩化运行时冒烟 + NaN 扫描
node $SK/scripts/verify_dashboard.js ./报价分析看板.html
# 第 3 道：静态查「Python 常量名泄漏进 JS」（运行时会静默中断后续全部渲染）
python scripts/lint_py_const_leak.py ./build_dashboard.py ./报价分析看板.html

# 4. 交付前必跑校验②：版式溢出体检（内容是否超出页面/卡片范围）
python $SK/scripts/check_overflow.py ./报价分析看板.html 1500,1280,1100
```

校验输出 `✅ JS 执行无异常 / 图表已 setOption: [...] / 内容为空的容器: 无 (OK) / 含 undefined|NaN 的容器: 无 (OK)` 且 exit 0，**并**第二道校验输出 `✅ 无横向溢出` 且 exit 0，才可交付。两道校验互不覆盖：前者查运行时，后者查版式。

**交付前 5 条文案自检**（脚本查不了，必须自己过一遍，否则容易交付"上一版残留"）：

```python
H = open(html, encoding="utf-8").read()
assert "名义·不完整" not in H        # 本次若有整包价有效报价，不应再出现
assert ("剔除后" in H) == (facade_cat_key is not None)   # 未设剔除项时不得出现
assert "cNoFac" in H == (facade_cat_key is not None)
# 有 history 时：'cHistSq' in H 且 '过往项目单方均值' in H
# 有 addenda 时：'附录 A' in H
```

---

## 第一步：收集输入（数据契约）

本技能吃 **3 个文件**，其中历史数据是可选的。

| 文件 | 必需 | 内容 |
|---|---|---|
| `config.json` | ✅ | 项目元信息、供应商清单与配色、轮次口径、模块开关、文件路径 |
| `quotes.json` | ✅ | 各家各轮的总价、分项小计、逐条明细（**单一真相源**） |
| `history.json` | ⬜ 可选 | 历史门店数据。**不提供 → 看板不出现任何历史对比** |

字段级规格见 `references/data-contract.md`（含最小可运行示例与字段校验规则）。

### 从 Excel 抽取数据

使用者通常给的是 Excel/PDF 报价表。抽取时**必须保留原文数字**，禁止任何推算：

```bash
# 用技能自带的归一化/统计工具做清洗与自检
python $SK/scripts/normalize_quote.py --in raw_quotes.json --out quotes.json --report
```

该工具负责：描述级匹配（多轮对照）、零单价逐条重算、分项求和 vs 原文总价勾稽、小计行剔除。详见 `references/pitfalls.md`。

---

## 第二步：模块开关（含历史数据这一开放选项）

看板共 9 节，**条件模块未满足时整节不渲染**（不留空白占位、不写"暂无数据"凑数）。

| 节 | 模块 | 出现条件 |
|---|---|---|
| 一 | 报价总览表 | 必选（各家 × 各轮 × 方案价/优惠价） |
| 二 | 供应商报价概况 | 必选（指标速览带 + 报价标尺 + 卡片网格 三种形式） |
| 三 | 总价 / 单方 / 剔除后对比 | 必选；「剔除后」需 `facade_cat_key` 命中 |
| 四 | 分部分项横向对比 | 必选（各轮 × 金额/单方，N 柱 + 均值线） |
| 五 | 分项明细逐条对比 | 需 `items` 明细非空 |
| 六 | 异常报价专项核查 | **需存在零单价/疑问/未报价条目**；全部正常则整节跳过 |
| 七 | **历史对比** | ⬜ **需 `history.json` 非空**；7.1 分项对比需历史门店**有分项拆分**，否则 7.1 不渲染、只保留 7.2 单方对比（含**过往均值线**） |
| 八 | 勾稽校验 | 必选 |
| 九 | 行动清单 | 必选 |
| 附录 A | 清单外增项核查 | ⬜ 需 `quotes.json` 里有 `addenda`（供应商以邮件/另表补充、不在 BOQ 内的报价项） |

### 整包价单位（`noBreakdown`）

某家只给**整包总价 + 书面 Included/Excluded 范围说明、不给逐条拆分**时（常见于店中店/快闪店短工期项目）：

- **它是有效报价**，不是"报价不完整" —— 只要给出明确总价与范围声明，就 `"complete": true` + `"status": ""`，正常计入排名。
- 在该供应商对象里加 `"noBreakdown": true`。效果：① 总价/单方（第二、三节）照常参与；② 第四、七节分项图**不含它**（避免 0 柱被读成"该项报价 0"）；③ 它的「分项求和 vs 采用价」勾稽转成**口径说明（已注明）**而非 ✗ 差异；④ 不拉低本项目分项均值。
- 它的 `cats` 仍须填满 `ncat` 个 0（长度校验），但**不要**把 0 当作"已含"来解读。
- 它的范围差（Excluded 项）用**其他家原文数字求和**量化，写进 `notes`，属透明算术。

### 清单外增项（`addenda`）

供应商邮件另附、不在 BOQ 内的报价（如西班牙法定的电气合法化+OCA、安全协调员、安全计划、分包台账等），在 `quotes.json` 里加：

```jsonc
"addenda": [{
  "vendor": "供应商名", "title": "…", "source": "邮件附件文件名",
  "items": [{"no":1,"desc":"原文条目","desc_cn":"中文","sub":"子行","amount":4800,
             "mandatory":"法定强制","basis":"法规依据","verdict":"必要性判定","flex":"高"}],
  "subtotal_printed": 10320, "vat_rate": 0.21, "vat": 2167.2, "total": 12487.2,
  "sum_unit_col": 10500,          // 逐项相加（与原文小计不一致时必填，用于暴露其内部勾稽问题）
  "reconcile_note": "…", "conclusion": "…", "impact": "…"
}]
```

看板渲染为**附录 A**（不动 9 节编号），含 A.1 指标带 / A.2 逐项核查表 / A.3 结论与处理建议；同时自动进第九节行动清单（P0 澄清 + P0 对齐四家口径）。

> ⚠️ **口径纪律**：法定合规义务的责任主体是**施工承包单位本身**，不是业主漏项。结论必须写"要求四家在同一口径下各自含入或书面声明不含"，而不是把某一家的加价当作既定增项照收。原文小计与逐项相加不一致时，**照原文列示并标注差额**，不自行更正。

### 历史数据：必须显式询问使用者

**开工前先问一句**（这是开放选项，不要替使用者决定）：

> 是否需要把本次报价与历史门店做对比？如需要，请提供历史数据清单，每条包含：
> **门店/项目名称、建筑面积(㎡)、总报价、**以及（可选）**按相同分项拆分的小计金额**。
> 只有单方造价(€/㎡)而无分项拆分也可以，此时仅参与单方对比，不参与分项对比。
> **若不提供，看板中将不体现任何历史对比内容。**

- 提供 → 填 `history.json`，第七节出现（分项金额对比 + 单方对比 + 历史均值线），且第四节出现「历史均值线」、第二节指标带出现「历史单方均值」格。
- 不提供 → `config.json` 里 `"history": null`（或干脆没有 `history.json`）。此时：
  - 第七节**整节不渲染**；
  - 第四节**不画**历史均值线，图例与说明同步消失；
  - 第二节指标带**不出现**历史单方均值格；
  - 全文不出现「历史」「过往」字样。

模板见 `examples/history.json`（含"有分项"与"仅单方"两类条目，可直接删改）。

### 可直接跑的示例（脱敏，无真实门店/供应商名）

`examples/` 下有成套示例，**4 家供应商（A/B/C/D）× 8 个分项 × 首轮+二轮**，其中 C 家含零单价疑问项、D 家无二轮报价，用于演示完整性标注与沿用首轮补位：

```bash
cd ~/.workbuddy/skills/bid-quote-cockpit/examples
python ../scripts/build_dashboard.py --config config.json                  # → demo.html                （提供历史：9 节 / 15 图）
python ../scripts/build_dashboard.py --config config_without_history.json  # → demo_without_history.html（不给历史：8 节 / 10 图）
```

对比打开两个 `demo_*.html` 即可直观确认：**不给历史时，第七节整节消失，第四节历史均值线与第二节历史单方均值格同步消失，全文无「历史 / 过往」字样**（仅保留一句"本次未提供历史门店数据"的说明）。

---

## 第三步：生成与交付

1. 跑 `build_dashboard.py` 生成 HTML（**echarts 内联**，产出即离线自包含单文件，无外部依赖）。
2. 跑 `verify_dashboard.js` 校验，必须 exit 0（**查的是"JS 能不能跑、图能不能画、有无 NaN"**）。
3. 跑 `check_overflow.py` 做**版式溢出体检**，必须 exit 0（**查的是"内容有没有超出页面/卡片范围"**，与上一步互不覆盖，两个都要跑）：
   ```bash
   python $SK/scripts/check_overflow.py ./报价分析看板.html 1500,1280,1100
   ```
   判读：`PAGE_SCROLL=0` + `BEYOND_WRAP=0` + **`CLIPPED=0`**。
   - `CLIPPED` = 内容被「人为高度上限」裁掉（如 `.tblwrap{max-height:420px}` 遇到超高表格），
     溢出部分只有滚动才看得到，**截图与打印一律丢失**，典型受害行是「合计 / 综合总分」。
     这是**纵向**裁切，旧的三个横向指标一个都命不中 —— 详见 `references/pitfalls.md` §15。
   - `SCROLLABLE>0` 只是信息项（某容器内部横滚，仍可看到），`--strict` 可把它也当失败。这个检查专抓"表格里有整段文字（法规依据/条款原文/长描述）被 `td{white-space:nowrap}` 撑破卡片"这类版式事故——**曾因漏检此步被使用者退回**（原话"显示出现重大失误，已经超出页面范围"）。成因与修复见 `references/pitfalls.md` §10。
4. 跑 `dump_rendered.py` 做**渲染级「单位↔金额」配对断言**，必须 exit 0
   （**查的是"客户端 JS 现拼的文案里，单位名有没有配错金额"**）：
   ```bash
   python $SK/scripts/dump_rendered.py ./报价分析看板.html --rules render_rules.json --log gate.log
   ```
   ⚠️ 前三道**都拦不住这一类**：`node --check`/`verify_dashboard.js` 只看能不能跑、有无 NaN；
   `check_overflow.py` 只看版式；`lint_py_const_leak.py` 只看常量泄漏。而 `grep` 也查不到 ——
   千分位是客户端 `fmt()` 现拼的，源码里只有裸数字。规则写法与实盘案例见 `references/pitfalls.md` §14。
5. 用 Chrome headless 截图抽查长图渲染（可选但推荐）：
   ```bash
   chrome --headless --disable-gpu --screenshot=./shot.png --window-size=1500,6000 ./报价分析看板.html
   ```

### 交付约定
- **默认只交付 HTML，不主动生成/同步 PDF**（除非使用者明确要求）。要 PDF 时用 Chrome headless 渲染，且**先写临时文件名再 `cp` 覆盖**主文件（预览锁定会 0x5 拒绝）。
- 若使用者要求托管到资料库云端：先过图片托管自检（无第三方 `<img>` 外链），再 `import_html.py --node-block-id <节点>` 覆盖同步。**完整发布与线上核验手册见 `references/publish-and-verify.md`（含"分享链接只是壳页""版本号会递增""双档案一致性"三个必修点）。**

---

## 评分与定标链路（可选）：评委打分 → 有效平均 → 综合评分 → 定标结论

当评审规则里含**人工打分**时启用。若项目是纯价格比价、无评委环节，**整套跳过**，看板不出现任何评分节。

**契约与算法见 `references/score-panel-contract.md`（唯一口径，改分流程也在那里）。**

### 核心原则：打分必须**固化**，不能让它在浏览器里活着

老做法把打分存 `localStorage`。三个坑：① `file://` 与 `https://` 是不同 origin，本地有分、云端全空；
② 云文档在 iframe 沙箱里，`setItem` 可能直接抛异常；③ 探不到分就**静默回退到静态基线** ——
不报错、不空白，只是显示一个看起来合理却是错的分数（最危险）。

**定稿做法**：分数**烘焙进 HTML 字节**（`window.__SCORE_SEED__`），页面只读，任何设备一致。

```bash
SK=~/.workbuddy/skills/bid-quote-cockpit

# 1. 由业务侧确认好评委 × 维度 × 单位的分数，写进 score_config.json
cp $SK/examples/score_config.example.json ./score_config.json

# 2. 生成打分区块 + 元数据（--report 打印综合分、名次、缺项告警）
python $SK/scripts/gen_score_panel.py --config ./score_config.json \
       --out ./score_panel.html --report
#    → score_panel.html     评分区块片段（CSS + 只读表 + 内联 seed）
#    → score_panel.meta.json  各格有效平均 / 综合分 / 名次 / 告警（供主看板取数）

# 3. 生成主看板时用 --score-panel 一步装配（⚠️ 路径按 config.json 所在目录解析）
python $SK/scripts/build_dashboard.py --config ./config.json \
       --score-panel ./score_panel.html --out ./看板.html

# 4. 交付前必跑：固化一致性真机校验（两个全新浏览器配置 = 两台电脑）
python $SK/scripts/verify_score_frozen.py ./看板.html --config ./score_config.json \
       --log ./verify_score.log
```

### ⚠️ 装配只能靠 `--score-panel`，**不要事后再往 HTML 里注入**

产物里内联了**压缩版 ECharts**，而 ECharts 的 `saveAsImage` 干函数中有一个字符串字面量
包含完整的 `</body>`、`<style>` 片段。因此 `re.search("<style")` / `html.find("</body>")`
这类"找锚点"的写法会命中**假锚点**，把面板塞进 JS 字符串：

- 文件变大 ✅、页面不报错 ✅、能搜到 `scorePanel` ✅（在 JS 源码里）
- **但渲染出来没有评分节** ❌ —— 校验器 10 项全 FAIL，且极难定位

正确路径就是生成器的 `--score-panel`（内部按结构顺序嵌入，不靠字符串匹配）。

### 评分节是可选模块（跳过 ≠ 通过）

纯价格比价版看板**没有**评分节时，`verify_score_frozen.py` 会打印 `--` 级说明并跳过
综合分/名次断言 —— 这不是失败。但若这个看板**本应含评分节**，说明 `render_rules.json`
的 `_selectors` 没指到正确容器 id（或用错了示例文件）。**跳过不能当通过读**。

```json
{ "_selectors": {
    "panel": "#scorePanel, #teamPanel",
    "scoreTable": "#tScore, #scoreTable",
    "hero": "#heroReco, #heroCards",
    "rulesBox": "#scoreRulesBox, #rulesBox" } }
```

### 三条不可协商的规则

| 规则 | 内容 |
|---|---|
| **页面只读** | 打分面板内 **0 个** `input/select/button/textarea`；不写入任何评分类 `localStorage`；不提供「保存/导出打分码/清空」入口。校验器按「控件数 == 0」与「无评分类 key」硬断言 |
| **脏数据置空，不许补齐** | 打分缺失 / 越界 / 非整数 → 该格**置空**并逐条告警，**绝不**自动填 max、填 0 或四舍五入。这是"只用原文数字"红线在打分场景的体现 |
| **缺项要留痕** | 某维度全无有效打分时按 0 计入，但**必须记入 `missing_dims`** 并在页面提示。静默压分会让人误以为该单位真的差 |

### 改分流程（交付后，唯一路径）

```
改 score_config.json 里的那格 → 重跑 gen_score_panel.py → 带 --score-panel 重新生成看板 → 重新发布 → verify_score_frozen --online 复核
```

**不要**为了"方便"在页面上留改分后门 —— 一旦开口子，「任何设备结果一致」这个保证就失效了。

---

## 上线发布与线上核验

交付链接时**只给一个最终链接**，并附上核验结论。关键要点（完整版见 `references/publish-and-verify.md`）：

1. **发布前硬门**：无第三方 `<img>` 外链、无 CDN 外链（ECharts/前端 SDK 一律**内联** —— 国内网络与微信内置浏览器取不到 CDN）、磁盘字节数 == 生成时打印的字节数。
2. **分享链接 ≠ 产物**：发布返回的 URL 通常只是几 KB 的**引导壳**（含 `__PUBLISH_BOOTSTRAP__`），真实 HTML 在另一个静态域名下、**版本号递增**。核验必须**下载真字节**再断言，否则你校验的是壳页。
3. **线上必须重跑固化一致性**：`verify_score_frozen.py ./online_static.html --config ./score_config.json --online`。客户端 JS 现算的数字（分数/名次/千分位）grep 不到，只能渲染断言。
4. **双档案是唯一真答案**：两个**全新** `--user-data-dir` 结果一致，才证明"换台电脑不会变"。同一 profile 跑两次证明不了任何事。

---

## 红线（所有环节，不可协商）

1. **只用报价文件原文数字**。禁止推算、补全、"同口径估算"。确需推算（如总价÷面积=单方）属**透明算术**，允许但必须在页面上标注公式。
2. **口径全程统一**：含税/不含税二选一并贯彻始终；跨项目对比一律**不含税**。原文未标税率 → 显示"待确认"，不自作主张。
3. **三态规则**（易错）：有报价+有税率=数字 ／ 有报价+无税率=**待确认** ／ 无报价=**暂无报价**。严禁混用。
4. **名义最低价必须显式标注**：某家数字最低但**报价不完整**（大量零单价/缺项/空表）时，排序一律加「名义·不完整」，并同时给出**有效可比排名**（只含完整报价单位）。绝不为给老板一个"最低价"而隐去完整性问题。
   - **反向也成立**（2026-09-14 教训）：某家**给了整包总价 + 书面 Included/Excluded 范围说明**、只是没做逐条拆分时，**不算不完整** —— 必须作为有效报价计入排名。不要把"未拆分"误当作"报价无效/名义价"。范围缺口单独作为 `notes` 说明，不据此剥夺其排名资格。
5. **中间产物 JSON 的统计字段不可直接采信**（如 `zero_count` 可能算错）。凡零单价、条目数、完整性占比一类统计，**一律回到 `items` 逐条重算**。
6. 多轮对比时**保留首轮列不删除**，二轮在旁边新增列；无二轮报价的单位沿用首轮价参与排名并标注，不静默剔除。

---

## 定标建议模块（可选）：满足工期前提下，价格最低优先

当使用者要求给出定标建议、或项目有明确的开业/安装目标日时启用本节。**判定逻辑必须唯一、可复算，不要把工期、价格、口径可信度混在一张表里讲**（2026-09-12 用「方案 A/B/C 矩阵」的写法被明确否掉，理由是"很乱"）。

### 三条判定规则（缺一不可）

| 规则 | 内容 |
|---|---|
| ① 起算日 | **统一按一个明确日期起算**（如「自 2026-09-15 起」），不沿用各家自报的不同起算点 |
| ② 工期门槛 | 各家所报工期自起算日推算，能在**截止日**（如 2026-10-31）前完成 → **满足工期**；不能 → 列入**「需请对方澄清」**（澄清能否压缩），**不是直接淘汰** |
| ③ 定标原则 | **在满足工期的候选中，报价最低者优先** —— 工期是门槛，价格是排序键 |

数据层建议留三个常量 + 一个函数，便于复算与改口径：`LEAD_START`（统一起算日）、`LEAD_DEADLINE`（完成截止日）、`LEAD_SPAN[{sup: {pid: 天数}}]`（各家自起算至完成的**总**天数，严格取自其报价原文）、`lead_result(sup, pid) → {days, est, ok}`。

### 三个易错点

1. **绝对日期排期者不顺延**：某家若给的是绝对日期排期（如「工程开发 9/10 起 → 安装 10/26–10/30」），其自身起点可能**早于**统一起算日，此时完成日按其原排期固定，**不可**用「统一起算日 + 天数」再算一遍（会得出错误结论）。
2. **只有相对工期者才平移**：给「N 周 / N 天」的家，才用 `统一起算日 + N 天` 推算完成日。
3. **最低价 ≠ 可定标**：新口径下经常出现「原最低价因工期超期被排除」——这正是本模块的价值所在，务必在结论里显式点出来，避免使用者误以为排名没变。

### 两个必备呈现

- **概览/回标状态表必须同时含「报价」与「所报工期 → 完成日」**，不能只有价格。列结构建议：`供应商 / 状态 / 回标日期 /〔项目A 报价 + 项目A 工期→完成日〕/〔项目B 报价 + 项目B 工期→完成日〕/ 合计`；工期格用 ✓满足 / ✗超期 双色，并加脚注说明起算日、截止日与「绝对日期不顺延」的例外。
- **定标建议节固定六段式**（顺序不要变）：
  1. 判定规则三条（起算日 / 门槛 / 原则）
  2. 工期满足性判定表（每家 × 每项目：天数、工期依据原文、完成日、✓/✗）
  3. 满足工期的候选 —— **按报价排序**（①②③…，首推行高亮）
  4. 定标推荐结论（每项目一张推荐卡 + 合计金额 + 备选方案及合计）
  5. 需请对方澄清（工期不满足者：完成日、超出天数、拟澄清事项）
  6. 定标前置条件（口径澄清、排期自洽、起算日统一定义、交付地等）

---

## 设计惯例（速查，详见 references）

- **配色**：莫兰迪低饱和多彩，商务活泼。钢蓝 `#3E6E9E` / 赭石 `#B5791F` / 雾青 `#3E8E80` / 紫灰 `#8B7FA8` / 琥珀 `#C99245`。**禁用纯粉、纯红、高饱和霓虹**。供应商配色由浅（首轮）/深（二轮）两档表达轮次。
- **成本涨降配色**：上涨=琥珀橙，下降=雾青绿（成本语境，与股市红涨绿跌相反，不冲突）。
- **核心模块须 ≥3 种互补呈现形式**（指标带 + 横向标尺 + 卡片网格），避免满屏卡片的呆板感。
- **基准线分两类**：总额级（不同城市/面积的历史金额均值）**不可比，不画**；分项级（同一分项工程量级）**可比，可画**。

完整规范见 `references/design-conventions.md`，数据陷阱见 `references/pitfalls.md`，各节字段级规格见 `references/module-spec.md`。

---

## 技能内文件地图

| 文件 | 作用 |
|---|---|
| `scripts/build_dashboard.py` | 主生成器（配置驱动，出 9 节看板 HTML；`--score-panel` 装配评分区块） |
| `scripts/gen_score_panel.py` | **评分区块生成器**（评委打分固化，出只读表 + seed + meta） |
| `scripts/verify_score_frozen.py` | **固化一致性真机校验**（双全新档案 = 两台电脑，本地/线上通用） |
| `scripts/verify_dashboard.js` | 语法门禁 + 桩化运行时冒烟 + NaN 扫描 |
| `scripts/check_overflow.py` | 版式溢出体检（`PAGE_SCROLL` / `BEYOND_WRAP` / `CLIPPED`） |
| `scripts/dump_rendered.py` | 渲染级「单位 ↔ 金额」配对断言 |
| `scripts/lint_py_const_leak.py` | 查 Python 常量泄漏进 JS（会静默中断后续渲染） |
| `scripts/normalize_quote.py` | 报价数据归一化 / 统计自检 |
| `references/data-contract.md` | `config.json` / `quotes.json` / `history.json` 字段级契约 |
| `references/score-panel-contract.md` | **`score_config.json` 契约 + 有效平均算法 + 改分流程** |
| `references/publish-and-verify.md` | **上线发布与线上核验手册（含缓存/壳页/版本陷阱）** |
| `references/module-spec.md` | 各节出现条件、数据源、呈现形式、易错点 |
| `references/pitfalls.md` | 全部实盘踩坑记录（含判据、根因、修复） |
| `references/design-conventions.md` | 配色 / 版式 / 图表规范 |
| `examples/` | 全套脱敏示例（可直接跑） |

## See Also
- `bid-quote-clarification-sync`（澄清/修订价回灌）
- `bid-price-analysis`（商务标分析表 / 串标识别）
- `excel-quote-compare`（两表逐项对比）
- `multi-project-quote-board`（同批供应商 × 多子项目并置，不做跨项目合计）
