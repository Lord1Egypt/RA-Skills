# AlphaShop 图像处理 SKILL

AlphaShop（遨虾）图像处理 API 工具集，支持图片翻译、高清放大、抠图、元素识别与消除、裁剪、虚拟试衣、模特换肤等 11 个接口。

更多有趣的电商SKILL，可以通过https://skill.alphashop.cn/获取，安全可靠的企业级别SKILL HUB

## ✨ 核心特性

- 🌐 **图片翻译** - 支持标准翻译和 PRO 翻译（源语种自动识别）
- 🔍 **高清放大** - 图片无损放大
- ✂️ **主题抠图** - 透明底或自定义背景色
- 🧹 **元素消除** - 智能消除水印、文字等
- 👗 **虚拟试衣** - AI 虚拟试穿效果
- 👤 **模特换肤** - 更换模特肤色和背景

## 🚀 快速开始

### 配置密钥

在 OpenClaw config 中配置：

```json5
{
  skills: {
    entries: {
      "alphashop-image": {
        env: {
          ALPHASHOP_ACCESS_KEY: "YOUR_AK",
          ALPHASHOP_SECRET_KEY: "YOUR_SK"
        }
      }
    }
  }
}
```

密钥获取：访问 https://www.alphashop.cn/seller-center/apikey-management 申请。

## 🎯 主要功能

### 图片翻译

```bash
# 标准翻译（中文→英文）
python scripts/alphashop_image.py translate \
  --image-url "https://example.com/img.jpg" \
  --source-lang zh --target-lang en

# PRO 翻译（自动识别源语种）
python scripts/alphashop_image.py translate-pro \
  --image-url "https://example.com/img.jpg" \
  --source-lang auto --target-lang ru
```

### 高清放大

```bash
python scripts/alphashop_image.py enlarge \
  --image-url "https://example.com/img.jpg" --factor 4
```

### 主题抠图

```bash
# 透明底
python scripts/alphashop_image.py extract-object \
  --image-url "https://example.com/img.jpg" --transparent true

# 白色背景
python scripts/alphashop_image.py extract-object \
  --image-url "https://example.com/img.jpg" --transparent false --bg-color "255,255,255"
```

### 元素消除

```bash
python scripts/alphashop_image.py remove-elements \
  --image-url "https://example.com/img.jpg" \
  --noobj-watermark 1 --noobj-character 1
```

### 图像裁剪

```bash
python scripts/alphashop_image.py crop \
  --image-url "https://example.com/img.jpg" \
  --target-width 800 --target-height 800
```

### 虚拟试衣

```bash
# 创建任务
python scripts/alphashop_image.py virtual-try-on \
  --model-images "https://example.com/model.jpg" \
  --clothes "https://example.com/shirt.jpg,tops" --count 1

# 查询结果
python scripts/alphashop_image.py query-try-on --task-id "abc123"
```

### 模特换肤

```bash
# 创建任务
python scripts/alphashop_image.py change-model \
  --image-url "https://example.com/img.jpg" \
  --model-type WHITE --bg-style NATURE --age YOUTH --gender FEMALE --num 2

# 查询结果
python scripts/alphashop_image.py query-change-model --task-id "xyz456"
```

## 📁 项目结构

```
alphashop-image/
├── SKILL.md                          # SKILL 配置文件
├── README.md                         # 本文档
├── requirements.txt                  # Python 依赖
├── references/
│   └── api-docs.md                   # API 详细文档
└── scripts/
    └── alphashop_image.py            # 图像处理主脚本
```

## 📝 注意事项

1. **异步接口** - 虚拟试衣和模特换肤为异步任务，需先创建再查询结果
2. **AlphaShop 欠费** - 如返回欠费错误，需前往 https://www.alphashop.cn/seller-center/home/api-list 购买积分

---

**最后更新**: 2026-03-19
