/**
 * dht11.h - DHT11 温湿度传感器驱动（可移植版）
 *
 * 适用：STM32 HAL/LL、Arduino、任何 MCU —— 只需在 dht11_port.h 提供 5 个接口
 * 特性：C99、无动态内存、解码与校验逻辑为纯函数（PC 上可单元测试）
 *
 * 用法：
 *   dht11_data_t d;
 *   if (dht11_read(&d) == DHT11_OK) {
 *       // d.humidity_int / d.humidity_dec / d.temp_int / d.temp_dec
 *   }
 *
 * 验证记录：见本目录 meta.txt
 */
#ifndef DHT11_H
#define DHT11_H

#include <stdint.h>

#define DHT11_OK            0
#define DHT11_ERR_TIMEOUT  -1   /* 总线无响应：查接线/上拉电阻 */
#define DHT11_ERR_CHECKSUM -2   /* 40bit 收到了但校验和不对：时序被中断打断 */

typedef struct {
    uint8_t humidity_int;   /* 湿度整数部分（DHT11 小数位恒 0） */
    uint8_t humidity_dec;
    uint8_t temp_int;       /* 温度整数部分 */
    uint8_t temp_dec;
} dht11_data_t;

/* ---- 移植适配层：在 dht11_port.h 中实现 ---- */
#include <dht11_port.h>   /* 提供 dht11_delay_us(ms) / dht11_delay_ms(ms)
                             dht11_pin_out(level) / dht11_pin_in() / dht11_pin_read() */

/* 高电平持续时间解码 1 字节（8 bit）。durations_us 为每个 bit 的高电平时长。
 * DHT11 协议：高电平 ~26-28us = "0"，~70us = "1"。
 * 纯函数，PC 可测。返回低 8 位数据；bit 数不足返回负数。 */
int dht11_decode_byte(const uint16_t durations_us[8]);

/* 5 字节报文校验：前 4 字节之和的低 8 位应等于第 5 字节。纯函数。 */
int dht11_checksum(const uint8_t bytes[5]);

/* 从 40 个 bit 时长解码完整数据。纯函数（不含总线时序）。 */
int dht11_decode_frame(const uint16_t durations_us[40], dht11_data_t *out);

/* 阻塞读取一次温湿度（内部完成起始信号+响应检测+40bit 采样+校验）。
 * 调用间隔应 >= 1s（DHT11 采样率 1Hz）。读时序期间会短暂关中断（见 .c）。 */
int dht11_read(dht11_data_t *out);

#endif /* DHT11_H */
