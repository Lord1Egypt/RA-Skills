# 硬件/软件调试方法与工具

## 调试工具速查

| 工具 | 用途 | 价格 | 推荐场景 |
|------|------|------|---------|
| ST-Link V2 | STM32调试烧录 | ¥30 | STM32开发必备 |
| J-Link | ARM调试/Trace | ¥300+ | 高级调试 |
| 逻辑分析仪 | 数字信号时序分析 | ¥80+ | I2C/SPI/UART协议 |
| 示波器 | 模拟信号/纹波/噪声 | ¥500+ | 电源/模拟电路 |
| 万用表 | 通断/电压/二极管 | ¥50+ | 硬件检查必备 |
| USB转TTL | 串口调试 | ¥10 | UART日志 |

## SWD 调试命令

```bash
# OpenOCD + ST-Link
openocd -f interface/stlink.cfg -f target/stm32f1x.cfg

# 常用 GDB 命令
monitor reset halt      # 复位并 halt
load                      # 烧录
break main               # 断点
continue                 # 运行
step                     # 单步
info registers          # 寄存器
x/16x 0x20000000        # 查看RAM
```

## printf 重定向

```c
int fputc(int ch, FILE *f) {
    while (!(USART1->SR & USART_SR_TXE));
    USART1->DR = ch;
    return ch;
}

#define LOG(fmt, ...) \
    printf("[%05ld] " fmt "\r\n", HAL_GetTick(), ##__VA_ARGS__)
LOG("ADC=%d Temp=%.2f", adc_val, temp);
```

## 常见故障排查

```
MCU不启动 → 检查 BOOT0 电平 / 晶振 / NRST
芯片发热 → 电源短路 / IO过载 / 反接
烧录失败 → SWD连接 / 读保护 / 接线错误
程序跑飞 → 堆栈溢出 / 数组越界 / 看门狗未喂
I2C无响应 → 地址错误 / 上拉缺失 / 总线被占用
UART乱码 → 波特率偏差 / 电平不匹配
ADC值不准 → 参考电压波动 / 采样时间不足
```

## HardFault 捕获

```c
void HardFault_Handler(void) {
    volatile uint32_t *sp = (volatile uint32_t*)__get_MSP();
    printf("HF: LR=%08X PC=%08X CFSR=%08X\r\n",
        sp[5], sp[6], SCB->CFSR);
    while(1);
}
```

## 逻辑分析仪使用

```bash
# sigrok-cli 采集
sigrok-cli -d saleae-logic16 --channels 1,2 \
  --config samplerate=1M -p ch1=SCL,ch2=SDA -o capture.sr
# 导入 PulseView 解码 I2C/SPI 协议
```
