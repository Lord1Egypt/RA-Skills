---
name: alphashop-text
category: official-1688
description: >-
  AlphaShop（遨虾）文本处理 API 工具集。支持3个接口：大模型文本翻译、
  生成商品多语言卖点、生成商品多语言标题。
  触发场景：翻译文本、文字翻译、多语言翻译、生成卖点、商品卖点、
  多语言卖点、生成标题、商品标题、多语言标题、SEO标题、
  AlphaShop文本、遨虾文本处理。
metadata:
  version: 1.0.1
  label: 文本处理
  author: 1688官方技术团队
---

# AlphaShop 文本处理

通过 `scripts/alphashop_text.py` 调用遨虾文本处理 API。

## 前置配置（必须先完成）

⚠️ **使用本 SKILL 前，必须先配置以下环境变量，否则所有接口调用都会失败。**

| 环境变量 | 说明 | 必填 | 获取方式 |
|---------|------|------|---------|
| `ALPHASHOP_ACCESS_KEY` | AlphaShop API 的 Access Key | ✅ 必填 | 可以访问1688-AlphaShop（遨虾）来申请 https://www.alphashop.cn/seller-center/apikey-management ，直接使用1688/淘宝/支付宝/手机登录即可 |
| `ALPHASHOP_SECRET_KEY` | AlphaShop API 的 Secret Key | ✅ 必填 | 可以访问1688-AlphaShop（遨虾）来申请 https://www.alphashop.cn/seller-center/apikey-management ，直接使用1688/淘宝/支付宝/手机登录即可 |

**⚠️ AlphaShop 接口欠费处理：** 如果调用 AlphaShop 接口时返回欠费/余额不足相关的错误，**必须立即中断当前流程**，提示用户前往 https://www.alphashop.cn/seller-center/home/api-list 购买积分后再继续操作。

### 配置方式

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

如果用户没有提供这些密钥，**必须先询问用户获取后再继续操作**。

## 命令速查

脚本路径：`scripts/alphashop_text.py`

| 命令 | 功能 | 必填参数 |
|------|------|----------|
| `translate` | 大模型文本翻译 | `--source-lang` `--target-lang` `--texts` |
| `selling-point` | 生成商品多语言卖点 | `--product-name` `--category` `--target-lang` |
| `title` | 生成商品多语言标题 | `--product-name` `--category` `--target-lang` |

## 使用示例

```bash
# 文本翻译（中文→英文，支持批量）
python scripts/alphashop_text.py translate \
  --source-lang zh --target-lang en \
  --texts "你好世界" "这是一个测试"

# 自动识别源语种
python scripts/alphashop_text.py translate \
  --source-lang auto --target-lang ru \
  --texts "Hello World"

# 生成商品卖点（俄语）
python scripts/alphashop_text.py selling-point \
  --product-name "纯棉女士T恤" \
  --category "女装/T恤" \
  --target-lang ru \
  --keywords "纯棉" "透气" \
  --spec "材质: 纯棉, 季节: 夏季"

# 生成商品标题（生成3条英文标题）
python scripts/alphashop_text.py title \
  --product-name "纯棉女士T恤短袖宽松版" \
  --category "女装/T恤" \
  --target-lang en \
  --count 3 \
  --keywords "cotton" "casual"
```

## 语言支持

- **翻译**：源语种支持 auto 自动识别，目标语种见语言代码表
- **卖点/标题生成**：支持45种语言，详见 `references/api-docs.md` 语言代码表
- **标题生成语言对**：中文→14种语言，英语→14种语言

## API 详细文档

完整参数说明和语言代码表见 `references/api-docs.md`。
