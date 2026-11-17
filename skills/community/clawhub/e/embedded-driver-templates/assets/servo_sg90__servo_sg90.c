/**
 * servo_sg90.c - SG90 舵机驱动实现
 * 换算依据：SG90 数据手册（周期 20ms，脉宽 0.5-2.5ms 对应 0-180°）
 * 注：SG90 实际可用范围约 500-2400us，个别个体 0/180° 到不了——
 *     实测后可在 servo_angle_to_pulse_us 里收紧 MIN/MAX（见 wiring.md 坑 3）
 */
#include "servo_sg90.h"

/* ---------------- 纯函数（PC 可单元测试） ---------------- */

int servo_angle_to_pulse_us(int angle)
{
    if (angle < 0)
        return -1;
    if (angle > 180)
        return -2;
    /* 先乘后除防精度损失：500 + angle*2000/180
     * 0°→500  45°→1000  90°→1500  180°→2500 */
    return SERVO_PULSE_MIN_US + (int)((int32_t)angle * 2000 / 180);
}

int servo_pulse_to_ccr(uint32_t pulse_us, uint32_t tim_clk_hz,
                       uint32_t psc, uint32_t arr)
{
    /* 定时器 tick 频率 = tim_clk / (psc+1)；周期 = (arr+1) tick */
    uint64_t tick_hz = (uint64_t)tim_clk_hz / ((uint64_t)psc + 1);
    uint64_t period_us = ((uint64_t)arr + 1) * 1000000ULL / tick_hz;

    /* 周期应在 20ms±5%（19.0-21.0ms）：50Hz 是舵机的硬要求 */
    if (period_us < 19000ULL || period_us > 21000ULL)
        return -1;

    uint64_t ccr = (uint64_t)pulse_us * tick_hz / 1000000ULL;
    if (ccr > (uint64_t)arr + 1)
        return -2;              /* 脉宽比周期还长，PWM 打不出来 */
    return (int)ccr;
}

int servo_angle_to_ccr(int angle, uint32_t tim_clk_hz,
                       uint32_t psc, uint32_t arr)
{
    int us = servo_angle_to_pulse_us(angle);
    if (us < 0)
        return us;
    return servo_pulse_to_ccr((uint32_t)us, tim_clk_hz, psc, arr);
}

/* ---------------- 硬件输出（目标机上运行） ---------------- */

void servo_write_angle(int angle)
{
    int ccr = servo_angle_to_ccr(angle, servo_tim_clk_hz(),
                                 servo_psc_default(), servo_arr_default());
    if (ccr >= 0)
        servo_pwm_write_ccr(ccr);
}
