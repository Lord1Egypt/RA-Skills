# 主流 MCU 架构对比与选型

## 主流架构一览

| 架构 | 代表芯片 | 优势 | 劣势 | 典型场景 |
|------|---------|------|------|---------|
| ARM Cortex-M0 | STM32F0, NXP LPC | 低功耗，成本低，生态好 | 性能有限 | 简单控制，IoT传感器 |
| ARM Cortex-M3 | STM32F1, TI Tiva | 性能均衡，外设丰富 | 功耗比M0高 | 通用工业控制 |
| ARM Cortex-M4 | STM32F4, NXP MK64 | DSP/FPU，性能强 | 成本稍高 | 电机控制，音频 |
| ARM Cortex-M7 | STM32F7, H7 | 性能最强，高带宽 | 功耗大，成本高 | 图像处理，高性能HMI |
| RISC-V | 乐鑫ESP32-C3, 沁芯CH32V | 免费开源，定制灵活 | 生态仍在成熟 | IoT，定制化场景 |
| 8051 | STC系列 | 简单，稳定，低成本 | 性能弱，外设有限 | 简单替换，低成本场景 |
| AVR | ATmega, ATtiny | 简单易用，Arduino兼容 | 资源有限 | 爱好者，教育 |
| ESP32 | 乐鑫ESP32 | WiFi+BT双频，性价比高 | 功耗偏大 | WiFiIoT，语音控制 |

## 选型决策树

```
                    应用场景
                        │
         ┌──────────────┼──────────────┐
      简单控制        通信+IoT        高性能
    (传感器/开关)   (WiFi/BLE)    (图像/电机/HMI)
         │              │              │
     Cortex-M0      ESP32系列      Cortex-M4+
     (STM32F0)      (ESP32-C3      (STM32F4/H7
                    /ESP32-S3)      GD32F4)
```

## STM32 家族速查

- **F0**: Cortex-M0, 48MHz, 简单低成本 → 替代8位MCU
- **F1**: Cortex-M3, 72MHz, 外设经典 → 工控入门首选
- **F4**: Cortex-M4, 180MHz, DSP+FPU → 电机驱动，音频
- **F7**: Cortex-M7, 216MHz+, 高性能 → HMI，图像
- **H7**: Cortex-M7+M4 双核, 极高性能 → 工业旗舰
- **WB**: 双核 + BLE+WiFi → 复杂IoT
- **WL**: LoRa + STM32 → 远距离IoT

## 时钟系统要点

STM32F1 示例（HSE 8MHz）：
```
HSE = 8MHz → PLL * 9 = 72MHz → SYSCLK
APB1 = 72MHz / 2 = 36MHz  (高速总线)
APB2 = 72MHz / 1 = 72MHz  (最高速总线)
```

关键：
- 使用 PLL 时必须等 PLL lock
- 外设时钟使能：RCC_APB1ENR / RCC_APB2ENR
- 未使用的时钟会自动关闭（低功耗模式）

## 电源设计注意事项

- **VDD**: 3.3V 数字电源，加 100nF + 10µF 去耦
- **VDDA**: 模拟部分独立电源，给ADC用
- **VREF+**: ADC 参考电压，高精度应用需单独参考芯片
- **VBAT**: RTC 备份电源，断电时维持RTC
- **BOOT0**: 启动模式选择（系统存储/Flash/SRAM）

## 最小系统必备

1. 电源：LDO（AMS1117-3.3 / AMS1086-3.3）输入建议5V-12V
2. 晶振：8MHz HSE + 32.768kHz LSE（RTC）
3. 复位电路：10kΩ 上拉 + 100nF 去耦
4. SWD 调试口：SWCLK / SWDIO / GND（最少3线）
5. 启动电阻：BOOT0 通过 10kΩ 下拉
