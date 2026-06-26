# 反证搜索完整用例

## 用例 1: 战略判断反证

**场景**: 某投资研究团队判断"印度GDP将在2026年超越日本成为全球第三大经济体"

### 输入

```json
{
  "mainline_claim": "印度GDP将在2026年超越日本成为全球第三大经济体",
  "primary_subject": "印度经济",
  "canonical_time_frame": "2024-2026",
  "search_results": null,
  "counter_goal": "寻找可能导致印度GDP增长不及预期、或日本GDP意外表现优于预期的反证"
}
```

### 输出

```json
{
  "counter_queries": [
    {
      "query": "印度2024-2025年GDP增速实际数据 vs IMF预测偏差",
      "rationale": "主线可能基于乐观预测而非实际数据，需验证预测兑现率",
      "expected_counter_type": "量级质疑"
    },
    {
      "query": "日元汇率对日本GDP（美元计价）的影响",
      "rationale": "如果日元大幅升值，日本以美元计价的GDP将显著增加，可能推迟被超越的时间",
      "expected_counter_type": "条件反转"
    },
    {
      "query": "印度结构性经济问题：就业率、制造业占比、基础设施瓶颈",
      "rationale": "高GDP增长可能掩盖结构问题，若结构问题爆发将限制增长持续性",
      "expected_counter_type": "因果替代"
    },
    {
      "query": "IMF/世界银行对印度GDP统计方法的质疑",
      "rationale": "印度GDP统计方法曾受到学术质疑，若存在系统性高估则结论不成立",
      "expected_counter_type": "样本偏差"
    }
  ],
  "counter_evidence": [
    {
      "content": "IMF 2025年4月WEO将印度2025年增速预期从6.8%下调至6.5%，2026年从6.5%下调至6.2%，主要因全球贸易不确定性",
      "source": "IMF World Economic Outlook, April 2025",
      "strength": "soft",
      "counter_type": "量级质疑",
      "rebuttal_to": "印度GDP增速足以支撑超越日本"
    },
    {
      "content": "若日元/美元汇率从160回升至130（日本央行加息预期），日本名义GDP（美元计）将增加约18%，从4.2万亿增至约5.0万亿美元",
      "source": "彭博经济学计算，基于日本内阁府数据",
      "strength": "soft",
      "counter_type": "条件反转",
      "rebuttal_to": "日本GDP停滞不前，将被超越"
    },
    {
      "content": "印度制造业占GDP比重从2015年的15.6%降至2024年的14.3%，与'印度制造'目标（25%）背道而驰",
      "source": "印度中央统计局，世界银行",
      "strength": "hard",
      "counter_type": "因果替代",
      "rebuttal_to": "印度经济结构正在健康转型"
    },
    {
      "content": "印度劳动力参与率（尤其是女性）持续低迷，2024年约为40%，远低于中国的67%和日本的60%",
      "source": "世界银行，ILO",
      "strength": "soft",
      "counter_type": "因果替代",
      "rebuttal_to": "印度人口红利将支撑持续高增长"
    },
    {
      "content": "某自媒体称'印度经济数据造假'，但未提供具体证据，仅引用匿名来源",
      "source": "不可追溯自媒体文章",
      "strength": "noise",
      "counter_type": "无",
      "rebuttal_to": "无"
    }
  ],
  "flip_conditions": [
    {
      "condition": "日元在2025-2026年因日本央行激进加息而大幅升值（USD/JPY < 130）",
      "probability": "medium",
      "impact_if_triggered": "日本以美元计价GDP将回升至4.8-5.0万亿美元，显著推迟被印度超越的时间（可能推迟至2028年）",
      "time_horizon": "2025 Q3 - 2026 Q4"
    },
    {
      "condition": "印度经济增速因全球贸易战影响跌至5%以下",
      "probability": "low-medium",
      "impact_if_triggered": "超越时间将推迟1-3年，且'超越'本身的意义将被质疑（只是增速放缓而非日本表现好转）",
      "time_horizon": "2025 Q4 - 2026 Q4"
    },
    {
      "condition": "印度发生系统性金融风险（如NBFC危机2.0）",
      "probability": "low",
      "impact_if_triggered": "短期GDP可能大幅下修1-2个百分点，'超越日本'的叙事将被完全推翻",
      "time_horizon": "不确定"
    }
  ],
  "alternative_supports": [
    {
      "alternative_path": "超越的驱动力不是印度实力增强，而是日元贬值导致的日本GDP（美元计价）萎缩",
      "supporting_evidence": [
        "2022-2024年日元贬值约30%，日本名义GDP从5.1万亿缩水至约4.2万亿美元",
        "印度同期GDP（美元计价）增长约20%，主要由汇率因素贡献"
      ],
      "compatibility_with_mainline": "qualifies"
    },
    {
      "alternative_path": "即使超越日本，印度的GDP质量（人均GDP、经济结构）仍远落后",
      "supporting_evidence": [
        "印度人均GDP约$2,500 vs 日本$33,000",
        "印度服务业占比过高，制造业空心化风险"
      ],
      "compatibility_with_mainline": "extends"
    }
  ],
  "confidence_assessment": {
    "mainline_robustness": "medium",
    "blind_spots": [
      "未考虑汇率波动对GDP排名的非线性影响",
      "未评估印度GDP统计方法与日本的可比性",
      "缺乏对印度经济结构质量的深度分析"
    ],
    "search_coverage": "adequate"
  }
}
```

