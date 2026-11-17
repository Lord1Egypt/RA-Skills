# 企服助手 - 安装指南

## 🚀 一键安装（推荐）

在 WorkBuddy 对话框中输入：

```
@WorkBuddy 请帮我安装企业服务助手技能包
```

或直接导入技能包文件：

```
@WorkBuddy 导入技能 enterprise-service-assistant
```

---

## 📦 手动安装

### 方式一：从 GitHub 安装

```bash
# 在 WorkBuddy 终端中执行
git clone https://github.com/perrykono-debug/enterprise-service-assistant.git ~/.workbuddy/skills/enterprise-service-assistant
```

### 方式二：本地导入

1. 下载 `enterprise-service-assistant` 技能包文件夹
2. 放入 `~/.workbuddy/skills/` 目录
3. 重启 WorkBuddy 会话

---

## ✅ 验证安装

在 WorkBuddy 中执行：

```
@WorkBuddy 列出已安装的 skills
```

应能看到 `enterprise-service-assistant`。

---

## ⚙️ 配置项目知识库（必须！）

安装完成后，需要为你的园区项目创建知识库：

1. 复制模板：`knowledge/TEMPLATE.md` → `knowledge/PROJECT_KB.md`
2. 填写你的项目信息（项目名称、数据文件路径、工作表结构）
3. 告诉我 `"知识库已配置，帮我验证一下"`

详细引导请参考 `knowledge/ONBOARDING.md`。

---

## 🔧 依赖技能

企服助手依赖以下 WorkBuddy 技能（通常已预装）：

- `docx` — Word 文档处理
- `pdf` — PDF 文档处理
- `xlsx` — Excel 表格处理
- `tencent-docs` — 腾讯文档 MCP 工具
- `online-search` — 联网搜索

如缺少任一技能，WorkBuddy 会提示安装。

---

## 🆘 常见问题

**Q: 安装后无法触发企服助手？**
A: 确保技能包放在 `~/.workbuddy/skills/enterprise-service-assistant/` 目录下，并重启会话。

**Q: 数据文件支持哪些格式？**
A: 优先支持 `.xlsx`，也支持 `.csv` 和腾讯在线文档。

**Q: 可以多人共享配置吗？**
A: 通用层（AGENTS.md 等）可分享；项目知识库（PROJECT_KB.md）每人独立，互不可见。
