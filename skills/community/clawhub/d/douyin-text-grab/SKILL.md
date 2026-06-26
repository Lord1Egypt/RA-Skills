---
name: douyin-text-extractor
description: "从抖音链接提取完整文案并生成Word文件。触发条件：用户发送抖音链接并要求提取文案/文本/内容，或说'抓文案''提取内容''做成文件'。支持视频和图文笔记。不做总结不改写，原文案完整提取。"
---

# 抖音文案提取技能

## 触发条件

用户发送抖音链接（`https://v.douyin.com/xxx` 或分享口令）+ 提取/抓取/文案/内容/文件 相关意图。

## 工作流程

### Step 1: 解析短链获取数据

```bash
curl -s -L -o /tmp/douyin_page.html \
  -w "%{http_code}" \
  "https://v.douyin.com/xxx/" \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1" \
  --connect-timeout 10
```

### Step 2: 提取 _ROUTER_DATA

从 HTML 中提取 `_ROUTER_DATA` JSON，关键字段：
- `item_list[0].desc` — **完整文案**（核心，一个字不改）
- `item_list[0].author.nickname` — 作者昵称
- `item_list[0].statistics` — 点赞/评论/转发/收藏
- `item_list[0].create_time` — 发布时间戳

### Step 3: 生成 Word 文件

使用 `scripts/create_docx.py`：

```bash
python3 scripts/create_docx.py --title "标题" --author "作者" --content "完整文案" --output /tmp/output.docx
```

### Step 4: 投递文件

```
message action=send filePath=/tmp/output.docx
```

## 核心规则

1. **原文案完整提取，不总结不改写**
2. **先交文件再说话** — 不问"要不要做"
3. 按原文结构排版：识别"第X组""复制这句"等结构化内容
4. 文件名包含作者名便于识别
