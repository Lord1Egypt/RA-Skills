# 🏢 Claude Code Team（OpenClaw 适配版）

**参照 Claude Code Team 模式，专为 OpenClaw 设计的团队任务分配技能**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/davidme6/openclaw-claude-code-team)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://openclaw.ai)

---

## 📖 简介

**Claude Code Team（OpenClaw 适配版）** 是参照 Anthropic Claude Code 的团队协作模式，专为 OpenClaw 设计的团队任务分配技能。

**核心功能：**
- 🤖 **自动识别平台**：百炼/火山/OpenAI，自动分配最优模型
- 🎯 **自动启动团队**：项目相关自动启动多 Agent 讨论
- 🧠 **记忆持久化**：团队记忆自动保存到 `memory/teams/`
- ⚡ **高性能**：Gateway 超时优化（120 秒）+ 连接自动清理

---

## 🚀 快速开始

### 安装

**方法 1：ClawHub 安装（推荐）**
```bash
clawhub install claude-code-team
```

**方法 2：Git 克隆**
```bash
git clone https://github.com/davidme6/openclaw-claude-code-team.git
cp -r openclaw-claude-code-team ~/.openclaw/skills/claude-code-team
```

### 使用

**标准团队任务：**
```
软件开发团队，优化这个项目
技术中台团队，解决 Gateway 问题
搞钱特战队，分析变现机会
```

**自定义团队：**
```
创建一个 AI 研究团队，包括 AI 专家、数据科学家
```

---

## 🎯 核心特性

### 1️⃣ 自动识别平台

```
检测当前使用的模型平台
├── 百炼 → 分配百炼最优模型（qwen-max/glm-5）
├── 火山 → 分配火山最优模型（doubao-pro）
└── OpenAI → 分配 OpenAI 最优模型（gpt-4o）
```

**不需要你说"百炼版本"，自动识别！**

### 2️⃣ 自动启动团队

| 场景 | 自动启动？ |
|------|-----------|
| 你说"团队" | ✅ 自动启动 |
| 你说"优化项目" | ✅ 自动启动 |
| 你上传项目 + 任务 | ✅ 自动启动 |
| 日常问题 | ❌ 自己回答 |

### 3️⃣ 标准团队配置

#### 软件开发团队（8 人）

| 角色 | 百炼模型 | 职责 |
|------|----------|------|
| 产品经理 | bailian/qwen-max | 需求分析 |
| 设计师 | bailian/qwen-plus | 视觉设计 |
| 程序员 | bailian/glm-5 | 代码实现 |
| 架构师 | bailian/qwen-max | 技术决策 |
| 测试员 | bailian/glm-5 | 质量检查 |
| 审查员 | bailian/glm-5 | 代码审查 |
| 运维师 | bailian/glm-5 | 部署运维 |
| 文档师 | bailian/glm-5 | 文档编写 |

#### 技术中台团队（4 人）

| 角色 | 百炼模型 | 职责 |
|------|----------|------|
| 技术总监 | bailian/qwen-max | 统筹决策 |
| 技术大拿 | bailian/glm-5 | 核心攻坚 |
| 技术老人 | bailian/qwen-coder-plus | 经验建议 |
| 技术新秀 | bailian/qwen-coder-next | 执行学习 |

#### 搞钱特战队（10 人）

| 角色 | 百炼模型 | 职责 |
|------|----------|------|
| 市场猎手 | bailian/qwen-max | 发现机会 |
| 商业顾问 | bailian/qwen-max | 评估可行性 |
| 技术专家 | bailian/glm-5 | 技术方案 |
| 流量操盘手 | bailian/qwen-plus | 获客推广 |
| ... | ... | ... |

---

## 📊 与 Claude Code 对比

| 维度 | Claude Code | 本技能（OpenClaw 适配） |
|------|-------------|------------------------|
| **任务分配** | 自动 | ✅ 自动 |
| **模型分配** | Claude 各版本 | ✅ 百炼/火山/OpenAI 各版本 |
| **进度追踪** | 有看板 | ✅ 团队记忆 |
| **记忆持久** | 自动读写 | ✅ 自动保存 |
| **Gateway 稳定** | ✅ 稳定 | ✅ 优化后稳定（120 秒） |
| **平台支持** | 仅 Claude | ✅ 多平台（百炼/火山/OpenAI） |

