/**
 * ssd1306_port.h - SSD1306 平台适配层（示例：STM32 HAL I2C1 @400kHz）
 *
 * 移植：只改这个文件。I2C 地址 0x3C（写地址字节 = 0x78，HAL 自动左移）。
 */
#ifndef SSD1306_PORT_H
#define SSD1306_PORT_H

#include <stdint.h>

#include "stm32f4xx_hal.h"
extern I2C_HandleTypeDef hi2c1;

static inline void ssd1306_delay_ms(uint32_t ms)
{
    HAL_Delay(ms);
}

/* 写一条命令：I2C 先发控制字节 0x00，再发命令字节 */
static inline int ssd1306_i2c_write_cmd(uint8_t cmd)
{
    uint8_t buf[2] = {0x00, cmd};
    return (HAL_I2C_Master_Transmit(&hi2c1, (uint16_t)(SSD1306_I2C_ADDR << 1),
                                    buf, 2, 20) == HAL_OK) ? 0 : -1;
}

/* 写数据：控制字节 0x40 表示"接下来是显存数据"，之后可连发整帧 */
static inline int ssd1306_i2c_write_data(const uint8_t *buf, uint16_t len)
{
    /* HAL 单次传输上限以内可一次发完（1024+1 字节）；部分 HAL 版本需分批发 */
    static uint8_t tmp[SSD1306_FB_SIZE + 1];
    tmp[0] = 0x40;
    for (uint16_t i = 0; i < len; i++) {
        tmp[i + 1] = buf[i];
    }
    return (HAL_I2C_Master_Transmit(&hi2c1, (uint16_t)(SSD1306_I2C_ADDR << 1),
                                    tmp, (uint16_t)(len + 1), 200) == HAL_OK) ? 0 : -1;
}

#endif /* SSD1306_PORT_H */
