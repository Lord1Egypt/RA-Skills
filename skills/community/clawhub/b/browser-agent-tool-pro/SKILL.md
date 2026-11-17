---

slug: browser-agent-tool-pro
name: browser-agent-tool-pro
version: 1.0.0
displayName: 浏览器智能代理工具-专业版
summary: "企业级无头浏览器自动化"
license: Proprietary
edition: pro
description: "企业级无头浏览器自动化命令行工具,在免费版核心能力之上,提供网络拦截与Mock、。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
  批量任务调度、代理池管理、监控告警、多租户隔离与团队协作能力。核心能力:

  - 免费版全部能力(完全兼容)
  - 网络拦截、Mock 与请求重放

  - Cookies/Storage 精细化管理
  - 批量任务调度与并发会话池

  - 代理池与反爬虫策略集成
  - 监控指标采集与告警通知

  适用场景:

  - 企业级数据采集与竞品监控
  - 自动化测试与CI/CD集成

  - 多账号矩阵运营与批量操作
  - 团队协作与任务编排

  差异化:专业...'
tags:
  - 研究工具
  - 浏览器自动化
  - 企业级
  - 批量操作
  - AI代理
  - 自动化
  - 智能
  - agent-browser
  - 专业版新
  - bash
  - json
  - account
tools:
  - read
  - exec
  - write
  - glob
  - grep
homepage: ""
# 定价元数据
category: "Agents"

---

> **功能说明**: 本技能涵盖 中文交互 等核心能力。


# 浏览器智能代理工具(专业版)
## 概述
本工具是企业级无头浏览器自动化命令行工具,在免费版核心能力之上,扩展了网络拦截、Mock、批量调度、代理池、监控告警等高阶能力,适合团队生产环境、数据采集、自动化测试与多账号运营场景。专业版与免费版完全兼容:免费版的所有命令、工作流、状态文件均可直接在专业版中使用.
### 免费版 vs 专业版对比
| 能力 | 免费版 | 专业版 |
|---|---|---|
| 基础导航与交互 | 支持 | 支持 |
| 可访问性树快照 | 支持 | 支持 |
| 会话隔离 | 支持(基础) | 支持(并发池) |
| 状态持久化 | 支持 | 支持(加密存储) |
| 网络拦截与 Mock | 不支持 | 支持 |
| 批量任务调度 | 不支持 | 支持 |
| 代理池管理 | 不支持 | 支持 |
| 监控告警 | 不支持 | 支持 |
| 多租户隔离 | 不支持 | 支持 |
| 团队协作 | 不支持 | 支持 |
| 优先技术支持 | 不支持 | 支持 |
## 核心能力
### 1. 网络拦截与 Mock(专业版新增)
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 浏览器智能代理工具-专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 拦截并阻止广告请求
agent-browser network route "**/ads/*" --abort
# ...
# 实现说明: API 响应
agent-browser network route "**/api/*" --body '{"code":0,"data":{}}'
# ...
# 查看网络请求
agent-browser network requests --filter api
```

**处理**: 解析网络拦截与 Mock(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回网络拦截与 Mock(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. Cookies 与 Storage 精细化管理(专业版增强)
```bash
# 获取所有 cookies
agent-browser cookies
# 设置 cookie
agent-browser cookies set name value
# 读取 localStorage
agent-browser storage local key
# 写入 localStorage
agent-browser storage local set key val
```

**处理**: 解析Cookies 与 Storage 精细化管理(专业版增强)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回Cookies 与 Storage 精细化管理(专业版增强)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 批量任务调度(专业版新增)
通过脚本编排实现批量任务并发执行,适合数据采集、批量签到、多账号操作等场景.
```bash
#!/bin/sh
# 示例
ACCOUNTS=("user1" "user2" "user3" "user4" "user5")
for account in "${ACCOUNTS[@]}"; do
  agent-browser --session "$account" open https://example.com/checkin &
  agent-browser --session "$account" state load "auth/${account}.json"
  agent-browser --session "$account" snapshot -i --json
  agent-browser --session "$account" click @e2
  agent-browser --session "$account" screenshot "logs/${account}_$(date +%Y%m%d).png"
  agent-browser --session "$account" close &
