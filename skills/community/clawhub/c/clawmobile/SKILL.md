---
name: clawmobile
description: >
  ClawMobile - 完整的 Android 自动化工具包，深度集成 AutoX.js。
  提供工作流管理、任务录制、AI 智能干预、会员系统、HTTP API 通信等完整功能。
  支持自动化测试、RPA 流程自动化、移动应用交互等场景。
  适用场景：自动化测试、批量操作、流程录制和回放、无人值守任务、移动应用 RPA。
version: 1.0.0
author: ClawMobile Team
email: support@clawmobile.com
license: MIT
repository: https://github.com/clawmobile/clawmobile
tags: android,automation,autox,rpa,workflow,testing,recording,ai,membership,http-api
metadata:
  category: automation
  complexity: advanced
  maintenance_stability: active
  openclaw:
    requires:
      bins:
        - adb
        - python3
        - curl
      env:
        - CLAWMOBILE_API_URL
        - CLAWMOBILE_API_TOKEN
      config:
        api_url: "http://localhost:8765"
        api_timeout: 30000
        max_retries: 3
        retry_delay: 1000
        default_kernel: "accessibility"
        device_connection:
          max_retries: 60
          test_interval: 30000
          auto_reconnect: true
        membership:
          default_tier: "free"
          daily_runs:
            free: 3
            vip: -1
            svip: -1
        recording:
          default_duration: 300
          max_duration: 3600
          capture_screenshots: true
    examples:
      - "执行工作流: 运行豆包视频生成工作流，参数：关键词春天风景"
      - "录制操作: 开始录制我的屏幕操作，生成 AutoX.js 代码"
      - "会员激活: 激活 VIP 会员兑换码 C-TEST1234-24-01M-A1B2C3D4"
      - "连接测试: 测试与 AutoX.js 服务器的连接状态"
      - "批量执行: 批量执行多个工作流，参数：workflows=[workflow_001,workflow_002]"
      - "AI干预: 启用 AI 干预模式，自动处理未知页面和异常"
      - "列出工作流: 查询所有可用工作流列表"
      - "会员状态: 查询当前用户的会员等级和权限"
    permissions:
      required:
        - android.permission.INTERNET
        - android.permission.ACCESS_NETWORK_STATE
        - android.permission.WRITE_EXTERNAL_STORAGE
        - android.permission.READ_PHONE_STATE
        - android.permission.ACCESS_WIFI_STATE
    api_version: "1.0"
    dependencies:
      openclaw: ">=1.0.0"
      autox: ">=6.5.5.10"
      python: ">=3.7"
    limitations:
      - 仅支持 Android 7.0+ (API 24+)
      - 需要 AutoX.js 已安装并运行 HTTP 服务器
      - 某些功能需要特定会员等级（VIP/SVIP）
      - 需要正确配置 ADB 连接
    keywords:
      - android automation
      - autox
      - rpa
      - workflow automation
      - mobile testing
      - task recording
      - ai intervention
      - membership system
      - http api
      - batch execution
---

# ClawMobile - Android Automation Toolkit 🤖

完整的企业级 Android 自动化解决方案，深度集成 AutoX.js，提供强大的工作流管理、任务录制、AI 智能干预和会员系统。

## 概述

ClawMobile 是一个功能强大的 Android 设备自动化工具包，通过 AutoX.js HTTP 服务器实现完整的设备控制。它将移动自动化、RPA（机器人流程自动化）和 AI 智能决策完美结合，为开发者、测试人员和 RPA 工程师提供全面的自动化解决方案。

### 核心价值

- 🎯 **低代码开发**：通过录制和 AI 生成快速创建自动化脚本
- 🤖 **AI 赋能**：智能异常处理和自动恢复机制
- 📊 **可观测性**：完整的日志记录和执行追踪
- 🔐 **权限管理**：三级会员体系，灵活的功能访问控制
- 🚀 **HTTP API**：标准的 RESTful API，易于集成
- 📦 **开箱即用**：完整的示例和配置，快速上手

