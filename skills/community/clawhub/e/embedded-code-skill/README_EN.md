# embedded-code-skill

> Embedded C Code Generation Specification — Unified team code style, generate production-grade driver code

<!-- Language Switcher -->
[简体中文](README.md) · [English](README_EN.md) · [日本語](README_JP.md)

---

[![Platform: Claude Code | VS Code | Cursor | OpenClaw | Hermes Agent](https://img.shields.io/badge/Platform-Claude%20Code%20%7C%20VS%20Code%20%7C%20Cursor%20%7C%20OpenClaw%20%7C%20Hermes%20Agent-blue)]()
[![Standard: MISRA-C Compliant](https://img.shields.io/badge/Standard-MISRA--C%20Compliant-green)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)]()

---

## Features

- **Three Work Modes** — GENERATE, REWRITE, REVIEW
- **Production-Grade Code** — Think like an embedded software architect, generate evolvable and testable code
- **Multi-Platform** — STM32 (Cortex-M), PowerPC, RISC-V, ARM Cortex-A
- **Team Uniformity** — Consistent code style, review with evidence
- **Self-Evolution** — Built-in Darwin-style optimization system, continuous improvement

---

## Quick Start

```bash
/embedded-code-skill Generate an STM32 UART driver, base address 0x4000C000
/embedded-code-skill Rewrite this code to conform to the specification
/embedded-code-skill Review if this code conforms to the specification
```

---

## Three Work Modes

### GENERATE Mode

Generate code directly using the specification, no need to preserve old code.

### REWRITE Mode

**Core Principle: Function Flow First**

- User-provided source code represents the original functional implementation flow
- Even if code has errors, you must fully understand its functional flow before rewriting
- Never破坏 the original functional logic to conform to the specification
- Bugs in the original code are part of the "functional flow" and are kept by default

### REVIEW Mode

Check if existing code conforms to the Embedded C specification, check item by item against the review checklist and provide modification suggestions.

---

## Core Requirements

| Requirement | Specification |
|------------|----------------|
| **Readability** | `snake_case` / `SCREAMING_SNAKE` / `camelCase` naming, Doxygen comments |
| **Portability** | `stdint.h` types, `volatile` register macros, no `int`/`char`/`long` |
| **Data Structure** | `struct`/`enum` for data organization, no scattered global variables |
| **Error Handling** | Public functions return `embedded_code_status_t`, NULL checks |
| **Safe Coding** | No `malloc`/`free`/VLA, fixed-size buffers |

---

## Required Information Before Code Generation

| Information | Necessity | Example |
|-------------|----------|---------|
| Peripheral register base address | **Required** | `UART_BASE_ADDR = 0x4000C000U` |
| Chip/Architecture type | Inferable | `STM32`, `Cortex-M4`, `RISC-V` |

> **Note**: Base address must be provided, AI must not fabricate register addresses.

---

## File Structure

```
embedded-code-skill/
├── SKILL.md                     # Slash command entry
├── README.md                    # This file (Chinese)
├── README_EN.md                 # English version
├── README_JP.md                 # Japanese version
│
├── .evolution/                  # Self-evolution system
│   ├── SKILL.md                # Evolution system main file
│   ├── test-prompts.json       # Test case set
│   ├── results.tsv            # Optimization history
│   └── README.md               # Evolution system docs
│
├── embedded-code-skill-standards/
│   └── SKILL.md
│
├── embedded-code-skill-arch/
│   └── SKILL.md                # Cortex-M/A, PowerPC, RISC-V
│
├── embedded-code-skill-drivers/
│   └── SKILL.md                # UART, SPI, I2C, DMA, CAN
│
└── embedded-code-skill-domains/
    └── SKILL.md                # Aerospace/Military/Industrial/Automotive
```

---

## Output Format

GENERATE mode outputs each peripheral module:

```
module/
├── module_reg.h    # Register structure definition
├── module.h        # Public interface
└── module.c       # Implementation
```

**uart_reg.h Example:**

```c
/**
 * @file uart_reg.h
 * @brief UART peripheral register definition
 */
#ifndef UART_REG_H
#define UART_REG_H

#include <stdint.h>

/* Base address */
#define UART_BASE_ADDR  (0x4000C000U)

/* Register structure */
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

/* Register access */
#define UART_REG  ((uart_reg_t *) UART_BASE_ADDR)

#endif /* UART_REG_H */
```

---

## Self-Evolution System

Built-in self-optimization system based on Darwin.skill:

- **8-Dimension Evaluation** — Structural quality (60pts) + Actual effect (40pts)
- **Ratchet Mechanism** — Only keep improvements, auto-rollback on regression
- **Sub-agent Verification** — Effect dimensions must use sub-agents
- **Human-in-the-Loop** — Pause after each optimization round for user confirmation

### Trigger Evolution

```
User: "Optimize embedded-code-skill"           → Full optimization flow
User: "Evaluate embedded-code-skill quality"  → Evaluation only
User: "Run embedded-code-skill self-evolution" → Auto-optimize until confirmed
```

---

## Contributing

Issues and Pull Requests are welcome!

---

## License

MIT License
