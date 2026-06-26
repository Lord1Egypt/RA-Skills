# 机甲/机器人运动场景提示词模板

## 必需元素清单

- [ ] 机甲/机器人类型（人形/兽形/载具形态）
- [ ] 体型比例（人类尺寸/巨型/超巨型）
- [ ] 运动类型（行走/奔跑/飞行/变形）
- [ ] 关节运动风格（流畅/机械顿挫/液压驱动）
- [ ] 质量感表现（轻盈/沉重/压迫地面）
- [ ] 动力系统视觉效果（喷射/电弧/蒸汽/能量核心）
- [ ] 表面材质（金属反光/做旧锈蚀/碳纤维/能量护盾）
- [ ] 环境互动（脚步震动/地面碎裂/气流扰动）

## 缺失检测规则

如果用户未指定以下要素，必须主动询问：
1. **运动质感**: "机甲的运动风格是什么？像高达那样流畅敏捷，还是像太平洋机甲那样沉重有力？"
2. **体型参照**: "机甲有多大？和人差不多大，还是可以踩扁汽车的巨型机器人？"
3. **关节细节**: "需要展示关节的机械细节吗？比如液压杆伸缩、齿轮转动、管线联动等。"
4. **环境反馈**: "机甲的运动是否需要影响环境？比如踏步碎裂地面、奔跑掀起沙尘等。"

## 示例 Prompt

### 输入
"一个巨型机器人从海里走上岸"

### 优化后 Prompt (LumaAI 适配)
```
Epic wide shot of a colossal humanoid mech rising from the ocean,
water cascading off its massive metallic frame. Camera starts at
water level, slowly craning upward to reveal the full towering
height. Each step sends enormous waves crashing against the
shoreline. Hydraulic joints hiss with steam as the legs lift from
the seabed, barnacles and seaweed clinging to the armor plates.
The mech's chest reactor glows with pulsing blue energy through
the water streaming down its torso. Heavy foot impacts create
small earthquakes on the beach, sand and debris flying upward.
Sunset backlighting creates a dramatic silhouette with rim light
on the wet metal surfaces. Volumetric mist and sea spray catch
golden light beams. Cinematic scale, photorealistic, IMAX quality.
```

## 机甲运动关键要素

### 质量感 (Weight & Mass)
| 级别 | 表现方式 | 参考作品 |
|------|---------|---------|
| 轻盈 | 快速移动、灵巧闪避、最小环境影响 | 全金属狂潮 |
| 标准 | 适度步伐、机械音效、轻微震动 | 高达系列 |
| 沉重 | 慢速行走、地面碎裂、建筑物震颤 | 太平洋机甲 |
| 超重 | 每步间隔长、地震级影响、环境大规模破坏 | 哥斯拉 MechaGodzilla |

### 关节运动类型
- **球形关节**: 流畅多方向旋转（如肩部、髋部）
- **铰链关节**: 单轴折叠（如膝盖、肘部）
- **滑动关节**: 线性伸缩（如液压臂、伸缩天线）
- **万向节**: 小范围多轴（如腕部、颈部）
- **变形关节**: 重新排列组合（如变形金刚）

### 动力效果
- **喷射推进**: 蓝白色火焰尾迹、热变形空气
- **电弧放电**: 蓝紫色电弧在关节间闪烁
- **蒸汽释放**: 关节处的高压蒸汽喷射
- **能量核心**: 胸腔/背部的发光核心脉冲
- **粒子引擎**: 全身散发的能量粒子流
