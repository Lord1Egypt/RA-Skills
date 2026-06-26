# diepre-vision-cognition

> DiePre 视觉认知 Skill —— 将包装/模切机器视觉与 SOUL 推理深度融合

**作者**: KingOfZhao  
**版本**: 1.1.0  
**发布日期**: 2026-03-31  
**许可证**: MIT

---

## 这个 Skill 解决什么问题？

DiePre（模切压痕）质检场景中，传统视觉模型给出"是/否"二值判断，无法说明为什么、不确定时也不求助人类。  
`diepre-vision-cognition` 将 SOUL 框架注入视觉感知层：

- 从四个视觉角度碰撞推理，避免单角度误判
- 区分「确定缺陷」和「需人工复核」，置信度 < 90% 自动升级
- 所有检测结果写入日志，实现质检记忆
- 人工标注反馈后持续进化，越用越准

## 快速安装

```bash
clawhub install diepre-vision-cognition
```

## 核心 API

```python
from skills.diepre_vision_cognition import DiePrevisionCognition

vision = DiePrevisionCognition(workspace=".")

# 单图检测
result = vision.analyze("path/to/dieline.png")
print(f"置信度: {result.confidence:.1%}")
print(f"缺陷: {result.defects}")
if result.requires_human_review:
    print("⚠️ 需要人工复核")

# 注入人工反馈
vision.add_human_label(
    image_id="dieline_20260331_001",
    label="crack",
    notes="左下角 3mm 裂缝，光线不足时容易漏检"
)
```

## 四向视觉碰撞原理

```
正视角  →  标准光照下的边缘检测
    ↓
反转180° →  旋转后重新检测（发现非对称缺陷）
    ↓
侧光增强 →  斜射光下的浮凸/压痕深度分析
    ↓
整体布局 →  全图构图分析（尺寸比例、对齐误差）
    ↓
    加权融合 → 最终置信度
```

## 变更日志

### v1.1.0 (2026-03-31)
- 新增学术参考文献（5篇精选arXiv论文）
- VLM→CAD技术路线引入（照片→DXF升级路径）
- 具身推理VLA作为未来"照片→动作决策"方向
- ICCV 2025 CAD Task Solver引入

### v1.0.0 (2026-03-31)
- 初始发布
- 四向视觉碰撞框架实现
- 通过自验证置信度: 96%

---

*开源认知 Skill by KingOfZhao*
