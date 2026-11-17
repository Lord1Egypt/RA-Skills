/**
 * servo_sg90_port.h - 舵机平台适配层（示例：STM32 HAL TIM1 CH1，168MHz）
 *
 * 移植：只改这个文件。要求 50Hz PWM 输出脚（橙=信号 红=VCC 棕=GND）。
 */
#ifndef SERVO_SG90_PORT_H
#define SERVO_SG90_PORT_H

#include <stdint.h>

/* ===== 定时器参数（改成你的配置） ===== */
/* 示例：F4 TIM1 APB2 168MHz，PSC=167 → 1MHz tick，ARR=19999 → 20ms(50Hz) */
#include "stm32f4xx_hal.h"
extern TIM_HandleTypeDef htim1;

static inline uint32_t servo_tim_clk_hz(void)  { return 168000000U; }
static inline uint32_t servo_psc_default(void) { return 167; }
static inline uint32_t servo_arr_default(void) { return 19999; }

static inline void servo_pwm_write_ccr(int ccr)
{
    __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, ccr);
    /* 启动只做一次（main 初始化）：
     * HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1); */
}

#endif /* SERVO_SG90_PORT_H */
