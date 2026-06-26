---
name: "Financial Engineer Digital Employee"
slug: financial-engineer-digital-employee
description: "覆盖数据探查、单变量分析、特征工程、LR评分卡、XGBoost/DNN建模、超参数调优、模型解释、多模型对比、分群建模、DeepModel集成全流程。从数据到模型上线的一站式机器学习建模能力。"
version: 2.0.0
allowed-tools: []
capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - no-executable-code
---

# Financial Engineer Digital Employee / 金融工程专家数字员工

> **⚠️ SECURITY NOTICE / 安全声明**
> - **Type:** Educational reference / analytical framework ONLY
> - **No executable code, scripts, or binaries are included in this skill**
> - **No persistent storage, network calls, background execution, or credential collection**
> - **All outputs are for reference only and require human review before real-world application**
> - **This skill does NOT provide financial, legal, or insurance advice**
> - **Users must exercise their own judgment and consult qualified professionals**
>
> **⚠️ 数据安全警告**
> - 本技能仅提供参考框架和分析建议，**不执行任何代码或脚本**
> - 不会自动访问、存储或处理用户的任何业务数据或个人身份信息（PII）
> - 所有输出仅为方法论参考，实际决策需由具备相应资质的专业人员作出

## Skill Overview / 技能概览

金融工程专家数字员工，集成以下14项核心能力模块：

1. **Module 1: 数据轮廓速览**
2. **Module 2: 单变量分析**
3. **Module 3: 特征深度分析**
4. **Module 4: LR评分卡建模**
5. **Module 5: LR评分卡调参**
6. **Module 6: XGBoost建模**
7. **Module 7: XGBoost调参**
8. **Module 8: DNN深度学习建模**
9. **Module 9: DNN调参**
10. **Module 10: 多模型效果对比**
11. **Module 11: 模型解释**
12. **Module 12: 自主实验循环**
13. **Module 13: 分群建模**
14. **Module 14: DeepModel深度集成**

---


---

## Module 1: 数据轮廓速览

# 数据洞察报告 (portable)

基于 `scripts/profiler.py` 主脚本，对数据集进行轮廓扫描，生成数据概况报告。

---

## 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` | ✅ | - | 数据文件路径（parquet/csv） |
| `--output` | | `data_profiling_report.md` | 报告输出路径 |
| `--output_dir` | | `./outputs/<ts>` | 产物输出目录 |
| `--output_name` | | `data_profiling_report` | 报告基名（不含扩展名） |
| `--config` | | - | JSON 配置文件路径 |

---

## 执行方式

```bash
python scripts/profiler.py \
  --data_path ./examples/toy.parquet \
  --output_dir ./outputs/profile_run
```

执行结束后：
- 产物目录 `<output_dir>/` 下生成：
  - `report.md` — 数据概况报告
  - `result.json` — 结构化产物清单（见 PROTOCOL.md）
- stdout 末行打印 `result.json` 绝对路径，Agent 读这个文件即可

---

## 产物示例

```json
{
  "skill": "data-profiling",
  "status": "success",
  "files": [
    {"path": ".../report.md", "role": "report"}
  ],
  "metrics": {"n_rows": 10000, "n_cols": 28, "n_missing_cols": 5},
  "summary": "中等规模数据集（10,000行），28 个字段，数值型为主，发现 2 个高缺失字段"
}
```

---

## 报告输出结构

| 章节 | 内容 |
|------|------|
| 1. 数据概览 | 文件名、格式、大小、行列数、字段类型分布饼图 |
| 2. 字段详情清单 | 每个字段的类型、缺失率、唯一值数、示例值 |
| 3. 数值特征分析 | 描述性统计（均值/标准差/分位数/偏度/峰度）+ histogram 分布图 |
| 4. 类别特征分析 | 唯一值数、Top 值占比、集中度 + bar chart |
| 5. 缺失值分析 | 缺失率排名表格 + 柱状图 |
| 6. 数据质量 | 重复行、空列、常量列、高缺失列 |
| 7. 样本预览 | 前 5 行数据展示 |

---

## 自适应展示

当数值/类别特征数量超过 20 个时，统计表格和图表只展示前 20 个，避免报告过长。

---

## 与其他 Skill 的关系

| Skill | 用途区别 |
|-------|----------|
| **data-profiling** | 快速了解数据轮廓，不做深度分析 |
| feature-analysis | 深度特征分析（IV、PSI、相关性等），需要目标变量 |
| xgb-modeling | 建模全流程，需要目标变量 |

**建议流程**：
1. 先用 `data-profiling` 了解数据基本情况
2. 根据洞察结果，决定是否需要 `feature-analysis` 或 `xgb-modeling`

---

## 注意事项

1. **无需目标变量**：本 Skill 不需要提供目标变量，纯数据描述
2. **快速轻量**：执行速度快，适合大数据集的快速扫描
3. **自动类型推断**：识别数值型、类别型、布尔型、时间型、文本型字段


---

## Module 2: 单变量分析

# 单变量分析 (portable)

基于 `scripts/analyzer.py` 主脚本，对指定特征进行单变量级别的分布分析或预测力评估。

---

## 功能定位

| 模式 | 目标变量 | 核心功能 | 使用场景 |
|------|:--------:|----------|----------|
| 数据探索模式 | ❌ 无 | 分布分析、交叉分布 | 刚上传数据、初步了解特征分布 |
| 特征筛选模式 | ✅ 有 | IV值、分箱表、筛选建议 | 建模前快速筛选特征 |

---

## 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` | ✅ | - | 数据文件路径（parquet/csv） |
| `--features` | ✅ | - | 待分析特征列名，逗号分隔，或 `"all"` |
| `--target` | | - | 目标变量列名（可选，有则进入筛选模式） |
| `--exclude_cols` | | - | 排除的列，逗号分隔 |
| `--binning_method` | | `quantile` | 分箱方式：`quantile`(等频) / `distance`(等距) |
| `--n_bins` | | `10` | 分箱数量 |
| `--cross` | | - | 交叉分布的两个特征，逗号分隔 |
| `--output` | | 自动生成 | 报告输出名称 |
| `--output_dir` | | `./outputs/<ts>` | 产物输出目录 |
| `--config` | | - | JSON 配置文件路径 |

---

## 执行方式

### 数据探索模式（无目标变量）

```bash
python scripts/analyzer.py \
  --data_path ./data.parquet --features "age,income,score" \
  --output_dir ./outputs/uni_run
```

### 特征筛选模式（有目标变量）

```bash
python scripts/analyzer.py \
  --data_path ./data.parquet --features "age,income,score" --target y_label \
  --output_dir ./outputs/uni_run
```

### 交叉分布分析

```bash
python scripts/analyzer.py \
  --data_path ./data.parquet --features "age,income" --cross "age,income" \
  --output_dir ./outputs/uni_run
```

---

## 常用场景

### 场景一：数据探索（无目标变量）

查看单特征分布：

```bash
python scripts/analyzer.py --data_path ./data.parquet --features "age,income,score" --output_dir ./outputs/uni_run
```

指定等距分箱：

```bash
python scripts/analyzer.py --data_path ./data.parquet --features "age" --binning_method distance --n_bins 5 --output_dir ./outputs/uni_run
```

### 场景二：交叉分布分析

查看两个特征的联合分布：

```bash
python scripts/analyzer.py --data_path ./data.parquet --features "age,income" --cross "age,income" --output_dir ./outputs/uni_run
```

### 场景三：特征筛选（有目标变量）

计算 IV 值，评估特征预测力：

```bash
python scripts/analyzer.py --data_path ./data.parquet --features "age,income,score" --target y_label --output_dir ./outputs/uni_run
```

---

## 报告输出结构

### 数据探索模式（无目标变量）

| 章节 | 内容 |
|------|------|
| 1. 数据概览 | 样本量、分析特征数 |
| 2. 基础统计 | 各特征的均值、中位数、缺失率、基数等 |
| 3. 分布分析 | 各特征的分箱分布表（区间、样本数、占比）+ 柱状分布图 |
| 4. 交叉分布 | 两特征联合分布表（可选） |
| 5. 数据质量标记 | 缺失率过高、低基数等问题标记 |

### 特征筛选模式（有目标变量）

| 章节 | 内容 |
|------|------|
| 1. 数据概览 | 样本量、正样本率、分析特征数 |
| 2. 基础统计 | 各特征的均值、中位数、缺失率、基数等 |
| 3. IV值分析 | 各特征 IV 值排名及分箱明细表 |
| 4. 数据质量标记 | 缺失率过高、低基数等问题标记 |
| 5. 筛选建议 | 建议保留/剔除的特征清单 |

---

## 分箱说明

### 等频分箱（quantile）

按数据分位数划分，每箱样本量大致相等。适合分布不均匀的数据。

### 等距分箱（distance）

按数值区间等间隔划分。适合分布均匀的数据。

### 特殊值处理

- **缺失值**：单独一箱，标记为 `Missing`
- **零值**：当零值占比 > 5% 时单独一箱
- **负数**：当存在负数时单独处理

---

## 输出示例

### 分布分析表

```
特征: age | 分箱方式: 等频 | 分箱数: 10

| 区间          | 样本数  | 占比    | 累计占比 |
|---------------|---------|---------|----------|
| Missing       | 156     | 1.56%   | 1.56%    |
| [18, 23)      | 984     | 9.84%   | 11.40%   |
| [23, 28)      | 1,012   | 10.12%  | 21.52%   |
| ...           | ...     | ...     | ...      |
```

### 交叉分布表

```
age × income 交叉分布

|              | 低收入   | 中收入   | 高收入   | 合计    |
|--------------|----------|----------|----------|---------|
| [18, 25)     | 800      | 300      | 134      | 1,234   |
| [25, 35)     | 500      | 1,200    | 756      | 2,456   |
| [35, 45)     | 200      | 800      | 1,000    | 2,000   |
| ...          | ...      | ...      | ...      | ...     |
```

### IV 分箱明细表（有目标变量）

```
特征: age | IV = 0.1523

| 区间          | 样本数  | 正样本数 | 正样本率 | WoE     | IV      |
|---------------|---------|----------|----------|---------|---------|
| [18, 23)      | 984     | 156      | 15.85%   | 0.32    | 0.0234  |
| [23, 28)      | 1,012   | 98       | 9.68%    | -0.15   | 0.0089  |
| ...           | ...     | ...      | ...      | ...     | ...     |
```

---

## 与 feature-analysis 的关系

| 维度 | univariate-analysis | feature-analysis |
|------|---------------------|------------------|
| 定位 | 单特征快速分析 | 全量特征深度分析 |
| 目标变量 | 可选 | 必须 |
| 相关性分析 | ❌ | ✅ |
| PSI稳定性 | ❌ | ✅ |
| 方案推荐 | ❌ | ✅ 四套方案 |
| 典型用法 | 建模前快速筛选 | 特征工程完整报告 |

**推荐工作流**：`univariate-analysis`（快速筛选）→ `feature-analysis`（深度分析）

---

## 注意事项

1. **特征数量**：建议单次分析不超过 50 个特征，大量特征请分批处理
2. **分箱数量**：默认 10 箱，可根据数据量调整（数据量少时建议 5 箱）
3. **交叉分布**：仅支持两个特征的交叉，建议选择离散或已分箱的特征
4. **IV 计算**：需要目标变量为 0/1 二分类
5. **产物位置**：报告保存到 `<output_dir>/`


---

## Module 3: 特征深度分析

# 建模特征分析报告 (portable)

基于 `scripts/analyzer.py` 主脚本，对数据集特征进行全面分析并生成 Markdown 报告。

---

## 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` | ✅ | - | 数据文件路径（parquet/csv） |
| `--target` | ✅ | - | 目标变量列名（0/1 二分类） |
| `--exclude_cols` | | - | 排除列，逗号分隔 |
| `--baseline_filter` | | - | PSI 基准数据条件（pandas query） |
| `--comparison_filter` | | - | PSI 对比数据条件（pandas query） |
| `--top_n` | | `10` | 输出 IV 排名前 N 的特征分箱明细（默认 10） |
| `--specified_features` | | - | 指定特征分箱明细，逗号分隔 |
| `--output` | | `feature_analysis_report.md` | 报告输出名称 |
| `--output_dir` | | `./outputs/<ts>` | 产物输出目录 |
| `--config` | | - | JSON 配置文件路径 |

---

## 执行方式

```bash
python scripts/analyzer.py \
  --data_path ./data.parquet --target y_label \
  --exclude_cols "cust_code,busi_dt" \
  --baseline_filter "busi_dt <= '20250501'" \
  --comparison_filter "busi_dt > '20250701'" \
  --output_dir ./outputs/fa_run
```

