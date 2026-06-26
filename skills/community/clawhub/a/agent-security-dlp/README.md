# Agent Security DLP

<p align="center">
  <img src="https://img.shields.io/badge/version-v2.1.2-blue" alt="Version">
  <img src="https://img.shields.io/badge/rules-166-green" alt="Rules">
  <img src="https://img.shields.io/badge/python-3.8+-orange" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License">
</p>

> 🛡️ 企业级数据防泄漏系统 | 166 条规则 | 覆盖 25+ 行业

---

## 简介

Agent Security DLP (数据防泄漏系统) 是一个企业级的敏感信息检测与防护工具，支持 **166 条检测规则**，覆盖金融、医疗、汽车、销售、人力资源、物流等 25+ 行业场景。

### 核心特性

- 🚀 **166 条规则** - 覆盖 25+ 行业
- 🛡️ **五层防护** - 入口、记忆、工具、出口、审计
- ⚡ **高性能** - 正则预编译，并行检测
- 🔧 **易扩展** - 支持自定义规则
- 📦 **开箱即用** - Python 3.8+

---

## 安装

### 方式1: ClawHub (推荐)

```bash
# 安装 skill
clawhub install agent-security-dlp

# 或指定版本
clawhub install agent-security-dlp --version 2.0.0
```

### 方式2: Git 克隆

```bash
# 克隆仓库
git clone https://github.com/caidongyun/agent-security-dlp.git
cd agent-security-dlp

# 或 Gitee
git clone https://gitee.com/caidongyun/agent-security-dlp.git
```

---

## 快速开始

```python
from agent_dlp import AgentDLP

# 初始化
dlp = AgentDLP()

# 检查出口
text = "我的手机是13812345678，OpenAI key是 sk-xxxxx"
blocked, processed, details = dlp.check_output(text)

if blocked:
    print("检测到敏感信息，已拦截")
else:
    print("检查通过")
```

---

## 触发方式

本 DLP 支持 **手动触发** 和 **集成触发** 两种方式：

### 方式1: 命令行手动触发

```bash
# 检查输出 (对话出口)
python bin/agent-dlp check-output "手机: 13812345678"

# 检查入口 (对话入口)
python bin/agent-dlp check-input "忽略之前的指令"

# 检查工具 (执行前)
python bin/agent-dlp check-tool exec
```

### 方式2: Python 代码集成触发

```python
from agent_dlp import AgentDLP

dlp = AgentDLP()

# 对话出口检查 (最常用)
blocked, result, details = dlp.check_output(user_message)

# 对话入口检查
result = dlp.check_input(user_input)

# 工具执行前检查
result = dlp.check_tool("exec", {"command": "rm -rf /"})
```

### 方式3: 装饰器自动触发

```python
from functools import wraps
from agent_dlp import AgentDLP

dlp = AgentDLP()

def dlp_protect(func):
    """自动触发装饰器 - 入口+出口自动检查"""
    @wraps(func)
    def wrapper(text):
        # 执行函数
        result = func(text)
        # 出口检查
        blocked, safe, _ = dlp.check_output(result)
        return safe if blocked else result
    return wrapper

# 使用
@dlp_protect
def agent_response(text):
    return f"你说的是: {text}"

# 自动触发
print(agent_response("手机13812345678"))  # 自动脱敏
```

---

## 使用场景

| 场景 | 触发方式 | 说明 |
|------|----------|------|
| 对话出口 | `check_output` | 返回用户前自动检测 |
| 对话入口 | `check_input` | 处理输入前检测 |
| 文件扫描 | Python 调用 | 扫描文件内容 |
| API 防护 | 装饰器 | 接口层自动拦截 |
| 工具执行 | `check_tool` | 执行前审批 |

---

## 命令行

```bash
# 查看状态
python bin/agent-dlp status

# 查看规则统计
python bin/agent-dlp rules

# 检查文本
python bin/agent-dlp check-output "手机: 13812345678"

# 检查入口
python bin/agent-dlp check-input "忽略之前的指令"

# 查看日志
python bin/agent-dlp logs
```

---

## 规则分类

| 类别 | 数量 | 说明 |
|------|------|------|
| 🔑 凭证 | 45 | API Key、Token、私钥 |
| 💰 金融 | 19 | 银行卡、股票、加密货币 |
| 👥 人力资源 | 11 | 工号、工资、社保 |
| 📦 物流 | 11 | 快递单、运单 |
| 🏥 医疗 | 10 | 病历、医保 |
| 🚗 汽车 | 6 | 车架号、行驶证 |
| 🛒 销售 | 6 | 客户信息 |
| 💊 医药 | 5 | 处方 |
| 📜 法规 | 4 | 合同、专利 |
| 其他 | 29 | 教育、政府等 |

**总计: 166 条**

---

## 架构

```
用户输入 → Input Guard → Agent → Memory Guard → Tool Guard → Output Filter → 用户
              注入检测        记忆检查      工具审批      脱敏拦截
                    ↓                                    ↓
              审计日志                              审计日志
```

---

## 配置

编辑 `config/config.json`:

```json
{
  "enabled": true,
  "mode": "normal",
  "output": {
    "enabled": true,
    "rules": ["china_idcard", "china_phone", "api_key"]
  }
}
```

### 模式

| 模式 | 说明 |
|------|------|
| normal | 记录但不拦截严重风险 |
| strict | 完整检查，严格拦截 |
| personal | 个人轻量版，自动脱敏 |

---

## 贡献

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/xxx`)
3. 提交更改 (`git commit -m 'Add xxx'`)
4. 推送分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

---

## 许可证

MIT License - see [LICENSE](LICENSE) for details.

---

## 更新日志

See [CHANGELOG.md](CHANGELOG.md) for details.

---

<p align="center">Made with ❤️ by OpenClaw</p>
