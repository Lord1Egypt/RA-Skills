# Cailianpress Unified

统一的财联社（CLS）数据技能。该技能为整个工作区提供单一、稳定、可审计的财联社数据访问入口，避免不同脚本、任务、报告各自调用不同 CLS 接口而导致口径漂移。

## 核心目标

- 统一财联社电报数据入口
- 统一加红、热度、详情字段解释
- 为其他技能提供稳定的可复用接口
- 将“原始抓取”与“展示格式”解耦
- 让整个系统以后只维护一个 CLS 真相源

## V1 能力边界

### 包含
- 普通电报查询
- 加红电报查询
- 热度电报查询
- 基础文章详情补全
- 页面兜底抓取

### 不包含
- 财联社深度稿件体系的完整解析
- 登录态内容或会员专享内容
- 评论、互动、专栏系统
- 专题页、热榜页、板块页的完整统一

## 统一数据源

### 主源
- `https://www.cls.cn/nodeapi/telegraphList`

### 详情源
- `https://api3.cls.cn/share/article/{id}`

### 兜底源
- `https://www.cls.cn/telegraph`

## 统一规则

基于当前工作区实测，V1 采用以下规则：
- `level in {"A", "B"}` → 视为加红
- `level == "C"` → 普通电报
- `reading_num` → 热度字段
- `ctime` → 原始发布时间戳
- `shareurl` → 文章分享链接

## 对外接口

### CLI

```bash
python3 skills/cailianpress-unified/scripts/cls_query.py telegraph --hours 1
python3 skills/cailianpress-unified/scripts/cls_query.py telegraph --hours 24
python3 skills/cailianpress-unified/scripts/cls_query.py red --hours 24
python3 skills/cailianpress-unified/scripts/cls_query.py hot --hours 1 --min-reading 10000
python3 skills/cailianpress-unified/scripts/cls_query.py article --id 2326490
```

### 服务层

推荐供其他 Python 技能调用：
- `scripts/cls_service.py`

## 输出格式

支持：
- `json`
- `text`
- `markdown`

## 目录结构

```text
skills/cailianpress-unified/
├── README.md
├── SKILL.md
├── CHANGELOG.md
├── docs/
│   └── api_contract.md
├── scripts/
│   ├── cls_query.py
│   ├── cls_service.py
│   ├── adapters/
│   │   ├── article_share.py
│   │   ├── telegraph_nodeapi.py
│   │   └── telegraph_page_fallback.py
│   ├── formatters/
│   │   ├── json_formatter.py
│   │   ├── markdown_formatter.py
│   │   └── text_formatter.py
│   └── models/
│       └── schemas.py
└── tests/
```

## 使用纪律

### 应该做
- 把本技能视为唯一公开 CLS 入口
- 保留原始字段，确保结果可审计
- 统一通过 schema 输出给下游

### 不应该做
- 不要在别的技能里直接请求 CLS 接口
- 不要再把页面热榜、加红、本地缓存、普通电报混为一谈
- 不要用临时脚本绕过这个技能去访问财联社

## 迁移建议

推荐顺序：
1. 先在本技能内跑通并稳定验证
2. 迁移 `hourly-pulse-report-001`
3. 迁移“过去1小时/24小时财联社电报”类任务
4. 迁移加红简报与依赖 CLS 的 stock-news 聚合链路
5. 最后清理旧的直接访问逻辑

## 发布说明

当前文档同步版本：`0.1.2`（2026-03-29）

这个技能已经按 GitHub / ClawHub 友好方式组织，但正式发布前仍建议：
- 在有 `pytest` 的环境里补跑测试
- 审查 README 示例与实际代码是否保持一致
- 确认发布仓库已配置远端与有效 GitHub 认证
- 发布到 ClawHub 前确认账号已登录且元数据完整
- 若独立仓库发布，补充仓库级 `LICENSE`
