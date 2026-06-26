# Agricultural Output Forecasting

A big data-driven agricultural product output forecasting tool that helps farmers, agronomists, and agricultural businesses predict crop yields and production outputs.

## Features

- **Yield Prediction** - Forecast crop yields based on historical data and current conditions
- **Weather Impact Analysis** - Factor in weather patterns and climate data
- **Market Trend Integration** - Consider market prices and demand trends
- **Multi-Crop Support** - Support for various agricultural products (grains, vegetables, fruits, etc.)
- **SkillPay Billing** - Pay-per-use monetization (1 token per call, ~0.001 USDT)

## Installation

1. Clone or download this skill to your OpenClaw workspace:
```bash
cd /home/node/.openclaw/workspace/skills/
```

2. Install Python dependencies (if any additional packages are needed):
```bash
pip install -r requirements.txt  # if requirements.txt exists
```

3. Copy the environment variables file and configure:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

## Environment Variables Configuration

Copy `.env.example` to `.env` and configure the following variables:

### Required Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SKILL_BILLING_API_KEY` | Your SkillPay API key for billing | Yes |
| `SKILL_ID` | Your Skill ID from SkillPay dashboard | Yes |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key for weather data | - |
| `WEATHERAPI_KEY` | WeatherAPI key for alternative weather data | - |
| `USDA_API_KEY` | USDA API key for US agricultural data | - |
| `OPENAI_API_KEY` | OpenAI API key for enhanced forecasting | - |
| `CACHE_DURATION_MINUTES` | Cache duration for weather/market data | 60 |
| `MAX_FORECAST_AREA` | Maximum area in hectares per request | 10000 |

## Usage Examples

### Python API

```python
from scripts.forecast import forecast_output
import os

# Set environment variables
os.environ["SKILL_BILLING_API_KEY"] = "your-api-key"
os.environ["SKILL_ID"] = "your-skill-id"

# Forecast wheat yield
result = forecast_output(
    crop_type="wheat",
    area_hectares=100,
    region="North China Plain",
    season="spring",
    user_id="user_123"
)

# Check result
if result["success"]:
    print("预测产量:", result["forecast"])
    print("剩余余额:", result["balance"])
else:
    print("错误:", result["error"])
    if "paymentUrl" in result:
        print("充值链接:", result["paymentUrl"])
```

### Command Line

```bash
# Set environment variables
export SKILL_BILLING_API_KEY="your-api-key"
export SKILL_ID="your-skill-id"

# Run forecast
python scripts/forecast.py \
  --crop wheat \
  --area 100 \
  --region "North China Plain" \
  --season spring \
  --user-id "user_123"
```

## Supported Crops

- **Grains**: wheat, rice, corn, barley, sorghum
- **Vegetables**: tomato, potato, cabbage, cucumber
- **Fruits**: apple, orange, grape, peach
- **Others**: soybean, cotton, sugarcane

## Output Format

Forecast results include:
- Predicted yield (tons/hectare)
- Confidence interval
- Weather impact factor
- Market price prediction
- Risk assessment
- Recommendations

## Security Considerations

### Data Privacy

- Agricultural data is treated as confidential business information
- No personally identifiable information (PII) is collected
- Weather and market data is cached to minimize API calls

### API Key Security

- Never commit API keys to version control
- Use environment variables for all sensitive configuration
- Rotate API keys regularly
- Monitor API usage for anomalies

### Best Practices

1. Use `.env` file for configuration (already in `.gitignore`)
2. Implement rate limiting for high-volume usage
3. Cache weather data to reduce API costs
4. Validate input parameters before processing

## Pricing

- **Provider**: skillpay.me
- **Pricing**: 1 token per call (~0.001 USDT)
- **Chain**: BNB Chain
- **Minimum Deposit**: 8 USDT

## References

- For forecast methodology: see [references/forecast-methodology.md](references/forecast-methodology.md)
- For billing API details: see [references/skillpay-billing.md](references/skillpay-billing.md)

## License

See LICENSE file for details.

## Disclaimer

This tool provides forecasts based on available data and models. Actual yields may vary due to unforeseen circumstances. Use as a decision support tool, not as a guarantee of outcomes.
