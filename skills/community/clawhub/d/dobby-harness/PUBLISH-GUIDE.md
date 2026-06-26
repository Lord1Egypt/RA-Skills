# Harness Engineering Skill 发布指南

> GitHub + ClawHub 发布完整流程

---

## 📋 发布清单

### 1. GitHub 仓库准备

#### 创建仓库

```bash
# 仓库名称建议
- harness-engineering
- harness-engineering-skill
- openclaw-harness
```

#### 仓库结构

```
harness-engineering/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/
│       └── ci.yml
├── harness/
├── workflows/
├── memory/
├── examples/
├── tests/
├── skills/
│   └── harness-engineering/
│       ├── SKILL.md
│       └── PUBLISH-GUIDE.md
├── .gitignore
├── LICENSE
├── README.md
├── HARNESS-ARCHITECTURE.md
├── WORKFLOWS.md
├── SELF-IMPROVEMENT.md
└── SECURITY-AUDIT.md
```

#### 必要文件

1. **LICENSE** - MIT 许可证
2. **README.md** - 项目说明
3. **.gitignore** - Git 忽略规则
4. **CONTRIBUTING.md** - 贡献指南（可选）

---

## 🚀 发布步骤

### 步骤 1: 准备发布文件

```bash
cd /home/admin/.openclaw/workspace

# 创建发布目录
mkdir -p skills/harness-engineering

# 复制必要文件
cp README.md skills/harness-engineering/
cp HARNESS-ARCHITECTURE.md skills/harness-engineering/
cp WORKFLOWS.md skills/harness-engineering/
cp SELF-IMPROVEMENT.md skills/harness-engineering/
cp SECURITY-AUDIT.md skills/harness-engineering/
```

### 步骤 2: 创建 GitHub 仓库

1. 访问 https://github.com/Panb-KG/dobby-harness
2. 点击 "Create repository"

### 步骤 3: 推送代码到 GitHub

```bash
cd /home/admin/.openclaw/workspace

# 初始化 Git (如果还没有)
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Harness Engineering v1.0.0

- Multi-Agent Orchestration System
- 5 task decomposition patterns
- 4 production workflows
- Self-improvement system with WAL
- Complete test suite and documentation"

# 添加远程仓库 (替换为你的 GitHub 用户名)
git remote add origin https://github.com/Panb-KG/harness-engineering.git

# 推送
git branch -M main
git push -u origin main
```

### 步骤 4: 发布到 ClawHub

#### 方法 A: 使用 clawhub CLI

```bash
# 安装 clawhub (如果还没有)
npm install -g clawhub

# 登录
clawhub login

# 发布技能
cd /home/admin/.openclaw/workspace/skills/harness-engineering
clawhub publish

# 或者指定仓库
clawhub publish --repo https://github.com/YOUR_USERNAME/harness-engineering.git
```

#### 方法 B: 手动注册

1. 访问 https://clawhub.ai
2. 登录账号
3. 点击 "Publish Skill"
4. 填写信息：
   - **Name**: `harness-engineering`
   - **Description**: "Multi-Agent Orchestration System"
   - **Repository URL**: https://github.com/Panb-KG/dobby-harness
   - **Version**: `1.0.0`
   - **Tags**: `orchestration`, `multi-agent`, `workflow`, `harness`

5. 提交审核

---

## 📝 ClawHub 注册信息

### Skill 元数据

```json
{
  "name": "harness-engineering",
  "version": "1.0.0",
  "description": "多 Agent 编排系统，提供任务分解、并行执行、生产工作流和自进化能力",
  "author": "Dobby",
  "license": "MIT",
  "repository": "https://github.com/YOUR_USERNAME/harness-engineering.git",
  "tags": [
    "orchestration",
    "multi-agent",
    "workflow",
    "harness",
    "automation"
  ],
  "capabilities": [
    "task-decomposition",
    "parallel-execution",
    "workflow-automation",
    "self-improvement"
  ],
  "requirements": {
    "node": ">=18.0.0",
    "openclaw": ">=1.0.0"
  }
}
```

### 触发条件

当用户提到以下关键词时触发：

- "多 Agent 编排"
- "任务分解"
- "并行执行"
- "Harness"
- "工作流"
- "代码审查"
- "测试生成"
- "文档自动化"

---

## ✅ 发布后验证

### 1. GitHub 验证

```bash
# 克隆仓库验证
git clone https://github.com/YOUR_USERNAME/harness-engineering.git
cd harness-engineering

# 运行测试
node tests/quick-test.js

# 运行演示
node examples/harness-demo.js
```

### 2. ClawHub 验证

```bash
# 安装技能测试
clawhub install harness-engineering

# 验证技能可用
# (在 OpenClaw 中尝试使用 Harness 功能)
```

---

## 📢 推广建议

### 1. 社交媒体

- Twitter/X: 发布项目链接和演示
- Discord: OpenClaw 社区频道
- 知乎/掘金：技术文章

### 2. 文档完善

- [ ] 添加中文文档
- [ ] 录制演示视频
- [ ] 创建在线 Demo

### 3. 社区互动

- [ ] 回复 Issues
- [ ] 接受 PRs
- [ ] 定期更新

---

## 🔄 版本更新

### 语义化版本

```
主版本。次版本.修订版本
  ↑      ↑      ↑
  |      |      └─ 向后兼容的 bug 修复
  |      └─ 向后兼容的新功能
  └─ 不兼容的 API 变更
```

### 更新流程

```bash
# 1. 更新版本号
# 在 SKILL.md 和 package.json (如果有) 中更新

# 2. 更新变更日志
# 在 README.md 中添加 CHANGELOG 章节

# 3. 提交并推送
git add .
git commit -m "Release v1.1.0"
git tag v1.1.0
git push origin main --tags

# 4. 更新 ClawHub
clawhub publish --version 1.1.0
```

---

## 📊 成功指标

### 短期 (1 个月)

- [ ] GitHub Stars: 10+
- [ ] 安装次数：50+
- [ ] Issues: 积极回复

### 中期 (3 个月)

- [ ] GitHub Stars: 50+
- [ ] 安装次数：200+
- [ ] 社区贡献：PRs 合并

### 长期 (6 个月)

- [ ] GitHub Stars: 100+
- [ ] 安装次数：500+
- [ ] 生态系统：衍生技能

---

## 🆘 常见问题

### Q: ClawHub 审核不通过？

A: 检查以下几点：
1. SKILL.md 格式是否正确
2. 代码是否能正常运行
3. 文档是否完整
4. 许可证是否明确

### Q: GitHub 推送失败？

A: 检查：
1. 仓库 URL 是否正确
2. 是否有推送权限
3. 网络连接是否正常

### Q: 技能安装后无法使用？

A: 验证：
1. 依赖是否满足
2. 文件路径是否正确
3. 触发条件是否匹配

---

## 📞 支持

- **GitHub Issues**: https://github.com/YOUR_USERNAME/harness-engineering/issues
- **OpenClaw Discord**: https://discord.com/invite/clawd
- **邮箱**: your-email@example.com

---

*发布指南版本：1.0.0 | 最后更新：2026-04-18*
