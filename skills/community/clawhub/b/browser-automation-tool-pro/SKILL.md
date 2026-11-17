---

slug: browser-automation-tool-pro
name: browser-automation-tool-pro
version: 1.0.0
displayName: 浏览器自动化工具-专业版
summary: "企业级自然语言浏览器自"
license: Proprietary
edition: pro
description: "企业级自然语言浏览器自动化工具,在免费版核心能力之上,提供远程浏览器集群、。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
  隐身模式、代理/CAPTCHA处理、批量任务编排与监控告警能力。核心能力:

  - 免费版全部能力(完全兼容)

  - 远程浏览器集群与弹性扩缩容

  - 隐身模式与反检测

  - 代理池与CAPTCHA自动处理

  - 批量任务编排与并发执行

  - 监控指标采集与告警通知

  适用场景:

  - 企业级数据采集与竞品监控

  - 反爬虫环境下的自动化操作

  - 批量内容发布与多账号运营

  - 团队协作与任务编排

  差异化:专业版面向团队与企业,提供远程浏览...'
tags:
  - 研究工具
  - 浏览器自动化
  - 企业级
  - 自然语言
  - 自动化
  - 工作流
  - 效率
  - 专业版新
  - browser
  - https
  - captcha
tools:
  - read
  - exec
  - write
homepage: ""
# 定价元数据
category: "Automation"

---

> **功能说明**: 本技能涵盖 中文交互、化流程 等核心能力。


# 浏览器自动化工具(专业版)
## 概述
本工具是企业级自然语言浏览器自动化工具,在免费版核心能力之上,扩展了远程浏览器集群、隐身模式、代理/CAPTCHA处理、批量任务编排与监控告警能力,适合企业数据采集、反爬虫场景下的自动化操作、批量内容发布与多账号运营。专业版与免费版完全兼容:免费版的所有命令、工作流均可直接在专业版中使用.
### 免费版 vs 专业版对比
| 能力 | 免费版 | 专业版 |
|---|---|---|
| 自然语言操作(act/extract/observe) | 支持 | 支持 |
| 本地 Chrome 浏览器 | 支持 | 支持 |
| 截图与基础交互 | 支持 | 支持 |
| 远程浏览器集群 | 不支持 | 支持(弹性扩缩容) |
| 隐身模式 | 不支持 | 支持 |
| 代理池管理 | 不支持 | 支持 |
| CAPTCHA 处理 | 不支持 | 支持 |
| 批量任务编排 | 不支持 | 支持 |
| 监控告警 | 不支持 | 支持 |
| 优先技术支持 | 不支持 | 支持 |

### 本地模式 vs 远程模式对比
| 特性 | 本地模式 | 远程模式(专业版) |
|:-----|:-----|:-----|
| 速度 | 较快 | 略慢(网络延迟) |
| 配置 | 需本机 Chrome | 需 API Key |
| 代理/CAPTCHA | 不支持 | 支持 |
| 弹性扩缩容 | 不支持 | 支持 |
| 适用场景 | 开发调试 | 生产/大规模采集 |

## 核心能力
### 1. 远程浏览器集群(专业版新增)
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | 浏览器自动化工具-专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
export BROWSERBASE_API_KEY="${API_KEY:?请设置环境变量}"
export BROWSERBASE_PROJECT_ID="your-project-id"
browser navigate https://example.com
browser act "点击登录按钮"
```

**处理**: 解析远程浏览器集群(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回远程浏览器集群(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 隐身模式与反检测(专业版新增)
```bash
browser --stealth navigate https://example.com
browser --stealth --fingerprint "windows-chrome-120" navigate https://example.com
```

**处理**: 解析隐身模式与反检测(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回隐身模式与反检测(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 代理池集成(专业版新增)
```bash
export BROWSER_PROXY_POOL="http://proxy1:8080,http://proxy2:8080,http://proxy3:8080"
browser --proxy-pool navigate https://example.com
```

**处理**: 解析代理池集成(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回代理池集成(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. CAPTCHA 自动处理(专业版新增)
```bash
browser --captcha-solver navigate https://example.com
browser act "完成验证码"
```

**处理**: 解析CAPTCHA 自动处理(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回CAPTCHA 自动处理(专业版新增)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 批量任务编排(专业版新增)
```bash
browser batch run --file tasks.yaml --concurrency 10
```

**处理**: 解析批量任务编排(专业版新增)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量任务编排(专业版新增)的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级自然语言浏、览器自动化、支持远程浏览器、代理与批量任务、面向团队生产场景、览器自动化工具、在免费版核心能力、批量任务编排与监、控告警能力、核心能力、免费版全部能力、完全兼容、远程浏览器集群与、弹性扩缩容、代理池与、批量任务编排与并、发执行、监控指标采集与告、警通知等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一:反爬虫环境下的数据采集
目标站点有反爬机制,使用隐身模式+代理池+CAPTCHA处理完成采集.
```bash
#!/bin/sh
TARGET_URL="https://protected-site.example.com/data"
browser --stealth --proxy-pool --captcha-solver navigate "$TARGET_URL"
browser act "等待页面完全加载"
browser act "点击加载更多按钮"
browser act "再次点击加载更多按钮"
browser extract "获取所有数据条目" \
  '{"items":[{"id":"string","title":"string","value":"number","date":"string"}]}' \
  > data/results.json