---

## 用例 2: 技术评估反证

**场景**: 技术架构评估，某团队主张"Next.js是构建大型企业级SaaS的最优框架选择"

### 输入

```json
{
  "mainline_claim": "Next.js是构建大型企业级SaaS应用的最优前端框架选择",
  "primary_subject": "Next.js框架",
  "canonical_time_frame": "2024-2025",
  "search_results": null,
  "counter_goal": "寻找Next.js在企业级SaaS场景下的局限性、替代方案的比较优势、以及可能导致选型结论翻转的条件"
}
```

### 输出

```json
{
  "counter_queries": [
    {
      "query": "Next.js App Router在生产环境中的已知问题和社区抱怨",
      "rationale": "Next.js 13+引入的App Router架构变动较大，生产环境可能存在未暴露的问题",
      "expected_counter_type": "直接反驳"
    },
    {
      "query": "Remix/Nuxt/Astro vs Next.js在大型SaaS场景的对比评估",
      "rationale": "替代框架可能在特定维度（性能、DX、可维护性）具有优势",
      "expected_counter_type": "因果替代"
    },
    {
      "query": "Next.js Vercel商业绑定和vendor lock-in风险评估",
      "rationale": "Next.js与Vercel平台的深度绑定可能构成企业风险",
      "expected_counter_type": "条件反转"
    },
    {
      "query": "企业级SaaS选择非Next.js框架的成功案例",
      "rationale": "如果头部SaaS公司选择了其他框架并成功运营，说明Next.js并非唯一最优解",
      "expected_counter_type": "样本偏差"
    }
  ],
  "counter_evidence": [
    {
      "content": "Next.js App Router的Server Actions在复杂表单场景存在水合(hydration)不匹配问题，且缓存策略( ISR/SSR )的配置复杂度高，多位资深开发者公开抱怨生产调试困难",
      "source": "GitHub Issues (vercel/next.js), 多位Twitter/X开发者反馈",
      "strength": "soft",
      "counter_type": "直接反驳",
      "rebuttal_to": "Next.js提供最佳的开发体验和稳定性"
    },
    {
      "content": "Remix的嵌套路由和数据加载模型在多步骤业务流程（如订单流程、审批链）中，天然比Next.js的并行路由更清晰",
      "source": "Remix官方文档对比, Shopify团队博客",
      "strength": "soft",
      "counter_type": "因果替代",
      "rebuttal_to": "Next.js的路由架构最适合企业SaaS"
    },
    {
      "content": "Vercel在2024年调整免费tier政策，将Serverless Function执行时间限制收紧，自托管Next.js的配置复杂度显著增加",
      "source": "Vercel官方博客, Hacker News讨论",
      "strength": "hard",
      "counter_type": "条件反转",
      "rebuttal_to": "Next.js的部署生态完全开放且低成本"
    },
    {
      "content": "Linear、Notion、Figma均使用自研或非Next.js方案构建其核心产品界面",
      "source": "各公司技术博客和Stack Share",
      "strength": "soft",
      "counter_type": "样本偏差",
      "rebuttal_to": "顶级SaaS产品都选择Next.js"
    },
    {
      "content": "某Reddit用户称'Next.js是垃圾'但未提供具体技术论据",
      "source": "Reddit r/webdev",
      "strength": "noise",
      "counter_type": "无",
      "rebuttal_to": "无"
    }
  ],
  "flip_conditions": [
    {
      "condition": "Vercel被收购或改变Next.js的开源协议（如转为SSPL）",
      "probability": "low",
      "impact_if_triggered": "企业级SaaS将被迫迁移框架，'最优选择'结论完全失效",
      "time_horizon": "不确定"
    },
    {
      "condition": "React Server Components的行业标准被替代方案取代（如Qwik的resumability范式成为主流）",
      "probability": "low",
      "impact_if_triggered": "Next.js的技术基础被动摇，长期竞争力下降",
      "time_horizon": "2026-2028"
    },
    {
      "condition": "企业需要非Web平台客户端（桌面/移动原生）的统一架构",
      "probability": "medium",
      "impact_if_triggered": "React Native + Expo或Electron + Tauri方案可能比Next.js更优，结论需限定为'仅Web端'",
      "time_horizon": "即时"
    }
  ],
  "alternative_supports": [
    {
      "alternative_path": "Astro + 独立交互框架（如Svelte/HTMX）适合内容密集型SaaS",
      "supporting_evidence": [
        "Astro的Islands Architecture在内容+交互混合场景中性能显著优于纯SPA",
        "多个内容管理SaaS已迁移至Astro并报告LCP提升40%"
      ],
      "compatibility_with_mainline": "qualifies"
    },
    {
      "alternative_path": "微前端架构（Module Federation + 多框架）适合大型企业SaaS的渐进式迁移",
      "supporting_evidence": [
        "多家大型SaaS（如AWS Console）采用微前端实现多团队并行开发",
        "避免了单框架绑定的风险"
      ],
      "compatibility_with_mainline": "contradicts"
    }
  ],
  "confidence_assessment": {
    "mainline_robustness": "medium",
    "blind_spots": [
      "未评估具体业务场景（如低延迟交易、离线优先）对框架选择的约束",
      "未考虑团队技术栈现有积累（切换成本）",
      "缺乏性能基准测试数据支撑'最优'的量化定义"
    ],
    "search_coverage": "adequate"
  }
}
```

