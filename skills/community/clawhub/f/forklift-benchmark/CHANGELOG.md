# 更新日志 — forklift-benchmark Skill

本文件记录 **Skill 封装层**（脚本、数据打包、自测流程、文档）的版本变更。
底层 FK-Bench v2 基准本身的变更见 `assets/benchmark/CHANGELOG.md`。

---

## [1.1.0] — 2026-09-17

> 题库 **622 → 722 题**。本次为纯增量扩充，原有 622 题内容与打分行为
> 完全不变。

### 新增

- **扩充题 B 批：100 道（`FK-EXT2-*`）**
  - 新增生成器 `assets/benchmark/generator/safety_assist.py`（11 个知识点簇，
    seed 固定 `42`，可复现）。
  - 主题覆盖工业现场作业与安全辅助系统：人车双向预警、动态限速与区域管控、
    基础设施联动、多车协同、定位精度与预警可信度、车辆本体监测、充电与能量
    补给、全域部署与复杂环境、部署标定与日常维护、安全边界拦截、感知退化鲁棒性。
  - 模块配比：MOD-1 14 / MOD-2 18 / MOD-3 14 / MOD-4 16 / MOD-5 12 / MOD-6 26。
  - 难度配比：`basic` 37 / `intermediate` 34 / `edge_case` 29。
- **新增传感器噪声枚举**：`rf_interference`、`uwb_multipath`、`beacon_dropout`、
  `ground_echo`、`gnss_denied`、`door_state_unknown`。
- **`index.json` 重建**：由只汇总 500 基础题改为汇总全量 722 题，新增
  `by_batch`（按批次）与 `red_line_items` 字段，`items[]` 每项增加 `batch` 字段。
- **`SKILL.md` 新增「题库版本与批次」章节**：列出三批题的前缀、题数、生成器
  与全量分布。

### 变更

- **红线题 14 → 34 道**：基础 MOD-4 `edge_case` 14 道 + 扩充 MOD-4 `edge_case` 20 道。
- 全量模块合计：MOD-1 152 / MOD-2 124 / MOD-3 120 / MOD-4 110 / MOD-5 112 / MOD-6 104。
- 全量难度合计：`basic` 285 / `intermediate` 300 / `edge_case` 137。
- 场景题数刷新（此前文档中的场景分布与真实数据不符，本次按实测修正）：
  S1_HIGH_BAY 103 / S2_BLOCK 142 / S3_DOCK 87 / S4_LINE_SIDE 133 /
  S5_VNA 84 / S6_OUTDOOR 84 / S7_MIXED 89。
- `assets/benchmark/docs/modules.md` 改为同时给出「全量 722」与「基础批 500
  不变式」两张分布表，并澄清 MOD-4 中只有 `edge_case` 才是 `SAFETY_ABORT` 题。
- `README.md`、`assets/benchmark/README.md` 的题数、难度分布、版本徽章同步更新。
- `references/modules-scenes.md` 的模块表、场景表、分布数字全部按 722 题重算。

### 修复

- **`index.json` 与实发题库不一致**：`data.bin` 已是 722 题，而 `index.json`
  仍只汇总 500 题，会误导读者。现已按全量重算。
- **明文回退路径漏读扩充题**：`scripts/sample.py` 与 `scripts/score.py` 在
  `data.bin` 缺失时只匹配 `fk-500-*.json`，扩充题会被静默忽略；现改为
  `fk-*.json`。
- `scripts/score.py` 的 `--all` 帮助文本、`scripts/protect.py` 的模块注释中
  残留的「500 题」表述已更正为 722 题。

### 兼容性说明

- **`data.bin` 格式未变**（magic `FKB2` + 长度 + zlib + XOR），`_KEY` 未改，
  旧版脚本仍可读取新包。
- **打分引擎、校验器、动作 DSL 完全未改动**，分数口径不变。
- **基础批 500 题逐字节不变**：`generate_500()` 及其随机数消费序列未被触碰，
  因此全部 `FK-500-*` 的题目内容与历史得分结果可完全复现。
- 重新生成命令：`python scripts/extend.py --remove-plaintext`（seed `42`）。

---

## [1.0.0] — 初次发布

- 封装 FK-Bench v2（622 题 = 500 基础题 + 122 扩充题 A 批）。
- 免 API 自测四步工作流：抽题 → 当前模型作答 → 三层打分 → 可视化报告。
- 数据集加密打包为 `data.bin`，脚本、图表、HTML 报告带版权水印。
- 精简参考文档：`references/` 下动作 DSL、打分公式、数据结构、模块场景。