### 触发条件

当用户提到以下需求时，自动触发此 Skill：

**工作流相关**：
- "执行工作流"、"运行工作流"
- "创建工作流"、"新建工作流"
- "列出工作流"、"查看工作流"
- "删除工作流"
- "验证工作流"

**录制相关**：
- "录制操作"、"开始录制"
- "停止录制"
- "录制回放"
- "生成 AutoX.js 代码"

**会员相关**：
- "激活会员"、"兑换码"
- "会员状态"、"查询会员"
- "VIP 激活"、"SVIP 激活"

**测试和自动化**：
- "自动化测试"、"Android 测试"
- "批量操作"、"批量执行"
- "RPA"、"流程自动化"
- "无人值守任务"

**AI 相关**：
- "AI 干预"、"智能决策"
- "自动处理异常"
- "自动恢复"

## 核心功能

### 1. 工作流管理 📋

**功能特性**：
- ✅ 工作流 CRUD（创建、读取、更新、删除）
- ✅ 参数化工作流支持
- ✅ 定时任务调度
- ✅ 工作流执行和监控
- ✅ 工作流验证和分析
- ✅ 工作流导入/导出（VIP 专属）

**使用场景**：
- 自动化测试脚本执行
- 批量任务处理
- 定时任务调度
- 工作流模板管理
- 跨设备工作流共享

**API 端点**：
- `GET /workflows` - 列出所有工作流
- `GET /workflows/{id}` - 获取工作流详情
- `POST /workflows` - 创建工作流
- `PUT /workflows/{id}` - 更新工作流
- `DELETE /workflows/{id}` - 删除工作流
- `POST /api/v1/workflows/{id}/validate` - 验证工作流

### 2. 录制功能 ⏺️

**功能特性**：
- ✅ UI 操作录制
- ✅ 自动代码生成
- ✅ 工作流创建
- ✅ 录制回放
- ✅ 录制暂停/恢复
- ✅ 截图捕获
- ✅ UI 树捕获

**使用场景**：
- 快速创建自动化脚本
- 学习 AutoX.js 编程
- 捕获和复现用户操作
- 生成测试用例

**API 端点**：
- `POST /recording/start` - 开始录制
- `POST /recording/pause` - 暂停录制
- `POST /recording/resume` - 恢复录制
- `POST /recording/stop` - 停止录制

### 3. AI 干预 🤖

**功能特性**：
- ✅ 未知页面智能识别
- ✅ 自动决策和恢复
- ✅ 上下文感知执行
- ✅ 学习型决策优化
- ✅ 参数自动决策（SVIP 专属）

**使用场景**：
- 处理预期外的 UI 变化
- 自动错误恢复
- 减少人工干预
- 提高脚本健壮性

**API 端点**：
- `POST /intervention` - 请求 AI 干预
- `POST /api/v1/parameters/decide` - 参数自动决策
- `GET /api/v1/parameters/decisions/stats` - 决策统计

### 4. 会员系统 💎

**功能特性**：
- ✅ 三级会员体系（Free/VIP/SVIP）
- ✅ 兑换码激活系统
- ✅ 功能权限控制
- ✅ 使用次数管理
- ✅ 会员历史记录

**会员等级对比**：

| 功能 | Free | VIP | SVIP |
|------|------|-----|------|
| 每日运行次数 | 3 | 无限 | 无限 |
| 定时任务 | ❌ | ✅ | ✅ |
| AI 干预 | ❌ | ✅ | ✅ |
| 导入/导出 | ❌ | ✅ | ✅ |
| 自然语言生成 | ✅ | ✅ | ✅ |
| 参数自动决策 | ❌ | ❌ | ✅ |
| 高级分析 | ❌ | ❌ | ✅ |

**兑换码格式**：`C-VENDORCODE-YY-DDM-CHECKSUM`（5 段格式）

