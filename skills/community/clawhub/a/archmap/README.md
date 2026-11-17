# ArchMap 架构测绘 Agent

终端原生架构测绘技能（Harness 生态 Agent），无 Web 界面。对目标项目做静态源码分析，生成架构基线与全套文本报告，并支持增量影响面分析、变更同步与行级 diff 影响面，实现精准开发、节约 tokens。

## 一、简介与能力矩阵

引擎包 `archmap_agent` 已随技能自包含分发（与包装脚本同目录），五种模式：

| 模式 | 一句话说明 |
|------|-----------|
| full 全量分析 | 全量扫描源码，生成完整架构基线（`full_index.json`）与 01~09 号 Markdown/Mermaid 报告 |
| lite 极简增量 | 日常迭代默认：只做变更检测 + 变更模块局部重解析 + 台账留痕，秒级完成，不重生成全量报告 |
| sync 同步更新 | 检测源码变更、合并回基线并重生成 01~09 全套报告，附带召回验证与 ETL 产物回填 |
| diff 影响面 | git 无关的行级快照比对：输出精确变更行区间、导入闭包、测试选择（`diff_impact.json`），并留痕变更历史 |
| 增量影响面 | 需求文本向量化匹配模块，叠加路由闭包/关键词硬匹配召回补强，产出 `precise_analysis.json` 精准定位文件/函数/路由 |

## 二、安装

```bash
cd /Users/xujin/.agents/skills/archmap
pip3 install -r requirements.txt
```

依赖分组（见 `requirements.txt`）：

- **必需**：`PyYAML` / `numpy` / `scipy`——full/lite/sync/diff 纯算法模式都依赖。
- **可选**：`sentence-transformers`——仅用于向量召回增强。缺失时 `VectorRecognizer` 自动回退到本地确定性哈希向量化（SHA256 哈希生成 384 维归一化向量），功能完整可用，仅向量匹配精度略降；增量影响面分析仍有路由闭包与关键词硬匹配等确定性信号兜底。

**离线说明**：包装脚本已预设 `HF_HUB_OFFLINE=1` 与 `TRANSFORMERS_OFFLINE=1`，加载模型时优先使用本地缓存；本地无模型缓存时加载快速失败，自动走哈希回退，全程不产生网络请求。

## 三、使用方式

```
/archmap <项目路径>                        # 零参自动分流（推荐）
/archmap <项目路径> full | lite [备注]      # 强制模式兜底
/archmap <项目路径> <需求文本>              # 增量影响面分析
/archmap <项目路径> sync                   # 同步变更并重生成全套报告
/archmap <项目路径> diff [修改内容备注]     # diff 影响面 + 变更台账
```

**零参自动分流**：零参调用按基线（`archmap/full_index.json`）存在与否自动分流——无基线 → full 完整初始化；有基线 → lite 极简增量。特殊场景用 `full` / `lite` 显式词强制兜底（大重构后 `full` 重生成完整图谱，无需删基线目录）。

**典型节奏**：

1. `full` 建基线：`/archmap /path/to/project`
2. 需求定影响面：`/archmap /path/to/project "新增用户积分系统"` → `precise_analysis.json`
3. 开发新功能并修改源码
4. `diff` 留痕（复盘前固定卡点）：`/archmap /path/to/project diff 本次修改内容备注` → `diff_impact.json` + `10_变更历史.md`
5. 复盘 / 验收
6. `sync` 刷新：验收通过后 `/archmap /path/to/project sync`，合并变更并重生成 01~09 分析文档，自动做召回验证

## 四、产物清单

全部产物写入 `<项目路径>/archmap/`（JSON/Markdown/Mermaid 纯文本）：

```
<项目路径>/archmap/
├── full_index.json           # 完整架构基线
├── vector_cache.json         # 模块向量缓存
├── module_hashes.json        # 模块内容指纹（SHA256）
├── file_line_hashes.json     # 行级快照（diff/lite 比对依据）
├── file_imports.json         # 文件级导入图缓存
├── 01_执行摘要.md
├── 02_架构图.md               # Mermaid 文本
├── 03_数据链路图.md
├── 04_时序图.md
├── 05_模块资产清单.md
├── 06_API资产清单.md
├── 07_存储资产清单.md
├── 08_依赖矩阵.md
├── 09_粒度校验报告.md
├── precise_analysis.json     # 增量影响面（模式 B）
├── precise_meta.json         # 预测元数据
├── diff_impact.json          # diff 影响面与测试选择（模式 F/lite）
├── diff_history.jsonl        # 变更留痕（机器可读）
├── 10_变更历史.md             # 变更台账（复盘输入）
├── recall_report.json        # 召回验证报告（sync/lite 有待验证预测时）
├── recall_history.jsonl      # 召回验证历史
├── etl_rule_registry.json    # 【可选】项目级自定义 ETL 规则注册表（见第五节）
└── etl_rules/                # ETL 项目自动产出（模式 D，8 项规则维护产物）
```

## 五、项目级配置：ETL 规则注册表覆盖

模式 D（ETL 底层规则探查）默认按特征目录（`etl/` / `etl_config/` / `etl/core` 等）自动检测并基于内置注册表产出。项目可在自身基线目录提供自定义注册表覆盖内置结构，驱动模式 D 的产出：

```
<项目路径>/archmap/etl_rule_registry.json
```

该 JSON 文件镜像内置注册表结构，字段包括：

| 字段 | 说明 |
|------|------|
| `rules` | 规则条目列表（编码、名称、分层、关键词标签、risk_level/priority、history 等） |
| `keyword_index` | 关键词 → 规则编码的快捷索引 |
| `layers` | 7 分层定义（预处理清洗→Chunk分片→向量化写入→一致性对账→隔离存储→异常重试→ETL编排） |
| `config_contracts` | 配置-代码契约（yaml 键与 read/use 特征串，驱动契约漂移检测） |
| `etl_detect_dirs` | ETL 特征目录列表（自定义检测入口） |
| `config_reads` | 配置文件读取点定义（参数基线回填来源） |

无自定义注册表时，按特征目录自动检测并使用内置注册表，无需任何配置。

## 六、下游生态对接

- **test-case-designer**：直接消费 `02~08` 号产物（架构图/数据链路图/时序图/模块/API/存储资产清单/依赖矩阵）做「节点 + 分支 + 方法」三要素测试设计；增量场景优先读取 `precise_analysis.json` 精准圈定测试范围，避免全量重设计。ArchMap 产物缺失或过期时由 test-case-designer 自行调用本技能生成，PM 无需单独调用。
- **whitebox-coverage**：增量模式以 `diff_impact.json` 为唯一范围依据（选择性执行 + `--diff-scope` 缺口过滤 + diff_gate 门禁）。
- **复盘流程**：以 `10_变更历史.md` + `diff_history.jsonl` 为变更台账输入；diff 留痕是复盘前固定卡点。

## 七、约束与边界

- 只读源码做静态分析，**不修改用户原始业务代码**。
- **不启动任何 Web 服务**，终端原生运行。
- 不读写 SQLite 任务表；所有状态保存在项目路径下的 `archmap/` 文件夹内。
- 输出均为 JSON/YAML/Markdown/Mermaid **纯文本**，不生成图片。
- 全量模式只扫描业务目录，自动过滤 test、node_modules、dist、build 等目录。
- 增量模式复用存量基线资产，不重复解析未变更模块，显著降低 Token 消耗。
