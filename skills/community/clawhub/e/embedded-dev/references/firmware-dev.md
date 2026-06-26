# 固件架构与 OTA 升级

## 模块化固件架构

```
Application Layer    ← 业务逻辑层（状态机/主循环）
Middleware Layer     ← 中间件层（协议解析/数据处理）
Driver Layer         ← 驱动层（GPIO/UART/I2C/SPI）
Hardware             ← 硬件抽象层（STM32/ESP32）
```

## 状态机设计

```c
typedef enum { STATE_INIT=0, STATE_STANDBY, STATE_RUNNING, STATE_ERROR, STATE_SLEEP } AppState;

typedef struct { AppState from; uint8_t event; AppState to; } Transition;

Transition transitions[] = {
    {STATE_INIT,      EV_READY,  STATE_STANDBY},
    {STATE_STANDBY,   EV_START,  STATE_RUNNING},
    {STATE_RUNNING,   EV_STOP,   STATE_STANDBY},
    {STATE_RUNNING,   EV_ERROR,  STATE_ERROR},
    {STATE_ERROR,     EV_RESET,  STATE_INIT},
};

void process_event(AppEvent ev) {
    for (int i = 0; i < sizeof(transitions)/sizeof(transitions[0]); i++) {
        if (transitions[i].from == current_state && transitions[i].event == ev) {
            on_exit_state(current_state);
            current_state = transitions[i].to;
            on_enter_state(current_state);
            break;
        }
    }
}
```

## STM32 Flash 布局

```
0x08000000 ┌──────────────────┐ Bootloader (32KB)
0x08008000 ┌──────────────────┤ App1 (128KB)
0x08020000 ┌──────────────────┤ App2 OTA区 (128KB)
0x08038000 ┌──────────────────┤ Config (4KB)
0x08039000 ┌──────────────────┘ OTA Flag (4KB)
```

## Bootloader 跳转

```c
void JumpToApp(uint32_t app_addr) {
    uint32_t sp = *(uint32_t*)app_addr;
    uint32_t pc = *(uint32_t*)(app_addr + 4);
    __set_MSP(sp);
    ((void(*)(void))pc)();
}
```

## OTA 标志位

```c
#define OTA_FLAG_ADDR  0x08039000
#define OTA_FLAG_VALID  0xBEEFCAFE

typedef struct {
    uint32_t valid;
    uint32_t active_app;   // 1=App1, 2=App2
    uint32_t crc;
} OTA_Info;
```

## CRC 自检

```c
uint32_t calc_firmware_crc(uint32_t addr, uint32_t len) {
    RCC->AHBENR |= RCC_AHBENR_CRCEN;
    CRC->CR = CRC_CR_RESET;
    for (uint32_t i = 0; i < len; i++)
        CRC->DR = ((uint8_t*)addr)[i];
    return CRC->DR;
}
```

## 低功耗模式

```c
// 停机模式 Stop（~0.5mA）
void enter_stop_mode(void) {
    HAL_PWR_EnterSTOPMode(PWR_LOWPOWERMODE_STOP, PWR_STOPENTRY_WFI);
    // 唤醒后重新配置时钟
    SystemClock_Config();
}

// 待机模式 Standby（<5µA）
void enter_standby_mode(void) {
    HAL_PWR_EnableWakeUpPin(PWR_WAKEUP_PIN1);
    __HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU);
    HAL_PWR_EnterSTANDBYMode();
}

// 动态调频
void set_cpu_freq(uint32_t freq_mhz) {
    // 72MHz: PLL=8MHz*9, 36MHz: PLL=8MHz*18
    if (freq_mhz == 72) {
        __HAL_RCC_PLL_CONFIG(RCC_PLLCFGR_PLLSRC_HSE, 8, 9);
    }
    HAL_RCC_DeInit();
    // 重新配置...
}
```

## 看门狗

```c
// 独立看门狗 IWDG（最快32s，适用死循环检测）
void IWDG_Init(uint16_t ms) {
    IWDG->KR = 0x5555;  // 解锁
    IWDG->PR = 4;       // 256分频
    IWDG->RLR = ms / (256 / 32000) * 1000; // 喂狗重装载值
    IWDG->KR = 0xCCCC;  // 启动
}
#define FEED_DOG()  do { IWDG->KR = 0xAAAA; } while(0)

// 窗口看门狗 WWDG（更快，最多83ms）
void WWDG_Init(void) {
    __HAL_RCC_WWDG_CLK_ENABLE();
    WWDG->CFR = 0x7F;      // 窗口值
    WWDG->CR = 0x7F;       // 计数器
    WWDG->CR |= 0x80;      // 启动
}
```

## 固件模块化头文件设计

```c
// bsp.h - 硬件抽象层
#ifndef __BSP_H__
#define __BSP_H__
#include "stm32f1xx_hal.h"
void BSP_Init(void);
void BSP_GPIO_Init(void);
void BSP_UART_Init(UART_HandleTypeDef *huart);
uint32_t BSP_GetTick(void);
#endif

// app.h - 业务层
#ifndef __APP_H__
#define __APP_H__
typedef enum { EV_NONE, EV_TIMER, EV_UART, EV_ERROR } AppEvent;
void APP_Init(void);
void APP_Loop(void);
void APP_OnEvent(AppEvent ev);
#endif
```
