# embedded-code-skill

> Embedded C コード生成仕様 — チームコードスタイルの統一、プロダクショングレードのドライバコード生成

<!-- Language Switcher -->
[简体中文](README.md) · [English](README_EN.md) · [日本語](README_JP.md)

---

[![Platform: Claude Code | VS Code | Cursor | OpenClaw | Hermes Agent](https://img.shields.io/badge/Platform-Claude%20Code%20%7C%20VS%20Code%20%7C%20Cursor%20%7C%20OpenClaw%20%7C%20Hermes%20Agent-blue)]()
[![Standard: MISRA-C Compliant](https://img.shields.io/badge/Standard-MISRA--C%20Compliant-green)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)]()

---

## 機能

- **3つの動作モード** — GENERATE（生成）、REWRITE（書き換え）、REVIEW（レビュー）
- **プロダクショングレードのコード** — 組込みソフトウェアアーキテクトのように考え、進化可能でテスト可能なコードを生成
- **マルチプラットフォーム** — STM32 (Cortex-M)、PowerPC、RISC-V、ARM Cortex-A
- **チーム統一** — 一貫したコードスタイル、レビューエビデンス
- **自己進化** — 組込みのダーウィン式最適化システム、継続的な改善

---

## クイックスタート

```bash
/embedded-code-skill STM32 UARTドライバを生成、ベースアドレス 0x4000C000
/embedded-code-skill このコードを仕様に合わせて書き換える
/embedded-code-skill このコードが仕様是否符合をレビュー
```

---

## 3つの動作モード

### GENERATE モード

仕様を直接適用してコードを生成。古いコードの保持は不要。

### REWRITE モード

**核心原則：機能フローファースト**

- ユーザーが提供したソースコードは元の機能実装フローを表す
- コードにエラーがあっても、書き換える前に機能フローを完全に理解する必要がある
- 仕様に合わせるために元の機能ロジックを壊してはならない
- 元コードのバグは「機能フロー」の一部であり、デフォルトで維持

### REVIEW モード

既存のコードが Embedded C 仕様に是否符合かをチェックし、レビューリストに従って項目ごとにチェックし、変更提案を提供。

---

## コア要件

| 要件 | 仕様 |
|------|------|
| **可読性** | `snake_case` / `SCREAMING_SNAKE` / `camelCase` 命名、Doxygenコメント |
| **移植性** | `stdint.h` タイプ、`volatile` レジスタマクロ、`int`/`char`/`long` 禁止 |
| **データ構造** | `struct`/`enum` でデータ組織、散らばったグローバル変数禁止 |
| **エラー処理** | public関数は `embedded_code_status_t` を返す、NULL チェック |
| **安全なコーディング** | `malloc`/`free`/VLA 禁止、固定サイズバッファ |

---

## コード生成前に提供する情報

| 情報 | 必要性 | 例 |
|------|--------|-----|
| 外周レジスタベースアドレス | **必須** | `UART_BASE_ADDR = 0x4000C000U` |
| チップ/アーキテクチャタイプ | 推論可能 | `STM32`, `Cortex-M4`, `RISC-V` |

> **注意**: ベースアドレスは必須。AIはレジスタアドレスを捏造してはならない。

---

## ファイル構造

```
embedded-code-skill/
├── SKILL.md                     # スラッシュコマンドエントリ
├── README.md                    # このファイル（中国語）
├── README_EN.md                 # 英語版
├── README_JP.md                # 日本語版
│
├── .evolution/                  # 自己進化システム
│   ├── SKILL.md                # 進化システムメインファイル
│   ├── test-prompts.json       # テストケースセット
│   ├── results.tsv            # 最適化履歴
│   └── README.md              # 進化システム文書
│
├── embedded-code-skill-standards/
│   └── SKILL.md
│
├── embedded-code-skill-arch/
│   └── SKILL.md                # Cortex-M/A, PowerPC, RISC-V
│
├── embedded-code-skill-drivers/
│   └── SKILL.md                # UART, SPI, I2C, DMA, CAN
│
└── embedded-code-skill-domains/
    └── SKILL.md                # 航空/軍事/産業/自動車
```

---

## 出力形式

GENERATE モードは各外周モジュールを出力：

```
module/
├── module_reg.h    # レジスタ構造体定義
├── module.h        # 公開インターフェース
└── module.c       # 実装
```

**uart_reg.h 例:**

```c
/**
 * @file uart_reg.h
 * @brief UART 外周レジスタ定義
 */
#ifndef UART_REG_H
#define UART_REG_H

#include <stdint.h>

/* ベースアドレス */
#define UART_BASE_ADDR  (0x4000C000U)

/* レジスタ構造体 */
typedef struct {
    volatile uint32_t DR;       /* 0x00: Data register */
    volatile uint32_t RSR;      /* 0x04: Receive status register */
    volatile uint32_t Reserved;
    volatile uint32_t FR;       /* 0x18: Flag register */
    volatile uint32_t IBRD;     /* 0x24: Integer baud rate divisor */
    volatile uint32_t FBRD;     /* 0x28: Fractional baud rate divisor */
    volatile uint32_t LCRH;     /* 0x2C: Line control register */
    volatile uint32_t CR;       /* 0x30: Control register */
} uart_reg_t;

/* レジスタアクセス */
#define UART_REG  ((uart_reg_t *) UART_BASE_ADDR)

#endif /* UART_REG_H */
```

---

## 自己進化システム

ダーウィン.skillに基づく組込み自己最適化システム：

- **8次元評価** — 構造品質（60点）+ 実際効果（40点）
- **ラチェット機構** — 改善のみ保持、自動的にロールバック
- **サブエージェント検証** — 効果次元はサブエージェントを使用する必要がある
- **人在ループ** — 各最適化ラウンド後に一時停止、ユーザーの確認待ち

### 進化をトリガー

```
ユーザー：「embedded-code-skillを最適化」           → 完全な最適化フロー
ユーザー：「embedded-code-skillの品質を評価」      → 評価のみ
ユーザー：「embedded-code-skillの自己進化を実行」  → 確認まで自動最適化
```

---

## 貢献

Issue と Pull Request を歓迎！

---

## ライセンス

MIT License
