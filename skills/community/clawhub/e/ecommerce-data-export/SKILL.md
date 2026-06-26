---
name: ecommerce-data-export
version: 1.0.0
description: 导出电商数据为 Excel/PDF 报告，支持价格历史、销量分析、竞品对比。适合电商卖家、市场分析师。
homepage: https://github.com/openclaw/skills
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "pandas",
              "kind": "pip",
              "package": "pandas openpyxl",
              "label": "安装依赖：pip3 install pandas openpyxl",
            },
          ],
      },
  }
---

# 电商数据导出技能

将电商数据导出为专业报告（Excel/PDF）。

## 功能

1. **价格历史导出**: 导出商品历史价格数据
2. **销量分析**: 生成销量趋势图表
3. **竞品对比**: 多商品对比报告
4. **定制模板**: 自定义报告格式
5. **定时生成**: 定期自动发送报告

## 使用方式

**导出数据**:
```
导出这个商品的价格历史为 Excel https://item.taobao.com/item.htm?id=123
```

**生成报告**:
```
生成我监控的 10 个商品的价格分析报告
```

**竞品对比**:
```
对比这 5 个商品的价格和销量，生成 PDF 报告
```

**定时报告**:
```
每周一早上 9 点生成上周销售报告
```

## 输出示例

生成 Excel 报告包含：
- 商品基本信息
- 价格历史数据表
- 价格趋势折线图
- 统计分析（均价、最高、最低）
- 建议售价

## 变现模式

- 免费：每月 3 次导出
- 付费 (¥79/月)：无限导出 + 定制模板
- 付费 (¥199/月)：+ 定时报告 + API 访问

## 优势

- ✅ B 端刚需
- ✅ 高客单价
- ✅ 易传播（报告带水印）
- ✅ 可扩展企业版

---

**声明**: 数据来自公开渠道，仅供参考。
