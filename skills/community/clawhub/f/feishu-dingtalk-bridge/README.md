# 🌐 飞书钉钉协同中枢 (feishu-dingtalk-bridge)

> 企业IM/审批/日历/文档API的结构化工作流引擎 | 开箱即用 | 安全合规

## 🎯 功能简介
将飞书/钉钉开放平台能力转化为标准化 AI 任务流，自动聚合碎片信息、识别流程阻塞点、生成可执行待办清单。适用于行政、项目管理、售前支持、跨部门协同等场景。

## 🚀 快速开始
### 1. 获取访问凭证
- **飞书**：登录[飞书开放平台](https://open.feishu.cn/) → 创建企业自建应用 → 开通 `日历`/`审批`/`文档` 权限 → 获取 `tenant_access_token`
- **钉钉**：登录[钉钉开放平台](https://open.dingtalk.com/) → 创建应用 → 申请 `工作流`/`日历`/`云盘` 权限 → 获取 `access_token`

### 2. 配置调用
```json
{
  "skill": "feishu_dingtalk_bridge",
  "inputs": {
    "platform": "feishu",
    "action": "sync_calendar",
    "auth_token": "{{YOUR_TOKEN}}",
    "query_context": "2024-10-01至2024-10-31"
  }
}