**API 端点**：
- `GET /api/v1/membership/status` - 获取会员状态
- `POST /api/v1/membership/validate` - 验证兑换码
- `POST /api/v1/membership/check-permission` - 检查权限
- `GET /api/v1/membership/history` - 获取历史记录

### 5. HTTP API 客户端 🌐

**功能特性**：
- ✅ RESTful API 设计
- ✅ JSON 请求/响应
- ✅ Bearer Token 认证
- ✅ 错误处理和重试
- ✅ 连接池管理
- ✅ 超时控制

**API 端点**：
- `GET /api/v1/health` - 健康检查
- `GET /status` - 服务器状态
- `POST /execute` - 执行任务
- `POST /check_status` - 检查状态
- `POST /stop` - 停止任务

## 快速开始

### 前置条件

#### 1. 硬件要求

- Android 设备（Android 7.0+ / API 24+）
- USB 数据线（用于 ADB 连接）
- 开发机（Windows/Linux/macOS）

#### 2. 软件要求

- **AutoX.js** v6.5.5.10+ （必需）
- **Python** 3.7+ （必需）
- **ADB**（Android Debug Bridge）（必需）
- **OpenClaw** Gateway（必需）

#### 3. 网络要求

- 局域网连接（远程模式）或 USB 调试（本地模式）
- 设备和开发机网络互通（远程模式）

### 安装步骤

#### 方式一：通过 ClawHub 安装（推荐）

```bash
# 安装 ClawMobile Skill
clawhub install clawmobile

# 验证安装
ls -la ~/.openclaw/skills/clawmobile/SKILL.md

# 刷新 OpenClaw
openclaw gateway restart
```

#### 方式二：通过 Git Clone 安装

```bash
# 创建技能目录
mkdir -p ~/.openclaw/skills

# 克隆仓库
cd ~/.openclaw/skills
git clone https://gitee.com/your-repo/clawmobile.git clawmobile

# 验证安装
ls -la clawmobile/SKILL.md
```

#### 方式三：手动安装

```bash
# 下载 Skill 包
wget https://github.com/clawmobile/clawmobile/archive/v1.0.0.zip

# 解压到技能目录
unzip v1.0.0.zip -d ~/.openclaw/skills/
mv ~/.openclaw/skills/clawmobile-1.0.0 ~/.openclaw/skills/clawmobile
```

### 基础配置

#### 1. 启动 AutoX.js HTTP 服务器

在 Android 设备上：
1. 打开 AutoX.js App
2. 进入"设置" → "HTTP 服务"
3. 启用 HTTP 服务器
4. 配置端口（默认 8765）
5. 设置认证 Token

#### 2. 配置 ADB 连接

```bash
# 连接设备
adb devices

# 验证连接
adb shell getprop ro.build.version.sdk

# 转发端口（如需远程访问）
adb forward tcp:8765 tcp:8765
```

#### 3. 配置 ClawMobile

**方法 A：使用配置文件**

```bash
cat > config/settings.yaml << 'EOF'
# API 配置
api:
  base_url: "http://localhost:8765"
  timeout: 30000
  max_retries: 3
  retry_delay: 1000

# 服务器配置
server:
  host: "0.0.0.0"
  port: 8765
  workers: 4

# 认证配置
auth:
  token_env: "CLAWMOBILE_API_TOKEN"
  default_token: "your-autox-token-here"

# 连接配置
connection:
  mode: "local"
  max_retries: 60
  test_interval: 30000
  auto_reconnect: true

# 会员配置
membership:
  default_tier: "free"
  daily_runs:
    free: 3
    vip: -1
    svip: -1

# 录制配置
recording:
  default_duration: 300
  max_duration: 3600
  capture_screenshots: true
  capture_ui_tree: true

# 日志配置
logging:
  level: "INFO"
  file: "clawmobile.log"
  max_size: "10MB"
  backup_count: 5
EOF
```

**方法 B：使用环境变量**

