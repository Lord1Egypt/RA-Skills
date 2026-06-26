# free-energy-analysis 故障排查

适用脚本: `scripts/analysis/free-energy-analysis.sh`

目标: 对 BAR/FEP、WHAM/PMF、AWH 结果做统一整理、误差评估和质量判读。

---

## ERROR-001: `gmx` 不可用，无法重算 BAR/WHAM/AWH

症状:
- 日志出现 `gmx bar failed` / `gmx wham failed` / `gmx awh failed`
- 但脚本本身未崩溃，只退化为读取已有结果

原因:
- 当前环境未 `source GMXRC`
- 机器上只有结果文件，没有 GROMACS 可执行程序

修复:
```bash
source /path/to/GMXRC
which gmx
gmx --version
```

说明:
- 本脚本优先“真实可用”，所以即使 `gmx` 不可用，也会尝试直接解析已有 `pmf.xvg` / `bar.xvg` / `awh_pmf.xvg`。
- 若你需要重新 bootstrap 或重新收敛分析，必须提供可运行的 `gmx`。

---

## ERROR-002: BAR 输入不足

症状:
- 报告中 `Input files: 0` 或 `1`
- BAR 部分被跳过

原因:
- `gmx bar` 至少需要多个相邻 lambda 窗口的数据
- `--bar-pattern` 没匹配到文件

修复:
```bash
bash scripts/analysis/free-energy-analysis.sh \
  --mode bar \
  --bar-pattern 'freeenergy_results/lambda_*/dhdl*.xvg'
```

建议:
- 使用明确 pattern，避免误把无关 `xvg` 当成 BAR 输入
- 输入应覆盖完整 lambda 邻接窗口，而不是只给单个窗口

---

## ERROR-003: WHAM 没有收敛

症状:
- 报告中 `WHAM convergence: no`
- `wham.log` 出现 `did not converge`

常见原因:
- 相邻窗口重叠不足
- 边缘窗口采样不够
- 反应坐标间距过大
- 伞状力常数过强或过弱

优先修复:
```bash
# 1) 增加采样时间，优先补边缘窗口
# 2) 减小窗口间距，例如 0.1 -> 0.05 nm
# 3) 检查 pullf 列表是否完整
# 4) 提高 bootstrap 前先确保原始 PMF 收敛
```

经验阈值:
- 相邻窗口重叠最好 > 30%
- 边缘窗口更容易漂移，通常需要更长采样

---

## ERROR-004: PMF 曲线很粗糙 / baseline drift 大

症状:
- 报告中 `roughness` 偏高
- `baseline_drift` 绝对值 > 5 kJ/mol
- PMF 出现锯齿、非物理尖峰、端点抬升

原因:
- 采样不足或相关性强
- 个别窗口中心偏移
- 反应坐标不够描述真实过程
- PBC/拉伸方向定义错误

修复顺序:
1. 先看 `hist.xvg`，确认不是窗口重叠问题
2. 检查各窗口 `pullx.xvg` 是否围绕目标中心稳定振荡
3. 增加窗口采样时长，尤其是峰顶和端点附近
4. 若反应坐标存在隐藏慢自由度，考虑二维坐标或改用 AWH/Metadynamics

---

## ERROR-005: bootstrap 误差没有生成

症状:
- `bootstrap_error = NA`
- 没有 `bsres.xvg`

原因:
- `gmx wham` 未成功运行 bootstrap
- 只提供了现成 `pmf.xvg`，但没有重新运行 `gmx wham`
- PMF 第三列本身不含误差

修复:
```bash
bash scripts/analysis/free-energy-analysis.sh \
  --mode wham \
  --wham-tpr-list umbrella/tpr_files.dat \
  --wham-pullf-list umbrella/pullf_files.dat \
  --bootstrap 500
```

说明:
- 没有 `tpr/pullf` 列表时，脚本只能读取已有 PMF，无法凭空生成 bootstrap 误差。

---

## ERROR-006: block averaging 没有结果

症状:
- 报告中 `Block average stderr: NA`

原因:
- 没有提供 `--series`
- 数据点少于 block 数
- 输入文件不是标准两列/多列数值格式

修复:
```bash
bash scripts/analysis/free-energy-analysis.sh \
  --mode summary \
  --series umbrella/windows/window_00/pullx.xvg \
  --blocks 5
```

建议:
- 对 block averaging，优先用单窗口的 `pullx.xvg`、`dhdl.xvg`、AWH 相关时间序列
- block 数不宜过多；通常 4-8 比较稳妥

---

## ERROR-007: AWH 只有建议，没有定量 PMF

症状:
- AWH 部分只有 `stage` 和 `recommendation`
- 没有 `awh_pmf.xvg`

原因:
- 只提供了 `md.log`，没提供 `md.edr` 或 PMF 文件
- 当前 GROMACS 版本/编译不支持 `gmx awh`

修复:
```bash
bash scripts/analysis/free-energy-analysis.sh \
  --mode awh \
  --awh-edr awh_run/md.edr \
  --awh-log awh_run/md.log
```

判读重点:
- AWH 的关键不只是“跑完”，而是目标分布覆盖、偏置更新稳定、后 1/3 PMF 与前段是否一致

---

## ERROR-008: 多方法结果互相矛盾

症状:
- BAR ΔG 与 PMF 积分/反应趋势明显不一致
- AWH 的自由能谷位置和 WHAM 差很多

优先排查:
1. 是否比较的是同一个热力学量
2. restraint 定义是否一致
3. 反应坐标是否遗漏关键慢变量
4. lambda 路径与 PMF 路径是否描述同一物理过程
5. 是否仍处于非收敛阶段

实践建议:
- 先比较趋势，再比较绝对值
- 只有在采样充分、误差重叠时，才把“多方法一致”当作强证据

---

## 推荐工作流

### 1. Umbrella 结果复核
```bash
bash scripts/analysis/free-energy-analysis.sh \
  --mode wham \
  --input-dir umbrella \
  --wham-tpr-list umbrella/tpr_files.dat \
  --wham-pullf-list umbrella/pullf_files.dat \
  --series umbrella/windows/window_00/pullx.xvg
```

### 2. FEP/BAR 结果汇总
```bash
bash scripts/analysis/free-energy-analysis.sh \
  --mode bar \
  --bar-pattern 'freeenergy_results/lambda_*/dhdl*.xvg'
```

### 3. 统一汇总多个方法
```bash
bash scripts/analysis/free-energy-analysis.sh \
  --mode all \
  --input-dir results \
  --bar-pattern 'results/lambda_*/dhdl*.xvg' \
  --wham-tpr-list results/tpr_files.dat \
  --wham-pullf-list results/pullf_files.dat \
  --awh-log results/md.log \
  --awh-edr results/md.edr
```

---

## 最后判读原则

- **先看采样质量，再看自由能数值**
- **先看 overlap / convergence，再谈势垒高度**
- **bootstrap 小不代表可靠；系统误差和坐标选择错误更危险**
- **多方法一致是加分项，但前提是每种方法本身都过了质量检查**
