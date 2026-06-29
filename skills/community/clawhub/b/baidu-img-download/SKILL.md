---
name: baidu-img-download
description: "百度图片下载：按关键词从百度图片搜索批量下载图片到本地。触发场景：用户说『下载 关键词 X 张图片』『百度图片下载 X』『用百度抓 N 张图』『按关键词 抓百度图』『百度图片批量下载』『Baidu image download』。底层用 acjson JSON 端点（image.baidu.com/search/acjson），无需浏览器，Node.js 零依赖实现，文件名采用来源页的中文标题，文件落到技能目录的 download/关键词名/ 子目录下。"
---

# 百度图片下载（baidu-img-download）

## Overview

按关键词从百度图片搜索批量下载图片到技能本地目录 `download/<关键词>/`。底层走百度 acjson JSON 端点（无需浏览器、无需登录），纯 Node.js 实现，**零 npm 依赖**。图片文件名采用来源页的中文标题（`fromPageTitle`），方便人工识别。

## Quick Start

```bash
# 默认：缩略图、30 张、文件名带中文标题、输出到 <skill_dir>/download/<keyword>/
node scripts/baidu_img.js -k openclaw

# 指定数量
node scripts/baidu_img.js -k 猫 -n 60

# 下载原图（搜狐/网易/CSDN/百家号等来源，会自动带 Referer）
node scripts/baidu_img.js -k 风景 -n 100 -s origin

# 自定义输出目录
node scripts/baidu_img.js -k 猫 -n 20 -o D:/images/cat
```

PowerShell / cmd / bash 通用，Node ≥ 14 即可。

## Command-Line Options

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--keyword` | `-k` | （必填） | 搜索关键词 |
| `--count` | `-n` | 30 | 目标下载数量 |
| `--source` | `-s` | `thumb` | `thumb` 缩略图（百度 CDN，最稳）/ `middle` 中等图 / `origin` 原始来源图（需 Referer） |
| `--output` | `-o` | `<skill_dir>/download/<关键词>/` | 自定义输出目录 |
| `--delay` | — | 0.3 | 下载间隔秒数（越大越礼貌） |
| `--help` | `-h` | — | 显示帮助 |

## Output Layout

```
<skill_dir>/download/<关键词>/
  ├── 0001_焦点丨从跟风_养虾_到理性选择_ai 智能体该怎么用_龙虾_openclaw_活_a1b2c3d4e5.jpg
  ├── 0002_openclaw低成本部署指南_阿里云68元_年 免费token,个人入门首选_f6g7h8i9j0.jpg
  ├── 0003_中转 api 实战_openclaw 龙虾 token 管控与高效调用技巧_k1l2m3n4o5.jpg
  └── ...
```

**文件名格式**：`{4位序号}_{中文标题}_{url_md5前10位}.{扩展名}`

- 序号：4 位，从 `0001` 开始
- 中文标题：来自搜索结果的 `fromPageTitle`（即来源页标题），清洗规则见下
- 短哈希：URL md5 前 10 位，保证唯一性 + 防重名

**标题清洗规则**：
- 替换非法文件名字符 `\` `/` `:` `*` `?` `"` `<` `>` `|` `\r` `\n` `\t` → `_`
- 多空白 → 单空格
- 去首尾的 `.` `_` `-` 空格
- 截断到 50 字符
- 若来源页没有标题，fallback 到来源域名（去 `www.` 前缀），再不行就是 `untitled`

## How It Works

1. **抓取 acjson**：循环请求 `https://image.baidu.com/search/acjson?tn=resultjson_com&word=KEYWORD&pn=N&rn=60`（每次 60 条，`pn` 递增翻页）
2. **抽取 URL**：从返回 JSON 的 `data[]` 中按 source 选 `thumbURL` / `middleURL` / `replaceUrl[].ObjURL`
3. **下载到本地**：使用 Node 内置 `https` + 自定义 UA / Referer 头，逐张下载并写入 `download/<关键词>/`
4. **去重 + 礼貌爬取**：URL md5 去重 + 翻页间 0.2s / 下载间 0.3s（可调），对每张图做 2 次重试

## Source Selection Tips

- **`thumb`（推荐入门）**：百度自己的 CDN `img0-2.baidu.com`，**不防盗链**，稳。尺寸通常 200~800px。
- **`middle`**：百度 CDN 中等尺寸，约 800~1500px，依然稳定。
- **`origin`**：原图，来自搜狐 / 网易 / CSDN / 百家号 / 阿里云 OSS 等原始站点，**多数会校验 Referer**。脚本会自动从 `fromURLHost` 拼 `https://<host>/` 作为 Referer。如果仍然 403，把 `--source` 改回 `thumb` 或 `middle` 即可。

## Notes

- **零依赖**：只用 Node 内置的 `https` / `http` / `fs` / `path` / `crypto` / `url`，不需要 `npm install`。
- 百度 acjson 偶尔会因风控返回空 `data[]`，脚本会优雅停止，不会卡死。
- 失败且已写入 < 1KB 的半成品文件会被自动删除，避免污染输出目录。
- 关键词中带空格 / 中文 / 特殊字符都没问题，URL encode 由脚本处理。
- 不需要登录，不需要 Cookie，不需要浏览器。

## Resources

### scripts/

- `baidu_img.js` — 主下载脚本（Node.js 零依赖，Node ≥ 14 即可）