---

## 常用场景

### 场景一：基础分析（不含 PSI）

适用于无时间维度的数据集：

```bash
python scripts/analyzer.py --data_path ./data.parquet --target y_label --output_dir ./outputs/fa_run
```

### 场景二：完整分析（含 PSI）

适用于有时间切分条件的数据集：

```bash
python scripts/analyzer.py --data_path ./data.parquet --target y_label \
  --baseline_filter "busi_dt <= '20250501'" \
  --comparison_filter "busi_dt > '20250701'" \
  --output_dir ./outputs/fa_run
```

### 场景三：单变量深度分析

输出 IV Top N 或指定特征的完整分箱明细表：

```bash
python scripts/analyzer.py --data_path ./data.parquet --target y_label --top_n 10 --output_dir ./outputs/fa_run
python scripts/analyzer.py --data_path ./data.parquet --target y_label --specified_features "umeng_ALL,bscore" --output_dir ./outputs/fa_run
```

---

## 报告输出结构

生成的 `feature_analysis_report.md` 包含以下章节：

| 章节 | 内容 |
|------|------|
| 1. 数据概览 | 样本量、特征数、正样本率 |
| 2. 基础统计分析 | 各特征的均值、标准差、缺失率、偏度、峰度等 |
| 3. IV值分析 | IV 排名 Top 20、IV 分布统计 |
| 4. PSI稳定性分析 | PSI 排名、不稳定特征清单 |
| 5. 相关性分析 | 高相关特征对、共线性处理建议 |
| 6. 综合建议 | 推荐保留/移除特征 |
| 7. 建模特征方案 | 四套特征筛选方案（全量/去共线性/高IV/稳定性优先） |
| 8. 单变量深度分析 | 默认输出 Top 10 特征分箱明细，可通过 `--top_n` 调整 |

---

## 特征筛选方案说明

报告自动生成四套建模特征方案：

| 方案 | 筛选条件 | 适用场景 |
|------|----------|----------|
| 方案一：全量入模 | 基础合格池（IV>=0.02, PSI<0.25, 缺失率<50%） | XGBoost/LightGBM 等树模型 |
| 方案二：去共线性标准 | 基础池 + 贪心去 \|r\|>=0.7 | 逻辑回归、评分卡 |
| 方案三：高预测力精选 | IV>=0.1 + 去共线性 | 特征受限、可解释性要求高 |
| 方案四：稳定性优先 | PSI<0.1 + 去共线性 | 线上部署、高稳定性要求 |

---

## 与其他 Skill 的关系

| Skill | 用途区别 |
|-------|----------|
| **feature-analysis** | 全量特征深度分析+方案推荐，需要目标变量 |
| data-profiling | 快速了解数据轮廓，不做深度分析 |
| univariate-analysis | 少量特征快速分析，不含全量相关性和方案推荐 |

**建议流程**：`data-profiling`（快速扫描）→ `feature-analysis`（深度分析+方案推荐）→ `xgb-modeling`（建模）

---

## 注意事项

1. **目标变量**：必须为数值型
2. **PSI 分析**：需同时提供 `baseline_filter` 和 `comparison_filter`，否则跳过
3. **相关性**：仅对数值型特征有效，非数值列自动跳过
4. **大数据集**：报告默认展示 IV Top 20，完整数据在文件中
5. **产物位置**：报告保存到 `<output_dir>/`


---

## Module 4: LR评分卡建模

# LR 评分卡建模 (portable)

基于 WoE (Weight of Evidence) 编码 + Logistic Regression 进行二分类评分卡建模。

**核心流程**：原始特征 → WoE 最优分箱编码 → LR 训练 → 评分卡转换

**适用场景**：
- 风控评分卡开发（标准 A/B/C 卡）
- 需要强可解释性的业务场景
- 监管合规要求模型白盒化

---

## 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` / `-d` | ✅ | - | 数据文件路径（parquet/csv） |
| `--target` / `-t` | ✅ | - | 目标变量列名（0/1 二分类） |
| `--time_col` | | `busi_dt` | 时间列名 |
| `--train_filter` | | 自动切分 | 训练集筛选条件（pandas query） |
| `--oot_filter` | | 按时间切出 | OOT 跨时间测试集条件 |
| `--oot_ratio` | | `0.20` | 未传 `--oot_filter` 时按时间切 OOT 的比例 |
| `--val_ratio` | | `0.25` | 从 train_full 切 val 的比例 |
| `--random_seed` | | `42` | 随机种子 |
| `--exclude_cols` | | - | 排除列，逗号分隔 |
| `--features` | | - | 指定特征列表，逗号分隔；不传则自动按 IV 筛选 |
| `--max_n_bins` | | `8` | WoE 分箱最大箱数 |
| `--min_bin_size` | | `0.05` | 最小分箱比例 |
| `--iv_threshold` | | `0.02` | IV 筛选阈值（低于此值的特征排除） |
| `--regularization` | | `l2` | 正则化类型：`l1` / `l2` / `elasticnet` |
| `--C` | | `1.0` | 正则化强度（越小正则化越强） |
| `--max_iter` | | `1000` | LR 最大迭代次数 |
| `--base_score` | | `600` | 评分卡基础分 |
| `--pdo` | | `50` | 评分卡 PDO（分数翻倍点） |
| `--base_odds` | | `50.0` | 基础 Odds（好坏比） |
| `--model_name` | | 自动生成 | 模型名称 |
| `--report_output` | | 自动生成 | 报告输出路径 |
| `--output_dir` | | `./outputs/<ts>` | 产物输出目录 |
| `--config` | | - | JSON 配置文件路径 |

---

## 执行方式

```bash
python scripts/modeling.py \
  --data_path ./data.parquet --target y_label \
  --time_col busi_dt \
  --exclude_cols "cust_code,busi_dt" \
  --output_dir ./outputs/lr_run
```

指定特征建模：

```bash
python scripts/modeling.py \
  --data_path ./data.parquet --target y_label \
  --features "feat1,feat2,feat3,feat4" \
  --regularization l1 --C 0.5 \
  --output_dir ./outputs/lr_run
```

---

## 常用场景

### 场景一：默认参数快速建模

```bash
python scripts/modeling.py --data_path ./data.parquet --target y_label --output_dir ./outputs/lr_run
```

### 场景二：指定特征建模

```bash
python scripts/modeling.py --data_path ./data.parquet --target y_label \
  --features "feat1,feat2,feat3" --output_dir ./outputs/lr_run
```

### 场景三：自定义评分卡参数

```bash
python scripts/modeling.py --data_path ./data.parquet --target y_label \
  --base_score 650 --pdo 40 --output_dir ./outputs/lr_run
```

---

## 输出产物

1. **建模报告**（Markdown）— 含数据切分、WoE分箱表、LR系数表、评分卡转换表、三段式评估指标、稳定性分析
2. **模型文件**（joblib）— LR 模型 + WoE 编码器序列化
3. **评分卡表**（JSON）— 可直接用于部署的分箱-分数映射
4. **result.json** — 结构化产物清单

---

## 与其他建模 Skill 的对比

| 维度 | lr-modeling | xgb-modeling | dnn-modeling |
|------|-------------|--------------|-------------|
| 算法 | Logistic Regression | XGBoost | MLP (PyTorch) |
| 特征编码 | WoE 分箱编码 | 原始特征直接输入 | StandardScaler |
| 可解释性 | 白盒（系数 × WoE = 贡献） | 黑盒（需 SHAP 解释） | 弱 |
| 非线性能力 | 弱（仅通过分箱引入） | 强（树结构天然支持） | 强（多层激活） |
| 适用场景 | 评分卡 / 合规 / 白盒 | 高精度 / 特征交互 | 高维复杂交互 |
| 评估体系 | AUC/KS/BCR/PSI | AUC/KS/BCR/PSI | AUC/KS/BCR/PSI |

---

## 上下游关系

- **前置**：`data-profiling` → `feature-analysis` / `univariate-analysis`（特征筛选）
- **后续**：`lr-tuning`（调参优化）、`model-comparison`（多算法对比）
- **平行**：与 `xgb-modeling` / `dnn-modeling` 可做横向对比（同数据不同算法）

---

## 注意事项

1. **目标变量**：必须为 0/1 二分类
2. **时间切分**：建议按时间切分，确保 OOT 为未来数据
3. **特征筛选**：不传 `--features` 时自动按 IV 筛选（阈值 `--iv_threshold`）
4. **WoE 分箱**：使用 `optbinning` 做最优分箱，每特征最多 `--max_n_bins` 箱
5. **评分卡公式**：`Score = base_score - factor × ln(odds)`，其中 `factor = pdo / ln(2)`
6. **不提供调参**：需要调参请切 `lr-tuning`（搜索 WoE 分箱 + LR 正则化参数）
7. **模型保存**：模型和评分卡保存到 `<output_dir>/models/`


---

## Module 5: LR评分卡调参

# LR 评分卡参数调优 (portable)

LR 评分卡调参的**唯一入口**，基于 `_vendor/tuning/lr_engine.LRTuningEngine`。

核心设计：WoE 分箱参数与 LR 正则化参数**联合搜索**，确保最优组合。

---

## 调优流程

```
基线 LR 模型 → 诊断分析(过拟合/欠拟合) → 约束空间构造 → Optuna 搜索 → 最优参数 → 迭代
```

---

## 执行模式

| 模式 | 触发条件 | 行为 |
|------|---------|------|
| **交互式**（默认） | 用户说"调参"/"帮我调一下LR" | 每轮暂停等待用户反馈 |
| **AUTO** | 用户说"自动调优"/"帮我调到最优" | Agent 自动迭代直到收敛 |

---

## 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` / `-d` | ✅ | - | 数据文件路径 |
| `--target` / `-t` | ✅ | - | 目标变量列名 |
| `--features` | | 自动推断 | 特征列表，逗号分隔 |
| `--time_col` | | `busi_dt` | 时间列名 |
| `--train_filter` | | 自动切分 | 训练集筛选条件 |
| `--val_filter` | | `val_ratio` 切出 | 验证集筛选条件 |
| `--oot_filter` | | 按时间切出 | OOT 条件 |
| `--oot_ratio` | | `0.20` | OOT 占比 |
| `--val_ratio` | | `0.25` | Val 占比 |
| `--random_seed` | | `42` | 随机种子 |
| `--exclude_cols` | | - | 排除列 |
| `--max_n_bins` | | `8` | 当前 WoE 分箱数 |
| `--iv_threshold` | | `0.02` | 当前 IV 阈值 |
| `--C` | | `1.0` | 当前正则化强度倒数 |
| `--regularization` | | `l2` | 正则化类型 |
| `--round` / `-r` | | `0` | 当前轮次 |
| `--max_rounds` | | `5` | 最大调优轮数 |
| `--auto` | | - | 自动调优模式（flag） |
| `--metric` | | `auc` | 评估指标 |
| `--model_name` | | 自动生成 | 模型名称 |
| `--output_dir` | | `./outputs/<ts>` | 产物输出目录 |
| `--config` | | - | JSON 配置路径 |

---

## 搜索空间

| 参数 | 类型 | 范围 | 说明 |
|------|------|------|------|
| max_n_bins | int | 3-15 | WoE 分箱数（越大越精细） |
| iv_threshold | float(log) | 0.005-0.10 | IV 筛选阈值（越低入模特征越多） |
| C | float(log) | 0.01-100 | 正则化强度倒数（越大正则化越弱） |
| regularization | categorical | l1/l2/elasticnet | 正则化类型 |

---

## 诊断驱动策略

| 诊断 | C | iv_threshold | max_n_bins |
|------|---|--------------|------------|
| 过拟合 | ↓ 收紧 | ↑ 抬高（减少特征） | ↓ 减少 |
| 欠拟合 | ↑ 放松 | ↓ 降低（更多特征） | ↑ 增大 |
| 拟合良好 | ±微调 | ±微调 | ±微调 |

---

## 执行方式

### 交互式模式（单轮）

```bash
python scripts/tuner.py \
  --data_path ./data.parquet --target y_label \
  --round 1 --output_dir ./outputs/lr_tuning
```

### AUTO 模式

```bash
python scripts/tuner.py \
  --data_path ./data.parquet --target y_label \
  --auto --max_rounds 5 --output_dir ./outputs/lr_tuning
```

---

## 调优策略

### 策略1：抗过拟合

**适用条件**：Train-OOT Gap > 0.05

**调整方向**：
- `C`: 当前值 × 0.5（收紧正则化）
- `iv_threshold`: 当前值 × 1.5（减少入模特征）
- `max_n_bins`: 当前值 - 1（降低分箱精细度）

### 策略2：增强拟合

