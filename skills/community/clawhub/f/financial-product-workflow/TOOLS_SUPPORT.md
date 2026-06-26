# 工具支持清单

**版本：** 1.0.0  
**最后更新：** 2026-03-26  
**说明：** 列出所有支持的工具及配置状态

---

## 🎯 设计理念

**核心原则：**
- ✅ **开放支持**：用户可以绑定任何工具
- ✅ **透明状态**：明确标注已支持/待支持
- ✅ **降级方案**：无工具也能用（输出文档/清单）
- ✅ **自定义扩展**：支持添加自己的工具

---

## 📊 工具支持矩阵

### 项目管理类

| 工具 | 支持状态 | API 配置 | 降级方案 | 使用场景 |
|------|---------|---------|---------|---------|
| **Jira Cloud** | ✅ 已支持 | [配置指南](#jira-cloud-配置) | Markdown 待办清单 | 需求管理/任务跟踪 |
| **Jira Server** | ⚠️ 待支持 | - | Markdown 待办清单 | 需求管理/任务跟踪 |
| **Trello** | ⚠️ 待支持 | - | Markdown 待办清单 | 看板管理 |
| **Asana** | ⚠️ 待支持 | - | Markdown 待办清单 | 任务管理 |
| **禅道** | ⚠️ 待支持 | - | Markdown 待办清单 | 需求管理/缺陷跟踪 |
| **Teambition** | ⚠️ 待支持 | - | Markdown 待办清单 | 任务管理 |
| **飞书项目** | ⚠️ 待支持 | - | Markdown 待办清单 | 项目管理 |
| **钉钉项目** | ⚠️ 待支持 | - | Markdown 待办清单 | 项目管理 |

**已支持脚本：**
- `scripts/jira-create-issue.py` - 创建 Jira Issue
- `scripts/jira-query-status.py` - 查询 Issue 状态

---

### 文档协作类

| 工具 | 支持状态 | API 配置 | 降级方案 | 使用场景 |
|------|---------|---------|---------|---------|
| **Confluence Cloud** | ✅ 已支持 | [配置指南](#confluence-cloud-配置) | Markdown 文档 | PRD 文档/会议纪要 |
| **Confluence Server** | ⚠️ 待支持 | - | Markdown 文档 | PRD 文档 |
| **飞书文档** | ⚠️ 待支持 | - | Markdown 文档 | PRD 文档/协作 |
| **钉钉文档** | ⚠️ 待支持 | - | Markdown 文档 | PRD 文档 |
| **腾讯文档** | ⚠️ 待支持 | - | Markdown 文档 | PRD 文档 |
| **Notion** | ⚠️ 待支持 | - | Markdown 文档 | 知识库 |
| **语雀** | ⚠️ 待支持 | - | Markdown 文档 | 知识库 |
| **GitBook** | ⚠️ 待支持 | - | Markdown 文档 | 产品文档 |

**已支持脚本：**
- `scripts/confluence-create-page.py` - 创建 Confluence 页面
- `scripts/confluence-update-page.py` - 更新页面内容

---

### 原型设计类

| 工具 | 支持状态 | API 配置 | 降级方案 | 使用场景 |
|------|---------|---------|---------|---------|
| **Figma** | ⚠️ 部分支持 | [配置指南](#figma-配置) | 文字原型描述 | UI 设计/原型 |
| **墨刀** | ⚠️ 待支持 | - | 文字原型描述 | 原型设计 |
| **Axure Cloud** | ⚠️ 待支持 | - | 文字原型描述 | 原型设计 |
| **Sketch** | ❌ 不支持 | - | 文字原型描述 | UI 设计 |
| **Adobe XD** | ❌ 不支持 | - | 文字原型描述 | UI 设计 |
| **即时设计** | ❌ 不支持 | - | 文字原型描述 | UI 设计 |
| **MasterGo** | ❌ 不支持 | - | 文字原型描述 | UI 设计 |

**降级方案：**
```
无 API → 输出详细文字原型描述 + mermaid 流程图
用户手动在原型工具中创建
```

---

### 数据分析类

| 工具 | 支持状态 | API 配置 | 降级方案 | 使用场景 |
|------|---------|---------|---------|---------|
| **神策数据** | ⚠️ 待支持 | - | 埋点设计文档 | 用户行为分析 |
| **GrowingIO** | ⚠️ 待支持 | - | 埋点设计文档 | 用户行为分析 |
| **Google Analytics** | ⚠️ 待支持 | - | 埋点设计文档 | 网站分析 |
| **Mixpanel** | ⚠️ 待支持 | - | 埋点设计文档 | 用户分析 |
| **Amplitude** | ⚠️ 待支持 | - | 埋点设计文档 | 用户分析 |
| **诸葛 IO** | ❌ 不支持 | - | 埋点设计文档 | 用户分析 |
| **神策分析云** | ❌ 不支持 | - | 埋点设计文档 | 用户分析 |

**降级方案：**
```
无 API → 输出数据埋点设计文档（事件列表）
用户手动在数据工具中配置
```

---

### 代码托管类

| 工具 | 支持状态 | API 配置 | 降级方案 | 使用场景 |
|------|---------|---------|---------|---------|
| **GitHub** | ✅ 已支持 | [配置指南](#github-配置) | 手动创建分支 | 代码托管/版本控制 |
| **GitLab** | ⚠️ 待支持 | - | 手动创建分支 | 代码托管 |
| **Gitee** | ⚠️ 待支持 | - | 手动创建分支 | 代码托管 |
| **Azure DevOps** | ❌ 不支持 | - | 手动创建分支 | 代码托管 |
| **Bitbucket** | ❌ 不支持 | - | 手动创建分支 | 代码托管 |

**已支持脚本：**
- `scripts/git-create-branch.py` - 创建 Git 分支
- `scripts/git-create-pr.py` - 创建 Pull Request

---

### 通讯通知类

| 工具 | 支持状态 | API 配置 | 降级方案 | 使用场景 |
|------|---------|---------|---------|---------|
| **钉钉** | ✅ 已支持 | [配置指南](#钉钉配置) | 输出通知文案 | 团队通知 |
| **企业微信** | ✅ 已支持 | [配置指南](#企业微信配置) | 输出通知文案 | 团队通知 |
| **飞书** | ✅ 已支持 | [配置指南](#飞书配置) | 输出通知文案 | 团队通知 |
| **Slack** | ⚠️ 待支持 | - | 输出通知文案 | 团队通知 |
| **Microsoft Teams** | ❌ 不支持 | - | 输出通知文案 | 团队通知 |
| **Discord** | ❌ 不支持 | - | 输出通知文案 | 团队通知 |

**已支持脚本：**
- `scripts/dingtalk-notify.py` - 发送钉钉通知
- `scripts/wecom-notify.py` - 发送企业微信通知
- `scripts/feishu-notify.py` - 发送飞书通知

---

### 搜索调研类

| 工具 | 支持状态 | API 配置 | 降级方案 | 使用场景 |
|------|---------|---------|---------|---------|
| **SearXNG** | ✅ 内置支持 | 无需配置 | N/A | 竞品信息搜索 |
| **Google Search** | ⚠️ 需 API Key | [配置指南](#google-search-配置) | 手动搜索 | 市场调研 |
| **七麦数据** | ⚠️ 需账号 | - | 手动查询 | APP 数据查询 |
| **蝉大师** | ⚠️ 需账号 | - | 手动查询 | APP 数据查询 |
| **QuestMobile** | ❌ 不支持 | - | 手动查询 | 行业报告 |
| **易观千帆** | ❌ 不支持 | - | 手动查询 | 行业报告 |

**已支持脚本：**
- `scripts/searxng-search.py` - 搜索竞品信息（内置）

---

## 🔧 工具配置指南

### Jira Cloud 配置

**前提条件：**
- Atlassian Cloud 账号
- Jira Software Cloud 订阅

**配置步骤：**
1. 访问：https://id.atlassian.com/manage-profile/security/api-tokens
2. 点击"Create API token"
3. 记录：`JIRA_SERVER`、`JIRA_EMAIL`、`API_TOKEN`
4. 添加到环境变量或 `.env` 文件

**环境变量：**
```bash
export JIRA_SERVER="https://your-company.atlassian.net"
export JIRA_EMAIL="your-email@company.com"
export JIRA_API_TOKEN="your-api-token"
```

**测试连接：**
```bash
cd scripts
python jira-create-issue.py "测试 Issue" "这是一个测试"
```

**预期输出：**
```
✅ 已创建 Jira Issue: PROD-123
链接：https://your-company.atlassian.net/browse/PROD-123
```

**失败降级：**
```
⚠️ Jira API 调用失败：[错误信息]

📋 待创建 Jira Issue（手动创建）
...
```

---

### Confluence Cloud 配置

**前提条件：**
- Atlassian Cloud 账号
- Confluence Cloud 订阅
- API Token（与 Jira 相同）

**环境变量：**
```bash
export CONFLUENCE_SERVER="https://your-company.atlassian.net/wiki"
export CONFLUENCE_SPACE="YOURSPACE"
export CONFLUENCE_API_TOKEN="your-api-token"
```

**测试连接：**
```bash
cd scripts
python confluence-create-page.py "测试页面" "这是测试内容"
```

---

### Figma 配置

**前提条件：**
- Figma 账号（免费即可）
- 文件访问权限

**获取 API Token：**
1. 访问：https://www.figma.com/developers/api#access-tokens
2. 点击"Get personal access token"
3. 记录：`FIGMA_API_TOKEN`

**环境变量：**
```bash
export FIGMA_API_TOKEN="your-token"
export FIGMA_FILE_KEY="file-key-from-url"
```

**使用场景：**
- 获取设计稿链接
- 创建设计评论
- 导出设计资源

**降级方案：**
```
无 API → 输出文字原型描述
用户手动在 Figma 中创建
```

---

### GitHub 配置

**前提条件：**
- GitHub 账号
- Personal Access Token

**获取 Token：**
1. 访问：https://github.com/settings/tokens
2. 点击"Generate new token (classic)"
3. 选择权限：`repo`、`workflow`
4. 记录：`GITHUB_TOKEN`

**环境变量：**
```bash
export GITHUB_TOKEN="your-token"
export GITHUB_REPO="owner/repo"
```

**测试连接：**
```bash
cd scripts
python git-create-branch.py "feature/new-feature"
```

---

### 钉钉配置

**前提条件：**
- 钉钉群机器人
- Webhook URL

**获取 Webhook：**
1. 钉钉群 → 群设置 → 智能群助手
2. 添加机器人 → 自定义
3. 记录：`DINGTALK_WEBHOOK`

**环境变量：**
```bash
export DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=xxx"
```

**测试连接：**
```bash
cd scripts
python dingtalk-notify.py "测试通知" "这是一条测试消息"
```

---

### 企业微信配置

**前提条件：**
- 企业微信群机器人
- Webhook URL

**获取 Webhook：**
1. 企业微信群 → 群设置 → 群机器人
2. 添加机器人
3. 记录：`WECOM_WEBHOOK`

**环境变量：**
```bash
export WECOM_WEBHOOK="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
```

---

### 飞书配置

**前提条件：**
- 飞书群机器人
- Webhook URL

**获取 Webhook：**
1. 飞书群 → 群设置 → 群机器人
2. 添加机器人
3. 记录：`FEISHU_WEBHOOK`

**环境变量：**
```bash
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

---

### Google Search 配置

**前提条件：**
- Google Custom Search API Key
- Custom Search Engine ID

**获取 API Key：**
1. 访问：https://developers.google.com/custom-search/v1/introduction
2. 点击"Get a Key"
3. 记录：`GOOGLE_API_KEY`、`GOOGLE_CSE_ID`

**环境变量：**
```bash
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CSE_ID="your-cse-id"
```

**降级方案：**
```
无 API → 使用 SearXNG（内置，无需配置）
```

---

## 🛠️ 自定义工具绑定

### 如何添加自己的工具？

**步骤 1：创建工具脚本**

在 `scripts/` 目录创建脚本，例如：
```bash
scripts/mytool-create-issue.py
```

**步骤 2：实现降级逻辑**

```python
#!/usr/bin/env python3
"""
我的工具集成脚本（含降级）
"""

import os
import sys

def create_with_fallback(title, description):
    """创建 Issue，失败则输出 Markdown"""
    
    # 检测是否有 API 配置
    api_key = os.getenv('MYTOOL_API_KEY')
    
    if not api_key:
        # Level 3：降级输出 Markdown
        return f"""
📋 待创建 Issue

**标题：** {title}
**描述：** {description}

**操作：** 请手动在 [工具名称] 中创建
"""
    
    try:
        # Level 1：调用 API
        # ... API 调用代码 ...
        return f"✅ 已创建：[链接]"
    
    except Exception as e:
        # Level 3：降级输出 Markdown
        return f"""
⚠️ API 调用失败：{e}

📋 待创建 Issue（手动创建）

**标题：** {title}
**描述：** {description}
"""

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python mytool-create-issue.py \"标题\" \"描述\"")
        sys.exit(1)
    
    title = sys.argv[1]
    description = sys.argv[2]
    
    result = create_with_fallback(title, description)
    print(result)
```

**步骤 3：在提示词中引用**

修改 `prompts/xxx.md`，添加：
```markdown
【工具串联】
- 我的工具：`python scripts/mytool-create-issue.py "标题" "描述"`
```

**步骤 4：提交 PR**

将脚本提交到 GitHub 仓库，我会合并到主分支。

---

### 如何请求支持新工具？

**方式 1：GitHub Issue**

访问：https://github.com/lj22503/financial-product-workflow/issues

**标题：** [工具支持] 请添加 [工具名称] 支持

**内容：**
```
**工具名称：** [如：Teambition]
**使用场景：** [如：任务管理]
**API 文档：** [链接]
**为什么需要：** [说明原因]
**优先级：** 高/中/低
```

**方式 2：微信反馈**

添加微信，回复"工具支持 + 工具名称"

**方式 3：邮件反馈**

发送邮件到：[你的邮箱]

---

## 📊 支持状态说明

| 状态 | 说明 | 配置难度 |
|------|------|---------|
| ✅ 已支持 | 有脚本 + API 配置指南 | ⭐⭐（10-30 分钟） |
| ⚠️ 部分支持 | 有 API 指南，无脚本 | ⭐⭐⭐（30-60 分钟） |
| ⚠️ 待支持 | 计划支持，等待开发 | - |
| ❌ 不支持 | 暂无计划，可提需求 | - |

---

## 🔄 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0.0 | 2026-03-26 | 初始版本，列出所有工具支持状态 |

---

## ❓ 常见问题

### Q1：我的工具不在列表中，能用吗？

**A：** 可以！使用降级方案。

- **无工具** → 输出 Markdown 文档/待办清单
- **手动创建** → 在你的工具中手动创建
- **请求支持** → 提交 GitHub Issue

---

### Q2：如何知道我的工具是否支持？

**A：** 查看本清单的"支持状态"列。

- ✅ 已支持 → 按配置指南操作
- ⚠️ 待支持 → 使用降级方案，或提交需求
- ❌ 不支持 → 使用降级方案

---

### Q3：配置 API 安全吗？

**A：** 安全。

- API Token 存储在本地环境变量
- 不会上传到云端
- 仅用于工具调用

**建议：**
- 使用只读 Token（如可能）
- 定期更换 Token
- 不要提交到 Git

---

### Q4：多个工具可以混用吗？

**A：** 可以！

例如：
- Jira（需求管理）+ Confluence（文档）+ 钉钉（通知）
- GitHub（代码）+ 飞书文档（PRD）+ 企业微信（通知）

**Skill 会自动检测每个工具的配置状态，分别处理。**

---

*如有问题或建议，欢迎提交 GitHub Issue 或微信反馈。*
