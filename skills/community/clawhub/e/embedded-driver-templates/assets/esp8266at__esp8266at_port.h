/**
 * esp8266at_port.h - ESP8266-AT 串口适配说明
 *
 * 本库是纯解析库（无总线时序），适配层只需要一条 UART：
 * MCU UART ←→ ESP8266 UART，默认 115200-8N1。
 */
#ifndef ESP8266AT_PORT_H
#define ESP8266AT_PORT_H

/* ===== 移植要点（按你用的 MCU 填三个函数即可） =====
 *
 * 1) uart_send_bytes(const uint8_t *buf, uint16_t len)
 *    阻塞发送。发 AT 指令时结尾必须是 "\r\n"（不是 "\n"！）。
 *
 * 2) uart_recv_line(char *line, uint16_t max_len, uint32_t timeout_ms)
 *    按行接收（以 \n 结尾）。ESP-AT 所有响应都是行式的。
 *
 * 3) esp8266_delay_ms(uint32_t ms)
 *
 * ===== 波特率与接线 =====
 * - 出厂固件 115200 或 9600（部分旧固件），两端必须一致
 * - ESP-01：VCC=3.3V 且电流 ≥500mA（接开发板板载 3.3V 常不够！）
 * - TX/RX 交叉：模块 TX→MCU RX，模块 RX→MCU TX
 * - CH_PD/EN 引脚必须拉高（ESP-01 忘接这根 = 模块完全不工作）
 *
 * ===== 发送变长 TCP 数据的正确姿势 =====
 * AT+CIPSEND=<len>  →  等待 ">" 提示符  →  再发 len 字节数据
 * 没等 ">" 就发数据是最常见的失败原因（本库 esp8266_classify_line
 * 会把 ">" 识别为 ESP8266_LINE_SEND_PROMPT）。
 */

#endif /* ESP8266AT_PORT_H */
