---
name: connector-hub
author: 王教成 Wang Jiaocheng (波动几何)
description: 连接器全景中心——33 个连接器的统一入口。三层分类（平台级/鉴权便利型/纯API查询型），决策树选择，每个连接器有独立参考文件和可执行脚本（前缀区分）。能用 Skill 替代的提供完整替代方案（scripts/references），不可替代的标注原因。触发词：连接器、connector、MCP、API对接、平台集成、数据源。
---

# 连接器全景中心

## 使用方式

### 快速使用

1. **查看所有连接器**：阅读本文件的注册表
2. **选择连接器**：根据需求在第二章找到对应连接器
3. **读取参考文件**：加载 `references/` 中的参考文件获取详细方案
4. **运行脚本**：使用 `scripts/` 中的 Python 脚本执行操作

### 目录结构

```
connector-hub/
├── SKILL.md                    # 本文件（注册表 + 决策树）
├── references/                 # 参考文档（33 个，扁平结构）
│   ├── L1-platform-*.md        # 平台级连接器参考
│   ├── L2-auth-*.md            # 鉴权便利型连接器参考
│   └── L3-api-*.md             # 纯 API 查询型连接器参考
└── scripts/                    # 可执行脚本（48 个）
    ├── L2-auth-*.py            # 鉴权便利型脚本
    └── L3-api-*.py             # 纯 API 查询型脚本
```

### 运行脚本

```bash
# 设置环境变量
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# 运行脚本
python scripts/L2-auth-messaging-C12-feishu-send-text.py "测试消息"
```

### 前缀规则

| 前缀 | 分类 | 数量 |
|------|------|------|
| `L1-platform-` | 平台级（不可替代） | 4 |
| `L2-auth-docs-kb-` | 鉴权便利型-文档/知识库 | 7 |
| `L2-auth-messaging-` | 鉴权便利型-消息/通讯 | 5 |
| `L2-auth-storage-` | 鉴权便利型-存储 | 2 |
| `L3-api-enterprise-` | 纯API查询型-企业查询 | 3 |
| `L3-api-finance-` | 纯API查询型-金融数据 | 1 |
| `L3-api-code-hosting-` | 纯API查询型-代码托管 | 4 |
| `L3-api-project-mgmt-` | 纯API查询型-项目管理 | 2 |
| `L3-api-biz-services-` | 纯API查询型-业务服务 | 5 |

## 触发词

连接器、connector、MCP、API对接、平台集成、数据源、企业微信、飞书、钉钉、天眼查、企查查、GitHub、TAPD、百度网盘、腾讯文档

---

# 第一章 三层分类

## 1.1 分类逻辑

```
用户需求
    ↓
┌─────────────────────────────────────────┐
│ 需要平台实时运行环境？                    │
│ （云函数/部署/CI/音视频）                 │
└────────────┬────────────────┬───────────┘
             │ 是             │ 否
             ↓                ↓
      L1 平台级          ┌─────────────────────────┐
      （不可替代）        │ 频繁交互 + 鉴权复杂？     │
                         │ （文档/消息/存储）         │
                         └────────┬────────┬────────┘
                                  │ 是     │ 否
                                  ↓        ↓
                           L2 鉴权便利型   L3 纯API查询型
                           （看需求选）    （没必要用连接器）
```

## 1.2 总览表

| 层级 | 分类 | 数量 | Skill 替代 | 建议 |
|------|------|------|-----------|------|
| L1 | 平台级实时能力 | 4 | ❌ 不可能 | 必须保留连接器 |
| L2 | 鉴权便利型 | 14 | ✅ 可替代 | 频繁用→保留；偶尔用→Skill |
| L3 | 纯 API 查询型 | 15 | ✅ 完全可替代 | 全部用 Skill |

---

# 第二章 连接器注册表

## 2.1 L1 平台级（不可替代）

