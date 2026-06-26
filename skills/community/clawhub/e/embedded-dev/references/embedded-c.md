# 嵌入式C语言编程规范与技巧

## 关键规范

### 1. 头文件保护

```c
#ifndef __MY_DRIVER_H__
#define __MY_DRIVER_H__
// ...
#endif
```

### 2. 寄存器定义方式

**推荐：结构体联合体映射（STM32标准方式）**
```c
// 不推荐：裸地址操作
*((volatile uint32_t*)(0x40021000 + 0x0C)) = 0x00000001;

// 推荐：结构体映射
#define RCC_BASE           0x40021000UL
typedef struct {
    volatile uint32_t CR;
    volatile uint32_t CFGR;
    volatile uint32_t CIR;
    volatile uint32_t APB2RSTR;
    volatile uint32_t APB1RSTR;
    volatile uint32_t AHBENR;
    volatile uint32_t APB2ENR;   // 偏移 0x18
    volatile uint32_t APB1ENR;
    // ...
} RCC_TypeDef;
#define RCC               ((RCC_TypeDef*)RCC_BASE)
RCC->APB2ENR |= RCC_APB2ENR_IOPAEN;  // 清晰直观
```

### 3. volatile 关键字

所有以下情况必须加 `volatile`：
```c
// 硬件寄存器（硬件可改变其值）
volatile uint32_t * const USART_SR = (uint32_t*)0x40013800;
volatile uint8_t rx_buffer[256];

// 多线程共享变量（RTOS任务间）
volatile bool data_ready = false;

// 中断/主循环共享变量
volatile uint16_t tick_count;
```

### 4. 内存屏障

```c
// ARM Cortex-M 必须加 DMB（数据内存屏障）
void barrier(void) {
    __asm__ volatile ("dmb sy" ::: "memory");
}

// 关中断保护共享数据
uint32_t saved = __get_PRIMASK();
__set_PRIMASK(1);
// 临界区
__set_PRIMASK(saved);
```

### 5. 位操作技巧

```c
// 置位
GPIOA->ODR |= (1 << 5);

// 清零
GPIOA->ODR &= ~(1 << 5);

// 翻转
GPIOA->ODR ^= (1 << 5);

// 读-改-写（保护）
uint32_t odr = GPIOB->IDR;
if (odr & (1 << 3)) { ... }

// 提取特定位
uint8_t val = (REG->DR & 0xFF);         // 取低8位
uint8_t bits = (REG->DR >> 4) & 0x0F;   // 取第4-7位

// 合并
REG->DR = (val << 4) | (bits & 0x0F);
```

### 6. 断言与错误处理

```c
#ifdef DEBUG
#define ASSERT(expr) \
    do { if (!(expr)) while(1); } while(0)
#else
#define ASSERT(expr) ((void)0)
#endif

ASSERT(pointer != NULL);
ASSERT(index < MAX_SIZE);
```

### 7. 编译器属性

```c
// 放在特定内存区域（STM32 DTCM/ITCM）
uint8_t rx_buffer[256] __attribute__((section(".RAM_D2")));

// 禁止编译器优化（硬件寄存器必备）
register volatile uint32_t * const reg = (uint32_t*)0x40021000;

// 对齐（DMA/USB必备）
__attribute__((aligned(4))) uint8_t dma_buf[1024];

// 函数放在Flash（不占用RAM）
__attribute__((section(".text"))) void FuncInFlash(void) { }

// 零初始化段
volatile uint32_t system_state __attribute__((section(".noinit")));
```

### 8. 链接脚本关键段

```
MEMORY
{
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 128K
  RAM (rwx)   : ORIGIN = 0x20000000, LENGTH = 20K
}

SECTIONS
{
  .text : { *(.text*) } > FLASH
  .data : { *(.data*) } > RAM AT > FLASH  /* 初始值副本放Flash */
  .bss  : { *(.bss*) } > RAM              /* 零初始化 */
}
```

### 9. 链接时从Flash复制.data

```c
// STM32 启动文件标准做法
extern uint32_t _sidata, _sdata, _edata, _sbss, _ebss;

void Reset_Handler(void) {
    // 复制 .data 段（从Flash到RAM）
    for (uint32_t *p = &_sdata; p < &_edata; )
        *p++ = *((uint32_t*)((uint8_t*)&_sidata + (p - &_sdata)));

    // 零初始化 .bss
    for (uint32_t *p = &_sbss; p < &_ebss; *p++ = 0);

    SystemInit();
    main();
}
```

### 10. 嵌入式常见陷阱

```c
// 陷阱1：除法运算极慢
uint32_t x = value / 10;   // 避免在中断中用，改用右移或查表

// 陷阱2：浮点运算（无FPU的M0/M0+上极慢）
float temp = adc_val * 3.3 / 4096;  // 换算：用整数放大法
uint32_t temp = (adc_val * 3300) / 4096;  // 结果是mV

// 陷阱3：字符串处理占用大量RAM
char buf[256]; sprintf(buf, "Temp:%d.%02d", t/100, t%100);
// 改用：
snprintf(buf, sizeof(buf), "Temp:%d.%02d", t/100, t%100);

// 陷阱4：递归调用耗尽栈
// 改写为循环或静态栈

// 陷阱5：隐式类型转换截断
uint16_t val = 0xFFFF;
uint8_t small = val;  // 截断为 0xFF，应明确处理
uint8_t small = (uint8_t)(val & 0xFF);
```
