# 技能：全能网页爬取与智能解析 (Crawl4AI)

## 1. 环境依赖与安装 (Prerequisites)
如果系统尚未安装 Crawl4AI，Agent 应参考以下步骤进行环境部署：

1. **核心库安装**: `pip3 install crawl4ai` (注意：尝试pip或者pip3)
2. **浏览器内核初始化**: `python3 -m playwright install chromium` (下载 Playwright 所需的 Chromium 内核)
3. **验证安装**: `crwl --help`

---

## 2. 技能描述
当用户提供 URL 并要求“总结内容”、“提取数据”或“分析网页”时触发。利用 Crawl4AI 引擎将复杂网页（含动态 JS 渲染）精准转化为 Markdown 格式。

---

## 3. 核心指令集

读取 URL 内容到控制台：
```bash
crwl {url} -o markdown
```

读取 URL 内容到文件：
```bash
crwl {url} -o markdown > {file_name}.md
```

---


## 4. 使用示例

| 用户指令 | 预期的 Agent 行为 (Command) |
| --- | --- |
| "帮我看看这个网页：[URL]" | `crwl {URL} -o markdown` |
| "总结这个文章：[URL]" | `crwl {URL} -o markdown > article.md` |

---

## 5. 约束与安全

* **隐私申明**: 不得爬取登录后可见的内容。