| ID | 连接器 | 名称 | 能力 | 不可替代原因 | 详细参考 |
|----|--------|------|------|-------------|---------|
| C01 | cloudbase | 腾讯云 CloudBase | 云函数/数据库/托管 | 需要平台运行时环境 | `references/L1-platform-C01-cloudbase.md` |
| C02 | edgeone-pages | EdgeOne Pages | 静态站点部署/CDN | 需要平台 CDN 节点和域名 | `references/L1-platform-C02-edgeone-pages.md` |
| C03 | zhiyan-ci-cd | 智研构建部署 | CI/CD 流水线 | 需要平台构建环境和制品库 | `references/L1-platform-C03-zhiyan-ci-cd.md` |
| C04 | tmeet | 腾讯会议 | 实时音视频/会议管理 | 需要平台实时通信基础设施 | `references/L1-platform-C04-tmeet.md` |

## 2.2 L2 鉴权便利型（可替代但需自管凭证）

### 文档/知识库类（7 个）

| ID | 连接器 | 名称 | 本质 | Skill 替代核心脚本 | 详细参考 |
|----|--------|------|------|-------------------|---------|
| C05 | tencent-docs | 腾讯文档 | 文档 CRUD API | L2-auth-docs-kb-C05-tencent-docs-create-doc.py | `references/L2-auth-docs-kb-C05-tencent-docs.md` |
| C06 | kdocs | 金山文档 | 文档 CRUD API | L2-auth-docs-kb-C06-kdocs-create-doc.py | `references/L2-auth-docs-kb-C06-kdocs.md` |
| C07 | notion | Notion | 文档 CRUD API | L2-auth-docs-kb-C07-notion-create-page.py, L2-auth-docs-kb-C07-notion-query-database.py | `references/L2-auth-docs-kb-C07-notion.md` |
| C08 | lexiang | 乐享知识库 | 知识库读取 API | L2-auth-docs-kb-C08-lexiang-search-docs.py | `references/L2-auth-docs-kb-C08-lexiang.md` |
| C09 | iwiki-woa | iWiki | 知识库读取 API | L2-auth-docs-kb-C09-iwiki-search.py | `references/L2-auth-docs-kb-C09-iwiki.md` |
| C10 | km | KM | 知识管理 API | L2-auth-docs-kb-C10-km-search.py | `references/L2-auth-docs-kb-C10-km.md` |
| C11 | ima-mcp | ima知识库 | 知识库读取 API | L2-auth-docs-kb-C11-ima-search.py | `references/L2-auth-docs-kb-C11-ima.md` |

### 消息/通讯类（5 个）

| ID | 连接器 | 名称 | 本质 | Skill 替代核心脚本 | 详细参考 |
|----|--------|------|------|-------------------|---------|
| C12 | feishu | 飞书 | Webhook + Bot API | L2-auth-messaging-C12-feishu-send-text.py, L2-auth-messaging-C12-feishu-send-post.py, L2-auth-messaging-C12-feishu-send-card.py | `references/L2-auth-messaging-C12-feishu.md` |
| C13 | dingtalk | 钉钉 | Webhook + Bot API | L2-auth-messaging-C13-dingtalk-send-text.py, L2-auth-messaging-C13-dingtalk-send-markdown.py, L2-auth-messaging-C13-dingtalk-send-action-card.py | `references/L2-auth-messaging-C13-dingtalk.md` |
| C14 | wecom | 企业微信 | Webhook + Bot API | L2-auth-messaging-C14-wecom-send-text.py, L2-auth-messaging-C14-wecom-send-markdown.py, L2-auth-messaging-C14-wecom-send-news.py | `references/L2-auth-messaging-C14-wecom.md` |
| C15 | qq-mail | QQ邮箱 | SMTP/API | L2-auth-messaging-C15-qq-mail-send-email.py | `references/L2-auth-messaging-C15-qq-mail.md` |
| C16 | netease-mail | 网易邮箱 | SMTP/API | L2-auth-messaging-C16-netease-mail-send-email.py | `references/L2-auth-messaging-C16-netease-mail.md` |

### 存储类（2 个）

