---
name: dcard
description: 擷取 Dcard 文章完整內文。Dcard 有 Cloudflare 保護，需用 patchright (Playwright) headless browser 繞過。支援文章標題、全文、圖片連結輸出。
metadata:
  openclaw:
    emoji: 🎴
    requires:
      bins:
        - python3.14
        - camoufox
---

# Dcard 🎴

用 Camoufox（Firefox-based stealth browser）+ patchright 繞過 Dcard 的 Cloudflare 保護。
Camoufox 內建 uBlock Origin + 反指紋偵測，可以直接 bypass Cloudflare challenge，
且 Firefox 不會有 WSL2 + Tailscale DNS 的問題。

## 使用方式

```bash
# 單篇文章
dcard_fetch.py https://www.dcard.tw/f/relationship/p/261529038

# 純 ID（預設看板 relationship）
dcard_fetch.py --id 261529038

# 指定看板
dcard_fetch.py --forum makeup --id 123456

# JSON 輸出
dcard_fetch.py https://www.dcard.tw/f/relationship/p/261529038 --format json

# 看板熱門
dcard_fetch.py list relationship

# 看板最新
dcard_fetch.py list relationship --sort latest --limit 10

# 全站熱門看板
dcard_fetch.py list --all-forums
```

## 腳本

- `scripts/dcard_fetch.py` — 主腳本（Python3.14）
- `scripts/_list_posts.js` — 看板列表用 JS extractor

## 安裝依賴

需要 **Camoufox** + **patchright** + **lxml**。

```bash
# 1. 安裝 Camoufox + patchright + lxml
pip3.14 install camoufox lxml patchright

# 2. 下載 Camoufox 瀏覽器（~280MB）
camoufox fetch

# 檢查
camoufox version
# → Camoufox: v135.0.1-beta.xx (Up to date!)
```

## 技術細節

**為什麼用 Camoufox 而不是 Chromium？**
- Firefox 在 WSL2 下 DNS 正常（Tailscale DNS 不會炸）
- 內建 uBlock Origin 擋廣告與 tracker
- 自訂指紋不會被 Cloudflare 標記為 headless
- 不需要 `--host-resolver-rules` 繞 DNS

**JSON-LD 解析：** 內文從 `<script type="application/ld+json">` 的 SocialMediaPosting schema 提取，
圖片抓 `megapx-assets` domain 的 orig/1280 圖床連結。

## 限制

- 短時間大量 request 仍可能觸發 Cloudflare rate-limit
- 首次使用需下載 Camoufox（`camoufox fetch`）
- 不支援搜尋功能（v0.1.0）
