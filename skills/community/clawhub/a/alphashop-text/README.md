# AlphaShop 文本处理 SKILL

AlphaShop（遨虾）文本处理 API 工具集，支持大模型文本翻译、生成商品多语言卖点和商品多语言标题。

更多有趣的电商SKILL，可以通过https://skill.alphashop.cn/获取，安全可靠的企业级别SKILL HUB

## ✨ 核心特性

- 🌐 **文本翻译** - 大模型驱动，支持批量翻译和源语种自动识别
- ✨ **卖点生成** - 根据商品信息生成多语言卖点文案
- 📝 **标题生成** - 生成 SEO 友好的多语言商品标题
- 🗣️ **多语言支持** - 支持 45 种语言

## 🚀 快速开始

### 配置密钥

在 OpenClaw config 中配置：

```json5
{
  skills: {
    entries: {
      "alphashop-text": {
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

### 文本翻译

```bash
# 中文→英文（支持批量）
python scripts/alphashop_text.py translate \
  --source-lang zh --target-lang en \
  --texts "你好世界" "这是一个测试"

# 自动识别源语种
python scripts/alphashop_text.py translate \
  --source-lang auto --target-lang ru \
  --texts "Hello World"
```

### 生成商品卖点

```bash
python scripts/alphashop_text.py selling-point \
  --product-name "纯棉女士T恤" \
  --category "女装/T恤" \
  --target-lang ru \
  --keywords "纯棉" "透气" \
  --spec "材质: 纯棉, 季节: 夏季"
```

### 生成商品标题

```bash
python scripts/alphashop_text.py title \
  --product-name "纯棉女士T恤短袖宽松版" \
  --category "女装/T恤" \
  --target-lang en \
  --count 3 \
  --keywords "cotton" "casual"
```

## 📁 项目结构

```
alphashop-text/
├── SKILL.md                          # SKILL 配置文件
├── README.md                         # 本文档
├── requirements.txt                  # Python 依赖
├── references/
│   └── api-docs.md                   # API 详细文档
└── scripts/
    └── alphashop_text.py             # 文本处理主脚本
```

## 📝 注意事项

1. **翻译源语种** - 支持 `auto` 自动识别
2. **标题生成语言对** - 中文→14种语言，英语→14种语言
3. **AlphaShop 欠费** - 如返回欠费错误，需前往 https://www.alphashop.cn/seller-center/home/api-list 购买积分

---

**最后更新**: 2026-03-19