| ID | 连接器 | 名称 | 本质 | Skill 替代核心脚本 | 详细参考 |
|----|--------|------|------|-------------------|---------|
| C17 | baidu-netdisk | 百度网盘 | 文件存储 API | L2-auth-storage-C17-baidu-list-files.py, L2-auth-storage-C17-baidu-upload.py | `references/L2-auth-storage-C17-baidu-netdisk.md` |
| C18 | tencent-weiyun | 微云 | 文件存储 API | L2-auth-storage-C18-tencent-weiyun-list-files.py | `references/L2-auth-storage-C18-tencent-weiyun.md` |

## 2.3 L3 纯 API 查询型（完全没必要用连接器）

### 企业/商业信息查询（3 个）

| ID | 连接器 | 名称 | 本质 | Skill 替代核心脚本 | 详细参考 |
|----|--------|------|------|-------------------|---------|
| C19 | tyc-mcp | 天眼查 | 企业信息查询 API | L3-api-enterprise-C19-tyc-query-basic.py | `references/L3-api-enterprise-C19-tyc-mcp.md` |
| C20 | qcc-company | 企查查 | 企业信息查询 API | L3-api-enterprise-C20-qcc-query-basic.py | `references/L3-api-enterprise-C20-qcc-company.md` |
| C21 | pkulaw | 北大法宝 | 法律文献检索 API | L3-api-enterprise-C21-pkulaw-search-law.py, L3-api-enterprise-C21-pkulaw-search-case.py | `references/L3-api-enterprise-C21-pkulaw.md` |

### 金融数据（1 个）

| ID | 连接器 | 名称 | 本质 | Skill 替代核心脚本 | 详细参考 |
|----|--------|------|------|-------------------|---------|
| C22 | tdx-connector | 通达信 | 行情/财务数据 API | L3-api-finance-C22-tdx-realtime-quote.py, L3-api-finance-C22-tdx-kline-data.py | `references/L3-api-finance-C22-tdx-connector.md` |

### 代码托管（4 个）

| ID | 连接器 | 名称 | 本质 | Skill 替代核心脚本 | 详细参考 |
|----|--------|------|------|-------------------|---------|
| C23 | github | GitHub | Git CLI + API | L3-api-code-hosting-C23-github-create-pr.py, L3-api-code-hosting-C23-github-manage-issues.py | `references/L3-api-code-hosting-C23-github.md` |
| C24 | cnb-api | CNB | 代码托管 API | L3-api-code-hosting-C24-cnb-repo-operations.py, L3-api-code-hosting-C24-cnb-mr-operations.py | `references/L3-api-code-hosting-C24-cnb-api.md` |
| C25 | cnb-woa | CNB司内版 | 代码托管 API | L3-api-code-hosting-C25-cnb-woa-repo-operations.py, L3-api-code-hosting-C25-cnb-woa-mr-operations.py | `references/L3-api-code-hosting-C25-cnb-woa.md` |
| C26 | gongfeng-woa | Gongfeng | 代码托管 API | L3-api-code-hosting-C26-gongfeng-repo-operations.py, L3-api-code-hosting-C26-gongfeng-mr-operations.py | `references/L3-api-code-hosting-C26-gongfeng.md` |

### 项目管理（2 个）

| ID | 连接器 | 名称 | 本质 | Skill 替代核心脚本 | 详细参考 |
|----|--------|------|------|-------------------|---------|
| C27 | tapd | TAPD | 项目管理 API | L3-api-project-mgmt-C27-tapd-create-story.py, L3-api-project-mgmt-C27-tapd-create-bug.py | `references/L3-api-project-mgmt-C27-tapd.md` |
| C28 | tapd-woa | TAPD司内版 | 项目管理 API | L3-api-project-mgmt-C28-tapd-woa-create-story.py, L3-api-project-mgmt-C28-tapd-woa-create-bug.py | `references/L3-api-project-mgmt-C28-tapd-woa.md` |

### 业务服务（5 个）

