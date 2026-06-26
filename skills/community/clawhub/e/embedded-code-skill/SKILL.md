---
name: embedded-code-skill
description: "Generate, rewrite, or review embedded C code. Use when creating/rewriting/reviewing embedded C for microcontrollers, drivers, firmware. Triggers automatically when user mentions: generate, create, write code, implement driver, rewrite, refactor, review, check, audit."
user-invocable: true
---

# Embedded C 代码生成规范

## 概述

本规范用于生成生产级嵌入式 C 代码，适用于 STM32、PowerPC、RISC-V 等平台。

**核心原则**: 像嵌入式软件架构师一样思考，生成可演进、可测试、可移植的代码。

---

## 思维方式

生成代码时必须以**嵌入式软件架构师**的思维进行:

| 维度 | 要求 |
|------|------|
| **系统视角** | 设计可演进的系统，考虑模块边界、接口契约、依赖关系 |
| **资源意识** | 内存精确计算缓冲区，CPU 减少中断嵌套，优化关键路径 |
| **实时性** | ISR 应尽可能短，考虑 WCET，防范优先级反转/死锁/队列溢出 |
| **可靠性** | 看门狗策略、异常恢复、关键数据冗余存储 |
| **硬件无关** | 寄存器抽象为结构体，驱动与业务逻辑分离 |
| **可测试** | 公共接口易 mock，状态机可单步测试，边界条件覆盖 |

---

## 编码规范

### 1. 类型规范

| 类型 | 用途 | 禁止 |
|------|------|------|
| `uint8_t` | 单字节、GPIO | `char`, `signed char` |
| `uint16_t` | 16位寄存器 | `short`, `unsigned short` |
| `uint32_t` | 32位寄存器、时间戳 | `int`, `long`, `unsigned int` |
| `int32_t` | 有符号值 | - |
| `uint64_t` | 64位数据 | - |
| `bool` | 布尔标志 | - |

**必须包含的头文件:**
```c
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
```

### 2. 命名规范

| 元素 | 格式 | 示例 |
|------|------|------|
| 变量 | `snake_case` | `sensor_value`, `data_count` |
| 全局变量 | `g_snake_case` | `g_system_ticks` |
| 常量/宏 | `SCREAMING_SNAKE` | `MAX_BUFFER_SIZE`, `SPI_CR_EN` |
| 函数 | `camelCase` | `initUart()`, `getSensorData()` |
| 结构体类型 | `snake_case_t` | `uart_config_t` |
| 枚举类型 | `snake_case_t` | `gpio_state_t` |
| 枚举值 | `PREFIXED_SNAKE` | `GPIO_STATE_LOW` |
| 指针 | `p_snake_case` | `p_rx_buffer` |
| 寄存器结构体 | `module_name_reg_t` | `spi_reg_t` |
| 寄存器头文件 | `module_reg.h` | `spi_reg.h` |

### 3. 错误处理

所有 public 函数必须:

1. 返回 `embedded_code_status_t` 枚举类型
2. 验证所有输入指针（NULL 检查）
3. 返回具体错误码

```c
typedef enum {
    EmbedCode_Ok = 0,
    EmbedCode_ErrNullPtr = -1,
    EmbedCode_ErrInvalidArg = -2,
    EmbedCode_ErrTimeout = -3,
    EmbedCode_ErrBusy = -4,
    EmbedCode_ErrNotInit = -5
} embedded_code_status_t;

#define VALIDATE_NOT_NULL(ptr) \
    do { if ((ptr) == NULL) return EmbedCode_ErrNullPtr; } while(0)
```

### 4. 注释规范

**注释语言: 优先使用中文**

| 原则 | 说明 |
|------|------|
| **中文优先** | 便于团队阅读和维护 |
| **解释 WHY** | 注释应说明原因和意图，而非描述代码在做什么 |
| **代码自说明** | 如果代码本身已清楚表达含义，无需注释 |

**Doxygen 文件头格式:**
```c
/**
 * @file spi_reg.h
 * @brief SPI 寄存器结构体定义
 * @author Claude Code
 * @date 2026-04-10
 */
```

**行内注释示例:**
```c
config |= SPI_CR_EN_MASK;  /* 启用 SPI，低电平有效 */
```

### 5. 寄存器结构体定义

**每个外设模块必须有独立的 reg.h 文件:**

