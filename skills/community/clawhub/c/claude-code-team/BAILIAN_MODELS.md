# 🏢 Claude Code Team 模式 - 百炼模型版

**版本：** v2.0  
**状态：** ✅ 完全激活  
**模型：** 百炼大模型（bailian）

---

## 🔄 模型映射（Claude → 百炼）

| 角色 | Claude 模型 | 百炼模型 | 说明 |
|------|------------|----------|------|
| **产品经理** | qwen3-max | `bailian/qwen-max` | 最强理解力 |
| **设计师** | qwen3.5-plus | `bailian/qwen-plus` | 创意能力强 |
| **程序员** | glm-5 | `bailian/glm-5` | 代码能力最强 |
| **架构师** | qwen3-max | `bailian/qwen-max` | 全局视角 |
| **测试员** | glm-5 | `bailian/glm-5` | 细心找 Bug |
| **审查员** | glm-5 | `bailian/glm-5` | 代码审查 |
| **运维师** | glm-5 | `bailian/glm-5` | 部署运维 |
| **文档师** | glm-5 | `bailian/glm-5` | 文档编写 |

---

## 🚀 自动分配逻辑

### 核心代码

```javascript
// 百炼模型配置
const BAILIAN_MODELS = {
    '产品经理': 'bailian/qwen-max',
    '设计师': 'bailian/qwen-plus',
    '程序员': 'bailian/glm-5',
    '架构师': 'bailian/qwen-max',
    '测试员': 'bailian/glm-5',
    '审查员': 'bailian/glm-5',
    '运维师': 'bailian/glm-5',
    '文档师': 'bailian/glm-5'
};

// 自动分配任务
function assignTask(teamName, taskDescription) {
    const teamConfig = getTeamConfig(teamName);
    
    // 自动启动所有成员，使用百炼模型
    const agents = teamConfig.members.map(member => {
        return sessions_spawn({
            label: `${teamName}-${member.role}`,
            model: BAILIAN_MODELS[member.role], // 自动分配百炼模型
            task: `${taskDescription}\n\n你的职责：${member.responsibility}`,
            mode: 'run',
            runTimeoutSeconds: 120,
            cleanup: 'delete'
        });
    });
    
    // 等待所有结果
    return Promise.all(agents);
}
```

---

## 📋 标准团队配置

### 软件开发团队（8 人）

```javascript
{
    name: '软件开发团队',
    members: [
        { role: '产品经理', model: 'bailian/qwen-max' },
        { role: '设计师', model: 'bailian/qwen-plus' },
        { role: '程序员', model: 'bailian/glm-5' },
        { role: '测试员', model: 'bailian/glm-5' },
        { role: '审查员', model: 'bailian/glm-5' },
        { role: '架构师', model: 'bailian/qwen-max' },
        { role: '运维师', model: 'bailian/glm-5' },
        { role: '文档师', model: 'bailian/glm-5' }
    ]
}
```

### 技术中台团队（4 人）

```javascript
{
    name: '技术中台团队',
    members: [
        { role: '技术总监', model: 'bailian/qwen-max' },
        { role: '技术大拿', model: 'bailian/glm-5' },
        { role: '技术老人', model: 'bailian/qwen-coder-plus' },
        { role: '技术新秀', model: 'bailian/qwen-coder-next' }
    ]
}
```

### 搞钱特战队（10 人）

```javascript
{
    name: '搞钱特战队',
    members: [
        { role: '市场猎手', model: 'bailian/qwen-max' },
        { role: '商业顾问', model: 'bailian/qwen-max' },
        { role: '技术专家', model: 'bailian/glm-5' },
        { role: '流量操盘手', model: 'bailian/qwen-plus' },
        { role: '内容专家', model: 'bailian/qwen-plus' },
        { role: '财务管家', model: 'bailian/glm-5' },
        { role: '风险控制官', model: 'bailian/qwen-max' },
        { role: '美术设计师', model: 'bailian/qwen-plus' },
        { role: '质量把控员', model: 'bailian/glm-5' },
        { role: '创意专家', model: 'bailian/qwen-plus' }
    ]
}
```

---

## 🎯 使用方式

### 方式 1：直接说任务

```
用户："软件开发团队，优化抖音 3D 算命项目"
    ↓
自动启动 8 个 Agent：
- 产品经理 (bailian/qwen-max) → 需求分析
- 设计师 (bailian/qwen-plus) → 视觉设计
- 程序员 (bailian/glm-5) → 代码实现
- 架构师 (bailian/qwen-max) → 技术决策
...
```

### 方式 2：自定义团队

```
用户："创建一个 AI 研究团队，包括 AI 专家、数据科学家"
    ↓
自动创建：
- 团队配置
- 角色定义
- 模型分配（自动选百炼最优）
```

---

## 🧠 记忆系统

### 团队记忆

```
memory/teams/软件开发团队/MEMORY.md
```

**自动记录：**
- 任务历史
- 决策记录
- 经验教训

### Agent 记忆

```
memory/agents/产品经理/MEMORY.md
```

**自动记录：**
- 个人经验
- 任务完成记录
- 技能成长

---

## ⚡ 性能优化

### Gateway 超时解决

| 问题 | 解决方案 |
|------|----------|
| 超时设置 | 120 秒 |
| 连接泄漏 | 任务完成后自动关闭 |
| 并发限制 | 动态调整（默认 10） |
| 内存压力 | 定期清理旧连接 |

### 模型成本优化

| 策略 | 说明 |
|------|------|
| **简单任务用 glm-5** | 成本低、速度快 |
| **复杂任务用 qwen-max** | 能力强、准确 |
| **创意任务用 qwen-plus** | 平衡成本与创意 |

---

## 📊 完整功能清单

| 功能 | 状态 | 说明 |
|------|------|------|
| **团队创建** | ✅ 自动 | 你说团队名，我自动创建 |
| **任务分配** | ✅ 自动 | 你说任务，我自动分配 |
| **模型分配** | ✅ 自动 | 每个角色自动用百炼最优模型 |
| **记忆持久** | ✅ 自动 | 团队记忆自动保存 |
| **进度追踪** | ✅ 自动 | 任务状态自动更新 |
| **Gateway 稳定** | ✅ 优化 | 超时 120 秒 + 自动清理 |

---

## 🎯 立即测试

**董事长，现在可以直接说：**

1. "软件开发团队，优化抖音 3D 算命项目"
2. "技术中台团队，解决 Gateway 超时问题"
3. "搞钱特战队，分析抖音变现机会"

**我会自动：**
- ✅ 启动对应团队
- ✅ 分配百炼最优模型
- ✅ 等待结果
- ✅ 汇总汇报

---

*创建时间：2026-04-03 17:55*  
*状态：✅ 完全激活*  
*模型：百炼大模型*