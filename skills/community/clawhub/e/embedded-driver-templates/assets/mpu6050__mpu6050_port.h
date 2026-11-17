/**
 * mpu6050_port.h - MPU6050 平台适配层（示例：STM32 HAL I2C1 @400kHz）
 *
 * 移植：只改这个文件。两个函数 + 一个延时，I2C 地址用 7 位。
 */
#ifndef MPU6050_PORT_H
#define MPU6050_PORT_H

#include <stdint.h>

/* 示例：STM32 HAL I2C1。工程里先完成 HAL_I2C_MspInit 与 hi2c1 初始化 */
#include "stm32f4xx_hal.h"
extern I2C_HandleTypeDef hi2c1;

static inline void mpu6050_delay_ms(uint32_t ms)
{
    HAL_Delay(ms);
}

/* 写寄存器：先发 reg 再发数据。返回 0 成功，非 0 失败 */
static inline int mpu6050_i2c_write(uint8_t addr7, uint8_t reg,
                                    const uint8_t *buf, uint16_t len)
{
    return (HAL_I2C_Mem_Write(&hi2c1, (uint16_t)(addr7 << 1), reg,
                              I2C_MEMADD_SIZE_8BIT, (uint8_t *)buf, len, 50)
            == HAL_OK) ? 0 : -1;
}

/* 读寄存器。返回 0 成功，非 0 失败 */
static inline int mpu6050_i2c_read(uint8_t addr7, uint8_t reg,
                                   uint8_t *buf, uint16_t len)
{
    return (HAL_I2C_Mem_Read(&hi2c1, (uint16_t)(addr7 << 1), reg,
                             I2C_MEMADD_SIZE_8BIT, buf, len, 50)
            == HAL_OK) ? 0 : -1;
}

#endif /* MPU6050_PORT_H */
