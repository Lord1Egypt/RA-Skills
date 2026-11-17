/**
 * PC 测试桩：把 dht11_port.h / hcsr04_port.h 的接口做成空实现。
 * 只编译逻辑函数（decode/checksum/换算），不测真总线时序。
 * 编译时用 -I stub 让驱动 include 到这里。
 */
#ifndef PORT_STUB_H
#define PORT_STUB_H

#include <stdint.h>

/* dht11_port.h 桩 */
static inline void    dht11_delay_us(uint32_t us) { (void)us; }
static inline void    dht11_delay_ms(uint32_t ms) { (void)ms; }
static inline void    dht11_pin_out(uint8_t l)    { (void)l; }
static inline void    dht11_pin_in(void)          { }
static inline uint8_t dht11_pin_read(void)        { return 0; }

/* hcsr04_port.h 桩 */
static inline void    hcsr04_delay_us(uint32_t us) { (void)us; }
static inline void    hcsr04_delay_ms(uint32_t ms) { (void)ms; }
static inline void    hcsr04_trig(uint8_t l)       { (void)l; }
static inline uint8_t hcsr04_echo_read(void)       { return 0; }

/* ds18b20_port.h 桩 */
static inline void    ds18b20_delay_us(uint32_t us) { (void)us; }
static inline void    ds18b20_delay_ms(uint32_t ms) { (void)ms; }
static inline void    ds18b20_line_out(int l)       { (void)l; }
static inline void    ds18b20_line_in(void)         { }
static inline int     ds18b20_line_read(void)       { return 0; }

/* mpu6050_port.h 桩 */
static inline void mpu6050_delay_ms(uint32_t ms) { (void)ms; }
static inline int  mpu6050_i2c_write(uint8_t a, uint8_t r, const uint8_t *b, uint16_t l)
{ (void)a; (void)r; (void)b; (void)l; return 0; }
static inline int  mpu6050_i2c_read(uint8_t a, uint8_t r, uint8_t *b, uint16_t l)
{ (void)a; (void)r; (void)b; (void)l; return 0; }

/* ssd1306_port.h 桩 */
static inline void ssd1306_delay_ms(uint32_t ms) { (void)ms; }
static inline int  ssd1306_i2c_write_cmd(uint8_t c)  { (void)c; return 0; }
static inline int  ssd1306_i2c_write_data(const uint8_t *b, uint16_t l)
{ (void)b; (void)l; return 0; }

/* servo_sg90_port.h 桩 */
static inline uint32_t servo_tim_clk_hz(void)  { return 72000000U; }
static inline uint32_t servo_psc_default(void) { return 71; }
static inline uint32_t servo_arr_default(void) { return 19999; }
static inline void servo_pwm_write_ccr(int ccr) { (void)ccr; }

/* stepper_28byj48_port.h 桩 */
static inline void stepper_write_phase(int pattern) { (void)pattern; }
static inline void stepper_delay_us(uint32_t us)    { (void)us; }

/* hc05_port.h 桩（UART 无回环：read 恒 0，只测纯函数） */
static inline int hc05_uart_write(const char *buf, int len) { (void)buf; return len; }
static inline int hc05_uart_read(char *buf, int size)       { (void)buf; (void)size; return 0; }
static inline uint32_t hc05_millis(void)                    { return 0; }

/* 让驱动的 #include "xxx_port.h" 落到本桩 */
#define DHT11_PORT_STUB_via 1
#define HCSR04_PORT_STUB_via 1
#define DS18B20_PORT_STUB_via 1
#define MPU6050_PORT_STUB_via 1
#define SSD1306_PORT_STUB_via 1
#define SERVO_SG90_PORT_STUB_via 1
#define STEPPER_28BYJ48_PORT_STUB_via 1
#define HC05_PORT_STUB_via 1

#endif /* PORT_STUB_H */
