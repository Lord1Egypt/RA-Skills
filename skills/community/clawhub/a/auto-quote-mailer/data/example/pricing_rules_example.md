# Example Pricing Rules - Medal Customization

This is an example pricing rule file for custom medal manufacturing business. Replace this with your own pricing rules.

---

# 报价规则示例 - 奖牌定制

这是奖牌定制行业的报价规则示例文件，请用您自己的报价规则替换此文件。

## 材质基础价格 / Material Base Prices

| Material Category | Retail Price (1-5pcs) | Bulk Price (50+pcs) | Description |
|-------------------|-----------------------|---------------------|-------------|
| Gold Foil/Wood | ¥85 | ¥45 | Classic style for authorization plaques |
| Crystal/Glass | ¥120 | ¥65 | Transparent and shiny for anniversaries |
| Metal Casting | ¥180 | ¥90 | Heavy texture with relief, requires mold fee |
| Acrylic/Composite | ¥55 | ¥28 | Colorful and various shapes |

## Size Coefficient / 尺寸系数

- **S** (< 15cm): 0.8 × base price
- **M** (15cm - 25cm): 1.0 × base price
- **L** (25cm - 40cm): 1.5 × base price
- **XL** (> 40cm): Quote manually

## Additional Process Fees / 附加工艺费

| Process | Fee (per unit) | Notes |
|---------|----------------|-------|
| 3D Laser Engraving | ¥20 | Only for crystal |
| UV Color Printing | ¥10 | Good for complex logos |
| Metal Etching + Paint | ¥30 | Durable, never fade |
| Gold Foil Stamping | ¥5 | For text on wood |
| Premium Wooden Box | ¥35 | Gift packaging |
| Heavy Marble Base | ¥25 | More stable and premium |

## Quantity Discounts / 数量折扣

- 1 - 5 pieces: Full price (100%)
- 6 - 20 pieces: 95% of total
- 21 - 100 pieces: 85% of total
- 101+ pieces: 70% of total

## Additional Terms / 附加条款

1. Standard packaging is included in the price
2. Sample can be ready in 24 hours after design confirmation
3. If damaged during shipping, free replacement after photo confirmation
4. Free domestic shipping for orders over ¥2000
5. Payment: 30% deposit, 70% before shipping

---

## How to Use This Example

1. Copy this file to `../pricing_rules.md`
2. Replace all the example data with your actual pricing
3. Update the `MATERIAL_PRICES`, `SIZE_COEFFICIENTS`, `PROCESS_FEES` and `DISCOUNTS` in `scripts/quote_calculator.py` to match this file

## 如何使用此示例

1. 复制此文件到 `../pricing_rules.md`
2. 将所有示例数据替换为您的实际报价
3. 更新 `scripts/quote_calculator.py` 中的 `MATERIAL_PRICES`、`SIZE_COEFFICIENTS`、`PROCESS_FEES` 和 `DISCOUNTS` 与此文件对应