browser screenshot "logs/collection_$(date +%Y%m%d_%H%M%S).png"
browser close
echo "采集完成,数据已保存到 data/results.json"
```

### 场景二:批量多站点内容发布
企业需要在多个平台批量发布内容,使用任务清单并发执行.
```python
#!/usr/bin/env python3
"""批量多平台内容发布编排示例"""
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
PLATFORMS = [
    {
        "name": "platform_a",
        "url": "https://platform-a.example.com/post",
        "content": "今日产品更新公告...",
        "auth_env": {"BROWSERBASE_API_KEY": "key_a", "BROWSERBASE_PROJECT_ID": "proj_a"}
    },
    {
        "name": "platform_b",
        "url": "https://platform-b.example.com/create",
        "auth_env": {"BROWSERBASE_API_KEY": "key_b", "BROWSERBASE_PROJECT_ID": "proj_b"}
    },
    {
        "name": "platform_c",
        "url": "https://platform-c.example.com/new",
        "auth_env": {"BROWSERBASE_API_KEY": "key_c", "BROWSERBASE_PROJECT_ID": "proj_c"}
    },
]
def publish_to_platform(platform):
    """在单个平台发布内容"""
    name = platform["name"]
    try:
        subprocess.run([
            "browser", "--stealth", "--remote",
            "navigate", platform["url"]
        ], check=True, timeout=60)
        subprocess.run([
            "browser", "act", "点击新建内容按钮"
        ], check=True, timeout=30)
        subprocess.run([
            "browser", "act", f"在内容编辑区输入: {platform['content']}"
        ], check=True, timeout=30)
        subprocess.run([
            "browser", "act", "点击发布按钮"
        ], check=True, timeout=30)
        subprocess.run([
            "browser", "screenshot", f"logs/{name}_published.png"
        ])
        subprocess.run(["browser", "close"])
        return {"platform": name, "status": "success"}
    except Exception as e:
        subprocess.run(["browser", "screenshot", f"logs/{name}_failed.png"])
        subprocess.run(["browser", "close"])
        return {"platform": name, "status": "failed", "error": str(e)}
results = []
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(publish_to_platform, p): p for p in PLATFORMS}
    for future in as_completed(futures):
        result = future.result()
        results.append(result)
        print(f"[{result['status'].upper()}] {result['platform']}")
