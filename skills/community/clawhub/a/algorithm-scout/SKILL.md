---
name: "algorithm-scout"
description: "独创的智能优化算法推荐系统，根据问题特征精准推荐 WOA/GWO/SOA/GOA/MFO/BAS/CVX/波束形成等算法"
---

# Algorithm Scout Skill

独创的智能优化算法推荐系统，根据用户描述的优化问题需求，精准推荐最合适的算法。

## 核心功能

1. **问题特征识别** - 自动分析问题类型（连续/离散、凸/非凸、有约束/无约束、维度等）
2. **智能算法推荐** - 根据特征匹配最合适的算法
3. **推荐理由说明** - 解释为什么推荐该算法
4. **参数使用建议** - 提供具体的参数配置建议
5. **代码位置指引** - 指向本地算法实现文件

## 算法库覆盖

### 元启发式算法 (7 种)
- **WOA**: 鲸鱼优化 - 全局搜索强、参数少
- **GWO**: 灰狼优化 - 收敛速度快
- **SOA**: 海鸥优化 - 全局搜索能力强
- **GOA**: 蝗虫优化 - 社交互动机制独特
- **MFO**: 蛾焰优化 - 螺旋机制、平衡性好
- **FireWorks**: 烟花算法 - 多样性保持好
- **BAS**: 细菌觅食 - 一维搜索高效（神经网络）

### 凸优化工具
- **CVX**: MATLAB 凸优化建模（SDP/SOCP/LP/QP）

### 阵列信号处理 (5 种)
- **Capon/MVDR**: 高分辨率 DOA 估计
- **LCMV**: 多约束波束形成
- **LMS/RLS**: 实时自适应滤波
- **SMI**: 块自适应波束形成

## 推荐逻辑

1. **凸优化** → CVX
2. **阵列信号** → Capon/LCMV/RLS
3. **神经网络** → BAS
4. **连续优化** → WOA/GWO/SOA/MFO
5. **高维问题** → GOA/FireWorks

## 使用示例

**用户**: 50 维连续全局优化，推荐算法？

**推荐**:
- 🎯 首选：WOA（种群 30-50，迭代 500-1000）
- 🥈 备选：GWO（收敛快）
- 🥉 备选：MFO（多峰表现好）

**用户**: BP 神经网络权重优化？

**推荐**:
- 🎯 BAS（专门用于神经网络）
- 🥈 WOA/GWO（备选）

**用户**: 阵列波束形成，提高 DOA 分辨率？

**推荐**:
- 🎯 Capon (MVDR)（高分辨率）
- 🥈 LCMV（多约束）
- 🥉 RLS/LMS（实时场景）

**用户**: 凸优化问题，带线性约束？

**推荐**:
- 🎯 CVX（建模简洁，自动求解）

## 文件位置

- 算法库：`/home/ym/.openclaw/workspace/Algorithm/algorithm_library.md`
- WOA: `/home/ym/.openclaw/workspace/Algorithm/WOA/`
- GWO: `/home/ym/.openclaw/workspace/Algorithm/all/WOLF/GWO/`
- BAS: `/home/ym/.openclaw/workspace/Algorithm/BAS_BP/`
- CVX: `/home/ym/.openclaw/workspace/Algorithm/cvx/`
- Beamforming: `/home/ym/.openclaw/workspace/Algorithm/Beamforming-Algorithm/`
