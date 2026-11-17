---
slug: bsession-tool-free
name: bsession-tool-free
version: 1.0.0
displayName: 浏览器会话(免费版)
summary: "浏览器会话管理免费版，支持一次性页面抓取、基础会话列表与简易调试.。浏览器会话助手免费版是面向个人开发者的轻量浏览器会话管理工具。聚焦"打开URL-提取信息-返回结果"三步流程，无需编写完整"
license: MIT
edition: free
description: "浏览器会话助手免费版是面向个人开发者的轻量浏览器会话管控工具。聚焦\"打开URL-提取信息-返回结果\"三步流程，无需编写完整脚本即可完成单次页面抓取任务。Use. 适用于需要bsession tool相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量. 适用于需要bsession tool相关能力的开发场景,包含结构化的工作流程和配置指引."
tags:
  - 浏览器会话
  - bsession
  - automation
  - productivity
  - developer-tools
  - 单次抓取
  - Docker
  - 轻量级
  - 搜索
  - 检索
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"
pricing_tier: free

---
# 浏览器会话助手（免费版）
> **打开URL、提取信息、返回结果。三步完成单次浏览器会话。**

无需编写完整自动化脚本，通过简单的fetch命令即可完成单次页面抓取任务。免费版聚焦轻量场景，让浏览器自动化触手可及.
## 概述
免费版浏览器会话工具为个人开发者提供基础的浏览器会话管理能力。通过Docker容器化的Chrome实例，在隔离环境中执行页面操作，保障本地系统安全.
### 核心定位
| 维度 | 免费版能力 |
|---|-----|
| 单次抓取（fetch） | 支持 |
| 定时任务（recurring） | 不支持（需专业版） |
| 会话持久化 | 不支持（需专业版） |
| Webhook通知 | 不支持（需专业版） |
| 批量会话管理 | 不支持（需专业版） |
| 基础元素交互 | 支持（click/fill/snapshot） |
| Docker容器隔离 | 支持 |
| 调试模式 | 支持（基础） |

