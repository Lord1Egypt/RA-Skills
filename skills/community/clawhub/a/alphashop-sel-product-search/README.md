# 商品搜索 API SKILL

通过 AlphaShop REST API 调用遨虾 AI 选品系统的商品搜索服务，支持 Amazon 和 TikTok 平台的关键词商品搜索。

更多有趣的电商SKILL，可以通过https://skill.alphashop.cn/获取，安全可靠的企业级别SKILL HUB

## ✨ 核心特性

- 🔍 **关键词搜索** - 根据关键词搜索目标平台商品
- 🎯 **多维度筛选** - 支持价格、销量、评分、上架时间等筛选
- 🌍 **多平台支持** - Amazon（8个国家）和 TikTok（15个国家）
- 📦 **丰富数据** - 返回商品详情、供应商信息、规格参数、物流选项

## 🚀 快速开始

### 配置密钥

在 OpenClaw config 中设置：

```json5
{
  skills: {
    entries: {
      "alphashop-sel-product-search": {
        env: {
          ALPHASHOP_ACCESS_KEY: "你的AccessKey",
          ALPHASHOP_SECRET_KEY: "你的SecretKey"
        }
      }
    }
  }
}
```

密钥获取：访问 https://www.alphashop.cn/seller-center/apikey-management 申请。

## 🎯 使用方法

### 基础搜索

```bash
# 搜索 Amazon 美国市场
python3 scripts/search.py --keyword "phone" --platform amazon --region US

# 搜索 TikTok 印尼市场
python3 scripts/search.py --keyword "yoga pants" --platform tiktok --region ID
```

### 带筛选条件

```bash
python3 scripts/search.py \
  --keyword "phone" --platform amazon --region US \
  --min-price 10 --max-price 100 \
  --min-sales 100 --min-rating 4.0 \
  --listing-time 90 --count 20
```

## 📁 项目结构

```
alphashop-sel-product-search/
├── SKILL.md                    # SKILL 配置文件
├── README.md                   # 本文档
├── references/
│   └── api.md                  # API 参考文档
└── scripts/
    └── search.py               # 商品搜索主脚本
```

## 📝 注意事项

1. **必填参数** - `--keyword`、`--platform`、`--region` 为必填项
2. **平台支持** - Amazon: US/UK/JP/DE/FR/IT/ES/CA；TikTok: ES/PH/FR/ID/MX/VN/DE/JP/TH/SG/BR/IT/US/GB/MY
3. **上架时间** - 支持 90/180/365 天
4. **价格单位** - 所有价格以美元计价
5. **评分范围** - 评分必须在 0-5.0 之间

---

**最后更新**: 2026-03-19
