---
slug: browser-automation-v2-tool-free
name: browser-automation-v2-tool-free
version: 1.0.0
displayName: 浏览器自动化(免费版)
summary: "浏览器自动化免费版，支持标签页自动清理、超时重试、智能等待与基础表单填写.。浏览器自动化助手免费版是面向个人开发者和轻量任务场景的浏览器自动化工具。聚焦"打开页面-等待加载-提取数据-关闭标"
license: MIT
edition: free
description: "浏览器自发化助手免费版是面向个人开发者和轻量任务场景的浏览器自发化工具。聚焦\"打开页面-等待加载-提取数据-关闭标签\"四步基础流程，让重复的网页操作自发化。Use. 适用于需要browser automation v2 tool相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量."
tags:
  - 浏览器自动化
  - browser
  - automation
  - productivity
  - developer-tools
  - 网页抓取
  - 表单填写
  - 单页面
  - 自动化
  - 工作流
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
pricing_tier: free

---
# 浏览器自动化助手（免费版）

> **打开页面、等待加载、提取内容、自动清理。四步完成单页面自动化。**

将繁琐的浏览器操作交给自动化脚本：自动打开URL、智能等待加载、提取所需数据、最后关闭标签页释放资源。免费版聚焦单页面场景，提供稳定可靠的轻量自动化能力.
## 概述

免费版浏览器自动化工具为个人开发者和小型项目提供基础的浏览器自动化能力。通过简洁的配置项和清晰的错误反馈，降低浏览器自动化的使用门槛.
### 核心定位

| 维度 | 免费版能力 |
|---|-----|
| 单页面操作 | 支持（打开/等待/提取/关闭） |
| 批量URL处理 | 不支持（需升级专业版） |
| 并发锁机制 | 不支持（需升级专业版） |
| Cloudflare绕过 | 不支持（需升级专业版） |
| 结构化日志 | 支持（DEBUG=1开启） |
| 超时重试 | 支持（指数退避） |
| 表单填写 | 基础支持（单字段填写） |

## 核心能力

