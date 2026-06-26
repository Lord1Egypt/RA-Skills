# ElevenLabs Voice Pipeline

Скилл для работы с ElevenLabs Text-to-Speech API: синтез речи, выбор голосов, пакетная генерация, интеграция с Telegram voice notes, многозыковой синтез, клонирование голоса и обработка ошибок.

## Когда использовать

- Пользователь хочет синтезировать речь из текста через ElevenLabs
- Нужно сгенерировать голосовое сообщение для Telegram
- Требуется клонировать голос по аудиообразцу
- Пользователь работает с несколькими языками и голосами
- Нужна пакетная генерация аудиофайлов (аудиокниги, подкасты)
- Пользователь жалуется на качество или ошибки ElevenLabs API
- Требуется интеграция ElevenLabs с Telegram-ботом

## Инструкции

### 1. Настройка API

```python
import os
import aiohttp
import asyncio
from pathlib import Path
from typing import Optional

# Конфигурация
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"

HEADERS = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY,
}

# Доступные модели (на май 2026)
MODELS = {
    "eleven_multilingual_v2": "Лучшее качество, 29 языков",
    "eleven_monolingual_v1": "Английский, высшее качество",
    "eleven_turbo_v2": "Быстрый синтез, 37 языков",
    "eleven_flash_v2": "Мгновенный синтез, низкая задержка",
    "eleven_flash_v2_5": "Flash с улучшенным качеством",
}
```

**Установка и проверка:**
```bash
# Проверка API ключа
curl -s -H "xi-api-key: $ELEVENLABS_API_KEY" \
  https://api.elevenlabs.io/v1/voices | python3 -m json.tool

# Установка зависимостей
pip install aiohttp pydub python-telegram-bot
```

### 2. Управление голосами

**Получение списка голосов:**

```python
async def list_voices(category: str | None = None) -> list[dict]:
    """Получает список доступных голосов.

    category: 'premade' — готовые голоса ElevenLabs
              'cloned' — клонированные голоса пользователя
              'professional' — профессиональные голоса
              None — все голоса
    """
    url = f"{ELEVENLABS_BASE_URL}/voices"
    if category:
        url += f"?category={category}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Failed to list voices: {resp.status}")
            data = await resp.json()
            return data.get("voices", [])
```

**Выбор голоса по параметрам:**

```python
async def find_voice(
    name: str | None = None,
    accent: str | None = None,
    gender: str | None = None,
    language: str | None = None,
    max_results: int = 5,
) -> list[dict]:
    """Ищет голос по заданным критериям."""
    voices = await list_voices()
    results = []

    for voice in voices:
        match = True
        if name and name.lower() not in voice.get("name", "").lower():
            match = False
        if accent and voice.get("accent", "").lower() != accent.lower():
            match = False
        if gender and voice.get("gender", "").lower() != gender.lower():
            match = False
        if language:
            labels = voice.get("labels", {})
            if labels.get("language", "").lower() != language.lower():
                match = False
        if match:
            results.append(voice)

    return results[:max_results]


# Популярные голоса для русского языка
# Jessie — женский, русский, чистый
# Natasha — женский, русский, эмоциональный
# Dmitry — мужской, русский, глубокий
# Anton — мужской, русский, разговорный
```

### 3. Базовый синтез речи

**TTS из текста:**

```python
async def text_to_speech(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel (default)
    model_id: str = "eleven_multilingual_v2",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    style: float = 0.0,
    speed: float = 1.0,
    output_path: str | Path | None = None,
) -> bytes:
    """Синтезирует речь из текста.

    Параметры voice_settings:
    - stability (0.0-1.0): 0 = эмоционально, 1 = стабильно
    - similarity_boost (0.0-1.0): 0 = отклонения, 1 = точное совпадение
    - style (0.0-1.0): 0 = нейтрально, 1 = экспрессивно
    - speed (0.7-1.2): скорость речи
    """
    url = f"{ELEVENLABS_BASE_URL}/text-to-speech/{voice_id}"

    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style,
            "speed": speed,
        },
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=HEADERS) as resp:
            if resp.status != 200:
                error_body = await resp.text()
                raise RuntimeError(f"TTS failed ({resp.status}): {error_body}")
            audio_data = await resp.read()

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(audio_data)

    return audio_data
```

