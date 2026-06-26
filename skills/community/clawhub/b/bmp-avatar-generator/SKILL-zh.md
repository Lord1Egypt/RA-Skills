---
name: bmp-avatar-generator
version: 0.1.2
description: 使用 @bitmappunks/avatar-generator npm 包（锁定 0.0.5 版本，通过 npx 运行）根据 seed 字符串生成确定性的像素风 SVG 头像，并保存到指定路径。只要用户要求基于 seed/name/id 创建、生成、制作头像——比如 "生成头像"、"avatar for user X"、"给我一个头像"、"bitmappunks"——都用这个 skill。
author: BitmapPunks
license: MIT
homepage: https://github.com/bitmappunks-com/avatar-generator-skill
---

# Avatar Generator

> [English](SKILL.md) · [中文](SKILL-zh.md)

通过 `npx` 调用 `@bitmappunks/avatar-generator@0.0.5` 生成确定性 SVG 头像。同一 seed → 同一头像。

**版本锁定在 `0.0.5`。** 没有用户明确指示时，不要升级，也不要去掉这个版本锁。

## 必需输入

1. **seed** —— 用来确定性地产生头像的字符串。可选：如果未提供，默认使用当前 Unix 时间戳（秒）作为 seed，这样每次都会不同；同时要把本次实际使用的 seed 告诉用户。
2. **output path** —— 保存 `.svg` 的路径。如果用户给的是目录，则拼上 `<seed>.svg`。如果完全没给路径，则默认写到当前工作目录下的 `./<seed>.svg`，并告诉用户你用的是这个路径。

只有在输出路径不明确时，才先问用户再执行。

## 执行

```bash
npx -y @bitmappunks/avatar-generator@0.0.5 --out "<output-path>" --seed "<seed>"
```

- `-y` 自动接受 npx 的安装提示。
- `@0.0.5` 版本锁必须保留——绝不要不带版本或用 `@latest` 跑。
- `<seed>` 优先使用用户提供的值；如果没有提供，则使用当前 Unix 时间戳（秒）。

## 预览

用 skill 自带的 `scripts/svg-tui.js`（路径从 skill 加载消息里给出的基础目录拼接）在终端里直接渲染刚生成的 SVG：

```bash
node "<skill-base-dir>/scripts/svg-tui.js" "<output-path>"
```

脚本解析头像的像素条，用 ANSI truecolor 块字符输出——任何支持 24 位色的终端 transcript 都能显示，除了 `node`（`npx` 已经依赖）之外不需要额外装东西。

## 确认

告诉用户输出文件的绝对路径和使用的 seed。一句话就够。

## 注意

- 输出只有 SVG。用户要 PNG 或改尺寸的话，单独转换（如 `rsvg-convert`、`sharp`）——不要悄悄改格式。
- 一次调用处理一个 seed。多个 seed 就循环多次调用。
- 如果 `npx` 报错（网络、registry、安装问题），直接把错误暴露给用户——不要悄悄重试，也不要退回到其它版本。
