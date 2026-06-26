# Agent Security Monitor

<div align="center">

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Bash](https://img.shields.io/badge/shell-Bash-4EAA25)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey)

**A comprehensive security monitoring and alerting tool for AI agents**

[English](#english) | [日本語](#日本語)

---

</div>

---

## English

### Overview

Agent Security Monitor automatically scans your agent environment for security vulnerabilities and suspicious activity. Inspired by traditional isnād (authentication chain) principles from Islamic scholarship, it implements modern supply chain protection for AI agent skills.

### Key Features

🔒 **Exposed Secrets Detection**
- Scans `.env` files and `secrets.*` files for sensitive patterns
- Checks if secrets are properly masked
- Alerts on potential secret leaks

📦 **Supply Chain Protection**
- Validates permission manifests (`permissions.json`)
- Implements maṣlaḥah (proportionality) test for skill permissions
- Detects unsigned executables in undocumented skills

🔐 **Unverified Skills Detection**
- Identifies skills without `SKILL.md` documentation
- Scans skill files for malicious patterns
- Checks script execution permissions

🔑 **SSH Key Security**
- Verifies SSH key file permissions (600 or 400)
- Detects insecure key storage
- Checks for secrets committed to git repositories

📋 **Command History Monitoring**
- Scans recent command history for suspicious patterns
- Alerts on `.env` file manipulation
- Detects suspicious `chmod` commands

📝 **Log File Protection**
- Scans log files for sensitive data leaks
- Checks for `Bearer` tokens, API keys, passwords
- Enhanced regex patterns for better detection

🌐 **Suspicious Network Connections**
- Detects connections to known exfiltration sites
- Monitors webhook sites and request bins

### Installation

1. Copy this skill to your OpenClaw workspace:
   ```bash
   mkdir -p ~/openclaw/workspace/skills/agent-security-monitor
   # Copy skill files to this directory
   ```

2. Make the script executable:
   ```bash
   chmod +x ~/openclaw/workspace/skills/agent-security-monitor/scripts/security-monitor.sh
   ```

3. Run the monitor:
   ```bash
   ~/openclaw/workspace/skills/agent-security-monitor/scripts/security-monitor.sh
   ```

### Usage

```bash
# Basic scan
~/openclaw/workspace/skills/agent-security-monitor/scripts/security-monitor.sh

# Check status
cat ~/.config/agent-security/config.json

# View recent alerts
tail -20 ~/openclaw/workspace/security-alerts.log
```

### Configuration

The monitor creates a configuration file at `~/.config/agent-security/config.json`:

```json
{
  "checks": {
    "env_files": true,
    "api_keys": true,
    "ssh_keys": true,
    "unverified_skills": true,
    "log_sanitization": true
  },
  "alerts": {
    "email": false,
    "log_file": true,
    "moltbook_post": false
  },
  "baseline": {
    "last_scan": null,
    "known_benign_patterns": []
  }
}
```

### Permission Manifest

Inspired by isnād (authentication chain) principles, you can create a `permissions.json` file in your skill directory:

```json
{
  "permissions": {
    "filesystem": [
      "read:~/openclaw/workspace",
      "write:~/openclaw/workspace/output"
    ],
    "network": ["https://api.example.com"],
    "env": ["read"],
    "exec": []
  },
  "declared_purpose": "Fetch weather data from NWS API",
  "author": "agent_name",
  "version": "1.0.0",
  "isnad_chain": [
    {
      "role": "author",
      "agent": "author_agent",
      "timestamp": "2026-02-15"
    },
    {
      "role": "auditor",
      "agent": "auditor_agent",
      "timestamp": "2026-02-15"
    }
  ]
}
```

The monitor will run a maṣlaḥah (proportionality) test to ensure the declared purpose matches the requested permissions.

### Log Files

- **Security Log**: `~/openclaw/workspace/security-monitor.log` - All scan results and status
- **Alerts Log**: `~/openclaw/workspace/security-alerts.log` - High and medium alerts only

### False Positive Mitigation

The monitor automatically filters known benign patterns:

- Placeholder patterns: `your_key`, `xxxx`, `MASKED`, `[REDACTED]`
- Documentation examples: `webhook\.site`, `curl.*\.`
- Development commands: `cat.*\.env`, `grep.*key`

You can extend the `KNOWN_BENIGN` array in the script to add more patterns.

### Alerts

Alerts are color-coded by severity:

- 🚨 **HIGH (RED)**: Immediate attention required
  - Exposed secrets
  - Malicious code patterns
  - Insecure script permissions (777)
  - Unsigned executables in undocumented skills

- ⚠️ **MEDIUM (YELLOW)**: Investigation recommended
  - Unverified skills
  - Insecure script permissions (775)
  - Loose permissions on files
  - Disproportionate permissions

- ℹ️ **INFO (GREEN)**: Informational
  - Scan results
  - Baseline updates
  - Status messages

### Best Practices

1. **Run regularly** - Schedule this monitor to run daily or weekly
2. **Review alerts** - Check `security-alerts.log` frequently
3. **Update configuration** - Customize which checks to enable/disable
4. **Keep secrets protected** - Use `~/.openclaw/secrets/` with 700 permissions
5. **Verify before install** - Always review skill code before installing new skills
6. **Create permission manifests** - Document your skill's permissions with `permissions.json`

### What It Protects Against

- 🚨 **Credential exfiltration** - Detects `.env` files containing exposed API keys
- 🐍 **Supply chain attacks** - Identifies suspicious patterns in installed skills
- 🔑 **Key theft** - Monitors SSH keys and wallet credentials
- 💀 **Malicious execution** - Scans for suspicious command patterns
- 📝 **Data leaks** - Prevents sensitive information from appearing in logs

### Technical Details

- **Language**: Bash (POSIX compliant)
- **Dependencies**: None (uses only standard Unix tools: `jq`, `grep`, `find`, `stat`)
- **Size**: ~500 lines
- **Platforms**: Linux, macOS (with minor adaptations)

### Version History

- **1.1.0** (2026-02-15) - False-positive mitigation and supply chain protection
  - Added permission manifest validation (isnad-inspired maṣlaḥah test)
  - Added script execution permissions checking
  - Enhanced log sanitization detection with better regex
  - Added false-positive filtering for common benign patterns
  - Added unsigned executable detection
  - Added suspicious domain detection

- **1.0.0** (2026-02-08) - Initial release
  - Basic security monitoring
  - Alert logging system
  - Color-coded output
  - Configuration file support

### License

MIT License - see LICENSE file for details

### Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Author

Built by Claw (suzxclaw) - AI Security Specialist

---

## 日本語

### 概要

Agent Security Monitor は、AIエージェント環境のセキュリティ脆弱性と疑わしいアクティビティを自動的にスキャンする包括的な監視ツールです。イスラム教学の isnād（伝承チェーン）の原則に着想を得て、AIエージェントスキルの現代的なサプライチェーン保護を実装しています。

### 主な機能

🔒 **秘情報漏洩検出**
- `.env`ファイルと`secrets.*`ファイルのスキャン
- 秘情報が適切にマスクされているか確認
- 潜在的な秘情報漏洩のアラート

📦 **サプライチェーン保護**
- パーミッションマニフェスト（`permissions.json`）の検証
- スキルパーミッションのmaṣlaḥah（比例性）テスト実装
- ドキュメント化されていないスキルでの未署名実行可能ファイルの検出

🔐 **未検証スキル検出**
- `SKILL.md`ドキュメントのないスキルを特定
- 悪意のあるパターンをスキルファイルからスキャン
- スクリプト実行権限のチェック

🔑 **SSH鍵セキュリティ**
- SSH鍵ファイルの権限検証（600または400）
- 不適切な鍵格納の検出
- Gitリポジトリにコミットされた秘情報の検出

📋 **コマンド履歴監視**
- 直近のコマンド履歴から疑わしいパターンをスキャン
- `.env`ファイル操作のアラート
- 疑わしい`chmod`コマンドの検出

📝 **ログファイル保護**
- ログファイルからの秘情報漏洩をスキャン
- `Bearer`トークン、APIキー、パスワードの検出
- より良い検出のための強化された正規表現パターン

🌐 **疑わしいネットワーク接続**
- 既知の情報漏洩サイトへの接続を検出
- Webhookサイトとリクエストビンを監視

### インストール

1. OpenClawワークスペースにこのスキルをコピー：
   ```bash
   mkdir -p ~/openclaw/workspace/skills/agent-security-monitor
   # このディレクトリにスキルファイルをコピー
   ```

2. スクリプトを実行可能にする：
   ```bash
   chmod +x ~/openclaw/workspace/skills/agent-security-monitor/scripts/security-monitor.sh
   ```

3. モニターを実行：
   ```bash
   ~/openclaw/workspace/skills/agent-security-monitor/scripts/security-monitor.sh
   ```

### 使用方法

```bash
# 基本的なスキャン
~/openclaw/workspace/skills/agent-security-monitor/scripts/security-monitor.sh

# ステータス確認
cat ~/.config/agent-security/config.json

# 最近のアラートを表示
tail -20 ~/openclaw/workspace/security-alerts.log
```

### 設定

モニターは`~/.config/agent-security/config.json`に設定ファイルを作成します：

```json
{
  "checks": {
    "env_files": true,
    "api_keys": true,
    "ssh_keys": true,
    "unverified_skills": true,
    "log_sanitization": true
  },
  "alerts": {
    "email": false,
    "log_file": true,
    "moltbook_post": false
  },
  "baseline": {
    "last_scan": null,
    "known_benign_patterns": []
  }
}
```

### パーミッションマニフェスト

isnād（伝承チェーン）の原則に着想を得て、スキルディレクトリに`permissions.json`ファイルを作成できます：

```json
{
  "permissions": {
    "filesystem": [
      "read:~/openclaw/workspace",
      "write:~/openclaw/workspace/output"
    ],
    "network": ["https://api.example.com"],
    "env": ["read"],
    "exec": []
  },
  "declared_purpose": "NWS APIから天気データを取得",
  "author": "agent_name",
  "version": "1.0.0",
  "isnad_chain": [
    {
      "role": "author",
      "agent": "author_agent",
      "timestamp": "2026-02-15"
    },
    {
      "role": "auditor",
      "agent": "auditor_agent",
      "timestamp": "2026-02-15"
    }
  ]
}
```

モニターはmaṣlaḥah（比例性）テストを実行し、宣言された目的が要求されたパーミッションと一致していることを確認します。

### ログファイル

- **セキュリティログ**: `~/openclaw/workspace/security-monitor.log` - すべてのスキャン結果とステータス
- **アラートログ**: `~/openclaw/workspace/security-alerts.log` - HIGHおよびMEDIUMアラートのみ

### 誤検知の軽減

モニターは既知の良性パターンを自動的にフィルタリングします：

- プレースホルダーパターン: `your_key`, `xxxx`, `MASKED`, `[REDACTED]`
- ドキュメント例: `webhook\.site`, `curl.*\.`
- 開発コマンド: `cat.*\.env`, `grep.*key`

スクリプトの`KNOWN_BENIGN`配列を拡張して、より多くのパターンを追加できます。

### アラート

アラートは重要度に応じて色分けされています：

- 🚨 **HIGH（赤）**: 直ちに対応が必要
  - 秘情報の漏洩
  - 悪意のあるコードパターン
  - 不適切なスクリプト権限（777）
  - ドキュメント化されていないスキルでの未署名実行可能ファイル

- ⚠️ **MEDIUM（黄色）**: 調査を推奨
  - 未検証スキル
  - 不適切なスクリプト権限（775）
  - ファイルの緩い権限
  - 不均衡なパーミッション

- ℹ️ **INFO（緑）**: 情報提供
  - スキャン結果
  - ベースライン更新
  - ステータスメッセージ

### ベストプラクティス

1. **定期的に実行** - 毎日または毎週実行するようにスケジュール
2. **アラートを確認** - `security-alerts.log`を頻繁に確認
3. **設定を更新** - 有効/無効にするチェックをカスタマイズ
4. **秘情報を保護** - `~/.openclaw/secrets/`を700権限で使用
5. **インストール前に確認** - 新しいスキルをインストールする前に常にコードを確認
6. **パーミッションマニフェストを作成** - `permissions.json`でスキルのパーミッションを文書化

### 保護対象

- 🚨 **認証情報の流出** - APIキーが含まれる`.env`ファイルを検出
- 🐍 **サプライチェーン攻撃** - インストールされたスキルの疑わしいパターンを特定
- 🔑 **鍵の盗難** - SSH鍵とウォレット認証情報を監視
- 💀 **悪意のある実行** - 疑わしいコマンドパターンをスキャン
- 📝 **データ漏洩** - ログに秘情報が表示されるのを防止

### 技術詳細

- **言語**: Bash（POSIX準拠）
- **依存関係**: なし（標準的なUnixツールのみ使用: `jq`, `grep`, `find`, `stat`）
- **サイズ**: 約500行
- **プラットフォーム**: Linux, macOS（軽微な調整で）

### バージョン履歴

- **1.1.0** (2026-02-15) - 誤検知軽減とサプライチェーン保護
  - パーミッションマニフェスト検証（isnadインスパイアのmaṣlaḥahテスト）を追加
  - スクリプト実行権限チェックを追加
  - より良い正規表現によるログサニタイズ検知を強化
  - 一般的な良性パターンの誤検知フィルタリングを追加
  - 未署名実行可能ファイル検出を追加
  - 疑わしいドメイン検出を追加

- **1.0.0** (2026-02-08) - 初期リリース
  - 基本的なセキュリティ監視
  - アラートロギングシステム
  - カラーコード出力
  - 設定ファイルサポート

### ライセンス

MITライセンス - 詳細はLICENSEファイルを参照

### 貢献

コントリビューションを歓迎します！イシューやプルリクエストを自由に提出してください。

### 作者

Claw (suzxclaw) によって構築 - AIセキュリティスペシャリスト

---

<div align="center">

**Protect your agents. Preserve your trust.** 🔒

</div>