**SSML-синтез (с паузами и ударениями):**

```python
async def text_to_speech_ssml(
    ssml_text: str,
    voice_id: str,
    model_id: str = "eleven_multilingual_v2",
) -> bytes:
    """Синтезирует SSML-размеченный текст.

    Поддерживаемые SSML-теги ElevenLabs:
    <break time="500ms"/>   — пауза
    <emphasis level="strong"> — усиление
    <prosody rate="slow">   — скорость
    <say-as interpret-as="digits"> 123 </say-as>
    <lang xml:lang="en-US">  — смена языка
    """
    if not ssml_text.strip().startswith("<speak>"):
        ssml_text = f"<speak>{ssml_text}</speak>"

    url = f"{ELEVENLABS_BASE_URL}/text-to-speech/{voice_id}"

    payload = {
        "text": ssml_text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.7,
        },
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=HEADERS) as resp:
            if resp.status != 200:
                raise RuntimeError(f"SSML TTS failed: {resp.status}")
            return await resp.read()
```

### 4. Пакетная генерация

**Генерация аудиокниги из глав:**

```python
async def batch_generate(
    texts: list[str],
    voice_id: str,
    output_dir: str | Path = "./audio",
    model_id: str = "eleven_multilingual_v2",
    voice_settings: dict | None = None,
    concurrency: int = 3,
    progress_callback=None,
) -> list[Path]:
    """Генерирует аудиофайлы для списка текстов.

    concurrency: количество одновременных запросов (rate limit).
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(concurrency)
    settings = voice_settings or {
        "stability": 0.5,
        "similarity_boost": 0.75,
    }

    async def generate_one(index: int, text: str) -> Path:
        async with semaphore:
            audio = await text_to_speech(
                text=text,
                voice_id=voice_id,
                model_id=model_id,
                **settings,
            )
            filepath = output_dir / f"chunk_{index:04d}.mp3"
            filepath.write_bytes(audio)
            if progress_callback:
                progress_callback(index, len(texts))
            return filepath

    tasks = [generate_one(i, text) for i, text in enumerate(texts)]
    return await asyncio.gather(*tasks)
```

**Конкатенация аудиофайлов:**

```python
from pydub import AudioSegment


def concatenate_audio(
    file_paths: list[Path],
    output_path: str | Path,
    crossfade_ms: int = 0,
) -> Path:
    """Склеивает несколько MP3-файлов в один.

    crossfade_ms: перекрёстное затухание между файлами (мс).
    """
    combined = AudioSegment.empty()

    for filepath in file_paths:
        segment = AudioSegment.from_mp3(str(filepath))
        if crossfade_ms > 0 and len(combined) > 0:
            combined = combined.append(segment, crossfade=crossfade_ms)
        else:
            combined = combined + segment

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined.export(str(output_path), format="mp3", bitrate="192k")
    return output_path
```

### 5. Интеграция с Telegram voice notes

