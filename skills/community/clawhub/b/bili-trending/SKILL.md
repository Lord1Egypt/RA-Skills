---
name: "bili-trending"
version: "1.2.0"
description: "获取B站Top20榜单，提取标题、摘要和链接。"
user-invocable: true
# 官方调度机制：绕过大模型推理，直接将指令分发给原生工具
command-dispatch: tool
command-tool: bili_fetch_tool
command-arg-mode: raw
---

# 技能介绍
这是一个遵循 OpenClaw 标准 Tool 插件架构的 B 站热榜抓取模块，底层通过 Node.js Bridge 唤起 Python 自动化脚本



## 更新日志 (v1.2.0)
- 修复了Windows环境下终端输出特殊字符（如Emoji）导致的GBK编码报错问题，强制采用UTF-8输出。遵循了openclaw3.23.2版本规范进行了修改
- 遵循了openclaw3.23.2版本规范进行了修改