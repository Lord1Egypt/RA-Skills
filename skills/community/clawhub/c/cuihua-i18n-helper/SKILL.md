---
name: cuihua-i18n-helper
description: |
  🌍 AI-powered internationalization (i18n) assistant for modern web applications.
  Automatically extract translatable strings, generate locale files, batch translate to 100+ languages,
  and maintain translation quality across your entire codebase.
  
  Built for developers who ship global products.

metadata:
  openclaw:
    requires:
      bins:
        - node
      env: []
    primaryEnv: null
  
  version: "1.0.0"
  author: "翠花 (Cuihua) - ClawHub Pioneer"
  license: "MIT"
  tags:
    - i18n
    - internationalization
    - translation
    - localization
    - react
    - vue
    - nextjs
    - multilingual
  
  capabilities:
    - Automatic string extraction from code
    - Smart translation key generation
    - Batch translation (DeepL, Google Translate, OpenAI)
    - Translation quality checks
    - Missing translation detection
    - Unused translation cleanup
    - Framework support (React, Vue, Angular, Next.js, Nuxt.js)
    - CI/CD integration
---

# cuihua-i18n-helper - AI i18n Assistant 🌍

> **Ship global products faster with AI-powered internationalization.**

An intelligent i18n assistant that automates the tedious parts of internationalization:
- 🔍 **Auto-extract** translatable strings from your code
- 🤖 **AI-translate** to 100+ languages in seconds
- ✅ **Quality checks** for consistency and completeness
- 📊 **Reports** on translation coverage and health
- 🔄 **Sync** translations across multiple frameworks

## 🎯 Why cuihua-i18n-helper?

Traditional i18n workflow is painful:
1. ❌ Manually find all hardcoded strings
2. ❌ Manually create translation keys
3. ❌ Manually copy to each locale file
4. ❌ Manually send to translators
5. ❌ Manually track what's missing
6. ❌ Manually clean up unused translations

**cuihua-i18n-helper automates ALL of this.**

---

## 🚀 Quick Start

### Extract translatable strings

Tell your OpenClaw agent:
> "Extract all translatable strings from src/"

The agent will:
- Find all hardcoded UI text
- Generate semantic translation keys
- Create locale files for your languages
- Show translation coverage report

### Translate to multiple languages

> "Translate to Chinese, Japanese, and Spanish"

The agent will:
- Batch translate all strings
- Preserve formatting and placeholders
- Check translation quality
- Report any issues

### Check translation health

> "Check for missing translations"

The agent will:
- Find missing translations
- Find unused translation keys
- Check for consistency issues
- Generate actionable report

---

## 🎨 Features

### 1. Smart String Extraction 🔍

Automatically detects translatable content:

```jsx
// Before
<button>Submit</button>
<p>Hello, {username}!</p>
<input placeholder="Enter email" />

// After extraction
<button>{t('button.submit')}</button>
<p>{t('greeting.hello', { username })}</p>
<input placeholder={t('form.email_placeholder')} />
```

**Supports**:
- JSX/TSX (React)
- Vue templates
- Angular templates
- Plain JavaScript strings
- Template literals with variables

### 2. Intelligent Key Generation 🧠

Creates semantic, readable translation keys:

```json
{
  "button": {
    "submit": "Submit",
    "cancel": "Cancel",
    "save": "Save"
  },
  "greeting": {
    "hello": "Hello, {{username}}!",
    "welcome": "Welcome back"
  },
  "form": {
    "email_placeholder": "Enter email",
    "password_placeholder": "Enter password"
  }
}
```

**Smart features**:
- Context-aware naming
- Namespace organization
- Collision prevention
- Consistent naming conventions

### 3. Batch Translation 🌐

Translate to 100+ languages instantly:

**Supported providers**:
- ✅ DeepL (best quality)
- ✅ Google Translate (fast, free tier)
- ✅ OpenAI GPT (context-aware)
- ✅ Azure Translator
- ✅ LibreTranslate (self-hosted)

**Smart translation**:
- Preserves placeholders: `{{count}}`, `{username}`
- Handles HTML tags: `<strong>Bold</strong>`
- Keeps special characters: `© ® ™`
- Context-aware translations

**Example output**:

```json
// en.json
{
  "user": {
    "greeting": "Hello, {{name}}!",
    "items_count": "You have {{count}} items"
  }
}

// zh.json (Chinese)
{
  "user": {
    "greeting": "你好，{{name}}！",
    "items_count": "你有 {{count}} 个物品"
  }
}

// ja.json (Japanese)
{
  "user": {
    "greeting": "こんにちは、{{name}}さん！",
    "items_count": "{{count}}個のアイテムがあります"
  }
}
```

### 4. Translation Quality Checks ✅

Automated quality assurance:

