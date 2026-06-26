# 系统平衡报告

**生成时间:** 2026-05-22 09:45:34

---

## 输入参数

- **输入结构:** em.gro
- **拓扑文件:** topol.top
- **温度:** 300 K
- **压强:** 1.0 bar
- **位置约束:** posre (力常数: 1000 kJ/mol/nm^2)

---

## NVT 平衡 (恒温)

- **步数:** 2500 ( ps)
- **输出文件:** nvt.gro, nvt.cpt, nvt.edr
- **温度曲线:** nvt_temperature.xvg

### 温度统计
```
平均温度: 299.64 K
```

---

## NPT 平衡 (恒温恒压)

- **步数:** 2500 ( ps)
- **输出文件:** npt.gro, npt.cpt, npt.edr
- **压强曲线:** npt_pressure.xvg
- **密度曲线:** npt_density.xvg

### 压强统计
```
平均压强: 282.08 bar
```

### 密度统计
```
平均密度: 1025.09 kg/m^3
```

---

## 输出文件

### 结构文件
- `nvt.gro` - NVT 平衡后的结构
- `npt.gro` - NPT 平衡后的结构 (用于生产运行)

### 检查点文件
- `nvt.cpt` - NVT 检查点
- `npt.cpt` - NPT 检查点 (用于继续模拟)

### 能量文件
- `nvt.edr` - NVT 能量轨迹
- `npt.edr` - NPT 能量轨迹

### 分析文件
- `nvt_temperature.xvg` - 温度曲线
- `npt_pressure.xvg` - 压强曲线
- `npt_density.xvg` - 密度曲线

---

## 下一步

系统已完成平衡,可以进行生产运行:

```bash
# 使用 npt.gro 和 npt.cpt 作为起点
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
gmx mdrun -v -deffnm md
```

---

**状态:** ✅ 平衡完成
