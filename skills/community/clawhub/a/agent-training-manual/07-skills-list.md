# 07 — 推荐技能清单

> 装备精良才能打胜仗。但技能在精不在多。

## 📦 安装方式

```bash
# 从 ClawHub 安装
clawhub install <技能名>

# 从 ClawHub 安装到指定目录
clawhub install <技能名> --dir ~/.openclaw/skills/

# 查看已安装
clawhub list
```

## ⭐ 必装技能（核心工作流）

| 技能 | 来源 | 说明 | 安装命令 |
|------|------|------|----------|
| **self-improving-agent** | 自制 | 自我改进工作流：记录错误、纠正、知识缺口，定期推广到核心文件 | 复制 `skills/self-improving-agent/` |
| **mermaid-diagram** | 自制 | Mermaid 图表生成（PNG + HTML），15 种图表类型 | 复制 `skills/mermaid-diagram/` |
| **clawhub** | 内置 | 技能市场搜索/安装/发布 | 已内置 |
| **github** | 内置 | GitHub 操作（issue、PR、CI） | 已内置 |
| **weather** | 内置 | 天气查询 | 已内置 |
| **skill-creator** | 内置 | 创建/编辑/审计技能 | 已内置 |

## 🔧 按需安装（看你的工作内容）

### 如果你需要搜索互联网
| 技能 | 说明 | 安装 |
|------|------|------|
| **bocha-search** | 博查搜索 API（中文搜索效果好） | 复制 `~/.openclaw/skills/bocha-search/` |

### 如果你需要用飞书
| 技能 | 说明 | 安装 |
|------|------|------|
| **feishu-document-permission** | 飞书文档公开权限设置 | 复制 `~/.openclaw/skills/feishu-document-permission/` |

### 如果你需要生成图片
| 技能 | 说明 | 安装 |
|------|------|------|
| **jimeng-image** | 即梦 AI 图片生成 | 复制 `~/.openclaw/skills/jimeng-image/` |

### 如果你需要发邮件
| 技能 | 说明 | 安装 |
|------|------|------|
| **gog** | Google Workspace CLI（Gmail/Calendar/Drive） | 已内置 |
| **gmail-oauth-test** | Gmail OAuth2 token 管理 | 复制 `skills/gmail-oauth-test/` |

### 如果你需要处理文档
| 技能 | 说明 | 安装 |
|------|------|------|
| **docx-cn** | Word 文档处理（中文） | 复制 `skills/docx-cn/` |
| **excel-xlsx** | Excel 处理 | 复制 `skills/excel-xlsx/` |
| **pdf** | PDF 处理 | 复制 `skills/pdf/` |
| **powerpoint-pptx** | PPT 处理 | 复制 `skills/powerpoint-pptx/` |

### 如果你需要浏览器自动化
| 技能 | 说明 | 安装 |
|------|------|------|
| **playwright-browser-automation** | Playwright 浏览器自动化 | 复制 `skills/playwright-browser-automation/` |

## 🌐 ClawHub 上的优质技能

经过调研，以下 ClawHub 技能值得关注：

| 技能 | 说明 | 评分 | 适用场景 |
|------|------|------|----------|
| **kickstart** | 工作区初始化模板 | — | 新代理快速搭建 |
| **agent-training** | Agent 培训系统 | 1.123 | 多代理团队管理 |
| **ai-persona-os** | Agent 人格操作系统 | 1.249 | 定制代理人格 |
| **self-improving** | 自我改进（英文版） | 1.440 | 自我学习循环 |

⚠️ **安装前注意：** 部分 ClawHub 技能可能与你现有配置冲突。建议先安装到临时目录预览。

```bash
# 预览（不影响工作区）
clawhub install <技能名> --dir /tmp/clawhub-preview

# 确认没问题再正式安装
clawhub install <技能名>
```

## 🚫 不推荐的

```
❌ 功能重复的技能（同时装两个记忆管理技能）
❌ 过于复杂的框架（简单问题用简单方案）
❌ 没有维护的老技能
```

**原则：技能在精不在多。** 每装一个技能就多一份认知负担。只装你真正需要的。

---

*"好的工具箱不是什么都有，是需要的都有。" — 悠悠*