| 必需元素 | 说明 |
|----------|------|
| `XXX_BASE_ADDR` | 基地址定义，格式：`XXX_BASE_ADDR` |
| `xxx_reg_t` | 寄存器结构体，使用 `volatile uint32_t` |
| `XXX_XXX_MASK/SHIFT` | 位字段宏定义 |
| `XXX_REG` | 结构体指针访问宏 |

**reg.h 模板:**
```c
/**
 * @file spi_reg.h
 * @brief SPI 外设寄存器定义
 */
#ifndef SPI_REG_H
#define SPI_REG_H

#include <stdint.h>

/* 基地址 */
#define SPI_BASE_ADDR  (0xA0010000U)

/* 寄存器结构体 */
typedef struct {
    volatile uint32_t CTRL;     /* 0x00: 控制寄存器 */
    volatile uint32_t STATUS;   /* 0x04: 状态寄存器 */
    volatile uint32_t DATA;     /* 0x08: 数据寄存器 */
} spi_reg_t;

/* 位字段定义 */
#define SPI_CTRL_EN_MASK      (1U << 0)
#define SPI_CTRL_MODE_MASK    (3U << 2)

/* 寄存器访问 */
#define SPI_REG  ((spi_reg_t *) SPI_BASE_ADDR)

#endif /* SPI_REG_H */
```

### 6. 寄存器赋值规范

**禁止直接赋字面值，必须使用已定义的宏:**

```c
// ❌ 错误
SPI_REG->CTRL = 0x47U;
SPI_REG->BAUD = 250U;

// ✅ 正确
SPI_REG->CTRL = SPI_CTRL_INIT_VAL;
SPI_REG->BAUD = SPI_BAUD_DIV;
```

### 7. 安全编码

| 禁止 | 必须 |
|------|------|
| `malloc`, `free`, `calloc`, `realloc` | 固定大小缓冲区 |
| `new`, `delete` | 环形缓冲区用于数据流 |
| VLA (变长数组) | 精确计算的缓冲区大小 |

```c
#define BUFFER_SIZE 256U
uint8_t buffer[BUFFER_SIZE];
```

### 8. 数据结构

| 场景 | 方式 |
|------|------|
| 相关配置数据 | `struct` |
| 相关常量集合 | `enum` |
| 相关状态数据 | `struct` |

```c
/* 配置结构体 */
typedef struct {
    uint32_t base_address;
    uint16_t interrupt_priority;
    bool     enable_dma;
} peripheral_config_t;

/* 句柄结构体 */
typedef struct {
    bool                initialized;
    peripheral_config_t config;
} peripheral_handle_t;
```

---

## 工作模式

### GENERATE 模式

直接应用本规范生成代码，无需保留任何旧代码。

### REWRITE 模式

**核心原则: 功能流程优先**

> ⚠️ 用户提供的源代码代表着原有的功能实现流程。即使代码有错误，在修改前必须先完整理解其功能流程，再进行符合规范的改写。不得为符合规范而破坏原有的功能流程。

**执行步骤:**

| 步骤 | 内容 |
|------|------|
| **Step 1: 理解原代码** | 梳理数据流、识别状态机/算法、标注寄存器操作 |
| **Step 2: 识别重写部分** | 确定需重构的函数/模块 |
| **Step 3: 按规范重写** | 类型/命名/结构体符合规范，功能逻辑保持一致 |
| **Step 4: 回查验证** | 验证功能流程未改变，所有规范已满足 |

**关于原代码中的 bug：**
- 原代码的 bug 属于"功能流程"的一部分
- 如果 bug 是用户期望保留的行为（如已知的工作around），保持原样
- 如果原代码有语法错误无法编译，标注问题但不擅自修复
- 除非用户明确要求，否则不修改原代码的功能逻辑

### REVIEW 模式

检查现有代码是否符合嵌入式 C 规范。

**执行步骤:**

| 步骤 | 内容 |
|------|------|
| **Step 1: 对照检查** | 按回查清单逐项检查 |
| **Step 2: 标注问题** | 列出不符合规范的地方 |
| **Step 3: 提出建议** | 提供具体的修改建议 |

---

## 项目文件结构

```
project/
├── inc/
│   ├── module_reg.h      # 寄存器结构体定义（每个外设必须有）
│   ├── module_config.h   # 配置参数
│   └── module.h          # 公共接口
└── src/
    └── module.c          # 实现
```

---

## PDCA 工作流

