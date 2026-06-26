---
name: dit360-panorama-generator
description: 通过影石DiT360生成360度全景图，自动转格式并创建查看器
tags: [DiT360, Insta360, 全景图, AI生成, Pannellum]
---

# DiT360 Panorama Generator

通过影石开源的 DiT360 模型，输入文字描述即可生成 360 度全景图，并自动创建可交互查看的网页。

## 功能

- 🤖 调用 Hugging Face 上的 DiT360 Space 生成全景图
- 🔄 自动将 webp 转为 jpg 格式
- 🌐 创建 Pannellum 全景查看器网页
- 🚀 启动本地 HTTP 服务器，浏览器直接查看

## 前置要求

- Python 3.9+
- uv (Python 包管理器)
- 网络连接（访问 Hugging Face）

## 使用方法

### 快速生成

```bash
./scripts/generate.sh "sunset over ocean beach"
```

### 自定义参数

```bash
./scripts/generate.sh "cyberpunk city at night" 42 50
# 参数：描述, seed, 推理步数
```

## 输出文件

| 文件 | 说明 |
|------|------|
| `output/panorama_*.webp` | 原始生成文件 |
| `output/panorama_*.jpg` | 转换后的 jpg |
| `output/viewer.html` | Pannellum 查看器 |

## 查看全景图

生成完成后，脚本会自动：
1. 启动本地 HTTP 服务器（端口 8899）
2. 在浏览器中打开查看器
3. 鼠标拖动即可 360 度旋转查看

## 注意事项

- 首次生成需要等待 Hugging Face Space 启动（GPU 排队）
- 生成时间：30秒 ~ 3分钟（取决于排队情况）
- 图片尺寸：2048×1024（2:1 全景比例）

## 相关链接

- DiT360 GitHub: https://github.com/Insta360-Research-Team/DiT360
- Hugging Face Space: https://huggingface.co/spaces/Insta360-Research/DiT360
