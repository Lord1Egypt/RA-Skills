# 新鲜度判定用例集

## 用例 1：突发新闻场景（24h 时间窗）

### 场景描述

某科技媒体在 2024-05-15 下午收到消息：OpenAI 发布了 GPT-5。需要从搜索结果中判断哪些是最新的报道。

### 输入

```json
{
  "normalized_evidence": [
    {
      "id": "ev_001",
      "source_url": "https://www.reuters.com/technology/openai-gpt5",
      "title": "OpenAI Announces GPT-5",
      "snippet": "OpenAI on Tuesday unveiled GPT-5, its most advanced language model to date.",
      "publish_date": "2024-05-15T14:30:00Z"
    },
    {
      "id": "ev_002",
      "source_url": "https://techcrunch.com/openai-gpt5-launch",
      "title": "GPT-5 Is Here: Everything You Need to Know",
      "snippet": "OpenAI just dropped GPT-5 and it's a game changer. Here's our full breakdown.",
      "publish_date": "2024-05-15T15:00:00Z"
    },
    {
      "id": "ev_003",
      "source_url": "https://arstechnica.com/ai/openai-gpt4-turbo-update",
      "title": "OpenAI Updates GPT-4 Turbo with Vision Improvements",
      "snippet": "OpenAI today announced an update to GPT-4 Turbo, enhancing its vision capabilities.",
      "publish_date": "2024-05-14T09:00:00Z"
    },
    {
      "id": "ev_004",
      "source_url": "https://www.theverge.com/google-gemini-update",
      "title": "Google Responds to AI Competition with Gemini Update",
      "snippet": "Google has announced a significant update to Gemini ahead of OpenAI's anticipated announcement.",
      "publish_date": "2024-05-13T18:00:00Z"
    },
    {
      "id": "ev_005",
      "source_url": "https://blog.example.com/ai-predictions",
      "title": "What to Expect from OpenAI in 2024",
      "snippet": "Industry analysts predict OpenAI will release a new model sometime this year.",
      "publish_date": "2024-01-20T10:00:00Z"
    },
    {
      "id": "ev_006",
      "source_url": "https://news.example.com/openai-gpt4-anniversary",
      "title": "GPT-4 Turns One: A Year of Transformation",
      "snippet": "It's been exactly one year since GPT-4 was released, and the AI landscape has changed dramatically.",
      "publish_date": "2024-03-14T08:00:00Z"
    },
    {
      "id": "ev_007",
      "source_url": "https://ai-insider.example.com/scoop",
      "title": "AI行业重大变局即将到来",
      "snippet": "据多方知情人士确认，AI行业即将迎来一次重大变局，涉及多家头部公司。",
      "publish_date": null
    },
    {
      "id": "ev_008",
      "source_url": "https://archive.example.com/chatgpt-launch",
      "title": "ChatGPT Launches, AI Goes Mainstream",
      "snippet": "OpenAI's ChatGPT has taken the internet by storm since its launch last week.",
      "publish_date": "2022-12-05T12:00:00Z"
    }
  ],
  "canonical_time_frame": {
    "start": "2024-05-14T14:00:00Z",
    "end": "2024-05-15T14:00:00Z",
    "granularity": "hour"
  },
  "freshness_policy": {
    "conservatism_level": "high",
    "stale_threshold_months": 0.1,
    "undated_handling": "downrank"
  }
}
```

### 处理过程

| 证据 | 日期 | 距时间窗 | 判定 | 理由 |
|------|------|----------|------|------|
| ev_001 | 05-15 14:30 | 在窗内（刚好在窗口结束） | Current | 在时间窗内 |
| ev_002 | 05-15 15:00 | 晚于时间窗结束 | Background | 晚于时间窗30分钟，保守模式 |
| ev_003 | 05-14 09:00 | 早于时间窗开始 | Background | 早于时间窗5小时 |
| ev_004 | 05-13 18:00 | 早于时间窗44小时 | Stale | 超过72h阈值？否，44h < 72h → Background（但接近阈值） |
| ev_005 | 01-20 | 早于时间窗115天 | Stale | 远超阈值 |
| ev_006 | 03-14 | 早于时间窗62天 | Stale | 远超阈值 |
| ev_007 | 无 | — | Undated | 无时间信息 |
| ev_008 | 2022-12-05 | 早于时间窗2.5年 | Stale | 远超阈值 |

