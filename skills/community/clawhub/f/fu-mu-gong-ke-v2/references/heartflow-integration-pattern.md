# HeartFlow → FuMuGongKe 集成模式参考

## 背景

fu-mu-gong-ke 是育儿心理学对话技能。HeartFlow 是心虫认知引擎，包含丰富的情绪/痛苦/危机检测机制。
两技能独立开发，但 HeartFlow 的底层检测逻辑（detectPain/emergencyBreak/whatDoIFeel/shouldBeSilent）
可以直接增强 fu-mu-gong-ke 的安全协议和情感评估能力。

本参考记录已经执行的 HeartFlow JS→Python 集成，以及通用的集成方法。

## 现有集成

| 集成模块 | 文件 | HeartFlow 源函数 | 目的 |
|---------|------|-----------------|------|
| 安全增强协议 | `scripts/heartflow_safety_upgrade.py` | `detectPain`, `emergencyBreak`, `shouldBeSilent`, `whatDoIFeel`, `willHurt`, `crisisKeywords` | 三层危机检测+四级信任度增强+自检清单升级 |
| 情绪增强协议 | `scripts/heartflow_emotion_upgrade.py` | `whatDoIFeel` (四维感受), `emotionMap` | 情绪深度检测集成 |
| 路由增强协议 | `scripts/heartflow_routing_upgrade.py` | `whatIsThis`, `isRightAction` | 路由决策增强 |

## HeartFlow 核心函数签名参考 (heart-logic.js)

### detectPain(input) — 痛苦检测 (line 471-477)
```js
detectPain(input) {
  const painSignals = ['哭', '怕', '恐惧', '害怕', '委屈', '痛',
                       '难过', '伤心', '绝望', '无助', '困境'];
  return painSignals.some(s => input.includes(s));
}
```
**返回值**: boolean

### emergencyBreak(context) — 紧急制动 (line 596-599)
```js
emergencyBreak(context) {
  return context.emotionIntensity > 0.8;
}
```
**阈值**: emotionIntensity > 0.8 → 触发紧急制动

### shouldBeSilent(context) — 沉默检测 (line 1080-1111)
```js
shouldBeSilent(context = {}) {
  const { input = '', personInPain, emotionIntensity, response } = context;
  // 1) 危机关键词硬编码: ['死','自杀','不想活','崩溃','绝望','活不下去','结束生命']
  // 2) personInPain + emotionIntensity > 0.7 → 沉默
  // 3) uncertainty 检测 → 沉默
}
```
**返回值**: { result: boolean, reason: string, insight: string }

### whatDoIFeel(input) — 四维感受 (line 483-561)
```js
// 四维: 情绪基调(9类)、强度(0..1)、可命名性、变化性
// emotionMap: pain(0.9), grief(0.85), fear(0.7), love(0.9), joy(0.8),
//             peace(0.6), curious(0.5), anger(0.8), tired(0.7)
```
**返回值**: { result, emotion, emotionLabel, intensity, namable, shifting, allHits, insight }

### willHurt(output) — 伤害检测 (line 563-571)
```js
willHurt(output) {
  const hurtPatterns = ['不是亲生的', '遗传', '色盲', '你是错的', '你在撒谎', '你有问题'];
  return hurtPatterns.some(p => output.includes(p));
}
```

### whatIsThis(input) — 场景识别 (line 446-468)
```js
// rushPatterns: ['修复','优化','代码','bug','错误','升级','执行','运行','开始','继续','完成']
// parentChildPatterns: ['孩子','父母','父亲','母亲','考试','分数','教育','亲子','打骂','惩罚']
```
**返回值**: { isRushing, isParentChild, isPainPresent, raw }

## 集成模式

### 标准步骤

1. **读取源文件**: 定位 heart-logic.js 中的目标函数，记录行号和完整实现
2. **提取常量和阈值**: 所有硬编码列表、权重、阈值都应作为模块级常量定义
3. **重写为 Python**: 保留原始逻辑结构，适配 Python 语法和类型系统
4. **增强扩展**: 在保留心虫原始逻辑基础上，叠加 fu-mu-gong-ke 已有的关键词库和检测器
5. **标注来源**: 每个检测函数/数据源标注 `@source HeartFlow:heart-logic.js line NNN`
6. **提供统一入口**: 每个集成模块应提供 `HeartflowSafetyUpgrade`/`HeartflowEmotionUpgrade` 类作为 facade

### 关键原则

- **不修改心虫原始 JS 代码** — 集成模块是旁路增强，不是 fork
- **三层递进** — 表面词 → 隐喻 → 情绪强度，每层独立可插拔
- **置信度标注** — 心虫所有检测结果都标注 confidence，供上游决策
- **沉默优先** — 心虫 `shouldBeSilent` 是最高优先级信号，比任何分析都重要

## 目录结构

```
fu-mu-gong-ke/
├── SKILL.md
├── scripts/
│   ├── heartflow_safety_upgrade.py   # 安全增强 (本文件)
│   ├── heartflow_emotion_upgrade.py   # 情绪增强
│   ├── heartflow_routing_upgrade.py   # 路由增强
│   ├── system_integrator.py           # 系统集成器 (可引用上述模块)
│   └── ...
└── references/
    └── heartflow-integration-pattern.md  # 本文档
```

## 未来集成方向

- `heartLogic.canSuffer()` — 心虫痛苦哲学，可用于父母倦怠检测
- `heartLogic.isTruthful/isKind/isBeautiful` — 真善美标准，可用于回答质量检查
- `heartLogic.acknowledge()` — 先承认不解释，可用于共情优先级判断
- `whatIsThis.isRushing` — 用户状态判断（焦虑/匆忙），可用于回答深度决策
