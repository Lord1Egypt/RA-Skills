---
name: embed-code-drivers
description: Peripheral driver templates. UART, SPI, I2C, DMA, CAN, CANFD, PWM, Ethernet, 1553B, SpaceWire, SDIO, Timer, WDT, GPIO.
---

# Driver Templates

## UART

```c
#define UART_DR(base)   (*(volatile uint32_t *)((base) + 0x00U))
#define UART_CR(base)   (*(volatile uint32_t *)((base) + 0x30U))
#define UART_FR(base)   (*(volatile uint32_t *)((base) + 0x18U))

typedef struct {
    uint32_t base_address;
    uint32_t baud_rate;
} uart_config_t;

typedef struct {
    bool     initialized;
    uint8_t  rx_buf[256];
    uint16_t rx_head;
    uint16_t rx_tail;
} uart_handle_t;
```

## SPI

```c
#define SPI_CR1(base)  (*(volatile uint32_t *)((base) + 0x00U))
#define SPI_SR(base)   (*(volatile uint32_t *)((base) + 0x08U))
#define SPI_DR(base)   (*(volatile uint32_t *)((base) + 0x0CU))

typedef struct {
    uint32_t base_address;
    uint32_t clock_hz;
    bool     master_mode;
} spi_config_t;
```

## I2C

```c
#define I2C_CR1(base)  (*(volatile uint32_t *)((base) + 0x00U))
#define I2C_DR(base)   (*(volatile uint32_t *)((base) + 0x10U))
#define I2C_SR1(base)  (*(volatile uint32_t *)((base) + 0x14U))
```

## DMA

```c
#define DMA_CCR(base,ch)  (*(volatile uint32_t *)((base) + 0x08U + (ch) * 0x14U))
#define DMA_CPAR(base,ch) (*(volatile uint32_t *)((base) + 0x10U + (ch) * 0x14U))
#define DMA_CMAR(base,ch) (*(volatile uint32_t *)((base) + 0x14U + (ch) * 0x14U))
```

## CAN

```c
#define CAN_MCR(base)  (*(volatile uint32_t *)((base) + 0x00U))
#define CAN_TSR(base)  (*(volatile uint32_t *)((base) + 0x08U))
#define CAN_BTR(base)  (*(volatile uint32_t *)((base) + 0x1CU))

typedef struct {
    uint32_t id;
    uint8_t  dlc;
    uint8_t  data[64];
} can_msg_t;
```

## GPIO

```c
#define GPIO_MODER(base)  (*(volatile uint32_t *)((base) + 0x00U))
#define GPIO_ODR(base)   (*(volatile uint32_t *)((base) + 0x14U))
#define GPIO_BSRR(base)  (*(volatile uint32_t *)((base) + 0x18U))

typedef enum {
    GPIO_MODE_INPUT = 0,
    GPIO_MODE_OUTPUT,
    GPIO_MODE_AF,
    GPIO_MODE_ANALOG
} gpio_mode_t;
```

## TIMER/WDT

```c
#define TIM_CR1(base)   (*(volatile uint32_t *)((base) + 0x00U))
#define TIM_ARR(base)   (*(volatile uint32_t *)((base) + 0x2CU))
#define TIM_CNT(base)   (*(volatile uint32_t *)((base) + 0x24U))

#define WDT_KR(base)   (*(volatile uint32_t *)((base) + 0x00U))
#define WDT_RLR(base)  (*(volatile uint32_t *)((base) + 0x08U))
```

## 1553B

```c
typedef enum {
    1553_MODE_BC = 0,
    1553_MODE_RT = 1,
    1553_MODE_BM = 2
}1553_mode_t;

typedef struct {
    uint8_t  cmd;
    uint16_t status;
    uint16_t data[32];
}1553_msg_t;
```