```python
import tempfile
import subprocess


async def tts_to_telegram_voice(
    text: str,
    chat_id: str | int,
    bot,
    voice_id: str = "EXAVITQu4vr0o4ZnvI1e",  # Natasha (русский)
    model_id: str = "eleven_multilingual_v2",
    stability: float = 0.4,
    similarity_boost: float = 0.8,
    speed: float = 1.0,
    bitrate: str = "32k",
) -> dict:
    """Генерирует TTS через ElevenLabs и отправляет как voice note.

    Конвейер: ElevenLabs API -> MP3 -> FFmpeg -> OGG (Opus) -> Telegram.
    """
    audio_data = await text_to_speech(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        stability=stability,
        similarity_boost=similarity_boost,
        speed=speed,
    )

    mp3_path = None
    ogg_path = None

    try:
        # временные файлы
        mp3_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        mp3_path = Path(mp3_file.name)
        mp3_file.write(audio_data)
        mp3_file.close()

        # конвертация в OGG Opus
        ogg_file = tempfile.NamedTemporaryFile(suffix=".ogg", delete=False)
        ogg_path = Path(ogg_file.name)
        ogg_file.close()

        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", str(mp3_path),
            "-c:a", "libopus",
            "-b:a", bitrate,
            "-ar", "24000",
            "-ac", "1",
            "-y",
            str(ogg_path),
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()

        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {proc.returncode}")

        # отправка
        with open(ogg_path, "rb") as f:
            voice = await bot.send_voice(
                chat_id=chat_id,
                voice=f,
                read_timeout=60,
                write_timeout=60,
            )
        return {"ok": True, "message_id": voice.message_id, "duration": voice.voice.duration}

    finally:
        for p in [mp3_path, ogg_path]:
            if p and p.exists():
                os.unlink(p)
```

### 6. Клонирование голоса

**Instant Voice Cloning:**

```python
async def clone_voice_instant(
    name: str,
    audio_file_path: str | Path,
    description: str = "",
    labels: dict | None = None,
) -> dict:
    """Мгновенное клонирование голоса из аудиофайла.

    Требования к образцу:
    - Формат: MP3, WAV, M4A, OGG
    - Длительность: 10-60 секунд (идеально 30-45с)
    - Качество: 16-48 kHz, mono
    - Содержание: чистый голос, без фонового шума и музыки
    """
    url = f"{ELEVENLABS_BASE_URL}/voices/add"

    data = aiohttp.FormData()
    data.add_field("name", name)
    if description:
        data.add_field("description", description)
    if labels:
        import json
        data.add_field("labels", json.dumps(labels))

    with open(audio_file_path, "rb") as f:
        data.add_field(
            "files",
            f.read(),
            filename=Path(audio_file_path).name,
            content_type="audio/mpeg",
        )

    headers = {"xi-api-key": ELEVENLABS_API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as resp:
            if resp.status != 200:
                error = await resp.text()
                raise RuntimeError(f"Clone failed: {error}")
            return await resp.json()
```

**Professional Voice Cloning:**

```python
async def request_professional_cloning(
    name: str,
    description: str,
    sample_texts: list[str],
    consent_file: str | Path,
) -> dict:
    """Запрос профессионального клонирования голоса (платная услуга).

    Процесс:
    1. ElevenLabs высылает текст для озвучки
    2. Вы записываете ~25-30 минут речи
    3. ElevenLabs обучает модель (2-5 дней)
    4. Голос появляется в вашей библиотеке
    """
    url = f"{ELEVENLABS_BASE_URL}/professional-voices/request"

    payload = {
        "name": name,
        "description": description,
        "sample_texts": sample_texts,
    }

    with open(consent_file, "rb") as f:
        consent_data = f.read()

    data = aiohttp.FormData()
    data.add_field("json", json.dumps(payload), content_type="application/json")

    import io
    data.add_field(
        "consent",
        consent_data,
        filename=Path(consent_file).name,
        content_type="application/pdf",
    )

    headers = {"xi-api-key": ELEVENLABS_API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Professional clone request failed: {resp.status}")
            return await resp.json()
```

### 7. Мультиязыковой синтез

