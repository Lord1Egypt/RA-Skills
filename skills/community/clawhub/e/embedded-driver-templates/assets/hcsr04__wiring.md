# HC-SR04 接线表与使用说明

## 接线（4 根线）

| HC-SR04 引脚 | 接到 | 说明 |
|-------------|------|------|
| VCC | 5V | **必须是 5V**，3.3V 供电测距不稳 |
| Trig | MCU GPIO（如 PA1） | 触发脉冲 |
| Echo | MCU GPIO（如 PA2） | **5V 输出！STM32 等 3.3V MCU 建议串 1kΩ+分压 2kΩ 到 GND**，或用 5V 容忍脚 |
| GND | GND | 共地 |

> Echo 是 5V 电平。STML43 等非 5V 容忍脚直连有风险——毕设答辩前被老师指出电平问题很扣分，分压两个电阻的事。

## 快速上手（STM32 HAL）

1. 把 `hcsr04.h`、`hcsr04.c`、`hcsr04_port.h` 复制进工程
2. 在 `hcsr04_port.h` 里按注释填 4 个接口
3. 读取：
   ```c
   int32_t d = hcsr04_read_cm_x10();      // 单位 0.1cm，如 233 = 23.3cm
   if (d == HCSR04_ERR_NO_ECHO)
       printf("no echo: out of range or wiring\r\n");
   else
       printf("distance = %d.%d cm\r\n", d / 10, d % 10);
   ```

## 测距跳动/异常时的排查

1. `serial_read` + `analyze_log`：回波恒无（超量程）→ 查目标距离是否 >4m 或角度太偏
2. 数值随机跳 → 阻塞轮询版依赖 delay_us 精度；上 TIM 输入捕获版（答辩加分点）
3. 恒无回波 → Trig 脉冲 ≥10us 是否达标、Echo 线是否接反、是否共地
4. 多传感器轮询时留 ≥60ms 间隔，避免上一轮回波串扰

## 精度速查

- 声速 343m/s（23°C），温度每变 1°C 声速变 ~0.6m/s——要求高时按温度补偿（正好配合 DHT11 的温度做闭环，毕设创新点+1）
- 阻塞轮询版 ±1cm；TIM 输入捕获版 ±1mm