```bash
# 设置环境变量
export CLAWMOBILE_API_URL="http://localhost:8765"
export CLAWMOBILE_API_TOKEN="your-autox-token-here"
export CLAWMOBILE_TIMEOUT="30000"

# 或添加到 ~/.bashrc
echo 'export CLAWMOBILE_API_URL="http://localhost:8765"' >> ~/.bashrc
echo 'export CLAWMOBILE_API_TOKEN="your-autox-token-here"' >> ~/.bashrc
source ~/.bashrc
```

#### 4. 验证连接

```bash
# 测试基本连接
curl http://localhost:8765/api/v1/health

# 预期响应：
# {"success": true, "health": {"status": "healthy", ...}}

# 使用 Python 客户端测试
python3 -c "
from skill.client import ClawMobileClient
client = ClawMobileClient()
health = client.get_health()
print(f'Health: {health}')
"
```

### 基本用法

#### 使用 Python 客户端

```python
from skill.client import ClawMobileClient

# 创建客户端
client = ClawMobileClient()

# 1. 列出工作流
workflows = client.list_workflows()
for workflow in workflows:
    print(f"{workflow['workflow_name']} - {workflow['workflow_id']}")

# 2. 执行工作流
result = client.execute_workflow(
    workflow_id="workflow_001",
    params={"keyword": "春天的风景"}
)
print(f"Task ID: {result['task_id']}")
print(f"Status: {result['status']}")

# 3. 开始录制
recording = client.start_recording(
    workflow_id="workflow_001",
    app_package="com.doubao.app",
    options={
        "capture_screenshots": True,
        "capture_ui_tree": True
    }
)
print(f"Recording ID: {recording['recording_id']}")

# 4. 检查会员状态
membership = client.get_membership_status(user_id="user_001")
print(f"Tier: {membership['tier']}")
print(f"Active: {membership['is_active']}")
print(f"Remaining Runs: {membership['today_usage']['runs_remaining']}")
```

#### 使用 cURL

```bash
# 设置认证 Token
export TOKEN="your-autox-token-here"

# 健康检查
curl http://localhost:8765/api/v1/health

# 列出工作流
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8765/workflows

# 执行工作流
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id":"task_001","workflow_id":"workflow_001"}' \
  http://localhost:8765/execute

# 开始录制
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"workflow_id":"workflow_001","app_package":"com.doubao.app"}' \
  http://localhost:8765/recording/start
```

## API 参考

### 核心端点

#### 工作流管理

##### GET /workflows
列出所有工作流

**响应**：
```json
{
  "workflows": [
    {
      "workflow_id": "workflow_001",
      "workflow_name": "豆包视频生成+发布",
      "kernel_type": "accessibility",
      "created_at": "2026-03-29T11:00:00Z",
      "run_count": 15,
      "success_rate": 93.3
    }
  ]
}
```

##### POST /workflows
创建工作流

**请求**：
```json
{
  "workflow_name": "新工作流",
  "kernel_type": "accessibility",
  "description": "工作流描述"
}
```

**响应**：
```json
{
  "success": true,
  "workflow_id": "workflow_002",
  "created_at": "2026-03-31T12:00:00Z"
}
```

#### 任务执行

##### POST /execute
执行工作流任务

**请求**：
```json
{
  "id": "task_001",
  "type": "sequence",
  "kernel_type": "accessibility",
  "priority": "normal",
  "timeout": 30000,
  "workflow_id": "workflow_001",
  "params": {
    "keyword": "春天的风景"
  }
}
```

**响应**：
```json
{
  "success": true,
  "result": {
    "task_id": "task_001",
    "status": "completed",
    "steps_result": [...],
    "total_duration_ms": 3200
  }
}
```

#### 录制功能

##### POST /recording/start
开始录制

**请求**：
```json
{
  "workflow_id": "workflow_001",
  "app_package": "com.doubao.app",
  "kernel_type": "accessibility",
  "options": {
    "capture_screenshots": true,
    "capture_ui_tree": true
  }
}
```