**Checks**:
- ✅ Missing translations
- ✅ Placeholder mismatches
- ✅ Inconsistent terminology
- ✅ Excessive string length
- ✅ Untranslated strings (still in source language)
- ✅ HTML tag mismatches
- ✅ Special character issues

**Example report**:

```
🔍 Translation Quality Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Coverage: 95% (190/200 strings)

⚠️  Issues Found: 5

1. Missing translations (zh.json):
   - user.profile_updated
   - error.network_timeout

2. Placeholder mismatch (ja.json):
   - user.items_count
     Expected: {{count}}
     Found: {count}

3. Excessive length (de.json):
   - button.submit_and_continue
     English: 21 chars
     German: 45 chars (214% longer)

💡 Run with --fix to auto-fix common issues
```

### 5. Framework Integration 🔧

Works seamlessly with popular frameworks:

**React / Next.js**:
```jsx
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();
  return <h1>{t('welcome.title')}</h1>;
}
```

**Vue / Nuxt.js**:
```vue
<template>
  <h1>{{ $t('welcome.title') }}</h1>
</template>
```

**Angular**:
```html
<h1>{{ 'welcome.title' | translate }}</h1>
```

**Vanilla JS**:
```javascript
import i18n from './i18n';
document.getElementById('title').textContent = i18n.t('welcome.title');
```

### 6. CI/CD Integration 🔄

Automate translation checks in your pipeline:

```yaml
# .github/workflows/i18n.yml
name: i18n Check

on: [pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check i18n
        run: |
          openclaw agent run "Check for missing translations"
          openclaw agent run "Verify translation quality"
```

**Pre-commit hook**:
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Checking i18n..."
openclaw agent run "Check for untranslated strings in staged files"

if [ $? -ne 0 ]; then
  echo "❌ Found untranslated strings. Please add translations."
  exit 1
fi
```

---

## 📋 Usage Examples

### Example 1: New Project Setup

**User**: "Set up i18n for my React project with English and Chinese"

**Agent**:
```
✅ i18n setup complete:

📦 Installed dependencies:
  - react-i18next
  - i18next

📁 Created structure:
  src/
    i18n/
      index.js (config)
      locales/
        en.json
        zh.json

⚙️  Configured:
  - Default language: en
  - Fallback language: en
  - Supported languages: en, zh

💡 Next steps:
  1. Import i18n in your root component
  2. Wrap app with I18nextProvider
  3. Use {t('key')} in components
```

### Example 2: Extract from Existing Code

**User**: "Extract all translatable strings from src/components/"

**Agent**:
```
🔍 Scanning src/components/...

✅ Found 42 translatable strings:
  - Button labels: 12
  - Form placeholders: 8
  - Error messages: 7
  - Page titles: 6
  - Tooltips: 5
  - Other: 4

📝 Generated locale files:
  locales/en.json (42 keys)
  locales/zh.json (42 keys, auto-translated)

🔄 Updated components:
  - src/components/Button.jsx (3 strings)
  - src/components/Form.jsx (8 strings)
  - src/components/Header.jsx (2 strings)
  ...

📊 Coverage: 100%

💡 Review translations in locales/ folder
```

### Example 3: Add New Language

**User**: "Add German and French translations"

**Agent**:
```
🌍 Adding languages: de (German), fr (French)

🤖 Translating 42 strings...
  [████████████████████] 100%

✅ Created locale files:
  locales/de.json (42 keys)
  locales/fr.json (42 keys)

⚠️  Review recommended for:
  - Technical terms (3 strings)
  - Brand names (1 string)
  - Colloquial expressions (2 strings)

📊 Translation provider: DeepL
📊 Cost: $0.02 (42 strings × 2 languages)

💡 Preview: http://localhost:3000?lng=de
```

### Example 4: Find Missing Translations

**User**: "Check for missing translations"

**Agent**:
```
🔍 Checking translation completeness...

📊 Coverage by language:
  ✅ en: 100% (50/50)
  ✅ zh: 100% (50/50)
  ⚠️  ja: 94% (47/50)
  ⚠️  de: 88% (44/50)
  ❌ fr: 76% (38/50)

❌ Missing in ja.json (3):
  - user.profile_updated
  - error.network_timeout
  - settings.privacy_policy

❌ Missing in de.json (6):
  - user.profile_updated
  - user.account_deleted
  - error.network_timeout
  - error.server_error
  - settings.privacy_policy
  - settings.terms_of_service

❌ Missing in fr.json (12):
  [... list truncated ...]

💡 Fix: openclaw agent run "Translate missing strings to all languages"
```

### Example 5: Clean Up Unused Translations

**User**: "Remove unused translation keys"

**Agent**:
```
🔍 Scanning codebase for used translation keys...

📊 Analysis:
  Total keys: 50
  Used keys: 45
  Unused keys: 5

