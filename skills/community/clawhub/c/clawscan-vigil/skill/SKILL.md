---
name: clawscan-vigil
description: 安装前扫描 OpenClaw Skill 安全风险，静态+动态双重检测，识别恶意代码
version: 0.2.0
author: ClawScan Team
metadata:
  openclaw:
    emoji: 🛡️
    homepage: https://github.com/clawscan/clawscan-vigil
    os: [linux, macos, windows]
    requires:
      bins: [python3, pip]
tags: [security, safety, scanning, skill-analysis, malware-detection]
---

# Skill: clawscan-vigil

**🔍 OpenClaw Skill 安全扫描器**

安装前扫描任意 Skill 的安全风险，静态 + 动态双重检测。

---

## 为什么需要 ClawScan？

- **341 个恶意 Skill** 已被发现可窃取 API Key、加密货币钱包
- ClawHub 审核机制薄弱，**12% Skill 存在恶意行为**
- 安装前无法判断代码安全性

---

## 版本对比

| 功能 | 免费版 | Premium |
|------|--------|---------|
| 静态代码分析 | ✅ | ✅ |
| 动态行为检测 | ✅ | ✅ |
| 扫描次数 | 5次/月 | 无限 |
| 依赖风险分析 | ❌ | ✅ |
| 批量扫描 | ❌ | ✅ |
| 优先支持 | ❌ | ✅ |
| 价格 | 免费 | ¥49/年 |

---

## 快速开始

```bash
# 安装
clawhub install clawscan

# 查看配额状态
clawscan status

# 扫描本地 Skill（消耗1次配额）
clawscan scan /path/to/skill

# 扫描已安装的 ClawHub Skill
clawscan check mcp-server-prompts

# 详细报告
clawscan scan /path/to/skill --verbose

# JSON 输出（用于脚本集成）
clawscan scan /path/to/skill --json
```

---

## 激活 Premium

```bash
# 获取 License: https://clawscan.dev
clawscan activate CLAW-XXXX-XXXX-XXXX

# 确认激活
clawscan status
```

---

## 风险分级

| 等级 | 图标 | 描述 |
|------|------|------|
| 🔴 高危 | HIGH | 网络请求、文件写入、命令执行 |
| 🟡 中危 | MEDIUM | 子进程导入、API Key 处理 |
| 🟢 低危 | LOW | 纯计算逻辑 |

---

## 示例输出

```
╭────────────────────────── Scan Summary ──────────────────────────╮
│ 🔴 malicious-skill                                               │
│                                                                  │
│ Overall Risk: HIGH                                               │
│ Files Scanned: 3                                                 │
│ Scan Duration: 15ms                                              │
│                                                                  │
│ Findings: 8 total                                                │
│   🔴 High: 4                                                     │
│   🟡 Medium: 3                                                   │
│   🟢 Low: 1                                                      │
╰──────────────────────────────────────────────────────────────────╯

🔴 HIGH RISK (4)
==================================================

network
  Network module imported: requests
  /skill/malicious.py:7

📦 Dependency Analysis (Premium)
==================================================
🔴 pyautogui (Potential keylogger/screenshot capability)
🟡 psutil (System access capabilities)

📋 Recommendations
==================================================
  🚨 This Skill can execute system commands...
```

---

## 退出码

| Code | 含义 |
|------|------|
| 0 | 低危 |
| 1 | 高危风险 |
| 2 | 中危风险 |
| 3 | 扫描错误 |
| 4 | 配额已用完 |

---

## 技术细节

**静态分析**：
- AST 解析识别危险函数
- 7 类风险模式匹配（网络、文件、子进程、加密等）

**动态分析**：
- RestrictedPython 沙箱执行
- 监控运行时导入和调用

**依赖分析** (Premium)：
- 扫描 requirements.txt / pyproject.toml
- 识别已知风险包（pyautogui, browser-cookie3 等）

---

## 隐私说明

- 扫描完全本地执行，代码不会上传
- License 验证可选离线模式
- 不收集 Skill 内容或扫描结果

---

## 支持与反馈

- 问题反馈：https://github.com/yourname/clawscan/issues
- 获取 License：https://clawscan.dev
- 邮件：support@clawscan.dev

---

**License**: MIT (Tool) + Commercial (Premium Features)
