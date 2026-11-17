/**
 * test_driver_logic.c - 驱动纯函数逻辑测试（PC 端，无硬件）
 *
 * 验证项：DHT11 位解码/校验/整帧解码、HC-SR04 换算/量程过滤
 * 编译运行：gcc -Wall -Wextra -o test_driver_logic test_driver_logic.c dht11_stub.c hcsr04_stub.c ..\drivers\dht11\dht11.c ..\drivers\hcsr04\hcsr04.c && ./test_driver_logic
 * （或直接用本目录 Makefile：make -f Makefile.logic test）
 *
 * 验证状态：本机 gcc (mingw64) 实测
 */
#include <stdio.h>
#include <string.h>
#include "dht11.h"
#include "hcsr04.h"
#include "ds18b20.h"
#include "mpu6050.h"
#include "esp8266at.h"
#include "ssd1306.h"
#include "servo_sg90.h"
#include "stepper_28byj48.h"
#include "hc05.h"

static int checks = 0;
static int failed = 0;

#define CHECK(cond, msg) do { \
    checks++; \
    if (!(cond)) { failed++; printf("FAIL L%d: %s\n", __LINE__, msg); } \
    else { printf("ok: %s\n", msg); } \
} while (0)

/* ---- DHT11 ---- */
static void test_dht11(void)
{
    /* decode_byte: 数组元素 = 每个 bit 的高电平时长。28us→0, 70us→1 */
    uint16_t bits0[8] = {28, 28, 28, 28, 28, 28, 28, 28};
    CHECK(dht11_decode_byte(bits0) == 0x00, "decode_byte all-zero bits (28us)");

    uint16_t bits1[8] = {70, 70, 70, 70, 70, 70, 70, 70};
    CHECK(dht11_decode_byte(bits1) == 0xFF, "decode_byte all-one bits (70us)");

    uint16_t mix[8] = {70, 28, 28, 70, 28, 28, 70, 28};  /* 1001 0010 */
    CHECK(dht11_decode_byte(mix) == 0x92, "decode_byte mixed pattern");

    /* 边界：45us 分界 */
    uint16_t edge[8] = {45, 45, 45, 45, 45, 45, 45, 45};
    CHECK(dht11_decode_byte(edge) == 0x00, "decode_byte 45us exactly -> 0 (midpoint)");

    /* 非法时长 */
    uint16_t bad0[8] = {0, 28, 28, 28, 28, 28, 28, 28};
    CHECK(dht11_decode_byte(bad0) == -1, "decode_byte zero duration -> -1");
    uint16_t badlow[8] = {15, 28, 28, 28, 28, 28, 28, 28};
    CHECK(dht11_decode_byte(badlow) == -2, "decode_byte <20us -> -2");
    uint16_t badhigh[8] = {95, 28, 28, 28, 28, 28, 28, 28};
    CHECK(dht11_decode_byte(badhigh) == -3, "decode_byte >=90us -> -3");

    /* checksum: 0x42+0x00+0x19+0x00 = 0x5B */
    uint8_t good[5] = {0x42, 0x00, 0x19, 0x00, 0x5B};
    CHECK(dht11_checksum(good) == 0, "checksum pass");
    uint8_t bad[5] = {0x42, 0x00, 0x19, 0x00, 0x5C};
    CHECK(dht11_checksum(bad) == -1, "checksum fail detect");

    /* 整帧：湿度 42%，温度 25°C */
    uint16_t frame[40];
    const uint8_t expect[5] = {42, 0, 25, 0, 67};
    for (int byte = 0; byte < 5; byte++) {
        for (int bit = 0; bit < 8; bit++) {
            int is_one = (expect[byte] >> (7 - bit)) & 1;
            frame[byte * 8 + bit] = (uint16_t)(is_one ? 70 : 28);
        }
    }
    dht11_data_t d;
    CHECK(dht11_decode_frame(frame, &d) == DHT11_OK, "decode_frame valid frame -> OK");
    CHECK(d.humidity_int == 42 && d.temp_int == 25, "decode_frame values 42%/25C");
    CHECK(d.humidity_dec == 0 && d.temp_dec == 0, "decode_frame decimals zero (DHT11)");

    /* 坏帧：篡改一位高电平时长导致校验失败 */
    frame[39] = (frame[39] == 28) ? 70 : 28;
    CHECK(dht11_decode_frame(frame, &d) == DHT11_ERR_CHECKSUM, "decode_frame corrupted frame -> CHECKSUM error");
}