| ID | 连接器 | 名称 | 本质 | Skill 替代核心脚本 | 详细参考 |
|----|--------|------|------|-------------------|---------|
| C29 | ctrip-wendao | 携程问道 | 旅行信息查询 API | L3-api-biz-services-C29-ctrip-search-flights.py, L3-api-biz-services-C29-ctrip-search-hotels.py | `references/L3-api-biz-services-C29-ctrip.md` |
| C30 | tencent-qidian-cs | 腾讯企点客服 | 客服系统 API | L3-api-biz-services-C30-qidian-cs-create-session.py, L3-api-biz-services-C30-qidian-cs-send-reply.py | `references/L3-api-biz-services-C30-qidian-cs.md` |
| C31 | tencent-survey | 腾讯问卷 | 问卷系统 API | L3-api-biz-services-C31-tencent-survey-create-survey.py | `references/L3-api-biz-services-C31-tencent-survey.md` |
| C32 | neo-crm | 销售易 CRM | CRM 系统 API | L3-api-biz-services-C32-neo-crm-create-lead.py, L3-api-biz-services-C32-neo-crm-query-pipeline.py | `references/L3-api-biz-services-C32-neo-crm.md` |
| C33 | fbs-connector | 福帮手 | 业务服务 API | L3-api-biz-services-C33-fbs-create-request.py | `references/L3-api-biz-services-C33-fbs.md` |

---

# 第三章 决策树

## 3.1 选择连接器还是 Skill？

```
用户需求：我需要对接 XX 平台
    ↓
┌─────────────────────────────────┐
│ Q1: 需要平台实时运行环境吗？      │
│ （云函数/部署/CI/音视频）         │
└────────────┬────────────────────┘
             │
    ┌────────┴────────┐
    ↓                 ↓
   是                 否
    ↓                 ↓
┌───────────┐   ┌─────────────────────────┐
│ 用连接器   │   │ Q2: 频繁使用吗？          │
│ L1 不可替代│   │ （每天/每周多次）          │
└───────────┘   └────────┬────────────────┘
                         │
                ┌────────┴────────┐
                ↓                 ↓
               是                 否
                ↓                 ↓
        ┌───────────────┐   ┌───────────────┐
        │ 看 L2 连接器   │   │ 用 Skill 替代  |
        │ 鉴权省事       │   │ L3 完全覆盖    │
        └───────────────┘   └───────────────┘
```

## 3.2 Skill 替代优势

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管，用户无感知 | 用户自管，可审计 |
| API 调用 | 单一 API | 多 API 编排组合 |
| 数据处理 | 原样返回 | 可自定义转换/清洗 |
| 多服务商 | 绑定一个 | 配置文件切换多个 |
| 输出格式 | 固定 | 模板化，可定制 |
| 迁移成本 | 换平台=重配连接器 | 改 API 地址即可 |
| 可审计性 | 黑盒 | 完全透明 |

## 3.3 迁移示例

**从天眼查迁移到企查查（Skill 方式）：**
```python
# 只需改 config/providers.json
{
  "default_provider": "qichacha",  # 改这一行
  "providers": {
    "tianyancha": { ... },
    "qichacha": { ... }
  }
}
```

**连接器迁移需要：**
1. 重新申请授权
2. 重新配置连接器
3. 验证所有工作流

---

# 附录：连接器与 Skill 对照表

