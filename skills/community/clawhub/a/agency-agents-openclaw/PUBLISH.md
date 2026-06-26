# 📦 ClawHub 发布指南

## 发布前准备

### 1. 登录 ClawHub

```bash
# 浏览器登录
clawhub login

# 或手动输入 token
clawhub auth set-token
```

### 2. 验证登录状态

```bash
clawhub whoami
```

---

## 发布步骤

### 方式 1: 使用完整配置（推荐）

```bash
cd /Users/g/.openclaw/workspace/agency-agents-openclaw

clawhub publish . \
  --slug agency-agents \
  --name "AI Agent 团队 - 61 个专业 Agent" \
  --version 1.0.0 \
  --tags "ai-agents,automation,productivity,enterprise,latest" \
  --changelog "初始发布：61 个专业 AI Agent，8 大部门，完整的 AI 代理机构"
```

### 方式 2: 简化发布

```bash
cd /Users/g/.openclaw/workspace

clawhub publish agency-agents-openclaw
```

---

## 发布后验证

### 1. 搜索技能

```bash
clawhub search agency-agents
```

### 2. 查看技能详情

```bash
clawhub inspect agency-agents
```

### 3. 安装测试

```bash
# 卸载当前版本
clawhub uninstall agency-agents

# 重新安装
clawhub install agency-agents

# 验证
clawhub list
```

---

## 定价配置

### ClawHub 定价设置

在 ClawHub 控制台设置：

**早鸟价**（前 50 名）:
- 标准版：¥999（5 折）
- 部门版：¥299（6 折）
- 订阅版：¥199/月

**正式价**:
- 标准版：¥1999
- 部门版：¥499/个
- 订阅版：¥299/月

---

## 营销材料

### 技能描述（ClawHub 页面）

```
🤖 AI Agent 团队 - 你的完整 AI 代理机构

61 个专业 AI Agent，8 大业务部门，从前端开发到增长黑客，
从 UI 设计到项目管理，一站式解决所有业务需求！

✨ 核心特性:
- 61 个专业 Agent，覆盖 8 大业务领域
- 单 Agent 使用或多 Agent 协作
- 智能编排器自动调度复杂项目
- 持续更新和新 Agent 添加

💼 适用场景:
- 创业公司 MVP 开发
- 企业项目开发
- 营销活动策划
- 产品设计优化
- 测试和质量保证

🎯 立即开始，用 AI 团队赋能你的业务！
```

### 使用示例

```bash
# 单个 Agent
/openclaw skill use agency-agents --agent frontend-developer "创建 React 组件"
/openclaw skill use agency-agents --agent growth-hacker "制定增长策略"

# 多 Agent 协作
/openclaw skill use agency-agents --agent orchestrator "开发完整应用"

# 部门协作
/openclaw skill use agency-agents --department engineering "开发 Web 应用"
```

---

## 推广计划

### 第 1 周：预热
- [ ] ClawHub 首页推荐申请
- [ ] 社交媒体预告
- [ ] 邮件列表通知

### 第 2 周：发布
- [ ] 正式发布 ClawHub
- [ ] 早鸟价促销开始
- [ ] Demo 视频发布
- [ ] 博客文章

### 第 3-4 周：推广
- [ ] 用户案例收集
- [ ] 社交媒体持续推广
- [ ] 社区演示
- [ ] 收集反馈迭代

---

## 成功指标

### 发布目标（30 天）
- [ ] 安装量 > 100
- [ ] 付费转化 > 20%
- [ ] 用户评分 > 4.5/5
- [ ] 收入 > ¥50k

### 长期目标（90 天）
- [ ] 安装量 > 500
- [ ] 订阅用户 > 100
- [ ] 企业客户 > 5
- [ ] 收入 > ¥200k

---

## 联系支持

- **ClawHub 文档**: https://clawhub.com/docs
- **技术支持**: support@clawhub.com
- **社区**: Discord/微信群

---

*准备就绪，开始发布！*