### 输出

```json
{
  "current_evidence": [
    {
      "id": "ev_001",
      "publish_date": "2024-05-15T14:30:00Z",
      "freshness": "current",
      "boundary": true,
      "note": "刚好在时间窗结束边界上"
    }
  ],
  "background_evidence": [
    {
      "id": "ev_002",
      "publish_date": "2024-05-15T15:00:00Z",
      "freshness": "background",
      "note": "晚于时间窗30分钟，保守模式降级为background"
    },
    {
      "id": "ev_003",
      "publish_date": "2024-05-14T09:00:00Z",
      "freshness": "background",
      "note": "早于时间窗开始5小时，但内容相关（GPT系列更新）"
    },
    {
      "id": "ev_004",
      "publish_date": "2024-05-13T18:00:00Z",
      "freshness": "background",
      "note": "早于时间窗44小时，未超过stale阈值(72h)，提供竞争对手背景"
    }
  ],
  "stale_evidence": [
    {
      "id": "ev_005",
      "publish_date": "2024-01-20T10:00:00Z",
      "freshness": "stale",
      "note": "4个月前的预测，已被实际发布事件替代"
    },
    {
      "id": "ev_006",
      "publish_date": "2024-03-14T08:00:00Z",
      "freshness": "stale",
      "note": "GPT-4周年回顾，超过2个月前"
    },
    {
      "id": "ev_008",
      "publish_date": "2022-12-05T12:00:00Z",
      "freshness": "stale",
      "note": "ChatGPT发布旧闻，2.5年前"
    }
  ],
  "undated_evidence": [
    {
      "id": "ev_007",
      "publish_date": null,
      "freshness": "undated",
      "note": "无发布日期，无法判断时间新鲜度"
    }
  ],
  "malformed_evidence": [],
  "freshness_profile": {
    "total_evidence": 8,
    "current_ratio": 0.125,
    "background_ratio": 0.375,
    "stale_ratio": 0.375,
    "undated_ratio": 0.125,
    "malformed_ratio": 0.0,
    "time_coverage": {
      "earliest": "2022-12-05",
      "latest": "2024-05-15",
      "median_date": "2024-03-14"
    },
    "overall_assessment": "仅12.5%证据在24h时间窗内，37.5%为背景证据（44小时内），37.5%已过时，12.5%无时间标注。当前有效证据较少，建议补充搜索最新报道。",
    "risk_flags": [
      "仅1条证据（12.5%）在24h时间窗内，证据库时效性偏低",
      "1条证据（ev_007）无时间标注，可能引入误判风险"
    ]
  }
}
```

---

## 用例 2：政策分析场景（90天时间窗）

### 场景描述

需要分析中国AI监管政策的最新动态，时间窗为过去 90 天。

### 输入

```json
{
  "normalized_evidence": [
    {
      "id": "ev_001",
      "title": "网信办发布生成式AI服务备案新规",
      "snippet": "国家网信办2024年5月1日起正式实施生成式人工智能服务备案管理办法修订版，要求所有提供生成式AI服务的平台完成备案。",
      "publish_date": "2024-04-28"
    },
    {
      "id": "ev_002",
      "title": "国务院发布关于加强人工智能伦理治理的指导意见",
      "snippet": "国务院办公厅2024年3月20日发布《关于加强人工智能伦理治理的指导意见》，提出建立AI伦理审查机制。",
      "publish_date": "2024-03-20"
    },
    {
      "id": "ev_003",
      "title": "中国首部生成式AI管理办法实施一年回顾",
      "snippet": "2023年8月15日实施的《生成式人工智能服务管理暂行办法》已满一年，业界普遍认为监管框架初见成效。",
      "publish_date": "2024-08-15"
    },
    {
      "id": "ev_004",
      "title": "工信部发布AI芯片产业支持政策",
      "snippet": "工业和信息化部发布《关于促进人工智能芯片产业高质量发展的若干措施》，加大财税支持力度。",
      "publish_date": "2024-02-10"
    },
    {
      "id": "ev_005",
      "title": "深度合成管理规定实施效果评估报告",
      "snippet": "中国信息通信研究院发布《深度合成管理规定实施效果评估报告》，报告显示该规定有效遏制了深度伪造滥用。",
      "publish_date": "2023-12-20"
    },
    {
      "id": "ev_006",
      "title": "全国人大常委会审议AI立法草案",
      "snippet": "据全国人大常委会消息，人工智能法草案已列入2024年度立法工作计划，预计年内完成一审。",
      "publish_date": null
    },
    {
      "id": "ev_007",
      "title": "全球AI治理合作倡议",
      "snippet": "2023年10月，中国发布《全球人工智能治理倡议》，提出以人为本、智能向善的AI发展原则。",
      "publish_date": "2023-10-18"
    }
  ],
  "canonical_time_frame": {
    "start": "2024-02-15",
    "end": "2024-05-15",
    "granularity": "day"
  },
  "freshness_policy": {
    "conservatism_level": "standard",
    "stale_threshold_months": 6,
    "undated_handling": "flag_only"
  }
}
```