| 连接器 | Skill 替代 | 核心 scripts | 鉴权方式 | 迁移成本 |
|--------|-----------|-------------|---------|---------|
| cloudbase | ❌ | — | — | — |
| edgeone-pages | ❌ | — | — | — |
| zhiyan-ci-cd | ❌ | — | — | — |
| tmeet | ❌ | — | — | — |
| tencent-docs | ✅ | L2-auth-docs-kb-C05-tencent-docs-create-doc.py | OAuth2 | 低 |
| kdocs | ✅ | L2-auth-docs-kb-C06-kdocs-create-doc.py | OAuth2 | 低 |
| notion | ✅ | L2-auth-docs-kb-C07-notion-create-page.py, L2-auth-docs-kb-C07-notion-query-database.py | Token/OAuth2 | 极低 |
| lexiang | ✅ | L2-auth-docs-kb-C08-lexiang-search-docs.py | OAuth2/API Key | 低 |
| iwiki-woa | ✅ | L2-auth-docs-kb-C09-iwiki-search.py | SSO/Cookie | 低 |
| km | ✅ | L2-auth-docs-kb-C10-km-search.py | SSO/Cookie | 低 |
| ima-mcp | ✅ | L2-auth-docs-kb-C11-ima-search.py | SSO/Cookie | 低 |
| feishu | ✅ | L2-auth-messaging-C12-feishu-send-text.py, L2-auth-messaging-C12-feishu-send-post.py, L2-auth-messaging-C12-feishu-send-card.py | Webhook/OAuth2 | 低 |
| dingtalk | ✅ | L2-auth-messaging-C13-dingtalk-send-text.py, L2-auth-messaging-C13-dingtalk-send-markdown.py, L2-auth-messaging-C13-dingtalk-send-action-card.py | Webhook | 低 |
| wecom | ✅ | L2-auth-messaging-C14-wecom-send-text.py, L2-auth-messaging-C14-wecom-send-markdown.py, L2-auth-messaging-C14-wecom-send-news.py | Webhook/OAuth2 | 低 |
| qq-mail | ✅ | L2-auth-messaging-C15-qq-mail-send-email.py | SMTP+授权码 | 低 |
| netease-mail | ✅ | L2-auth-messaging-C16-netease-mail-send-email.py | SMTP+授权码 | 低 |
| baidu-netdisk | ✅ | L2-auth-storage-C17-baidu-list-files.py, L2-auth-storage-C17-baidu-upload.py | OAuth2 | 低 |
| tencent-weiyun | ✅ | L2-auth-storage-C18-tencent-weiyun-list-files.py | OAuth2 | 低 |
| tyc-mcp | ✅ | L3-api-enterprise-C19-tyc-query-basic.py | API Key | 低 |
| qcc-company | ✅ | L3-api-enterprise-C20-qcc-query-basic.py | API Key | 低 |
| pkulaw | ✅ | L3-api-enterprise-C21-pkulaw-search-law.py, L3-api-enterprise-C21-pkulaw-search-case.py | API Key | 低 |
| tdx-connector | ✅ | L3-api-finance-C22-tdx-realtime-quote.py, L3-api-finance-C22-tdx-kline-data.py | 无需鉴权 | 极低 |
| github | ✅ | L3-api-code-hosting-C23-github-create-pr.py, L3-api-code-hosting-C23-github-manage-issues.py | gh auth/Token | 极低 |
| cnb-api | ✅ | L3-api-code-hosting-C24-cnb-repo-operations.py, L3-api-code-hosting-C24-cnb-mr-operations.py | Token/OAuth2 | 低 |
| cnb-woa | ✅ | L3-api-code-hosting-C25-cnb-woa-repo-operations.py, L3-api-code-hosting-C25-cnb-woa-mr-operations.py | Token/OAuth2 | 低 |
| gongfeng-woa | ✅ | L3-api-code-hosting-C26-gongfeng-repo-operations.py, L3-api-code-hosting-C26-gongfeng-mr-operations.py | Token/OAuth2 | 低 |
| tapd | ✅ | L3-api-project-mgmt-C27-tapd-create-story.py, L3-api-project-mgmt-C27-tapd-create-bug.py | Token | 低 |
| tapd-woa | ✅ | L3-api-project-mgmt-C28-tapd-woa-create-story.py, L3-api-project-mgmt-C28-tapd-woa-create-bug.py | Token | 低 |
| ctrip-wendao | ✅ | L3-api-biz-services-C29-ctrip-search-flights.py, L3-api-biz-services-C29-ctrip-search-hotels.py | API Key | 低 |
| tencent-qidian-cs | ✅ | L3-api-biz-services-C30-qidian-cs-create-session.py, L3-api-biz-services-C30-qidian-cs-send-reply.py | OAuth2 | 低 |
| tencent-survey | ✅ | L3-api-biz-services-C31-tencent-survey-create-survey.py | OAuth2 | 低 |
| neo-crm | ✅ | L3-api-biz-services-C32-neo-crm-create-lead.py, L3-api-biz-services-C32-neo-crm-query-pipeline.py | OAuth2 | 低 |
| fbs-connector | ✅ | L3-api-biz-services-C33-fbs-create-request.py | API Key/SSO | 低 |