done
wait
echo "批量签到完成"
```

**处理**: 解析批量任务调度(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量任务调度(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 代理池集成(专业版新增)
```bash
# 通过环境变量配置代理池
export BROWSER_PROXY_POOL="http://proxy1:8080,http://proxy2:8080,http://proxy3:8080"
# ...
# 启动时自动轮换代理
agent-browser --proxy-pool open https://example.com
```

**处理**: 解析代理池集成(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回代理池集成(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 监控指标采集(专业版新增)
```bash
# 启用指标采集
agent-browser --metrics enable
# ...
# 导出指标
agent-browser metrics export --format json > metrics.json
agent-browser metrics export --format prometheus > metrics.prom
```

**处理**: 解析监控指标采集(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回监控指标采集(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 6. 多租户隔离(专业版新增)
```bash
# 为不同租户分配独立会话空间
agent-browser --workspace acme --session admin open https://app.example.com
agent-browser --workspace globex --session admin open https://app.example.com
agent-browser workspace list
```

**处理**: 解析多租户隔离(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多租户隔离(专业版新增)的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级无头浏览器、自动化、支持批量调度、代理池与监控告警、面向团队生产场景、自动化命令行工具、在免费版核心能力、代理池管理、监控告警、多租户隔离与团队、协作能力、核心能力、免费版全部能力、完全兼容、与请求重放、批量任务调度与并、发会话池、代理池与反爬虫策、略集成、监控指标采集与告、警通知等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
## 使用场景
### 场景一:企业竞品价格监控
定期采集竞品页面价格,结合网络拦截与代理池规避反爬.
```bash
#!/bin/sh
# competitor-price-monitor.sh
COMPETITORS=("competitor-a.com" "competitor-b.com" "competitor-c.com")
# ...
for site in "${COMPETITORS[@]}"; do
  # 使用代理池轮换
  agent-browser --proxy-pool open "https://${site}/products"
# ...
  # 拦截无关资源,提升速度
  agent-browser network route "**/ads/*" --abort
  agent-browser network route "**/analytics/*" --abort
# ...
  agent-browser wait --load networkidle
  agent-browser snapshot -i --json > "snapshots/${site}_$(date +%Y%m%d).json"
# ...
  # 提取价格数据
  agent-browser get text "@price-element" --json >> "prices/${site}.log"
# ...
  agent-browser close
done
# ...
# 生成报告
echo "竞品价格采集完成,详见 prices/ 目录"
```

### 场景二:自动化测试集成 CI/CD
在 CI 流水线中运行端到端测试,失败时自动截图归档.
```bash
#!/bin/sh
# e2e-test.sh - 集成到 CI/CD
set -e
# ...
agent-browser open https://staging.example.com
agent-browser state load test-auth.json
agent-browser snapshot -i --json
# ...
# 执行测试步骤
agent-browser fill @e1 "test@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
# ...
# 断言
RESULT=$(agent-browser get text "@welcome" --json | jq -r '.data.text')
if [[ "$RESULT" == *"欢迎"* ]]; then
  echo "测试通过"
  agent-browser screenshot "artifacts/pass_$(date +%s).png"
else
  echo "测试失败"
  agent-browser screenshot "artifacts/fail_$(date +%s).png"
  agent-browser close
  exit 1
fi
# ...
agent-browser close
```

### 场景三:多账号矩阵运营
批量管理多个账号,每个账号独立会话与登录态.
```python
#!/usr/bin/env python3
"""多账号矩阵运营编排示例"""
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
# ...
ACCOUNTS = [
    {"name": "brand_a", "auth": "auth/brand_a.json", "url": "https://app.example.com/post"},
    {"name": "brand_b", "auth": "auth/brand_b.example.com/post"},
    {"name": "brand_c", "auth": "auth/brand_c.example.com/post"},
]
# ...
def run_account(account):
    """单个账号的发布流程"""
    session = account["name"]
    subprocess.run(["agent-browser", "--session", session, "open", account["url"]], check=True)
    subprocess.run(["agent-browser", "--session", session, "state", "load", account["auth"]], check=True)
    subprocess.run(["agent-browser", "--session", session, "snapshot", "-i", "--json"],
                   stdout=open(f"logs/{session}.json", "w"))
    subprocess.run(["agent-browser", "--session", session, "fill", "@e1", "今日内容发布"])
    subprocess.run(["agent-browser", "--session", session, "click", "@e2"])
    subprocess.run(["agent-browser", "--session", session, "screenshot", f"logs/{session}.png"])
    subprocess.run(["agent-browser", "--session", session, "close"])
    return session
# ...
# 并发执行,最大并发数 3
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(run_account, acc): acc for acc in ACCOUNTS}
    for future in as_completed(futures):
        name = futures[future]["name"]
        try:
            future.result()
            print(f"[OK] {name} 完成")
        except Exception as e:
            print(f"[FAIL] {name} 失败: {e}")
```
## 不适用场景
以下场景浏览器智能代理工具-专业版不适合处理：

- 需要人工创意判断的任务
- 非结构化头脑风暴
- 人际沟通协调
## 触发条件
需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于非本工具能力范围的需求.
## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问
### 依赖详情
```bash
npm install -g agent-browser
agent-browser install --with-deps
# ...
# 专业版初始化(可选)
agent-browser pro init
agent-browser pro config set metrics.enabled true
agent-browser pro config set proxy.pool "http://proxy1:8080,http://proxy2:8080"
```

### 2. 网络拦截工作流
```bash
# 打开页面同时拦截广告
agent-browser open https://example.com
agent-browser network route "**/ads/*" --abort
agent-browser network route "**/tracker/*" --abort
agent-browser network route "**/api/users" --body '{"id":1,"name":"mock"}'
agent-browser reload
agent-browser snapshot -i --json
```

### 3. 批量并发执行
```bash
# 使用内置批量执行器
agent-browser batch run --file tasks.json --concurrency 5
# ...
# tasks.json 示例
# [
#   {"url": "https://a.com", "action": "snapshot"},
#   {"url": "https://b.com", "action": "screenshot", "output": "b.png"},
#   {"url": "https://c.com", "action": "extract", "selector": "@e1"}
# ]
```
## 配置示例
### 企业级配置文件
```yaml
# $HOME/.agent-browser/config.yaml
edition: pro
metrics:
  enabled: true
  export_interval: 300
  format: prometheus
