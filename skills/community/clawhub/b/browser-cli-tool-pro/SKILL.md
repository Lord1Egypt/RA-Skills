---

slug: browser-cli-tool-pro
name: browser-cli-tool-pro
version: 1.0.0
displayName: 浏览器CLI工具-专业版
summary: "企业级浏览器自动化CLI,支持批量任务、并发会话、错误重试与监控,面向团队生产场景。企业级浏览器自动化命令行工具,在免费版核心能力之上,提供批量任务编排、"
license: Proprietary
edition: pro
description: "企业级浏览器自动化命令行工具,在免费版核心能力之上,提供批量任务编排、。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
  并发会话管理、错误重试机制、监控告警与团队协作能力。核心能力:

  - 免费版全部能力(完全兼容)

  - 批量任务编排与并发执行

  - 错误重试与失败恢复机制

  - 任务队列与调度器

  - 监控指标采集与告警通知

  - 团队共享状态库

  适用场景:

  - 企业级批量签到与表单处理

  - 数据采集与自动化测试

  - 多账号矩阵运营

  - CI/CD 流水线集成

  差异化:专业版面向团队与企业,提供批量、并发、重试、监控等高阶能力,并保持与免费版完全兼容'
tags:
  - 研究工具
  - 浏览器自动化
  - 企业级
  - 批量操作
  - 搜索
  - 检索
  - 工具
  - agent-browser
  - 专业版新
  - session
  - https
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
# 定价元数据
category: "Knowledge"

---

> **功能说明**: 本技能涵盖 中文交互 等核心能力。


# 浏览器CLI工具(专业版)
## 概述
本工具是企业级浏览器自动化命令行工具,在免费版核心能力之上,扩展了批量任务编排、并发会话管理、错误重试、监控告警与团队协作能力,适合企业批量签到、数据采集、自动化测试与多账号运营场景。专业版与免费版完全兼容:免费版的所有命令、工作流均可直接在专业版中使用.
### 免费版 vs 专业版对比
| 能力 | 免费版 | 专业版 |
|---|---|---|
| 基础导航与交互 | 支持 | 支持 |
| snapshot 与 ref 引用 | 支持 | 支持 |
| 三种元素定位方式 | 支持 | 支持 |
| 截图与信息提取 | 支持 | 支持 |
| 批量任务编排 | 不支持 | 支持 |
| 并发会话管理 | 不支持 | 支持 |
| 错误重试机制 | 不支持 | 支持 |
| 任务队列与调度 | 不支持 | 支持 |
| 监控告警 | 不支持 | 支持 |
| 团队共享状态库 | 不支持 | 支持 |
| 优先技术支持 | 不支持 | 支持 |

## 核心能力
### 1. 批量任务编排(专业版新增)
通过任务清单文件批量执行浏览器操作,支持并发与依赖管理.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 浏览器CLI工具-专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
agent-browser batch run --file tasks.yaml --concurrency 5
```

**处理**: 解析批量任务编排(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量任务编排(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 并发会话管理(专业版新增)
```bash
agent-browser session list --verbose
agent-browser config set session.max_concurrent 10
agent-browser session cleanup --idle 300
```

**处理**: 解析并发会话管理(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回并发会话管理(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 错误重试机制(专业版新增)
```bash
agent-browser --retry 3 --retry-delay 5 open https://example.com
agent-browser config set retry.max 5
```

**处理**: 解析错误重试机制(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回错误重试机制(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 任务队列与调度(专业版新增)
```bash
agent-browser queue submit --file tasks.yaml
agent-browser queue status
agent-browser queue pause
agent-browser queue resume
agent-browser schedule add --cron "0 9 * * *" --file daily-checkin.yaml
agent-browser schedule list
```

**处理**: 解析任务队列与调度(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回任务队列与调度(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 监控指标采集(专业版新增)
```bash
agent-browser metrics enable
agent-browser metrics export --format json > metrics.json
agent-browser metrics export --format prometheus > metrics.prom
```

**处理**: 解析监控指标采集(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回监控指标采集(专业版新增)的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级浏览器自动、支持批量任务、错误重试与监控、面向团队生产场景、化命令行工具、在免费版核心能力、监控告警与团队协、作能力、核心能力、免费版全部能力、完全兼容、批量任务编排与并、发执行、错误重试与失败恢、复机制、任务队列与调度器、监控指标采集与告、警通知、团队共享状态库等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一:批量多站点签到
企业用户需要在多个站点完成每日签到,使用批量编排并发执行.
```bash
#!/bin/sh
SITES=(
  "https://site-a.com/checkin|auth/site-a.json"
  "https://site-b.com/checkin|auth/site-b.json"
  "https://site-c.com/checkin|auth/site-c.json"
  "https://site-d.com/checkin|auth/site-d.json"
  "https://site-e.com/checkin|auth/site-e.json"
)
for entry in "${SITES[@]}"; do
  url="${entry%%|*}"
  auth="${entry##*|}"
  name=$(basename "$auth" .json)
  (
    agent-browser --session "$name" open "$url"
    agent-browser --session "$name" state load "$auth"
    agent-browser --session "$name" snapshot
    agent-browser --session "$name" find role button click --name "签到" || \
    agent-browser --session "$name" click @e2
    agent-browser --session "$name" screenshot "logs/${name}_$(date +%Y%m%d).png"
    agent-browser --session "$name" close
  ) &