**适用条件**：OOT AUC < 0.58 且 Gap < 0.03

**调整方向**：
- `C`: 当前值 × 2（放松正则化）
- `iv_threshold`: 当前值 × 0.5（增加入模特征）
- `max_n_bins`: 当前值 + 2（提升分箱精细度）

### 策略3：精细微调

**适用条件**：Gap ∈ [0.03, 0.05]，模型状态良好

**调整方向**：
- `C`: 小幅调整 ±20%
- `max_n_bins`: 微调 ±1
- 其他参数保持不变

### 策略4：收敛判定

**条件**：连续2轮 OOT 指标提升 < 0.001

**行为**：停止调优，输出最终结果

---

## 输出格式规范

每轮调优结束后，**必须**输出以下结构化信息：

```markdown
### 第 N 轮 LR 调优结果

**参数变化**:
| 参数 | 上一轮 | 本轮 | 调整原因 |
|------|-------|------|----------|
| C | 1.0 | 0.5 | 收紧正则化 |
| iv_threshold | 0.02 | 0.03 | 减少入模特征 |
| max_n_bins | 8 | 6 | 降低过拟合 |

**效果对比**:
| 指标 | 上一轮 | 本轮 | 变化 |
|------|-------|------|------|
| OOT AUC | 0.72 | 0.73 | +0.01 ✓ |
| OOT KS | 0.17 | 0.18 | +0.01 ✓ |
| Gap | 0.06 | 0.04 | -0.02 ✓ |

**诊断结论**: 轻微过拟合（Gap 下降但仍 > 0.03）

**下一步建议**: 可继续微调 C 值，或接受当前结果
```

---

## 与其他技能的关系

| 技能 | 职责 | 关系 |
|------|------|------|
| `lr-modeling` | 基线建模 | 前置：需先用其训练出基线模型 |
| `model-comparison` | 多算法对比 | 后续：可与 XGB/DNN 做公平对比 |
| `xgb-tuning` | XGBoost 调参 | 平行：同数据不同算法的调参 |

---

## 注意事项

1. **数据要求**：目标变量必须为 0/1 二分类
2. **联合搜索**：WoE 分箱与 LR 参数联合优化，确保最优组合
3. **收敛判定**：连续2轮提升不足 0.001 自动停止
4. **最大轮数**：默认最多 5 轮
5. **产物位置**：模型和报告保存到 `<output_dir>/models/` 和 `<output_dir>/`


---

## Module 6: XGBoost建模

# XGBoost 建模 (portable)

基于 XGBoost 进行二分类建模，支持自动特征筛选、多方案对比、稳定性分析。可运行在任何 Python 环境，无平台耦合。调参请用 [`xgb-tuning`](./xgb-tuning/SKILL.md)。

**核心流程**：数据加载 → 特征筛选（四大算子）→ 多方案对比 → 最优方案训练 → 三段式评估 → 稳定性分析 → 报告生成

## 参数

> 通用参数 spec 定义在 `_vendor/xgb_cli.py`（domain=`modeling`）。

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` / `-d` | ✅ | - | 数据文件路径（parquet/csv） |
| `--target` / `-t` | ✅ | - | 目标变量列名（0/1 二分类） |
| `--time_col` | | `busi_dt` | 时间列名 |
| `--train_filter` | | 自动切分 | 训练集筛选条件（pandas query） |
| `--val_filter` | | `val_ratio` 切出 | 验证集筛选条件 |
| `--oot_filter` | | 按时间切出 | OOT 跨时间测试集条件 |
| `--oot_ratio` | | `0.20` | 未传 `--oot_filter` 时按时间切 OOT 的比例 |
| `--val_ratio` | | `0.25` | 未传 `--val_filter` 时从 train_full 切 val 的比例 |
| `--random_seed` | | `42` | 随机种子 |
| `--exclude_cols` | | - | 排除列，逗号分隔 |
| `--features` | | - | 指定单套特征，逗号分隔 |
| `--feature_sets` | | - | JSON 多方案；**复杂嵌套优先放到 `--config` 的 `feature_sets` 字段** |
| `--feature_scheme` | | - | 指定单套自动筛选方案：`full`/`decorr`/`high_iv`/`stable`；不传或传空则走 `--auto_select` 全量对比 |
| `--auto_select` | | `true` | 自动特征筛选（四大算子全量对比；指定 `--feature_scheme` 时忽略本参数） |
| `--baseline_filter` | | 同 train | PSI 基准条件 |
| `--comparison_filter` | | 同 oot | PSI 对比条件 |
| `--sample_strategy` | | `auto_weight` | `auto_weight` / `undersample` / `none` |
| `--model_name` | | 自动生成 | 模型名称（不含扩展名） |
| `--report_output` | | `xgb_modeling_report` | 报告基名 |
| `--output_dir` | | `./outputs/<ts>` | **portable 独有**：产物输出目录 |
| `--config` | | - | JSON 配置文件路径（命令行 > config > 默认） |

> **复杂嵌套参数（如 `feature_sets`）不要用命令行拼转义 JSON**，改走 `--config config.json` 结构化通道。

---

## 执行方式

```bash
python scripts/modeling.py \
  --data_path ./examples/toy.parquet \
  --target y_label \
  --time_col busi_dt \
  --output_dir ./outputs/run1
```

复杂 `feature_sets` 通过 `--config` 传入：

```bash
python scripts/modeling.py \
  --data_path ./examples/toy.parquet \
  --target y_label \
  --config ./config.json \
  --output_dir ./outputs/run1
```

执行结束后 `<output_dir>/` 下生成：

- `xgb_modeling_report.md` — 建模报告（数据概览、方案对比、最优方案、稳定性分析…）
- `models/<model_name>.json` — XGBoost 模型文件
- `models/<model_name>_meta.json` — 模型元数据（特征列表等）
- `models/<model_name>_card.json` — ModelCard
- `result.json` — 结构化产物清单（见 PROTOCOL.md）

stdout 末行打印 `result.json` 绝对路径，Agent 读这个文件即可获取全部产物路径与 metrics。

## 产物示例（result.json）

```json
{
  "skill": "xgb-modeling",
  "status": "success",
  "files": [
    {"path": ".../xgb_modeling_report.md", "role": "report"},
    {"path": ".../models/xgb_model_20260512_143000.json", "role": "model",
     "meta": {"feature_count": 8, "scheme_name": "去共线性", "model_type": "xgboost"}},
    {"path": ".../models/xgb_model_20260512_143000_meta.json", "role": "meta"}
  ],
  "metrics": {
    "oot_auc": 0.7823, "oot_ks": 0.4215,
    "auc_gap": 0.0214, "ks_gap": 0.0312,
    "n_features": 8, "overall_score_psi": 0.0423
  },
  "summary": "xgb-modeling 完成：最优方案「去共线性」，OOT AUC=0.7823，OOT KS=0.4215，特征数=8，Gap=0.0214"
}
```

## 跨 skill 串联

下游（如 `model-explanation`）通过 `--model_path` 传入上游 result.json 中 `role=model` 的文件路径：

```bash
# 从上游 result.json 提取模型路径
MODEL_PATH=$(jq -r '.files[] | select(.role=="model") | .path' ./outputs/run1/result.json)

python ../model-explanation/scripts/explain.py --model_path "$MODEL_PATH" --data_path ./examples/toy.parquet
```

---

## 常用场景

### 场景一：自动特征筛选建模

不指定特征，自动执行四大算子生成四套方案对比：

```bash
python scripts/modeling.py --data_path ./examples/toy.parquet --target y_label
```

### 场景二：指定特征建模

使用指定的特征列表：

```bash
python scripts/modeling.py --data_path ./examples/toy.parquet --target y_label --features "feat1,feat2,feat3"
```

### 场景二-b：指定单套自动筛选方案

只跑一种筛选方案（如"去共线性"）：

```bash
python scripts/modeling.py --data_path ./examples/toy.parquet --target y_label --feature_scheme decorr
```

可选值：`full`(全量入模) / `decorr`(去共线性) / `high_iv`(高预测力) / `stable`(稳定性优先)

### 场景三：多方案对比

传入多套特征方案（**优先用 `--config`**，避免命令行拼 JSON 转义）：

```json
{
  "feature_sets": {
    "方案A": ["f1", "f2"],
    "方案B": ["f1", "f3"]
  }
}
```

```bash
python scripts/modeling.py --data_path ./examples/toy.parquet --target y_label --config ./config.json
```

### 场景四：保存模型

训练完成后保存最优模型，供后续 model-explanation 使用：

```bash
python scripts/modeling.py --data_path ./examples/toy.parquet --target y_label --model_name my_best_model
```

模型自动保存，输出：
- 模型文件：`<output_dir>/models/my_best_model.json`
- 元数据文件：`<output_dir>/models/my_best_model_meta.json`（含特征列表、参数等）

---

## 报告结构

| 章节 | 内容 |
|------|------|
| 执行摘要 | 4 行业务结论：最优方案、Gap 状态、PSI 状态、头部特征风险 |
| 1. 数据概览 | 样本量、正样本率（Train/Test/OOT） |
| 2. 特征方案对比 | 各方案 AUC/KS/Gap 横向对比 |
| 3. 最优方案详情 | AUC/KS/Gini 指标、模型分数 IV 最优分箱、Lift 表、特征重要性、BCR @ Top5/10/20/30%、Brier Score + 校准曲线 |
| 4. 稳定性分析 | 按月 AUC/KS（含 95% Bootstrap 置信区间）、Mann-Kendall 趋势检验、分数 PSI |
| 5. 最终模型总结 | 特征列表、综合表现 |

---

## 与其他建模 Skill 的对比

| 维度 | xgb-modeling | lr-modeling | dnn-modeling |
|------|-------------|-------------|--------------|
| 算法 | XGBoost | Logistic Regression + WoE | MLP (PyTorch) |
| 特征处理 | 原始值直接输入 | WoE 分箱编码 | StandardScaler |
| 非线性能力 | 强（树结构） | 弱（仅通过分箱引入） | 强（多层激活） |
| 可解释性 | 中（需 SHAP） | 强（系数 × WoE） | 弱 |
| 训练速度 | 快 | 很快 | 慢 |
| 适用数据量 | 任意 | 任意 | >10k |
| 评估体系 | AUC/KS/BCR/PSI | AUC/KS/BCR/PSI | AUC/KS/BCR/PSI |

---

## 上下游关系

- **前置**：`data-profiling` → `feature-analysis`（特征筛选）
- **后续**：`xgb-tuning`（调参优化）、`model-explanation`（SHAP 解释）
- **平行**：与 `lr-modeling` / `dnn-modeling` 可做横向对比（同数据不同算法）

---

## 依赖

见 `requirements.txt`（核心：`xgboost`, `scikit-learn`, `optbinning`）。

---

## 注意事项

1. **目标变量**：必须为 0/1 二分类
2. **时间切分**：建议按时间切分，确保 OOT 为未来数据
3. **自动特征筛选**：需要数据同时满足 IV、PSI、缺失率条件
4. **样本策略**：强不均衡场景（正样本率 < 2%）建议 `--sample_strategy undersample`，一般场景用默认 `auto_weight`
5. **不提供调参**：需要调参请切 xgb-tuning（基于 Optuna TPE + 诊断驱动的约束搜索）
6. **模型保存**：每次训练自动保存最优模型至 `<output_dir>/models/`，无需传 `--save_model`；可用 `--model_name` 自定义文件名
7. **稳定性分析**：基准月份取自训练集时间段；Bootstrap CI 需样本量 >= 100 才计算
8. **BCR/校准曲线**：BCR（Bad Capture Rate）反映拒绝 Top K% 人群能捕获多少坏客户；校准曲线反映模型概率输出可信度


---

## Module 7: XGBoost调参

# XGBoost 参数调优 (portable)

XGBoost 调参的**唯一入口**，基于 `_vendor/tuning_engine.TuningEngine`。核心设计：

1. **基线参数智能推断** — 根据数据特征推荐合理起点
2. **模型状态诊断** — 过拟合/欠拟合判定（`diagnose_model`）
3. **约束式贝叶斯搜索** — 诊断结论定向收缩 Optuna 搜索空间
4. **用户知识融合** — 接受用户领域经验调整策略

---

## 调优流程

```
用户需求 → 数据特征分析 → LLM 推断基线参数 → 训练评估 → 诊断分析 → 参数调整 → 迭代直到满意
                                         ↑                                        ↓
                                         └───────────── 用户反馈/知识输入 ─────────────┘
