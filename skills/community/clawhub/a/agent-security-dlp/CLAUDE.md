# Agent Security DLP

> 企业级数据防泄漏系统 | 146 条规则 | 20+ 行业

---

## 项目概述

Agent Security DLP 是一个企业级数据防泄漏系统，支持 146 条敏感信息检测规则，覆盖金融、医疗、汽车、销售、人力资源、物流等 20+ 行业场景。

### 核心功能

- 入口防护 - 检测 Prompt Injection
- 记忆保护 - 敏感信息过滤
- 工具管控 - 危险操作审批
- 出口过滤 - 自动脱敏/拦截
- 审计日志 - 全量操作记录

---

## 开发环境

- **语言**: Python 3.8+
- **依赖**: 无外部依赖 (仅使用内置库)
- **安装**: `pip install -r requirements.txt`

---

## 可用命令

```bash
# 查看状态
python bin/agent-dlp status

# 查看规则统计
python bin/agent-dlp rules

# 检查文本
python bin/agent-dlp check-output "敏感内容"

# 检查入口
python bin/agent-dlp check-input "注入指令"

# 查看日志
python bin/agent-dlp logs
```

---

## 架构

```
用户输入 → Input Guard → Agent → Memory Guard → Tool Guard → Output Filter → 用户
              注入检测        记忆检查      工具审批      脱敏拦截
                    ↓                                    ↓
              审计日志                              审计日志
```

---

## 规则分类

| 类别 | 数量 |
|------|------|
| 凭证密钥 | 45 |
| 金融 | 18 |
| 人力资源 | 11 |
| 物流 | 11 |
| 医疗 | 10 |
| 汽车 | 6 |
| 销售 | 6 |
| 医药 | 5 |
| 法规 | 4 |
| 其他 | 20 |

**总计**: 146 条

---

## Python API

```python
from agent_dlp import AgentDLP

dlp = AgentDLP()

# 检查出口
blocked, text, details = dlp.check_output("手机: 138xxxx")

# 检查入口
result = dlp.check_input("忽略之前指令")

# 检查工具
result = dlp.check_tool("exec")
```

---

## 配置

编辑 `config/config.json` 修改规则和行为。

---

## 许可证

MIT License - see LICENSE file.