/* ---- HC-SR04 ---- */
static void test_hcsr04(void)
{
    /* 换算：cm_x10 = us * 1715 / 10000 */
    CHECK(hcsr04_us_to_cm_x10(583) == 99, "583us -> 9.9cm");       /* 手册经典值 ~10cm */
    CHECK(hcsr04_us_to_cm_x10(116) == 19, "116us -> 1.9cm (~2cm min)");
    CHECK(hcsr04_us_to_cm_x10(23300) == 3995, "23300us -> 399.5cm (~4m max)");

    /* 量程过滤 */
    CHECK(hcsr04_us_to_cm_x10(100) == HCSR04_ERR_PARAM, "100us (<2cm) rejected");
    CHECK(hcsr04_us_to_cm_x10(25000) == HCSR04_ERR_PARAM, "25000us (>4m) rejected");

    /* 无回波特征 */
    CHECK(hcsr04_is_no_echo(38000) == 1, "38000us flagged as no-echo");
    CHECK(hcsr04_is_no_echo(3800) == 0, "3800us not no-echo");
}

/* ---- DS18B20 ---- */
static void test_ds18b20(void)
{
    /* CRC8：Dallas 多项式反射 0x8C。期望值与 tests/test_driver_logic_py.py 同源 */
    uint8_t z = 0x00;
    CHECK(ds18b20_crc8(&z, 1) == 0x00, "crc8 single 0x00 -> 0x00");
    uint8_t two = 0x02;
    CHECK(ds18b20_crc8(&two, 1) == 0xBC, "crc8 single 0x02 -> 0xBC");
    uint8_t zeros[8] = {0, 0, 0, 0, 0, 0, 0, 0};
    CHECK(ds18b20_crc8(zeros, 8) == 0x00, "crc8 eight zeros -> 0x00");

    /* 温度换算（12 位补码） */
    CHECK(ds18b20_raw_to_temp_x16(0x91, 0x01) == 401, "raw 0x0191 -> +25.0625C (x16=401)");
    CHECK(ds18b20_raw_to_temp_x16(0x5E, 0xFF) == -162, "raw 0xFF5E -> -10.125C (x16=-162)");
    CHECK(ds18b20_raw_to_temp_x16(0x10, 0xFE) == -496, "raw 0xFE10 -> -31.0C (x16=-496)");

    /* 复位值 85.0°C = 1360 */
    CHECK(ds18b20_is_reset_value(1360) == 1, "1360 flagged as reset value (85.0C)");
    CHECK(ds18b20_is_reset_value(400) == 0, "400 not reset value");

    /* scratchpad 校验：前 8 字节 CRC 应等于第 9 字节（8x00 + crc=0x00 平凡样例） */
    uint8_t sp[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0x00};
    CHECK(ds18b20_check_scratchpad(sp) == DS18B20_OK, "scratchpad all-zero CRC pass");
    sp[8] = 0x5A;
    CHECK(ds18b20_check_scratchpad(sp) == DS18B20_ERR_CRC, "scratchpad bad CRC detected");
}

/* ---- MPU6050 ---- */
static void test_mpu6050(void)
{
    /* 加速度：±2g 档 16384 = 1g = 1000mg */
    CHECK(mpu6050_raw_to_mg(16384, 0) == 1000, "accel 16384 @2g -> 1000mg");
    CHECK(mpu6050_raw_to_mg(-16384, 0) == -1000, "accel -16384 @2g -> -1000mg");
    CHECK(mpu6050_raw_to_mg(8192, 0) == 500, "accel 8192 @2g -> 500mg");
    CHECK(mpu6050_raw_to_mg(16384, 1) == 2000, "accel 16384 @4g -> 2000mg");

    /* 角速度：±250dps 档 raw 131 ≈ 1dps（整数截断 99） */
    CHECK(mpu6050_raw_to_dps_centi(131, 0) == 99, "gyro 131 @250dps -> 99 (0.99dps)");

    /* 温度：Temp = raw/340 + 36.53 */
    CHECK(mpu6050_temp_c_x100(0) == 3653, "temp raw 0 -> 36.53C");
    CHECK(mpu6050_temp_c_x100(340) == 3753, "temp raw 340 -> 37.53C");
    CHECK(mpu6050_temp_c_x100(-340) == 3553, "temp raw -340 -> 35.53C");

    /* 静止自检：静止合成 ≈1g */
    CHECK(mpu6050_static_check(0, 0, 16384) == 1, "static check 1g on z pass");
    CHECK(mpu6050_static_check(0, 0, 0) == 0, "static check all-zero fail");
    CHECK(mpu6050_static_check(0, 0, 24576) == 0, "static check 1.5g fail");
}