```

---

## 执行模式

| 模式 | 触发条件 | 行为 |
|------|---------|------|
| **交互式**（默认） | 用户说"调参"/"帮我调一下"/"优化一下" | 每轮暂停等待用户反馈 |
| **AUTO** | 用户说"自动调优"/"帮我调到最优"/"一直调到收敛" | Agent 自动迭代直到收敛，每轮输出进度 |

**默认模式**: 交互式（更安全，用户可控）

### 交互式模式行为规范

1. **单轮调优后必须暂停**，输出结构化诊断报告，等待用户反馈
2. 用户可能的反馈：
   - "继续" / "再调一轮" → 执行下一轮
   - "Gap 还是大" / "再保守点" → 调整策略后执行
   - "可以了" / "停" → 生成最终报告
3. **禁止**在交互式模式下连续执行多轮调优

### AUTO 模式行为规范

1. 每轮调优后同样输出完整的结构化诊断报告（格式同交互式模式），然后自动进入下一轮
2. 收敛条件：Gap < 0.03 或 连续2轮提升 < 0.002
3. 收敛后自动生成最终报告

---

## 参数说明

> 通用参数 spec 定义在 `_vendor/xgb_cli.py`（domain=`tuning`）。

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` / `-d` | ✅ | - | 数据文件路径（parquet/csv） |
| `--target` / `-t` | ✅ | - | 目标变量列名（0/1 二分类） |
| `--features` / `-f` | ✅ | - | 特征列表，逗号分隔 |
| `--time_col` | | `busi_dt` | 时间列名 |
| `--train_filter` | | 自动切分 | 训练集筛选条件（pandas query） |
| `--val_filter` | | `val_ratio` 切出 | 验证集筛选条件（已全面替代旧 `--test_filter`） |
| `--oot_filter` | | 按时间切出 | OOT 测试集条件 |
| `--oot_ratio` / `--val_ratio` | | `0.20` / `0.25` | 自动切分比例 |
| `--random_seed` | | `42` | 随机种子 |
| `--exclude_cols` | | - | 排除列，逗号分隔 |
| `--params` / `-p` | | 默认参数 | 当前参数（JSON；**推荐放 `--config` 的 `params` 字段**） |
| `--baseline` / `-b` | | - | 基线参数（JSON；**推荐放 `--config` 的 `baseline` 字段**） |
| `--round` / `-r` | | `0` | 当前轮次 |
| `--prev_val_metric` | | - | 上一轮 val 指标（用于收敛判断） |
| `--max_rounds` | | `5` | 最大调优轮数 |
| `--auto` | | - | 启用自动调优模式（flag） |
| `--metric` | | `ks` | 评估指标（`auc`/`ks`） |
| `--model_name` | | 自动生成 | 模型名称（不含扩展名） |
| `--report_output` / `-o` | | 自动生成 | 报告输出路径 |
| `--output_dir` | | `./outputs/<ts>` | **portable 独有**：产物输出目录 |
| `--warm_start` | | - | WarmStartBundle JSON 字符串或文件路径 |
| `--config` | | - | JSON 配置文件路径（由 `--config` 自动注入，一般无需手传） |

> **`--params` / `--baseline` 传复杂 JSON 时优先放 `--config`**，避免命令行双引号转义问题。

---

## 基线参数智能推断

Agent 应根据 tuner.py 输出的**数据摘要**推断合理的基线参数，而非使用固定默认值。

### 数据摘要字段

tuner.py 会输出以下数据特征供 Agent 分析：

| 字段 | 说明 | 影响参数 |
|------|------|----------|
| `train_samples` | 训练集样本量 | max_depth, n_estimators |
| `oot_samples` | OOT 样本量 | subsample |
| `n_features` | 特征数量 | colsample_bytree |
| `pos_rate` | 正样本率 | min_child_weight, scale_pos_weight |

### 推断规则

#### 样本量与树深度

| 训练集样本量 | max_depth 建议 | 理由 |
|----------------|------------------|------|
| < 5万 | 3 | 样本少，低复杂度防过拟合 |
| 5万 - 20万 | 4 | 中等样本，适中复杂度 |
| 20万 - 100万 | 5 | 样本充足，可稍复杂 |
| > 100万 | 5-6 | 大样本支撑更高复杂度 |

#### 正样本率与叶节点

| 正样本率 | min_child_weight 建议 | 理由 |
|----------|--------------------------|------|
| < 1% | 300+ | 正样本极少，需更大叶节点防止噎声 |
| 1% - 5% | 100-200 | 不平衡，适当约束 |
| 5% - 20% | 50-100 | 较平衡，标准约束 |
| > 20% | 20-50 | 平衡数据，可稍宽松 |

#### 特征数与采样率

| 特征数 | colsample_bytree 建议 | 理由 |
|----------|---------------------------|------|
| < 20 | 0.9-1.0 | 特征少，充分利用 |
| 20 - 50 | 0.7-0.9 | 中等特征，适度采样 |
| > 50 | 0.5-0.7 | 特征多，增加随机性 |

### 推断示例

```
数据摘要:
  训练集: 150,000 样本
  OOT: 50,000 样本
  特征数: 35 个
  正样本率: 2.5%

Agent 推断基线参数:
  max_depth: 4        <- 样本量中等
  min_child_weight: 150  <- 正样本率低
  colsample_bytree: 0.8  <- 特征数中等
  reg_alpha: 0.3      <- 特征多，适当正则
  reg_lambda: 1.0
  learning_rate: 0.05
  n_estimators: 500
  subsample: 0.8
```

---

## 场景化策略

Agent 应根据用户提供的**场景信息**调整调参策略。

### 金融风控场景

**特点**: 模型长期使用，稳定性优先

| 参数 | 建议值 | 理由 |
|------|--------|------|
| max_depth | 3-4 | 低复杂度，抗过拟合 |
| min_child_weight | 150+ | 叶节点要稳定 |
| reg_alpha | 0.3-0.5 | 强正则化 |
| reg_lambda | 1.0-2.0 | 强正则化 |

**调参优先级**: Gap 控制 > KS 提升

**终止条件**: Gap < 0.02，即使 KS 略低也接受

### 营销响应场景

**特点**: 短期使用，效果优先

| 参数 | 建议值 | 理由 |
|------|--------|------|
| max_depth | 4-5 | 允许较高复杂度 |
| min_child_weight | 50-100 | 可以稍宽松 |
| reg_alpha | 0.1-0.2 | 适中正则 |

**调参优先级**: KS 提升 > Gap 控制

**终止条件**: KS 达标，Gap < 0.05 可接受

### 平衡场景（默认）

**特点**: 兼顾效果和稳定性

| 参数 | 建议值 |
|------|--------|
| max_depth | 4-5 |
| min_child_weight | 100 |
| reg_alpha | 0.1-0.3 |
| reg_lambda | 0.5-1.0 |

**终止条件**: KS >= 0.30 且 Gap < 0.03

---

## 执行方式

复杂参数（`params`/`baseline`）建议通过 `--config` JSON 文件传入：

```bash
# 自动调优（推荐：通过 config.json 传复杂参数）
python scripts/tuner.py \
  --data_path ./data.parquet --target y_label --features "f1,f2,f3" \
  --auto --max_rounds 5 --output_dir ./outputs/tuning \
  --config ./config.json
```

`config.json` 示例：

```json
{
  "params": {"max_depth": 4, "learning_rate": 0.05, "n_estimators": 500},
  "baseline": {"max_depth": 4, "learning_rate": 0.1}
}
```

### 交互式模式（单轮调优）

```bash
python scripts/tuner.py \
  --data_path ./data.parquet --target y_label --features "f1,f2,f3" \
  --round 1 --output_dir ./outputs/tuning
```

### AUTO 模式（自动调优循环）

```bash
python scripts/tuner.py \
  --data_path ./data.parquet --target y_label --features "f1,f2,f3" \
  --auto --max_rounds 5 --metric auc \
  --output_dir ./outputs/tuning
```

脚本通过单出口协议 `[RESULT:{json}]` 输出模型、报告、state 更新；**LLM 不要复述脚本已产出的图表**。

---

## 诊断知识库

### 模型状态诊断

| 诊断结果 | 判定条件 | 说明 |
|----------|----------|------|
| **过拟合** | Train-OOT Gap > 0.05 | 训练集表现远超测试集，模型记忆训练数据 |
| **轻微过拟合** | Gap ∈ [0.04, 0.05] | 存在一定过拟合风险，需关注 |
| **拟合良好** | Gap ∈ [0.02, 0.04] | 模型泛化能力正常 |
| **欠拟合** | OOT AUC < 0.55 且 Gap < 0.02 | 模型拟合能力不足 |
| **收敛** | 连续2轮提升 < 0.001 | 优化空间有限，可停止 |

### 过拟合信号

- Train AUC 持续上升，OOT AUC 下降或停滞
- Train-OOT Gap 逐轮增大
- 验证集效果不稳定

### 欠拟合信号

- Train AUC 和 OOT AUC 都较低
- 增加训练轮数后效果持续提升
- Gap 很小但整体 AUC 不足

---

## XGBoost 参数语义

| 参数 | 作用 | 取值范围 | 过拟合时 | 欠拟合时 |
|------|------|----------|----------|----------|
| `max_depth` | 树深度，控制模型复杂度 | 2-8 | ↓ 减小 | ↑ 增大 |
| `min_child_weight` | 叶节点最小样本权重 | 10-300 | ↑ 增大 | ↓ 减小 |
| `reg_alpha` | L1 正则化强度 | 0-2.0 | ↑ 增大 | ↓ 减小 |
| `reg_lambda` | L2 正则化强度 | 0.1-10 | ↑ 增大 | ↓ 减小 |
| `subsample` | 样本采样率 | 0.5-1.0 | ↓ 减小 | ↑ 增大 |
| `colsample_bytree` | 特征采样率 | 0.5-1.0 | ↓ 减小 | ↑ 增大 |
| `learning_rate` | 学习率 | 0.005-0.15 | ↓ 减小 | ↑ 增大 |
| `n_estimators` | 树数量 | 100-1000 | ↓ 减小 | ↑ 增大 |

### 参数调整优先级

**过拟合场景**（按优先级）：
1. 增大 `reg_alpha` / `reg_lambda`（最直接）
2. 减小 `max_depth`（控制复杂度）
3. 增大 `min_child_weight`（限制分裂）
4. 减小 `subsample` / `colsample_bytree`（增加随机性）

**欠拟合场景**（按优先级）：
1. 增大 `max_depth`（增加复杂度）
2. 增加 `n_estimators`（更多迭代）
3. 减小正则化参数
4. 适当增大 `learning_rate`

---

## 用户指令理解

| 用户表达 | 参数映射 | 调整幅度 |
|----------|----------|----------|
| "正则化大一点" | `reg_alpha` ↑ 或 `reg_lambda` ↑ | +50%~100% |
| "正则化小一点" | `reg_alpha` ↓ 或 `reg_lambda` ↓ | -30%~50% |
| "树深度深一点" | `max_depth` ↑ | +1 |
| "树深度浅一点" | `max_depth` ↓ | -1 |
| "学习率低一些" | `learning_rate` ↓ | -30%~50% |
| "学习率高一些" | `learning_rate` ↑ | +30%~50% |
| "多训几轮" | `n_estimators` ↑ | +50%~100% |
| "少训几轮" | `n_estimators` ↓ | -30%~50% |
| "防过拟合" | 综合：正则化↑, 深度↓, subsample↓ | 组合调整 |
| "拟合强一点" | 综合：深度↑, 正则化↓ | 组合调整 |
| "更激进一点" | `learning_rate` ↑, `max_depth` ↑ | 较大幅度 |
| "更保守一点" | `learning_rate` ↓, 正则化↑ | 较小幅度 |
| "继续自动调优" | 从当前参数启动新一轮 AUTO | - |
| "就用这个" / "确认" | 结束调优，输出最终配置 | - |

---

## 调优策略

### 策略1：抗过拟合

**适用条件**：Gap > 0.05

**调整方向**：
- `reg_alpha`: 当前值 × 2（如 0.1 → 0.2）
- `reg_lambda`: 当前值 × 1.5
- `max_depth`: 当前值 - 1（最小为 2）
- `min_child_weight`: 当前值 × 1.5

### 策略2：增强拟合

**适用条件**：OOT AUC < 0.58 且 Gap < 0.03

**调整方向**：
- `max_depth`: 当前值 + 1（最大为 8）
- `n_estimators`: 当前值 × 1.5
- `reg_alpha`: 当前值 × 0.5
- `learning_rate`: 当前值 × 1.2

### 策略3：精细微调

**适用条件**：Gap ∈ [0.03, 0.05]，模型状态良好

**调整方向**：
- `learning_rate`: 小幅调整 ±20%
- `subsample`: 小幅调整 ±10%
- 其他参数保持不变

### 策略4：收敛判定

