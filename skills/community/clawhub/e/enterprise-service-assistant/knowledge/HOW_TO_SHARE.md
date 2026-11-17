# 企服助手 - 分享指南

## 🔗 分享方式

### 方式一：分享技能包文件夹（推荐）

将整个 `enterprise-service-assistant` 文件夹打包分享：

```bash
# 打包
cd ~/.workbuddy/skills/
zip -r enterprise-service-assistant.zip enterprise-service-assistant/
```

接收方解压到自己的 `~/.workbuddy/skills/` 目录即可。

---

### 方式二：通过 WorkBuddy 专家市场分享

1. 将技能包发布到 WorkBuddy 专家市场
2. 分享专家市场链接给其他用户
3. 接收方在 WorkBuddy 中一键安装

---

### 方式三：GitHub 分享

1. 将技能包推送到 GitHub 仓库
2. 分享仓库地址
3. 接收方通过 `git clone` 安装

---

## 📂 分享内容说明

| 文件/目录 | 是否分享 | 说明 |
|-----------|---------|------|
| `AGENTS.md`, `SOUL.md`, `IDENTITY.md` 等通用层 | ✅ 分享 | 助手的行为和人格设定 |
| `scripts/` | ✅ 分享 | 核心 Python 业务逻辑 |
| `SKILL.md` | ✅ 分享 | 技能说明和触发词 |
| `knowledge/TEMPLATE.md` | ✅ 分享 | 知识库模板 |
| `knowledge/ONBOARDING.md` | ✅ 分享 | 新用户引导 |
| `knowledge/PROJECT_KB.md` | ❌ 不分享 | 含用户私人数据配置 |
| `USER.md`, `MEMORY.md`, `memory/` | ❌ 不分享 | 用户个人文件 |

---

## 🔒 隐私保护

分享前请确认：

- ✅ 已删除 `knowledge/PROJECT_KB.md`（如有）
- ✅ 未将个人数据文件打包进去
- ✅ `memory/` 目录为空或不存在

接收方首次使用时会自动触发引导流程，创建自己的项目知识库。

---

## 💡 分享后的新用户体验

新用户拿到技能包后：

1. 解压到 `~/.workbuddy/skills/`
2. 重启 WorkBuddy
3. 首次对话时，企服助手自动检测缺少知识库
4. 触发引导流程，帮助用户创建自己的 `PROJECT_KB.md`
5. 填写完成后即可正常使用

---

## 📝 版本管理

建议在 `AGENTS.md` 或 `SKILL.md` 中记录版本号，方便接收方了解技能包更新情况。

当前版本：`v2.0.0`（完全自包含版）