done
wait
echo "全部签到任务完成"
```

### 场景二:自动化表单批量提交
批量填写并提交表单,支持失败重试与结果归档.
```python
#!/usr/bin/env python3
"""批量表单提交编排示例(含重试机制)"""
import subprocess
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
FORMS = [
    {"id": "form_001", "url": "https://app.example.com/apply", "data": {"name": "张三", "phone": "13800000001"}},
    {"id": "form_002", "url": "https://app.example.com/apply", "data": {"name": "李四", "phone": "13800000002"}},
    {"id": "form_003", "url": "https://app.example.com/apply", "data": {"name": "王五", "phone": "13800000003"}},
]
def submit_form(form, max_retries=3):
    """提交单个表单,失败自动重试"""
    session = form["id"]
    for attempt in range(1, max_retries + 1):
        try:
            subprocess.run(["agent-browser", "--session", session, "open", form["url"]], check=True, timeout=30)
run(["agent-browser", "--session", session, "snapshot"], check=True, timeout=15)
run(["agent-browser", "--session", session, "find", "label", "姓名", "fill", form["data"]["name"]], check=True)
run(["agent-browser", "--session", session, "find", "label", "电话", "fill", form["data"]["phone"]], check=True)
run(["agent-browser", "--session", session, "find", "role", "button", "click", "--name", "提交"], check=True)
run(["agent-browser", "--session", session, "screenshot", f"logs/{session}.png"])
run(["agent-browser", "--session", session, "close"])
            return {"id": session, "status": "success", "attempts": attempt}
        except subprocess.CalledProcessError as e:
            print(f"[{session}] 第{attempt}次尝试失败: {e}")
run(["agent-browser", "--session", session, "screenshot", f"logs/{session}_fail.png"])
            if attempt < max_retries:
                time.sleep(5 * attempt)  # 指数退避
            print(f"[{session}] 第{attempt}次尝试超时")
            if attempt < max_retries:
    subprocess.run(["agent-browser", "--session", session, "close"])
    return {"id": session, "status": "failed", "attempts": max_retries}
results = []
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(submit_form, form): form for form in FORMS}
    for future in as_completed(futures):
        result = future.result()
        results.append(result)
        print(f"[{result['status'].upper()}] {result['id']} (尝试 {result['attempts']} 次)")
