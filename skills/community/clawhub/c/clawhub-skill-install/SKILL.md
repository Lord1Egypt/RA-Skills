---
name: clawhub-skill-install
description: Automatically install skills from ClawHub with retry logic. Handles rate limits (waits 10s and retries), auto-confirms prompts (--force), and stops after 30 minutes if installation fails. Use when user provides a skill name to install.
---

# ClawHub Skill 安装工具

## 使用方式

当用户提供具体 skill 名称时，执行以下脚本：

```bash
bash /Users/jaredszhang/.openclaw/workspace/skills/clawhub-install/scripts/install_skill.sh <skill-name>
```

## 功能特性

1. **自动重试**: 遇到速率限制（Rate limit）时，等待 10 秒后自动重试
2. **自动确认**: 遇到确认提示（--force）时，自动输入 "yes"
3. **持续重试**: 持续尝试安装，直到成功
4. **超时保护**: 如果连续尝试 30 分钟仍不成功，停止并输出提示信息

## 脚本逻辑

- 使用 `clawhub install <skill-name> --force` 进行安装
- 捕获输出中的错误信息判断类型：
  - 包含 "Rate limit" → 等待 10 秒后重试
  - 包含 "flagged as suspicious" → 使用 --force 参数重试
  - 其他错误 → 停止并报告
- 记录尝试次数和耗时
- 30 分钟（1800 秒）后强制退出