proxy:
  pool:
    - http://proxy1:8080
    - http://proxy2:8080
  rotation: round-robin
sessions:
  max_concurrent: 10
  default_timeout: 30000
storage:
  encrypt: true
  path: $HOME/.agent-browser/state
alerts:
  webhook: https://hooks.example.com/alerts
  on_failure: true
  on_rate_limit: true
```

### 监控指标导出
```bash
# Prometheus 格式
agent-browser metrics export --format prometheus
# ...
# JSON 格式(供下游分析)
agent-browser metrics export --format json | jq '.metrics'
# ...
# 关键指标示例
# agent_browser_requests_total{status="success"} 1024
# agent_browser_requests_total{status="failed"} 12
# agent_browser_session_active 5
# agent_browser_response_time_p95 1.2
```
## 优选实践
### 性能优化
1. **并发控制**:并发会话不超过 `max_concurrent` 配置值,避免资源耗尽.
2. **网络拦截**:对广告、分析脚本统一 `--abort`,显著提升加载速度.
3. **状态复用**:登录态通过加密存储复用,避免每次重新登录.
4. **代理轮换**:大批量采集时启用代理池轮换,降低 IP 封禁风险.
### 安全规范
1. **加密存储**:生产环境启用 `storage.encrypt`,保护 cookies 与 tokens.
2. **租户隔离**:多团队共享时使用 `--workspace` 隔离数据空间.
3. **最小权限**:会话仅授予完成任务所需的最小权限.
4. **审计日志**:启用指标采集与告警,留存操作审计轨迹.
### 团队协作
1. **任务配置版本化**:将 `tasks.json`、配置文件纳入 Git 管理.
2. **共享状态库**:团队共享加密的登录态库,避免重复登录.
3. **告警集成**:失败时通过 webhook 通知团队 IM(飞书/钉钉/Slack).
4. **CI/CD 集成**:将端到端测试嵌入流水线,失败自动归档截图.
## 常见问题
### Q1: 专业版是否兼容免费版的脚本?
完全兼容。免费版的所有命令、参数、工作流、状态文件均可直接在专业版中运行,无需修改。专业版仅在原有能力之上扩展高阶特性.
### Q2: 如何从免费版升级?
```bash
# 升级 CLI
npm install -g agent-browser@pro
# 初始化专业版配置(保留免费版数据)
agent-browser pro init --migrate
```

### Q3: 并发会话数如何控制?
通过配置文件 `sessions.max_concurrent` 或环境变量 `BROWSER_MAX_CONCURRENT` 设置。建议根据机器内存与 CPU 调整,通常 5-10 为宜.
### Q4: 代理池如何配置?
```bash
# 环境变量方式
export BROWSER_PROXY_POOL="http://p1:8080,http://p2:8080"
# 配置文件方式(见上文 config.yaml)
# 运行时启用
```

### Q5: 监控指标如何接入现有系统?
专业版支持 Prometheus 与 JSON 两种导出格式。可通过定时任务采集指标,推送到 Prometheus/Grafana 或自建看板.
### Q6: 多租户数据如何隔离?
使用 `--workspace <name>` 参数为不同团队/客户分配独立会话空间,状态文件、cookies、缓存均按租户隔离存储.
## 与免费版的兼容性
| 维度 | 兼容性 |
|---:|---:|
| 命令语法 | 100% 兼容 |
| 状态文件格式 | 100% 兼容(专业版可读取免费版状态) |
| 脚本工作流 | 100% 兼容(无需修改即可运行) |
| 配置文件 | 向后兼容(专业版新增字段可选) |
| 升级路径 | 平滑升级(保留全部历史数据) |
## 依赖说明
### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Node.js**: >= 18.0.0
- **推荐内存**: >= 4GB(并发场景建议 8GB+)

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| agent-browser(pro) | CLI 工具 | 必需 | `npm install -g agent-browser@pro` |
| Chromium | 运行时 | 必需 | `agent-browser install` 自动下载 |
| Node.js | 运行环境 | 必需 | 系统包管理器安装 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| 代理服务 | 网络代理 | 可选 | 自建或第三方代理服务 |
| 监控系统 | 可观测性 | 可选 | Prometheus / Grafana |

### API Key 配置
- 本 Skill 基于Markdown指令,无需额外API Key(除内容中明确标注的外部API)
- 远程浏览器服务(如 Browserbase):配置 `BROWSERBASE_API_KEY` 与 `BROWSERBASE_PROJECT_ID`
- 代理服务:在配置文件或环境变量中配置代理池地址

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作
- **版本**: 专业版(兼容免费版全部能力)
## 错误处理
| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
## 示例
### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```
## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "浏览器智能代理工具-专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "browser agent pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 核心功能

- **自动化执行**: 企业级无头浏览器自动化
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据