---
name: book-report
version: 1.0.0
author: AlZero-t
license: MIT
description: Use when the user wants to "了解一本书" or "出一份书的研究报告" or "做读书弹药库" or "用 book-report skill 研究 XXX". Produces two artifacts per book -- HTML 报告 for self-study, 弹药库 for casual conversation. Supports Chinese classics (default), English classics (--lang en), and PDF text extraction (--pdf). Workflow -- 维基百科+百度百科+知乎 抓取 + LLM 抽取 + 模板渲染 输出两件套。
keywords: [books, research, chinese, english, pdf, mermaid, knowledge-report, reading]
metadata:
  hermes:
    tags: [books, research, content, knowledge, pdf, mermaid, chinese, english]
    homepage: https://github.com/AlZero-t/book-report
    related_skills: [deep-research, blogwatcher, last30days]
    category: research
    trust: community
---

# book-report skill

## 用途

输入一个书名（或书名+作者），输出两件套：

1. **HTML 报告**（`reports/<书名>-<日期>.html`）— 给你"看完了解这本书"用
2. **弹药库**（`reports/chat-弹药库-<书名>-v1.md`）— 给你"跟人聊能现成调出"用

## 三种使用模式

### 模式 1：中文经典（默认）
```
./agent.sh book 活着 --author 余华
```
- 数据源：百度百科 + 维基百科(zh) + 知乎
- 适合：茅盾文学奖/鲁迅文学奖/古典四大名著/当代中文小说

### 模式 2：英文经典
```
./agent.sh book "The Old Man and the Sea" --author "Hemingway" --lang en
```
- 数据源：维基百科(en) + Goodreads + 豆瓣英文区
- 适合：英文经典/诺贝尔文学奖/英美现代小说
- **报告仍用中文样式输出**（界面统一）

### 模式 3：PDF 抽取 + web 兜底
```
./agent.sh book 三体 --pdf /path/to/三体.pdf
```
- **4 字段从 PDF 抽**（情节/人物/金句/创作背景）—— 真正的"原文金句"
- **5 字段仍走 web**（主题/获奖/作者其他作品/关系图/书名）—— 9 字段框架不能全靠 PDF
- **老实标注**哪些字段从 PDF 来、哪些从 web 来
- **只支持文本型 PDF**（扫描版 PDF 抽不出字，PyMuPDF 限制）

## 适用范围

**擅长**：
- 中文经典/中国现当代文学
- 英文经典（英美现代小说、诺贝尔文学奖）
- 用户手头有 PDF 时（精准抽取原文金句）

**不擅长（会降级告知用户）**：
- 冷门/学术/非英中文（web 抓不全）
- 扫描版 PDF（PyMuPDF 抽不出图像里的字）
- 网络小说/未出版手稿（无结构化数据源）

## 数据源策略

**中文 (lang=zh)**：
- 百度百科：主题/情节/人物/获奖。**在用户机器上不稳定**（m.baike 走代理 SSL EOF，桌面版 403）—— 实际往往只抓到维基
- 维基百科（zh）：主题/情节/作者。**最稳定** ✅
- 知乎：评价/争议/读者金句。**反爬挡死**

**英文 (lang=en)**：
- 维基百科（en）：主题/情节/作者。**最稳定** ✅
- Goodreads：评分/书评。**经常被反爬**（ratingCount 经常抽不到）
- 豆瓣英文区：中文读者评价。**经常 SSL EOF**（代理问题）

**不抓**：豆瓣主站（反爬严）、微信读书评论（要登录态）、起点/晋江/番茄等网络小说站

## 流程（每本书跑 5-7 步）

1. **抓源数据**（`lib/fetch.py`）— 3 个源并行（zh 或 en 配置）
2. **PDF 抽取**（`lib/pdf_extract.py`，可选）—— 提供 `--pdf` 才走
3. **结构化抽取**（LLM 处理）— 从源数据中提取 9 个固定字段
4. **渲染 HTML**（`lib/render.py`）— 套 `templates/report.html.j2`
5. **渲染弹药库**（`lib/render.py`）— 套 `templates/chat-kit.md.j2`
6. **信息可信度扫一遍** — 按"不展示原则"清理不确定信息
7. **交付** — 告知用户两个文件路径

## 9 个固定字段（必抽齐）

