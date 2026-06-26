# audio-analyze-skill-for-openclaw

Transcrivez et analysez du contenu audio/vidéo avec une grande précision. [Propulsé par Evolink.ai](https://evolink.ai/?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

🌐 [Anglais](README.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [한국어](README.ko.md) | [Español](README.es.md) | Français | [Deutsch](README.de.md) | [Türkçe](README.tr.md) | [Русский](README.ru.md)

## Qu'est-ce que c'est ?

Transcrivez et analysez vos fichiers audio/vidéo automatiquement en utilisant Gemini 3.1 Pro. [Obtenez votre clé API gratuite →](https://evolink.ai/signup?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

## Installation

### Via ClawHub (Recommandé)

```bash
openclaw skills add https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
```

### Installation manuelle

```bash
git clone https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
cd audio-analyze-skill-for-openclaw
pip install -r requirements.txt
```

## Configuration

| Variable | Description | Par défaut |
| :--- | :--- | :--- |
| `EVOLINK_API_KEY` | Clé API EvoLink | (Requis) |
| `EVOLINK_MODEL` | Modèle de transcription | gemini-3.1-pro-preview-customtools |

*Pour une configuration détaillée de l'API et la prise en charge des modèles, consultez la [Documentation de l'API EvoLink](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze).*

## Utilisation

### Utilisation de base

```bash
export EVOLINK_API_KEY="votre-cle-ici"
./scripts/transcribe.sh audio.mp3
```

### Utilisation avancée

```bash
./scripts/transcribe.sh audio.mp3 --diarize --lang ja
```

### Exemple de sortie

* **TL;DR** : L'audio est une piste d'essai pour les tests.
* **Points clés** : Son haute fidélité, réponse en fréquence claire.
* **Actions à entreprendre** : Mettre en ligne en production pour les tests finaux.

## Modèles disponibles

- **Série Gemini** (API OpenAI — `/v1/chat/completions`)

## Structure des fichiers

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

## Dépannage

- **Argument list too long** : Utilisez des fichiers temporaires pour les données audio volumineuses.
- **Erreur de clé API** : Assurez-vous que la variable `EVOLINK_API_KEY` est exportée.

## Liens

- [ClawHub](https://clawhub.ai/EvoLinkAI/audio-analyze)
- [Référence de l'API](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)
- [Communauté](https://discord.com/invite/5mGHfA24kn)
- [Assistance](mailto:support@evolink.ai)

## Licence

MIT