/* ---- ESP8266-AT ---- */
static void test_esp8266at(void)
{
    CHECK(esp8266_classify_line("OK\r\n") == ESP8266_LINE_OK, "classify OK");
    CHECK(esp8266_classify_line("ERROR\r\n") == ESP8266_LINE_ERROR, "classify ERROR");
    CHECK(esp8266_classify_line("WIFI CONNECTED\r\n") == ESP8266_LINE_WIFI_CONNECTED, "classify WIFI CONNECTED");
    CHECK(esp8266_classify_line("WIFI GOT IP\r\n") == ESP8266_LINE_WIFI_GOT_IP, "classify WIFI GOT IP");
    CHECK(esp8266_classify_line("+IPD,12:hello") == ESP8266_LINE_IPD, "classify +IPD");
    CHECK(esp8266_classify_line("busy p...\r\n") == ESP8266_LINE_BUSY, "classify busy");
    CHECK(esp8266_classify_line(">\r\n") == ESP8266_LINE_SEND_PROMPT, "classify send prompt '>'");
    CHECK(esp8266_classify_line("AT+RST\r\n") == ESP8266_LINE_OTHER, "classify other");

    CHECK(esp8266_cwjap_err(2) == ESP8266_JAP_BAD_PASS, "cwjap code 2 = wrong password");
    CHECK(esp8266_cwjap_err(5) == ESP8266_JAP_UNKNOWN, "cwjap code 5 = unknown");

    int ch = -9, len = 0, off = 0;
    CHECK(esp8266_ipd_parse("+IPD,12:hello,world!", &ch, &len, &off) == 0, "ipd single parse ok");
    CHECK(ch == -1 && len == 12 && off == 8, "ipd single values ch=-1 len=12 off=8");
    CHECK(esp8266_ipd_parse("+IPD,0,5:hello", &ch, &len, &off) == 0, "ipd multi parse ok");
    CHECK(ch == 0 && len == 5 && off == 9, "ipd multi values ch=0 len=5 off=9");
    CHECK(esp8266_ipd_parse("garbage", &ch, &len, &off) == -1, "ipd malformed -> -1");
    CHECK(esp8266_ipd_parse("+IPD,abc", &ch, &len, &off) == -1, "ipd non-numeric -> -1");
}

/* ---- SSD1306 ---- */
static void test_ssd1306(void)
{
    uint16_t idx = 9999;
    uint8_t bit = 9;
    CHECK(ssd1306_coord_to_fb(0, 0, &idx, &bit) == SSD1306_OK && idx == 0 && bit == 0,
          "coord (0,0) -> fb[0] bit0");
    CHECK(ssd1306_coord_to_fb(5, 9, &idx, &bit) == SSD1306_OK && idx == 133 && bit == 1,
          "coord (5,9) -> fb[133] bit1 (page 1)");
    CHECK(ssd1306_coord_to_fb(127, 63, &idx, &bit) == SSD1306_OK && idx == 1023 && bit == 7,
          "coord (127,63) -> fb[1023] bit7 (last byte)");
    CHECK(ssd1306_coord_to_fb(128, 0, &idx, &bit) == SSD1306_ERR_PARAM, "coord x=128 -> param err");
    CHECK(ssd1306_coord_to_fb(0, 64, &idx, &bit) == SSD1306_ERR_PARAM, "coord y=64 -> param err");

    ssd1306_fb_clear();
    CHECK(ssd1306_fb_set_pixel(0, 0) == SSD1306_OK, "set_pixel (0,0)");
    CHECK(ssd1306_fb_set_pixel(0, 1) == SSD1306_OK, "set_pixel (0,1)");
    CHECK(ssd1306_fb[0] == 0x03, "two pixels in same byte -> 0b00000011");
    CHECK(ssd1306_fb_set_pixel(128, 0) == SSD1306_ERR_PARAM, "set_pixel out of range");

    CHECK(ssd1306_ascii_index(' ') == 0, "ascii index space=0");
    CHECK(ssd1306_ascii_index('A') == 33, "ascii index A=33");
    CHECK(ssd1306_ascii_index('\n') == 0, "ascii non-printable maps to 0");
}

/* ---- SG90 舵机 ---- */
static void test_servo(void)
{
    CHECK(servo_angle_to_pulse_us(0) == 500, "angle 0 -> 500us");
    CHECK(servo_angle_to_pulse_us(180) == 2500, "angle 180 -> 2500us");
    CHECK(servo_angle_to_pulse_us(90) == 1500, "angle 90 -> 1500us (center)");
    CHECK(servo_angle_to_pulse_us(45) == 1000, "angle 45 -> 1000us");
    CHECK(servo_angle_to_pulse_us(-1) == -1, "angle negative -> -1");
    CHECK(servo_angle_to_pulse_us(181) == -2, "angle >180 -> -2");

    /* 72MHz / (71+1) = 1MHz tick，ARR=19999 -> 20ms(50Hz) */
    CHECK(servo_pulse_to_ccr(1500, 72000000, 71, 19999) == 1500, "ccr 1500us @1MHz tick");
    CHECK(servo_pulse_to_ccr(500, 72000000, 71, 19999) == 500, "ccr 500us @1MHz tick");
    /* PSC=35 -> 2MHz tick -> 周期 10ms，不是 50Hz */
    CHECK(servo_pulse_to_ccr(1500, 72000000, 35, 19999) == -1, "period 10ms rejected (-1)");
}

