---
name: embed-code-arch
description: Architecture patterns for ARM Cortex-M, ARM Cortex-A, PowerPC, SPARC V8, RISC-V. Memory barriers, interrupt handling, register access.
---

# Architecture Patterns

## ARM Cortex-M (MCU)

```c
/* NVIC */
#define NVIC_BASE   0xE000E100U
#define NVIC_ISER(n) (*(volatile uint32_t *)(NVIC_BASE + (n) * 4U))

#define NVIC_ENABLE_IRQ(irq)  do { NVIC_ISER((irq) >> 5) = (1U << ((irq) & 0x1F)); } while(0)

/* Memory barriers */
__DMB(); __DSB(); __ISB();

/* ISR */
void __attribute__((interrupt)) TIM2_IRQHandler(void) {
    volatile uint32_t *irq_flag = (uint32_t *)(TIM2_BASE + FLAG_OFFSET);
    *irq_flag = 0U;
    g_ticks++;
    __DSB();
}
```

## ARM Cortex-A (SoC)

```c
/* GIC */
#define GICD_BASE  0x1E001000U
#define GICC_BASE  0x1E000000U

/* SMP barrier */
__asm volatile ("dmb ish" ::: "memory");

/* Cache */
__asm volatile ("ic iallu" ::: "memory");
```

## PowerPC (SoC)

```c
/* SPR access */
static inline uint32_t mfspr(uint16_t spr) {
    uint32_t val;
    __asm volatile ("mfspr %0, %1" : "=r"(val) : "K"(spr));
    return val;
}

/* Barrier */
__asm volatile ("msync");
```

## SPARC V8 (Leon3)

```c
/* PSR */
static inline uint32_t sparc_get_psr(void) {
    uint32_t psr;
    __asm volatile ("rd %%psr, %0" : "=r"(psr));
    return psr;
}

/* Barrier */
__asm volatile ("stbar");
```

## RISC-V

```c
/* CSR */
#define CSR_MSTATUS 0x300
#define CSR_MIE     0x304

static inline uint32_t csrr(uint32_t csr) {
    uint32_t val;
    __asm volatile ("csrr %0, %1" : "=r"(val) : "K"(csr));
    return val;
}

/* Barrier */
__asm volatile ("fence" ::: "memory");
```

## Quick Ref

| Arch | Barrier | Interrupt | SPR/CSR |
|------|---------|-----------|---------|
| Cortex-M | `__DMB()` | NVIC | N/A |
| Cortex-A | `dmb ish` | GIC | N/A |
| PowerPC | `msync` | PIC | `mfspr` |
| SPARC V8 | `stbar` | INTC | `rd psr` |
| RISC-V | `fence` | PLIC | `csrr` |

## 未知架构处理

如果用户提到的架构不在上述列表中:

### 处理步骤

1. **先尝试推断**: 根据用户描述推断架构类型
2. **尝试网上搜索**: 如果是未知架构,使用WebSearch/WebFetch搜索该架构的基础信息
3. **使用通用模式**: 如果无法找到信息,使用通用嵌入式C模式
4. **与用户沟通**: 把学到的架构信息反馈给用户,确认理解是否正确

### 网上搜索流程

当遇到未知架构时:

```
1. 使用 WebSearch 搜索: "<架构名> embedded C programming"
2. 使用 WebSearch 搜索: "<架构名> register map memory"
3. 使用 WebFetch 获取该架构的官方文档或芯片手册摘要
4. 分析搜索结果,提取:
   - 寄存器访问模式
   - 中断处理方式
   - 内存屏障指令
   - 工具链信息
5. 把学到的信息反馈给用户确认
```

### 搜索示例

| 用户提到 | 搜索关键词 |
|----------|-----------|
| MIPS | "MIPS embedded C interrupt controller" |
| ARC | "ARC EM or ARC HS interrupt handling" |
| Tensilica | "Tensilica Xtensa register access" |
| Andes | "Andes RISC-V interrupt" |

### 与用户沟通格式

```markdown
🤖 **已搜索并学习该架构**

根据搜索结果,我了解到该架构的一些基础信息:

| 特性 | 信息 |
|------|------|
| 内存屏障 | 搜索到的指令 |
| 中断方式 | 搜索到的信息 |
| 寄存器访问 | 搜索到的模式 |

**请确认以下理解是否正确:**
1. ...
2. ...

如果信息有误,请纠正或提供正确的信息。
```

### 通用模式 (所有架构可用)

```c
/* 通用寄存器定义 - 架构无关 */
#define REG32(base, offset)  (*(volatile uint32_t *)((base) + (offset)))

/* 通用内存屏障 - 编译器级别 */
#define MEMORY_BARRIER()  __asm volatile("" ::: "memory")

/* 通用中断使能宏 - 假设架构提供 */
#define ENABLE_INTERRUPTS()  /* 架构特定实现 */
#define DISABLE_INTERRUPTS() /* 架构特定实现 */

/* 通用volatile指针类型 */
typedef volatile uint32_t *reg_ptr_t;
```

### 提醒用户格式

```markdown
⚠️ **架构信息待确认**

您提到的架构不在已知列表中。

为了生成正确的代码,请提供:
1. 架构类型 (如 MIPS, ARC, Tensilica等)
2. 内存屏障指令
3. 中断控制器类型
4. 寄存器基地址

或者:
- 提供该架构的代码片段作为参考
- 说明与已知架构的相似之处
```

### 常见架构归类 (供参考)

以下是基于常见芯片的架构归类,但**不保证完全准确**:

| 常见芯片 | 架构 |
|----------|------|
| STM32系列 | ARM Cortex-M |
| NXP LPC, Kinetis | ARM Cortex-M |
| GD32 | ARM Cortex-M (兆易创新,兼容STM32) |
| i.MX6, i.MX7, STM32MP | ARM Cortex-A |
| MPC5748, QorIQ | PowerPC |
| FE310, SiFive | RISC-V |

**重要: 如果芯片不在列表中,不要猜测架构,请用WebSearch搜索确认。**
