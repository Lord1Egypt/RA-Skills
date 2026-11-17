/**
 * ssd1306.c - SSD1306 驱动实现
 *
 * 结构约定：坐标/帧缓冲纯函数与 I2C 传输严格分离。
 */
#include "ssd1306.h"

uint8_t ssd1306_fb[SSD1306_FB_SIZE];

/* ---------------- 纯函数区（PC 可测） ---------------- */

int ssd1306_coord_to_fb(uint8_t x, uint8_t y, uint16_t *fb_index, uint8_t *bit)
{
    if (x >= SSD1306_W || y >= SSD1306_H) {
        return SSD1306_ERR_PARAM;
    }
    if (fb_index) {
        *fb_index = (uint16_t)(y / 8) * SSD1306_W + x;   /* 页寻址：每页 8 行 ×128 列 */
    }
    if (bit) {
        *bit = (uint8_t)(y % 8);
    }
    return SSD1306_OK;
}

void ssd1306_fb_clear(void)
{
    for (int i = 0; i < SSD1306_FB_SIZE; i++) {
        ssd1306_fb[i] = 0;
    }
}

int ssd1306_fb_set_pixel(uint8_t x, uint8_t y)
{
    uint16_t idx;
    uint8_t bit;
    if (ssd1306_coord_to_fb(x, y, &idx, &bit) != SSD1306_OK) {
        return SSD1306_ERR_PARAM;
    }
    ssd1306_fb[idx] |= (uint8_t)(1u << bit);
    return SSD1306_OK;
}

uint8_t ssd1306_ascii_index(char c)
{
    if (c < ' ' || c > '~') {
        return 0;   /* 非可打印字符映射为空格 */
    }
    return (uint8_t)(c - ' ');
}

/* ---------------- I2C 传输区（需真实硬件） ---------------- */

int ssd1306_init(void)
{
    /* 官方 datasheet 初始化序列（128x64, I2C, 电荷泵开） */
    static const uint8_t init_cmds[] = {
        0xAE,       /* display off */
        0xD5, 0x80, /* clock div */
        0xA8, 0x3F, /* multiplex 1/64 */
        0xD3, 0x00, /* display offset 0 */
        0x40,       /* start line 0 */
        0x8D, 0x14, /* charge pump ON（没这步屏不亮，高频坑） */
        0x20, 0x00, /* 水平寻址模式（本驱动按页寻址刷，也可用 0x02 页模式） */
        0xA1,       /* segment remap */
        0xC8,       /* COM 扫描方向：上下不反 */
        0xDA, 0x12, /* COM pins 128x64 */
        0x81, 0xCF, /* contrast（0~255，屏暗调大） */
        0xD9, 0xF1, /* precharge */
        0xDB, 0x40, /* VCOM detect */
        0xA4,       /* 显示跟随 RAM 内容（0xA5 全亮点测试用） */
        0xA6,       /* 正常显示（非反色） */
        0xAF,       /* display ON（必须最后发） */
    };
    for (unsigned i = 0; i < sizeof(init_cmds); i++) {
        if (ssd1306_i2c_write_cmd(init_cmds[i]) != 0) {
            return -1;
        }
    }
    ssd1306_fb_clear();
    return 0;
}

int ssd1306_flush(void)
{
    /* 列地址归 0、页地址归 0，然后整帧推出去 */
    (void)ssd1306_i2c_write_cmd(0x21);  /* set column range */
    (void)ssd1306_i2c_write_cmd(0x00);
    (void)ssd1306_i2c_write_cmd(0x7F);
    (void)ssd1306_i2c_write_cmd(0x22);  /* set page range */
    (void)ssd1306_i2c_write_cmd(0x00);
    (void)ssd1306_i2c_write_cmd(0x07);
    return (ssd1306_i2c_write_data(ssd1306_fb, SSD1306_FB_SIZE) == 0) ? SSD1306_OK : -1;
}
