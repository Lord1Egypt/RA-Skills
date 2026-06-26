# 证据清洗用例集

## 用例 1：搜索结果清洗（混合高质量和农场号结果）

### 场景描述

通过搜索获取了关于"OpenAI 发布 GPT-5"的 8 条结果，其中包含权威媒体报道、自媒体搬运、营销号和完全无关内容。

### 输入

```json
{
  "raw_evidence_items": [
    {
      "source_url": "https://www.reuters.com/technology/openai-gpt5",
      "title": "OpenAI Announces GPT-5 with Enhanced Reasoning Capabilities",
      "snippet": "OpenAI on Tuesday unveiled GPT-5, its most advanced language model to date, featuring significant improvements in mathematical reasoning and code generation.",
      "publish_date": "2024-05-15"
    },
    {
      "source_url": "https://www.zaobao.com.sg/tech/openai-gpt5",
      "title": "OpenAI发布GPT-5，推理能力大幅提升",
      "snippet": "OpenAI周二发布了GPT-5模型，该模型在数学推理和代码生成方面取得重大突破。",
      "publish_date": "2024-05-15"
    },
    {
      "source_url": "https://baijiahao.baidu.com/s?id=1800000001",
      "title": "重磅！OpenAI发布GPT-5，AI行业格局将彻底改变！",
      "snippet": "今日，OpenAI正式发布了GPT-5大模型。据知情人士透露，该模型性能是GPT-4的10倍以上。这将对整个AI行业产生深远影响。与此同时，XX品牌AI智能音箱正在限时促销中...",
      "publish_date": "2024-05-15"
    },
    {
      "source_url": "https://mp.weixin.qq.com/s/abc123",
      "title": "GPT-5发布！AI从业者的生存指南",
      "snippet": "GPT-5来了！作为AI从业者，你需要了解的10个关键变化。本文将从技术原理、行业影响、个人应对三个维度进行深度分析...",
      "publish_date": "2024-05-15"
    },
    {
      "source_url": "https://toutiao.com/item/7300000001",
      "title": "OpenAI发布GPT-5，根据全球人工智能治理委员会报告",
      "snippet": "根据全球人工智能治理委员会（GAIGC）发布的报告，OpenAI此次发布的GPT-5在安全性方面做出了重大改进...",
      "publish_date": "2024-05-15"
    },
    {
      "source_url": "https://www.36kr.com/news/openai-gpt5",
      "title": "36氪独家 | OpenAI发布GPT-5，一文看懂技术亮点",
      "snippet": "OpenAI今日正式发布GPT-5。核心亮点包括：1. 数学推理能力提升300% 2. 代码生成准确率达到95% 3. 上下文窗口扩展至500K tokens",
      "publish_date": "2024-05-15"
    },
    {
      "source_url": "https://www.cooking-ai-recipes.com/gpt5",
      "title": "AI帮你做菜！GPT-5最强菜谱推荐",
      "snippet": "GPT-5不仅能写代码，还能帮你做饭！以下是10个AI推荐的周末菜谱...",
      "publish_date": "2024-05-16"
    },
    {
      "source_url": "https://news.cn/tech/openai-gpt5",
      "title": "新华社：OpenAI发布新一代大语言模型GPT-5",
      "snippet": "新华社旧金山5月15日电 美国人工智能研究公司OpenAI15日发布新一代大语言模型GPT-5，该模型在推理能力方面较上一代有显著提升。",
      "publish_date": "2024-05-15"
    }
  ],
  "primary_subject": "OpenAI GPT-5发布",
  "canonical_time_frame": {
    "start": "2024-05-01",
    "end": "2024-05-31",
    "granularity": "day"
  },
  "cleaning_goal": "为新闻分析准备关于OpenAI GPT-5发布的权威证据"
}
```

### 处理过程

**Step 1 DOM 噪声剥离**：无需处理（所有 snippet 格式正常）

**Step 2 伪实体检测**：
- 条目 5：引用"全球人工智能治理委员会（GAIGC）"→ 该组织无法验证存在 → 标记伪实体
- 条目 3：声称"性能是GPT-4的10倍以上"→ 无法验证 → 标记可疑声明

**Step 3 去重压缩**：
- 条目 1（Reuters）和条目 2（联合早报）：内容高度相似，为同一事件不同语言报道 → 合并保留 Reuters（一手英文来源）
- 条目 1（Reuters）和条目 8（新华社）：内容高度相似 → 合并保留，标注双来源