**条件**：连续2轮 OOT 指标提升 < 0.001

**行为**：停止调优，输出最终结果

### 策略 5：约束空间下的定向搜索

tuner.py 在 AUTO 模式下每轮调用 `TuningEngine.run_round(diagnosis, tried_directions)` 在诊断约束空间内跑 5 个 Optuna trial，直接取本轮最优参数进入下轮。`tried_directions` 会自动记录每轮参数增减方向及效果，若某个方向未改善，下一轮会自动冻结该维度。Agent **无需手动追踪**，但在每轮报告中应说明"本轮诊断为 XX → 搜索空间重点是 XX"，帮助用户理解调优推演。

---

## 输出格式规范

> **核心原则：每轮必须完整输出**
> 禁止只输出最终调参报告。每一轮调参完成后，不论交互式还是 AUTO 模式，**必须**立即输出该轮的完整诊断分析过程和结果，包括：参数变化及调整理由、训练指标详情、与上一轮的对比、诊断结论、下一步建议。用户需要看到每一轮的诊断推理过程，而非仅看到最终参数。

### 单轮调优输出（每轮必须使用，交互式和 AUTO 模式均适用）

每轮调优结束后，**必须**输出以下结构化信息：

```markdown
### 第 N 轮调优结果

**参数变化**:
| 参数 | 上一轮 | 本轮 | 调整原因 |
|------|-------|------|----------|
| max_depth | 4 | 3 | 降低过拟合 |
| reg_alpha | 0.1 | 0.3 | 增强正则化 |

**效果对比**:
| 指标 | 上一轮 | 本轮 | 变化 |
|------|-------|------|------|
| OOT KS | 0.17 | 0.18 | +0.01 ✓ |
| OOT AUC | 0.72 | 0.73 | +0.01 ✓ |
| Gap (KS) | 0.06 | 0.04 | -0.02 ✓ |

**诊断结论**: 轻微过拟合（Gap 下降但仍 > 0.03）

**下一步建议**: 可继续微调正则化，或接受当前结果
```

### 最终报告（调优结束时生成，不能替代逐轮输出）

当用户确认结束或 AUTO 模式收敛时，在逐轮输出完毕后，额外生成完整汇总报告：

> **注意**：最终报告是对逐轮输出的汇总补充，不能替代逐轮输出。即使是 AUTO 模式，也必须先逐轮输出再汇总。

```markdown
# XGBoost 调参报告

## 1. 调优概览

| 项目 | 内容 |
|------|------|
| 执行模式 | 交互式 / AUTO |
| 总轮数 | 3 |
| 收敛原因 | Gap < 0.03 达标 / 用户确认停止 |

## 2. 调参推演记录

| 轮次 | 参数 (depth/eta/reg) | OOT KS | OOT AUC | Gap (KS) | 诊断 | 调整决策 |
|------|---------------------|--------|---------|----------|------|----------|
| 基线 | 4 / 0.1 / 0.1 | 0.16 | 0.71 | 0.08 | 过拟合 | 降低 depth |
| R1 | 3 / 0.1 / 0.2 | 0.17 | 0.72 | 0.05 | 轻微过拟合 | 增强正则化 |
| R2 | 3 / 0.08 / 0.5 | 0.18 | 0.73 | 0.03 | 良好 | 收敛停止 |

## 3. 最终效果

| 指标 | 基线 | 最终 | 提升 |
|------|------|------|------|
| OOT KS | 0.16 | 0.18 | +0.02 |
| OOT AUC | 0.71 | 0.73 | +0.02 |
| Gap (KS) | 0.08 | 0.03 | -0.05 |

## 4. 最终参数

```json
{
  "max_depth": 3,
  "learning_rate": 0.08,
  "reg_alpha": 0.5,
  "reg_lambda": 1.0,
  "min_child_weight": 100,
  "subsample": 0.8,
  "colsample_bytree": 0.8,
  "n_estimators": 500
}
```

## 5. 调参结论

相比基线模型，最终模型：
- OOT KS 提升 0.02（0.16 → 0.18）
- OOT AUC 提升 0.02（0.71 → 0.73）
- Gap (KS) 降低 0.05（0.08 → 0.03）
- 稳定性显著改善，可安全部署

如需进一步探索，请给出您的调优建议。
```

---

## 与其他技能的关系

| 技能 | 职责 | 关系 |
|------|------|------|
| `xgb-modeling` | 基线建模 | 前置：需先用其训练出基线模型 |
| `model-explanation` | SHAP 解释 | 后续：调参完成后解释最优模型 |
| `model-comparison` | 多算法对比 | 平行：可与 LR/DNN 调参后做公平对比 |
| `auto-experiment` | 特征探索 | 区别：本 Skill 调参数，auto-experiment 探索特征 |

---

## 注意事项

1. **数据要求**：目标变量必须为 0/1 二分类
2. **特征要求**：需提供已筛选的特征列表（`--features` 必填）
3. **基线参数**：可传入自定义基线参数，否则使用默认值
4. **收敛判定**：连续2轮提升不足 0.001 自动停止
5. **最大轮数**：默认最多 5 轮，避免过度调优
6. **复杂 JSON**：`--params` / `--baseline` 等复杂 JSON 优先通过 `--config config.json` 传入
7. **产物位置**：模型和报告保存到 `<output_dir>/models/` 和 `<output_dir>/`


---

## Module 8: DNN深度学习建模

# DNN 深度学习建模 (portable)

基于 PyTorch 实现 MLP (Multi-Layer Perceptron) 进行二分类建模。

**核心流程**：特征标准化 → MLP 训练（BatchNorm + Dropout + Early Stopping） → 概率预测 → 三段式评估

**适用场景**：
- 高维特征交互建模
- 特征间存在复杂非线性关系
- 数据量充足（>10k 样本）
- 对模型性能有极致追求（可与 XGBoost 做 ensemble）

---

## 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` / `-d` | ✅ | - | 数据文件路径（parquet/csv） |
| `--target` / `-t` | ✅ | - | 目标变量列名（0/1 二分类） |
| `--time_col` | | `busi_dt` | 时间列名 |
| `--train_filter` | | 自动切分 | 训练集筛选条件（pandas query） |
| `--oot_filter` | | 按时间切出 | OOT 跨时间测试集条件 |
| `--oot_ratio` | | `0.20` | 未传 `--oot_filter` 时按时间切 OOT 的比例 |
| `--val_ratio` | | `0.25` | 从 train_full 切 val 的比例 |
| `--random_seed` | | `42` | 随机种子 |
| `--exclude_cols` | | - | 排除列，逗号分隔 |
| `--features` | | - | 指定特征列表，逗号分隔；不传则自动推断 |
| `--hidden_dims` | | `128,64,32` | 隐藏层维度，逗号分隔 |
| `--dropout` | | `0.3` | Dropout 比率 |
| `--learning_rate` | | `0.001` | 学习率 |
| `--batch_size` | | `512` | 批次大小 |
| `--epochs` | | `100` | 最大训练轮次 |
| `--patience` | | `10` | 早停耐心轮数 |
| `--weight_decay` | | `1e-4` | 权重衰减（L2 正则化） |
| `--pos_weight` | | `auto` | 正样本权重（auto=自动计算） |
| `--model_name` | | 自动生成 | 模型名称 |
| `--report_output` | | 自动生成 | 报告输出路径 |
| `--output_dir` | | `./outputs/<ts>` | 产物输出目录 |
| `--config` | | - | JSON 配置文件路径 |

---

## 执行方式

默认参数运行：

```bash
python scripts/modeling.py \
  --data_path ./data.parquet --target y_label \
  --time_col busi_dt \
  --exclude_cols "cust_code,busi_dt" \
  --output_dir ./outputs/dnn_run
```

自定义网络结构：

```bash
python scripts/modeling.py \
  --data_path ./data.parquet --target y_label \
  --hidden_dims "256,128,64" \
  --dropout 0.4 \
  --learning_rate 0.0005 \
  --epochs 200 \
  --output_dir ./outputs/dnn_run
```

---

## 常用场景

### 场景一：默认参数快速建模

```bash
python scripts/modeling.py --data_path ./data.parquet --target y_label --output_dir ./outputs/dnn_run
```

### 场景二：自定义网络结构

```bash
python scripts/modeling.py --data_path ./data.parquet --target y_label \
  --hidden_dims "256,128,64" --dropout 0.4 --learning_rate 0.0005 \
  --output_dir ./outputs/dnn_run
```

### 场景三：指定特征建模

```bash
python scripts/modeling.py --data_path ./data.parquet --target y_label \
  --features "feat1,feat2,feat3" --output_dir ./outputs/dnn_run
```

---

## 输出产物

1. **建模报告**（Markdown）— 含数据切分、网络结构、训练曲线、三段式评估指标、稳定性分析
2. **模型文件**（.pt）— PyTorch state_dict + 模型配置
3. **训练日志**（JSON）— 每 epoch 的 loss/AUC/KS 记录
4. **result.json** — 结构化产物清单

---

## 与其他建模 Skill 的对比

| 维度 | dnn-modeling | xgb-modeling | lr-modeling |
|------|-------------|--------------|-------------|
| 算法 | MLP (PyTorch) | XGBoost | LR + WoE |
| 特征处理 | StandardScaler | 原始值 | WoE 分箱 |
| 非线性能力 | 强（多层激活） | 强（树结构） | 弱 |
| 可解释性 | 弱 | 中（SHAP） | 强（系数） |
| 训练速度 | 慢 | 快 | 很快 |
| 适用数据量 | >10k | 任意 | 任意 |
| 评估体系 | AUC/KS/BCR/PSI | AUC/KS/BCR/PSI | AUC/KS/BCR/PSI |

---

## 上下游关系

- **前置**：`data-profiling` → `feature-analysis`（特征筛选）
- **后续**：`dnn-tuning`（调参优化）、`model-comparison`（多算法对比）
- **平行**：与 `xgb-modeling` / `lr-modeling` 可做横向对比

---

## 注意事项

1. **数据要求**：目标变量必须为 0/1 二分类
2. **数据量**：建议训练样本 > 10k，DNN 在小样本上易过拟合
3. **缺失值**：脚本自动使用中位数填充 + 添加缺失指示列
4. **标准化**：自动对数值特征做 StandardScaler 标准化
5. **早停**：当 val loss 连续 `patience` 轮不下降时自动停止
6. **不提供调参**：需要调参请切 `dnn-tuning`（搜索网络架构 + 训练参数）
7. **GPU**：自动检测 CUDA，无 GPU 时回退到 CPU
8. **模型保存**：模型文件保存到 `<output_dir>/models/`


---

## Module 9: DNN调参

# DNN 深度学习参数调优 (portable)

DNN 调参的**唯一入口**，基于 `_vendor/tuning/dnn_engine.DNNTuningEngine`。

核心设计：搜索期间缩减 epochs（加速），诊断驱动动态约束搜索空间。

---

## 调优流程

```
基线 DNN 模型 → 诊断分析(过拟合/欠拟合) → 约束空间构造 → Optuna 搜索(30 epochs) → 最优参数 → 迭代
```

---

## 执行模式

| 模式 | 触发条件 | 行为 |
|------|---------|------|
| **交互式**（默认） | 用户说"调参"/"帮我调一下DNN" | 每轮暂停等待用户反馈 |
| **AUTO** | 用户说"自动调优"/"帮我调到最优" | Agent 自动迭代直到收敛 |

**默认模式**: 交互式（更安全，用户可控）

---

## 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` / `-d` | ✅ | - | 数据文件路径（parquet/csv） |
| `--target` / `-t` | ✅ | - | 目标变量列名（0/1 二分类） |
| `--features` | | 自动推断 | 特征列表，逗号分隔 |
| `--time_col` | | `busi_dt` | 时间列名 |
| `--train_filter` | | 自动切分 | 训练集筛选条件 |
| `--val_filter` | | `val_ratio` 切出 | 验证集筛选条件 |
| `--oot_filter` | | 按时间切出 | OOT 条件 |
| `--oot_ratio` | | `0.20` | OOT 占比 |
| `--val_ratio` | | `0.25` | Val 占比 |
| `--random_seed` | | `42` | 随机种子 |
| `--exclude_cols` | | - | 排除列，逗号分隔 |
| `--n_layers` | | `3` | 隐藏层数 |
| `--layer_width` | | `128` | 首层宽度 |
| `--dropout` | | `0.3` | Dropout 率 |
| `--learning_rate` | | `0.001` | 学习率 |
| `--weight_decay` | | `1e-4` | L2 正则化 |
| `--batch_size` | | `512` | 批次大小 |
| `--epochs` | | `100` | 完整训练 epochs |
| `--search_epochs` | | `30` | 搜索期间 epochs（加速） |
| `--round` / `-r` | | `0` | 当前轮次 |
| `--max_rounds` | | `5` | 最大调优轮数 |
| `--auto` | | - | 自动调优模式（flag） |
| `--metric` | | `auc` | 评估指标 |
| `--model_name` | | 自动生成 | 模型名称 |
| `--output_dir` | | `./outputs/<ts>` | 产物输出目录 |
| `--config` | | - | JSON 配置路径 |

