/**
 * hc05_port.h - HC-05 平台适配层（示例：STM32 HAL UART2，115200 或 38400）
 *
 * 移植：只改这个文件。注意 HC-05 是 3.3V TTL 电平，直接接 MCU UART 即可。
 */
#ifndef HC05_PORT_H
#define HC05_PORT_H

#include <stdint.h>
#include "stm32f4xx_hal.h"

extern UART_HandleTypeDef huart2;

static inline int hc05_uart_write(const char *buf, int len)
{
    return HAL_UART_Transmit(&huart2, (uint8_t *)buf, (uint16_t)len, 200) == HAL_OK
           ? len : -1;
}

/* 非阻塞读：当前收不到就返回 0（驱动内部用总超时兜底） */
static inline int hc05_uart_read(char *buf, int size)
{
    return HAL_UART_Receive(&huart2, (uint8_t *)buf, (uint16_t)size, 10) == HAL_OK
           ? size : 0;
}

static inline uint32_t hc05_millis(void) { return HAL_GetTick(); }

#endif /* HC05_PORT_H */
