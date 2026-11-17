/**
 * hcsr04.c - HC-SR04 驱动实现（可移植版）
 */
#include "hcsr04.h"

/* ---------------- 纯函数（PC 可单元测试） ---------------- */

#define HCSR04_NO_ECHO_US   38000u   /* 模块超量程时 echo 高电平固定 ~38ms */
#define HCSR04_MIN_US       116u     /* 2cm 对应往返时间 */
#define HCSR04_MAX_US       23300u   /* 400cm 对应往返时间 */

int32_t hcsr04_us_to_cm_x10(uint32_t echo_us)
{
    /* 343 m/s = 0.0343 cm/us；往返除 2 → 0.01715 cm/us
     * x10 表示 → 0.1715 cm_x10/us = 1715/10000 */
    int32_t cm_x10 = (int32_t)((uint64_t)echo_us * 1715UL / 10000UL);
    if (echo_us < HCSR04_MIN_US || echo_us > HCSR04_MAX_US)
        return HCSR04_ERR_PARAM;    /* 超出量程的数据不可信，显式报错而不是返回离谱值 */
    return cm_x10;
}

int hcsr04_is_no_echo(uint32_t echo_us)
{
    return echo_us >= HCSR04_NO_ECHO_US;
}

/* ---------------- 总线时序（目标机上运行） ---------------- */

int32_t hcsr04_read_cm_x10(void)
{
    /* 1. Trig: >=10us 高脉冲 */
    hcsr04_trig(0);
    hcsr04_delay_us(2);
    hcsr04_trig(1);
    hcsr04_delay_us(15);
    hcsr04_trig(0);

    /* 2. 等 echo 拉高（模块内部发出声波需要几百 us） */
    uint32_t guard = 0;
    while (hcsr04_echo_read() == 0) {
        hcsr04_delay_us(1);
        if (++guard > 10000)                /* 10ms 内 echo 没起来 */
            return HCSR04_ERR_NO_ECHO;
    }

    /* 3. 测 echo 高电平宽度（us）。和 DHT11 一样依赖 us 级延时精度 */
    uint32_t echo_us = 0;
    while (hcsr04_echo_read() == 1) {
        hcsr04_delay_us(1);
        if (++echo_us > 40000) {            /* 硬超时兜底 40ms */
            return HCSR04_ERR_NO_ECHO;
        }
    }

    if (hcsr04_is_no_echo(echo_us))
        return HCSR04_ERR_NO_ECHO;

    return hcsr04_us_to_cm_x10(echo_us);
}
