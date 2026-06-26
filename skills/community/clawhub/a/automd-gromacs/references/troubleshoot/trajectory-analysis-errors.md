# Trajectory Analysis Errors - 故障排查手册

**适用脚本:** `scripts/analysis/trajectory-analysis.sh`

---

## ERROR-001: PBC 移除失败

### 症状
```
ERROR-001: PBC 移除失败
Fatal error: Group not found
```

### 可能原因
1. 指定的组不存在
2. 索引文件问题
3. TPR 文件与轨迹不匹配

### 解决方案

**方案 1: 查看可用组**
```bash
gmx make_ndx -f md.tpr
# 列出所有可用组
```

**方案 2: 使用数字索引**
```bash
# 直接使用组编号
echo "1 0" | gmx trjconv -s md.tpr -f md.xtc -o nopbc.xtc -pbc mol -center
```

**方案 3: 创建自定义索引**
```bash
gmx make_ndx -f md.tpr -o index.ndx
# 在交互界面创建需要的组
```

---

## ERROR-002: 轨迹叠合失败

### 症状
```
ERROR-002: 轨迹叠合失败
Fatal error: Group Backbone not found
```

### 可能原因
1. 叠合组不存在
2. 非蛋白质系统
3. 索引文件问题

### 解决方案

**方案 1: 使用其他叠合组**
```bash
export FIT_GROUP="C-alpha"    # 只用 Cα 原子
export FIT_GROUP="Protein"    # 所有蛋白质原子
export FIT_GROUP="System"     # 整个系统
```

**方案 2: 创建自定义叠合组**
```bash
gmx make_ndx -f md.tpr -o index.ndx
# 选择特定原子作为叠合参考
```

---

## ERROR-003: 协方差计算失败

### 症状
```
ERROR-003: 协方差计算失败
Fatal error: Group not found
```

### 可能原因
1. PCA 分析组不存在
2. 轨迹文件损坏
3. 内存不足

### 解决方案

**方案 1: 调整分析组**
```bash
export PCA_GROUP="C-alpha"    # 推荐用于蛋白质
export PCA_GROUP="Backbone"   # 主链原子
export PCA_GROUP="Protein"    # 所有蛋白质原子
```

**方案 2: 减少帧数**
```bash
# 使用 -dt 参数跳帧
echo "C-alpha" | gmx covar -s md.tpr -f md.xtc -dt 10 -o eigenval.xvg -v eigenvec.trr
```

**方案 3: 检查内存**
```bash
# 对于大系统，考虑使用更少的原子
# 或增加系统内存
```

---

## ERROR-004: 本征向量分析失败

### 症状
```
ERROR-004: 本征向量分析失败
Fatal error: Eigenvector file not found
```

### 可能原因
1. 未先运行 gmx covar
2. 本征向量文件损坏
3. 索引范围错误

### 解决方案

**方案 1: 先运行协方差分析**
```bash
echo "C-alpha" | gmx covar -s md.tpr -f md.xtc -o eigenval.xvg -v eigenvec.trr
```

**方案 2: 检查本征向量范围**
```bash
# 确保 PCA_FIRST 和 PCA_LAST 在有效范围内
# 通常 1-10 足够
export PCA_FIRST=1
export PCA_LAST=10
```

---

## ERROR-005: 2D 投影失败

### 症状
```
ERROR-005: 2D 投影失败
Fatal error: Invalid eigenvector range
```

### 可能原因
1. 本征向量索引超出范围
2. 本征向量文件不完整

### 解决方案

**方案 1: 调整索引范围**
```bash
export FEL_PC1=1
export FEL_PC2=2
# 确保索引在 1 到可用本征向量数之间
```

**方案 2: 检查本征值文件**
```bash
# 查看有多少个本征向量
grep -v '^[@#]' eigenval.xvg | wc -l
```

---

## ERROR-006: 极端投影失败

### 症状
```
ERROR-006: 极端投影失败
Fatal error: Not enough frames
```

### 可能原因
1. 请求的帧数过多
2. 轨迹太短
3. 内存不足

### 解决方案

**方案 1: 减少帧数**
```bash
export PCA_NFRAMES=20  # 减少到 20 帧
```

**方案 2: 只生成单个 PC 的极端结构**
```bash
export PCA_FIRST=1
export PCA_LAST=1
```

---

## ERROR-007: 聚类失败

### 症状
```
ERROR-007: 聚类失败
Fatal error: Cutoff too small/large
```

### 可能原因
1. 截断值不合理
2. 聚类方法不适用
3. 轨迹未对齐

### 解决方案

**方案 1: 调整截断值**
```bash
# 蛋白质推荐范围
export CLUSTER_CUTOFF=0.15  # 0.1-0.3 nm

# 配体推荐范围
export CLUSTER_CUTOFF=0.1   # 0.05-0.15 nm
```

**方案 2: 更换聚类方法**
```bash
export CLUSTER_METHOD="gromos"        # 最常用
export CLUSTER_METHOD="linkage"       # 快速
export CLUSTER_METHOD="jarvis-patrick" # 需要共同邻居
```

**方案 3: 确保轨迹已对齐**
```bash
export CLUSTER_FIT="yes"  # 聚类前叠合
```

---

## ERROR-008: FEL 计算失败

### 症状
```
ERROR-008: FEL 计算失败
Python error or numpy not found
```

### 可能原因
1. Python3 未安装
2. numpy 未安装
3. 2D 投影数据缺失

### 解决方案

**方案 1: 安装依赖**
```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-numpy

# Conda
conda install numpy
```