/* ---- 28BYJ-48 步进 ---- */
static void test_stepper(void)
{
    CHECK(stepper_steps_per_rev(1) == 4076, "halfstep 4076 steps/rev (gear 63.684:1)");
    CHECK(stepper_steps_per_rev(0) == 2038, "fullstep 2038 steps/rev");
    CHECK(stepper_angle_to_steps(90, 1) == 1019, "90 deg halfstep -> 1019");
    CHECK(stepper_angle_to_steps(90, 0) == 510, "90 deg fullstep -> 510 (509.5 rounded)");
    CHECK(stepper_angle_to_steps(360, 1) == 4076, "360 deg halfstep -> 4076");
    CHECK(stepper_angle_to_steps(-90, 1) == -1019, "-90 deg -> -1019 (reverse)");

    /* 半步 8 拍：0001 0011 0010 0110 0100 1100 1000 1001 */
    CHECK(stepper_phase_pattern(0, 1) == 0x1, "halfstep phase[0] = 0001");
    CHECK(stepper_phase_pattern(1, 1) == 0x3, "halfstep phase[1] = 0011");
    CHECK(stepper_phase_pattern(7, 1) == 0x9, "halfstep phase[7] = 1001");
    CHECK(stepper_phase_pattern(8, 1) == 0x1, "halfstep idx wraps at 8");
    CHECK(stepper_phase_pattern(0, 0) == 0x3, "fullstep phase[0] = 0011 (dual-phase)");

    CHECK(stepper_rpm_to_delay_us(15, 1) == 981, "15rpm halfstep -> 981us/step");
    CHECK(stepper_rpm_to_delay_us(0, 1) == -1, "rpm<=0 -> -1");
    CHECK(stepper_rpm_to_delay_us(60, 1) == -2, "rpm>18 -> -2 (torque limit)");
}

/* ---- HC-05 AT 助手 ---- */
static void test_hc05(void)
{
    CHECK(hc05_classify("OK") == HC05_OK, "classify OK");
    CHECK(hc05_classify("ERROR") == HC05_ERROR, "classify ERROR");
    CHECK(hc05_classify("ERROR:(1)") == HC05_ERROR, "classify ERROR:(n) as ERROR");
    CHECK(hc05_classify("FAIL") == HC05_FAIL, "classify FAIL");
    CHECK(hc05_classify("+NAME:HC-05") == HC05_DATA, "classify +NAME as DATA");
    CHECK(hc05_classify("") == HC05_IGNORE, "classify empty as IGNORE");
    CHECK(hc05_classify("hello") == HC05_UNKNOWN, "classify other as UNKNOWN");

    CHECK(hc05_error_detail("ERROR:(1)") == 1, "error detail 1");
    CHECK(hc05_error_detail("ERROR:(4)") == 4, "error detail 4");
    CHECK(hc05_error_detail("OK") == -1, "error detail on non-error -> -1");

    char buf[64];
    CHECK(hc05_uart_cmd(9600, 0, 0, buf, sizeof(buf)) > 0 &&
          strcmp(buf, "AT+UART=9600,0,0\r\n") == 0, "uart cmd 9600 generated");
    CHECK(hc05_uart_cmd(115200, 1, 2, buf, sizeof(buf)) > 0 &&
          strcmp(buf, "AT+UART=115200,1,2\r\n") == 0, "uart cmd 115200 generated");
    CHECK(hc05_uart_cmd(1234, 0, 0, buf, sizeof(buf)) == -2, "baud not in table -> -2");
    CHECK(hc05_uart_cmd(9600, 2, 0, buf, sizeof(buf)) == -3, "stop=2 invalid -> -3");
    CHECK(hc05_uart_cmd(9600, 0, 5, buf, sizeof(buf)) == -4, "parity=5 invalid -> -4");
}

int main(void)
{
    printf("=== DHT11 logic ===\n");
    test_dht11();
    printf("=== HC-SR04 logic ===\n");
    test_hcsr04();
    printf("=== DS18B20 logic ===\n");
    test_ds18b20();
    printf("=== MPU6050 logic ===\n");
    test_mpu6050();
    printf("=== ESP8266-AT logic ===\n");
    test_esp8266at();
    printf("=== SSD1306 logic ===\n");
    test_ssd1306();
    printf("=== SG90 servo logic ===\n");
    test_servo();
    printf("=== 28BYJ-48 stepper logic ===\n");
    test_stepper();
    printf("=== HC-05 logic ===\n");
    test_hc05();
    printf("\nSummary: %d checks, %d failed\n", checks, failed);
    return failed == 0 ? 0 : 1;
}
