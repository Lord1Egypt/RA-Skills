# book-report

**书籍研究工具** — 输入书名，自动产出两份产物：HTML 研究报告（自用）+ 弹药库（跟人聊用）。

> 给中文经典/中国现当代文学读者：输入书名，自动出 HTML 报告 + 弹药库。一次安装，反复用。

## 这是什么

把"想了解一本书"这件事拆成 5 步自动化：
1. 抓维基百科 / 百度百科 / 知乎 / Goodreads / 豆瓣 三源原文
2. （可选）从用户提供的 PDF 抽 4 字段原文（情节/人物/金句/创作背景）
3. LLM 抽取 9 个固定字段（主题/人物/关系/获奖/作者/金句等）
4. 套 Jinja2 模板渲染 HTML 报告（含 Mermaid 人物关系图）
5. 套 Jinja2 模板渲染 Markdown 弹药库（3 开场+6 故事+5 反问+3 收尾）

**典型产物**（30-50 分钟出一本）：
- `reports/<书名>-<日期>.html`（约 15-20KB，10 大章节 + Mermaid 关系图 + 10 人速览表 + 速读指南）
- `reports/chat-弹药库-<书名>-v1.md`（约 12-14KB，4 块结构）

## 三种使用模式

| 模式 | 触发命令 | 数据源 | 适合 |
|---|---|---|---|
| **中文经典**（默认） | `./agent.sh book 活着 --author 余华` | 百度+维基(zh)+知乎 | 茅盾奖/四大名著/当代中文 |
| **英文经典** | `./agent.sh book "..." --author "..." --lang en` | 维基(en)+Goodreads+豆瓣 | 英文经典/诺贝尔/英美现代 |
| **PDF 抽取** | `./agent.sh book 三体 --pdf /path/to/三体.pdf` | 4 字段 PDF + 5 字段 web | 手头有 PDF 想要"原文金句" |

**注意**：
- 英文模式报告**仍是中文样式输出**（界面统一），英文内容放在"摘要/书评"段
- PDF 模式**只支持文本型 PDF**（扫描版 PyMuPDF 抽不出字）
- 任意模式都可叠加：`./agent.sh book 三体 --author 刘慈欣 --lang zh --pdf /path/三体.pdf`

## Quick Start（专家路径 · 5 分钟）

```bash
# 1. 克隆
git clone https://github.com/你的用户名/book-report.git ~/ops/book-report
cd ~/ops/book-report

# 2. 装依赖
pip3 install requests jinja2

# 3. 注册 skill 到 Hermes（如果用 Hermes）
mkdir -p ~/.hermes/skills/book-report
cp SKILL.md ~/.hermes/skills/book-report/

# 4. 跑（任选一种方式）
#    方式 A：用 Claude/Hermes 主对话触发 skill（最简）
#    → 说"用 book-report skill 研究《活着》"
#
#    方式 B：CLI 单独跑（仅骨架版，要 LLM 抽取层需在主对话跑）
./agent.sh book 活着
```

**前置要求**：
- macOS / Linux
- Python 3.10+（jinja2 + requests）
- 可选：Hermes Agent（用于 LLM 主对话抽取）

## 详细步骤（新手路径 · 20 分钟）

### 第 1 步：环境检查

```bash
# 检查 Python
python3 --version  # 需要 3.10+

# 检查 pip
pip3 --version

# 检查 git
git --version
```

如果缺哪个，去 https://www.python.org/ 或 `brew install python git` 装。

### 第 2 步：装到本地

```bash
git clone https://github.com/你的用户名/book-report.git ~/ops/book-report
cd ~/ops/book-report
pip3 install requests jinja2
```

### 第 3 步：测试

```bash
# 试跑 CLI（输出骨架版报告）
./agent.sh book 活着 --author 余华

# 看产物
ls -la reports/
open reports/活着-*.html  # macOS
```

### 第 4 步：完整模式（用 Hermes/Claude LLM 抽取）

CLI 跑出来的报告是**骨架版**（60 分）—— 要 85 分版本，**必须在主对话里触发**：

```
你：用 book-report skill 研究《活着》
AI：（加载 SKILL.md → 抓源数据 → LLM 抽取 → 渲染 → 验证 → 交付）
```

这样 LLM 会现场做抽取层 + 信息可信度自检。

### 第 5 步：代理配置（如果 GitHub / 百度 / 知乎 抓不到）

很多源在国内访问需要代理。如果抓取失败：

```bash
# 默认走代理 7897 端口（已写死）
# 走代理跑
./agent.sh book 活着

# 不走代理跑
USE_PROXY=0 ./agent.sh book 活着
```

或者改 `lib/fetch.py` 顶部的 `PROXY_HTTP` 环境变量。

## 文件结构

```
book-report/
├── README.md                # 本文件
├── .gitignore
├── SKILL.md                 # 注册到 Hermes 的 skill 描述
├── agent.sh                 # CLI 入口（book/html/chat/pdf）
├── lib/
│   ├── fetch.py             # 三源抓取（百度/维基/知乎/Goodreads/豆瓣英文区，zh+en 切换）
│   ├── pdf_extract.py       # PDF 文本抽取（PyMuPDF）
│   └── render.py            # Jinja2 渲染
├── templates/
│   ├── report.html.j2       # HTML 报告模板
│   └── chat-kit.md.j2       # 弹药库模板
└── reports/                 # 输出目录（运行后产生）
    └── README.md            # 产物说明（详见该文件）
```

