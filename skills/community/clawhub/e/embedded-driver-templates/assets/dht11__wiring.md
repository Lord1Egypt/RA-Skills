# DHT11 接线表与使用说明

## 接线（3 根线）

| DHT11 引脚 | 接到 | 说明 |
|-----------|------|------|
| VCC (1)   | 3.3V 或 5V | 与 MCU 同电源域 |
| DATA (2)  | MCU 任意 GPIO（如 PA0） | **必须加 4.7kΩ~10kΩ 上拉电阻到 VCC**（模块板载的可省） |
| GND (3/4) | GND | 共地 |

> 裸传感器（3 脚封装）没有上拉电阻，**不接上拉 = 读出全 0xFF 或无响应**，这是第一大坑。

## 快速上手（STM32 HAL）

1. CubeMX 里把数据脚配成 GPIO_Output（驱动运行时动态切输入输出）
2. 把 `dht11.h`、`dht11.c`、`dht11_port.h` 三个文件复制进工程
3. 在 `dht11_port.h` 里按注释填 5 个接口（取消 HAL 示例的注释即可）
4. **main 里先使能 DWT 微秒计时**（没有它时序全错）：
   ```c
   CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
   DWT->CYCCNT = 0;
   DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
   ```
5. 循环读取（间隔 ≥1s）：
   ```c
   dht11_data_t d;
   int r = dht11_read(&d);
   if (r == DHT11_OK)
       printf("temp=%d.%d C humi=%d.%d %%\r\n", d.temp_int, d.temp_dec, d.humidity_int, d.humidity_dec);
   else if (r == DHT11_ERR_TIMEOUT)
       printf("DHT11 no response: check wiring/pull-up\r\n");
   else
       printf("DHT11 checksum error: timing interrupted\r\n");
   ```

## 读不到数据时的排查顺序

1. `mcu-debug-mcp` 的 `serial_read` 看是超时、全 0 还是全 FF → `analyze_log` 自动给出对应诊断
2. 全 FF → 查上拉电阻；超时 → 查 delay_us 是否 us 级精度（HAL_Delay 不行！）
3. 校验错 → 读时序期间被中断打断，确认 `dht11_read` 内部的关中断保护没被去掉
4. 恒 85.0°C 那是 DS18B20 的毛病，别混淆；DHT11 读出 0 且无错误码 → 看是不是忘了等 1s 上电稳定

## 数据格式速查

40 bit = 湿度整数 + 湿度小数 + 温度整数 + 温度小数 + 校验和（前 4 字节之和低 8 位）。
DHT11 小数位恒 0（需要真实小数上 DHT22，驱动逻辑相同、分辨率不同）。
