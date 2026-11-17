/**
 * stepper_28byj48_port.h - 28BYJ-48 平台适配层（示例：STM32 HAL 4 路 GPIO）
 *
 * 移植：只改这个文件。ULN2003 板 IN1-IN4 ↔ 4 路 GPIO 推挽输出。
 */
#ifndef STEPPER_28BYJ48_PORT_H
#define STEPPER_28BYJ48_PORT_H

#include <stdint.h>
#include "stm32f4xx_hal.h"

/* ===== 4 路 GPIO（改成你的引脚；IN1-IN4 与 bit0-3 对应） ===== */
static inline void stepper_write_phase(int pattern)
{
    /* 示例：PB0-PB3 → IN1-IN4，一次写 4 位 */
    uint32_t base = GPIO_PIN_0;
    GPIOB->BSRR = (base << 4) |                       /* 先清 bit0-3 */
                  ((uint32_t)(pattern & 0xF) * base); /* 再置位 */
}

/* ===== 延时（HAL_Delay 毫秒粒度即可，半步延时通常 1-10ms 量级） ===== */
static inline void stepper_delay_us(uint32_t us)
{
    uint32_t ms = us / 1000U + 1U;
    HAL_Delay(ms);
}

#endif /* STEPPER_28BYJ48_PORT_H */
