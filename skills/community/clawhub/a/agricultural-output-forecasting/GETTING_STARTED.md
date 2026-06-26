# 🚀 Getting Started

Get up and running with Agricultural Output Forecasting in 5 minutes!

## ⚡ Quick Start (Zero Configuration)

The fastest way to try the skill - no setup required!

### Step 1: Run the Demo
```bash
cd /home/node/.openclaw/workspace/skills/agricultural-output-forecasting
python demo.py
```

This will:
- Generate forecasts for 3 sample crops
- Show yield predictions and recommendations
- Demonstrate all features

### Step 2: Try with Your Own Data
```bash
python demo.py --crop wheat --area 50 --region "North China Plain" --season spring
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies
```bash
# No external dependencies required!
# The skill uses only Python standard library
```

## 🎯 Basic Usage

### Using the Demo Script
```bash
# Run with built-in examples
python demo.py

# Run with custom parameters
python demo.py --crop rice --area 100 --region "Yangtze River Delta" --season summer

# Save output to file
python demo.py --crop corn --area 200 --output forecast.json
```

### Using the Python API
```python
from scripts.forecast import forecast_output

# Generate forecast (free trial - no API key needed!)
result = forecast_output(
    crop_type="wheat",
    area_hectares=100,
    region="North China Plain",
    season="spring",
    user_id="user_123"
)

print(result["forecast"]["yield_forecast"])
```

### Using Command Line
```bash
python scripts/forecast.py \
  --crop wheat \
  --area 100 \
  --region "North China Plain" \
  --season spring \
  --user-id "user_123"
```

## 🎁 Free Trial

Every new user gets **10 free calls** - no credit card required!

```python
result = forecast_output(
    crop_type="wheat",
    area_hectares=100,
    region="North China Plain",
    season="spring",
    user_id="your_unique_user_id"  # Any string works!
)

# Check remaining free calls
if result.get("trial_mode"):
    print(f"剩余免费次数: {result['trial_remaining']}")
```

## 💳 After Free Trial

When your free trial ends:

1. Get an API key from [skillpay.me](https://skillpay.me)
2. Set environment variable:
   ```bash
   export SKILL_BILLING_API_KEY="your-api-key"
   export SKILL_ID="your-skill-id"
   ```
3. Continue using the skill - only $0.001 per call!

## 📋 Supported Crops

### Grains
- Wheat (小麦)
- Rice (水稻)
- Corn (玉米)
- Barley (大麦)
- Sorghum (高粱)

### Vegetables
- Tomato (番茄)
- Potato (土豆)
- Cabbage (卷心菜)
- Cucumber (黄瓜)

### Fruits
- Apple (苹果)
- Orange (橙子)
- Grape (葡萄)
- Peach (桃子)

### Others
- Soybean (大豆)
- Cotton (棉花)
- Sugarcane (甘蔗)

## 📤 Output Format

The skill returns detailed forecast information:

```json
{
  "forecast_id": "AGR_20240306120000",
  "crop_type": "wheat",
  "region": "North China Plain",
  "season": "spring",
  "area_hectares": 100,
  "yield_forecast": {
    "per_hectare": 6.5,
    "total": 650,
    "unit": "tons",
    "confidence_interval": {
      "lower": 5.5,
      "upper": 7.5,
      "confidence": "85%"
    }
  },
  "factors": {
    "weather_factor": 1.05,
    "market_factor": 1.02
  },
  "risk_assessment": {
    "level": "low",
    "weather_risk": "low"
  },
  "recommendations": [
    "市场价格有利，建议扩大种植面积",
    "建议购买农业保险以降低风险"
  ]
}
```

## 🌍 Supported Regions

The skill supports any region name. Examples:
- North China Plain (华北平原)
- Yangtze River Delta (长江三角洲)
- Northeast China (东北地区)
- Sichuan Basin (四川盆地)
- Any custom region name

## 📅 Supported Seasons

- Spring (春季)
- Summer (夏季)
- Autumn/Fall (秋季)
- Winter (冬季)

## 🔧 Troubleshooting

### "User ID is required"
Make sure to provide a user_id parameter:
```python
forecast_output(crop_type="wheat", area_hectares=100, 
                region="North China", season="spring", 
                user_id="any_unique_id")
```

### "Unsupported crop type"
Check the supported crops list above. Use English names:
```python
# ✅ Correct
forecast_output(crop_type="wheat", ...)

# ❌ Incorrect
forecast_output(crop_type="小麦", ...)
```

### Permission Denied
If you see permission errors for `~/.openclaw/`:
```bash
mkdir -p ~/.openclaw/skill_trial
chmod 755 ~/.openclaw
```

## 📚 Next Steps

- Read the [full documentation](SKILL.md)
- Check out [examples](EXAMPLES.md)
- See [FAQ](FAQ.md) for common questions
- Review [security policy](SECURITY.md)

## 💬 Need Help?

- 📧 Email: support@openclaw.dev
- 💬 Discord: [Join our community](https://discord.gg/openclaw)
- 🐛 Issues: [GitHub Issues](https://github.com/openclaw/skills/issues)

---

**Happy Forecasting! 🌾**
