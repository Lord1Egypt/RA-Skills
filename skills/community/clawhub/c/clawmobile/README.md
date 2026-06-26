# ClawMobile - Android Automation Toolkit

> 完整的企业级 Android 自动化解决方案，深度集成 AutoX.js

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skill Version](https://img.shields.io/badge/Skill%20Version-1.0.0-brightgreen)](https://github.com/clawmobile/clawmobile)
[![AutoX.js](https://img.shields.io/badge/AutoX.js-6.5.5.10%2B-blue)](https://autoxjs.com/)

## 简介

ClawMobile 是一个功能强大的 Android 设备自动化工具包，通过 AutoX.js HTTP 服务器实现完整的设备控制。它将移动自动化、RPA（机器人流程自动化）和 AI 智能决策完美结合。

### 核心特性

- 🎯 **工作流管理** - 创建、执行、调度自动化工作流
- ⏺️ **操作录制** - 录制屏幕操作并生成 AutoX.js 代码
- 🤖 **AI 干预** - 智能异常处理和自动恢复
- 💎 **会员系统** - 三级会员体系（Free/VIP/SVIP）
- 🌐 **HTTP API** - 标准 RESTful API，易于集成
- 📊 **可观测性** - 完整的日志记录和执行追踪

## 快速开始

### 前置条件

- Android 7.0+ 设备
- AutoX.js v6.5.5.10+
- Python 3.7+
- ADB（Android Debug Bridge）

### 安装

```bash
# 通过 ClawHub 安装（推荐）
clawhub install clawmobile

# 或通过 Git Clone
git clone https://github.com/clawmobile/clawmobile.git ~/.openclaw/skills/clawmobile
```

### 配置

1. 在 Android 设备上启动 AutoX.js HTTP 服务器（端口 8765）
2. 配置 ADB 连接：`adb devices`
3. 设置环境变量：
   ```bash
   export CLAWMOBILE_API_URL="http://localhost:8765"
   export CLAWMOBILE_API_TOKEN="your-autox-token"
   ```

### 使用

```python
from skill.client import ClawMobileClient

client = ClawMobileClient()

# 列出工作流
workflows = client.list_workflows()

# 执行工作流
result = client.execute_workflow(
    workflow_id="workflow_001",
    params={"keyword": "春天的风景"}
)

# 开始录制
recording = client.start_recording(
    workflow_id="workflow_001",
    app_package="com.doubao.app"
)
```

## 文档

- [SKILL.md](SKILL.md) - Skill 完整说明和使用指南
- [API-DOCUMENTATION.md](docs/API-DOCUMENTATION.md) - API 参考手册
- [DATA-MODELS.md](docs/DATA-MODELS.md) - 数据模型定义
- [MEMBERSHIP-SYSTEM-GUIDE.md](docs/MEMBERSHIP-SYSTEM-GUIDE.md) - 会员系统指南

## 目录结构

```
clawmobile-skill/
├── SKILL.md              # Skill 元数据和完整指南
├── README.md             # 项目说明（本文件）
├── VERSION               # 版本号
├── CHANGELOG.md          # 变更日志
├── LICENSE               # 许可证
├── skill/                # Skill 实现代码
│   ├── __init__.py
│   ├── api_server.py    # AutoX.js HTTP 服务器
│   ├── client.py        # HTTP API 客户端
│   ├── executor.py      # 任务执行器
│   └── models.py        # 数据模型
├── config/               # 配置文件
│   ├── settings.yaml    # 默认配置
│   └── schema.json      # 配置架构
├── scripts/              # 辅助脚本
│   ├── setup.sh         # 安装脚本
│   ├── validate.sh      # 验证脚本
│   └── test.sh          # 测试脚本
├── docs/                 # 文档目录
├── tests/                # 测试文件
└── assets/               # 资源文件
```

## 功能对比

| 功能 | Free | VIP | SVIP |
|------|------|-----|------|
| 每日运行次数 | 3 | 无限 | 无限 |
| 定时任务 | ❌ | ✅ | ✅ |
| AI 干预 | ❌ | ✅ | ✅ |
| 导入/导出 | ❌ | ✅ | ✅ |
| 自然语言生成 | ✅ | ✅ | ✅ |
| 参数自动决策 | ❌ | ❌ | ✅ |

## API 示例

### 健康检查

```bash
curl http://localhost:8765/api/v1/health
```

### 列出工作流

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8765/workflows
```

### 执行工作流

```bash
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"workflow_id":"workflow_001"}' \
  http://localhost:8765/execute
```

### 开始录制

```bash
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"workflow_id":"workflow_001","app_package":"com.doubao.app"}' \
  http://localhost:8765/recording/start
```

## 开发

### 环境设置

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
python3 -m pytest tests/

# 启动服务器
python3 skill/api_server.py
```

### 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](docs/CONTRIBUTING.md) 了解详情。

## 常见问题

### Q: 如何激活会员？

A: 使用兑换码激活：
```python
client.activate_membership(
    code="C-VENDORCODE-24-01M-A1B2C3D4",
    user_id="user_001"
)
```

### Q: 连接失败怎么办？

A: 检查：
1. AutoX.js 是否运行
2. ADB 连接是否正常：`adb devices`
3. 端口是否正确：`curl http://localhost:8765/api/v1/health`

### Q: 如何调试工作流？

A: 启用调试模式：
```python
result = client.execute_workflow(
    workflow_id="workflow_001",
    debug=True
)
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 支持

- Email: support@clawmobile.com
- GitHub Issues: https://github.com/clawmobile/clawmobile/issues
- 文档: https://docs.clawmobile.com

## 致谢

- [AutoX.js](https://autoxjs.com/) - 强大的 Android 自动化框架
- [OpenClaw](https://openclaw.ai) - AI Agent 框架
- [ClawHub](https://clawhub.ai) - Skills 注册中心

---

**ClawMobile** - 让 Android 自动化更简单 🚀

*README.md v1.0.0 | Last Updated: 2026-03-31*
