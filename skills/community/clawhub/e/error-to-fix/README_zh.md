# Error To Fix

[English](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-1.0-blue)

> 用通俗语言解释编程错误 — 根因、修复方法、预防措施

## 解决什么问题

错误消息是加密的，用户被卡住了。这个技能解析错误/堆栈跟踪，识别错误类型，用通俗语言解释发生了什么，并给出最小针对性的修复——不是重写，只是正确的解决方案。

**触发条件：** 错误消息、堆栈跟踪或异常 + 解释/修复/解决意图。

## 功能特性

- **错误类型分类** — SyntaxError、TypeError、ImportError、ConnectionError 等 8+ 种错误类型，各有特定诊断策略
- **根因识别** — 超越表面症状，解释实际的失败机制
- **最小针对性修复** — 提供最小必要变更，不重写整个文件
- **预防措施** — 每个错误类型一条可操作实践，避免再次发生 |

## 快速开始

```bash
# 通过 ClawHub 安装
clawhub install error-to-fix

# 或手动复制
cp -r error-to-fix ~/.openclaw/skills/
```

### 使用方法

```
/error-to-fix
```

粘贴错误消息或堆栈跟踪，问哪里出了问题以及如何修复。

```
/error-to-fix/root-cause
```

更深入分析——系统级根因，不仅仅是表面症状。

```
/error-to-fix/prevent
```

关注模式和实践，长期避免此错误。

## 工作模式

| 模式 | 说明 |
|------|------|
| `/error-to-fix` | 解释错误 + 提供修复 |
| `/error-to-fix/root-cause` | 系统级根因分析 |
| `/error-to-fix/prevent` | 预防模式和实践 |

## 示例

| 错误 | 解释 |
|-------|-------------|
| Python TypeError | "TypeError: list.append 期望 str，得到 int——在输入外加 `str()` 转换" |
| Node ModuleNotFoundError | "ModuleNotFoundError: 'requests' 不在 requirements.txt——运行 `pip install requests`" |
| React "undefined is not an object" | "`props.user.address` 在 `user` 设置前被访问。添加守卫：`props.user?.address`" |
| Connection refused | "ECONNREFUSED：localhost:5432 上的服务器不接受连接。PostgreSQL 在运行吗？" |

## 目录结构

```
error-to-fix/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # 错误分类、堆栈跟踪模式、修复速查表
└── tests/
```

## 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。