---
name: embedded-timing-calc
description: 嵌入式时序计算器：凡问"该填多少/是多少/选多大/误差多少/几位分辨率/多久"的具体数字，先跑本工具算，不要心算——UART 波特率与 BRR、定时器 PWM 分频（PSC/ARR 互算）、I2C 上拉电阻、CAN 位时序与采样点、ADC 源阻抗、RC 滤波、SPI 分频、采样定理、I2C 总线耗时、死区占比，以及 USB 48M 时钟链、传感器 LSB、RTC 走时、电池续航、Modbus 帧间隔、Flash 擦写寿命、WS2812/舵机/步进、看门狗、PLL/分压/NTC，外加 FPGA 专属（UART 分频误差、时序 slack 与 Fmax、PWM 位深）。一次算出并回显公式、判定合法性与依据，全离线。Use when any concrete number is asked - UART BRR, timer prescaler, I2C pull-up resistor, CAN bit timing, ADC source impedance, RC filter cutoff, SPI divider, USB 48MHz clock chain, sensor LSB, RTC drift, battery life, flash wear, Modbus frame gap, WS2812/servo/stepper, FPGA clock divider or timing slack. 关键词：波特率计算、该填多少、分频、上拉电阻选多大、采样点、位时序、源阻抗、截止频率、slack、USB 48M、传感器 LSB、RTC 走时、电池续航、Modbus、Flash 寿命、WS2812、舵机、步进、timing calc。不用于：排障决策（用 embedded-debug-trees）、配置坑查询（用 embedded-peripheral-pitfalls）、寄存器事实（用 embedded-register-lookup）。
license: MIT
compatibility: 需要 Python 3.9+，仅使用标准库，无需联网。纯计算，不执行用户代码。
metadata:
  author: fangcun
  version: "1.1.2"
---


# Embedded Timing Calc

Timer, baud rate, divider and sampling timing calculator. Convert a requirement into a configuration value and back, with the formulas shown so results can be checked by hand.

## How to Use

Load this skill and state your concrete inputs. The bundled references, scripts and templates carry the detailed rules and worked examples; the assistant should consult them before answering.

## Bundled Resources

- `scripts/timing.py`

## Notes

This package is a static knowledge and tooling bundle. It does not call external services, does not place orders or trades, and makes no return promises. Verify any hardware-specific values against the official datasheet for your part.

Author: fangcun. License: MIT.
