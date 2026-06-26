# Daily News Brief

## Purpose
每日定时抓取、处理和推送新闻资讯的 skill。支持全量模式和重点领域模式，自动去重、分类、排序和改写新闻，输出结构化的日报。

## Capabilities
- 定时抓取多个新闻源（财联社、IT之家、36氪等）
- 智能去重：URL去重、标题规范化去重、多源事件优先级去重
- 显式规则分类：政策类、上市公司、非上市公司/产业动态
- 一句话新闻改写：保留关键数据，行业研报级表达
- 智能排序：按分类优先级、主题相关性、数据完整性、时间新鲜度
- 支持全量模式和重点领域监控模式
- Markdown格式输出，支持Telegram推送

## Configuration
### config/default.json
```json
{
  "mode": "all", // "all" 或 "focused"
  "focus_topics": ["robot", "real_estate", "ai"],
  "sources": {
    "primary": ["cls", "ithome", "36kr"],
    "backup": ["jiemian", "yicai", "zqrb", "xinhua", "ssnews", "mnjs", "gov"]
  },
  "schedule": ["08:00", "17:30", "22:30"],
  "max_items": 15,
  "include_links": true,
  "timezone": "Asia/Shanghai",
  "include_keywords": [],
  "exclude_keywords": ["广告", "推广", "营销"]
}
```

## Source Retention Rules
1. 同一事件多来源时优先保留财联社
2. 如果没有财联社，则保留信息最完整、关键数据最全的一条
3. 最终日报里同一事件只保留一条

## Classification Rules
### 政策类
标题或正文出现这些关键词时优先归为政策：
- 政府、政策、国务院、发改委、工信部、证监会、财政部、商务部
- 标准、规划、指导意见、通知、方案、办法、条例

### 上市公司
标题或正文里出现股票代码或明确识别为上市公司：
- （603xxx.SH）、（000xxx.SZ）、（688xxx.SH）、（xxxx.HK）

### 非上市公司 / 产业动态
不属于政策类，也不属于上市公司时归到这里

## Processing Pipeline
```
定时触发 → 配置加载 → 新闻源抓取 → 数据标准化 → 去重 → 过滤 → 分类 → 改写 → 排序 → 截取 → 输出 → 推送
```

## Fixed Rewrite Prompt
```typescript
const REWRITE_PROMPT = `请将我提供的新闻按照以下规则改写成"一句话新闻"：

1. 结构要求：
   * 用 1–2 句完成整条新闻。
   * 主题要明确，突出核心事件（如发布、布局、出货、融资、合作、产品突破等）。

2. 内容要求：
   * 必须保留所有关键数据（如营收、出货量、占比、市场份额、融资金额、注册资本等）。
   * 保持文字简洁、行业研报级表达。

3. 风格要求：
   * 参考以下格式风格：
   "【公司名】关键动作 + 场景落地/战略意义；关键数据（出货/市占率/营收/利润等）。"

同时要遵守：
- 不编造数字
- 不增加无依据判断
- 公司名、政策名、股票代码、技术术语必须保留准确`;
```

## Output Format
```markdown
# 每日日报｜YYYY-MM-DD HH:mm

## 一、政策
- 【机构名】关键动作 + 场景落地/战略意义；关键数据（出货/市占率/营收/利润等）。
- 【机构名】关键动作 + 场景落地/战略意义；关键数据（出货/市占率/营收/利润等）。

## 二、上市公司
- 【公司名】关键动作 + 场景落地/战略意义；关键数据（出货/市占率/营收/利润等）。
- 【公司名】关键动作 + 场景落地/战略意义；关键数据（出货/市占率/营收/利润等）。

## 三、非上市公司 / 产业动态
- 【公司名/机构名】关键动作 + 场景落地/战略意义；关键数据（出货/市占率/营收/利润等）。
- 【公司名/机构名】关键动作 + 场景落地/战略意义；关键数据（出货/市占率/营收/利润等）。
```

## Manual Triggers
- `daily-news-brief run` - 立即执行一次
- `daily-news-brief test` - 测试模式运行（不发送推送）
- `daily-news-brief config` - 查看当前配置

## Implementation Requirements
1. **Source Fetchers**: 每个fetcher输出统一结构 {title, source, published_at, url, summary, full_text}
2. **Normalizer**: 统一不同来源的数据格式
3. **Deduper**: URL去重 + 标题规范化去重 + 语义相似去重预留
4. **Classifier**: 显式规则分类，避免复杂NLP
5. **Rewriter**: 固定prompt，先写占位函数
6. **Ranker**: 按分类优先级、主题相关性、数据完整性、时间新鲜度排序
7. **Scheduler**: 支持Asia/Shanghai时区的三个定时任务
8. **Deliverer**: Telegram发送函数