🗑️  Unused keys found:
  - old.deprecated_feature (last used: 6 months ago)
  - temp.debug_message (never used)
  - test.sample_text (test artifact)
  - button.old_submit (replaced by button.submit)
  - error.obsolete_error (feature removed)

❓ Remove these keys? (y/n)
```

**User**: "Yes"

```
✅ Removed 5 unused keys from all locale files

📁 Updated files:
  - locales/en.json (-5 keys)
  - locales/zh.json (-5 keys)
  - locales/ja.json (-5 keys)
  - locales/de.json (-5 keys)
  - locales/fr.json (-5 keys)

💾 Backup created: locales/.backup-2026-03-24/
```

### Example 6: Translation Review Workflow

**User**: "Mark translations needing review"

**Agent**:
```
🔍 Analyzing translations for review...

⚠️  Flagged for review (8 strings):

1. user.welcome_premium
   Translation seems too literal
   Suggestion: Use more natural phrasing

2. error.payment_failed (zh)
   Contains English words: "payment"
   Suggestion: Translate to "支付"

3. button.purchase_now (de)
   Too long for button (28 characters)
   Suggestion: Shorten to "Jetzt kaufen"

📝 Created review.md with details

💡 Next: Share review.md with translators
```

---

## ⚙️ Configuration

Create `.i18nrc.json` in your project root:

```json
{
  "sourceLanguage": "en",
  "targetLanguages": ["zh", "ja", "de", "fr", "es"],
  "localesPath": "./src/locales",
  "extractFrom": ["./src"],
  "ignore": ["**/*.test.js", "**/*.spec.js"],
  "translationProvider": "deepl",
  "keyStyle": "nested",
  "keyCase": "snake_case",
  "placeholderPattern": "{{%s}}",
  "qualityChecks": {
    "checkMissingTranslations": true,
    "checkPlaceholders": true,
    "checkLength": true,
    "maxLengthRatio": 2.0
  }
}
```

---

## 🌐 Supported Languages

100+ languages including:

**Popular**:
- 🇨🇳 Chinese (Simplified, Traditional)
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇩🇪 German
- 🇫🇷 French
- 🇪🇸 Spanish
- 🇮🇹 Italian
- 🇷🇺 Russian
- 🇵🇹 Portuguese
- 🇦🇪 Arabic

**And many more**: Dutch, Swedish, Danish, Polish, Turkish, Thai, Vietnamese, Indonesian, Hindi, Hebrew, Greek, Czech, Romanian, Hungarian, Finnish, Norwegian, Ukrainian, and more!

---

## 💰 Pricing

### Free Tier
- ✅ Extract up to 100 strings
- ✅ 2 target languages
- ✅ Basic quality checks
- ✅ Google Translate only

### Pro ($12/month)
- ✅ Unlimited extraction
- ✅ Unlimited languages
- ✅ All translation providers
- ✅ Advanced quality checks
- ✅ CI/CD integration
- ✅ Priority support

### Enterprise ($99/month)
- ✅ Everything in Pro
- ✅ Team collaboration
- ✅ Translation memory
- ✅ Custom translation engines
- ✅ On-premise deployment
- ✅ SLA support

---

## 🔒 Privacy & Security

- ✅ **Local processing** - Extraction happens locally
- ✅ **Secure API calls** - Encrypted communication with translation providers
- ✅ **No data retention** - Translations not stored on our servers
- ✅ **Self-hosted option** - Use LibreTranslate for complete privacy

---

## 🤝 Integration

### Translation Providers

**DeepL** (Recommended):
```bash
export DEEPL_API_KEY=your_api_key
```

**Google Translate**:
```bash
export GOOGLE_TRANSLATE_API_KEY=your_api_key
```

**OpenAI**:
```bash
export OPENAI_API_KEY=your_api_key
```

### i18n Libraries

**react-i18next**:
```bash
npm install react-i18next i18next
```

**vue-i18n**:
```bash
npm install vue-i18n
```

**angular-translate**:
```bash
npm install @ngx-translate/core
```

---

## 📚 Resources

- 📖 [Full Documentation](./docs/README.md)
- 🎓 [Video Tutorials](https://youtube.com/cuihua-i18n)
- 💬 [Discord Community](https://discord.gg/clawd)
- 🐛 [Report Issues](https://github.com/cuihua/i18n-helper/issues)

---

## 📜 License

MIT License - see [LICENSE](./LICENSE) for details.

---

## 🙏 Acknowledgments

Built with 🌸 by 翠花 (Cuihua) for the OpenClaw community.

Special thanks to:
- OpenClaw team for the amazing framework
- i18next, vue-i18n, and other i18n library maintainers
- Translation API providers
- Early adopters and contributors

---

**Made with 🌸 | Cuihua Series | ClawHub Pioneer**

_Ship global products faster with AI-powered i18n._
