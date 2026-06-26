# audio-analyze-skill-for-openclaw

音声/動画コンテンツを高精度で文字起こしおよび分析します。[Powered by Evolink.ai](https://evolink.ai/?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

🌐 English | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Türkçe](README.tr.md) | [Русский](README.ru.md)

## 概要

Gemini 3.1 Proを使用して、音声/動画ファイルを自動的に文字起こし・分析します。[無料のAPIキーを取得する →](https://evolink.ai/signup?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

## インストール

### ClawHub 経由 (推奨)

```bash
openclaw skills add https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
```

### 手動インストール

```bash
git clone https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
cd audio-analyze-skill-for-openclaw
pip install -r requirements.txt
```

## 設定

| 変数 | 説明 | デフォルト値 |
| :--- | :--- | :--- |
| `EVOLINK_API_KEY` | EvoLink API キー | (必須) |
| `EVOLINK_MODEL` | 文字起こしモデル | gemini-3.1-pro-preview-customtools |

*API設定の詳細やサポートされているモデルについては、[EvoLink API ドキュメント](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)をご参照ください。*

## 使用方法

### 基本的な使用方法

```bash
export EVOLINK_API_KEY="your-key-here"
./scripts/transcribe.sh audio.mp3
```

### 高度な使用方法

```bash
./scripts/transcribe.sh audio.mp3 --diarize --lang ja
```

### 出力例

* **要約 (TL;DR)**: この音声はテスト用のサンプルトラックです。
* **重要なポイント (Key Takeaways)**: 高忠実度のサウンド、クリアな周波数特性。
* **アクションアイテム**: 最終テストのために本番環境にアップロードする。

## 利用可能なモデル

- **Gemini シリーズ** (OpenAI API — `/v1/chat/completions`)

## ファイル構成

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

## トラブルシューティング

- **Argument list too long (引数リストが長すぎます)**: 大容量の音声データには一時ファイルを使用してください。
- **API キーエラー**: `EVOLINK_API_KEY` が正しくエクスポート（環境変数に設定）されているか確認してください。

## リンク

- [ClawHub](https://clawhub.ai/EvoLinkAI/audio-analyze)
- [API リファレンス](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)
- [コミュニティ](https://discord.com/invite/5mGHfA24kn)
- [サポート](mailto:support@evolink.ai)

## ライセンス

MIT