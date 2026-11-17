# 业务规则 - content-template

> 来源: skills/content-template/SKILL.md (v25.0合并 content-catalog, R75.5 Skill 去重)

## 规则列表

### Jinja2 模板引擎

- 引擎: Jinja2 (主引擎)
- 向后兼容: 旧格式 `{var}` 自动转换为 `{{ var }}` 后 Jinja2 渲染
- 格式检测: 含 `{{ }}` / `{% %}` → Jinja2 引擎; 仅含 `{var}` → 自动转换
- 降级: Jinja2 语法错误 → 简单字符串替换; 变量未定义 → 使用默认值

### Jinja2 语法支持

| 语法 | 用途 | 示例 |
|:-----|:-----|:-----|
| `{{ var }}` | 变量替换 | `{{ date }}` |
| `{% if %}` | 条件渲染 | `{% if has_discount %}限时特惠{% endif %}` |
| `{% for %}` | 循环渲染 | `{% for item in features %}{{ item }}{% endfor %}` |
| `{% extends %}` | 模板继承 | `{% extends "tpl_base_001" %}` |
| `{% block %}` | 块覆盖 | `{% block title %}自定义{% endblock %}` |

### 模板类型

| 类型 | 说明 | 适用场景 |
|:-----|:-----|:---------|
| video | 视频文案模板 | 短视频、Vlog |
| article | 图文文案模板 | 小红书图文 |
| reply | 回复话术模板 | 客服自动回复 |
| product_desc | 商品描述模板 | 电商商品描述 |
| hook | 引流钩子模板 | 评论区/私信引流引导 |

### 模板 ID 格式

- 格式: `tpl_{category}_{seq}`
- 示例: `tpl_video_001`, `tpl_article_002`

### 模板存储

- 模板文件: `data/content/templates/{tpl_id}.json`
- 索引文件: `data/content/templates/index.json`

### A/B 测试

- 最少模板数: 至少 2 个模板
- 流量分配: 默认 50%/50%
- 统计显著性: p < 0.05
- 优胜标记: 标记为 recommended
- 注意: 当前为简易对比模式,非完整 A/B 测试

### 文案润色四步法 (v1.3新增)

1. 诊断 AI 味: 识别套话/空话/过度修辞
2. 营销注入: 调用 market-copywriter → 卖点 + 情绪钩子 + CTA
   - 失败→重试1次 (降级为基础营销模板: 痛点钩子+FAB卖点+CTA)
   - 重试仍失败→拦截发布 (营销注入为强制门控)
3. 识别商业目标: 点击 (好奇心) / 转化 (购买欲) / 降疑虑 (信任感)
4. 改写保留卖点: 保留核心卖点 + 数据 + 限时信息,替换 AI 套话为口语化表达
5. 风险合规检查: 绝对化用语→替换, 平台规则违规→删除

### 多版本改写

| 版本 | 适用场景 |
|:-----|:---------|
| 克制版 | 品牌官方号 |
| 种草版 | KOC 素人号 |
| 转化版 | 促销活动 |

### 品类目录查询 (v25.0合并)

- 原 content-catalog 已合并到本 Skill (R75.5 Skill 去重)
- 执行脚本: content_catalog.py
- 功能: 返回支持的内容生成品类/格式/平台/方法
