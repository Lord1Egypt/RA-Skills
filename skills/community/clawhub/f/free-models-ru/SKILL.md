---
name: free-models-ru
version: 1.0.0
description: Бесплатные AI модели для русскоязычных пользователей. Гайд по OpenRouter, SiliconFlow, Groq, Modal. Без VPN, без санкций.
metadata:
  openclaw:
    emoji: "🆓"
---

# Бесплатные AI модели для РФ

## OpenRouter (25+ бесплатных моделей)

| Модель | Контекст | Для чего |
|--------|----------|----------|
| nvidia/nemotron-3-super-120b-a12b:free | 262k | Топ бесплатная |
| stepfun/step-3.5-flash:free | 256k | Быстрая, китайская |
| qwen/qwen3-coder:free | 262k | Кодинг (rate limit 8 RPM) |
| openai/gpt-oss-120b:free | 131k | Стабильная |

API Key: https://openrouter.ai/keys

## SiliconFlow (98+ моделей, китайские)

| Модель | Цена |
|--------|------|
| Qwen3-8B | 🆓 Бесплатно |
| DeepSeek-R1-8B | 🆓 Бесплатно |
| Kimi K2 | Очень дёшево |

Регистрация: https://cloud.siliconflow.cn/i/ihj5inat

## Groq (бесплатно, быстро)

| Модель | Лимит |
|--------|-------|
| GPT OSS 120B | 40 req/min |
| Kimi K2.5 | 40 req/min |

API Key: https://console.groq.com

## Modal (GLM-5 бесплатно до апреля)

Регистрация: https://modal.com

## Конфиг для OpenClaw

```json
{
  "auth": {
    "profiles": {
      "openrouter:default": {
        "provider": "openrouter",
        "mode": "api_key",
        "apiKey": "sk-or-v1-ВАШ_КЛЮЧ"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/nvidia/nemotron-3-super-120b-a12b:free"
      }
    }
  }
}
```

## Советы
- Всегда проверяй актуальный список: openrouter.ai/models?max_price=0
- Используй каскадный конфиг: основная → запасная → fallback
- Rate limit: избегай моделей с <10 RPM для ботов
