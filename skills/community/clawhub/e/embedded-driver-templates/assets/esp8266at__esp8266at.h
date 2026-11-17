/**
 * esp8266at.h - ESP8266/ESP-AT 响应解析库（纯函数，PC 全量可测）
 *
 * 定位：不是"驱动 ESP8266"——ESP-AT 固件的模块本身就是黑盒，MCU 只跟它
 * 说话（串口收发）。真正容易写错的是【响应解析】：IPD 帧、错误码、状态行。
 * 本库把这些全部做成纯函数，PC 上拿真实响应样例测试。
 *
 * 用法（串口收到一行后调用）：
 *   esp8266_line_type_t t = esp8266_classify_line(line);
 *   if (t == ESP8266_LINE_IPD) { esp8266_ipd_parse(line, &ch, &len); }
 *
 * 验证记录：见本目录 meta.json
 */
#ifndef ESP8266AT_H
#define ESP8266AT_H

#include <stdint.h>

/* 行类型 */
typedef enum {
    ESP8266_LINE_OTHER = 0,
    ESP8266_LINE_OK,            /* "OK" */
    ESP8266_LINE_ERROR,         /* "ERROR" */
    ESP8266_LINE_FAIL,          /* "FAIL"（CWJAP 失败） */
    ESP8266_LINE_WIFI_CONNECTED,/* "WIFI CONNECTED" */
    ESP8266_LINE_WIFI_GOT_IP,   /* "WIFI GOT IP" */
    ESP8266_LINE_WIFI_DISCONNECT,/* "WIFI DISCONNECT" */
    ESP8266_LINE_IPD,           /* "+IPD,..."：收到网络数据 */
    ESP8266_LINE_CME_ERROR,     /* "+CME ERROR:..." */
    ESP8266_LINE_BUSY,          /* "busy p..." / "busy s..."：模块忙 */
    ESP8266_LINE_SEND_PROMPT,   /* ">"：可发数据的提示符 */
} esp8266_line_type_t;

/* +CWJAP 错误码 → 枚举（Espressif AT 手册） */
typedef enum {
    ESP8266_JAP_OK = 0,
    ESP8266_JAP_TIMEOUT   = 1,  /* 路由器无响应：查 2.4G/信号 */
    ESP8266_JAP_BAD_PASS  = 2,  /* 密码错误 */
    ESP8266_JAP_NO_AP     = 3,  /* 找不到 AP：SSID 错/信号弱 */
    ESP8266_JAP_FAIL      = 4,  /* 连接被拒：DHCP 满/过滤 */
    ESP8266_JAP_UNKNOWN   = -1,
} esp8266_cwjap_err_t;

/* 行分类。纯函数：输入以 \0 结尾的一行（可含 \r），返回类型。 */
esp8266_line_type_t esp8266_classify_line(const char *line);

/* +CWJAP 错误码映射。纯函数。 */
esp8266_cwjap_err_t esp8266_cwjap_err(int code);

/* 解析 +IPD 帧。兼容两种形式：
 *   单连接：  +IPD,<len>:data
 *   多连接：  +IPD,<ch>,<len>:data
 * 纯函数。成功返回 0 并填 *ch（单连接为 -1）*len *data_off（data 起始下标）；
 * 格式不对返回 -1。 */
int esp8266_ipd_parse(const char *line, int *ch, int *len, int *data_off);

#endif /* ESP8266AT_H */
