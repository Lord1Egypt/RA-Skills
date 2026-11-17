---
name: embedded-debug-trees
description: 排查 MCU 硬件/固件故障时使用：程序跑飞、HardFault、死机复位、总线错误；串口/UART/I2C/SPI/CAN 通信不通、超时、乱码；DMA 丢数据、只收一次、数据错位、偶发损坏；RTOS 任务不跑、卡死死锁、中断优先级问题；上电起不来、Bootloader 跳转异常、莫名周期复位；CAN/CAN-FD 通信不通、错误帧、发不出去、bus-off；USB 识别不到/枚举失败/虚拟串口不弹；Flash 写不进/擦除失败/选项字节读保护；RTC 走时不准/掉电重置；LCD 全黑白屏/花屏/触摸；低功耗睡死叫不醒、唤醒后外设异常。十一棵排障决策树、69 个节点，每步先给证据采集动作（回读寄存器/示波器/故障快照）再下判断，附按实战经验排序的高频根因。Use when debugging MCU crashes, bus faults, I2C/SPI/UART failures, DMA data loss, RTOS deadlocks, CAN/CAN-FD failures, USB/Flash/RTC/Display issues, boot failures, low-power wake issues. 检索不到明说，不编造决策路径。不用于：寄存器事实查询（用 embedded-register-lookup）、寄存器写入核验（用 embedded-register-verify）、配置语义坑（用 embedded-peripheral-pitfalls）、电机行为故障（电机控制域）、FPGA/RTL 综合后异常与跨时钟域（用 embedded-fpga-trees）。
license: MIT
compatibility: 需要 Python 3.9+，仅使用标准库，无需联网。纯知识检索，不执行用户代码。
metadata:
  author: fangcun
  version: "1.4.0"
---


# Embedded Debug Trees

Symptom-driven debugging decision trees for hard faults, hangs, unresponsive peripherals and packet loss. Each tree lists checkpoints and the exact tool commands to run at each branch.

## How to Use

Load this skill and state your concrete inputs. The bundled references, scripts and templates carry the detailed rules and worked examples; the assistant should consult them before answering.

## Bundled Resources

- `references/trees.md`

## Notes

This package is a static knowledge and tooling bundle. It does not call external services, does not place orders or trades, and makes no return promises. Verify any hardware-specific values against the official datasheet for your part.

Author: fangcun. License: MIT.
