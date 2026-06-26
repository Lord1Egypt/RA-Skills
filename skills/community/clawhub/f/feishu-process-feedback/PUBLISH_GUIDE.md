# 📤 发布到 ClawHub 完整指南

本指南详细说明如何将 `feishu-process-feedback` 技能发布到 ClawHub.ai

---

## 📋 发布前检查清单

### 1. 文件结构验证

确保技能目录包含以下文件：

```
feishu-process-feedback/
├── SKILL.md              ✅ 必需 - 技能说明（含 YAML frontmatter）
├── package.json          ✅ 必需 - 项目元信息
├── README.md             ✅ 推荐 - 使用文档
├── PUBLISH_GUIDE.md      ✅ 推荐 - 发布指南
├── scripts/
│   ├── listener.js       ✅ 必需 - 监听器主程序
│   └── process_task.js   ✅ 必需 - 任务处理器
└── .gitignore            ✅ 推荐 - Git 忽略文件
```

### 2. SKILL.md 验证

检查 frontmatter 格式：

```yaml
---
name: feishu-process-feedback      # 小写，连字符分隔
description: |                     # 多行描述
  飞书消息自动处理与进度反馈技能...
---
```

**要求：**
- `name`: 小写字母、数字、连字符，不超过 64 字符
- `description`: 清晰描述功能和使用场景

### 3. package.json 验证

```json
{
  "name": "feishu-process-feedback",
  "version": "1.0.0",
  "description": "...",
  "license": "MIT",
  "engines": { "node": ">=14.0.0" }
}
```

**要求：**
- `name` 与 SKILL.md 中的 `name` 一致
- `version` 遵循语义化版本
- `license` 明确许可证

### 4. 功能测试

```bash
# 本地测试
cd ~/.openclaw/skills/feishu-process-feedback

# 测试监听器
node scripts/listener.js

# 测试任务处理器
node scripts/process_task.js "测试：1. 步骤一 2. 步骤二" test_001
```

---

## 🚀 发布步骤

### 步骤 1: 安装 ClawHub CLI

```bash
npm install -g clawhub
```

验证安装：

```bash
clawhub --version
```

### 步骤 2: 登录 ClawHub

```bash
clawhub login
```

按提示输入账号密码或 API Token。

验证登录状态：

```bash
clawhub whoami
```

### 步骤 3: 进入技能目录

```bash
cd ~/.openclaw/skills/feishu-process-feedback
```

### 步骤 4: 发布技能

```bash
clawhub publish . \
  --slug feishu-process-feedback \
  --name "Feishu Process Feedback" \
  --version 1.0.0 \
  --changelog "初始版本：基础监听、进度反馈、进程管理、错误重试"
```

**参数说明：**

| 参数 | 说明 | 必需 |
|------|------|------|
| `.` | 技能目录路径 | 是 |
| `--slug` | 技能标识符 | 是 |
| `--name` | 技能显示名称 | 是 |
| `--version` | 版本号 | 是 |
| `--changelog` | 更新说明 | 推荐 |
| `--registry` | 自定义 Registry | 否 |

### 步骤 5: 验证发布

```bash
# 搜索技能
clawhub search feishu-process-feedback

# 查看技能详情
clawhub info feishu-process-feedback
```

---

## 🔄 更新技能

### 修改代码后

1. **更新版本号**

编辑 `package.json`：

```json
{
  "version": "1.0.1"  // 递增版本号
}
```

2. **更新 SKILL.md 版本历史**

```markdown
## 版本历史

### v1.0.1 (2026-03-10)
- 修复 xxx bug
- 优化 xxx 性能
- 新增 xxx 功能
```

3. **发布新版本**

```bash
clawhub publish . \
  --slug feishu-process-feedback \
  --version 1.0.1 \
  --changelog "修复 bug + 性能优化"
```

### 版本命名规范

遵循 [语义化版本 2.0.0](https://semver.org/)：

- **MAJOR** (1.0.0 → 2.0.0): 不兼容的 API 变更
- **MINOR** (1.0.0 → 1.1.0): 向后兼容的功能新增
- **PATCH** (1.0.0 → 1.0.1): 向后兼容的问题修复

---

## 📊 常用命令

### 搜索技能

```bash
# 按名称搜索
clawhub search feishu

# 按标签搜索
clawhub search --tag automation
```

### 安装技能

```bash
# 安装最新版
clawhub install feishu-process-feedback

# 安装指定版本
clawhub install feishu-process-feedback --version 1.0.0
```

### 更新技能

```bash
# 更新单个技能
clawhub update feishu-process-feedback

# 更新所有技能
clawhub update --all

# 强制更新
clawhub update feishu-process-feedback --force
```

### 列出已安装技能

```bash
clawhub list
```

### 卸载技能

```bash
clawhub uninstall feishu-process-feedback
```

---

## ⚠️ 常见问题

### Q1: 发布失败 - "Invalid skill structure"

**原因：** 缺少必需文件或格式错误

**解决：**

```bash
# 检查文件结构
ls -la

# 验证 SKILL.md frontmatter
head -10 SKILL.md

# 验证 package.json
cat package.json | jq .
```

### Q2: 发布失败 - "Slug already taken"

**原因：** 技能标识符已被占用

**解决：**

- 使用不同的 slug（如 `feishu-process-feedback-pro`）
- 或联系原发布者

### Q3: 登录失败 - "Invalid credentials"

**原因：** 账号密码错误或未注册

**解决：**

- 检查账号密码
- 注册 ClawHub 账号：https://clawhub.com/signup
- 使用 API Token 登录

### Q4: 发布后搜索不到

**原因：** 索引延迟

**解决：**

- 等待 1-2 分钟
- 检查发布是否成功：`clawhub info feishu-process-feedback`

---

## 🎯 发布最佳实践

### 1. 发布前

- ✅ 完整测试所有功能
- ✅ 更新文档和版本历史
- ✅ 清理临时文件（`.log`, `.json` 状态文件）
- ✅ 确保 Git 仓库干净

### 2. 发布时

- ✅ 使用语义化版本号
- ✅ 编写清晰的更新说明
- ✅ 选择合适的时间（避开高峰期）

### 3. 发布后

- ✅ 验证技能可被搜索到
- ✅ 测试安装流程
- ✅ 收集用户反馈
- ✅ 及时修复问题

---

## 📁 清理发布文件

发布前清理不必要的文件：

```bash
# 创建 .gitignore
cat > .gitignore << EOF
# 日志文件
*.log

# 状态文件
.listener_state.json

# 系统文件
.DS_Store
Thumbs.db

# 依赖
node_modules/
EOF

# 删除临时文件
rm -f .listener.log .tasks.log
```

---

## 🔗 相关资源

- [ClawHub 官方文档](https://clawhub.com/docs)
- [ClawHub CLI 源码](https://github.com/clawhub/cli)
- [OpenClaw 技能开发指南](https://docs.openclaw.ai/skills)
- [语义化版本规范](https://semver.org/)

---

_最后更新：2026-03-10_