---

## 搜索空间

| 参数 | 类型 | 范围 | 说明 |
|------|------|------|------|
| n_layers | int | 2-4 | 隐藏层数 |
| layer_width | int | 32-256 | 首层宽度（递减结构） |
| dropout | float | 0.1-0.5 | Dropout 比率 |
| learning_rate | float(log) | 1e-4 ~ 0.01 | Adam 学习率 |
| weight_decay | float(log) | 1e-5 ~ 1e-3 | L2 正则化 |
| batch_size | categorical | 128/256/512/1024 | 批次大小 |

---

## 诊断驱动策略

| 诊断 | dropout | weight_decay | n_layers | layer_width |
|------|---------|-------------|----------|-------------|
| 过拟合 | ↑ 抬高 | ↑ 增强 | ↓ 减少 | ↓ 缩小 |
| 欠拟合 | ↓ 降低 | ↓ 减弱 | ↑ 增加 | ↑ 增大 |
| 拟合良好 | ±微调 | ±微调 | ±微调 | ±微调 |

---

## 执行方式

### 交互式模式（单轮调优）

```bash
python scripts/tuner.py \
  --data_path ./data.parquet --target y_label \
  --round 1 --output_dir ./outputs/dnn_tuning
```

### AUTO 模式（自动调优循环）

```bash
python scripts/tuner.py \
  --data_path ./data.parquet --target y_label \
  --auto --max_rounds 5 --output_dir ./outputs/dnn_tuning
```

---

## 调优策略

### 策略1：抗过拟合

**适用条件**：Train-Val Gap > 0.05

**调整方向**：
- `dropout`: 当前值 + 0.1（上限 0.5）
- `weight_decay`: 当前值 × 2
- `n_layers`: 当前值 - 1（最小为 2）
- `layer_width`: 当前值 - 32（最小为 32）

### 策略2：增强拟合

**适用条件**：Val AUC < 0.58 且 Gap < 0.03

**调整方向**：
- `n_layers`: 当前值 + 1（最大为 4）
- `layer_width`: 当前值 + 32（最大为 256）
- `weight_decay`: 当前值 × 0.5
- `learning_rate`: 当前值 × 1.2

### 策略3：精细微调

**适用条件**：Gap ∈ [0.03, 0.05]，模型状态良好

**调整方向**：
- `learning_rate`: 小幅调整 ±20%
- `dropout`: 小幅调整 ±0.05
- 其他参数保持不变

### 策略4：收敛判定

**条件**：连续2轮 Val 指标提升 < 0.001

**行为**：停止调优，输出最终结果

---

## 输出格式规范

与 xgb-tuning 保持一致的逐轮诊断报告格式。

每轮调优结束后，**必须**输出以下结构化信息：

```markdown
### 第 N 轮 DNN 调优结果

**参数变化**:
| 参数 | 上一轮 | 本轮 | 调整原因 |
|------|-------|------|----------|
| n_layers | 3 | 3 | 不变 |
| layer_width | 128 | 96 | 降低过拟合 |
| dropout | 0.3 | 0.4 | 增强正则化 |

**效果对比**:
| 指标 | 上一轮 | 本轮 | 变化 |
|------|-------|------|------|
| Val AUC | 0.72 | 0.73 | +0.01 ✓ |
| OOT AUC | 0.70 | 0.71 | +0.01 ✓ |
| Gap | 0.06 | 0.04 | -0.02 ✓ |

**诊断结论**: 轻微过拟合（Gap 下降但仍 > 0.03）

**下一步建议**: 可继续微调 dropout，或接受当前结果
```

---

## 与其他技能的关系

| 技能 | 职责 | 关系 |
|------|------|------|
| `dnn-modeling` | 基线建模 | 前置：需先用其训练出基线模型 |
| `model-comparison` | 多算法对比 | 后续：可与 XGB/LR 做公平对比 |
| `xgb-tuning` | XGBoost 调参 | 平行：同数据不同算法的调参 |

---

## 注意事项

1. **数据要求**：目标变量必须为 0/1 二分类
2. **搜索加速**：搜索期间使用 `search_epochs=30`，最终模型使用 `epochs=100`
3. **收敛判定**：连续2轮提升不足 0.001 自动停止
4. **最大轮数**：默认最多 5 轮
5. **产物位置**：模型和报告保存到 `<output_dir>/models/` 和 `<output_dir>/`


---

## Module 10: 多模型效果对比

# 多模型效果对比 (portable)

基于**同一份数据切分**，横向运行多种算法，统一评估并生成**客观事实报告**。

**设计原则（v3 重要变更）**：
- **只陈述事实，不做主观推荐**：删除了旧版的"五维加权综合评分"与"门禁淘汰"。主观权重本质上将多个不可比指标压成一个数，丢失信息并引入拍脑袋假设；门禁阈值则不同业务差异巨大。
- **Pareto 前沿（无主观权重）**：在 OOT AUC / OOT KS / BCR@10% / KS Gap / PSI 五个方向明确的目标上，识别未被任何算法严格优于的候选集。
- **LLM 推理接手**：报告末尾提供「已知事实清单 + 开放问题」，交由对话中的 AI 结合业务背景推理取舍。
- 同数据同切分 → 消除数据差异对对比结论的干扰
- 多维指标原始陈述 → OOT AUC/KS/BCR/Brier + KS Gap + PSI + 特征数 + 可解释性
- 统计显著性 → DeLong 检验回答"差距是真的还是采样噪声"

---

## 推荐工作流：先调参再对比

"哪个算法好"这个问题只有在**三个算法都调优后**对比才公平。默认超参下对比只能作为初筛。推荐三步调用：

```
1. xgb-tuning  → 产出 xgb_tuning_best_*_meta.json
2. lr-tuning   → 产出 lr_tuning_best_*_meta.json
3. dnn-tuning  → 产出 dnn_tuning_best_*_meta.json
4. model-comparison --use_tuned   → 自动扫描上述产物使用最优超参跑对比
```

---

## 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` / `-d` | ✅ | - | 数据文件路径（parquet/csv） |
| `--target` / `-t` | ✅ | - | 目标变量列名（0/1 二分类） |
| `--time_col` | | `busi_dt` | 时间列（用于 OOT 切分与分月表现） |
| `--train_filter` | | 自动切分 | 训练集筛选条件 |
| `--oot_filter` | | 按时间切出 | OOT 测试集条件 |
| `--oot_ratio` | | `0.20` | OOT 占比 |
| `--val_ratio` | | `0.25` | Val 占比 |
| `--random_seed` | | `42` | 随机种子 |
| `--exclude_cols` | | - | 排除列，逗号分隔 |
| `--features` | | - | 指定特征，逗号分隔；不传则自动推断 |
| `--algorithms` | | `xgb,lr,dnn` | 对比算法列表，逗号分隔 |
| `--scenario` | | `general` | `general` / `scorecard` / `fraud` / `stability_first` |
| `--use_tuned` | flag | 关 | 自动扫描 models 目录加载最新调参最优参数 |
| `--tuned_params_file` | | - | 显式指定 `{"xgb":{},"lr":{},"dnn":{}}` JSON |
| `--config` | | - | 手工覆盖各算法超参的 JSON（优先级高于 tuned） |
| `--model_name` | | 自动生成 | 产物名称前缀 |
| `--output_dir` | | `./outputs/<ts>` | 产物输出目录 |

---

## 场景预设（`--scenario`）

场景仅作为**业务上下文标签**，供 LLM 推理时使用；不再参与加权评分、不做门禁淘汰。

| 场景 | 描述 |
|------|------|
| `general` | 通用；首次对比探索 |
| `scorecard` | 评分卡 / 白盒合规；LR + WoE 天然占优 |
| `fraud` | 反欺诈 / 高风险；关注 OOT KS / BCR |
| `stability_first` | 存量运维；重点关注 PSI 与分月 KS |

---

## 执行方式

默认三算法 + 通用场景：

```bash
python scripts/comparison.py \
  --data_path ./data.parquet --target y_label \
  --exclude_cols "cust_code,busi_dt" \
  --output_dir ./outputs/compare
```

评分卡场景（只跑 XGB + LR）：

```bash
python scripts/comparison.py \
  --data_path ./data.parquet --target y_label \
  --algorithms "xgb,lr" --scenario scorecard \
  --output_dir ./outputs/compare
```

使用历史调参最优参数：

```bash
python scripts/comparison.py \
  --data_path ./data.parquet --target y_label \
  --use_tuned --scenario fraud \
  --output_dir ./outputs/compare
```

---

## 对比维度（原始指标，不做加权）

| 维度 | 字段 | 说明 |
|------|------|------|
| **效果** | OOT AUC / KS / Gini / BCR@10% / Precision@10% / Recall@10% / Brier / LogLoss | 全量原始指标陈列 |
| **泛化** | KS Gap = Train KS - OOT KS | 越小越好；>0.10 标记过拟合风险 |
| **稳定** | PSI（OOT vs Train 分数分布）+ 分月 KS 波动 σ | 越小越稳；≥0.25 标记显著漂移 |
| **可解释** | LR 强 / XGB 中 / DNN 弱 | 仅作文本标签，不参与计算 |
| **简洁** | 入模特征数 | 仅作参考 |

---

## 统计显著性（DeLong 检验）

两两算法 AUC 差异通过 **Fast-DeLong** 做渐近正态检验（O(N log N)，10w+ 样本也秒级完成）：

- `p < 0.05` → 差距统计显著
- `p ≥ 0.05` → 差距可能是采样波动

---

## 输出产物

1. **对比报告**（Markdown，倒金字塔结构）：
   - 执行摘要（客观指标速览 + Pareto 前沿标记，**无推荐列**）
   - 多算法叠加曲线（ROC/KS/Lift）
   - 数据概览
   - 详细指标总表（train/val/oot × 8 指标）
   - **Pareto 前沿候选集**（无主观权重）
   - DeLong 显著性检验
   - 稳定性（真实 PSI + 分月 KS）
   - 样本级一致性（Top-K Jaccard / Spearman / 分歧数）
   - 跨算法特征重叠（Jaccard + 共识特征）
   - 每算法独立评估图
   - **LLM 推理引导**：事实清单 + 开放问题，交由对话中的 AI 推理取舍
   - 各算法适用场景背景知识

2. **各模型文件**：XGB(.json) / LR(.joblib) / DNN(.pt，含 imputer+scaler 元数据)

---

## 与其他技能的关系

| 技能 | 职责 | 关系 |
|------|------|------|
| `xgb-tuning` / `lr-tuning` / `dnn-tuning` | 调参优化 | 前置：公平对比前需先调参 |
| `xgb-modeling` / `lr-modeling` / `dnn-modeling` | 基线建模 | 被复用训练对比模型 |
| `model-explanation` | 模型解释 | 后续：对比完成后解释最优模型 |

---

## 注意事项

1. **公平对比**："哪个算法好"只有在三个算法都调优后对比才公平
2. **同数据同切分**：本技能确保所有算法使用完全相同的数据切分
3. **DeLong 检验**：p < 0.05 才认为差距统计显著
4. **Pareto 前沿**：只识别未被任何算法严格优于的候选集，不做主观排序
5. **场景标签**：`--scenario` 仅作文本标签，不参与加权评分
6. **产物位置**：模型和报告保存到 `<output_dir>/`


---

## Module 11: 模型解释

# 模型解释报告 (portable)

基于 SHAP (SHapley Additive exPlanations) 对 XGBoost 模型进行可解释性分析，生成包含可视化图表的 Markdown 报告。

---

## 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--model_path` | ✅ | - | XGBoost 模型文件路径 (.json) |
| `--data_path` | ✅ | - | 数据文件路径（parquet/csv） |
| `--target` | ✅ | - | 目标变量列名 |
| `--features` | | *auto* | 特征列表，逗号分隔。不传时从 `<model>_meta.json` 自动读取 |
| `--sample_id` | | - | 单样本解释：样本索引或ID |
| `--sample_filter` | | - | 单样本解释：pandas query 条件 |
| `--top_n` | | `20` | 全局解释显示 Top N 特征 |
| `--interaction_features` | | - | 交互分析特征对，如 `f1,f2` |
| `--output_dir` | | `./outputs/<ts>` | 产物输出目录 |
| `--output_name` | | `model_explanation_report` | 报告基名 |
| `--config` | | - | JSON 配置文件路径 |

