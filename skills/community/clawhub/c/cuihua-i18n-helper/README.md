# cuihua-i18n-helper

🌍 **AI-powered internationalization assistant for modern web applications**

Automate the tedious parts of i18n: extract strings, generate keys, translate to 100+ languages, and maintain quality.

## Quick Start

### Extract translatable strings

```bash
node i18n-helper.js extract ./src
```

Output:
- `locales/en.json` - Source language
- `locales/zh.json` - Chinese (auto-created)
- `locales/ja.json` - Japanese (auto-created)

### Check translation status

```bash
node i18n-helper.js check
```

## Features

- 🔍 **Auto-extract** from JSX, Vue, Angular, HTML
- 🤖 **Smart key generation** (semantic, namespaced)
- 🌐 **100+ languages** support
- ✅ **Quality checks** (missing, unused, inconsistent)
- 📊 **Coverage reports**
- 🔄 **Framework agnostic**

## Supported Frameworks

- ✅ React / Next.js (react-i18next)
- ✅ Vue / Nuxt.js (vue-i18n)
- ✅ Angular (@ngx-translate)
- ✅ Vanilla JavaScript

## Installation

Via ClawHub:
```bash
clawhub install cuihua-i18n-helper
```

Manual:
```bash
git clone https://github.com/cuihua/i18n-helper
cd cuihua-i18n-helper
```

## Usage with OpenClaw

Tell your agent:
> "Extract translatable strings from src/"

> "Check for missing translations"

> "Translate to Chinese and Japanese"

## Configuration

Create `.i18nrc.json`:

```json
{
  "sourceLanguage": "en",
  "targetLanguages": ["zh", "ja", "de", "fr"],
  "localesPath": "./locales",
  "extractFrom": ["./src"]
}
```

## Example Output

```json
{
  "common": {
    "welcome": "Welcome",
    "hello_user": "Hello, {{name}}!"
  },
  "button": {
    "submit": "Submit",
    "cancel": "Cancel"
  },
  "form": {
    "email_placeholder": "Enter email",
    "password_placeholder": "Enter password"
  }
}
```

## Translation Providers

- DeepL (recommended)
- Google Translate
- OpenAI GPT
- Azure Translator
- LibreTranslate (self-hosted)

## License

MIT

## Author

Made with 🌸 by 翠花 (Cuihua)

---

**Part of the Cuihua Series** | ClawHub Pioneer
