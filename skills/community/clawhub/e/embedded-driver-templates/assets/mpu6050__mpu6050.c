/**
 * mpu6050.c - MPU6050 驱动实现
 *
 * 结构约定：换算纯函数与 I2C 操作严格分离——纯函数可直接在 PC 上单元测试。
 */
#include "mpu6050.h"

/* ---------------- 纯函数区（PC 可测） ---------------- */

int32_t mpu6050_raw_to_mg(int16_t raw, uint8_t fs_sel)
{
    /* ±2g 满量程 = 2000mg；每升一档量程翻倍。raw 32768 对应满量程。
     * 先乘后除防精度丢失；2000<<(fs_sel) 最大 16000，raw 32767 相乘在 int32 内不溢出。 */
    if (fs_sel > 3) {
        fs_sel = 3;
    }
    return ((int32_t)raw * (2000L << fs_sel)) / 32768L;
}

int32_t mpu6050_raw_to_dps_centi(int16_t raw, uint8_t fs_sel)
{
    /* ±250°/s 满量程 = 25000（0.01°/s 单位）；每升一档翻倍。 */
    if (fs_sel > 3) {
        fs_sel = 3;
    }
    return ((int32_t)raw * (25000L << fs_sel)) / 32768L;
}

int32_t mpu6050_temp_c_x100(int16_t raw)
{
    /* Temp(°C) = raw/340 + 36.53 → x100: raw*100/340 + 3653 = raw*10/34 + 3653 */
    return ((int32_t)raw * 10) / 34 + 3653;
}

int mpu6050_who_am_i_ok(uint8_t val)
{
    /* 正品为 0x68；部分兼容芯片返回 0x69/0x98 仍按 MPU6050 兼容处理 */
    return (val == 0x68 || val == 0x69 || val == 0x98) ? 1 : 0;
}

int mpu6050_static_check(int16_t ax, int16_t ay, int16_t az)
{
    /* 静止时合成加速度 ≈ 1g = 16384（±2g 档）。容差 ±15%。
     * 用 int64 防平方和溢出。 */
    int64_t sum2 = (int64_t)ax * ax + (int64_t)ay * ay + (int64_t)az * az;
    int64_t one_g = 16384LL;
    /* sum2 与 (0.85g)^2 ~ (1.15g)^2 比较：(0.85)^2=0.7225, (1.15)^2=1.3225 */
    return (sum2 * 10000LL >= one_g * one_g * 7225LL &&
            sum2 * 10000LL <= one_g * one_g * 13225LL) ? 1 : 0;
}

/* ---------------- I2C 操作区（需真实硬件） ---------------- */

static int _write_reg(uint8_t reg, uint8_t val)
{
    return mpu6050_i2c_write(MPU6050_ADDR_LOW, reg, &val, 1);
}

int mpu6050_init(void)
{
    uint8_t who = 0;
    if (_write_reg(MPU6050_REG_PWR_MGMT_1, 0x00) != 0) {  /* 解除睡眠 */
        return MPU6050_ERR_I2C;
    }
    mpu6050_delay_ms(10);
    if (mpu6050_i2c_read(MPU6050_ADDR_LOW, MPU6050_REG_WHO_AM_I, &who, 1) != 0) {
        return MPU6050_ERR_I2C;
    }
    if (!mpu6050_who_am_i_ok(who)) {
        return MPU6050_ERR_WHO_AM_I;
    }
    /* 采样率 1kHz/(1+4)=200Hz；DLPF 44Hz；量程 ±250°/s + ±2g（默认 0） */
    (void)_write_reg(MPU6050_REG_SMPLRT_DIV, 0x04);
    (void)_write_reg(MPU6050_REG_CONFIG, 0x03);
    (void)_write_reg(MPU6050_REG_GYRO_CONFIG, 0x00);
    (void)_write_reg(MPU6050_REG_ACCEL_CONFIG, 0x00);
    return MPU6050_OK;
}

int mpu6050_read_raw(mpu6050_raw_t *out)
{
    uint8_t b[14] = {0};   /* 显式清零：I2C 部分读失败时不留脏数据（也消 -Wmaybe-uninitialized） */
    if (out == 0) {
        return MPU6050_ERR_I2C;
    }
    /* 0x3B 起连续读 14 字节：ax ay az temp gx gy gz（高字节在前） */
    if (mpu6050_i2c_read(MPU6050_ADDR_LOW, MPU6050_REG_ACCEL_XOUT_H, b, 14) != 0) {
        return MPU6050_ERR_I2C;
    }
    out->ax = (int16_t)(((uint16_t)b[0] << 8) | b[1]);
    out->ay = (int16_t)(((uint16_t)b[2] << 8) | b[3]);
    out->az = (int16_t)(((uint16_t)b[4] << 8) | b[5]);
    out->temp = (int16_t)(((uint16_t)b[6] << 8) | b[7]);
    out->gx = (int16_t)(((uint16_t)b[8] << 8) | b[9]);
    out->gy = (int16_t)(((uint16_t)b[10] << 8) | b[11]);
    out->gz = (int16_t)(((uint16_t)b[12] << 8) | b[13]);
    return MPU6050_OK;
}
