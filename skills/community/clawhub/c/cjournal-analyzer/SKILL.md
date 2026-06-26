---
name: cjournal-analyzer
description: >
  C刊（CSSCI来源期刊）论文全面分析工具。当用户提供一个具体的C刊期刊名称（如"管理世界"、
  "社会学研究"、"经济研究"等）时，自动通过知网（CNKI）查询该期刊最近5年所有期次的文章
  目录、作者和摘要信息，并生成专业的Word分析报告。报告包含：选题热点趋势、高频关键词、
  研究方法偏好、核心作者群、栏目主题演变、研究空白识别、投稿方向建议等全维度分析。
  触发条件：用户提到需要分析某个C刊/CSSCI期刊/核心期刊的发文趋势、选题偏好、投稿方向；
  或提供中文学术期刊名称并要求查看近年发表论文的主题分布和趋势；或说"帮我分析一下XX期刊"。
  注意：本skill用于期刊层面的宏观分析，不同于paper-analyzer（单篇论文拆解）和
  literature-review-writer（文献综述写作）。
---

# C刊论文全面分析工具

## Phase 1: 确定期刊与CNKI代码

1. 从用户输入中提取期刊名称
2. 查询 `references/journal_codes.md` 获取CNKI代码（如"管理世界"→ `GLSJ`）
3. 若未收录，用WebSearch搜索 `site:navi.cnki.net/knavi/journals "{期刊名}"` 从URL提取代码
4. 向用户确认期刊后继续

## Phase 2: 浏览器数据采集

使用Chrome DevTools MCP工具从知网采集数据。

### Step 2.1: 打开期刊页

```
navigate_page → https://navi.cnki.net/knavi/journals/{CODE}/detail
```

**验证码处理**：若页面出现"请完成安全验证"或"拖动下方拼图"，立即提示用户：
> "知网需要安全验证，请在浏览器中完成滑块验证，完成后告诉我。"

等用户确认后，用 `navigate_page` 重新加载页面。

### Step 2.2: 提取期刊基本信息

```javascript
() => {
  const title = document.querySelector('h3')?.textContent?.trim() || '';
  const info = {};
  document.querySelectorAll('.detailInfo p, .s-info p').forEach(p => {
    const text = p.textContent;
    if (text.includes('主办单位')) info.sponsor = text.split('：')[1]?.trim();
    if (text.includes('ISSN')) info.issn = text.split('：')[1]?.trim();
    if (text.includes('CN')) info.cn = text.split('：')[1]?.trim();
    if (text.includes('出版周期')) info.frequency = text.split('：')[1]?.trim();
    if (text.includes('复合影响因子')) info.cif = text.split('：')[1]?.trim();
    if (text.includes('综合影响因子')) info.aif = text.split('：')[1]?.trim();
  });
  return { title, ...info };
}
```

也可直接从snapshot中读取基本信息（StaticText节点）。

### Step 2.3: 点击"论文"标签并提取年份期次

点击 uid 对应"论文"的链接，等待加载，然后提取：

```javascript
() => {
  const results = [];
  document.querySelectorAll('dl[id$="_Year_Issue"]').forEach(dl => {
    const year = dl.querySelector('dt em')?.textContent?.trim();
    if (!year) return;
    const issues = [];
    dl.querySelectorAll('dd a').forEach(a => {
      issues.push({ id: a.id, issue: a.textContent.trim(), value: a.getAttribute('value') });
    });
    results.push({ year: parseInt(year), issues });
  });
  return results;
}
```

筛选最近5年数据（当前年份 - 4 至当前年份）。若知网分页显示年份（每页显示部分年份），需翻页加载更多。

### Step 2.4: 逐期采集文章列表

对每个期次，点击对应的期次链接（通过 `click` uid 或 `evaluate_script` 模拟点击），等待文章列表加载（`wait_for` 等待标题出现或等1-2秒），然后提取：

```javascript
() => {
  const articles = [];
  document.querySelectorAll('#CatalogList dd.row').forEach(dd => {
    const titleEl = dd.querySelector('span.name a');
    const authorEl = dd.querySelector('span.author');
    const pageEl = dd.querySelector('span.company');
    const sectionEl = dd.closest('div')?.querySelector('dt.tit');
    if (titleEl) {
      articles.push({
        title: titleEl.textContent.trim(),
        url: titleEl.href,
        authors: authorEl?.getAttribute('title')?.replace(/;$/,'') || '',
        pages: pageEl?.getAttribute('title') || '',
        section: sectionEl?.textContent?.trim() || ''
      });
    }
  });
  return articles;
}
```

**关键**：
- 每个期次采集间隔1-2秒，避免触发反爬
- 持续向用户报告进度（如"正在采集2024年第6期，已完成32/60期..."）
- 所有数据暂存到一个JSON数组中

### Step 2.5: 摘要采集（抽样策略）

全量摘要采集耗时极长，采用抽样：每年选取2期（如第1期和第7期），每期取前3篇文章访问摘要页。

访问文章详情页后提取摘要：

```javascript
() => {
  const abs = document.querySelector('#ChDivSummary, .abstract-text, [name="abstracts"]');
  const kw = document.querySelector('#ChDivKeyWord, .keywords');
  return {
    abstract: abs?.textContent?.trim() || '',
    keywords: kw?.textContent?.replace('关键词：','').trim() || ''
  };
}
```

若浏览器方式受阻，用WebSearch搜索 `"{文章标题}" site:cnki.net` 补充摘要和关键词。

## Phase 3: 数据分析

采集完成后，将所有数据保存为JSON，然后运行 `scripts/analyze_journal.py` 进行分析。

该脚本依赖：`pip3 install jieba wordcloud python-docx matplotlib numpy`

脚本接收JSON数据文件路径，输出分析结果和可视化图表：

1. **发文量趋势**：按年度统计发文数量折线图
2. **高频关键词Top30**：jieba分词 → 去停用词 → 词频统计 → 柱状图+词云
3. **主题聚类**：基于高频词共现进行粗粒度主题归类
4. **栏目分析**：各栏目发文占比饼图及趋势变化
5. **核心作者Top20**：发文频次柱状图
6. **研究方法识别**：从标题中匹配方法关键词（实证/案例/实验/模型/仿真/调查/访谈/文献计量/元分析/回归/面板数据/DID/RDD/PSM/机器学习/深度学习/SEM/扎根理论等）
7. **热点演变**：前3年 vs 近2年的关键词对比，识别新兴/衰退主题
8. **研究空白与投稿建议**：基于以上分析综合给出

## Phase 4: 生成Word报告

使用python-docx生成格式化报告，结构：

```
封面：《{期刊名}》近五年（{起始年}-{结束年}）发文分析报告

一、期刊概况
二、发文量与趋势分析（含图表）
三、选题热点分析（含词云图、高频词柱状图）
四、热点演变与新兴主题
五、核心作者群分析
六、研究方法偏好分析
七、栏目主题分析
八、研究空白与投稿建议
附录：完整文章目录（按年份-期次排列）
```

报告保存至 `~/Downloads/{期刊名}_近五年发文分析报告.docx`。

## 注意事项

- 知网有反爬机制，每次请求间隔≥1秒
- 验证码出现时必须请用户手动完成
- 安装依赖：`pip3 install jieba wordcloud python-docx matplotlib numpy`
- 期刊代码优先查 `references/journal_codes.md`
- 采集全程保持进度播报