**Step 4 错域降权**：
- 条目 3（百家号）：夹带广告 → 降权 D3
- 条目 4（微信公众号）：未认证自媒体，标题党 → 降权 D2
- 条目 7（cooking-ai-recipes.com）：完全无关 → Drop

**Step 5 Snippet 标准化**：统一格式

### 输出

```json
{
  "cleaned_evidence": [
    {
      "id": "ev_001",
      "source_url": "https://www.reuters.com/technology/openai-gpt5",
      "title": "OpenAI Announces GPT-5 with Enhanced Reasoning Capabilities",
      "cleaned_snippet": "OpenAI on Tuesday unveiled GPT-5, its most advanced language model to date, featuring significant improvements in mathematical reasoning and code generation.",
      "source_reliability": "S",
      "cleaning_actions": [],
      "merged_with": ["https://www.zaobao.com.sg/tech/openai-gpt5", "https://news.cn/tech/openai-gpt5"],
      "original_index": 0
    },
    {
      "id": "ev_002",
      "source_url": "https://www.36kr.com/news/openai-gpt5",
      "title": "36氪独家 | OpenAI发布GPT-5，一文看懂技术亮点",
      "cleaned_snippet": "OpenAI今日正式发布GPT-5。核心亮点包括：1. 数学推理能力提升300% 2. 代码生成准确率达到95% 3. 上下文窗口扩展至500K tokens",
      "source_reliability": "A",
      "cleaning_actions": [],
      "original_index": 5
    }
  ],
  "removed_noise": [
    {
      "id": "noise_001",
      "original_snippet": "AI帮你做菜！GPT-5最强菜谱推荐",
      "removal_reason": "off_topic",
      "noise_category": "irrelevant_content"
    },
    {
      "id": "noise_002",
      "original_snippet": "根据全球人工智能治理委员会（GAIGC）发布的报告...",
      "removal_reason": "pseudo_entity",
      "noise_category": "unverifiable_entity"
    }
  ],
  "downranked_items": [
    {
      "id": "ev_003",
      "original_rank": 2,
      "new_rank": 8,
      "downrank_reason": "aggregated_repost + ad_mixed_content",
      "warning": "百家号内容夹带广告（'XX品牌AI智能音箱限时促销'），性能声称'10倍提升'无法验证"
    },
    {
      "id": "ev_004",
      "original_rank": 3,
      "new_rank": 7,
      "downrank_reason": "unverified_self_media + clickbait_title",
      "warning": "微信公众号未认证，标题党风格"
    }
  ],
  "warnings": [
    "条目5引用'全球人工智能治理委员会（GAIGC）'无法验证存在性，已移除",
    "条目3声称'性能是GPT-4的10倍以上'缺乏可靠来源佐证，已降权"
  ],
  "cleaning_stats": {
    "total_input": 8,
    "kept": 2,
    "removed": 2,
    "downranked": 2,
    "merged": 2,
    "snr_ratio": 0.75
  }
}
```

---

## 用例 2：网页抓取清洗（含 DOM 噪声）

### 场景描述

通过 web_fetch 抓取了一篇科技新闻网页的全文，内容中混入了大量 DOM 噪声。

### 输入

```json
{
  "raw_evidence_items": [
    {
      "source_url": "https://www.techcrunch.com/2024/05/15/apple-ai-strategy",
      "title": "Apple's AI Strategy Revealed at WWDC 2024",
      "raw_text": "TechCrunch\n> Navigation: Home > AI > Apple\n> Topics: AI, Apple, WWDC, Machine Learning\n\n<div class=\"ad-banner\">Subscribe to TechCrunch+ for exclusive AI coverage. Plans start at $10/month.</div>\n\nApple's AI Strategy Revealed at WWDC 2024\n\nBy Sarah Chen | May 15, 2024 at 2:30 PM PST\n\n\n.share-bar { position: fixed; left: 0; bottom: 0; width: 100%; background: #fff; z-index: 999; }\n\nApple today unveiled its comprehensive AI strategy at WWDC 2024, introducing a new framework called 'Apple Intelligence' that integrates generative AI capabilities across its entire product ecosystem.\n\nKey announcements include:\n- On-device AI processing for all iPhone 15 Pro models and later\n- A new Siri powered by large language models\n- Integration with OpenAI's GPT models for complex queries\n\n\"This represents a fundamental shift in how we think about AI on consumer devices,\" said Craig Federighi, Apple's senior vice president of software engineering.\n\nwindow.addEventListener('scroll', function() { trackScrollDepth(); });\n\nIndustry analysts predict this move will significantly impact the competitive landscape of consumer AI.\n\n---\nRelated Articles:\n1. Google's Response to Apple AI\n2. Microsoft Copilot vs Apple Intelligence\n3. The Future of On-Device AI\n\n---\nFooter: About | Careers | Privacy | Terms | © 2024 TechCrunch"
    }
  ],
  "primary_subject": "Apple AI战略",
  "canonical_time_frame": {
    "start": "2024-06-01",
    "end": "2024-06-30",
    "granularity": "day"
  },
  "cleaning_goal": "提取Apple WWDC 2024 AI战略的核心信息"
}
```

