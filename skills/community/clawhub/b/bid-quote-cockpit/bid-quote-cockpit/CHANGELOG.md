# 版本记录（CHANGELOG）

## v1.0 — 2026-09-23

首个可分发版本。把「多家供应商投标报价 → 可决策看板 → 上线发布」的全过程沉淀为
配置驱动的通用技能，**不含任何真实门店 / 公司 / 供应商 / 评委名称**。

### 能力范围

| 模块 | 说明 |
|---|---|
| 报价总览 / 概况 / 单方造价 | 多轮（首轮 / 二轮 / 澄清后）并列对比，采用价排名 |
| 分部分项横向对比 | 类别 × 单位矩阵 + 均值线（含与历史项目对比） |
| 逐条明细对比 | 需提供 `items` 明细才渲染 |
| 异常报价专项核查 | 需存在零单价 / 疑问项才渲染 |
| 勾稽校验 | 分项求和 vs 原文总价 |
| **评委打分（固化）** | 打分烘焙进 HTML 字节，任何设备结果一致、页面只读 |
| **综合评分与名次** | 价格分 + 固定分项 + 打分维度有效平均 |
| 定标建议 | 工期门槛 + 最低价优先（选项模块） |
| 行动清单 / 附录 A | 待澄清事项、清单外增项核查 |
| 上线发布 | 云端 Page + 公开链接，含线上真字节核验 |

### 条件模块（数据不足则整节不渲染，不留空占位）

- 历史对比 → 需 `history.json`
- 逐条明细 → 需 `items`
- 异常核查 → 需存在零单价 / 疑问项
- 附录 A → 需 `addenda`
- 评分与定标 → 需 `score_config.json`

### 校验工具

| 脚本 | 查什么 | 必须 |
|---|---|---|
| `verify_dashboard.js` | JS 能否跑、图能否画、有无 NaN | ✅ |
| `check_overflow.py` | 版式溢出 / 内容被裁切 | ✅ |
| `lint_py_const_leak.py` | Python 常量泄漏进 JS | ✅ |
| `dump_rendered.py` | 渲染后「单位 ↔ 金额」配对 | ✅ |
| `verify_score_frozen.py` | **固化一致性（双全新档案 = 两台电脑）** | 含评分节时 ✅ |

### 本版修复

- **评分区块改为一步装配**：`build_dashboard.py` 新增 `--score-panel`，生成时直接嵌入
  片段（CSS / DOM / JS 三处），不再需要事后手工往 HTML 里注入。
  背景：产物内联的压缩版 ECharts 源码里含 `</body>`、`<style>` 字符串字面量
  （来自 `saveAsImage` 干函数），按字符串找锚点会命中**假锚点**把面板塞进 JS ——
  文件变大、不报错、却渲染不出来，10 项断言全 FAIL 且极难定位。
  已在 `SKILL.md`、`references/score-panel-contract.md`、`references/pitfalls.md §17` 写明此坑。
- **`verify_dashboard.js` 改用内容特征定位 DATA / app 块**：原先按 `blocks[n-2]` / `blocks[n-1]`
  取，一旦主生成器装配了额外 script 块（如评分注入段），DATA 就会被误当成 app 去执行 →
  报 `DATA is not defined` 假失败。现在按 `var DATA=` 与渲染器特征串定位，块数变化不影响。
- 评分脚本支持 `_selectors` 多候选选择器，一套脚本适配不同命名的看板；
  纯价格比价版（无评分节）自动跳过综合分/名次断言，并明确提示「跳过 ≠ 通过」。
- 修复 `lint_py_const_leak.py` 的 docstring 转义告警。
- 全量脱敏：历史案例改用「甲公司 / 乙公司 / 丁公司」代称，教学价值保留。

### 已知边界

- 装配路径（`--score-panel` / `--out`）按 **`config.json` 所在目录**解析，
  与 `quotes` / `history` 同口径；跨目录调用请用绝对路径。
- 真机校验依赖 Chrome；未找到 Chrome 时直接判失败（不静默跳过）。
- 打包内 `examples/demo.html` 是**纯价格比价版**，不含评分节；
  要连评分一起看效果，用 `--score-panel` 重跑一次即可：
  `python ../scripts/build_dashboard.py --config config.json --score-panel demo_score_panel.html`
