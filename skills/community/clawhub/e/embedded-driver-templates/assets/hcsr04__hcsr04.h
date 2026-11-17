/**
 * hcsr04.h - HC-SR04 超声波测距驱动（可移植版）
 *
 * 原理：Trig 打 10us 高脉冲 → 模块发 8 个 40kHz 声波 → Echo 高电平宽度 = 声波往返时间
 * 距离(cm) = echo_us * 0.0343 / 2（声速 343m/s @ 23°C）
 * 量程：2cm ~ 400cm；echo 无回波（超时 38ms）= 超量程或未接
 *
 * 验证记录：见本目录 meta.txt
 */
#ifndef HCSR04_H
#define HCSR04_H

#include <stdint.h>

#define HCSR04_OK            0
#define HCSR04_ERR_NO_ECHO  -1   /* echo 超时：目标超量程/接线错/未共地 */
#define HCSR04_ERR_PARAM    -2

#include <hcsr04_port.h>   /* 适配层：hcsr04_trig(level) / hcsr04_echo_read()
                              hcsr04_delay_us(us) / hcsr04_delay_ms(ms) */

/* echo 高电平时间(us) → 距离 cm（保留 1 位小数，返回值*10）。
 * 纯函数，PC 可测。no_echo_us = 38ms（模块对超量程的固定超时特征）。 */
int32_t hcsr04_us_to_cm_x10(uint32_t echo_us);

/* 判断 echo 是否处于"无回波"特征区间（>= 38000us）。纯函数。 */
int hcsr04_is_no_echo(uint32_t echo_us);

/* 阻塞测距一次。返回值同 hcsr04_us_to_cm_x10，错误码用负数。 */
int32_t hcsr04_read_cm_x10(void);

#endif /* HCSR04_H */
