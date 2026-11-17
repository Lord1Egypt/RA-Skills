/**
 * hc05.c - HC-05 蓝牙 AT 命令助手实现
 * 依据：HC-05 AT 指令集（常见固件 HC-05 at command sets，ZS-040/HC-05 主流版本）
 * 注：ERROR:(n) 细分码各固件含义不统一，代码只负责提取 n，语义见 wiring.md
 */
#include "hc05.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* HC-05 手册支持的波特率（AT+UART= 参数 1） */
static const long BAUD_TABLE[] = {
    1200, 2400, 4800, 9600, 19200, 38400,
    57600, 115200, 230400, 460800, 921600, 1382400
};

/* ---------------- 纯函数（PC 可单元测试） ---------------- */

hc05_result_t hc05_classify(const char *line)
{
    if (line == 0)
        return HC05_IGNORE;
    while (*line == ' ' || *line == '\t')
        line++;                          /* 容忍前导空格 */
    if (*line == '\0')
        return HC05_IGNORE;
    if (strcmp(line, "OK") == 0)
        return HC05_OK;
    if (strncmp(line, "ERROR", 5) == 0)
        return HC05_ERROR;               /* ERROR / ERROR:(n) 都算 */
    if (strcmp(line, "FAIL") == 0)
        return HC05_FAIL;
    if (line[0] == '+')
        return HC05_DATA;                /* +NAME: / +VERSION: / +UART: ... */
    return HC05_UNKNOWN;
}

int hc05_error_detail(const char *line)
{
    if (line == 0)
        return -1;
    /* 匹配 "ERROR:(n)"，n 为数字 */
    const char *p = strstr(line, "ERROR:(");
    if (p == 0)
        return -1;
    p += 7;
    long n = strtol(p, 0, 10);
    if (n <= 0 || n > 255)
        return -1;
    return (int)n;
}

int hc05_uart_cmd(long baud, int stop, int parity, char *buf, int size)
{
    if (buf == 0 || size < 16)
        return -1;
    int ok = 0;
    for (unsigned i = 0; i < sizeof(BAUD_TABLE) / sizeof(BAUD_TABLE[0]); i++)
        if (BAUD_TABLE[i] == baud) { ok = 1; break; }
    if (!ok)
        return -2;                       /* 波特率不在 HC-05 支持列表 */
    if (stop != 0 && stop != 1)
        return -3;
    if (parity < 0 || parity > 2)
        return -4;
    int n = snprintf(buf, (size_t)size, "AT+UART=%ld,%d,%d\r\n", baud, stop, parity);
    if (n < 0 || n >= size)
        return -5;
    return n;
}

/* ---------------- 硬件交互（目标机上运行） ---------------- */

hc05_result_t hc05_send_cmd_line(const char *cmd)
{
    hc05_uart_write(cmd, (int)strlen(cmd));

    char line[64];
    int len = 0;
    uint32_t t0 = hc05_millis();
    while ((int)(hc05_millis() - t0) < 2000) {
        char c;
        if (hc05_uart_read(&c, 1) == 1) {
            if (c == '\n') {
                if (len > 0) {
                    line[len] = '\0';
                    hc05_result_t r = hc05_classify(line);
                    if (r != HC05_IGNORE)
                        return r;
                    len = 0;
                }
                continue;
            }
            if (c != '\r' && len < (int)sizeof(line) - 1)
                line[len++] = c;
        }
    }
    return HC05_UNKNOWN;                 /* 2 秒无有效响应：模式不对或波特率不对 */
}
