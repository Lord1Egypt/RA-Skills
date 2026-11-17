/**
 * ssd1306.h - SSD1306 0.96" OLED 驱动（可移植版，I2C 页寻址 + 帧缓冲）
 *
 * 适用：任何 MCU —— 在 ssd1306_port.h 提供 I2C 写 + 延时即可
 * 特性：C99；坐标换算/帧缓冲位操作为纯函数（PC 可单元测试）
 *
 * 帧缓冲模式：128x64 = 1024 字节，全部画完后一次刷屏（I2C 传 1024+ 字节）。
 * 用法：
 *   ssd1306_fb_clear();
 *   ssd1306_fb_set_pixel(10, 20);
 *   ssd1306_flush();
 *
 * 验证记录：见本目录 meta.json
 */
#ifndef SSD1306_DRIVER_H
#define SSD1306_DRIVER_H

#include <stdint.h>

#define SSD1306_OK            0
#define SSD1306_ERR_PARAM    -1   /* 坐标越界等参数错误 */

#define SSD1306_W            128
#define SSD1306_H            64
#define SSD1306_FB_SIZE      (SSD1306_W * SSD1306_H / 8)   /* 1024 字节 */

#define SSD1306_I2C_ADDR     0x3C   /* 少数模块为 0x3D（SA0 接高） */

/* 帧缓冲（调用方分配或用驱动内置静态缓冲二选一，见 .c） */
extern uint8_t ssd1306_fb[SSD1306_FB_SIZE];

/* ---- 移植适配层：在 ssd1306_port.h 中实现 ---- */
#include <ssd1306_port.h>   /* 提供 ssd1306_i2c_write_cmd(byte)
                                                          ssd1306_i2c_write_data(buf, len)
                                                          ssd1306_delay_ms(ms) */

/* 坐标 → 页寻址换算。纯函数。page=y/8, bit=y%8, fb 下标 = page*128+x。
 * 返回 SSD1306_OK 或 SSD1306_ERR_PARAM（越界）。 */
int ssd1306_coord_to_fb(uint8_t x, uint8_t y, uint16_t *fb_index, uint8_t *bit);

/* 帧缓冲清空。纯函数。 */
void ssd1306_fb_clear(void);

/* 帧缓冲置 1 个像素。纯函数。返回 SSD1306_OK / SSD1306_ERR_PARAM。 */
int ssd1306_fb_set_pixel(uint8_t x, uint8_t y);

/* 5x7 ASCII 字库索引：' ' (0x20) ~ '~' (0x7E)。纯函数。
 * 越界字符返回 0（映射到空格）。 */
uint8_t ssd1306_ascii_index(char c);

/* 初始化（发送官方 datasheet 初始化序列，约 25 条命令）。 */
int ssd1306_init(void);

/* 全屏刷新：把整个帧缓冲推给 OLED。I2C @400kHz 约 25ms。 */
int ssd1306_flush(void);

#endif /* SSD1306_DRIVER_H */
