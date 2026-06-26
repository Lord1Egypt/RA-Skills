# 八爪鱼 RPA Webhook Skill 完整使用手册

> 📘 本手册详细介绍如何配置和使用八爪鱼 RPA Webhook Skill，实现 OpenClaw 与八爪鱼 RPA 的自动化集成。

---

## 📖 目录

1. [什么是八爪鱼 RPA](#1-什么是八爪鱼-rpa)
2. [前置准备](#2-前置准备)
3. [安装 Skill](#3-安装-skill)
4. [配置八爪鱼 RPA 端](#4-配置八爪鱼-rpa-端)
5. [配置 Skill](#5-配置-skill)
6. [使用示例](#6-使用示例)
7. [与 OpenClaw 集成](#7-与-openclaw-集成)
8. [常见问题排查](#8-常见问题排查)

---

## 1. 什么是八爪鱼 RPA

**八爪鱼 RPA（Octoparse RPA）** 是一款企业级机器人流程自动化平台，支持：

- 🖱️ **网页自动化** - 模拟人工操作浏览器
- 📊 **数据采集** - 从网站提取结构化数据
- ⚙️ **流程编排** - 可视化设计自动化流程
- 🔗 **API 集成** - 通过 Webhook/API 触发任务

### 典型应用场景

| 场景 | 说明 |
|------|------|
| 电商监控 | 自动抓取商品价格、库存变化 |
| 舆情采集 | 定时抓取新闻、社交媒体数据 |
| 数据录入 | 自动填写表单、同步数据 |
| 报表生成 | 定期采集数据并生成报告 |

---

## 2. 前置准备

### 2.1 八爪鱼 RPA 账号

1. 访问 [八爪鱼 RPA 官网](https://rpa.bazhuayu.com/)
2. 注册/登录账号
3. 完成企业认证（如需使用 Webhook 功能）

### 2.2 环境要求

| 项目 | 要求 |
|------|------|
| Python | 3.6+ |
| 系统 | Linux / macOS / Windows |
| 网络 | 可访问八爪鱼 API 服务器 |

### 2.3 检查 Python 环境

```bash
python3 --version
# 应输出 Python 3.x.x
```

---

## 3. 安装 Skill

### 方式一：复制现有 Skill（推荐）

Skill 已存在于你的 OpenClaw 工作区：

```bash
# 进入工作区
cd ~/.openclaw/workspace/skills/

# 确认目录存在
ls -la bazhuayu-webhook/
```

### 方式二：从 ClawHub 安装（如已发布）

```bash
clawhub install bazhuayu-webhook
```

### 方式三：手动创建

```bash
# 创建目录
mkdir -p ~/.openclaw/workspace/skills/bazhuayu-webhook
cd ~/.openclaw/workspace/skills/bazhuayu-webhook

# 下载主程序（需要主程序文件）
# 将 bazhuayu-webhook.py 放入此目录
```

---

## 4. 配置八爪鱼 RPA 端

### 4.1 创建 Webhook 触发器

在使用 Webhook 之前，首先需要在八爪鱼 RPA 中创建 Webhook 触发器。

#### 步骤 1：进入触发器管理

1. 登录 [八爪鱼 RPA 控制台](https://rpa.bazhuayu.com/)
2. 进入【触发器】栏目
3. 点击 **"Webhook 触发器"**

#### 步骤 2：填写触发器信息

按顺序填写以下信息：

1. **触发器名称** → 输入易于识别的名称
   - 示例：`订单处理 `、`数据采集 `、` 每日报表`
   
2. **指定运行的机器人** → 选择要执行任务的机器人
   - 选择已配置好的机器人
   
3. **选择要运行的应用** → 选择对应的 RPA 应用
   - 选择你创建好的 RPA 流程/应用
   
4. 点击 **"确定"** 保存

#### 步骤 3：获取 Webhook 信息

创建成功后，会显示 Webhook 的详细信息：

| 信息 | 说明 | 示例 |
|------|------|------|
| **Webhook URL** | 调用接口地址 | `https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/xxx/invoke` |
| **签名密钥 (Key)** | 用于签名验证 | `a1b2c3d4e5f6g7h8` |

⚠️ **重要**：请立即复制并保存这两个信息，后续配置需要用到！

#### 步骤 4：启动触发器

⚠️ **必须勾选**："启动触发器"

- 未勾选则 Webhook 不会生效
- 勾选后状态显示为"运行中"

### 4.2 创建 RPA 应用

1. 登录 [八爪鱼 RPA 控制台](https://rpa.bazhuayu.com/)
2. 点击「创建应用」或「新建流程」
3. 设计你的自动化流程（使用可视化编辑器）

### 4.2 设置输入变量

在流程设计中添加**输入变量**：

1. 点击「变量」→「添加变量」
2. 设置变量名（如：`keyword`、`url`、`startDate`）
3. 设置默认值（可选）

> ⚠️ **重要**：记住变量名，后续配置需要完全一致！

### 4.3 创建 Webhook 触发器

1. 进入应用详情页
2. 点击「触发器」→「新建触发器」
3. 选择触发类型为 **Webhook**
4. 配置触发器：
   - **触发器名称**：自定义（如：OpenClaw 触发）
   - **签名密钥**：点击生成或自定义（请妥善保存！）
   - **允许的参数**：选择你创建的输入变量

5. 保存后复制 **Webhook URL**

### 4.4 记录关键信息

创建完成后，请记录以下信息：

```
✅ Webhook URL: https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/xxx/invoke
✅ 签名密钥：your-secret-key-here
✅ 参数名称：keyword, url, startDate
✅ 参数默认值：测试关键词，https://example.com, 2026-01-01
```

---

## 5. 配置 Skill

### 5.1 初始化配置

```bash
cd ~/.openclaw/workspace/skills/bazhuayu-webhook
python3 bazhuayu-webhook.py init
```

### 5.2 或手动编辑配置文件

创建/编辑 `config.json`：

```bash
# 复制配置模板
cp config.example.json config.json

# 编辑配置
vim config.json
# 或使用你喜欢的编辑器
```

### 5.3 配置文件格式

```json
{
  "url": "https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/你的 webhook ID/invoke",
  "key": "你的签名密钥",
  "paramNames": ["keyword", "url", "startDate"],
  "defaultParams": {
    "keyword": "默认搜索词",
    "url": "https://example.com",
    "startDate": "2026-01-01"
  }
}
```

### 5.4 配置项说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `url` | ✅ | Webhook 接口完整 URL |
| `key` | ✅ | 签名密钥（区分大小写） |
| `paramNames` | ✅ | 参数名称数组，顺序不限 |
| `defaultParams` | ❌ | 参数默认值，键名需与 paramNames 对应 |

### 5.5 验证配置

```bash
# 查看当前配置
python3 bazhuayu-webhook.py config

# 测试模式（不实际发送）
python3 bazhuayu-webhook.py test
```

---

## 6. 使用示例

### 6.1 运行任务（使用默认参数）

```bash
cd ~/.openclaw/workspace/skills/bazhuayu-webhook
python3 bazhuayu-webhook.py run
```

**输出示例：**
```
✅ 任务已触发！
   企业 ID: ent_xxxxx
   应用 ID: flow_xxxxx
   运行批次：20260307001
```

### 6.2 运行任务（指定参数）

```bash
# 单个参数
python3 bazhuayu-webhook.py run --keyword=人工智能

# 多个参数
python3 bazhuayu-webhook.py run --keyword=AI --url=https://news.example.com --startDate=2026-03-01
```

### 6.3 创建快捷命令

编辑 Shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）：

```bash
# 添加别名
alias rpa-run='cd ~/.openclaw/workspace/skills/bazhuayu-webhook && python3 bazhuayu-webhook.py run'
alias rpa-config='cd ~/.openclaw/workspace/skills/bazhuayu-webhook && python3 bazhuayu-webhook.py config'

# 使配置生效
source ~/.bashrc
```

之后可以直接运行：
```bash
rpa-run --keyword=测试
```

### 6.4 在脚本中调用

```bash
#!/bin/bash
# run-rpa-task.sh

SKILL_DIR=~/.openclaw/workspace/skills/bazhuayu-webhook
KEYWORD=$1
URL=$2

cd $SKILL_DIR
python3 bazhuayu-webhook.py run --keyword="$KEYWORD" --url="$URL"
```

---

## 7. 与 OpenClaw 集成

### 7.1 在 OpenClaw Skill 中调用

创建新的 OpenClaw Skill 来封装 RPA 调用：

```python
# ~/.openclaw/workspace/skills/my-rpa-automation/rpa_caller.py

import subprocess
import json

def run_rpa_task(keyword=None, url=None):
    """调用八爪鱼 RPA 任务"""
    
    cmd = [
        "python3",
        "~/.openclaw/workspace/skills/bazhuayu-webhook/bazhuayu-webhook.py",
        "run"
    ]
    
    if keyword:
        cmd.append(f"--keyword={keyword}")
    if url:
        cmd.append(f"--url={url}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout
```

### 7.2 创建自动化流程示例

**场景**：用户说"采集新闻"时自动触发 RPA

```python
# 在 OpenClaw 的自定义技能中
async def handle_news_collection(user_message):
    # 从用户消息提取关键词
    keyword = extract_keyword(user_message)
    
    # 调用 RPA
    result = run_rpa_task(keyword=keyword, url="https://news.example.com")
    
    # 返回结果给用户
    return f"已启动新闻采集任务，关键词：{keyword}"
```

### 7.3 定时任务集成

结合 OpenClaw 的 cron 技能实现定时采集：

```bash
# 每天上午 9 点自动运行
0 9 * * * cd ~/.openclaw/workspace/skills/bazhuayu-webhook && python3 bazhuayu-webhook.py run
```

---

## 8. 常见问题排查

### 8.1 签名验证失败

**错误信息：** `SignatureVerificationFailureOrTimestampExpired`

**解决方案：**

1. **检查系统时间**
   ```bash
   date
   # 确保时间与网络时间同步
   ```

2. **同步系统时间**
   ```bash
   # Linux
   sudo ntpdate pool.ntp.org
   
   # 或使用 timedatectl
   sudo timedatectl set-ntp true
   ```

3. **检查签名密钥**
   - 确认 Key 复制完整，无多余空格
   - 确认 Key 区分大小写

### 8.2 参数未设置值

**错误信息：** 参数值为空或使用默认值

**解决方案：**

1. **检查参数名拼写**
   ```bash
   # 查看配置文件
   cat config.json | jq .paramNames
   ```

2. **确认参数名完全一致**
   - 包括空格、大小写
   - 中文参数名注意编码

3. **测试模式验证**
   ```bash
   python3 bazhuayu-webhook.py test
   # 查看实际发送的参数
   ```

### 8.3 网络连接失败

**错误信息：** 连接超时或无法访问 API

**解决方案：**

1. **检查网络连通性**
   ```bash
   curl -I https://api-rpa.bazhuayu.com/
   ```

2. **检查防火墙设置**
   ```bash
   # 确保 443 端口开放
   sudo ufw allow 443/tcp
   ```

3. **检查代理设置**
   ```bash
   # 如有代理，配置环境变量
   export https_proxy=http://your-proxy:port
   ```

### 8.4 Python 环境问题

**错误信息：** `ModuleNotFoundError` 或 `python3: command not found`

**解决方案：**

1. **安装 Python 3**
   ```bash
   # Ubuntu/Debian
   sudo apt install python3 python3-pip
   
   # macOS
   brew install python3
   
   # CentOS/RHEL
   sudo yum install python3
   ```

2. **安装依赖**
   ```bash
   pip3 install requests
   ```

### 8.5 权限问题

**错误信息：** `Permission denied`

**解决方案：**

```bash
# 赋予执行权限
chmod +x bazhuayu-webhook.py
chmod +x bazhuayu-webhook

# 或使用 python3 直接运行
python3 bazhuayu-webhook.py run
```

---

## 📞 技术支持

### 官方文档

- [八爪鱼 RPA 帮助中心](https://rpa.bazhuayu.com/helpcenter)
- [Webhook 触发任务文档](https://rpa.bazhuayu.com/helpcenter/docs/skmvua)
- [API 接口文档](https://rpa.bazhuayu.com/helpcenter/docs/rpaapi)

### 获取帮助

1. 查看本手册的常见问题章节
2. 使用测试模式调试：`python3 bazhuayu-webhook.py test`
3. 查看八爪鱼 RPA 控制台的运行日志
4. 联系 OpenClaw 社区或技能作者

---

## 📝 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0 | 2026-03-07 | 初始版本，支持基础 Webhook 调用 |
| 1.1 | TBD | 计划支持批量任务、异步回调 |

---

**🎉 祝你使用愉快！如有问题欢迎反馈。**
