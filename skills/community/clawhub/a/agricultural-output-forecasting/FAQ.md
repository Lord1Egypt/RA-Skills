# Frequently Asked Questions (FAQ)

## General Questions

### What is Agricultural Output Forecasting?
Agricultural Output Forecasting is a big data-driven tool that predicts crop yields based on historical data, weather patterns, and market trends. It helps farmers, agronomists, and agricultural businesses make data-driven decisions.

### Is it free to use?
Yes! Every new user gets **10 free calls** with no credit card required. After that, it's only $0.001 per call.

### Do I need an API key?
- **For the first 10 calls**: No API key needed!
- **After free trial**: Yes, you'll need a SkillPay API key

### What crops are supported?
We support 16+ crops including:
- Grains: wheat, rice, corn, barley, sorghum
- Vegetables: tomato, potato, cabbage, cucumber
- Fruits: apple, orange, grape, peach
- Others: soybean, cotton, sugarcane

## Usage Questions

### How accurate are the forecasts?
Forecast accuracy depends on:
- Quality of input data
- Regional weather patterns
- Market stability

Typical confidence intervals are 70-95%.

### What regions are supported?
Any region can be specified by name. The skill uses the region name to apply appropriate weather and soil factors.

### Can I forecast for multiple fields?
Yes, call the API for each field:
```python
for field in fields:
    result = forecast_output(
        crop_type=field["crop"],
        area_hectares=field["area"],
        region=field["region"],
        season=field["season"],
        user_id="user_123"
    )
```

### How often should I run forecasts?
We recommend:
- **Before planting**: For planning decisions
- **Mid-season**: To adjust expectations
- **Before harvest**: For logistics planning

## Technical Questions

### What data is stored?
Only **free trial usage counts** are stored locally:
- User ID (hashed)
- Number of calls used
- Timestamps

**No agricultural data is ever stored.**

### Is my data secure?
Yes! See our [Security Policy](SECURITY.md) for details. Key points:
- Farm data is processed locally
- No data is transmitted to third parties
- All code is open source and auditable

### What are the system requirements?
- Python 3.8+
- No external dependencies
- Works offline (except for billing after trial)

### Can I integrate this with my farm management software?
Yes! The skill provides a simple Python API that can be integrated into any system:
```python
from scripts.forecast import forecast_output

# Integrate with your system
result = forecast_output(...)
```

## Billing Questions

### How much does it cost?
- **First 10 calls**: Free
- **After trial**: $0.001 USDT per call

### What payment methods are accepted?
Payments are processed via SkillPay using BNB Chain USDT.

### How do I check my balance?
```python
result = forecast_output(...)
print(f"Balance: {result.get('balance')}")
```

### What happens if I run out of balance?
You'll receive a payment URL to top up your account:
```python
if "paymentUrl" in result:
    print(f"Please recharge: {result['paymentUrl']}")
```

## Troubleshooting

### "User ID is required" error
You must provide a user_id parameter:
```python
forecast_output(crop_type="wheat", area_hectares=100, 
                region="North China", season="spring",
                user_id="any_unique_string")
```

### "Unsupported crop type" error
Use English crop names:
```python
# ✅ Correct
forecast_output(crop_type="wheat", ...)

# ❌ Incorrect  
forecast_output(crop_type="小麦", ...)
```

### Permission denied errors
Create the required directory:
```bash
mkdir -p ~/.openclaw/skill_trial
chmod 755 ~/.openclaw
```

### Forecast seems unrealistic
Forecasts are estimates based on historical patterns. Factors like:
- Extreme weather events
- Pest outbreaks
- Market disruptions

may cause actual yields to differ.

## Business Questions

### Can I use this for commercial farming?
Yes! The skill is designed for both small and large-scale agricultural operations.

### Is there an enterprise plan?
For high-volume usage, contact us at enterprise@openclaw.dev for custom pricing.

### Can I white-label this for my clients?
Contact us at enterprise@openclaw.dev to discuss partnership opportunities.

## Getting Help

### Where can I get support?
- 📧 Email: support@openclaw.dev
- 💬 Discord: [Join our community](https://discord.gg/openclaw)
- 🐛 GitHub Issues: [Report bugs](https://github.com/openclaw/skills/issues)

### How do I report a bug?
Please include:
1. Crop type and region
2. Expected vs actual output
3. Python version

### Can I request new crop types?
Yes! Please open a feature request on GitHub. We're constantly expanding our crop database.

---

**Still have questions?** Contact us at support@openclaw.dev
