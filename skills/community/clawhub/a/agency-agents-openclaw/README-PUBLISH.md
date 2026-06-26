# 🚀 发布到 ClawHub

## 📋 发布清单

### 准备阶段 ✅

- [x] 完成全部 61 个 Agent
- [x] 编写 SKILL.md 和 README.md
- [x] 配置 package.json
- [x] 测试核心 Agent
- [ ] 登录 ClawHub
- [ ] 执行发布命令
- [ ] 验证发布成功

---

## 🔐 步骤 1: 登录 ClawHub

**在终端执行**:

```bash
clawhub login
```

这会打开浏览器让你登录 ClawHub 账号。

**或者手动设置 token**:

```bash
clawhub auth set-token
# 然后粘贴你的 token
```

---

## 📦 步骤 2: 发布技能

**执行发布命令**:

```bash
cd /Users/g/.openclaw/workspace/agency-agents-openclaw

clawhub publish . \
  --slug agency-agents \
  --name "AI Agent 团队 - 61 个专业 Agent" \
  --version 1.0.0 \
  --tags "ai-agents,automation,productivity,enterprise,latest" \
  --changelog "🎉 初始发布：61 个专业 AI Agent，8 大部门，完整的 AI 代理机构！

核心特性:
- 61 个专业 Agent 覆盖工程/设计/市场/产品/测试/支持
- 智能编排器自动调度多 Agent 协作
- 完整的文档和使用示例
- 持续更新和新 Agent 添加

适用场景:
- 创业公司 MVP 开发
- 企业项目开发
- 营销活动策划
- 产品设计优化
- 测试和质量保证"
```

---

## ✅ 步骤 3: 验证发布

**搜索技能**:
```bash
clawhub search agency-agents
```

**查看详情**:
```bash
clawhub inspect agency-agents
```

**测试安装**:
```bash
# 卸载旧版本（如果有）
clawhub uninstall agency-agents

# 安装新版本
clawhub install agency-agents

# 验证
clawhub list
```

---

## 💰 步骤 4: 设置定价

登录 ClawHub 控制台，在技能管理页面设置：

### 早鸟价（前 50 名）
| 版本 | 价格 | 原价 |
|------|------|------|
| 标准版 | ¥999 | ¥1999 |
| 部门版 | ¥299 | ¥499 |
| 订阅版 | ¥199/月 | ¥299/月 |

### 正式价
| 版本 | 价格 |
|------|------|
| 标准版 | ¥1999 |
| 部门版 | ¥499/个 |
| 订阅版 | ¥299/月 |
| 企业版 | 联系销售 |

---

## 📢 步骤 5: 营销推广

### 技能描述（用于 ClawHub 页面）

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

### 社交媒体文案

**Twitter/微博**:
```
🎉 发布了 61 个 AI Agent！从前端开发到增长黑客，
从 UI 设计到项目管理，完整的 AI 代理机构上线！

早鸟价 5 折，只要 ¥999！

#AI #OpenClaw #开发者工具
```

**朋友圈/LinkedIn**:
```
【新产品发布】AI Agent 团队 - 61 个专业 AI Agent

花了 1 天时间，把 61 个专业 Agent 打包成 OpenClaw 技能。
包括：前端开发、后端架构、UI 设计、增长黑客、
项目经理、测试 QA、客服支持...几乎涵盖所有业务场景。

早鸟价 ¥999（原价 ¥1999），前 50 名优惠！

欢迎试用反馈 🚀
```

---

## 📊 成功指标

### 30 天目标
- [ ] 安装量 > 100
- [ ] 付费转化 > 20%
- [ ] 用户评分 > 4.5/5
- [ ] 收入 > ¥50k

### 90 天目标
- [ ] 安装量 > 500
- [ ] 订阅用户 > 100
- [ ] 企业客户 > 5
- [ ] 收入 > ¥200k

---

## 🆘 常见问题

**Q: 发布失败怎么办？**
A: 检查是否已登录，验证 package.json 格式是否正确。

**Q: 如何更新技能？**
A: 修改版本号后，再次运行 `clawhub publish`。

**Q: 如何设置定价？**
A: 在 ClawHub 控制台的技能管理页面设置。

**Q: 如何查看销售数据？**
A: ClawHub 控制台有销售仪表板。

---

## 📞 支持

- **ClawHub 文档**: https://clawhub.com/docs
- **技术支持**: support@clawhub.com
- **社区**: Discord

---

**准备好了吗？开始发布吧！** 🚀

```bash
# 1. 登录
clawhub login

# 2. 发布
cd /Users/g/.openclaw/workspace/agency-agents-openclaw
clawhub publish . --slug agency-agents --name "AI Agent 团队" --version 1.0.0

# 3. 验证
clawhub search agency-agents
```
