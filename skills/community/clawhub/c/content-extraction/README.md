# content-extraction

OpenClaw 原生内容提取技能：把 URL / 文档转成干净 Markdown。

## 这是什么

它做一件事：**识别输入来源，走最稳的抓取通道，输出可读 Markdown。**

这版是**可执行版**，保留了路由和执行骨架：
- `scripts/extract_router.py`：判定来源并生成路由计划
- `scripts/extract.py`：把路由计划整理成可执行 extraction spec

## 适用场景
- 公众号文章整理
- 飞书文档 / 知识库导出
- YouTube 字幕 / 转录整理
- 通用网页清洗、摘要、归档

## 路由原则

先判断来源，再决定通道，不要一把梭。

| 输入类型 | 首选通道 | 备选通道 |
|---|---|---|
| `mp.weixin.qq.com` | browser | 失败后再考虑通用网页降级 |
| `feishu.cn` / `larksuite.com` | Feishu 工具 | 结构化读取失败时再退回通用网页思路 |
| `youtube.com` / `youtu.be` | YouTube transcript 链 | 失败后返回明确原因，不硬抓 HTML |
| 其他 URL | `r.jina.ai` → `defuddle.md` → `web_fetch` / browser | 按级联顺序逐步降级 |

## 输出目标

抓到内容后，默认输出这几个部分：

```md
**标题**: ...
**作者**: ...
**来源**: 公众号 / 飞书文档 / 网页 / YouTube
**URL**: ...

### 内容摘要
...

### 正文
...
```

长内容建议同时保存本地 Markdown 文件，只在回复里给摘要和路径。

## 路由细则

### 1) 微信公众号

- 用 browser 打开页面
- 等正文区域加载完成
- 提取标题、作者、发布时间、正文、图片
- 输出 Markdown frontmatter 或头部字段
- 图片保留为链接，必要时转成 `![image](url)`

### 2) 飞书文档 / 飞书知识库

- 先解析 URL 类型：doc / docx / wiki
- 优先走 Feishu 工具直接读结构化内容
- 尽量保留标题、列表、引用、代码块、待办、表格、图片
- 以 block → Markdown 的方式做格式映射

### 3) YouTube

- 走 transcript / transcript-summary 链
- 优先输出字幕文本，再按需压成 Markdown
- 不把普通网页抓取当成主路径

### 4) 通用网页

按顺序尝试：
1. `r.jina.ai`
2. `defuddle.md`
3. `web_fetch`
4. browser fallback

每一层失败都要能说清楚为什么失败，而不是沉默。

## 使用示例

### 公众号

- 输入：公众号文章 URL
- 预期：返回标题、作者、摘要、正文 Markdown

### 飞书文档

- 输入：飞书 doc / docx / wiki URL
- 预期：返回保留层级结构的 Markdown

### 通用网页

- 输入：新闻、博客、知识页 URL
- 预期：先走代理清洗，再做本地回退

### YouTube

- 输入：视频 URL
- 预期：返回字幕或整理后的转录 Markdown

## 失败策略

失败时不要装作成功。要明确返回：
- 失败在哪一层
- 为什么失败
- 下一层为什么被尝试或跳过
- 如果无法继续，给出最短可理解的原因

## 设计原则

- 先路由，再抓取
- 先专用，再通用
- 先高质量，再降级
- 默认保存，长内容优先落盘
- 输出要干净，不要 HTML 噪音

## 安装提示

这个技能不依赖 Claude Code 私有实现。
它只需要 OpenClaw 现有能力：
- browser
- feishu
- web_fetch
- YouTube transcript 链

## 维护

如果后面要继续增强，优先补这三块：
1. 平台判定规则
2. block → Markdown 映射表
3. 测试样例集
