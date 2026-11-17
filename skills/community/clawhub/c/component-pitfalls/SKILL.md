---
name: component-pitfalls
version: 1.0.0
slug: component-pitfalls
displayName: 元器件选型避坑指南
summary: 电子元器件采购避坑：渠道四级分级、四类假芯片识别、五步验真法、高频模块坑速查与缺货替代链。
display_name: 元器件选型避坑指南
display_name_en: Component Selection Pitfall Guide
description_zh: 电子 DIY/创客/硬件工程师/毕设学生下单前对照避坑：渠道四级分级（自营→官方店→认证店→个人与二手，风险递增）、四类假芯片识别（打磨改标/翻新拆机/白盒假冒/克隆片）、五步验真法、高频模块坑速查、缺货替代链、220V 与锂电池安全红线。买元器件/选传感器/假芯片/翻新料/采购渠道/缺货替代时使用。
description_en: Pre-purchase pitfall guide for electronics DIY, makers, hardware engineers and students — channel tiering (self-operated catalog distributor / board maker's official store / certified shop / personal and second-hand channel), four counterfeit chip types (remarked/revived/white-box/clones), five-step authenticity checks, common module pitfalls (SHT30/MQ/HC-05/fake LM2596/cloned TP4056/overrated 18650/ESP32 modules/power/relay), out-of-stock substitution chains, and 220V safety red lines.
description: 电子 DIY、创客、硬件工程师、毕设学生采购避坑指南。买元器件/选传感器/渠道选择/假芯片排查/缺货替代时使用。渠道分级：自营目录商城→开发板官方店→认证企业店→个人与二手渠道为翻新高发；四类假芯片识别（打磨改标/翻新拆机/白盒假冒/克隆片）与五步验真法（看包装/溶剂擦丝印/微距看背面/查日期码/测参数）；高频模块坑速查（SHT30 兼容料/MQ 裸探头/HC-05 与 06 区别/W25Q64 翻新/LM2596 假芯片实为 MC34063/TP4056 克隆过充/18650 虚标容量/ESP32 模组翻新料 esptool 验 Flash/USB 供电纹波/继电器 220V）；缺货替代链（F103→GD32、SHT30→AHT20 等，改动量标清）；220V 强电与锂电池安全红线无例外。价格给区间不编造，不推荐具体店铺。
author: fangcun
license: MIT
agent_created: true
examples_zh:
- "我要买 SHT30 传感器有什么坑"
- "HC-05 和 HC-06 有什么区别，该买哪个"
- "STM32F103 缺货了有什么能替代的"
examples_en:
- "What pitfalls should I know before buying an SHT30 sensor?"
- "HC-05 vs HC-06 - which one should I buy for AT commands?"
- "STM32F103 is out of stock - what is a drop-in replacement?"
license: MIT
---


# Component Pitfalls

A static knowledge base of component-selection pitfalls for electronics buyers. Covers supplier channel tiering, four counterfeit chip types, a five-step authenticity check, common module traps, substitution chains and mains/lithium safety red lines. Prices are given as ranges, no specific shops are recommended.

## How to Use

Load this skill and state your concrete inputs. The bundled references, scripts and templates carry the detailed rules and worked examples; the assistant should consult them before answering.

## Bundled Resources

- `README_____.md`

## Notes

This package is a static knowledge and tooling bundle. It does not call external services, does not place orders or trades, and makes no return promises. Verify any hardware-specific values against the official datasheet for your part.

Author: fangcun. License: MIT.
