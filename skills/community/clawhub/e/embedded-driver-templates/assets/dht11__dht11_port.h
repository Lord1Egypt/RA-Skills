/**
 * dht11_port.h - DHT11 移植适配层（在你的 MCU 工程里实现）
 *
 * 必须提供 5 个接口。以下给出 STM32 HAL 与 Arduino 两种实现示例。
 * ⚠ delay_us 必须 us 级精度（DWT/TIM 实现），HAL_Delay 只有 ms 粒度不能用，
 *   这是 DHT11 "读出来全是 0 或超时" 的头号原因。
 */
#ifndef DHT11_PORT_H
#define DHT11_PORT_H

/* ================= STM32 HAL（CubeMX）适配示例 =================
 * 假设数据脚 = PA0，在 CubeMX 里配成 GPIO_Output（读时动态切输入）。
 *
 * #include "main.h"
 *
 * #define DHT_PORT  GPIOA
 * #define DHT_PIN   GPIO_PIN_0
 *
 * static inline void dht11_delay_us(uint32_t us) {
 *     uint32_t start = DWT->CYCCNT;
 *     uint32_t ticks = us * (SystemCoreClock / 1000000U);
 *     while ((DWT->CYCCNT - start) < ticks) {}
 * }
 * static inline void dht11_delay_ms(uint32_t ms) { HAL_Delay(ms); }
 * static inline void dht11_pin_out(uint8_t level) {
 *     GPIO_InitTypeDef g = {0};
 *     g.Pin = DHT_PIN; g.Mode = GPIO_MODE_OUTPUT_PP; g.Speed = GPIO_SPEED_FREQ_HIGH;
 *     HAL_GPIO_Init(DHT_PORT, &g);
 *     HAL_GPIO_WritePin(DHT_PORT, DHT_PIN, (GPIO_PinState)level);
 * }
 * static inline void dht11_pin_in(void) {
 *     GPIO_InitTypeDef g = {0};
 *     g.Pin = DHT_PIN; g.Mode = GPIO_MODE_INPUT; g.Pull = GPIO_PULLUP;
 *     HAL_GPIO_Init(DHT_PORT, &g);
 * }
 * static inline uint8_t dht11_pin_read(void) {
 *     return (uint8_t)HAL_GPIO_ReadPin(DHT_PORT, DHT_PIN);
 * }
 *
 * DWT 使能（main 里调一次）：
 *   CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
 *   DWT->CYCCNT = 0;
 *   DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
 * ============================================================== */

/* ================= Arduino 适配示例 =================
 * static inline void dht11_delay_us(uint32_t us) { delayMicroseconds(us); }
 * static inline void dht11_delay_ms(uint32_t ms) { delay(ms); }
 * // pin 模式切换用 pinMode / digitalWrite / digitalRead
 * ============================================================== */

void     dht11_delay_us(uint32_t us);
void     dht11_delay_ms(uint32_t ms);
void     dht11_pin_out(uint8_t level);   /* 推挽输出并置电平 */
void     dht11_pin_in(void);             /* 切高阻输入（带上拉） */
uint8_t  dht11_pin_read(void);           /* 读电平 */

#endif /* DHT11_PORT_H */
