# audio-analyze-skill-for-openclaw

Транскрибируйте и анализируйте аудио/видео контент с высокой точностью. [Работает на базе Evolink.ai](https://evolink.ai/?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

🌐 English | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Türkçe](README.tr.md) | [Русский](README.ru.md)

## Что это?

Автоматически транскрибируйте и анализируйте ваши аудио/видео файлы с помощью Gemini 3.1 Pro. [Получите бесплатный ключ API →](https://evolink.ai/signup?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

## Установка

### Через ClawHub (Рекомендуется)

```bash
openclaw skills add https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
```

### Ручная установка

```bash
git clone https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
cd audio-analyze-skill-for-openclaw
pip install -r requirements.txt
```

## Конфигурация

| Переменная | Описание | По умолчанию |
| :--- | :--- | :--- |
| `EVOLINK_API_KEY` | Ключ API EvoLink | (Обязательно) |
| `EVOLINK_MODEL` | Модель транскрибации | gemini-3.1-pro-preview-customtools |

*Для получения подробной информации о конфигурации API и поддержке моделей обратитесь к [Документации API EvoLink](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze).*

## Использование

### Базовое использование

```bash
export EVOLINK_API_KEY="your-key-here"
./scripts/transcribe.sh audio.mp3
```

### Расширенное использование

```bash
./scripts/transcribe.sh audio.mp3 --diarize --lang ja
```

### Пример вывода

* **TL;DR**: Аудио представляет собой пример трека для тестирования.
* **Основные выводы**: Звук высокой точности, четкая частотная характеристика.
* **План действий**: Загрузить в продакшн для финального тестирования.

## Доступные модели

- **Серия Gemini** (OpenAI API — `/v1/chat/completions`)

## Структура файлов

```
.
├── README.md
├── SKILL.md
├── _meta.json
├── scripts/
│   └── transcribe.sh
└── references/
    └── api-params.md
```

## Устранение неполадок

- **Argument list too long (Слишком длинный список аргументов)**: Используйте временные файлы для больших аудиоданных.
- **API Key Error (Ошибка ключа API)**: Убедитесь, что переменная `EVOLINK_API_KEY` экспортирована.

## Ссылки

- [ClawHub](https://clawhub.ai/EvoLinkAI/audio-analyze)
- [Справочник по API](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)
- [Сообщество](https://discord.com/invite/5mGHfA24kn)
- [Поддержка](mailto:support@evolink.ai)

## Лицензия

MIT