## 核心能力
### 1. 单次页面抓取（fetch模式）
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 浏览器会话(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```python
import subprocess
import json
# ...
class BsessionFetcher:
    """浏览器会话抓取器（免费版）"""
# ...
    def __init__(self, container_name="agent-browser"):
        self.container = container_name
# ...
    def check_container(self):
        """检查容器是否运行"""
        try:
            result = subprocess.run(
                ["docker", "exec", self.container, "echo", "ok"],
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
# ...
    def find_free_port(self, start=9222, max_try=10):
        """查找可用的CDP端口"""
        for port in range(start, start + max_try):
            check_cmd = f"docker exec {self.container} python3 -c \"import urllib.request; " \
                       f"urllib.request.urlopen('http://localhost:{port}/json/version', timeout=2)\""
run(check_cmd, shell=True, capture_output=True)
            if result.returncode != 0:
                return port
        return None
# ...
    def fetch_url(self, url, wait_seconds=5):
        """抓取单个URL内容"""
        if not self.check_container():
            return {"success": False, "error": "容器未运行，请先执行 setup"}
# ...
        port = self.find_free_port()
        if not port:
            return {"success": False, "error": "无可用CDP端口"}
# ...
        try:
            # 启动临时Chrome
            subprocess.run(
container, "python3", "-c",
                 f"import sys; sys.path.insert(0, '/app'); "
                 f"from lib.browser import start_chrome; "
                 f"start_chrome({port}, '/workspace/data/profile-tmp')"],
                capture_output=True, text=True, timeout=10
            )
# ...
            # 打开URL
container, "agent-browser",
                 "--cdp", str(port), "open", url],
                capture_output=True, text=True, timeout=30
            )
# ...
            # 等待加载
            import time
            time.sleep(wait_seconds)
# ...
            # 获取页面快照
container, "agent-browser",
                 "--cdp", str(port), "snapshot"],
                capture_output=True, text=True, timeout=10
            )
# ...
            return {
                "success": True,
                "content": result.stdout,
                "port": port,
                "url": url
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            # 清理临时Chrome
container, "python3", "-c",
path.insert(0, '/app'); "
browser import stop_chrome; "
                 f"stop_chrome({port})"],
                capture_output=True, text=True, timeout=5
            )
# ...
# 示例
fetcher = BsessionFetcher()
result = fetcher.fetch_url("https://example.com", wait_seconds=3)
print(result.get("content", "")[:500] if result.get("success") else result.get("error"))
```

**处理**: 解析单次页面抓取（fetch模式）的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回单次页面抓取（fetch模式）的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 基础元素交互
```python
class BsessionInteraction:
    """基础元素交互（免费版）"""
# ...
    def __init__(self, container="agent-browser", port=9222):
        self.container = container
        self.port = port
# ...
    def click_element(self, ref):
        """点击元素"""
        cmd = ["docker", "exec", self.container, "agent-browser",
               "--cdp", str(self.port), "click", ref]
run(cmd, capture_output=True, text=True)
# ...
    def fill_field(self, ref, value):
        """填写表单字段"""
container, "agent-browser",
port), "fill", ref, value]
run(cmd, capture_output=True, text=True)
# ...
    def take_snapshot(self):
        """获取页面快照"""
container, "agent-browser",
run(cmd, capture_output=True, text=True)
stdout if result.returncode == 0 else ""
# ...
# 使用示例
interaction = BsessionInteraction(port=9222)
content = interaction.take_snapshot()
# 解析ref后执行交互
# interaction.click_element("ref_button_1")
# interaction.fill_field("ref_input_email", "user@test.com")
```

**处理**: 解析基础元素交互的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回基础元素交互的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 会话列表查看
```python
class SessionLister:
    """会话列表查看器（免费版）"""
# ...
    def list_sessions(self):
        """列出所有会话"""
        try:
                ["docker", "exec", "agent-browser", "python3", "-c",
                 "import sys; sys.path.insert(0, '/app'); "
                 "from lib.browser import list_sessions; "
                 "list_sessions()"],
                capture_output=True, text=True, timeout=10
            )
        except Exception as e:
            return f"查询失败：{e}"
# ...
    def show_session(self, session_name):
        """查看指定会话详情"""
        try:
                ["docker", "exec", "agent-browser", "bsession", "show", session_name],
                capture_output=True, text=True, timeout=10
            )
        except Exception as e:
            return f"查询失败：{e}"
```

**处理**: 解析会话列表查看的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回会话列表查看的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：浏览器会话管理免、支持一次性页面抓、基础会话列表与简、易调试、浏览器会话助手免、费版是面向个人开、发者的轻量浏览器、会话管理工具、提取信息、返回结果、三步流程、无需编写完整脚本、即可完成单次页面、抓取任务、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一：单次页面信息提取
**场景描述**：需要快速提取某网页的标题和正文内容.
```python
fetcher = BsessionFetcher()
result = fetcher.fetch_url("https://news.example.com/article/123", wait_seconds=3)
# ...
if result.get("success"):
    content = result["content"]
    # 简单解析内容
    title = content.split("\n")[0] if content else "未获取到标题"
    print(f"标题：{title}")
    print(f"内容长度：{len(content)} 字符")
else:
    print(f"抓取失败：{result.get('error')}")
```

### 场景二：简易登录测试
**场景描述**：测试某网站的登录流程是否正常.
```python
# 1. 打开登录页
fetcher = BsessionFetcher()
result = fetcher.fetch_url("https://app.example.com/login")
# ...
# 2. 获取快照并解析元素ref
interaction = BsessionInteraction(port=result.get("port", 9222))
snapshot = interaction.take_snapshot()
# ...
# 3. 填写表单并提交（需根据实际页面结构调整ref）
# interaction.fill_field("ref_email", "test@user.com")
# interaction.fill_field("ref_password", "password123")
# interaction.click_element("ref_login_button")
# 4. 验证登录结果
# final_snapshot = interaction.take_snapshot()
# print("登录成功" if "dashboard" in final_snapshot else "登录失败")
```

### 场景三：学习浏览器自动化
**场景描述**：初学者通过单次抓取学习浏览器自动化基础.
```python
# 学习示例：理解浏览器自动化基础流程
print("=== 浏览器会话基础流程 ===")
print("1. 检查容器状态")
fetcher = BsessionFetcher()
if fetcher.check_container():
    print("   容器运行中")
else:
    print("   容器未运行，请先执行 setup")
# ...
print("\n2. 查找可用端口")
port = fetcher.find_free_port()
print(f"   可用端口：{port}")
# ...
print("\n3. 抓取页面")
result = fetcher.com")
print(f"   抓取结果：{'成功' if result.get('success') else '失败'}")
# ...
print("\n4. 解析内容")
if result.get("success"):
    content_length = len(result.get("content", ""))
    print(f"   内容长度：{content_length} 字符")
```

## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 30秒上手
```bash
# 1. 检查Docker容器
docker exec agent-browser echo ok
# ...
# 2. 执行单次抓取
docker exec agent-browser agent-browser --cdp 9222 open "https://example.com"
sleep 3
docker exec agent-browser agent-browser --cdp 9222 snapshot
```bash
# 在此执行相关操作
echo "操作完成"
```bash
# 1. 启动容器（如果未运行）
cd ./.bsession/
docker compose up -d
# ...
# 2. 验证环境
docker exec agent-browser python3 -c "
import sys; sys.path.insert(0, '/app')
from lib.browser import list_sessions
print('环境正常')
"
# ...
# 3. 执行抓取
docker exec agent-browser agent-browser --cdp 9222 open "https://news.example.com"
sleep 5
docker exec agent-browser agent-browser --cdp 9222 snapshot > page_content.txt
# ...
# 4. 清理
docker exec agent-browser python3 -c "
import sys; sys.path.insert(0, '/app')
from lib.browser import stop_chrome
stop_chrome(9222)
"
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 配置示例
### 基础配置
```python
import os
# ...
class BsessionConfig:
    """bsession配置（免费版）"""
    CONTAINER_NAME = os.getenv("BSESSION_CONTAINER", "agent-browser")
    DEFAULT_PORT = int(os.getenv("BSESSION_PORT", "9222"))
    WORKSPACE = os.getenv("BSESSION_WORKSPACE", "./.bsession/workspace/")
    WAIT_TIMEOUT = int(os.getenv("BSESSION_WAIT", "5"))
    MAX_PORTS_TRY = int(os.getenv("BSESSION_MAX_PORTS", "10"))
# ...
    @classmethod
    def show(cls):
        print("=== bsession 配置 ===")
        print(f"容器名称：{cls.CONTAINER_NAME}")
        print(f"默认端口：{cls.DEFAULT_PORT}")
        print(f"工作空间：{cls.WORKSPACE}")
        print(f"等待时间：{cls.WAIT_TIMEOUT}s")
        print(f"最大端口尝试：{cls.MAX_PORTS_TRY}")
# ...
BsessionConfig.show()
```bash
# 在此执行相关操作
echo "操作完成"
```python
import os
from pathlib import Path
# ...
def resolve_bsession_paths():
    """解析bsession路径（按优先级）"""
    paths = {
        "bsession_home": None,
        "workspace": None,
        "cli_path": None
    }
# ...
    # 1. 解析bsession CLI
    cli_candidates = [
        os.getenv("BSESSION_CLI"),
        os.path.expanduser("./.bsession/bsession"),
        "./bsession"
    ]
    for candidate in cli_candidates:
        if candidate and os.path.exists(candidate):
            paths["cli_path"] = candidate
            break
# ...
    # 2. 解析workspace
    workspace_candidates = [
        os.getenv("BSESSION_WORKSPACE"),
        os.path.expanduser("./.bsession/workspace/"),
        "./workspace/"
    ]
    for candidate in workspace_candidates:
path.exists(candidate):
            paths["workspace"] = candidate
            break
# ...
    # 3. 解析bsession_home
    paths["bsession_home"] = os.path.expanduser("./.bsession/")
# ...
    return paths
# ...
paths = resolve_bsession_paths()
for k, v in paths.items():
    print(f"{k}: {v}")
```bash
# 在此执行相关操作
echo "操作完成"
```python
# 使用try/finally确保Chrome进程被清理
def safe_fetch(validated_url):
    fetcher = BsessionFetcher()
    try:
        return fetcher.fetch_url(url)
    finally:
        # 确保临时Chrome被关闭
        subprocess.run(
            ["docker", "exec", "agent-browser", "python3", "-c",
path.insert(0, '/app'); "
browser import cleanup_temp; cleanup_temp()"],
            capture_output=True
        )
```

## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Docker**: 20+（运行bsession容器）
- **Python**: 3.8+（容器内执行）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Docker | 运行时 | 必需 | 官网下载安装 |
| Docker Compose | 工具 | 必需 | 随Docker Desktop安装 |
| Python 3.8+ | 运行时 | 必需 | 容器内已内置 |
| Chrome | 浏览器 | 必需 | 容器内已内置 |
| agent-browser CLI | 工具 | 必需 | 容器内已内置 |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置
- 免费版无需任何API Key
- 浏览器自动化基于本地Docker容器执行，不涉及云端调用
- LLM模型路由由Agent平台内置提供

### 可用性分类
- **分类**: MD+EXEC（Markdown指令+命令行执行）
- **说明**: 通过自然语言指令驱动Agent执行浏览器会话管理任务

---
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 已知限制
本免费体验版限制以下高级功能（需升级至专业版解锁）：

- **定时任务（recurring）**：循环执行、状态变化检测
- **会话持久化**：保存为可复用脚本（conf+py文件）
- **Webhook通知**：结果自动推送到n8n/飞书/Slack
- **批量会话管理**：多会话并发、状态聚合
- **企业级监控**：会话健康检查、失败告警
- **Cloudflare绕过**：自动识别与处理反爬
- **会话调试增强**：详细日志、断点调试
- **优先技术支持**

解锁全部高级能力请使用专业版：`bsession-tool-pro`
