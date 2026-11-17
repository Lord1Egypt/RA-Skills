/**
 * stepper_28byj48.c - 28BYJ-48 步进电机驱动实现
 * 换算依据：28BYJ-48 数据手册（转子 32 步/圈，减速比 63.68395:1）
 * 相序依据：ULN2003 板 IN1-IN4 半步 8 拍 / 全步（双相激励）4 拍
 */
#include "stepper_28byj48.h"

/* 精确减速比：63.68395:1（= 32/9 × 22/11 × 26/9 × 31/10 四级齿轮）。
 * 32 步/圈 × 63.68395 = 2037.886 全步 → 取 2038；半步 ×2 = 4075.77 → 取 4076。 */
#define STEPPER_ROTOR_STEPS   32

/* 半步 8 拍（IN1..IN4 依次励磁）：
 * 0001 → 0011 → 0010 → 0110 → 0100 → 1100 → 1000 → 1001 */
static const uint8_t HALF_SEQ[8] = {0x1, 0x3, 0x2, 0x6, 0x4, 0xC, 0x8, 0x9};

/* 全步 4 拍（双相激励，转矩最大）：
 * 0011 → 0110 → 1100 → 1001 */
static const uint8_t FULL_SEQ[4] = {0x3, 0x6, 0xC, 0x9};

/* ---------------- 纯函数（PC 可单元测试） ---------------- */

int stepper_steps_per_rev(int halfstep)
{
    /* 精确值：32 × 63.68395 ≈ 2037.9 → 2038 全步 / 4076 半步 */
    return halfstep ? 4076 : 2038;
}

int stepper_angle_to_steps(int angle, int halfstep)
{
    int spr = stepper_steps_per_rev(halfstep);
    if (spr <= 0)
        return -1;
    /* 先乘后除 + 四舍五入：steps = angle × spr / 360 */
    int32_t n = (int32_t)angle * spr;
    if (n >= 0)
        return (int)((n + 180) / 360);
    return -((int)((-n + 180) / 360));
}

int stepper_phase_pattern(int idx, int halfstep)
{
    if (halfstep)
        return HALF_SEQ[((idx % 8) + 8) % 8];
    return FULL_SEQ[((idx % 4) + 4) % 4];
}

int stepper_rpm_to_delay_us(int rpm, int halfstep)
{
    if (rpm <= 0)
        return -1;
    if (rpm > 18)
        return -2;              /* 28BYJ-48 转矩小，>15RPM 基本失步 */
    int spr = stepper_steps_per_rev(halfstep);
    /* 每步延时 us = 60 秒 / (rpm×spr 步) = 6e7 / (rpm×spr) */
    return (int)(60000000LL / ((int64_t)rpm * spr));
}