**响应**：
```json
{
  "success": true,
  "recording_id": "rec_001",
  "started_at": "2026-03-31T12:00:00Z",
  "floating_window_enabled": true
}
```

#### 会员系统

##### GET /api/v1/membership/status
获取会员状态

**参数**：
- `user_id`（查询参数）：用户 ID

**响应**：
```json
{
  "success": true,
  "membership": {
    "user_id": "user_001",
    "tier": "vip",
    "is_active": true,
    "activated_at": "2026-03-30T14:30:00Z",
    "expires_at": "2026-04-30T14:30:00Z"
  },
  "permissions": {
    "max_daily_runs": -1,
    "can_schedule": true,
    "can_use_ai_intervention": true
  },
  "today_usage": {
    "runs_completed": 2,
    "runs_remaining": -1
  }
}
```

##### POST /api/v1/membership/validate
验证兑换码

**请求**：
```json
{
  "code": "C-VENDORCODE-24-01M-A1B2C3D4",
  "user_id": "user_001"
}
```

**响应**：
```json
{
  "success": true,
  "membership": {
    "tier": "vip",
    "activated_at": "2026-03-31T12:00:00Z",
    "expires_at": "2026-04-30T12:00:00Z"
  }
}
```

### 完整 API 文档

详细的 API 文档请参考：`docs/API-DOCUMENTATION.md`

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `CLAWMOBILE_API_URL` | API 服务器地址 | http://localhost:8765 | ✅ |
| `CLAWMOBILE_API_TOKEN` | API 认证 Token | - | ✅ |
| `CLAWMOBILE_TIMEOUT` | 请求超时(ms) | 30000 | ❌ |
| `CLAWMOBILE_MAX_RETRIES` | 最大重试次数 | 3 | ❌ |
| `CLAWMOBILE_DEVICE_ID` | 目标设备 ID | - | ❌ |

### 配置文件

**config/settings.yaml**：
```yaml
# API 配置
api:
  base_url: "http://localhost:8765"
  timeout: 30000
  max_retries: 3
  retry_delay: 1000

# 服务器配置
server:
  host: "0.0.0.0"
  port: 8765
  workers: 4

# 认证配置
auth:
  token_env: "CLAWMOBILE_API_TOKEN"
  default_token: "clawmobile-secret-token-change-in-production"

# 连接配置
connection:
  mode: "local"
  remote_host: null
  max_retries: 60
  test_interval: 30000
  auto_reconnect: true

# 会员配置
membership:
  default_tier: "free"
  api_url: "http://localhost:8765"
  daily_runs:
    free: 3
    vip: -1
    svip: -1

# 录制配置
recording:
  default_duration: 300
  max_duration: 3600
  capture_screenshots: true
  capture_ui_tree: true

# 日志配置
logging:
  level: "INFO"
  file: "clawmobile.log"
  max_size: "10MB"
  backup_count: 5
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## 使用示例

### 示例 1：执行工作流

**场景**：自动化执行豆包视频生成工作流

```python
from skill.client import ClawMobileClient

client = ClawMobileClient()

# 执行工作流
result = client.execute_workflow(
    workflow_id="workflow_001",
    params={
        "keyword": "春天的风景",
        "duration": 45
    }
)

if result['success']:
    print("✅ 工作流执行成功")
    print(f"Task ID: {result['task_id']}")
    print(f"Status: {result['status']}")
    print(f"Duration: {result['total_duration_ms']}ms")
else:
    print(f"❌ 工作流执行失败: {result.get('error')}")
```

### 示例 2：录制操作并创建工作流

**场景**：录制屏幕操作并自动生成工作流

```python
# 开始录制
recording = client.start_recording(
    workflow_id="workflow_002",
    app_package="com.doubao.app",
    options={
        "capture_screenshots": True,
        "auto_stop": False
    }
)

print(f"录制已开始，ID: {recording['recording_id']}")
print("请在设备上执行操作...")

# 等待用户操作
import time
time.sleep(60)  # 录制 60 秒