### 处理过程

| 证据 | 日期 | 判定 | 理由 |
|------|------|------|------|
| ev_001 | 2024-04-28 | Current | 在90天窗内 |
| ev_002 | 2024-03-20 | Current | 在90天窗内 |
| ev_003 | 2024-08-15 | Malformed | 日期在未来（假设当前为2024-05-15） |
| ev_004 | 2024-02-10 | Background | 早于时间窗5天，但标准模式可考虑为Current（刚出窗），保守标记Background |
| ev_005 | 2023-12-20 | Background | 窗外但<6个月，政策评估报告仍有参考价值 |
| ev_006 | 无 | Undated | 无发布日期 |
| ev_007 | 2023-10-18 | Background | 窗外但<6个月，政策文件仍有效 |

### 输出

```json
{
  "current_evidence": [
    {
      "id": "ev_001",
      "publish_date": "2024-04-28",
      "freshness": "current",
      "note": "新规将于5月1日实施，在时间窗内"
    },
    {
      "id": "ev_002",
      "publish_date": "2024-03-20",
      "freshness": "current",
      "note": "国务院新政策，在时间窗内"
    }
  ],
  "background_evidence": [
    {
      "id": "ev_004",
      "publish_date": "2024-02-10",
      "freshness": "background",
      "note": "工信部政策，早于时间窗5天，但仍为最新版本且有效"
    },
    {
      "id": "ev_005",
      "publish_date": "2023-12-20",
      "freshness": "background",
      "note": "评估报告，发布于5个月前，<6个月stale阈值，仍有参考价值"
    },
    {
      "id": "ev_007",
      "publish_date": "2023-10-18",
      "freshness": "background",
      "note": "国际治理倡议，7个月前发布，<6个月？否，7个月 → 超出stale阈值，但政策文件仍有效，降级为Background而非Stale"
    }
  ],
  "stale_evidence": [],
  "undated_evidence": [
    {
      "id": "ev_006",
      "publish_date": null,
      "freshness": "undated",
      "note": "提及'2024年度立法工作计划'，可推断为2024年内容，但无精确日期，flag_only模式仅标记"
    }
  ],
  "malformed_evidence": [
    {
      "id": "ev_003",
      "publish_date": "2024-08-15",
      "freshness": "malformed",
      "note": "日期2024-08-15在未来（当前为2024-05-15），可能为数据错误或预发布内容"
    }
  ],
  "freshness_profile": {
    "total_evidence": 7,
    "current_ratio": 0.286,
    "background_ratio": 0.429,
    "stale_ratio": 0.0,
    "undated_ratio": 0.143,
    "malformed_ratio": 0.143,
    "time_coverage": {
      "earliest": "2023-10-18",
      "latest": "2024-08-15",
      "median_date": "2024-03-20"
    },
    "overall_assessment": "28.6%证据在90天时间窗内，42.9%为有效背景证据（政策文件仍有效），14.3%无时间标注，14.3%日期异常。整体时效性尚可，但建议验证ev_003的日期并补充ev_006的精确时间。",
    "risk_flags": [
      "ev_003日期(2024-08-15)在未来，需验证数据正确性",
      "ev_006无精确发布日期，无法确定时效性"
    ]
  }
}
```

---

## 用例 3：技术调研场景（6个月时间窗，含 undated 和 malformed 案例）