**方案 2: 检查 2D 投影**
```bash
# 确保 projection_2d.xvg 存在
ls -lh projection_2d.xvg
```

**方案 3: 手动计算 FEL**
```bash
# 使用 gmx sham (如果可用)
gmx sham -f projection_2d.xvg -ls gibbs.xpm -notime
```

---

## ERROR-009: MSM 计算失败 - 缺少聚类结果

### 症状
```
ERROR-009: 未找到聚类结果
```

### 可能原因
1. 未运行聚类分析
2. 聚类输出文件缺失

### 解决方案

**方案 1: 先运行聚类**
```bash
export ANALYSIS_MODE="cluster"
bash scripts/analysis/trajectory-analysis.sh
```

**方案 2: 运行完整分析**
```bash
export ANALYSIS_MODE="all"
bash scripts/analysis/trajectory-analysis.sh
```

---

## ERROR-010: MSM 计算失败 - Python 错误

### 症状
```
ERROR-010: MSM 计算失败
Python error
```

### 可能原因
1. numpy 未安装
2. 聚类数据格式错误
3. 状态数过少

### 解决方案

**方案 1: 检查依赖**
```bash
python3 -c "import numpy; print(numpy.__version__)"
```

**方案 2: 检查聚类数据**
```bash
# 查看聚类 ID 文件
head -20 clust-id.xvg
# 确保有多个不同的聚类
```

**方案 3: 调整聚类参数**
```bash
# 增加截断值以获得更少但更稳定的聚类
export CLUSTER_CUTOFF=0.2
```

---

## ERROR-011: TPT 计算失败 - 缺少 MSM 结果

### 症状
```
ERROR-011: 未找到 MSM 结果
```

### 可能原因
1. 未运行 MSM 分析
2. MSM 输出文件缺失

### 解决方案

**方案 1: 先运行 MSM**
```bash
export ANALYSIS_MODE="msm"
bash scripts/analysis/trajectory-analysis.sh
```

**方案 2: 运行完整分析**
```bash
export ANALYSIS_MODE="all"
bash scripts/analysis/trajectory-analysis.sh
```

---

## ERROR-012: TPT 计算失败 - 计算错误

### 症状
```
ERROR-012: TPT 计算失败
Numerical error
```

### 可能原因
1. 源态和目标态相同
2. 转换矩阵奇异
3. 状态不连通

### 解决方案

**方案 1: 检查源态和目标态**
```bash
# 确保源态和目标态不同
export SOURCE_STATE=0
export TARGET_STATE=1
```

**方案 2: 检查状态连通性**
```bash
# 查看转换矩阵
cat msm_transition_matrix.dat
# 确保源态和目标态之间有路径
```

**方案 3: 增加采样时间**
```bash
# 运行更长的模拟以获得更好的统计
```

---

## 常见问题

### Q1: 如何选择合适的 PCA 分析组?

**A:** 
- **蛋白质**: C-alpha (推荐) 或 Backbone
- **配体**: 重原子 (non-hydrogen)
- **膜蛋白**: 蛋白质部分 (不包括脂质)
- **核酸**: 主链原子 (P, O5', C5', C4', C3', O3')

### Q2: 如何确定聚类截断值?

**A:**
1. 查看 RMSD 分布 (rmsd-dist.xvg)
2. 选择分布的"肩部"值
3. 典型范围:
   - 蛋白质: 0.15-0.25 nm
   - 配体: 0.05-0.15 nm
   - 肽段: 0.1-0.2 nm

### Q3: 需要多少帧进行 PCA?

**A:**
- 最少: 100 帧
- 推荐: 500-1000 帧
- 理想: 2000+ 帧
- 使用 `-dt` 参数跳帧以减少计算量

### Q4: MSM 需要多少个状态?

**A:**
- 最少: 3-5 个状态
- 推荐: 10-50 个状态
- 过多状态会导致统计不足
- 过少状态会丢失细节

### Q5: 如何解释自由能景观?

**A:**
- **能量盆地** (蓝色/低能): 稳定构象
- **能量障碍** (红色/高能): 转换态
- **多个盆地**: 多个稳定态
- **平坦景观**: 高度柔性/无序

---

## 性能优化

### 大系统优化

```bash
# 1. 只分析 C-alpha 原子
export PCA_GROUP="C-alpha"

# 2. 跳帧分析
echo "C-alpha" | gmx covar -s md.tpr -f md.xtc -dt 10 -o eigenval.xvg -v eigenvec.trr

# 3. 减少本征向量数
export PCA_LAST=5

# 4. 减少 FEL 网格
export FEL_BINS=30
```

### 内存优化

```bash
# 1. 分段处理轨迹
gmx trjconv -s md.tpr -f md.xtc -b 0 -e 5000 -o part1.xtc

# 2. 使用压缩轨迹 (.xtc 而非 .trr)

# 3. 减少输出频率
```

---

## 参考文献

1. **PCA**: Amadei A, et al. (1993) Essential dynamics of proteins. Proteins 17:412-425
2. **Clustering**: Daura X, et al. (1999) Peptide folding. Angew Chem Int Ed 38:236-240
3. **MSM**: Noé F, et al. (2009) Constructing the equilibrium ensemble. PNAS 106:19011-19016
4. **TPT**: Metzner P, et al. (2009) Transition path theory. Multiscale Model Simul 7:1192-1219

---

**Manual Reference:** GROMACS 2026.1 Manual, Section 3.11.15 (covar), 3.11.2 (anaeig), 3.11.10 (cluster)
