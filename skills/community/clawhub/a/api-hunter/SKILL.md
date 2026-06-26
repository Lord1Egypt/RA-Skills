# API Hunter Skill

## 功能
全自動 API 服務商獵人 - 根據功能需求搜尋免費 API

## 安裝
```bash
# 依賴已安裝
pip install beautifulsoup4 requests
```

## 使用方式

### 方法 1: Python 程式碼
```python
from api_hunter import hunt

# 搜尋天氣 API
report = hunt("weather")

# 搜尋 AI 圖片生成 API
report = hunt("AI image generation")

# 搜尋翻譯 API
report = hunt("translation")
```

### 方法 2: 命令列
```bash
cd ~/.openclaw/ai-operator/skills
python api_hunter/hunter.py "weather"
```

### 方法 3: 實例化
```python
from api_hunter import APIHunter

hunter = APIHunter()

# 自訂搜尋
results = hunter.search("stock market data")
print(results)

# 獵取並生成報告
report = hunter.hunt("email verification")
```

## 輸出範例

```
## 🎯 weather API 獵人報告

### 搜尋結果

1. 🌤️ Free Open-Source Weather API | Open-Meteo.com
   URL: https://open-meteo.com/
   
2. Free Weather API - WeatherAPI.com
   URL: https://www.weatherapi.com/

### ✅ 無需註冊的 API

| API 名稱 | 網址 |
|----------|------|
| Open-Meteo | https://open-meteo.com/ |
| OpenWeatherMap | https://openweathermap.org/api |
```

## 已知免費 API 清單

### 天氣
| API | URL | 特色 |
|-----|-----|------|
| Open-Meteo | https://open-meteo.com/ | 無需 API Key |
| OpenWeatherMap | https://openweathermap.org/api | 免費 tier |

### 資料
| API | URL | 特色 |
|-----|-----|------|
| JSONPlaceholder | https://jsonplaceholder.typicode.com/ | 測試用 |
| Public APIs | https://github.com/public-apis/public-apis | 集合 |

### AI/ML
| API | URL | 特色 |
|-----|-----|------|
| **Puter.js** | https://developer.puter.com/ | 完全免費，無需 API Key，客戶端直接調用 |
| HuggingFace | https://huggingface.co/inference-api | 免費 tier |
| OpenAI | https://platform.openai.com/ | 免費 credit |

### 圖片生成 (完全免費，無需 API Key)

**Puter.js** - 最強大的免費選擇：
```html
<script src="https://js.puter.com/v2/"></script>
<script>
puter.ai.txt2img("A cute cat").then(img => {
    document.body.appendChild(img);
});
</script>
```

支持的模型：
- GPT Image (1, 1.5, 1.5-mini)
- DALL-E 2/3
- Gemini 2.5 Flash Image
- Flux.1 Schnell / Pro
- Stable Diffusion 3 / XL
- HiDream-I1
- Qwen-Image

## 限制
- 臨時郵件服務有時不穩定
- 部分網站需要 Cloudflare 驗證
- 建議優先使用無需註冊的 API
