/**
 * ds18b20.c - DS18B20 驱动实现
 *
 * 结构约定：纯函数（crc8/check_scratchpad/raw_to_temp_x16/is_reset_value）
 * 与总线时序（start_convert/read）严格分离——纯函数可直接在 PC 上单元测试。
 */
#include "ds18b20.h"

/* ---------------- 纯函数区（PC 可测） ---------------- */

uint8_t ds18b20_crc8(const uint8_t *data, int len)
{
    uint8_t crc = 0;
    for (int i = 0; i < len; i++) {
        uint8_t b = data[i];
        for (int j = 0; j < 8; j++) {
            uint8_t mix = (uint8_t)((crc ^ b) & 0x01u);
            crc >>= 1;
            if (mix) {
                crc ^= 0x8Cu;   /* 反射多项式 X^8+X^5+X^4+1 */
            }
            b >>= 1;
        }
    }
    return crc;
}

int ds18b20_check_scratchpad(const uint8_t sp[9])
{
    if (ds18b20_crc8(sp, 8) != sp[8]) {
        return DS18B20_ERR_CRC;
    }
    return DS18B20_OK;
}

int16_t ds18b20_raw_to_temp_x16(uint8_t lsb, uint8_t msb)
{
    /* 12 位分辨率：16bit 补码，LSB = 0.0625°C = 1/16°C */
    return (int16_t)(((uint16_t)msb << 8) | lsb);
}

int ds18b20_is_reset_value(int16_t temp_x16)
{
    /* 上电复位后温度寄存器恒为 85.0°C = 1360 = 0x0550 */
    return (temp_x16 == 850 * 16 / 10) ? 1 : 0;   /* 850/10*16 = 1360 */
}

/* ---------------- 总线时序区（需真实硬件） ---------------- */

/* 单总线复位脉冲 + 应答检测。返回 0=有器件应答，-1=无应答。 */
static int bus_reset(void)
{
    int presence;
    ds18b20_line_out(0);
    ds18b20_delay_us(480);          /* 复位：拉低 ≥480us */
    ds18b20_line_out(1);
    ds18b20_delay_us(70);           /* 等 15~60us 后器件拉低应答 */
    presence = (ds18b20_line_read() == 0) ? 0 : -1;
    ds18b20_delay_us(410);          /* 等待应答时隙结束（共 ≥480us） */
    return presence;
}

static void bus_write_bit(int bit)
{
    ds18b20_line_out(0);
    if (bit) {
        ds18b20_delay_us(6);        /* "1"：拉低 <15us 后释放 */
        ds18b20_line_out(1);
        ds18b20_delay_us(64);
    } else {
        ds18b20_delay_us(60);       /* "0"：拉低 60~120us */
        ds18b20_line_out(1);
        ds18b20_delay_us(10);
    }
}

static int bus_read_bit(void)
{
    int bit;
    ds18b20_line_out(0);
    ds18b20_delay_us(3);            /* 起始 >1us */
    ds18b20_line_out(1);
    ds18b20_delay_us(10);           /* 在 15us 内采样 */
    bit = (ds18b20_line_read() != 0);
    ds18b20_delay_us(47);           /* 读时隙总长 ≥60us */
    return bit;
}

static void bus_write_byte(uint8_t b)
{
    for (int i = 0; i < 8; i++) {
        bus_write_bit(b & 0x01u);
        b >>= 1;
    }
}

static uint8_t bus_read_byte(void)
{
    uint8_t b = 0;
    for (int i = 0; i < 8; i++) {
        b >>= 1;
        if (bus_read_bit()) {
            b |= 0x80u;
        }
    }
    return b;
}

static int _cmd_sequence(uint8_t skip_then_cmd)
{
    if (bus_reset() != 0) {
        return DS18B20_ERR_NO_DEVICE;
    }
    bus_write_byte(0xCC);           /* Skip ROM：单器件总线 */
    bus_write_byte(skip_then_cmd);
    return DS18B20_OK;
}

int ds18b20_start_convert(void)
{
    return _cmd_sequence(0x44);     /* ConvertT */
}

int ds18b20_read(int16_t *out_temp_x16)
{
    uint8_t sp[9];
    if (out_temp_x16 == 0) {
        return DS18B20_ERR_NO_DEVICE;
    }
    /* 转换命令 + 等待（12 位需要 750ms） */
    if (_cmd_sequence(0x44) != 0) {
        return DS18B20_ERR_NO_DEVICE;
    }
    ds18b20_delay_ms(750);
    /* 读 Scratchpad */
    if (_cmd_sequence(0xBE) != 0) { /* Read Scratchpad */
        return DS18B20_ERR_NO_DEVICE;
    }
    for (int i = 0; i < 9; i++) {
        sp[i] = bus_read_byte();
    }
    if (ds18b20_check_scratchpad(sp) != DS18B20_OK) {
        return DS18B20_ERR_CRC;
    }
    *out_temp_x16 = ds18b20_raw_to_temp_x16(sp[0], sp[1]);
    return DS18B20_OK;
}