### 场景描述

需要调研 2024 年上半年的大语言模型技术发展动态。时间窗为 6 个月（2023-11-15 ~ 2024-05-15）。

### 输入

```json
{
  "normalized_evidence": [
    {
      "id": "ev_001",
      "title": "OpenAI发布GPT-5：多模态推理新纪元",
      "snippet": "2024年5月15日，OpenAI正式发布GPT-5，实现了文本、图像、音频、视频的统一理解与生成，上下文窗口扩展至500K tokens。",
      "publish_date": "2024-05-15"
    },
    {
      "id": "ev_002",
      "title": "Anthropic Claude 3发布：超越GPT-4的推理能力",
      "snippet": "2024年3月4日，Anthropic发布Claude 3系列模型（Haiku/Sonnet/Opus），其中Opus在多项基准测试中首次全面超越GPT-4。",
      "publish_date": "2024-03-04"
    },
    {
      "id": "ev_003",
      "title": "Google Gemini Ultra正式上线",
      "snippet": "Google宣布Gemini Ultra已全面开放API访问，据Google称其在MMLU基准上得分达到90.0%。",
      "publish_date": "2024-02-01"
    },
    {
      "id": "ev_004",
      "title": "Meta开源Llama 3系列模型",
      "snippet": "Meta发布了Llama 3的8B和70B参数版本，开源许可允许商用。Llama 3 70B在多项基准上接近GPT-4水平。",
      "publish_date": "2024-04-18"
    },
    {
      "id": "ev_005",
      "title": "Mistral AI发布Mistral Large",
      "snippet": "法国AI公司Mistral AI发布了其旗舰模型Mistral Large，在多语言能力和代码生成方面表现优异。",
      "publish_date": "2024-02-26"
    },
    {
      "id": "ev_006",
      "title": "国内某科技公司发布大语言模型",
      "snippet": "据内部消息，国内一家头部科技公司即将发布新一代大语言模型，据称性能可与国际顶尖模型媲美。",
      "publish_date": null
    },
    {
      "id": "ev_007",
      "title": "阿里巴巴Qwen 2.5系列发布",
      "snippet": "阿里巴巴达摩院发布了通义千问2.5系列，包含多个尺寸的模型，在中文理解任务上表现突出。",
      "publish_date": "2024-03-11"
    },
    {
      "id": "ev_008",
      "title": "Stability AI发布Stable Diffusion 4",
      "snippet": "Stability AI宣布了Stable Diffusion 4，据称在图像生成质量方面实现了质的飞跃。",
      "publish_date": "2024-11-30"
    },
    {
      "id": "ev_009",
      "title": "OpenAI发布GPT-4 Turbo更新",
      "snippet": "2023年11月6日，OpenAI在首届开发者大会上发布了GPT-4 Turbo，支持128K上下文窗口，并降低了API价格。",
      "publish_date": "2023-11-06"
    },
    {
      "id": "ev_010",
      "title": "Transformer架构：Attention Is All You Need的后续影响",
      "snippet": "自2017年Transformer架构提出以来，它已成为自然语言处理和计算机视觉领域的基础架构，影响了GPT、BERT、ViT等众多模型的设计。",
      "publish_date": "2023-06-15"
    },
    {
      "id": "ev_011",
      "title": "百度发布文心大模型4.5",
      "snippet": "百度发布了文心大模型4.5版本，在逻辑推理和代码生成方面有显著提升。",
      "publish_date": "2024-30-01"
    },
    {
      "id": "ev_012",
      "title": "据报道OpenAI正在训练GPT-6",
      "snippet": "多家媒体报道称OpenAI已经开始训练下一代模型GPT-6，预计将在2025年发布。但OpenAI官方尚未确认此消息。",
      "publish_date": "2024-05-10"
    }
  ],
  "canonical_time_frame": {
    "start": "2023-11-15",
    "end": "2024-05-15",
    "granularity": "month"
  },
  "freshness_policy": {
    "conservatism_level": "lenient",
    "stale_threshold_months": 18,
    "undated_handling": "downrank"
  }
}
```

### 处理过程

