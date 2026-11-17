---
name: embedded-peripheral-pitfalls
description: 配置 MCU 外设前对照避坑清单，或排查"配置看起来都对但就是不工作"：RCC 时钟使能与顺序、GPIO 复用/开漏/上拉/5V 兼容、EXTI 与 NVIC 中断（标志清除/优先级分组）、定时器（ARR/PSC/PWM 频率/死区）、ADC（采样时间/校准/序列）、DMA（循环模式/地址自增/宽度/标志清除/请求映射）、UART 波特率、I2C（上拉/时钟拉伸/地址）、SPI（CPOL/CPHA/片选/溢出）、CAN（位时序/过滤器/终端电阻）、低功耗（唤醒/待机）、看门狗（喂狗/窗口/调试冻结）、USB（HSI48 时钟/上拉软断开/端点缓冲对齐/CDC 驱动）、片上 Flash 擦写、RTC（时钟源/写保护/首次上电判定）、DAC/CRC/MPU、调试与链接（semihosting/SWO/DBGMCU/VTOR/栈堆/段溢出）、以太网（RMII 时钟/MDIO/cache/lwIP 内存）、SD 卡、C 代码、Modbus、1-Wire 传感器总线。二十五类外设 148 个实战坑，每坑=症状+对策，含配置口诀。Use when configuring MCU peripherals, checking init code, or troubleshooting peripheral misconfiguration. 与 verify 分工：verify 查寄存器写入合法性，本库查配置语义陷阱。不用于：故障已发生要定位根因（用 embedded-debug-trees）、寄存器事实查询（用 embedded-register-lookup）。
license: MIT
compatibility: 需要 Python 3.9+，仅使用标准库，无需联网。纯知识检索，不执行用户代码。
metadata:
  author: fangcun
  version: "1.2.2"
---


# Embedded Peripheral Pitfalls

Peripheral initialisation and usage pitfalls: missing clock gating, pin-mux conflicts, interrupt priority mistakes, DMA cache coherence and similar issues, each with a verifiable source.

## How to Use

Load this skill and state your concrete inputs. The bundled references, scripts and templates carry the detailed rules and worked examples; the assistant should consult them before answering.

## Bundled Resources

- `references/pitfalls.md`

## Notes

This package is a static knowledge and tooling bundle. It does not call external services, does not place orders or trades, and makes no return promises. Verify any hardware-specific values against the official datasheet for your part.

Author: fangcun. License: MIT.
