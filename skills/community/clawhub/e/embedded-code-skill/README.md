# embedded-code-skill

> 嵌入式 C 代码生成规范 — 统一团队代码风格，生成生产级驱动代码

<!-- Language Switcher -->
[简体中文](README.md) · [English](README_EN.md) · [日本語](README_JP.md)

---

[![Platform: Claude Code | VS Code | Cursor | OpenClaw | Hermes Agent](https://img.shields.io/badge/Platform-Claude%20Code%20%7C%20VS%20Code%20%7C%20Cursor%20%7C%20OpenClaw%20%7C%20Hermes%20Agent-blue)]()
[![Standard: MISRA-C Compliant](https://img.shields.io/badge/Standard-MISRA--C%20Compliant-green)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)]()

---

## 特性

- **三种工作模式** — GENERATE（生成）、REWRITE（重写）、REVIEW（审查）
- **生产级代码** — 像嵌入式软件架构师一样思考，生成可演进、可测试的代码
- **多平台支持** — STM32 (Cortex-M)、PowerPC、RISC-V、ARM Cortex-A
- **团队统一** — 代码风格一致，review 有据可依
- **自我进化** — 内置达尔文式优化系统，持续改进规范质量

---

## 快速开始

```bash
/embedded-code-skill 生成一个STM32 UART驱动，基地址 0x4000C000
/embedded-code-skill 重写这段代码为符合规范的版本
/embedded-code-skill 审查这段代码是否符合规范
```

---

## 三种工作模式

### GENERATE 模式

直接应用规范生成代码，无需保留任何旧代码。

### REWRITE 模式

**核心原则: 功能流程优先**

- 用户提供的源代码代表着原有的功能实现流程
- 即使代码有错误，也必须先完整理解其功能流程再改写
- 不得为符合规范而破坏原有的功能逻辑
- 原代码的 bug 属于"功能流程"的一部分，默认保持原样

### REVIEW 模式

检查现有代码是否符合嵌入式 C 规范，按回查清单逐项检查并提出修改建议。

---

## 核心要求

| 要求 | 规范 |
|------|------|
| **可读性** | `snake_case` / `SCREAMING_SNAKE` / `camelCase` 命名，Doxygen 注释，中文优先 |
| **可移植性** | `stdint.h` 类型，`volatile` 寄存器宏，无 `int`/`char`/`long` |
| **数据结构** | `struct`/`enum` 组织数据，无散落全局变量 |
| **错误处理** | public 函数返回 `embedded_code_status_t`，NULL 检查 |
| **安全编码** | 禁止 `malloc`/`free`/VLA，固定大小缓冲区 |

---

## 生成代码前请提供

| 信息 | 必要性 | 示例 |
|------|--------|------|
| 外设寄存器基地址 | **必需** | `UART_BASE_ADDR = 0x4000C000U` |
| 芯片/架构类型 | 可推断 | `STM32`, `Cortex-M4`, `RISC-V` |

> **注意**: 基地址必须提供，禁止 AI 编造寄存器地址。

---

## 文件结构

```
embedded-code-skill/
├── SKILL.md                     # 斜杠命令入口
├── README.md                    # 本文档
│
├── .evolution/                  # 自我进化系统
│   ├── SKILL.md                # 进化系统主文件
│   ├── test-prompts.json       # 测试用例集
│   ├── results.tsv             # 优化历史记录
│   └── README.md               # 进化系统说明
│
├── embedded-code-skill-standards/        # 编码标准详情
│   └── SKILL.md
│
├── embedded-code-skill-arch/             # 架构模式
│   └── SKILL.md                # Cortex-M/A, PowerPC, RISC-V
│
├── embedded-code-skill-drivers/          # 驱动模板
│   └── SKILL.md                # UART, SPI, I2C, DMA, CAN
│
└── embedded-code-skill-domains/          # 领域规范
    └── SKILL.md                # 航天/军工/工业/汽车
```

---

## 输出格式

GENERATE 模式输出每个外设模块：

```
module/
├── module_reg.h    # 寄存器结构体定义
├── module.h        # 公共接口
└── module.c       # 实现
```

**uart_reg.h 示例:**

```c
/**
 * @file uart_reg.h
 * @brief UART 外设寄存器定义
 */
#ifndef UART_REG_H
#define UART_REG_H

#include <stdint.h>

/* 基地址 */
#define UART_BASE_ADDR  (0x4000C000U)

/* 寄存器结构体 */
typedef struct {
    volatile uint32_t DR;       /* 0x00: Data register */
    volatile uint32_t RSR;      /* 0x04: Receive status register */
    volatile uint32_t Reserved;
    volatile uint32_t FR;       /* 0x18: Flag register */
    volatile uint32_t IBRD;     /* 0x24: Integer baud rate divisor */
    volatile uint32_t FBRD;     /* 0x28: Fractional baud rate divisor */
    volatile uint32_t LCRH;     /* 0x2C: Line control register */
    volatile uint32_t CR;       /* 0x30: Control register */
} uart_reg_t;

/* 寄存器访问 */
#define UART_REG  ((uart_reg_t *) UART_BASE_ADDR)

#endif /* UART_REG_H */
```

---

## 自我进化系统

内置自我优化系统：

- **8维度评估** — 结构质量（60分）+ 实际效果（40分）
- **棘轮机制** — 只保留改进，自动回滚退步
- **子 agent 验证** — 效果维度必须用子 agent 执行
- **人在回路** — 每轮优化后暂停等待用户确认

### 触发进化

```
用户："优化 embedded-code-skill"      → 完整优化流程
用户："评估 embedded-code-skill 质量"  → 仅评估不优化
用户："运行 embedded-code-skill 自我进化" → 自动优化直到确认
```

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 许可

MIT License
