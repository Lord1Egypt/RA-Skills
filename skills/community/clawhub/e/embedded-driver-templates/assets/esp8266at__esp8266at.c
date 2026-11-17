/**
 * esp8266at.c - ESP-AT 响应解析实现（全部纯函数，无总线时序）
 */
#include "esp8266at.h"
#include <stddef.h>

static int _starts_with(const char *s, const char *prefix)
{
    while (*prefix) {
        if (*s++ != *prefix++) {
            return 0;
        }
    }
    return 1;
}

esp8266_line_type_t esp8266_classify_line(const char *line)
{
    if (line == 0) {
        return ESP8266_LINE_OTHER;
    }
    while (*line == '\r' || *line == '\n' || *line == ' ' || *line == '\t') {
        line++;
    }
    if (_starts_with(line, "OK"))         return ESP8266_LINE_OK;
    if (_starts_with(line, "ERROR"))      return ESP8266_LINE_ERROR;
    if (_starts_with(line, "FAIL"))       return ESP8266_LINE_FAIL;
    if (_starts_with(line, "WIFI CONNECTED"))     return ESP8266_LINE_WIFI_CONNECTED;
    if (_starts_with(line, "WIFI GOT IP"))        return ESP8266_LINE_WIFI_GOT_IP;
    if (_starts_with(line, "WIFI DISCONNECT"))    return ESP8266_LINE_WIFI_DISCONNECT;
    if (_starts_with(line, "+IPD,"))      return ESP8266_LINE_IPD;
    if (_starts_with(line, "+CME ERROR")) return ESP8266_LINE_CME_ERROR;
    if (_starts_with(line, "busy "))      return ESP8266_LINE_BUSY;
    if (line[0] == '>')                   return ESP8266_LINE_SEND_PROMPT;
    return ESP8266_LINE_OTHER;
}

esp8266_cwjap_err_t esp8266_cwjap_err(int code)
{
    switch (code) {
    case 1: return ESP8266_JAP_TIMEOUT;
    case 2: return ESP8266_JAP_BAD_PASS;
    case 3: return ESP8266_JAP_NO_AP;
    case 4: return ESP8266_JAP_FAIL;
    default: return ESP8266_JAP_UNKNOWN;
    }
}

int esp8266_ipd_parse(const char *line, int *ch, int *len, int *data_off)
{
    if (line == 0 || len == 0) {
        return -1;
    }
    while (*line == '\r' || *line == '\n') {
        line++;
    }
    if (!_starts_with(line, "+IPD,")) {
        return -1;
    }
    const char *p = line + 5;   /* 跳过 "+IPD," */

    /* 第一个数字 */
    int a = 0, has = 0;
    while (*p >= '0' && *p <= '9') {
        a = a * 10 + (*p - '0');
        has = 1;
        p++;
    }
    if (!has) {
        return -1;
    }

    if (*p == ',') {
        /* 多连接：+IPD,<ch>,<len>:data */
        p++;
        int b = 0, hasb = 0;
        while (*p >= '0' && *p <= '9') {
            b = b * 10 + (*p - '0');
            hasb = 1;
            p++;
        }
        if (!hasb || *p != ':') {
            return -1;
        }
        if (ch) {
            *ch = a;
        }
        *len = b;
        if (data_off) {
            *data_off = (int)((p + 1) - line);
        }
        return 0;
    }
    if (*p != ':') {
        return -1;
    }
    /* 单连接：+IPD,<len>:data */
    if (ch) {
        *ch = -1;
    }
    *len = a;
    if (data_off) {
        *data_off = (int)((p + 1) - line);
    }
    return 0;
}
