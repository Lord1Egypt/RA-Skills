---
name: dwg-to-dxf-converter
version: 1.0.0
description: >
  专门用于在 Windows 环境下将 AutoCAD DWG 图纸转换为 DXF 格式。
  当用户提到“DWG转DXF”、“图纸格式转换”、“处理DWG”，或工作流接收到 .dwg 后缀的文件并需要解析前置处理时，必须立即触发本技能。
---

# DWG 转 DXF 转换技能 (本地调用版)

## 🛠️ 运行机制
本技能通过调用位于 `tools/oda/` 目录下的本地绿色版 ODA File Converter 执行静默转换。

## 🚀 执行指令
Agent 在接收到 DWG 文件后，应调用 Python 脚本进行转换：

```cmd
python scripts\dwg_to_dxf.py "输入文件绝对路径.dwg" "输出目录绝对路径\"