# 停止录制
result = client.stop_recording(
    recording_id=recording['recording_id']
)

print(f"录制已完成，捕获 {len(result['recording']['events'])} 个事件")

# 生成工作流
workflow = client.create_workflow_from_recording(
    recording_id=recording['recording_id'],
    workflow_name="录制的操作"
)

print(f"工作流已创建: {workflow['workflow_id']}")
```

### 示例 3：会员激活

**场景**：激活 VIP 会员

```python
# 激活兑换码
result = client.activate_membership(
    code="C-VENDORCODE-24-01M-A1B2C3D4",
    user_id="user_001"
)

if result['success']:
    print("✅ 会员激活成功")
    print(f"等级: {result['membership']['tier']}")
    print(f"有效期至: {result['membership']['expires_at']}")

    # 查看权限
    membership = client.get_membership_status("user_001")
    print(f"每日运行次数: {membership['permissions']['max_daily_runs']}")
    print(f"可使用定时任务: {membership['permissions']['can_schedule']}")
    print(f"可使用 AI 干预: {membership['permissions']['can_use_ai_intervention']}")
else:
    print(f"❌ 激活失败: {result.get('error')}")
```

### 示例 4：批量执行

**场景**：批量执行多个工作流

```python
workflows = [
    {"workflow_id": "workflow_001", "params": {"keyword": "春天"}},
    {"workflow_id": "workflow_002", "params": {"content": "今日分享"}},
    {"workflow_id": "workflow_003", "params": {"style": "技术"}}
]

results = []
for wf in workflows:
    try:
        result = client.execute_workflow(**wf)
        results.append({
            "workflow_id": wf['workflow_id'],
            "status": "success",
            "task_id": result['task_id']
        })
        print(f"✅ {wf['workflow_id']}: {result['status']}")
    except Exception as e:
        results.append({
            "workflow_id": wf['workflow_id'],
            "status": "failed",
            "error": str(e)
        })
        print(f"❌ {wf['workflow_id']}: {e}")

# 统计结果
success_count = sum(1 for r in results if r['status'] == 'success')
print(f"\n完成: {success_count}/{len(workflows)}")
```

### 示例 5：AI 干预

**场景**：启用 AI 干预模式处理未知页面

```python
# 执行工作流时启用 AI 干预
result = client.execute_workflow(
    workflow_id="workflow_001",
    params={"keyword": "测试"},
    options={
        "enable_ai_intervention": True,
        "ai_intervention_threshold": 0.7
    }
)