| # | 字段 | 来源（zh） | 来源（en） | 可从 PDF 抽？ |
|---|---|---|---|---|
| 1 | book_title | 维基/百度 | 维基/Goodreads | ✓ 封面 |
| 2 | book_summary | 维基/百度 summary | 维基 lead | ✗ |
| 3 | theme | 维基正文 | 维基正文 | ✓（LLM 抽） |
| 4 | characters | 维基/百度 | 维基 | ✓ **最稳** |
| 5 | relationships | 维基/百度星图 | 维基 | ✓ |
| 6 | awards | 维基/百度 | 维基 | ✗（除非书里写）|
| 7 | author | 维基 | 维基 | ✓ 前言/后记 |
| 8 | other_works | 维基/百度 | 维基 | ✗ |
| 9 | quotes | 读者笔记/书评 | Goodreads 书评 | ✓ **最准** |

**PDF 抽 4 字段**（稳定）：情节/人物/金句/创作背景
**web 抽 5 字段**（必要）：主题/获奖/作者其他作品/关系图/书名

## 弹药库必含 4 块

1. **3 句开场**（反常识/代际/生活 三选一）
2. **6 个故事**（按"画面 > 节奏 > 共情 > 灰度 > 作者 > 销量"排序）
3. **5 个反问接住**（"讲什么"/vs 经典书/过时吗/为什么火/作者怎样）
4. **3 句收尾**（记一个人 / 戳一句 / 留尾巴）

## 「不展示」原则（用户强偏好）

凡是"凭印象写"的细节，**没有 100% 把握就**：
- 改成模糊表述（"几章"/"部分支线"/"经典一版"）
- 或直接删除
- **绝对不展示**具体集数/章数/演员名/排名/销量/未核对的"原话"

**例外**：维基/百度已确认的事实（生卒年、奖项年份、书名/作者名）保留具体数字。

**适用范围**：所有 book-report 输出的报告、笔记、文案、小红书/抖音脚本。**优先级高于「让内容更丰富」**——宁可少说不可错说。

## 质量自检清单（每本必走）

- 9 个字段是否都填了？缺哪几个要在报告里标"未抓到"
- Mermaid 关系图能否渲染？（必打开看一次）
- 金句是否全部标"未原文核对"？或全部来自 PDF（带页码）？
- 是否有"凭印象写的具体数字"？有就改/删
- 弹药库 4 块是否齐全？
- 文件路径是否告知用户？

## 失败模式（必须老实告诉用户）

- 源数据缺失 → 报告里留 "未抓到" 标签，**不编造**
- 关系图超过 25 节点 → 拆成 2 张
- 抓取超时 → 重试 2 次后放弃，告知用户
- 维基无条目（如冷门书） → 改用百度 + Goodreads 双源 + 提示用户数据稀薄
- 扫描版 PDF → 老实说"PDF 抽不出字，建议提供文本型 PDF"

## 触发关键词

中英文皆可：
- "用 book-report skill 研究 XXX"
- "做一份 XXX 的读书报告"
- "我需要了解 XXX 这本书"
- "出一份书的研究报告"
- "做个读书弹药库"
- "讲 XXX 这本书给我听"

## 相关文件

本 skill 的实现代码（CLI 工具 + 模板）位于：
- `agent.sh` — CLI 入口（book/html/chat/pdf）
- `lib/fetch.py` — 三源抓取（zh/en 切换 + Wikipedia 多语言 + Goodreads + 豆瓣英文区）
- `lib/pdf_extract.py` — PDF 文本抽取（PyMuPDF）
- `lib/render.py` — 模板渲染
- `templates/` — Jinja2 模板
- `reports/` — 输出目录

## 已验证可用的书

3 本中文经典已在本机跑通（HTML 报告 + 弹药库均产出）：
- 茅盾文学奖获奖作品 ×1
- 古典四大名著之一 ×1
- 茅盾文学奖获奖作品 ×1

英文测试：The Old Man and the Sea（Hemingway）跑通（lang=en + Wikipedia EN + Goodreads）

## 已知限制

- **LLM 抽取层**靠主对话里的 LLM 现场完成，**没有固化成代码**——CLI 单独跑只能出骨架版
- **百度/知乎抓取**在用户机器上不稳定，**只维基 100% 稳定**
- **Goodreads/豆瓣英文区**英文模式下经常失败
- **PDF 只支持文本型**（扫描版 PyMuPDF 抽不出）
- **金句可信度**：5-10 句全部标"未原文核对"，不做学术引用
- **playwright 浏览器**因 169MB 下载卡住未装，**当前 lib/fetch.py 走 requests 轻量方案**