```python
LANGUAGE_MAP = {
    "ru": "Русский", "en": "Английский", "de": "Немецкий",
    "fr": "Французский", "es": "Испанский", "it": "Итальянский",
    "pt": "Португальский", "pl": "Польский", "tr": "Турецкий",
    "ja": "Японский", "ko": "Корейский", "zh": "Китайский",
    "ar": "Арабский", "hi": "Хинди", "vi": "Вьетнамский",
}

# Рекомендуемые голоса по языкам
VOICE_RECOMMENDATIONS = {
    "ru": ["Natasha (EXAVITQu4vr0o4ZnvI1e)", "Dmitry (pNInz6obpgDQGcXma3g1)"],
    "en": ["Rachel (21m00Tcm4TlvDq8ikWAM)", "Adam (pNInz6obpgDQGcXma3g1)"],
    "de": ["Lena (g0gLPR4m2hS0V7N6WXuY)", "Felix (pMsXgVXc3g4HZ2bGqUoM)"],
    "fr": ["Bella (EXAVITQu4vr0o4ZnvI1e)", "Antoine (pMsXgVXc3g4HZ2bGqUoM)"],
    "es": ["Sofia (pMsXgVXc3g4HZ2bGqUoM)", "Jose (pNInz6obpgDQGcXma3g1)"],
}


async def multilingual_tts(
    text: str,
    language: str,
    voice_id: str | None = None,
    model_id: str = "eleven_multilingual_v2",
) -> bytes:
    """Синтезирует речь на указанном языке.

    Если voice_id не указан, выбирается рекомендуемый голос.
    """
    if voice_id is None:
        recs = VOICE_RECOMMENDATIONS.get(language, [])
        if not recs:
            raise ValueError(f"No recommended voice for language: {language}")
        voice_id = recs[0].split("(")[-1].rstrip(")")

    return await text_to_speech(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
    )


async def translate_and_speak(
    text: str,
    source_lang: str,
    target_lang: str,
    translation_func,
    voice_id: str | None = None,
) -> bytes:
    """Переводит текст и синтезирует речь на целевом языке.

    Использует переданную функцию перевода (может быть OpenAI, DeepL и т.д.).
    """
    translated = await translation_func(text, source_lang, target_lang)
    return await multilingual_tts(translated, target_lang, voice_id)
```

### 8. Обработка ошибок

| Код | Ошибка | Причина | Решение |
|---|---|---|---|
| 400 | Bad Request | Некорректный JSON или параметры | Проверить payload, длину текста (<5000 символов) |
| 401 | Unauthorized | Неверный API-ключ | Проверить ELEVENLABS_API_KEY |
| 402 | Insufficient Credits | Закончились токены | Пополнить счёт, снизить качество (turbo вместо v2) |
| 422 | Unprocessable | Текст содержит недопустимые символы | Очистить текст от управляющих символов |
| 429 | Rate Limited | Превышен лимит запросов | Retry с exponential backoff (1s, 2s, 4s, 8s) |
| 500+ | Server Error | Проблема на стороне ElevenLabs | Retry 3 раза, затем сообщить пользователю |

**Retry с exponential backoff:**

```python
import random


async def tts_with_retry(
    text: str,
    voice_id: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
    **kwargs,
) -> bytes:
    """TTS с автоматическим повторением при ошибках."""
    last_error = None

    for attempt in range(max_retries):
        try:
            return await text_to_speech(text, voice_id, **kwargs)
        except RuntimeError as e:
            last_error = e
            if "429" in str(e):
                delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                await asyncio.sleep(delay)
            elif "500" in str(e) or "502" in str(e) or "503" in str(e):
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
            else:
                raise

    raise RuntimeError(f"TTS failed after {max_retries} retries: {last_error}")
```

### 9. Оптимизация качества

**Рекомендации по тексту:**

```python
def preprocess_text(text: str, language: str = "ru") -> str:
    """Подготавливает текст для TTS: нормализация чисел, дат, аббревиатур."""
    import re

    # Замена многоточий на паузы
    text = re.sub(r"\.{3,}", ", ", text)

    # Удаление лишних пробелов
    text = re.sub(r"\s+", " ", text)

    # Обработка дат (15.05.2026 -> 15 мая 2026 года)
    text = re.sub(
        r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b",
        r"\1 \2 \3",  # упрощённо, по-хорошему через locale
        text,
    )

    # Удаление Markdown-разметки
    text = re.sub(r"[*_~`#]", "", text)

    # Удаление URL
    text = re.sub(r"https?://\S+", "ссылка", text)

    # Нормализация кавычек
    text = text.replace('"', '«').replace('"', '»')

    return text.strip()