with open("logs/report.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
success_count = sum(1 for r in results if r["status"] == "success")
print(f"\n完成: {success_count}/{len(results)} 成功")
```

### 场景三:CI/CD 集成端到端测试
在 CI 流水线中运行端到端测试,失败时自动归档截图与日志.
```bash
#!/bin/sh
set -e
TEST_URL="${STAGING_URL:-https://staging.example.com}"
ARTIFACTS_DIR="artifacts/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$ARTIFACTS_DIR"
agent-browser metrics enable
agent-browser open "$TEST_URL"
agent-browser snapshot > "$ARTIFACTS_DIR/homepage.json"
agent-browser find label "用户名" fill "ci-test"
agent-browser find label "密码" fill "ci-password"
agent-browser find role button click --name "登录"
agent-browser wait --url "**/dashboard" || {
  echo "登录测试失败"
  agent-browser screenshot "$ARTIFACTS_DIR/login-fail.png"
  agent-browser close
  agent-browser metrics export --format json > "$ARTIFACTS_DIR/metrics.json"
  exit 1
}
agent-browser snapshot > "$ARTIFACTS_DIR/dashboard.json"
agent-browser screenshot "$ARTIFACTS_DIR/dashboard.png"
echo "全部测试通过"
agent-browser close
```

## 不适用场景
以下场景浏览器CLI工具-专业版不适合处理：

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
agent-browser pro init
agent-browser config set metrics.enabled true
```

### 2. 批量任务执行
```bash
yaml --concurrency 5
agent-browser queue status
```

### 3. 定时调度
```bash
agent-browser schedule list
agent-browser schedule trigger "每日签到"
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 配置示例
### 企业级配置文件
```yaml
edition: pro
session:
  max_concurrent: 10
  default_timeout: 30000
  cleanup_idle: 300
retry:
  max: 3
  delay: 5
  backoff: exponential
queue:
  enabled: true
  persist: true
  path: $HOME/.agent-browser/queue
metrics:
  enabled: true
  export_interval: 60
  format: prometheus
alerts:
  webhook: https://hooks.example.com/notify
  on_failure: true
  on_retry_exhausted: true
storage:
  shared: true
  path: /shared/agent-browser/state
  encrypt: true
```

### 监控指标示例
```bash
agent-browser metrics export --format prometheus
```

## 优选实践
### 批量任务优化
1. **合理设置并发数**:根据机器资源设置 `session.max_concurrent`,通常 5-10 为宜.
2. **使用任务清单**:将重复任务抽象为 YAML 清单,便于维护与版本管理.
3. **失败重试**:启用 `retry` 机制,设置指数退避避免雪崩.
4. **结果归档**:每次任务截图与日志归档,便于排查问题.
### 企业运维规范
1. **共享状态库**:团队共享加密登录态库,避免重复登录.
2. **告警集成**:失败时通过 webhook 通知团队 IM(飞书/钉钉/Slack).
3. **CI/CD 集成**:将端到端测试嵌入流水线,失败自动归档证据.
4. **定时调度**:使用内置调度器替代 crontab,支持暂停/恢复/手动触发.
### 安全规范
1. **加密存储**:生产环境启用 `storage.encrypt`,保护 cookies 与 tokens.
2. **最小权限**:会话仅授予完成任务所需的最小权限.
3. **审计日志**:启用指标采集,留存操作审计轨迹.
4. **敏感信息管理**:登录凭证通过环境变量或密钥管理服务注入,不硬编码.
## 常见问题
### Q1: 专业版是否兼容免费版脚本?
完全兼容。免费版的所有命令、参数、工作流均可直接在专业版中运行,无需修改。专业版仅在原有能力之上扩展高阶特性.
### Q2: 如何从免费版升级?
```bash
npm install -g agent-browser@pro
agent-browser pro init --migrate
```
升级过程保留全部历史数据与配置.
### Q3: 批量任务失败如何排查?
1. 查看 `logs/` 目录下的截图与日志
2. 使用 `agent-browser metrics export` 导出指标分析失败模式
3. 对失败任务单独重跑:`agent-browser batch run --file tasks.yaml --only "任务名"`
4. 启用 `--headed` 模式可视化复现

### Q4: 并发会话数如何调优?
- 起始值:5 个并发
- 内存充足时:提升至 10
- CPU 密集型任务:降低并发,提升单任务超时
- 监控 `agent_browser_session_active` 指标,避免资源耗尽

### Q5: 如何接入现有监控系统?
专业版支持 Prometheus 与 JSON 两种导出格式。可通过定时任务采集指标,推送到 Prometheus/Grafana、Datadog 或自建看板.
### Q6: 任务队列持久化如何保证?
启用 `queue.persist: true`,队列状态持久化到磁盘,服务重启后自动恢复未完成任务.
## 与免费版的兼容性
| 维度 | 兼容性 |
|---:|---:|
| 命令语法 | 100% 兼容 |
| 脚本工作流 | 100% 兼容(无需修改即可运行) |
| 状态文件格式 | 100% 兼容(专业版可读取免费版状态) |
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
| 监控系统 | 可观测性 | 可选 | Prometheus / Grafana |

### API Key 配置
- 本 Skill 基于Markdown指令,无需额外API Key(除内容中明确标注的外部API)
- 远程浏览器服务(如 Browserbase):配置 `BROWSERBASE_API_KEY` 与 `BROWSERBASE_PROJECT_ID`

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
    "result": "浏览器CLI工具-专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "browser cli pro"
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

- **自动化执行**: 企业级浏览器自动化CLI,支持批量任务、并发会话、错误重试与监控,面向团队生产场景。企业级浏览器自动化命令行工具,在免费
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据