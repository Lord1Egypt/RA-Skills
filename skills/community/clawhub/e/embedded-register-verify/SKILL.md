---
name: embedded-register-verify
description: 核验 C 代码里的 MCU 寄存器写入是否与芯片 SVD 一致：外设、寄存器、位域是否存在；值是否超位宽；枚举是否合法；是否写只读位；是否访问前未开时钟；是否硬编码地址。按"报 / 未判定 / 通过"分桶输出，并可生成复查清单。Use when reviewing embedded C init code, register writes, or AI-generated firmware registers; verify register writes against a chip SVD. 关键词：寄存器核验、寄存器检查、AI 生成代码、驱动复查、初始化代码检查、对拍、register check、verify register writes。不用于：HAL/LL 结构体配置语义（会进未判定）、外挂器件命令（Flash、传感器）、时序正确性、通用代码风格、寄存器事实查询（用 embedded-register-lookup）。
license: MIT
compatibility: 需要 Python 3.9+，仅使用标准库，无需联网。需要目标芯片的 CMSIS SVD 文件（查找规则同 embedded-register-lookup）；没有 SVD 时可用内置演示芯片（--demo）零配置试用。
metadata:
  author: fangcun
  version: "1.17.0"
---


# Embedded Register Verify

Verify register configuration values bit by bit against the datasheet. Give an address, bit field and manual page; get a correctness verdict plus a corrected value. Designed to stop copy-paste register bugs before flashing.

## How to Use

Load this skill and state your concrete inputs. The bundled references, scripts and templates carry the detailed rules and worked examples; the assistant should consult them before answering.

## Bundled Resources

- `references/rules.md`
- `references/syntax.md`
- `scripts/crules.py`
- `scripts/cscan.py`
- `scripts/verify.py`
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
