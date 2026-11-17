/**
 * servo_sg90.h - SG90 舵机驱动（可移植版）
 *
 * 适用：任何 MCU，只需在 servo_sg90_port.h 提供 PWM 写入接口
 * 特性：C99、无动态内存、角度→脉宽→CCR 换算全为纯函数（PC 上可单元测试）
 *
 * 用法：
 *   servo_write_angle(90);            // 转到 90°（内部完成全部换算）
 *   // 或只用纯函数（推荐：换算在 PC 上先验好再上板）：
 *   int us  = servo_angle_to_pulse_us(90);   // → 1500
 *   int ccr = servo_pulse_to_ccr(1500, 168000000, 167, 19999);  // → 1500
 *
 * 验证记录：见本目录 meta.json
 */
#ifndef SERVO_SG90_H
#define SERVO_SG90_H

#include <stdint.h>

#define SERVO_PULSE_MIN_US  500     /* 0° 对应脉宽 */
#define SERVO_PULSE_MAX_US  2500    /* 180° 对应脉宽 */

/* ---- 移植适配层：在 servo_sg90_port.h 中实现 ---- */
#include <servo_sg90_port.h>   /* 提供 servo_tim_clk_hz() / servo_psc_default()
                                  servo_arr_default() / servo_pwm_write_ccr(ccr) */

/* 角度 → 脉宽（微秒）。0-180° → 500-2500us。
 * 纯函数。angle 越界返回负数（<0 → -1，>180 → -2）。 */
int servo_angle_to_pulse_us(int angle);

/* 脉宽 → 定时器 CCR 值。tick = tim_clk/(psc+1)，周期 = (arr+1) tick。
 * 纯函数。周期不在 19-21ms（50Hz±5%）返回 -1；脉宽超周期返回 -2。 */
int servo_pulse_to_ccr(uint32_t pulse_us, uint32_t tim_clk_hz,
                       uint32_t psc, uint32_t arr);

/* 角度一步到位算 CCR（前两者组合）。参数错误透传负错误码。纯函数。 */
int servo_angle_to_ccr(int angle, uint32_t tim_clk_hz,
                       uint32_t psc, uint32_t arr);

/* 写角度到硬件（目标机上运行；阻塞换算极短可忽略） */
void servo_write_angle(int angle);

#endif /* SERVO_SG90_H */
