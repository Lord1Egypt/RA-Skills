/**
 * ds18b20.h - DS18B20 数字温度传感器驱动（可移植版）
 *
 * 适用：任何 MCU —— 只需在 ds18b20_port.h 提供微秒延时 + 单总线 GPIO 操作
 * 特性：C99、无动态内存；CRC/换算/校验为纯函数（PC 上可单元测试）
 *
 * 用法：
 *   ds18b20_start_convert();          // 发 0xCC 0x44
 *   ds18b20_delay_ms(750);            // 12 位分辨率必须等满 750ms
 *   if (ds18b20_read(&t_x16) == DS18B20_OK) {   // t_x16 = 温度×16
 *       // t_x16 / 16 = 摄氏度；注意 85.0°C 是复位值（见 ds18b20_is_reset_value）
 *   }
 *
 * 验证记录：见本目录 meta.json
 */
#ifndef DS18B20_H
#define DS18B20_H

#include <stdint.h>

#define DS18B20_OK             0
#define DS18B20_ERR_CRC       -1   /* Scratchpad CRC 不对：时序被中断打断/上拉不足 */
#define DS18B20_ERR_NO_DEVICE -2   /* 总线无应答：接线/上拉/供电问题 */

/* ---- 移植适配层：在 ds18b20_port.h 中实现 ---- */
#include <ds18b20_port.h>   /* 提供 ds18b20_delay_us / ds18b20_delay_ms
                               ds18b20_line_out(level) / ds18b20_line_in() / ds18b20_line_read() */

/* Dallas/Maxim CRC8（多项式 X^8+X^5+X^4+1，反射形式 0x8C）。
 * 纯函数，PC 可测。输入数据返回 1 字节 CRC。 */
uint8_t ds18b20_crc8(const uint8_t *data, int len);

/* Scratchpad 9 字节校验：前 8 字节 CRC 应等于第 9 字节。纯函数。
 * 返回 DS18B20_OK / DS18B20_ERR_CRC。 */
int ds18b20_check_scratchpad(const uint8_t sp[9]);

/* 温度寄存器换算（12 位分辨率，默认配置）：(msb<<8)|lsb 为补码，×0.0625°C。
 * 纯函数。返回温度×16 的整数（即 raw 本身），保留符号。 */
int16_t ds18b20_raw_to_temp_x16(uint8_t lsb, uint8_t msb);

/* 检测是否为上电复位值 85.0°C：是则说明转换命令没生效（没发 0x44/
 * 等待不足 750ms/寄生供电电流不够）。纯函数。 */
int ds18b20_is_reset_value(int16_t temp_x16);

/* 阻塞读取一次温度（起始信号→Skip ROM→ConvertT→等待→读 Scratchpad→CRC）。
 * 注意：内部等待 750ms，阻塞型；不要在中断上下文调用。 */
int ds18b20_read(int16_t *out_temp_x16);

/* 只发转换命令（非阻塞用法）：发 0xCC 0x44 后自行等待 ≥750ms 再调 ds18b20_read。 */
int ds18b20_start_convert(void);

#endif /* DS18B20_H */