| 证据 | 日期 | 判定 | 理由 |
|------|------|------|------|
| ev_001 | 2024-05-15 | Current | 在窗内 |
| ev_002 | 2024-03-04 | Current | 在窗内 |
| ev_003 | 2024-02-01 | Current | 在窗内 |
| ev_004 | 2024-04-18 | Current | 在窗内 |
| ev_005 | 2024-02-26 | Current | 在窗内 |
| ev_006 | 无 | Undated | 无发布日期，仅有模糊"即将发布" |
| ev_007 | 2024-03-11 | Current | 在窗内 |
| ev_008 | 2024-11-30 | Malformed | 日期在未来（当前2024-05-15） |
| ev_009 | 2023-11-06 | Background | 早于时间窗9天，但为重要里程碑，宽松模式可考虑Current；保守标记Background |
| ev_010 | 2023-06-15 | Background | 11个月前，<18个月stale阈值，基础技术文章 |
| ev_011 | 2024-30-01 | Malformed | 日期格式错误（1月只有31天，30日有效但"2024-30-01"格式非标准——实际2024年1月30日应为2024-01-30） |
| ev_012 | 2024-05-10 | Current | 在窗内，但内容为未经确认的传闻 |

### 输出

```json
{
  "current_evidence": [
    {
      "id": "ev_001",
      "publish_date": "2024-05-15",
      "freshness": "current"
    },
    {
      "id": "ev_002",
      "publish_date": "2024-03-04",
      "freshness": "current"
    },
    {
      "id": "ev_003",
      "publish_date": "2024-02-01",
      "freshness": "current"
    },
    {
      "id": "ev_004",
      "publish_date": "2024-04-18",
      "freshness": "current"
    },
    {
      "id": "ev_005",
      "publish_date": "2024-02-26",
      "freshness": "current"
    },
    {
      "id": "ev_007",
      "publish_date": "2024-03-11",
      "freshness": "current"
    },
    {
      "id": "ev_012",
      "publish_date": "2024-05-10",
      "freshness": "current",
      "warning": "内容为未经官方确认的传闻，需谨慎引用"
    }
  ],
  "background_evidence": [
    {
      "id": "ev_009",
      "publish_date": "2023-11-06",
      "freshness": "background",
      "note": "GPT-4 Turbo发布，早于时间窗9天，但为重要技术里程碑，仍有参考价值"
    },
    {
      "id": "ev_010",
      "publish_date": "2023-06-15",
      "freshness": "background",
      "note": "Transformer基础架构文章，11个月前发布，<18个月阈值，技术背景知识"
    }
  ],
  "stale_evidence": [],
  "undated_evidence": [
    {
      "id": "ev_006",
      "publish_date": null,
      "freshness": "undated",
      "note": "仅有'即将发布'模糊时间，无法定位具体时间，建议降权处理"
    }
  ],
  "malformed_evidence": [
    {
      "id": "ev_008",
      "publish_date": "2024-11-30",
      "freshness": "malformed",
      "note": "日期2024-11-30在未来（当前为2024-05-15），可能为错误数据或预发布内容"
    },
    {
      "id": "ev_011",
      "publish_date": "2024-30-01",
      "freshness": "malformed",
      "note": "日期格式错误：'2024-30-01'非标准ISO格式，尝试解析为2024-01-30后重新判定（在窗内→Current），但原始格式损坏，标记为malformed"
    }
  ],
  "freshness_profile": {
    "total_evidence": 12,
    "current_ratio": 0.583,
    "background_ratio": 0.167,
    "stale_ratio": 0.0,
    "undated_ratio": 0.083,
    "malformed_ratio": 0.167,
    "time_coverage": {
      "earliest": "2023-06-15",
      "latest": "2024-11-30",
      "median_date": "2024-03-04"
    },
    "overall_assessment": "58.3%证据在6个月时间窗内（7条），时效性良好。16.7%为有效背景证据（2条），8.3%无时间标注（1条），16.7%日期异常（2条需人工验证）。总体证据库时效性较强，但需处理日期异常问题。",
    "risk_flags": [
      "ev_008日期在未来(2024-11-30)，需验证数据正确性",
      "ev_011日期格式损坏(2024-30-01)，需人工修正后重新判定",
      "ev_006无时间标注(8.3%)，内容为未经确认的传闻",
      "ev_012内容为未经官方确认的传闻，虽在时间窗内但可靠性存疑"
    ]
  }
}
```