---

## 执行方式

```bash
python scripts/explainer.py \
  --model_path ./models/my_model.json \
  --data_path ./examples/toy.parquet \
  --target y_label \
  --output_dir ./outputs/explain_run
```

单样本解释：

```bash
python scripts/explainer.py \
  --model_path ./models/my_model.json \
  --data_path ./examples/toy.parquet \
  --target y_label \
  --sample_id 1001 \
  --output_dir ./outputs/explain_run
```

特征交互分析：

```bash
python scripts/explainer.py \
  --model_path ./models/my_model.json \
  --data_path ./examples/toy.parquet \
  --target y_label \
  --interaction_features "age,income" \
  --output_dir ./outputs/explain_run
```

---

## 常用场景

### 场景一：全局特征重要性分析

解释模型整体决策逻辑：

```bash
python scripts/explainer.py --model_path ./models/my_model.json \
  --data_path ./examples/toy.parquet --target y_label \
  --output_dir ./outputs/explain_run
```

输出：
- SHAP Summary Plot（特征重要性排序）
- SHAP Bar Plot（平均绝对 SHAP 值）
- 特征重要性表格

### 场景二：单样本预测解释

解释特定样本的预测原因：

```bash
python scripts/explainer.py --model_path ./models/my_model.json \
  --data_path ./examples/toy.parquet --target y_label \
  --sample_id 1001 --output_dir ./outputs/explain_run
```

输出：
- SHAP Force Plot（推动预测的正负特征）
- 瀑布图（特征贡献分解）
- 该样本特征值与分布对比

### 场景三：特征交互分析

分析两个特征的交互效应：

```bash
python scripts/explainer.py --model_path ./models/my_model.json \
  --data_path ./examples/toy.parquet --target y_label \
  --interaction_features "age,income" --output_dir ./outputs/explain_run
```

输出：
- SHAP Dependence Plot（特征值 vs SHAP 值）
- 交互热力图

---

## 跨 skill 串联（推荐流程）

`xgb-modeling` 产物的 `result.json` 中 `role=model` 的 path 可直接喂给 `model-explanation`：

```bash
# 1) 训练
python ../xgb-modeling/scripts/modeling.py \
  --data_path ./examples/toy.parquet --target y_label \
  --exclude_cols "cust_code" --output_dir ./outputs/mdl

# 2) 从 result.json 提模型路径
MODEL=$(jq -r '.files[] | select(.role=="model") | .path' ./outputs/mdl/result.json)

# 3) 解释（特征自动从 <model>_meta.json 读取）
python scripts/explainer.py \
  --model_path "$MODEL" \
  --data_path ./examples/toy.parquet --target y_label \
  --output_dir ./outputs/xpl
```

---

## 特征列表来源

1. `--features "f1,f2,..."` 显式传入
2. `config.json` 中 `"features": [...]`
3. **自动发现** `<model>_meta.json`（xgb-modeling 产物自带）

---

## 报告输出结构

生成的 `model_explanation_report.md` 包含以下章节：

| 章节 | 内容 |
|------|------|
| 1. 模型概览 | 模型路径、特征数量、样本规模 |
| 2. 全局特征解释 | SHAP Summary Plot、Top N 特征重要性表 |
| 3. 单样本解释 | Force Plot、瀑布图、特征值对比（如指定样本） |
| 4. 特征交互分析 | Dependence Plot、交互效应说明（如指定） |
| 5. 可视化附件 | 生成的 PNG 图表文件列表 |

---

## 产物目录

```
<output_dir>/
├── model_explanation_report.md
└── assets/
    ├── shap_summary.png
    ├── shap_bar.png
    ├── force_plot_sample_1001.png
    └── dependence_age_income.png
```

---

## 与其他技能的关系

| 技能 | 职责 | 关系 |
|------|------|------|
| `xgb-modeling` | 训练模型 | 前置：需先用其训练并保存模型 |
| `model-comparison` | 多算法对比 | 后续：可与 LR/DNN 模型做对比解释 |
| `feature-analysis` | 特征分析 | 区别：feature-analysis 分析建模前特征质量 |

---

## 依赖

- `shap`、`matplotlib`（图表）
- `xgboost`、`pandas`、`numpy`

---

## 注意事项

1. **模型格式**：仅支持 XGBoost JSON 格式模型文件
2. **数据一致性**：`--data_path` 需与训练时使用的数据字段一致
3. **样本定位**：`--sample_id` 为数据框的整数索引，非业务ID
4. **内存占用**：大数据集的全局 SHAP 计算可能耗时较长
5. **图表依赖**：需要 matplotlib 和 shap 库支持
6. **base_score 兼容**：XGBoost >= 1.7 的 `base_score` 为数组，脚本会自动修复为标量以兼容 SHAP


---

## Module 12: 自主实验循环

# 自主实验循环 (portable)

自动发现数据中的特征分组，执行四阶段渐进式探索实验，每轮完整展示探索逻辑和量化结果。

---

## 核心理念

借鉴 autoresearch 的自主循环思想，升级为**组级探索**：

```
发现特征组 → 组独立评估 → 组间叠加 → 组级消融 → 精细筛选
```

---

## 四阶段探索流程

### Phase 1: 特征组独立评估
- 自动发现数据中的特征分组（按前缀聚合: `firefly_*`, `mob3_*`, `umeng_*` 等）
- 逐组单独建模，评估每组的独立预测能力
- 输出各组的独立 AUC/KS 排名

### Phase 2: 组间增量叠加
- 从 Phase 1 表现最佳的组开始
- 逐步叠加下一个最强组，观察边际增量
- 找到最优组合点

### Phase 3: 组级消融分析
- 从全量特征出发，逐组移除
- 量化每个组的不可替代性
- 如果移除后指标不降，说明该组信息已被其他组覆盖

### Phase 4: 组内精细筛选
- 在最优组合内，逐个尝试移除特征
- 剔除冗余特征，精简模型

---

## 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` | ✅ | - | 数据文件路径（parquet/csv） |
| `--target` | ✅ | - | 目标变量列名（0/1 二分类） |
| `--exploration` | ✅ | - | 探索方向描述，如 "不同特征组对mob3逾期的贡献" |
| `--max_rounds` | | `5` | 最大实验轮数 |
| `--metric` | | `ks` | 优化指标（auc/ks） |
| `--direction` | | `maximize` | 优化方向（maximize/minimize） |
| `--significance` | | `2.0` | 显著性阈值（MAD倍数） |
| `--baseline_features` | | - | 基线特征列表，JSON格式（默认使用全量特征） |
| `--time_col` | | `busi_dt` | 时间列名 |
| `--train_filter` | | - | 训练集筛选条件 |
| `--val_filter` | | - | 验证集筛选条件 |
| `--test_filter` | | - | [Deprecated] 等价 `--val_filter`，仅作向后兼容 |
| `--oot_filter` | | - | OOT测试集条件 |
| `--val_ratio` | | `0.25` | val 在 train_full 内占比 |
| `--oot_ratio` | | `0.20` | OOT 在全量内占比 |
| `--output_dir` | | `./outputs/<ts>` | 产物输出目录 |
| `--config` | | - | JSON 配置文件 |

---

## 执行方式

```bash
python scripts/run_experiment.py \
  --data_path ./data.parquet --target y_label \
  --exploration "不同特征组(firefly/子模型/友盟)对mob3逾期的贡献" \
  --max_rounds 10 \
  --output_dir ./outputs/exp
```

---

## 常用场景

### 场景一：探索各特征组贡献

```bash
python scripts/run_experiment.py \
  --data_path ./data.parquet --target y_label \
  --exploration "不同特征组(firefly模型/子模型/友盟数据)对mob3逾期预测的贡献" \
  --max_rounds 10 --output_dir ./outputs/exp
```

### 场景二：探索特定时间窗口特征

```bash
python scripts/run_experiment.py \
  --data_path ./data.parquet --target y_label \
  --exploration "mob3相关的逾期、还款特征" \
  --max_rounds 8 --output_dir ./outputs/exp
```

### 场景三：在已有基线上探索新组

```bash
python scripts/run_experiment.py \
  --data_path ./data.parquet --target y_label \
  --baseline_features '["feat1","feat2","feat3"]' \
  --exploration "添加mob6时间窗口特征组" \
  --max_rounds 5 --output_dir ./outputs/exp
```

---

## 输出内容

> **核心原则：每轮必须完整输出探索逻辑和结果**
> 禁止只输出最终汇总。每一轮实验完成后，**必须**立即输出：探索策略、推理逻辑、假设描述、新增/移除特征、训练指标详情、与基线的对比、显著性检验、决策理由。

### 数据概览（实验开始前）

- 数据规模、特征数、正样本率
- 自动发现的特征分组及其统计

### 单轮输出格式（每轮必须使用）

```markdown
### Round N/总轮数

**Phase X: 探索策略名称**

**探索逻辑**:
[Phase 1/3/5] 特征组独立评估
目标: 单独测试「firefly」组的 12 个特征
逻辑: 先让每个特征组独立上场，获得各组的独立贡献排名

**本轮假设**: 独立评估特征组「firefly」(12个特征)

**模型评估** (共 12 个特征):
| 指标 | Train | Test | 基线Test | 变化 |
|------|-------|------|----------|------|
| AUC | 0.812 | 0.735 | 0.726 | +0.009 |

**Top-5 特征重要性**:
| # | 特征 | 重要性 |
|---|------|--------|
| 1 | firefly_score [NEW] | 0.2341 |

**显著性检验**: [PASS] 2.3x MAD → 改进显著
**决策**: [+] KEEP - 改进显著
```

### 最终汇总（所有轮次后输出）

- 实验总览表（Round/阶段/假设/指标/决策）
- 最终 vs 基线对比
- 保留和丢弃的特征组/特征列表
- 下一步建议

---

## 统计显著性检验

使用 MAD (Median Absolute Deviation) 判断改进是否显著：

| 置信度 | 标记 | 含义 |
|--------|------|------|
| ≥ 2.0× | [PASS] | 改进可能是真实的 |
| 1.0-2.0× | [EDGE] | 高于噪声但边缘 |
| < 1.0× | [FAIL] | 在噪声范围内 |

---

## 与其他技能的关系

| 技能 | 职责 | 关系 |
|------|------|------|
| `xgb-modeling` | 单次训练和评估 | 被本技能复用 |
| `xgb-tuning` | 超参调优 | 可在循环后使用 |
| `feature-analysis` | 特征分析 | 辅助假设生成 |

---

## 注意事项

1. **探索方向**：可以是宽泛的（如"探索各特征组贡献"），系统会自动发现分组
2. **轮数建议**：设置为特征组数的2-3倍（如6个组建议10-15轮），以覆盖多个探索阶段
3. **基线策略**：默认使用全量特征作为基线，也可指定特定特征集
4. **显著性阈值**：默认2.0×，数据量小时可适当降低
5. **可打断**：用户可随时停止，已有结果会保留
6. **产物位置**：报告和模型保存到 `<output_dir>/`


---

## Module 13: 分群建模

# 分群自主探索 (portable)

在用户指定或 AI 自主发现的分群策略下，拆分客群训练子模型，自动探索最优分群方案。

**核心理念**：

```
探索空间（策略 × 参数 × 组合）
        │
        ▼
Try → Measure → Keep/Discard → Repeat
        │
        ▼
    最优分群方案 + 子模型
```

---

## 三种分群策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| **规则分群** | 用户指定规则（如 `age < 30`） | 有业务先验知识 |
| **聚类分群** | K-Means 等无监督自动发现 | 探索数据内在结构 |
| **决策树分群** | 有监督找最优分割点 | 直接优化目标变量 |

---

## 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` | ✅ | - | 数据文件路径（parquet/csv） |
| `--target` | ✅ | - | 目标变量列名（0/1 二分类） |
| `--mode` | | `auto` | 模式: `auto`(自主探索) / `manual`(指定策略) |
| `--max_rounds` | | `5` | 自主探索最大轮数 |
| `--segment_rules` | | - | 规则分群，JSON格式 |
| `--segment_col` | | - | 直接指定分群列名 |
| `--n_clusters` | | `3` | 聚类分群数 |
| `--tree_depth` | | `2` | 决策树分群深度 |
| `--tree_features` | | - | 决策树使用的特征，逗号分隔 |
| `--min_segment_ratio` | | `0.05` | 最小分群占比（<5%会警告） |
| `--merge_strategy` | | `route` | 汇总策略: `route` / `stacking` |
| `--metric` | | `ks` | 优化指标（auc/ks） |
| `--significance` | | `2.0` | 显著性阈值（MAD倍数） |
| `--time_col` | | `busi_dt` | 时间列名 |
| `--train_filter` | | - | 训练集筛选条件 |
| `--val_filter` | | - | 验证集筛选条件 |
| `--output_dir` | | `./outputs/<ts>` | 产物输出目录 |
| `--config` | | - | JSON 配置文件 |

