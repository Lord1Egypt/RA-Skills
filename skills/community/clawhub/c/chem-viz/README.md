# chem-viz 化学可视化引擎

> v1.1.0 | 米赋AI教育 | MIT-0 License
> 状态：生产可用（v1.1解决file://协议CDN空白问题）

## 一句话定位

将抽象化学过程转化为**交互式可视化HTML页面**，让学生"看见"化学——分子转得起来、电子流看得见、平衡拉得动、流程拆得开。

## 支持9类可视化

| 类型 | 技术方案 | 典型应用 |
|------|---------|---------|
| 分子结构3D | **纯Canvas2D+手动3D数学**（零依赖） | VSEPR构型、配合物 |
| 有机分子3D | 纯Canvas2D | 官能团高亮、反应位点 |
| 晶胞结构 | 纯Canvas2D | 均摊法计数、晶体密度 |
| 氧化还原过程 | Canvas+动画引擎 | 电子转移动画、化合价标注 |
| 电化学 | Canvas+SVG | 原电池/电解池电子流向 |
| 化学平衡 | JSXGraph | 浓度/温度滑块+实时曲线 |
| 离子平衡 | JSXGraph | pH曲线、水解、沉淀溶解 |
| 工艺流程 | SVG+交互 | 流程逐步展开+原理标注 |
| 实验装置 | SVG+Canvas | 仪器组装、操作模拟 |

## 核心踩坑经验（v1.1重点）

- **3Dmol.js/Three.js CDN在file://协议下被CORS阻止**→页面空白。v1.1起分子3D改用**纯Canvas2D+手动3D数学**（rotX/rotY旋转+透视投影+径向渐变球体+z排序遮挡），零外部依赖100%可靠
- 技术优先级：**纯Canvas2D > 经典script CDN > ES Module importmap（file://下必失败）**

## 质量保障

- 每个产物必须暴露测试API `window.__CHEMVIZ_STATE`（ready/error/version）
- **两级验证**：Level 1语法验证（scripts/verify_output.sh）→ Level 2功能验证（交互/数值/渲染）
- 生成前9项执行自检清单

## 快速上手

```
触发语示例：
- "把NaCl晶胞画出来，我要演示均摊法"
- "可视化这个原电池的电子流向"
- （chem-coach遇到分子结构/平衡/电化学题时自动调用）
```

## 依赖

无硬依赖。JSXGraph/Three.js为可选CDN增强（仅HTTP服务器环境）。与chem-coach配套使用效果最佳。

## 版本

- v1.1.0 分子3D改纯Canvas2D，移除CDN依赖，解决file://空白
- v1.0.0 初版：7类可视化+两级验证+与chem-coach集成
