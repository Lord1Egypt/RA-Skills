---
slug: "email-daily-summary-free"
name: "email-daily-summary-free"
version: "1.0.0"
displayName: "邮件摘要免费版"
summary: "基于 browser-,提供核心能力"
summary_zh: "基于 browser-,提供核心能力"
license: "MIT"
description: "|- 基于 browser-use CLI 自发化登录 Gmail、Outlook、QQ 邮箱等 Web 邮箱, 抓取当日收件箱列表,提取发件人、主题、摘要片段与时间戳,产出基础邮件日报. 兼容未读统计与截图归档。适用于个人开发者每日邮件快速梳理场景.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
tags:
  - Communication
  - Email
  - 邮件
  - 通信
  - 工具
  - browser-use
  - chrome
  - browser
  - real
  - 邮箱
tools:
  - read
  - exec
  - write
homepage: ""
category: "Communication"
pricing_tier: free
---
# Email Daily Summary Free

通过 `browser-use` CLI 驱动浏览器自动化登录 Web 邮箱,抓取当日邮件并生成基础日报。本免费版支持单邮箱当日摘要,适合个人日常使用.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Email Summary Free处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

- **单邮箱登录**:复用 Chrome 已登录会话(`--browser real`),覆盖 Gmail、Outlook、QQ 邮箱
- **邮件列表抓取**:通过 DOM 选择器提取发件人、主题、摘要片段、时间戳四元组
- **未读统计**:实时计算未读数与可见邮件总数
- **截图归档**:当日 inbox 快照保存为 PNG
- **基础日报**:生成 Markdown 格式邮件日报
### 单邮箱登录

针对单邮箱登录,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供单邮箱登录相关的配置参数、输入数据和处理选项.
**输出**: 返回单邮箱登录的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`单邮箱登录`的配置文档进行参数调优
### 邮件列表抓取

针对邮件列表抓取,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供邮件列表抓取相关的配置参数、输入数据和处理选项.
**输出**: 返回邮件列表抓取的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`邮件列表抓取`的配置文档进行参数调优
### 未读统计

针对未读统计,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供未读统计相关的配置参数、输入数据和处理选项.
**输出**: 返回未读统计的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`未读统计`的配置文档进行参数调优
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 前置依赖

1. 安装 browser-use CLI:

```bash
uv pip install browser-use[cli]
browser-use install
```

2. 在本机 Chrome 中至少登录过一次目标邮箱(用于 `--browser real` 复用会话)

## 支持的邮箱服务

| 邮箱服务 | 收件箱 URL |
|---:|---:|
| Gmail | https://mail.google.com |
| Outlook | https://example.com.com |
| QQ 邮箱 | https://mail.qq.com |

## 使用流程

1. 确认 `browser-use --version` 可正常输出
2. 使用 `--browser real` 打开目标邮箱收件箱 URL
3. `browser-use state` 探测当前 DOM 结构
4. 执行 `eval` 脚本提取邮件四元组
5. `screenshot` 归档快照,`browser-use close` 释放会话

## 适用场景

### 场景 1:每日邮件快速梳理

- **输入**:Gmail 收件箱 URL + 当日日期
- **输出**:Markdown 日报,含未读数、前 20 封邮件列表;附 inbox 截图

## 案例展示

### 案例 1:生成今日 Gmail 日报

```bash
DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="./email_summaries"
mkdir -p "$OUTPUT_DIR"
# ...
browser-use --browser real open https://mail.google.com
sleep 3
# ...
browser-use state
browser-use screenshot "$OUTPUT_DIR/inbox_$DATE.png"
# ...
browser-use eval "
  const emails = [];
  document.querySelectorAll('tr.zA').forEach((row, i) => {
    if (i < 20) {
      const sender = row.querySelector('.yX.xY span')?.innerText || '';
      const subject = row.querySelector('.y6 span')?.innerText || '';
      const snippet = row.querySelector('.y2')?.innerText || '';
      const time = row.querySelector('.xW.xY span')?.innerText || '';
      emails.push({ sender, subject, snippet, time });
    }
  });
  JSON.stringify(emails, null, 2);
"
# ...
browser-use close
```

输出示例:

```text
==========================================
邮件日报 - 2026-07-20
==========================================
未读邮件: 12 封
可见邮件: 50 封
# ...
前 20 封邮件:
1. boss@company.com | 项目进度汇报 | 09:30
2. finance@bank.com | 账单提醒 | 08:15
...
==========================================
```

## 异常处理

### 1. browser-use CLI 未安装

- **现象**:执行 `browser-use` 报 `command not found`
- **处理**:`uv pip install browser-use[cli]` 后执行 `browser-use install`

### 2. Chrome 会话过期

- **现象**:`--browser real` 打开邮箱后跳转到登录页
- **处理**:在本机 Chrome 中重新登录目标邮箱后检查网络连接和配置后重试

### 3. CSS 选择器失效

- **现象**:`eval` 返回空数组但页面有邮件
- **处理**:`browser-use state` 重新探测 DOM,更新选择器

### 4. 邮件列表加载缓慢

- **现象**:`state` 显示已加载但 `tr.zA` 数量为 0
- **处理**:在 `open` 与 `eval` 之间插入 `sleep 5`

### 5. screenshot 写入失败

- **现象**:截图报权限错误
- **处理**:执行前 `mkdir -p "$OUTPUT_DIR"` 创建目录并确认写权限

## FAQ

### Q1:如何避免在脚本中保存邮箱密码?

使用 `--browser real` 模式复用本机 Chrome 已登录会话,凭证由 Chrome 管理,脚本不接触密码.
### Q2:支持哪些邮箱?

免费版支持 Gmail、Outlook、QQ 邮箱。163/126/企业微信邮箱及多账号汇总需升级付费版.
### Q3:邮件量很大时怎么办?

免费版单次抓取前 20 封,可通过滚动加载更多。超大量邮箱(>100 封/日)建议升级付费版使用分页抓取.
### Q4:可以定时自动执行吗?

免费版不提供定时任务模板。每日需手动执行。定时调度、launchd 配置需升级付费版.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 检查网络连接和配置后重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- 仅支持单邮箱当日摘要,不支持多账号汇总
- CSS 选择器依赖邮箱 Web 版 DOM 结构,改版可能导致失效
- `--browser real` 需要本机 Chrome 已登录,服务器环境不适用
- 不支持 AI 智能摘要、关键词监控、周报统计等高级功能
- 验证码、二次验证必须人工干预

## 升级提示

需要多账号汇总、AI 智能摘要、关键词监控告警、周报统计、定时任务调度等高级功能?升级至 **email-daily-summary 付费版**,获取完整能力:

- 6 大邮箱全覆盖(Gmail/Outlook/QQ/163/126/企业微信邮箱)
- 跨账号合并日报
- AI 自然语言摘要(`browser-use extract`)
- 发件人白名单监控告警
- 周报邮件统计与趋势分析
- 定时任务管理 + launchd 定时任务模板
- 大邮件量分页抓取(>100 封)

前往 SkillHub 搜索 `email-daily-summary` 获取付费版.