# 技术计划: Agent-SBTI

## 技术选型

| 组件 | 选型 | 理由 |
|------|------|------|
| 核心语言 | JavaScript/Node.js | 与 OpenClaw 生态兼容 |
| 测试数据 | sbti-personality-test | 现成的 20 题 + 5 人格 |
| 配置格式 | JSON → SOUL.md | OpenClaw 原生支持 |
| 用户界面 | 纯对话式 / 可选 Web | 直接在 Agent 内运行 |

## 架构设计

```
用户 → Agent (对话式测试)
         ↓
    test.js (答题系统)
         ↓
    report.js (计算维度 + 识别人格)
         ↓
    agent_config.js (生成配置)
         ↓
    apply.js (写入 SOUL.md 或提供复制)
```

## 核心模块

### 1. test.js
- 存储 20 道题目（复用数据包）
- 记录用户答案
- 计算维度分数

### 2. report.js
- 生成雷达图数据
- 识别人格类型
- 输出性格报告

### 3. agent_config.js
- 根据性格 + 用户选择（互补/同频/微调）
- 生成 Agent 配置 JSON

### 4. apply.js
- 将配置写入 SOUL.md
- 或生成可复制的配置片段

## 配置映射逻辑

```
用户维度分数 → 标准化(0-1) → Agent配置参数
     ↓
用户选择 → 互补(取反)/同频(相同)/微调(混合)
     ↓
Agent SOUL.md 配置片段
```

## 接口设计（内部）

```javascript
// 计算维度
calcDimensions(answers) → dimensions

// 生成报告
generateReport(dimensions) → { radar, personality, description }

// 生成 Agent 配置
generateAgentConfig(dimensions, type) → config

// 应用配置
applyConfig(config) → success/failed
```

## 数据模型

### UserProfile
```json
{
  "answers": [1-20],
  "dimensions": { "维度名": 分数 },
  "personality": "DEAD|FUCK|ATM|MALO|SHIT",
  "createdAt": "ISO时间"
}
```

### AgentConfig
```json
{
  "communication": { ... },
  "personality": { ... },
  "behavior": { ... },
  "raw": { "原始维度": "配置值" }
}
```

## 风险与依赖

| 类型 | 描述 |
|------|------|
| 风险 | SOUL.md 写入可能覆盖用户自定义内容 |
| 风险 | 用户性格与 Agent 配置映射需要调试验证 |
| 依赖 | sbti-personality-test 数据包 |
| 依赖 | OpenClaw Agent 环境 |

## 实现优先级

1. **P0**: test.js + report.js（核心功能）
2. **P1**: agent_config.js（配置生成）
3. **P2**: apply.js（配置应用）
4. **P3**: 分享功能

---

## 自定义模式扩展

### 配置生成扩展
```javascript
// 自定义模式：直接指定人格
generateAgentConfig(dimensions, personality) → config

// 5 种人格配置预设
const PERSONALITY_PRESETS = {
  DEAD: { communication: {...}, personality: {...} },
  FUCK: { communication: {...}, personality: {...} },
  ATM:  { communication: {...}, personality: {...} },
  MALO: { communication: {...}, personality: {...} },
  SHIT: { communication: {...}, personality: {...} }
}
```

### 自定义模式流程
```
用户: "都不喜欢"
     ↓
罗列 5 种人格 + 配置预览
     ↓
用户选择人格
     ↓
确认配置
     ↓
应用配置
```
