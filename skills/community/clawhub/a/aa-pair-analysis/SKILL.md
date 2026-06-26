---
name: aa-pair-analysis
description: 蛋白质氨基酸功能类别相邻对频率分析。对任意蛋白质家族的多物种序列进行多序列比对（MSA）、共识序列提取、对型统计和配方计算，输出Top5高频对型及φ值。适用于：（1）对新物种/类群运行完整分析流程，（2）从已有共识序列进行对型统计，（3）横向比较不同物种/类群的氨基酸对组成差异，（4）修改氨基酸分类或统计参数后重新分析。适用于任何蛋白质家族。
---

# 氨基酸对频率分析（aa-pair-analysis）

## 首次使用：环境初始化

**首次调用本 skill 前，先运行初始化脚本**，自动检测并安装所有依赖：

```bash
bash skills/aa-pair-analysis/scripts/setup.sh
```

脚本会依次检查并安装：

| 依赖 | 说明 | 自动安装方式 |
|------|------|------------|
| Python 3.8+ | 运行分析脚本 | 需手动预装 |
| pandas | 数据处理与CSV输出 | `pip install pandas` |
| biopython | 序列处理（可选） | `pip install biopython` |
| ClustalOmega | 多序列比对（MSA） | apt / brew / conda / 二进制下载 |

> 如果环境已配置好，跳过此步骤直接运行分析即可。

---

## 联合分析（与关键片段预测联动）

当同时需要氨基酸对频率分析 + 蛋白质关键片段预测时，使用联合分析包装器，**MSA 只执行一次**，并**自动生成单体配方投料表**。

```bash
cd skills/aa-pair-analysis

# 联合分析（自动整合 + 自动生成投料表）
python scripts/run_combined_analysis.py 任务名 数据目录
```

工作流：
1. 共享 MSA（clustalo，缓存复用）
2. aa-pair 分析（跳过已比对物种）
3. 关键片段预测（跳过已完成物种）
4. 整合物种结果（按物种合并两份分析结果）
5. **自动生成单体配方投料表 Word 文档**

### 单体配方投料表生成

联合分析完成后自动调用：

```bash
python scripts/gen_monomer_formulation_table.py 整合结果目录
```

**投料规则（2026-05-11 更新）**：
- 单体总浓度：**1.0 M**
- 最终总体积：**1.5 mL**
- DMSO：根据单体总投料量**动态补全**至 1.5 mL
- 总摩尔数 = 1.0 M × 0.0015 L = **1.5 mmol**
- 各单体按 φ 值比例分配 1.5 mmol
- 引发剂 2-oxoglutaric acid：**3.75 mg**（MW 146.10）
- 交联剂：**不使用**

**单体对照**：
| 氨基酸类别 | 单体 | M (g/mol) | 密度/浓度 |
|-----------|------|-----------|-----------|
| Hydrophobic | BA | 128.17 | 0.90 g/mL |
| Nucleophilic | HEA | 116.12 | 1.10 g/mL |
| Aromatic | PEA | 192.21 | 1.10 g/mL |
| Amide | AAm | 71.08 | 0.18 g/mL |
| Acidic | CBEA | 144.13 | 1.10 g/mL |
| Cationic | ATAC (80%) | 193.67 | 1.15 g/mL |

输出：横向A4 Word 文档，按分类分表，含斑马纹。

---

## 核心文件

- **分析脚本（完整流程）**: `scripts/species_analysis_workflow.py`（FASTA→MSA→结果）
- **联合分析包装器**: `scripts/run_combined_analysis.py`（MSA共享 + 自动整合 + 自动投料表）
- **投料表生成器**: `scripts/gen_monomer_formulation_table.py`（Word文档生成）
- **结果整合工具**: `scripts/integrate_species_results.py`（按物种合并两份分析结果）
- **方法详情**: `references/method.md`
- **氨基酸分类**: `references/classification.md`

## 快速运行

```bash
cd skills/aa-pair-analysis

# 从原始FASTA完整流程（MSA→共识→对分析）
python scripts/species_analysis_workflow.py 任务名 数据目录 --threshold 0.5

# 断点续传
python scripts/species_analysis_workflow.py 任务名 数据目录 --resume 已有结果目录
```

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--threshold` | 0.5 | 共识序列保守性阈值（最高频氨基酸占比≥该值才写入，否则标X） |
| `--resume` | 无 | 指定已有结果目录，从断点继续 |

## 输出文件

| 文件 | 内容 |
|------|------|
| `species_formulations.csv` | 每个类群的Top5对型、φ值、21种对型计数 |
| `top_5_pairs_details.csv` | Top5对型逐条明细 |
| `formulation_summary.csv` | 总类群数、独特配方数 |

## 氨基酸分类（固定，不可更改）

详见 `references/classification.md`。

**参与统计（17种）**：Hydrophobic(V,L,I,M) / Nucleophilic(S,T,C) / Aromatic(F,Y,W) / Amide(N,Q) / Acidic(D,E) / Cationic(H,K,R)

**排除（不统计）**：X、A（丙氨酸）、G（甘氨酸）、P（脯氨酸）

## 计数方法（已验证，不可更改）

1. 剔除共识序列中所有 X/A/G/P，直接拼接为新序列
2. 统计新序列所有相邻对（有方向）
3. 合并对称对（N-H + H-N → H-N）得21种无向对型
4. 按计数排名选Top5

## 修改分析参数时的注意事项

- **修改氨基酸分类**：同步更新 `scripts/run_pdf_analysis.py` 和 `scripts/species_analysis_workflow.py` 中的 `FUNCTIONAL_CLASSES` 字典
- **修改阈值**：使用 `--threshold` 参数，无需改代码
- **修改计数方法**：Step3（过滤拼接）和Step5（对称合并）需同步修改两个脚本