```

**Voice settings по типу контента:**

| Контент | stability | similarity_boost | style | speed |
|---|---|---|---|---|
| Аудиокнига (нарратив) | 0.7 | 0.5 | 0.3 | 0.9 |
| Аудиокнига (диалоги) | 0.3 | 0.7 | 0.6 | 1.0 |
| Подкаст | 0.4 | 0.7 | 0.4 | 1.1 |
| Озвучка видео | 0.5 | 0.6 | 0.5 | 1.0 |
| Голосовой помощник | 0.8 | 0.8 | 0.1 | 1.0 |
| Реклама | 0.3 | 0.7 | 0.8 | 1.15 |

### 10. История и стоимость

**Получение истории генераций:**

```python
async def get_generation_history(limit: int = 10) -> list[dict]:
    """Получает историю сгенерированных аудио."""
    url = f"{ELEVENLABS_BASE_URL}/history?page_size={limit}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status != 200:
                raise RuntimeError(f"History request failed: {resp.status}")
            data = await resp.json()
            return data.get("history", [])
```

**Стоимость (приблизительно, май 2026):**

| Модель | Токенов в час | Цена за 1М символов |
|---|---|---|
| eleven_multilingual_v2 | ~8000 | $5.00 |
| eleven_monolingual_v1 | ~9000 | $5.00 |
| eleven_turbo_v2 | ~12000 | $1.50 |
| eleven_flash_v2 | ~15000 | $1.00 |
| eleven_flash_v2_5 | ~14000 | $1.50 |
| Voice cloning (instant) | — | $1.00 за голос |
| Voice cloning (professional) | — | $500+ за голос |

1 символ = 1 буква, пробел или знак препинания. Пробелы не тарифицируются.

### 11. Полный пример интеграции

```python
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes


async def tts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /tts <текст> для Telegram-бота."""
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text(
            "Использование: /tts <текст>\n"
            "Опции: /tts --voice <id> --lang <lang> <текст>"
        )
        return

    # парсинг опций
    voice_id = "EXAVITQu4vr0o4ZnvI1e"  # Natasha
    model_id = "eleven_multilingual_v2"

    if text.startswith("--voice "):
        parts = text.split(" ", 2)
        if len(parts) >= 2:
            voice_id = parts[1]
            text = parts[2] if len(parts) > 2 else ""

    await update.message.reply_text("Генерирую голосовое сообщение...")

    try:
        audio = await tts_with_retry(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            stability=0.4,
            similarity_boost=0.8,
        )
        await update.message.reply_voice(voice=audio)
    except Exception as e:
        await update.message.reply_text(f"Ошибка генерации: {e}")


# Регистрация в боте
# application.add_handler(CommandHandler("tts", tts_command))
```

## Референсы

- ElevenLabs API Docs: `https://docs.elevenlabs.io/`
- Состояние на май 2026: v2 API (основной)
- Voice IDs: UUID-формат (пример: `21m00Tcm4TlvDq8ikWAM`)
- Максимальная длина текста: 5000 символов на запрос
- Поддерживаемые форматы: MP3 (по умолчанию), PCM, WAV, OGG
- Частота дискретизации: 22050 Hz (по умолчанию), 44100 Hz
- Rate limit: зависит от тарифа (Starter ~1000 req/day, Pro ~5000 req/day)
- SSML: ограниченная поддержка (break, emphasis, prosody, lang, say-as)
- Аудиообразцы для клонирования: 10-60 сек, 16-48 kHz, без шума
