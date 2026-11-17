/**
 * ds18b20_port.h - DS18B20 平台适配层（示例：STM32 HAL + DWT 微秒延时）
 *
 * 移植：只改这个文件。核心要求是"微秒级精度的单总线时序"，HAL_Delay 的
 * 毫秒粒度完全不够用（头号移植坑），必须用 DWT CYCCNT 或 TIM 计数。
 */
#ifndef DS18B20_PORT_H
#define DS18B20_PORT_H

#include <stdint.h>

/* ===== 1) 微秒/毫秒延时（示例：STM32 DWT，SystemCoreClock=168MHz+） ===== */
static inline void ds18b20_delay_us(uint32_t us)
{
    uint32_t start = DWT->CYCCNT;
    uint32_t ticks = us * (SystemCoreClock / 1000000U);
    while ((DWT->CYCCNT - start) < ticks) { /* busy-wait */ }
}
/* DWT 使能（main 初始化时调用一次）：
 *   CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
 *   DWT->CYCCNT = 0;
 *   DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk; */

static inline void ds18b20_delay_ms(uint32_t ms)
{
    while (ms--) {
        ds18b20_delay_us(1000);
    }
}

/* ===== 2) 单总线 GPIO：改成你的引脚 ===== */
/* 示例：PA1 推挽输出 + 浮空输入，开漏模式亦可 */
#include "stm32f4xx_hal.h"
#define DS18B20_GPIO_PORT  GPIOA
#define DS18B20_GPIO_PIN   GPIO_PIN_1

static inline void ds18b20_line_out(int level)
{
    HAL_GPIO_WritePin(DS18B20_GPIO_PORT, DS18B20_GPIO_PIN,
                      level ? GPIO_PIN_SET : GPIO_PIN_RESET);
}
static inline void ds18b20_line_in(void)
{
    GPIO_InitTypeDef g = {0};
    g.Pin = DS18B20_GPIO_PIN;
    g.Mode = GPIO_MODE_INPUT;
    g.Pull = GPIO_PULLUP;           /* DQ 必须上拉：内部上拉可用但外接 4.7k 更稳 */
    HAL_GPIO_Init(DS18B20_GPIO_PORT, &g);
}
static inline int ds18b20_line_read(void)
{
    return (int)HAL_GPIO_ReadPin(DS18B20_GPIO_PORT, DS18B20_GPIO_PIN);
}

#endif /* DS18B20_PORT_H */
