/**
 * hcsr04_port.h - HC-SR04 移植适配层（在你的 MCU 工程里实现）
 *
 * 必须提供 4 个接口。echo 计时必须 us 级精度：
 * 推荐 TIM 输入捕获（精度高、不阻塞），下面给的是阻塞轮询的简化版。
 */
#ifndef HCSR04_PORT_H
#define HCSR04_PORT_H

/* ================= STM32 HAL 适配示例（阻塞轮询版） =================
 * 假设 Trig=PA1（输出），Echo=PA2（输入）。
 *
 * #define TRIG_PORT GPIOA
 * #define TRIG_PIN  GPIO_PIN_1
 * #define ECHO_PORT GPIOA
 * #define ECHO_PIN  GPIO_PIN_2
 *
 * static inline void hcsr04_delay_us(uint32_t us) { // 同 DHT11 的 DWT 实现 }
 * static inline void hcsr04_delay_ms(uint32_t ms) { HAL_Delay(ms); }
 * static inline void hcsr04_trig(uint8_t level) {
 *     HAL_GPIO_WritePin(TRIG_PORT, TRIG_PIN, (GPIO_PinState)level);
 * }
 * static inline uint8_t hcsr04_echo_read(void) {
 *     return (uint8_t)HAL_GPIO_ReadPin(ECHO_PORT, ECHO_PIN);
 * }
 * ============================================================== */

/* 进阶：TIM 输入捕获版可把精度从 ±1us 提到 ±0.1us，且不阻塞 CPU。
 * 硬件连接不变，只改 echo 计时实现。毕设答辩提这个是加分点。 */

void     hcsr04_delay_us(uint32_t us);
void     hcsr04_delay_ms(uint32_t ms);
void     hcsr04_trig(uint8_t level);   /* Trig 脚输出 */
uint8_t  hcsr04_echo_read(void);       /* Echo 脚输入 */

#endif /* HCSR04_PORT_H */
