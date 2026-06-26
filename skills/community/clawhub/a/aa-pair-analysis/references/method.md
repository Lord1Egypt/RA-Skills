# 完整分析方法

## 环境依赖

| 依赖 | 用途 | 安装 |
|------|------|------|
| Python 3.8+ | 运行分析脚本 | 预装 |
| pandas | CSV读写 | `pip install pandas` |
| ClustalOmega (`clustalo`) | Step 1 多序列比对 | 见下方 |

**ClustalOmega 安装：**
```bash
# Linux (apt)
sudo apt-get install clustalo

# macOS (Homebrew)
brew install clustal-omega

# Conda（跨平台）
conda install -c bioconda clustalo

# 或运行 skill 自带初始化脚本（自动选择合适方式）
bash scripts/setup.sh
```

---

## 目录
1. [总体流程](#总体流程)
2. [Step 1: 多序列比对（MSA）](#step-1-多序列比对)
3. [Step 2: 提取共识序列](#step-2-提取共识序列)
4. [Step 3: 序列过滤与拼接](#step-3-序列过滤与拼接)
5. [Step 4: 统计有向相邻对](#step-4-统计有向相邻对)
6. [Step 5: 合并对称对与Top5排名](#step-5-合并对称对与top5排名)
7. [Step 6: 计算φ值](#step-6-计算φ值)
8. [输出格式](#输出格式)

---

## 总体流程

```
原始蛋白序列（FASTA，每分类群N条）
        │
        ▼  Step 1: 多序列比对（MSA，ClustalOmega）
比对矩阵（等长，gap='-'）
        │
        ▼  Step 2: 提取共识序列（保守性阈值过滤）
共识序列（低保守位点标X）
        │
        ▼  Step 3: 剔除X/A/G/P → 直接拼接
纯净连续序列
        │
        ▼  Step 4: 统计有向相邻对（最多36种）
        │
        ▼  Step 5: 合并对称对（21种）→ 按计数取Top5
        │
        ▼  Step 6: 计算φ值
        │
        ▼  输出CSV
```

---

## Step 1: 多序列比对

**工具：** ClustalOmega

```bash
clustalo -i <物种.fasta> -o <物种_aligned.fasta> --outfmt=fasta --force
```

**结果：** 所有序列等长，不同位置用 `-` 填充，每列对应同源位置。

---

## Step 2: 提取共识序列

```python
def _calculate_consensus(sequences, threshold=0.5):
    for 每列 i:
        valid = {aa: count for aa, count in Counter(seq[i] for seq in sequences).items()
                 if aa != '-'}                          # 忽略gap
        best_aa    = max(valid, key=valid.get)
        best_ratio = valid[best_aa] / sum(valid.values())

        共识[i] = best_aa if best_ratio >= threshold else 'X'

    return ''.join(共识).replace('-', '')
```

**阈值说明（`--threshold`，默认0.5）：**

| 阈值 | 含义 | 效果 |
|------|------|------|
| 0.5（默认） | 最高频氨基酸需占≥50% | 与文献推测一致 |
| 0.3 | 宽松 | 更少X，有效序列更长 |
| 0.7 | 严格 | 更多X，仅高度保守位点保留 |
| 0.0 | 无过滤 | 强制选最高频，不产生X |

---

## Step 3: 序列过滤与拼接

**规则：** 删除 X、A、G、P，剩余字符**直接拼接**（不保留位置关系）：

```
共识：  M  A  A  L  K  X  X  X  S  R  P  D  V
排除：     ×  ×        ×  ×  ×           ×
新序列：M  L  K  S  R  D  V
```

> ⚠️ 拼接后原本被X/A/G/P隔开的残基成为直接相邻关系。  
> 此处理方式已通过与文献逐对型对比验证（完全一致）。

**代码实现：**
```python
EXCLUDE = set('XAGP')
filtered_seq = ''.join(aa for aa in consensus_seq if aa not in EXCLUDE)
```

---

## Step 4: 统计有向相邻对

```python
for i in range(len(filtered_seq) - 1):
    cls_i = AA_TO_CLASS[filtered_seq[i]]
    cls_j = AA_TO_CLASS[filtered_seq[i + 1]]
    pair_counts[(cls_i, cls_j)] += 1
    total_pairs += 1
```

最多 **36种有向对型**（6×6，方向区分）。

---

## Step 5: 合并对称对与Top5排名

```python
# 合并对称对（字母序较小的在前）
sym_counts = defaultdict(int)
for (ci, cj), cnt in pair_counts.items():
    sym_key = tuple(sorted([ci, cj]))
    sym_counts[sym_key] += cnt

# 按计数排名取Top5
top5 = sorted(sym_counts.items(), key=lambda x: -x[1])[:5]
```

**21种无向对型：**

```
Ac-Ac  Ac-Am  Ac-Ar  Ac-C   Ac-H   Ac-N
       Am-Am  Am-Ar  Am-C   Am-H   Am-N
              Ar-Ar  Ar-C   Ar-H   Ar-N
                     C-C    C-H    C-N
                            H-H    H-N
                                   N-N
```

---

## Step 6: 计算φ值

```
Ni（某类别）= Top5中含该类别的所有对型计数之和（双侧计）
φ = Ni / (Top5总对数 × 2) × 100%
```

**示例逻辑（以某对型 H-N 为例）：**
- H-N 对型计数为 k
- H 的 Ni += k，N 的 Ni += k
- 每个对型对两侧类别各贡献一次

---

## 输出格式

### species_formulations.csv

| 列组 | 列名 |
|------|------|
| 基础 | `species`, `total_pairs`, `top_5_pairs`, `top_5_percentage` |
| φ值 | `{类别}_Ni`, `{类别}_phi`（×6类，共12列） |
| 计数 | `count_{对型}`（×21种，共21列） |

**总列数：** 4 + 12 + 21 = **37列**

### top_5_pairs_details.csv

| 列名 | 说明 |
|------|------|
| `species` | 分类群名称 |
| `rank` | 排名（1～5） |
| `pair` | 对型名称（如 Hydrophobic-Nucleophilic） |
| `count` | 合并后计数 |
| `frequency_percent` | 占总对数比例（%） |

### formulation_summary.csv

| 列名 | 说明 |
|------|------|
| `total_species` | 总类群数 |
| `unique_formulations` | 独特配方（Top5组合）数 |
| `duplicate_formulations` | 与其他类群共享配方的类群数 |