---

## 用例 3: 政策影响反证

**场景**: 某研究机构判断"美国对华AI芯片出口管制将导致中国AI产业在3年内严重落后"

### 输入

```json
{
  "mainline_claim": "美国对华AI芯片出口管制将导致中国AI产业在3年内严重落后于西方",
  "primary_subject": "中国AI产业",
  "canonical_time_frame": "2024-2027",
  "search_results": null,
  "counter_goal": "寻找中国AI产业的自主替代进展、管制规避路径、以及可能导致'严重落后'结论失效的因素"
}
```

### 输出

```json
{
  "counter_queries": [
    {
      "query": "中国国产AI芯片（华为昇腾910B、寒武纪思元370等）性能实测与国际竞品对比",
      "rationale": "如果国产芯片性能差距在快速缩小，管制的实际影响将被削弱",
      "expected_counter_type": "直接反驳"
    },
    {
      "query": "中国通过第三国转口获取高端GPU的规模和效果",
      "rationale": "管制可能存在执行漏洞，通过东南亚/中东的转口贸易使实际供应量大于预期",
      "expected_counter_type": "条件反转"
    },
    {
      "query": "算法效率和模型架构创新对算力需求的替代效应",
      "rationale": "如果中国团队在算法效率上取得突破，可以部分弥补硬件差距",
      "expected_counter_type": "因果替代"
    },
    {
      "query": "中国AI产业在应用层（非基础模型训练）的表现和竞争力",
      "rationale": "管制主要影响大模型训练，如果应用层创新不受影响，'整体落后'的结论需要限定范围",
      "expected_counter_type": "量级质疑"
    }
  ],
  "counter_evidence": [
    {
      "content": "华为昇腾910B在大模型推理场景的性能已达到NVIDIA A100的80-90%，且有大量企业开始部署昇腾集群替代NVIDIA方案",
      "source": "华为官方技术白皮书，多个中国云服务商实测报告",
      "strength": "hard",
      "counter_type": "直接反驳",
      "rebuttal_to": "中国缺乏可用的AI算力基础设施"
    },
    {
      "content": "2024年中国通过马来西亚、迪拜等地的转口贸易获取的NVIDIA H100数量估计为实际出口量的15-25%，实际到货量远超公开许可数据",
      "source": "半导体供应链追踪机构（TechInsights）、路透社调查报道",
      "strength": "soft",
      "counter_type": "条件反转",
      "rebuttal_to": "管制完全阻断了中国获取高端GPU的途径"
    },
    {
      "content": "DeepSeek-V2/R1采用MoE架构和混合精度训练，以H800集群训练出与GPT-4级别相当的大模型，训练成本仅为西方同类模型的1/10",
      "source": "DeepSeek技术报告，多篇同行评审分析论文",
      "strength": "hard",
      "counter_type": "因果替代",
      "rebuttal_to": "算力限制将直接导致模型能力落后"
    },
    {
      "content": "中国AI应用层（如电商推荐、短视频算法、自动驾驶）已处于全球领先水平，不依赖最先进的通用大模型",
      "source": "McKinsey中国AI报告，斯坦福AI Index 2025",
      "strength": "soft",
      "counter_type": "量级质疑",
      "rebuttal_to": "中国AI产业将'整体'严重落后"
    },
    {
      "content": "部分观点认为'管制无效'但未区分训练和推理场景的差异",
      "source": "技术论坛讨论",
      "strength": "noise",
      "counter_type": "无",
      "rebuttal_to": "无"
    }
  ],
  "flip_conditions": [
    {
      "condition": "华为昇腾芯片在2025-2026年实现7nm等效制程的自产，且集群规模突破10万卡",
      "probability": "medium",
      "impact_if_triggered": "中国将建立独立于NVIDIA的AI算力生态，'严重落后'结论方向反转",
      "time_horizon": "2025 Q4 - 2027"
    },
    {
      "condition": "美国进一步收紧管制至消费级GPU（如RTX 4090级别全面禁运）",
      "probability": "low-medium",
      "impact_if_triggered": "即使算法创新存在，缺乏任何高端GPU将严重限制实验和迭代速度",
      "time_horizon": "2025-2026"
    },
    {
      "condition": "中国大模型在算法效率上持续突破（如MoE+蒸馏+量化范式成为主流），算力需求降低5-10倍",
      "probability": "medium",
      "impact_if_triggered": "硬件差距对实际能力差距的影响将大幅缩小，'严重落后'退行为'略有差距'",
      "time_horizon": "2025-2027"
    }
  ],
  "alternative_supports": [
    {
      "alternative_path": "中国AI产业的竞争优势从基础模型训练转向应用落地和数据优势",
      "supporting_evidence": [
        "中国拥有全球最大的互联网用户基础和数据生态",
        "中国AI应用（视频生成、语音合成、推荐系统）的用户体验已领先",
        "开源模型生态（Qwen、DeepSeek、Baichuan）的活跃度全球第二"
      ],
      "compatibility_with_mainline": "qualifies"
    },
    {
      "alternative_path": "管制反而加速了中国芯片自主化的进程（类似制裁倒逼效果）",
      "supporting_evidence": [
        "中芯国际2024年14nm产能大幅扩张",
        "华为自研EDA工具链取得突破",
        "中国政府加大对半导体产业的投资（大基金三期3000亿元）"
      ],
      "compatibility_with_mainline": "contradicts"
    }
  ],
  "confidence_assessment": {
    "mainline_robustness": "low",
    "blind_spots": [
      "未充分评估中国在特定AI子领域（如具身智能、自动驾驶）的独立进展",
      "未考虑开源生态对算力差距的弥补作用",
      "未量化'严重落后'的判断标准（是在基础模型、应用层、还是商业化层面？）",
      "未考虑地缘政治变量（如中美关系缓和可能导致管制松动）"
    ],
    "search_coverage": "adequate"
  }
}
```
