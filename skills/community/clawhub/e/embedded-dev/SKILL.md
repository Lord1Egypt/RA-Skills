---
name: embedded-dev
description: 单片机嵌入式全栈开发技能，覆盖从底层硬件到上层应用的全链路技术问题。当用户询问嵌入式开发、微控制器、RTOS、电机控制、传感器接口、固件编写、调试上线等任何软硬件相关问题时应调用此技能。
---

# Embedded Dev Skill

单片机嵌入式全栈开发技能，掌握从芯片底层到产品上层的全链路知识。

## 技能范围

- 主流 MCU 架构（ARM Cortex-M、RISC-V、8051、AVR、ESP32、STM32）
- 外设驱动开发（GPIO、UART、I2C、SPI、ADC、PWM、Timer、CRC 等）
- 嵌入式C语言与汇编优化
- RTOS（FreeRTOS/RT-Thread/Zephyr）任务调度与进程间通信
- 有线/无线通信协议（UART、SPI、I2C、CAN、Modbus、RS485、LoRa、BLE、WiFi）
- 传感器与执行器接口（I2C/SPI 传感器、电机驱动、PWM 控制）
- 底层调试（JTAG/SWD、逻辑分析仪、示波器、printf 调试）
- 硬件原理图与 PCB 设计基础
- 固件架构（模块化设计、状态机、事件驱动）
- OTA 升级与 bootloader
- 低功耗设计
- 嵌入式 Linux（树莓派/全志/TI/NXP）基础

## 工作流程

遇到嵌入式问题时，按以下步骤处理：

1. **明确硬件平台** — 确认 MCU 型号、时钟配置、电源环境
2. **定位问题层级** — 硬件层/驱动层/RTOS层/应用层/通信层
3. **查参考文件** — 根据问题类型加载对应 reference 文件
4. **给出完整解答** — 包含代码示例（寄存器配置/C语言/驱动）、接线图要点、调试方法

## Reference 文件索引

- `references/mcu-architectures.md` — 主流 MCU 架构对比与选型
- `references/peripherals.md` — 外设驱动开发手册（GPIO/UART/I2C/SPI/ADC/PWM）
- `references/embedded-c.md` — 嵌入式C语言编程规范与技巧
- `references/rtos.md` — RTOS 实战（任务/队列/信号量/内存）
- `references/communication-protocols.md` — 通信协议对比与实现
- `references/debugging.md` — 硬件/软件调试方法与工具
- `references/hardware-design.md` — 原理图/PCB 设计要点
- `references/firmware-dev.md` — 固件架构与 OTA 升级

## 常用代码模板

### GPIO 配置（STM32 HAL 风格）
```c
// 配置 PB0 为推挽输出
HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET);  // 输出高
HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET);  // 输出低
// 读取 PA1
GPIO_PinState state = HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_1);
```

### UART 中断接收（轮询+中断混合）
```c
uint8_t rx_buf[64];
volatile uint8_t rx_len = 0;
void USART1_IRQHandler(void) {
    if (USART->SR & USART_SR_RXNE) {
        rx_buf[rx_len++] = USART->DR;
    }
}
```

### I2C 传感器读取（示例：MPU6050）
```c
void I2C_WriteReg(uint8_t addr, uint8_t reg, uint8_t val) {
    I2C_Start();
    I2C_SendAddr(addr << 1);
    I2C_SendByte(reg);
    I2C_SendByte(val);
    I2C_Stop();
}
uint8_t I2C_ReadReg(uint8_t addr, uint8_t reg) {
    I2C_Start();
    I2C_SendAddr(addr << 1 | 0);
    I2C_SendByte(reg);
    I2C_RepeatedStart();
    I2C_SendAddr(addr << 1 | 1);
    uint8_t val = I2C_RecvByte(NACK);
    I2C_Stop();
    return val;
}
```

### FreeRTOS 任务创建
```c
void sensor_task(void *arg) {
    while (1) {
        float temp = read_temperature();
        xQueueSend(temp_queue, &temp, portMAX_DELAY);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
xTaskCreate(sensor_task, "Sensor", 512, NULL, 2, &sensor_handle);
```

### PWM 电机控制
```c
// 配置 TIM3 CH2 (PB5) PWM 50Hz
void Motor_PWM_Init(void) {
    TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
    TIM_OCInitTypeDef TIM_OCInitStructure;
    // 72MHz / 720 => 100kHz, 100kHz / 2000 => 50Hz
    TIM_TimeBaseStructure.TIM_Period = 2000 - 1;   // ARR
    TIM_TimeBaseStructure.TIM_Prescaler = 72 - 1;   // PSC
    TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure);
    TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;
    TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable;
    TIM_OCInitStructure.TIM_Pulse = 1500;  // 占空比 75%
    TIM_OC2Init(TIM3, &TIM_OCInitStructure);
    TIM_Cmd(TIM3, ENABLE);
}
// 设置速度 0~100%
void Motor_SetSpeed(uint8_t speed) {
    TIM3->CCR2 = (speed * 20);  // 0-2000
}
```

## 常用调试命令

```bash
# OpenOCD + ST-Link 调试
openocd -f interface/stlink.cfg -f target/stm32f1x.cfg

# JLink GDB Server
JLinkGDBServer -if SWD -device STM32F103RC

# 逻辑分析仪（Saleae 协议）
sigrok-cli -d saleae-logic16 --channels 1,2,3,4 -o capture.sr

# 串口查看
minicom -b 115200 -D /dev/ttyUSB0
screen /dev/ttyUSB0 115200
```

## 常见问题速查

| 问题 | 常见原因 | 解决方案 |
|------|---------|---------|
| I2C 无响应 | 地址错误/未接上拉/SCL被占用 | 用逻辑仪确认 SDA/SCL 波形 |
| UART 乱码 | 波特率不匹配/电平不匹配 | 示波器检查波特率 |
| PWM 无输出 | 时钟未使能/IO复用错误 | 检查 TIM_EN 和 AFIO 配置 |
| 程序跑飞 | 堆栈溢出/看门狗未喂狗 | 减小堆栈/加看门狗 |
| OTA 升级失败 | Flash 偏移地址错误/签名校验失败 | 确认 bootloader 大小配置 |
| 低功耗电流大 | 未关闭未用外设时钟/LDO功耗高 | 逐个禁用外设定位 |