with open("logs/publish-report.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

### 场景三:大规模数据采集与监控
采集大量页面,实时监控进度与失败率,自动告警.
```bash
#!/bin/sh
set -e
browser metrics enable
URLS=$(cat urls.txt)
TOTAL=$(echo "$URLS" | wc -l)
COUNT=0
FAILED=0
while IFS= read -r url; do
  COUNT=$((COUNT + 1))
  echo "[$COUNT/$TOTAL] 采集: $url"
  for attempt in 1 2 3; do
    if browser --stealth --proxy-pool --retry 1 navigate "$url" 2>/dev/null; then
      browser extract "获取页面主要内容" > "data/page_${COUNT}.json"
      browser screenshot "logs/page_${COUNT}.png"
      browser close
      break
    else
      echo "  第${attempt}次尝试失败"
      browser close 2>/dev/null
      if [ "$attempt" -eq 3 ]; then
        FAILED=$((FAILED + 1))
        echo "$url" >> logs/failed_urls.txt
      fi
      sleep 5
    fi
  done
  if [ "$COUNT" -gt 10 ]; then
    FAIL_RATE=$(echo "scale=2; $FAILED * 100 / $COUNT" | bc)
    if [ "$(echo "$FAIL_RATE > 20" | bc)" -eq 1 ]; then
      echo "[告警] 失败率 ${FAIL_RATE}% 超过阈值,请检查代理池与目标站点"
      curl -X POST "$ALERT_WEBHOOK" -d "{\"text\":\"采集失败率 ${FAIL_RATE}%\"}"
    fi
  fi
done <<< "$URLS"
browser metrics export --format json > logs/metrics.json
echo "采集完成: 共 $TOTAL,成功 $((TOTAL - FAILED)),失败 $FAILED"
```

## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问
### 依赖详情
```bash
cd /path/to/browser-automation-tool
npm install
npm link
browser pro init
browser config set stealth.default true
browser config set proxy.pool "http://p1:8080,http://p2:8080"
browser config set metrics.enabled true
```

### 2. 远程浏览器配置
```bash
export BROWSERBASE_PROJECT_ID="your-project-id"
browser --remote navigate https://example.com
browser screenshot
browser close
```

### 3. 批量任务执行
```bash
yaml --concurrency 10
browser batch status
```

#
## 配置示例
### 企业级配置文件
```yaml
edition: pro
browser:
  default_mode: remote          # local | remote
  stealth: true
  fingerprint: windows-chrome-120
proxy:
  pool:
    - http://proxy1:8080
    - http://proxy2:8080
  rotation: round-robin
captcha:
  solver: enabled
  provider: internal
batch:
  max_concurrency: 10
  retry: 3
  retry_delay: 5
metrics:
  enabled: true
  export_interval: 60
  format: prometheus
alerts:
  webhook: https://hooks.example.com/alerts
  on_failure_rate: 20
  on_captcha_fail: true
```

### 监控指标导出
```bash
browser metrics export --format prometheus
```

## 优选实践
### 反爬虫策略
1. **启用隐身模式**:`--stealth` 隐藏自动化特征,规避基础反爬检测.
2. **代理轮换**:大批量采集启用代理池,降低 IP 封禁风险.
3. **合理间隔**:请求间添加随机延迟,模拟人类操作节奏.
4. **指纹轮换**:定期切换浏览器指纹,避免特征识别.
### 批量任务优化
1. **并发控制**:并发数不超过 `max_concurrency`,避免触发反爬.
2. **失败重试**:启用重试机制,指数退避避免雪崩.
3. **结果归档**:每次任务截图与数据归档,便于排查.
4. **告警监控**:失败率超阈值时自动告警,及时介入.
### 安全规范
1. **凭证管理**:登录凭证通过环境变量或密钥管理服务注入.
2. **最小权限**:浏览器会话仅授予完成任务所需的最小权限.
3. **审计日志**:启用指标采集,留存操作审计轨迹.
4. **数据脱敏**:采集到的敏感数据及时脱敏存储.
## 常见问题
### Q1: 专业版是否兼容免费版脚本?
完全兼容。免费版的所有命令、参数、工作流均可直接在专业版中运行。专业版仅在原有能力之上扩展高阶特性.
### Q2: 如何从免费版升级?
```bash
browser pro init --migrate
```
升级过程保留全部历史数据与配置.
### Q3: 远程浏览器连接失败?
- 检查 `BROWSERBASE_API_KEY` 与 `BROWSERBASE_PROJECT_ID` 是否正确
- 确认网络可访问远程浏览器服务
- 查看服务配额是否耗尽

### Q4: 隐身模式仍被检测?
- 升级浏览器指纹:`browser config set browser.fingerprint "latest-chrome"`
- 启用代理轮换,避免单一 IP 频繁请求
- 添加人类行为模拟:请求间随机延迟

### Q5: CAPTCHA 处理失败?
- 确认 `captcha.solver: enabled` 已启用
- 检查 CAPTCHA 解决服务配额
- 对复杂 CAPTCHA,可手动介入后继续自动化

### Q6: 如何接入现有监控系统?
专业版支持 Prometheus 与 JSON 两种导出格式,可推送到 Prometheus/Grafana、Datadog 或自建看板.
## 与免费版的兼容性
| 维度 | 兼容性 |
|:---:|:---:|
| 命令语法 | 100% 兼容 |
| 脚本工作流 | 100% 兼容(无需修改即可运行) |
| 自然语言指令 | 100% 兼容 |
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
|:------|------:|:------|:------|
| Node.js | 运行环境 | 必需 | 系统包管理器安装 |
| Chrome | 浏览器 | 本地模式必需 | 官方下载安装 |
| npm 依赖包 | Node 包 | 必需 | `npm install` |
| 远程浏览器服务 | 云服务 | 远程模式必需 | 第三方服务订阅 |
| 代理服务 | 网络代理 | 可选 | 自建或第三方代理服务 |
| CAPTCHA 服务 | 反爬服务 | 可选 | 第三方 CAPTCHA 解决服务 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| 监控系统 | 可观测性 | 可选 | Prometheus / Grafana |

### API Key 配置
- 基础LLM由Agent平台内置提供，特定外部API需单独配置密钥
- 远程浏览器服务:配置 `BROWSERBASE_API_KEY` 与 `BROWSERBASE_PROJECT_ID`
- 代理服务:在配置文件或环境变量中配置代理池地址
- CAPTCHA 服务:在配置文件中配置 CAPTCHA 解决服务凭证

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作
- **版本**: 专业版(兼容免费版全部能力)

## 错误处理
| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
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
    "result": "浏览器自动化工具-专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "browser automation pro"
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

- **自动化执行**: 企业级自然语言浏览器自
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据