### 处理过程

**Step 1 DOM 噪声剥离**：
- 移除导航栏：`> Navigation: Home > AI > Apple > Topics:...`
- 移除广告：`<div class=\"ad-banner\">Subscribe to TechCrunch+...`
- 移除 CSS：`.share-bar { position: fixed;...`
- 移除 JS：`window.addEventListener('scroll',...`
- 移除相关文章：`Related Articles: 1. Google's Response...`
- 移除页脚：`Footer: About | Careers |...`
- 保留元信息：作者 Sarah Chen, 日期 May 15, 2024

**Step 2-4**：内容权威（TechCrunch 一手报道），无伪实体，无重复，保留

**Step 5 标准化**：格式化输出

### 输出

```json
{
  "cleaned_evidence": [
    {
      "id": "ev_001",
      "source_url": "https://www.techcrunch.com/2024/05/15/apple-ai-strategy",
      "title": "Apple's AI Strategy Revealed at WWDC 2024",
      "cleaned_snippet": "Apple today unveiled its comprehensive AI strategy at WWDC 2024, introducing a new framework called 'Apple Intelligence' that integrates generative AI capabilities across its entire product ecosystem. Key announcements include: on-device AI processing for all iPhone 15 Pro models and later; a new Siri powered by large language models; integration with OpenAI's GPT models for complex queries. Craig Federighi, Apple's SVP of software engineering: \"This represents a fundamental shift in how we think about AI on consumer devices.\" Industry analysts predict this move will significantly impact the competitive landscape of consumer AI.",
      "author": "Sarah Chen",
      "publish_date": "2024-05-15",
      "source_reliability": "A",
      "cleaning_actions": [
        "dom_navigation_removed",
        "dom_ad_removed",
        "dom_css_removed",
        "dom_js_removed",
        "dom_related_articles_removed",
        "dom_footer_removed",
        "format_standardized"
      ],
      "original_index": 0
    }
  ],
  "removed_noise": [],
  "downranked_items": [],
  "warnings": [],
  "cleaning_stats": {
    "total_input": 1,
    "kept": 1,
    "removed": 0,
    "downranked": 0,
    "snr_before": 0.35,
    "snr_after": 1.0
  }
}
```

---

## 用例 3：OCR 残片清洗

### 场景描述

从一份扫描版 PDF 中 OCR 提取了关于全球半导体市场的数据，内容包含乱码、残片和格式问题。

### 输入

```json
{
  "raw_evidence_items": [
    {
      "source_url": "file:///reports/semiconductor_report_2024.pdf",
      "title": "2024年全球半导体市场报告（扫描版）",
      "raw_text": "2024年全球半导体市场报告\n\n第一章 市场概况\n\n2024年全球半导体市场规模预计达到$6,120亿美元，同比增长16.8％。\n\n根据国际半导体产业协会(SEMI)数据，...织产能利用率在2024年Q2回升至82％。\n\n注：本段为PDF扫描件OCR提取，部分内容缺失\n\n主要驱动因素：\n1. 人工智能芯片需求暴增，NVIDIA数据巾心GPU出货量同比增氏350％\n2. 汽车电子化转型加速，车规级芯片需求持续旺盛\n3. 5G基站建设拉动通信芯片需求\n\nFigure 1: Global Semiconductor Revenue Forecast\n[图表：2020-2026年全球半导体收入预测]\n（注：图表内容OCR无法提取）\n\n据波士顿咨询集团(BCG)和半导体行业协会(SIA)联合报告，到2030年全球芯片产业规模将突破$1万亿...\n\n第三章 竞争格局\n\nNVIDIA以52.3％的市场份额占据AI加速器市场第一，AMD以18.7％位居第二，英特尔以8.2％排名第三。\n\n值得注意的是，中国本土芯片制造商...（第12页内容缺失）...预计到2027年将达到15％的自给率..."
    }
  ],
  "primary_subject": "全球半导体市场",
  "canonical_time_frame": {
    "start": "2024-01-01",
    "end": "2024-12-31",
    "granularity": "quarter"
  },
  "cleaning_goal": "清洗OCR提取的半导体市场报告数据，保留可用信息"
}
```

