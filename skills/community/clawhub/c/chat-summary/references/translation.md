# 翻译集成指南

## 支持的翻译服务

### 1. DeepL API（推荐）
**优点**：质量高，支持中文
**缺点**：付费（有免费额度）

```python
import deepl

translator = deepl.Translator("YOUR_DEEPL_API_KEY")
result = translator.translate_text("你好", target_lang="EN-US")
print(result.text)  # "Hello"
```

**支持语言**：
- 中文（简体/繁体）
- 英文
- 日文
- 韩文
- 德文、法文、西班牙文等 20+ 语言

### 2. Google Translate API
**优点**：语言支持多
**缺点**：需要信用卡

```python
from google.cloud import translate_v2 as translate

client = translate.Client()
result = client.translate("你好", target_language='en')
print(result['translatedText'])
```

### 3. OpenAI API
**优点**：已有 API Key 可直接用
**缺点**：成本较高

```python
from openai import OpenAI

client = OpenAI(api_key="sk-xxx")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Translate to English"},
        {"role": "user", "content": "你好"}
    ]
)
print(response.choices[0].message.content)
```

### 4. LibreTranslate（免费/自托管）
**优点**：免费，可自托管
**缺点**：质量一般

```python
import requests

response = requests.post("https://libretranslate.com/translate", json={
    "q": "你好",
    "source": "zh",
    "target": "en",
    "format": "text"
})
print(response.json()["translatedText"])
```

## 在 chat-summary 中使用翻译

### 场景 1：跨语言汇总
用户要求："用英文总结今天的中文讨论"

```python
def summarize_with_translation(messages, output_lang):
    # 1. 生成原文摘要
    summary = generate_summary(messages, lang='auto')
    
    # 2. 翻译摘要
    if output_lang != detect_language(summary):
        summary = translate_text(summary, target_lang=output_lang)
    
    return summary
```

### 场景 2：多语言混合聊天
当聊天包含多种语言时：

```python
def handle_multilingual_chat(messages):
    # 1. 检测语言分布
    distribution = detect_mixed_languages(messages)
    
    # 2. 按语言分组
    lang_groups = group_by_language(messages)
    
    # 3. 分别生成摘要
    summaries = {}
    for lang, msgs in lang_groups.items():
        summaries[lang] = generate_summary(msgs, lang=lang)
    
    # 4. 合并或翻译
    return merge_summaries(summaries)
```

## 语言代码对照表

| 代码 | 语言 | DeepL | Google | OpenAI |
|------|------|-------|--------|--------|
| zh-CN | 简体中文 | ZH | zh-CN | zh-CN |
| zh-TW | 繁体中文 | ZH | zh-TW | zh-TW |
| en | 英文 | EN-US | en | en |
| ja | 日文 | JA | ja | ja |
| ko | 韩文 | KO | ko | ko |

## 最佳实践

1. **保持原文**：默认不翻译，除非用户明确要求
2. **质量检查**：翻译后保留关键术语原文
3. **成本优化**：优先使用已有 API（如 OpenAI）
4. **缓存**：相同文本避免重复翻译

## 配置示例

```json
{
  "translation": {
    "provider": "deepl",
    "apiKey": "xxx",
    "defaultTarget": "zh-CN",
    "cacheEnabled": true
  }
}
```
