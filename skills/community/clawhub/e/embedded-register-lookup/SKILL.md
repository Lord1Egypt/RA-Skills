---
name: embedded-register-lookup
description: 查询 MCU 外设寄存器、位域、复位值和地址（基于 CMSIS SVD），每条结论带出处与证据标签；支持地址反查、寄存器值解码与写入值计算、位域速查与位图、中断号与 NVIC 使能提示、CMSIS 风格宏生成、跨芯片与外设级整体对比、地址区间查询、SVD 质量检查、本机芯片清单与环境体检、Markdown 表格输出、解析结果缓存。Use when the user asks about a register, bit field, reset value, peripheral base address, interrupt number, wants to decode or compute a register value to write, generate register macros, compare register definitions between devices, or find/verify SVD files on the machine. 关键词：寄存器、位域、复位值、SVD、外设地址、寄存器值、掩码、位图、中断号、IRQn、NVIC、宏定义、对比、整体对比、质量检查、SVD 位置、芯片清单、读改写、USART1->CR1、register、bitfield、mask、reset value、decode、interrupt。不用于：引脚复用、手册章节检索、勘误查询、核对代码中的寄存器写入（用 embedded-register-verify）。
license: MIT
compatibility: 需要 Python 3.9+，仅使用标准库，无需联网。需要目标芯片的 CMSIS SVD 文件：厂商 CMSIS-Pack 或用户自备的 .svd；没有 SVD 时可用内置演示芯片（--demo）零配置试用。
metadata:
  author: fangcun
  version: "1.11.3"
---


# Embedded Register Lookup

Quick reference for common MCU peripheral registers: addresses, bit fields and typical configuration values with datasheet section citations, so register-level code does not require flipping through the manual.

## How to Use

Load this skill and state your concrete inputs. The bundled references, scripts and templates carry the detailed rules and worked examples; the assistant should consult them before answering.

## Bundled Resources

- `references/glossary.md`
- `references/query-syntax.md`
- `references/svd-support.md`
- `scripts/lookup.py`
- `scripts/etk_core/__init__.py`
- `scripts/etk_core/cache.py`
- `scripts/etk_core/discovery.py`
- `scripts/etk_core/errors.py`
- `scripts/etk_core/output.py`
- `scripts/etk_core/query.py`
- `scripts/etk_core/svd.py`
- `scripts/etk_core/values.py`

## Notes

This package is a static knowledge and tooling bundle. It does not call external services, does not place orders or trades, and makes no return promises. Verify any hardware-specific values against the official datasheet for your part.

Author: fangcun. License: MIT.
