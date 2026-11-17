# ESP8266-AT 模块接线与避坑指南（ESP-01 / ESP-01S）

## 接线（ESP-01，8 脚）

```
ESP-01           MCU (3.3V！)
┌─────────┐
│ VCC ─────────── 3.3V（独立供电，电流 ≥500mA）
│ GND ─────────── GND（与 MCU 共地）
│ TX  ─────────── MCU RX（3.3V 电平直连）
│ RX  ───[分压]── MCU TX（若 MCU 是 5V 电平必须分压：1k+2k）
│ CH_PD(EN) ──── 3.3V（★忘接这根 = 模块死）
│ (GPIO0/GPIO2/RST 悬空即可)
└─────────┘
```

## 头号坑清单（毕设翻车率排序）

| 坑 | 症状 | 解法 |
|---|---|---|
| CH_PD/EN 没拉高 | 完全无响应（命中 AT_NO_RESP） | CH_PD 接 3.3V，ESP-01S 可以直接接 |
| 供电电流不足 | 能连上但发数据就重启/掉线（命中 ESP_BROWNOUT/BOOT_LOOP） | 独立 3.3V 电源 + 470uF 电容；板载 LDO 带不动 |
| TX/RX 接反 | 无响应 | 交叉接线 |
| 5V 电平直灌 RX | 模块烧/不稳定 | MCU 是 5V 系统时分压：TX→1kΩ→RX，RX→2kΩ→GND |
| 指令结尾 \\n 而不是 \\r\\n | ERROR 或无响应 | AT 指令标准结尾是 \\r\\n |
| 5G 热点 | +CWJAP:3 找不到 AP | ESP8266 只支持 2.4GHz |
| CIPSEND 没等 ">" | 数据丢失/ERROR | 发 AT+CIPSEND=len 后等 ">" 再发数据 |

## 典型联网流程（背下来，答辩要用）

```
AT                        → OK           （测通信）
AT+CWMODE=1               → OK           （Station 模式）
AT+CWJAP="ssid","pwd"     → OK           （连 WiFi；失败返回 +CWJAP:<1-4>）
AT+CIFSR                  → 返回 IP      （确认拿到 IP）
AT+CIPSTART="TCP","ip",port → OK         （建 TCP 连接）
AT+CIPSEND=<len>          → >            （等提示符！）
<data len 字节>           → SEND OK / +IPD,<len>:<data>
AT+CIPCLOSE               → OK
```

## 输出解读（配合本 MCP 的 analyzer）

- `+CWJAP:1/2/3/4` → 命中 `CWJAP_ERR`，码表直译原因
- `+CME ERROR: n` → 命中 `AT_CME_ERROR`，3GPP 错误码
- `busy p...` → 命中 `BUSY` 类提示：上一条指令还没执行完，加延时或等 OK 再发下一条
- `WIFI DISCONNECT` → 命中 `NET_LINK`：供电不足高发（大功率发射瞬间掉电）
- 指令发出无任何响应 → 命中 `AT_NO_RESP`：接线/波特率/CH_PD

## 答辩加分点

1. **透传模式（AT+CIPMODE=1）**：MCU 当"透明管道"，讲清透传与指令模式的切换
2. **断线重连设计**：WIFI DISCONNECT 事件的检测与自动重连状态机——工程健壮性加分
3. **为什么 2.4G only**：可以讲 ESP8266 射频架构（802.11 b/g/n 2.4GHz）
4. **多连接 vs 单连接**：CIPMUX 的应用场景（单设备 TCP vs 本机做服务器）