---

## 执行方式

### 自主探索最优分群

```bash
python scripts/run_segment.py \
  --data_path ./data.parquet --target y_label \
  --mode auto --max_rounds 5 \
  --output_dir ./outputs/seg
```

### 用户规则分群

```bash
python scripts/run_segment.py \
  --data_path ./data.parquet --target y_label \
  --mode manual \
  --segment_rules '{"年轻": "age < 30", "中年": "age >= 30 and age < 50", "高龄": "age >= 50"}' \
  --output_dir ./outputs/seg
```

### 聚类自动分群

```bash
python scripts/run_segment.py \
  --data_path ./data.parquet --target y_label \
  --mode manual --n_clusters 4 \
  --output_dir ./outputs/seg
```

### 决策树分群

```bash
python scripts/run_segment.py \
  --data_path ./data.parquet --target y_label \
  --mode manual \
  --tree_depth 3 --tree_features "age,income,credit_score" \
  --output_dir ./outputs/seg
```

---

## 输出内容

### 实时进度（流式输出）

```
━━━ Round 1/5: 基线（不分群）━━━
单一模型 AUC: 0.742

━━━ Round 2/5: 用户规则分群 ━━━
规则: age < 30 | 30-50 | > 50
分群样本: [12,340 | 18,560 | 14,288]
子模型 AUC: [0.71 | 0.75 | 0.78]
汇总 AUC: 0.758 (+2.2%)
决策: ✅ KEEP

━━━ Round 3/5: 决策树分群 (depth=2) ━━━
自动分割: income < 5000 → ...
汇总 AUC: 0.772 (+1.8%)
决策: ✅ KEEP (新最佳!)
```

### 最终报告

- 最优分群方案详情
- 各策略对比表
- 子模型列表及指标
- vs 基线提升幅度
- 分群稳定性分析（PSI）

---

## 评估标准

| 指标 | 说明 | 阈值 |
|------|------|------|
| 整体 AUC | 分群模型汇总后效果 | 越高越好 |
| vs 基线 | 相比不分群的提升 | > 0 |
| 分群稳定性 | OOT分群比例变化 | PSI < 0.1 |
| 最小覆盖率 | 最小群占比 | > 5% |

---

## 与其他技能的关系

| 技能 | 职责 | 关系 |
|------|------|------|
| `xgb-modeling` | 单模型训练 | 被复用训练子模型 |
| `auto-experiment` | 特征探索 | 可在分群后对各群独立优化 |
| `feature-analysis` | 特征分析 | 辅助选择分群特征 |

---

## 注意事项

1. **分群数量**：建议 2-5 群，太多易过拟合
2. **最小样本量**：每群建议 > 5% 总样本
3. **稳定性**：关注 OOT 分群比例是否稳定
4. **业务可解释**：决策树分群规则更易解释
5. **组合使用**：可先分群再对各群做特征探索


---

## Module 14: DeepModel深度集成

# XGBoost DeepModel — 分群集成建模 (portable)

分群训练多个 XGBoost 子模型，通过 OOF Stacking 融合成主模型，评估集成收益。

---

## 阶段1：训练分群子模型

### 参数说明

> 参数 spec：`_vendor/xgb_cli.py` 中 `domain=deepmodel-sub`。复杂嵌套 JSON（segments / features_per_segment / pos_weight_per_segment）**必须**走 `--config`。

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` / `-d` | ✅ | - | 数据文件路径 |
| `--target` / `-t` | ✅ | - | 目标变量列名 |
| `--segments` | ✅* | - | 分群条件 JSON（**推荐通过 `--config` 的 `segments` 字段**） |
| `--segment_col` | ✅* | - | 按列唯一值自动分群（与 segments 二选一） |
| `--time_col` | | `busi_dt` | 时间列名 |
| `--train_filter` | | 自动切分 | 全局训练集筛选条件 |
| `--val_filter` | | `val_ratio` 切出 | 全局验证集筛选条件 |
| `--oot_filter` | | 按时间切出 | OOT 测试集条件 |
| `--exclude_cols` | | - | 排除列，逗号分隔 |
| `--features` | | 自动筛选 | 全局特征列表，逗号分隔 |
| `--features_per_segment` | | - | 分群差异化特征 JSON（**走 `--config`**） |
| `--sample_weight_col` | | - | 样本权重列名 |
| `--pos_weight_per_segment` | | - | 各分群正样本权重 JSON（**走 `--config`**） |
| `--auto` | | `false` | flag。对 OOT Gap > 0.05 的分群自动调参 |
| `--output_dir` | | `./outputs/<ts>` | 子模型保存目录 |
| `--config` | | - | JSON 配置路径 |

### 执行方式

```bash
python scripts/sub_trainer.py \
  --data_path ./data.parquet --target y_label \
  --time_col busi_dt --exclude_cols "cust_code,busi_dt" \
  --auto --output_dir ./outputs/deepmodel
```

配合 `--config` 传入结构化 JSON：

```json
{
  "segments": {"高风险": "risk_score > 500", "低风险": "risk_score <= 500"},
  "pos_weight_per_segment": {"高风险": 2.0, "低风险": 1.0}
}
```

```bash
python scripts/sub_trainer.py \
  --data_path ./data.parquet --target y_label \
  --auto --config ./config.json --output_dir ./outputs/deepmodel
```

### 输出

- 每个分群的模型文件：`{output_dir}/{segment_name}.json`
- Markdown 报告：各分群 Train/Val/OOT AUC/KS/Gap 对比表、质量门控检查结果

---

## 阶段2：Stacking 融合

### 参数说明

> 参数 spec：`domain=deepmodel-stack`。`submodel_paths` / `segments` 等结构化 JSON **走 `--config`**。

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` / `-d` | ✅ | - | 数据文件路径 |
| `--target` / `-t` | ✅ | - | 目标变量列名 |
| `--submodel_paths` | ✅ | - | 子模型路径 JSON 列表（**走 `--config`**） |
| `--segments` | ✅* | - | 与 sub_trainer 一致的分群条件 |
| `--segment_col` | ✅* | - | 与 sub_trainer 一致的分群列 |
| `--time_col` | | `busi_dt` | 时间列名 |
| `--train_filter` | | 自动切分 | 训练集条件（与 sub_trainer 一致） |
| `--val_filter` | | `val_ratio` 切出 | 验证集条件 |
| `--oot_filter` | | 按时间切出 | OOT 条件 |
| `--cv_folds` | | `5` | OOF 交叉验证折数 |
| `--output_dir` | | `./outputs/<ts>` | Meta-learner 保存目录 |
| `--config` | | - | JSON 配置路径 |

### 执行方式

```bash
python scripts/stacker.py \
  --data_path ./data.parquet --target y_label \
  --cv_folds 5 --output_dir ./outputs/deepmodel
```

配合 `--config`：

```json
{
  "submodel_paths": ["./outputs/deepmodel/高风险.json", "./outputs/deepmodel/低风险.json"],
  "segments": {"高风险": "risk_score > 500", "低风险": "risk_score <= 500"}
}
```

```bash
python scripts/stacker.py \
  --data_path ./data.parquet --target y_label \
  --config ./config.json --output_dir ./outputs/deepmodel
```

### 输出

- Meta-learner 模型文件：`{output_dir}/stack_meta.json`
- OOF 预测分分布图（各子模型 OOF AUC vs Meta-learner）

---

## 阶段3：集成对比报告

### 参数说明

> 参数 spec：`domain=deepmodel-compare`。

| 参数 | 必选 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--data_path` / `-d` | ✅ | - | 数据文件路径 |
| `--target` / `-t` | ✅ | - | 目标变量列名 |
| `--stack_model_path` | | - | Stacking 模型路径（可选） |
| `--submodel_paths` | ✅ | - | 子模型路径 JSON 列表（**走 `--config`**） |
| `--segments` | ✅* | - | 分群条件 |
| `--segment_col` | ✅* | - | 分群列 |
| `--time_col` | | `busi_dt` | 时间列名 |
| `--train_filter` | | 自动切分 | 训练集条件 |
| `--val_filter` | | `val_ratio` 切出 | 验证集条件 |
| `--oot_filter` | | 按时间切出 | OOT 条件 |
| `--baseline_model_path` | | - | 单模型基线路径（不传则自动训练一个全量基线） |
| `--extra_baseline_algos` | | - | 额外单模型基线算法，逗号分隔（可选值：`lr,dnn`） |
| `--output_dir` | | `./outputs/<ts>` | 产物保存目录 |
| `--config` | | - | JSON 配置路径 |

### 执行方式

```bash
python scripts/comparator.py \
  --data_path ./data.parquet --target y_label \
  --stack_model_path ./outputs/deepmodel/stack_meta.json \
  --output_dir ./outputs/deepmodel
```

配合 `--config`：

```json
{
  "submodel_paths": ["./outputs/deepmodel/高风险.json", "./outputs/deepmodel/低风险.json"],
  "segments": {"高风险": "risk_score > 500", "低风险": "risk_score <= 500"}
}
```

```bash
python scripts/comparator.py \
  --data_path ./data.parquet --target y_label \
  --stack_model_path ./outputs/deepmodel/stack_meta.json \
  --config ./config.json --output_dir ./outputs/deepmodel
```

### 输出

- 对比表：**单模型 XGB 基线 / （可选 LR 基线 / DNN 基线）/ 最优子模型 / Stacking 集成**（Train/Val/OOT AUC/KS/Gap）
- 每个分群在各模型下的 OOT KS 对比
- 最终推荐：是否 Stacking / 最优子模型 / 基线

> 提示：如需**严格的多算法公平对比（含调参）**，请切换回 Agent 模式调用 `xgb-tuning → lr-tuning → dnn-tuning → model-comparison --use_tuned`。本技能的 `--extra_baseline_algos` 仅走默认超参，定位为"低成本初筛对照"。

---

## 完整工作流示例

```bash
# 阶段1：训练分群子模型
python scripts/sub_trainer.py \
  --data_path ./data.parquet --target y_label \
  --config ./config.json --auto --output_dir ./outputs/deepmodel

# 阶段2：Stacking 融合
python scripts/stacker.py \
  --data_path ./data.parquet --target y_label \
  --config ./config.json --output_dir ./outputs/deepmodel

# 阶段3：集成对比报告
python scripts/comparator.py \
  --data_path ./data.parquet --target y_label \
  --stack_model_path ./outputs/deepmodel/stack_meta.json \
  --config ./config.json --output_dir ./outputs/deepmodel
```

---

## 质量门控标准

| 检查项 | 标准 | 不达标处理 |
|--------|------|-----------|
| 各分群样本量 | ≥ 500 | 建议合并该分群 |
| 各分群 OOT Gap | < 0.05 | 启用 `--auto` |
| Stacking OOT AUC | ≥ max(子模型 OOT AUC) - 0.01 | 说明集成无明显增益 |
| 集成 vs 基线 OOT AUC | 集成更高 | 建议放弃集成，用最优子模型或基线 |

---

## 与其他技能的关系

| 技能 | 职责 | 关系 |
|------|------|------|
| `xgb-modeling` | 单模型训练 | 被复用训练子模型和基线 |
| `segment-modeling` | 分群策略探索 | 区别：segment-modeling 探索最优分群，本 Skill 按指定分群做 Stacking |
| `model-comparison` | 多算法公平对比 | 后续：严格对比请用 model-comparison（含调参） |

---

## 注意事项

1. **分群互斥**：各分群条件应互斥（一个样本只属于一个分群），否则 Stacking 会有信息泄漏
2. **样本量**：每个分群的训练样本应 ≥ 500，过少的分群建议合并
3. **OOF 生成**：Stacking 的 OOF 预测在各分群内独立做 k-fold，保证无标签泄漏
4. **Meta-learner**：固定使用保守参数（max_depth=2），不做超参搜索，避免过拟合
5. **子模型路径传递**：stacker 和 comparator 支持从 `--config` 读取子模型路径
6. **三阶段顺序**：必须先 sub_trainer → stacker → comparator，阶段间通过文件系统传递产物

---

## Disclaimer / 免责声明

> ⚠️ **重要声明**
> - 本技能提供参考框架和分析建议，不构成任何形式的投资建议、法律意见或专业判断
> - 所有分析结果仅供参考，最终决策须由具备相应资质的专业人员作出
> - 用户应结合实际情况独立判断