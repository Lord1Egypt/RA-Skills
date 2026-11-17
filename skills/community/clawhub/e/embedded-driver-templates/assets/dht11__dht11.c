/**
 * dht11.c - DHT11 驱动实现（可移植版）
 * 时序依据：DHT11 数据手册（起始 >=18ms，响应 80us+80us，bit: 50us 低 + 26-28us("0")/70us("1") 高）
 */
#include "dht11.h"

/* ---------------- 纯函数（PC 可单元测试） ---------------- */

int dht11_decode_byte(const uint16_t durations_us[8])
{
    int byte = 0;
    for (int i = 0; i < 8; i++) {
        uint16_t d = durations_us[i];
        if (d == 0)
            return -1;              /* 无效时长 */
        if (d <= 20)
            return -2;              /* 高电平过短（<20us 不可能是合法 bit） */
        if (d >= 90)
            return -3;              /* 高电平过长，总线异常 */
        byte <<= 1;
        if (d > 45)                 /* 26-28us=0 / 70us=1，取中值 45us 判分界 */
            byte |= 1;
    }
    return byte & 0xFF;
}

int dht11_checksum(const uint8_t bytes[5])
{
    uint16_t sum = (uint16_t)bytes[0] + bytes[1] + bytes[2] + bytes[3];
    return ((sum & 0xFF) == bytes[4]) ? 0 : -1;
}

int dht11_decode_frame(const uint16_t durations_us[40], dht11_data_t *out)
{
    if (durations_us == 0 || out == 0)
        return -1;

    uint8_t b[5];
    for (int i = 0; i < 5; i++) {
        int byte = dht11_decode_byte(&durations_us[i * 8]);
        if (byte < 0)
            return -1;
        b[i] = (uint8_t)byte;
    }

    if (dht11_checksum(b) != 0)
        return DHT11_ERR_CHECKSUM;

    out->humidity_int = b[0];
    out->humidity_dec = b[1];
    out->temp_int     = b[2];
    out->temp_dec     = b[3];
    return DHT11_OK;
}

/* ---------------- 总线时序（目标机上运行） ---------------- */

/* 读一段高电平时长（us）。超时返回 0xFFFF。
 * 移植提示：若你的 delay_us 精度差（比如基于 HAL_GetTick 的 1ms 粒度），
 * 这里的采样会不可靠 —— 必须用 DWT->CYCCNT 或 TIM 计数实现 us 级延时。 */
static uint16_t measure_high_us(void)
{
    uint16_t t = 0;
    while (dht11_pin_read() == 1) {
        dht11_delay_us(1);
        if (++t > 200)          /* 最长 bit ~80us，200us 一定超时 */
            return 0xFFFF;
    }
    return t;
}

static uint16_t measure_low_us(void)
{
    uint16_t t = 0;
    while (dht11_pin_read() == 0) {
        dht11_delay_us(1);
        if (++t > 200)
            return 0xFFFF;
    }
    return t;
}

int dht11_read(dht11_data_t *out)
{
    if (out == 0)
        return -1;

    uint16_t durations[40];

    /* 1. 起始信号：拉低 >=18ms 再拉高 30us */
    dht11_pin_out(0);
    dht11_delay_ms(20);
    dht11_pin_out(1);
    dht11_delay_us(30);
    dht11_pin_in();             /* 释放总线转输入 */

    /* 2. 器件响应：80us 低 + 80us 高（各留 200us 容差） */
    if (measure_low_us() == 0xFFFF)  return DHT11_ERR_TIMEOUT;
    if (measure_high_us() == 0xFFFF) return DHT11_ERR_TIMEOUT;

    /* 3. 40 bit：每个 bit = 50us 低（值不重要）+ 高电平时长决定 0/1 */
    for (int i = 0; i < 40; i++) {
        uint16_t low = measure_low_us();
        if (low == 0xFFFF)
            return DHT11_ERR_TIMEOUT;
        durations[i] = measure_high_us();
        if (durations[i] == 0xFFFF)
            return DHT11_ERR_TIMEOUT;
    }

    /* 4. 解码+校验（纯函数） */
    return dht11_decode_frame(durations, out);
}