## 9 个固定字段（每本报告都含）

| # | 字段 | 说明 |
|---|---|---|
| 1 | book_title | 书名 |
| 2 | book_summary | 一句话总结 |
| 3 | theme | 核心主题 + 章节梗概 |
| 4 | characters | 主要人物（4-10 个） |
| 5 | relationships | 人物关系（Mermaid flowchart） |
| 6 | awards | 获奖情况 + 评语要点 |
| 7 | author | 作者生平 + 创作背景 |
| 8 | other_works | 作者其他作品 |
| 9 | quotes | 5-10 句金句（标"未原文核对"） |

## 数据源策略

**中文 (lang=zh，默认)**：
- **百度百科**：主题/情节/人物/获奖。**在某些网络环境不稳定**（m.baike 走代理 SSL EOF，桌面版 403）
- **维基百科（zh）**：主题/情节/作者。**最稳定** ✅
- **知乎**：评价/争议/读者金句。**反爬挡死**（API 路径 400，搜索页 403）

**英文 (lang=en)**：
- **维基百科（en）**：主题/情节/作者。**最稳定** ✅
- **Goodreads**：评分/书评。**经常被反爬**（ratingCount 经常抽不到）
- **豆瓣英文区**：中文读者评价。**经常 SSL EOF**（代理问题）

**PDF（提供时）**：
- 4 字段从 PDF 抽：情节/人物/金句/创作背景
- 5 字段仍走 web：主题/获奖/作者其他作品/关系图/书名
- 只支持**文本型 PDF**（扫描版 PyMuPDF 抽不出字）

**不抓**：豆瓣主站（反爬严）、微信读书评论（要登录态）、起点/晋江/番茄等网络小说站。

实际跑出来往往只 1/3 源（维基）能稳定抓，**这就是为什么必须靠 LLM 抽取层补"未抓到的"那 70%**。

## 「不展示」原则

凡是"凭印象写"的细节，**没有 100% 把握就**：
- 改成模糊表述（"几章"/"部分支线"/"经典一版"）
- 或直接删除
- **绝对不展示**具体集数/章数/演员名/排名/销量/未核对的"原话"

**例外**：维基/百度已确认的事实（生卒年、奖项年份、书名/作者名）保留具体数字。

**优先级高于「让内容更丰富」**——宁可少说不可错说。

## 适用 / 不适用

**适合**：
- 中文经典/中国现当代文学
- 茅盾文学奖/鲁迅文学奖/诺贝尔文学奖等获奖作品
- 维基百科有完整条目的书

**不适合**：
- 冷门/学术/外文原版（web 抓不全）
- 网络小说/未出版手稿（无结构化数据源）
- 需要"逐字引用原文"（当前不支持 PDF 解析）

## 已知限制

- LLM 抽取层靠主对话里的 LLM 现场完成，**没有固化成代码**——CLI 单独跑只能出骨架版
- 百度/知乎抓取在某些网络环境不稳定，**只维基 100% 稳定**
- Goodreads/豆瓣英文区英文模式下经常失败
- **PDF 只支持文本型**（扫描版 PyMuPDF 抽不出字）
- 金句 5-10 句全部标"未原文核对"，**不做学术引用**

## 已验证过的书

3 本中文经典已在本机跑通（HTML 报告 + 弹药库均产出）：
- 茅盾文学奖获奖作品 ×1
- 古典四大名著之一 ×1
- 茅盾文学奖获奖作品 ×1

具体书名不在 README 中列出，**这是有意为之**——本工具是通用能力，不是为某几本书定制。`reports/` 目录里**没有**自带示例，**用户跑出来才生成**。想看产物长什么样，自己 `agent.sh book <任意一本>` 跑一下最快。

如果你在网络受限环境（GitHub 拉不动 / 维基抓不到），README 末尾的"常见问题"里有排查清单。

## 常见问题

**Q：跑 `./agent.sh book 活着` 没反应？**
A：先 `chmod +x agent.sh`。再 `python3 lib/fetch.py --title 活着` 看抓取日志。

**Q：报告里人物关系图没渲染？**
A：HTML 需要联网加载 Mermaid CDN（cdn.jsdelivr.net）。如果网络受限，关系图区域会显示源代码。

**Q：金句/作者生平等信息不全？**
A：见「不展示」原则。**宁可少不可错**。补全方式：用主对话触发 skill，让 LLM 现场判断。

**Q：想跑外文书？**
A：当前是中文专用。外文书要改 `lib/fetch.py` 里的 URL 模板（去 wikipedia 英文版等），暂未支持。

## 路线图

- [ ] 把 LLM 抽取层固化成代码（需要 API key）
- [ ] 解决 playwright 浏览器安装（让百度/知乎抓取稳定）
- [ ] 支持更多语言（日/法/德，Wikipedia 多语言已留接口）
- [ ] ~~PDF 文本抽取~~ ✅ 已支持（仅文本型）
- [ ] 推送到 Hermes Skills Hub（`hermes skills publish`）

## 许可

MIT
