/**
 * hc05.h - HC-05 蓝牙串口模块 AT 命令助手（可移植版）
 *
 * 适用：任何 MCU/PC，只需在 hc05_port.h 提供 UART 收发
 * 特性：C99、无动态内存、响应分类/命令生成全为纯函数（PC 上可单元测试）
 *
 * 核心知识（新手最常翻车的地方）：
 *   - AT 模式波特率是 38400（不是透传的 9600！），EN/KEY 脚拉高后上电进入
 *   - 透传模式下发 AT 没有任何反应（它不是命令模式）——像"坏了"其实是模式不对
 *   - HC-05 和 HC-06 是两套 AT 命令集（详见 wiring.md 坑 5）
 *
 * 用法：
 *   hc05_send_cmd_line("AT\r\n");              // 适配层把字符串发出去
 *   hc05_result_t r = hc05_wait_response(2000);
 *   if (r == HC05_OK) { ... }
 *
 * 验证记录：见本目录 meta.json
 */
#ifndef HC05_H
#define HC05_H

#include <stdint.h>

/* ---- 移植适配层：在 hc05_port.h 中实现 ---- */
#include <hc05_port.h>   /* 提供 hc05_uart_write(buf, len) / hc05_uart_read(buf, size)
                            hc05_millis() */

/* AT 响应分类结果 */
typedef enum {
    HC05_OK = 0,        /* 行内容 == "OK"：命令执行成功 */
    HC05_ERROR,         /* "ERROR" 或 "ERROR:(n)"：命令被拒绝 */
    HC05_FAIL,          /* "FAIL"：连接/配对类命令失败（AT+INQ/AT+LINK 等） */
    HC05_DATA,          /* "+NAME:..." / "+VERSION:..." 数据行 */
    HC05_IGNORE,        /* 空行 / \r\n 噪声 */
    HC05_UNKNOWN        /* 其他内容（透传数据或非预期输出） */
} hc05_result_t;

/* 单行响应分类。line 不含行尾 \r\n。纯函数（PC 可测）。 */
hc05_result_t hc05_classify(const char *line);

/* ERROR:(n) 细分码提取。line 形如 "ERROR:(1)" 时返回 1，非 ERROR:(n) 返回 -1。
 * 纯函数（PC 可测）。 */
int hc05_error_detail(const char *line);

/* 生成 AT+UART= 命令写进 buf（含 \r\n 结尾，NUL 结束）。
 * baud 合法值：1200/2400/4800/9600/19200/38400/57600/115200/230400/460800/921600/1382400
 * stop：0=1 位 1=2 位；parity：0=None 1=Odd 2=Even。
 * 纯函数。返回写入长度（不含 NUL）；参数非法返回负数。 */
int hc05_uart_cmd(long baud, int stop, int parity, char *buf, int size);

/* 发送一行 AT 命令并等待响应（目标机上运行）。
 * timeout_ms 内收到 OK/ERROR/FAIL 即返回对应值，超时返回 HC05_UNKNOWN。 */
hc05_result_t hc05_send_cmd_line(const char *cmd);

#endif /* HC05_H */