# 查看 AI 决策统计
stats = client.get_ai_decision_stats()
print(f"总决策次数: {stats['total_decisions']}")
print(f"成功率: {stats['success_rate']}%")
print(f"平均响应时间: {stats['avg_response_time']}ms")
```

## 故障排除

### 常见问题

#### 问题 1：连接失败

**症状**：
```
ConnectionError: Failed to connect to API server
```

**解决方案**：

1. 检查 AutoX.js 是否运行：
   ```bash
   adb shell ps | grep autojs
   ```

2. 检查服务器端口：
   ```bash
   adb shell netstat -an | grep 8765
   ```

3. 验证连接：
   ```bash
   curl http://localhost:8765/api/v1/health
   ```

4. 检查 ADB 连接：
   ```bash
   adb devices
   ```

5. 重启 AutoX.js HTTP 服务器

#### 问题 2：权限不足

**症状**：
```
PermissionError: Feature requires VIP membership
```

**解决方案**：

1. 检查当前会员等级：
   ```python
   membership = client.get_membership_status("user_001")
   print(f"Current tier: {membership['tier']}")
   ```

2. 激活会员或升级：
   ```python
   result = client.activate_membership("VIP-2024-ABCD1234")
   ```

3. 检查权限：
   ```python
   permission = client.check_permission("user_001", "can_use_ai_intervention")
   print(f"Permission granted: {permission['granted']}")
   ```

#### 问题 3：工作流执行失败

**症状**：
```
WorkflowExecutionError: Task execution failed
```

**诊断步骤**：

1. 查看详细错误信息：
   ```python
   result = client.execute_workflow(
       workflow_id="workflow_001",
       debug=True
   )
   print(result.get('error'))
   ```

2. 检查工作流状态：
   ```python
   workflow = client.get_workflow("workflow_001")
   print(f"Status: {workflow['status']}")
   print(f"Success Rate: {workflow['success_rate']}%")
   ```

3. 验证参数配置：
   ```python
   validation = client.validate_workflow("workflow_001")
   print(f"Valid: {validation['is_valid']}")
   print(f"Errors: {validation.get('errors', [])}")
   ```

4. 查看日志：
   ```bash
   tail -f clawmobile.log
   ```

#### 问题 4：兑换码验证失败

**症状**：
```
InvalidCodeError: Redeem code format invalid or expired
```

**解决方案**：

1. 验证兑换码格式：
   ```python
   # 正确格式：C-VENDORCODE-24-01M-A1B2C3D4
   # 5 段：类型-供应商-年份-时长-校验和
   from skill.membership import validate_redeem_code_format
   is_valid = validate_redeem_code_format("C-VENDORCODE-24-01M-A1B2C3D4")
   print(f"Format valid: {is_valid}")
   ```

2. 检查兑换码是否已使用：
   ```python
   result = client.validate_redeem_code("C-VENDORCODE-24-01M-A1B2C3D4", "user_001")
   print(f"Already used: {result.get('already_used', False)}")
   ```

3. 联系管理员获取新的兑换码

### 支持和帮助

**获取帮助**：
```bash
# 查看文档
cat clawmobile/docs/API-DOCUMENTATION.md
cat clawmobile/README.md

# 查看日志
cat clawmobile/clawmobile.log

# 运行测试
cd clawmobile
python3 -m pytest tests/
```

**联系支持**：
- Email: support@clawmobile.com
- GitHub Issues: https://github.com/clawmobile/clawmobile/issues
- 文档: https://docs.clawmobile.com

## 附录

### A. 相关文档

- **API-DOCUMENTATION.md** - 完整 API 参考
- **DATA-MODELS.md** - 数据模型定义
- **PRD.md** - 产品需求文档
- **TRD.md** - 技术需求文档
- **MEMBERSHIP-SYSTEM-GUIDE.md** - 会员系统指南
- **REDEEM-CODE-FORMAT.md** - 兑换码格式说明

### B. 工具和资源

#### ClawHub CLI
- 安装：`npm install -g clawhub`
- 文档：`clawhub --help`
- 网站：https://clawhub.ai

#### OpenClaw 文档
- Skills 指南：`/usr/lib/node_modules/openclaw/docs/creating-skills.md`
- ClawHub 指南：`/usr/lib/node_modules/openclaw/docs/tools/clawhub.md`

#### AutoX.js 资源
- 官方文档：https://autoxjs.com/
- GitHub：https://github.com/TonyJiangWJ/AutoX.js

### C. 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 1.0.0 | 2026-03-31 | 初始版本：完整的 ClawMobile Skill |

### D. 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### E. 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 总结

ClawMobile 是一个功能完整、生产就绪的 Android 自动化 Skill。通过本 SKILL.md，您应该能够：

- ✅ 理解 ClawMobile 的核心功能和使用场景
- ✅ 快速安装和配置 ClawMobile Skill
- ✅ 使用 Python 客户端或 HTTP API 与 AutoX.js 交互
- ✅ 管理工作流、录制操作、激活会员
- ✅ 排查常见问题

**下一步**：
1. 阅读详细的 API 文档：`docs/API-DOCUMENTATION.md`
2. 查看更多示例：`docs/examples/`
3. 加入社区讨论：https://github.com/clawmobile/clawmobile/discussions

---

*ClawMobile SKILL.md v1.0.0 | Last Updated: 2026-03-31 | Status: Production Ready*
