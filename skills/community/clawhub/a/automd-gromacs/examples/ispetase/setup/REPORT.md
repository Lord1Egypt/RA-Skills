# 系统准备报告

## 输入
- PDB 文件: protein_clean.pdb
- 力场: amber99sb-ildn
- 水模型: tip3p

## 系统组成
- 蛋白质原子: 0
- 水分子: 10127
- Na+ 离子: 31
- Cl- 离子: 32
- 总原子数: 0

## 盒子
- 类型: dodecahedron
- 尺寸: 7.89038 nm
- 距离: 1.2 nm

## 能量最小化
- 最终势能: -498744 kJ/mol
- 收敛状态: 已收敛

## 输出文件
- 系统坐标: system.gro
- 拓扑文件: topol.top
- 能量最小化: em.gro, em.edr
- 运行输入: em.tpr

## 下一步
系统已准备好进行平衡模拟:
```bash
# 使用 equilibration.sh
./equilibration.sh --input em.gro --topology topol.top --output ./equilibration
```

## 质量检查
- [ ] 检查势能是否为负值
- [ ] 检查是否有 LINCS 警告
- [ ] 可视化检查系统 (pymol system.gro)

---
生成时间: Fri May 22 09:41:02 CST 2026
