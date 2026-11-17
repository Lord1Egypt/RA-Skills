/**
 * mpu6050.h - MPU6050 六轴传感器驱动（可移植版）
 *
 * 适用：任何 MCU —— 在 mpu6050_port.h 提供 I2C 读写两个接口即可
 * 特性：C99；换算/校准判断为纯函数（PC 可单元测试）
 *
 * 用法：
 *   if (mpu6050_init() == MPU6050_OK) {
 *       mpu6050_raw_t r;
 *       mpu6050_read_raw(&r);
 *       int32_t mg  = mpu6050_raw_to_mg(r.ax, 0);      // ±2g 档
 *       int32_t dps = mpu6050_raw_to_dps_centi(r.gx, 0); // ±250°/s 档
 *   }
 *
 * 验证记录：见本目录 meta.json
 */
#ifndef MPU6050_H
#define MPU6050_H

#include <stdint.h>

#define MPU6050_OK            0
#define MPU6050_ERR_I2C      -1   /* I2C 读写失败：接线/地址/上拉 */
#define MPU6050_ERR_WHO_AM_I -2   /* WHO_AM_I 不是 0x68：型号不对或总线不稳 */

#define MPU6050_ADDR_LOW     0x68  /* AD0=GND（模块默认） */
#define MPU6050_ADDR_HIGH    0x69  /* AD0=VCC */

/* 寄存器（本驱动用到的子集） */
#define MPU6050_REG_SMPLRT_DIV   0x19
#define MPU6050_REG_CONFIG       0x1A
#define MPU6050_REG_GYRO_CONFIG  0x1B
#define MPU6050_REG_ACCEL_CONFIG 0x1C
#define MPU6050_REG_ACCEL_XOUT_H 0x3B
#define MPU6050_REG_TEMP_OUT_H   0x41
#define MPU6050_REG_GYRO_XOUT_H  0x43
#define MPU6050_REG_PWR_MGMT_1   0x6B
#define MPU6050_REG_WHO_AM_I     0x75

typedef struct {
    int16_t ax, ay, az;    /* 加速度原始值（16bit 补码） */
    int16_t temp;          /* 温度原始值 */
    int16_t gx, gy, gz;    /* 角速度原始值 */
} mpu6050_raw_t;

/* ---- 移植适配层：在 mpu6050_port.h 中实现 ---- */
#include <mpu6050_port.h>   /* 提供 mpu6050_i2c_write(addr, reg, buf, len)
                                                          mpu6050_i2c_read(addr, reg, buf, len) */

/* 换算：加速度 raw → 毫克（mg）。fs_sel: 0=±2g, 1=±4g, 2=±8g, 3=±16g。
 * 纯函数。示例：±2g 档 raw=16384 → 1000mg（即 1g）。 */
int32_t mpu6050_raw_to_mg(int16_t raw, uint8_t fs_sel);

/* 换算：角速度 raw → 0.01°/s（百分之一度每秒）。fs_sel: 0=±250, 1=±500,
 * 2=±1000, 3=±2000 °/s。纯函数。示例：±250 档 raw=131 → 100（≈1°/s）。 */
int32_t mpu6050_raw_to_dps_centi(int16_t raw, uint8_t fs_sel);

/* 换算：温度 raw → 0.01°C。数据手册：Temp = raw/340 + 36.53。纯函数。 */
int32_t mpu6050_temp_c_x100(int16_t raw);

/* WHO_AM_I 返回值合法性：0x68（少数固件 0x69/0x98 也能用）。纯函数。 */
int mpu6050_who_am_i_ok(uint8_t val);

/* 静止自检：三轴加速度合成应接近 1g（容差 ±15%）。纯函数。
 * 用途：初始化后校准零偏；不满足说明量程档配错或传感器在动。 */
int mpu6050_static_check(int16_t ax, int16_t ay, int16_t az);

/* 阻塞读一次原始六轴+温度。 */
int mpu6050_read_raw(mpu6050_raw_t *out);

/* 初始化：解除睡眠 → 配置量程（±2g / ±250°/s 默认）→ 校验 WHO_AM_I。 */
int mpu6050_init(void);

#endif /* MPU6050_H */
