# audio-analyze-skill-for-openclaw

Ses/video içeriklerini yüksek doğrulukla metne dökün ve analiz edin. [Evolink.ai tarafından desteklenmektedir](https://evolink.ai/?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

🌐 English | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Türkçe](README.tr.md) | [Русский](README.ru.md)

## Bu Nedir?

Gemini 3.1 Pro kullanarak ses/video dosyalarınızı otomatik olarak metne dökün ve analiz edin. [Ücretsiz API anahtarınızı alın →](https://evolink.ai/signup?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

## Kurulum

### ClawHub Aracılığıyla (Önerilen)

```bash
openclaw skills add https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
```

### Manuel Kurulum

```bash
git clone https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
cd audio-analyze-skill-for-openclaw
pip install -r requirements.txt
```

## Yapılandırma

| Değişken | Açıklama | Varsayılan |
| :--- | :--- | :--- |
| `EVOLINK_API_KEY` | EvoLink API Anahtarı | (Gerekli) |
| `EVOLINK_MODEL` | Transkripsiyon Modeli | gemini-3.1-pro-preview-customtools |

*Ayrıntılı API yapılandırması ve model desteği için [EvoLink API Belgeleri](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)'ne göz atın.*

## Kullanım

### Temel Kullanım

```bash
export EVOLINK_API_KEY="your-key-here"
./scripts/transcribe.sh audio.mp3
```

### Gelişmiş Kullanım

```bash
./scripts/transcribe.sh audio.mp3 --diarize --lang ja
```

### Örnek Çıktı

* **Özet (TL;DR)**: Bu ses kaydı test amaçlı bir örnek parçadır.
* **Önemli Çıkarımlar**: Yüksek kaliteli ses, net frekans tepkisi.
* **Eylem Maddeleri**: Son testler için canlı ortama (production) yükleyin.

## Kullanılabilir Modeller

- **Gemini Serisi** (OpenAI API — `/v1/chat/completions`)

## Dosya Yapısı

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

## Sorun Giderme

- **Argument list too long (Argüman listesi çok uzun)**: Büyük ses verileri için geçici dosyalar kullanın.
- **API Key Error (API Anahtarı Hatası)**: `EVOLINK_API_KEY` değişkeninin dışa aktarıldığından (export edildiğinden) emin olun.

## Bağlantılar

- [ClawHub](https://clawhub.ai/EvoLinkAI/audio-analyze)
- [API Referansı](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)
- [Topluluk](https://discord.com/invite/5mGHfA24kn)
- [Destek](mailto:support@evolink.ai)

## Lisans

MIT