**结论：** 功能对等，多平台支持！✅

---

## 🔧 技术细节

### Gateway 超时修复

**问题：** 默认 10 秒超时，复杂任务失败

**修复：**
```json
{
  "gateway": {
    "timeout": 120000,
    "maxConnections": 20,
    "autoCleanup": true
  }
}
```

### 连接自动清理

**封装 sessions_spawn：**
```javascript
sessions_spawn({
    mode: 'run',
    runTimeoutSeconds: 120,
    cleanup: 'delete'  // 完成后自动清理
});
```

### 自动重试机制

```javascript
async function spawnWithRetry(options, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await sessions_spawn(options);
        } catch (e) {
            if (i === maxRetries - 1) throw e;
            await sleep(1000);
        }
    }
}
```

---

## 📁 文件结构

```
claude-code-team/
├── SKILL.md                    # 技能定义
├── teams.json                  # 团队配置 + 模型映射
├── README.md                   # 使用说明
├── PLATFORM_AUTO_DETECT.md     # 平台自动检测说明
├── GATEWAY_FIX.md              # Gateway 超时修复说明
├── TEST_REPORT.md              # 测试报告
└── LICENSE                     # MIT 许可证
```

---

## 🧪 测试报告

### 测试 1：软件开发团队

**输入：**
```
软件开发团队，优化 I Ching 项目
```

**结果：**
- ✅ 启动 8 个 Agent
- ✅ 产品经理 (qwen-max) → 需求分析
- ✅ 设计师 (qwen-plus) → 视觉设计
- ✅ 程序员 (glm-5) → 代码实现
- ✅ 架构师 (qwen-max) → 技术决策
- ✅ 汇总结果

**时间：** ~2 分钟

### 测试 2：技术中台团队

**输入：**
```
技术中台团队，解决 Gateway 超时问题
```

**结果：**
- ✅ 启动 4 个 Agent
- ✅ 永久修复 Gateway 问题
- ✅ 连接自动清理
- ✅ 超时优化到 120 秒

**时间：** ~2 分钟

---

## 🎯 使用示例

### 示例 1：软件开发

```
用户：软件开发团队，做一个抖音 3D 算命项目

自动启动：
- 产品经理 → 需求分析
- 设计师 → 视觉设计
- 程序员 → 代码实现
- 架构师 → 技术决策

输出：完整的项目方案 + 代码实现
```

### 示例 2：技术攻关

```
用户：技术中台团队，解决 Gateway 超时问题

自动启动：
- 技术总监 → 统筹决策
- 技术大拿 → 核心攻坚
- 技术老人 → 经验建议
- 技术新秀 → 测试验证

输出：根因分析 + 永久修复方案
```

### 示例 3：商业分析

```
用户：搞钱特战队，分析抖音变现机会

自动启动：
- 市场猎手 → 发现机会
- 商业顾问 → 评估可行性
- 技术专家 → 技术方案
- 流量操盘手 → 获客策略

输出：商业分析报告
```

---

## ⚠️ 注意事项

1. **Gateway 超时** - 复杂任务可能超过 120 秒，可手动延长
2. **记忆清理** - 定期清理旧记忆（建议每周）
3. **模型成本** - 多 Agent 同时运行，注意 API 成本
4. **并发限制** - 默认 10 个并发，大团队需调整

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**开发环境搭建：**
```bash
git clone https://github.com/davidme6/openclaw-claude-code-team.git
cd openclaw-claude-code-team
# 编辑 SKILL.md 等文件
# 测试通过后提交 PR
```

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- **Anthropic Claude Code** - 团队模式灵感来源
- **OpenClaw** - 技能运行平台
- **百炼大模型** - 模型支持

---

**Created by davidme6 | 2026-04-03**