### 处理过程

**Step 1 DOM 噪声**：无 DOM 噪声，但含 OCR 特有噪声

**Step 2 伪实体**：
- "国际半导体产业协会(SEMI)" → 已知真实实体 ✓
- "波士顿咨询集团(BCG)" → 已知真实实体 ✓
- "半导体行业协会(SIA)" → 已知真实实体 ✓

**Step 3 去重**：无重复

**Step 4 错域降权**：
- 来源为 PDF 扫描件 → 可能存在 OCR 误差 → 降权 D1
- 部分内容缺失 → 降权 D1

**Step 5 标准化 + OCR 修正**：
- "数据巾心" → "数据中心" [OCR_ERROR_CORRECTED]
- "增氏" → "增长" [OCR_ERROR_CORRECTED]
- 图表无法提取 → 标注 [CHART_NOT_EXTRACTED]
- 缺失页标注 → 标注 [OCR_FRAGMENT]

### 输出

```json
{
  "cleaned_evidence": [
    {
      "id": "ev_001",
      "source_url": "file:///reports/semiconductor_report_2024.pdf",
      "title": "2024年全球半导体市场报告（扫描版）",
      "cleaned_snippet": "[OCR_FRAGMENT] 2024年全球半导体市场规模预计达到6,120亿美元，同比增长16.8%。根据国际半导体产业协会(SEMI)数据，晶圆产能利用率在2024年Q2回升至82%。[OCR_FRAGMENT]\n\n主要驱动因素：\n1. 人工智能芯片需求暴增，NVIDIA数据中心GPU出货量同比增长350%[OCR_ERROR_CORRECTED]\n2. 汽车电子化转型加速，车规级芯片需求持续旺盛\n3. 5G基站建设拉动通信芯片需求\n\n[CHART_NOT_EXTRACTED] Figure 1: 2020-2026年全球半导体收入预测\n\n据波士顿咨询集团(BCG)和半导体行业协会(SIA)联合报告，到2030年全球芯片产业规模将突破1万亿美元。\n\nNVIDIA以52.3%的市场份额占据AI加速器市场第一，AMD以18.7%位居第二，英特尔以8.2%排名第三。[OCR_FRAGMENT]中国本土芯片制造商...预计到2027年将达到15%的自给率[OCR_FRAGMENT]",
      "source_reliability": "B",
      "cleaning_actions": [
        "ocr_error_corrected:数据巾心→数据中心",
        "ocr_error_corrected:增氏→增长",
        "ocr_fragment_marked",
        "chart_not_extracted_marked",
        "html_entity_decoded:$→纯数字"
      ],
      "original_index": 0
    }
  ],
  "removed_noise": [],
  "downranked_items": [
    {
      "id": "ev_001",
      "original_rank": 1,
      "new_rank": 4,
      "downrank_reason": "ocr_source + partial_content_missing",
      "warning": "来源为PDF扫描件OCR提取，存在识别误差和内容缺失，关键数据建议与原始报告交叉验证"
    }
  ],
  "warnings": [
    "OCR修正2处：'数据巾心'→'数据中心'、'增氏'→'增长'",
    "图表内容无法通过OCR提取，可能包含关键数据",
    "报告第12页内容缺失，'中国本土芯片制造商'相关段落不完整"
  ],
  "cleaning_stats": {
    "total_input": 1,
    "kept": 1,
    "removed": 0,
    "downranked": 1,
    "ocr_corrections": 2,
    "ocr_fragments": 3,
    "snr_after": 0.82
  }
}
```