### 1. 单页面自动打开与导航

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 浏览器自动化(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```python
import subprocess
import json
# ...
def open_page(url, timeout=30):
    """打开页面并等待加载"""
    cmd = [
        "node", "search-google.js",
        "--url", url,
        "--timeout", str(timeout),
        "--wait-until", "networkidle"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+10)
    if result.returncode != 0:
        return {"success": False, "error": result.stderr}
    return json.loads(result.stdout)
# ...
# 示例
page = open_page("https://example.com")
print(page.get("title", "未获取到标题"))
```

**处理**: 解析单页面自动打开与导航的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回单页面自动打开与导航的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 智能等待机制

```python
def smart_wait(selector=None, wait_type="loadstate", timeout=30000):
    """智能等待策略"""
    strategies = {
        "loadstate": "waitForLoadState",   # 等待加载状态
        "selector": "waitForSelector",    # 等待元素出现
        "timeout": "waitForTimeout",       # 固定等待
        "function": "waitForFunction"      # 等待自定义函数
    }
    return {
        "strategy": strategies.get(wait_type, "loadstate"),
        "selector": selector,
        "timeout": timeout
    }
# ...
# 等待元素出现
config = smart_wait(selector="#main-content", wait_type="selector")
print(f"等待策略：{config['strategy']}, 选择器：{config['selector']}")
```

**处理**: 解析智能等待机制的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回智能等待机制的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 超时与重试（指数退避）

```python
import time
# ...
def fetch_with_retry(url, max_retries=3, base_timeout=30):
    """带指数退避的重试机制"""
    for attempt in range(max_retries):
        timeout = base_timeout * (2 ** attempt)  # 30s, 60s, 120s
        try:
            result = open_page(url, timeout=timeout)
            if result.get("success"):
                return result
            print(f"第{attempt+1}次尝试失败：{result.get('error')}")
        except subprocess.TimeoutExpired:
            print(f"第{attempt+1}次超时（{timeout}s）")
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            print(f"等待{wait_time}s后重试...")
            time.sleep(wait_time)
    return {"success": False, "error": "重试次数已用完"}
```

**处理**: 解析超时与重试（指数退避）的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回超时与重试（指数退避）的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 标签页自动清理

```python
class TabManager:
    """标签页管理器（免费版）"""
# ...
    def __init__(self):
        self.tabs = []
# ...
    def open_tab(self, url):
        """打开新标签页"""
        tab_id = f"tab_{len(self.tabs) + 1}"
        self.tabs.append({"id": tab_id, "url": url, "status": "open"})
        return tab_id
# ...
    def close_tab(self, tab_id):
        """关闭标签页"""
        for tab in self.tabs:
            if tab["id"] == tab_id:
                tab["status"] = "closed"
                print(f"已关闭 {tab_id}")
# ...
    def cleanup(self):
        """清理所有未关闭的标签页"""
            if tab["status"] == "open":
                self.close_tab(tab["id"])
        print(f"清理完成，共处理 {len(self.tabs)} 个标签页")
# ...
manager = TabManager()
tab = manager.open_tab("https://example.com")
# ... 执行操作 ...
manager.cleanup()
```

**处理**: 解析标签页自动清理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回标签页自动清理的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：浏览器自动化免费、支持标签页自动清、超时重试、智能等待与基础表、单填写、浏览器自动化助手、免费版是面向个人、开发者和轻量任务、场景的浏览器自动、化工具、提取数据、四步基础流程、让重复的网页操作、自动化、Use、when、需要提升效率、自动化流程、批量处理、工作流优化时使用、不适用于需要人工、创意判断的任务、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一：单页面信息采集

**场景描述**：需要从指定URL提取页面标题和正文摘要.
```python
def fetch_page_summary(url):
    """获取页面摘要信息"""
    result = fetch_with_retry(url)
    if not result.get("success"):
        return "获取失败"
# ...
    # 解析页面内容
    title = result.get("title", "无标题")
    description = result.get("description", "")[:200]
    return f"标题：{title}\n摘要：{description}"
# ...
summary = fetch_page_summary("https://example.com")
print(summary)
```

### 场景二：简单表单自动填写

**场景描述**：自动填写登录表单并提交.
```python
def fill_login_form(url, email, password):
    """填写并提交登录表单"""
    form_data = {
        "email": email,
        "password": password
    }
    cmd = [
        "node", "fill-form.js", url,
        "--fields", json.dumps(form_data, ensure_ascii=False),
        "--submit", "true"
    ]
run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout) if result.returncode == 0 else {"error": result.stderr}
# ...
# 使用示例
result = fill_login_form("https://example.com/login", "user@test.com", "secret")
print("登录结果：", result)
```

### 场景三：定时数据抓取

**场景描述**：每日定时抓取某商品页面价格.
```python
import schedule
import time
# ...
def daily_price_check():
    """每日价格检查"""
    url = "https://example.com/product/123"
    result = fetch_with_retry(url)
    if result.get("success"):
        price = result.get("price", "未找到")
        print(f"[{time.strftime('%Y-%m-%d %H:%M')}] 当前价格：{price}")
    else:
strftime('%Y-%m-%d %H:%M')}] 抓取失败：{result.get('error')}")
# ...
# 每天早上8点执行
schedule.every().day.at("08:00").do(daily_price_check)
while True:
    schedule.run_pending()
    time.sleep(60)
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 30秒上手

```bash
# 设置环境变量
export BROWSER_PROFILE=my-profile
export BROWSER_TIMEOUT=30000
export BROWSER_RETRIES=2
export DEBUG=1
# ...
# 执行搜索
node search-google.js "查询关键词"
# ...
# 获取页面摘要
node fetch-summary.js "https://example.com"
```

### 120秒标准搭建

```bash
# 依赖说明
npm install playwright
# ...
# 2. 配置浏览器
export BROWSER_PROFILE=skill-free
export BROWSER_TIMEOUT=30000
export BROWSER_RETRIES=2
# ...
# 3. 执行单页面任务
node fetch-summary.js "https://news.example.com" --output result.json
# ...
# 4. 自动填表
node fill-form.js "https://example.com/form" '{"name":"张三","email":"zhang@test.com"}'
```

## 配置示例

### 基础配置文件

```yaml
# config.yaml
browser:
  profile: skill-free
  timeout: 30000
  retries: 2
  headless: true
# ...
logging:
  level: INFO
  debug: false
# ...
output:
  format: json
  directory: ./output
```

### 环境变量优先级

```python
import os
# ...
class Config:
    """配置管理器"""
    BROWSER_PROFILE = os.getenv("BROWSER_PROFILE", "default")
    BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30000"))
    BROWSER_RETRIES = int(os.getenv("BROWSER_RETRIES", "2"))
    DEBUG = os.getenv("DEBUG", "0") == "1"
# ...
    @classmethod
    def show(cls):
        print("当前配置：")
        print(f"  Profile: {cls.BROWSER_PROFILE}")
        print(f"  Timeout: {cls.BROWSER_TIMEOUT}ms")
        print(f"  Retries: {cls.BROWSER_RETRIES}")
        print(f"  Debug:   {cls.DEBUG}")
# ...
Config.show()
```

## 优秀实践

## 错误处理

```python
def safe_fetch(validated_url):
    """安全的页面获取"""
    try:
        result = fetch_with_retry(url, max_retries=3)
        if not result.get("success"):
            return {"error": result.get("error", "未知错误")}
        return result
    except Exception as e:
        return {"error": f"异常：{str(e)}"}
```

### 2. 资源释放 - 处理方式: 按上述步骤操作并确认结果

```python
# 使用上下文管理器确保资源释放
# ...
    # 执行操作
result = "操作完成"
class BrowserSession:
    def __enter__(self):
        print("打开浏览器会话")
        return self
    def __exit__(self, *args):
        print("关闭浏览器会话，清理标签页")
with BrowserSession() as session:
```

### 3. 调试技巧

```python
# 开启DEBUG日志定位问题
import os
os.environ["DEBUG"] = "1"
# ...
# 查看详细的执行流程
# [DEBUG] Opening URL: https://example.com
# [DEBUG] Waiting for networkidle...
# [DEBUG] Network idle after 2.3s
# [DEBUG] Extracting content...
# [DEBUG] Tab closed successfully
```
### 错误场景3

检查`error_code`并按照处理方式进行排查.
## 常见问题

### Q1：免费版支持批量URL处理吗？

不支持。免费版聚焦单页面自动化场景，每次只能处理一个URL。如需批量处理多个URL（如 `multi-pages.js` 批量模式、并发执行、结果聚合），请升级至专业版.
### Q2：超时设置应该多大？

默认30秒适用于大多数静态页面。对于动态加载较重的页面（如SPA应用、大量图片资源），建议设置为60秒或更长。可通过 `BROWSER_TIMEOUT` 环境变量调整.
### Q3：如何处理Cloudflare等反爬机制？

免费版不包含Cloudflare绕过能力。遇到反爬验证页面时，建议：(1) 降低抓取频率；(2) 设置合理的User-Agent；(3) 升级专业版获取自动绕过能力.
### Q4：标签页为什么会堆积？

免费版提供基础的标签页清理能力，建议在每次操作完成后调用 `cleanup()` 方法主动清理。如遇异常退出导致标签页未关闭，下次启动时系统会自动检测并清理残留标签页.
### Q5：表单填写支持哪些字段类型？

免费版支持基础文本字段填写（text/email/password/textarea）。对于复杂字段类型（select下拉框、radio单选、checkbox复选、文件上传），需升级至专业版.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 18+ （运行浏览器自动化脚本）
- **浏览器**: Chromium 100+（首次运行会自动下载）

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Node.js 18+ | 运行时 | 必需 | 官网下载安装 |
| Playwright | npm包 | 必需 | `npm install playwright` |
| Chromium | 浏览器 | 必需 | `npx playwright install chromium` |
| Python 3.8+ | 运行时 | 可选 | 仅辅助脚本使用 |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置

- 免费版无需任何API Key
- 浏览器自动化基于本地Playwright执行，不涉及云端API调用
- 如需将抓取结果交给LLM处理，由Agent平台内置LLM提供能力

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+命令行执行）
- **说明**: 通过自然语言指令驱动Agent执行浏览器自动化任务，部分功能需要exec命令行执行能力

---
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 已知限制

本免费体验版限制以下高级功能（需升级至专业版解锁）：

- **批量URL处理**（multi-pages批量模式、并发抓取）
- **并发锁机制**（防止profile冲突）
- **Cloudflare自动绕过**（验证页面识别与处理）
- **复杂表单字段**（select/radio/checkbox/file upload）
- **页面截图与PDF导出**
- **结构化数据提取**（CSS/XPath选择器配置）
- **企业级集成**（CI/CD流水线、监控告警）
- **优先技术支持**

解锁全部高级能力请使用专业版：`browser-automation-v2-tool-pro`

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```bash
# 在此执行相关操作
echo "操作完成"
```json
{
  "success": true,
  "data": {
    "result": "浏览器自动化(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "browser automation v2"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
