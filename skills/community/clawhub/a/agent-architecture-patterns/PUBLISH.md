# 🚀 发布到 ClawHub 指南

## 前置条件

- ✅ 已完成技能开发
- ✅ 已通过单元测试
- ✅ 已登录 ClawHub (`clawhub login`)

---

## 发布步骤

### 步骤 1: 登录 ClawHub

```bash
clawhub login
```

浏览器会自动打开，完成认证后返回终端。

验证登录状态：
```bash
clawhub whoami
# 应显示：✓ Logged in as <your-username>
```

---

### 步骤 2: 准备发布

检查技能文件结构：

```bash
# 查看技能目录
tree skills/agent-architecture-patterns/

# 确保包含必要文件：
# - SKILL.md (必需)
# - README.md (推荐)
# - package.json (推荐)
# - 源代码和文档
```

---

### 步骤 3: 发布技能

```bash
clawhub publish skills/agent-architecture-patterns
```

发布命令会：
1. 读取 `SKILL.md` 获取技能元数据
2. 打包所有文件
3. 上传到 ClawHub 注册表
4. 返回技能 slug 和访问链接

---

### 步骤 4: 验证发布

```bash
# 搜索已发布的技能
clawhub search agent-architecture-patterns

# 查看技能详情
clawhub inspect agent-architecture-patterns
```

---

## 发布后

### 分享链接

发布成功后，技能可通过以下链接访问：

```
https://clawhub.ai/skills/<your-username>/agent-architecture-patterns
```

### 安装命令

其他人可以通过以下命令安装：

```bash
clawhub install agent-architecture-patterns
```

---

## 更新技能

修改技能后，更新发布：

```bash
# 更新版本号 (在 SKILL.md 中)
# 然后重新发布
clawhub update agent-architecture-patterns
```

---

## 常见问题

### Q: 发布失败怎么办？

**A**: 检查以下项：
- 是否已登录 (`clawhub whoami`)
- `SKILL.md` 格式是否正确
- 网络连接是否正常

### Q: 如何删除已发布的技能？

**A**: 
```bash
clawhub delete agent-architecture-patterns
```

### Q: 如何转移技能所有权？

**A**: 
```bash
clawhub transfer agent-architecture-patterns <new-owner>
```

---

## 技能元数据

`SKILL.md` 中应包含：

```markdown
# agent-architecture-patterns - AI Agent 架构设计模式

> **版本**: 1.0.0
> **作者**: AI-Agent
> **描述**: 提供 10 种 AI Agent 架构设计模式...
```

ClawHub 会从中提取：
- 技能名称
- 版本号
- 描述
- 作者信息

---

## 发布清单

- [ ] 登录 ClawHub
- [ ] 检查 SKILL.md 格式
- [ ] 运行测试确保通过
- [ ] 执行发布命令
- [ ] 验证发布成功
- [ ] 分享技能链接

---

**祝发布顺利！** 🎉