```
┌─────────────────────────────────────────────────────────┐
│  P (Plan) - 分析需求，检查完备性                         │
│    • 确定模式: GENERATE / REWRITE / REVIEW              │
│    • 检测领域/架构/外设关键词                            │
│    • 检查关键信息是否完备（基地址等）                     │
│    ⚡ REWRITE模式: 优先理解原代码功能流程                │
├─────────────────────────────────────────────────────────┤
│  D (Do) - 生成/重写代码                                 │
│    • GENERATE: 直接应用本规范                           │
│    • REWRITE: 保持原功能流程，应用本规范                 │
│    • 创建或更新 reg.h 寄存器结构体定义                   │
│    • 生成符合规范的代码                                  │
├─────────────────────────────────────────────────────────┤
│  C (Check) - 回查验证                                   │
│    • 对照回查清单逐项检查                               │
│    • 验证寄存器结构体定义是否正确                        │
│    ⚡ REWRITE模式: 验证功能流程是否保持一致             │
├─────────────────────────────────────────────────────────┤
│  A (Act) - 修正输出                                     │
│    • 修正所有发现的问题                                  │
│    • 重新回查确认                                       │
│    • 输出合格代码                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 回查清单

生成后必须逐项检查:

| # | 检查项 | 不合格则修正 |
|---|--------|------------|
| 1 | 是否有对应的 reg.h 文件? | 创建 reg.h |
| 2 | 寄存器是否用 `volatile uint32_t` 结构体定义? | 重构为结构体 |
| 3 | 位字段是否有宏定义 (MASK/SHIFT)? | 添加位字段宏 |
| 4 | 类型是否仅用 stdint.h? | 替换所有非标准类型 |
| 5 | 命名是否符合规范表? | 修正所有命名 |
| 6 | 所有 public 函数有错误处理? | 添加状态返回 |
| 7 | 无任何 malloc/free/VLA? | 替换为固定缓冲区 |
| 8 | 注释是否使用中文? | 重写注释 |
| 9 | 文件头是否完整 (Doxygen)? | 添加 Doxygen |
| 10 | 生成的代码是否符合规范? | 修正生成代码 |
| ⚡ 11 | REWRITE 模式: 原代码的功能流程是否保持一致? | 确保数据流/状态机/算法逻辑不变 |
| ⚡ 12 | 寄存器赋值是否都使用宏? | 添加宏定义，禁止字面值赋值 |

---

## 常见错误

### 错误 1: 寄存器定义散落各处

```c
// ❌ 错误
#define SPI_CTRL_ADDR  (*(volatile uint32_t *)0xA0010000)
void spiInit(void) { SPI_CTRL_ADDR = 0x47; }

// ✅ 正确 - 独立的 reg.h，统一的命名风格
#include "spi_reg.h"
void spiInit(void) { SPI_REG->CTRL = SPI_CTRL_INIT_VAL; }
```

### 错误 2: 魔法数字

```c
// ❌ 错误 - 含义不清
if (SPI_REG->STATUS & 0x04) { }
SPI_REG->CTRL |= (1U << 7);

// ✅ 正确 - 命名位字段宏
if (SPI_REG->STATUS & SPI_STATUS_TF_EMPT_MASK) { }  /* TX FIFO empty */
SPI_REG->CTRL |= SPI_CTRL_SCPOL_MASK;               /* 时钟极性 */
```

### 错误 3: 使用 `__I`/`__IO` 前缀

```c
// ❌ 错误 - ARM CMSIS 特有，不具可移植性
typedef struct {
    __I uint32_t DATA;
    __IO uint32_t CTRL;
} spi_reg_t;

// ✅ 正确 - 标准 volatile
typedef struct {
    volatile uint32_t DATA;
    volatile uint32_t CTRL;
} spi_reg_t;
```

### 错误 4: 直接赋字面值

```c
// ❌ 错误 - 魔法数字
SPI_REG->BAUD = 250U;
SPI_REG->CTRL = 0x08U;

// ✅ 正确 - 使用宏定义
SPI_REG->BAUD = SPI_BAUD_DIV;
SPI_REG->CTRL = SPI_CTRL_INIT_VAL;
```

---

## 输出格式

GENERATE 模式输出每个外设模块:

```
module/
├── module_reg.h    # 寄存器结构体定义
├── module.h        # 公共接口
└── module.c       # 实现
```
