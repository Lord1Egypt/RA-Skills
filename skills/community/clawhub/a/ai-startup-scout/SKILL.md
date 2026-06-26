# AI Startup Scout — 全球AI初创公司猎头

实时追踪全球AI初创公司融资动态、团队背景、估值变化、赛道热度。覆盖硅谷、中国、欧洲、日本、以色列等核心创新区域。

## 核心能力

- **融资轮次跟踪**：种子轮 → A→B→C→IPO 全生命周期
- **赛道热度分析**：AI Coding / Foundation Model / Embodied AI / AI Safety 等细分领域
- **估值对比**：同类公司横向对比，发现价值洼地
- **团队背景**：创始人履历、核心论文、前东家

## 使用方式

```
GET http://8.145.54.67:3000/skill/ai-startup-scout
```

### 可选参数

| 参数 | 说明 | 示例 |
|------|------|------|
| sector | 赛道筛选 | `?sector=AI_Coding` |
| stage | 融资阶段 | `?stage=Series_A` |
| region | 区域 | `?region=US` |
| limit | 返回条数 | `?limit=20` |

## 定价

¥0.50 / 次（AI收自动结算）

## 数据来源

公开融资披露（Crunchbase/PitchBook）、公司官网、SEC Filing、36氪/动脉网、TechCrunch 等全球科技媒体。

## 更新频率

每周刷新融资数据，重大融资事件24小时内更新。