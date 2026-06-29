---
name: 2d-print
description: "2D 打印控制。通过 macOS CUPS 系统将图片、PDF 等文件发送到本地打印机。支持选择打印机、设置份数、纸张大小等参数。当用户提到 2D 打印、打印图片、打印文件时激活。"
version: "1.0.0"
author: 打印侠
---

# 2D 打印 Skill

通过 macOS 内置的 CUPS 打印系统（`lp` / `lpstat` 命令）控制本地打印机。

## 已知打印机

| 打印机名称 | 类型 | 备注 |
|------------|------|------|
| Epson-L4260 | 爱普生墨仓式实体打印机 | 主力打印机 |
| TencentCloudPrinterPS | 腾讯云虚拟打印机 | 远程打印用 |

## 常用命令

### 查看可用打印机

```bash
lpstat -p
```

### 打印文件

```bash
# 基本打印（默认打印机）
lp <文件路径>

# 指定打印机
lp -d Epson-L4260 <文件路径>

# 指定份数
lp -d Epson-L4260 -n 3 <文件路径>

# 指定纸张大小（A4/Letter 等）
lp -d Epson-L4260 -o media=A4 <文件路径>

# 横向打印
lp -d Epson-L4260 -o landscape <文件路径>

# 彩色打印
lp -d Epson-L4260 -o ColorModel=Color <文件路径>

# 灰度打印
lp -d Epson-L4260 -o ColorModel=Gray <文件路径>

# 打印质量（draft/normal/high）
lp -d Epson-L4260 -o print-quality=high <文件路径>
```

### 查看打印队列

```bash
lpq -d Epson-L4260
```

### 取消打印任务

```bash
cancel <job-id>
# 或取消所有任务
cancel -a Epson-L4260
```

### 查看打印机详细信息

```bash
lpstat -l -p Epson-L4260
```

## 支持的文件格式

- 图片：PNG、JPEG、GIF、TIFF、BMP
- 文档：PDF
- 文本：TXT

## 打印路径

- 2D 打印素材目录：`/Users/yanfenma/workspace/baby/print`

## 注意事项

- macOS 自带 CUPS，无需额外安装驱动
- Epson L4260 是墨仓式打印机，支持彩色和灰度
- 大图打印注意纸张大小匹配
- 打印前建议先确认打印机状态：`lpstat -p Epson-L4260`
