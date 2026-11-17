---
name: content-template
description: "内容模板管理(v25.0合并content-catalog)，Jinja2引擎变量替换/条件渲染/循环/继承，A/B测试和文案润色+内容品类目录查询。 触发词：内容模板/模板创建/变量替换/A-B测试/文案润色/去AI味/电商文案/Jinja2模板/内容品类/内容菜单 不触发：内容发布/趋势发现/视频生成"
version: 2.2.0
user-invocable: true
tools: [read, exec]
dependencies: [market-copywriter]
metadata:
  priority: "P1"
  openclaw:
    emoji: "📝"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      env: []
      config: []
---
> **v25.0合并**: content-catalog已合并到本Skill(R75.5 Skill去重)。内容品类目录查询(返回支持的内容生成品类/格式/平台/方法)由content_catalog.py执行。原content-catalog目录已删除。

> **运行环境**: 本Skill的exec脚本必须使用 **Python 3.11.x** (`.venv/Scripts/python.exe`) 执行。禁止使用系统Python 3.14+。

# Content Template Skill

内容模板管理、Jinja2引擎变量替换/条件渲染/循环/继承、A/B测试、文案润色(去AI味)、内容品类目录查询。

## 使用场景

1. 模板创建: 创建新的内容模板(视频/图文/话术/商品描述/引流钩子)
2. 模板使用: Jinja2引擎变量替换生成具体内容(向后兼容旧`{var}`格式)
3. 条件渲染: `{% if has_discount %}限时优惠{% endif %}` 按条件显示内容
4. 循环渲染: `{% for item in features %}• <动态配置>{% endfor %}` 批量生成列表
5. 模板继承: 子模板`{% extends "parent_id" %}` + `{% block name %}` 继承父模板
6. A/B测试: 对比不同模板效果(⚠️当前为简易对比模式，非完整A/B测试)
7. 文案润色: 电商文案去AI味改写，保留卖点+转化意图
8. 营销文案生成: 调用market-copywriter提炼卖点+情绪钩子，生成高转化营销文案
9. **品类目录查询(v25.0合并)**: 管理员问"能生成哪些内容"时,返回完整内容品类目录

## 工作流

### 模板创建
1. 接收创建请求(name/type/category/content/variables[]/extends)，验证名称唯一+类型有效
2. 自动提取变量: 同时支持旧格式`{var}`和Jinja2格式`<动态配置>`/`{% if var %}`/`{% for x in var %}`
3. 生成模板ID: `tpl_{category}_{seq}`
4. 写入 `data/content/templates/{tpl_id}.json`，注册索引到 `index.json`
5. 返回 template_id + status

### 模板使用(Jinja2引擎)
1. 接收使用请求(template_id/variables{})，验证模板存在+变量完整
2. 自动检测模板格式: 含`<动态配置>`/`{% %}`→Jinja2引擎，仅含`{var}`→自动转换为`<动态配置>`后Jinja2渲染
3. Jinja2渲染: 变量替换`<动态配置>` + 条件渲染`{% if %}` + 循环`{% for %}`
4. 渲染失败降级: Jinja2语法错误→简单字符串替换，变量未定义→使用默认值
5. 更新使用次数，写入memory日志
6. 返回 template_id + generated_content + engine_used

### 模板继承
1. 接收继承渲染请求(template_id/variables{})
2. 检测子模板`{% extends "parent_id" %}`，加载父模板
3. Jinja2继承渲染: 父模板`{% block name %}`被子模板`{% block name %}新内容{% endblock %}`覆盖
4. 返回 rendered_content + parent_id

### A/B测试
1. 接收测试请求(template_ids[]/metric/duration)，验证至少2个模板
2. 创建测试组，分配流量(默认50%/50%)
3. 执行测试: 内容发布时随机选择模板，记录效果数据
4. 分析结果: 计算各模板metric值，统计显著性(p<0.05)
5. 标记优胜模板为recommended

### 文案润色四步法(v1.3新增)
1. **诊断AI味**: 识别套话/空话/过度修辞
2. **营销注入**: 调用market-copywriter，输入商品/服务信息→提炼核心卖点(selling_points)→选择情绪钩子(emotional_hook)→获取CTA话术，失败→重试1次(降级为基础营销模板:痛点钩子+FAB卖点+CTA)，重试仍失败→❌拦截发布(营销注入为强制门控，不允许跳过)
3. **识别商业目标**: 点击(好奇心) / 转化(购买欲) / 降疑虑(信任感)
4. **改写保留卖点**: 保留核心卖点+数据+限时信息，融合market-copywriter返回的卖点+情绪钩子，替换AI套话为口语化表达
5. **风险合规检查**: 绝对化用语→替换，平台规则违规→删除

**多版本改写**: 克制版(品牌官方号) / 种草版(KOC素人号) / 转化版(促销活动)

## Jinja2模板语法

### 变量替换
```
旧格式(向后兼容): 大家好，今天是{date}，今天我们来{topic}
Jinja2格式: 大家好，今天是<动态配置>，今天我们来<动态配置>
```

### 条件渲染
```
{% if has_discount %}限时特惠，原价<动态配置>元，现价<动态配置>元{% endif %}
{% if is_new %}新品首发{% else %}经典回归{% endif %}
```

### 循环渲染
```
{% for feature in features %}• <动态配置>
{% endfor %}
{% for item in product_list %}<动态配置> - <动态配置>元
{% endfor %}
```

### 模板继承
```
父模板(base): {% block title %}默认标题{% endblock %} - {% block content %}默认内容{% endblock %}
子模板: {% extends "tpl_base_001" %}{% block title %}自定义标题{% endblock %}{% block content %}自定义内容{% endblock %}
```

## 模板类型

| 类型 | 说明 | 适用场景 |
|:-----|:-----|:---------|
| video | 视频文案模板 | 短视频、Vlog |
| article | 图文文案模板 | 小红书图文 |
| reply | 回复话术模板 | 客服自动回复 |
| product_desc | 商品描述模板 | 电商商品描述 |
| hook | 引流钩子模板 | 评论区/私信引流引导 |

> 完整模板JSON格式、钩子模板字段说明、exec脚本命令、输入/输出JSON示例、润色语气适配表详见 scripts/content_template_reference.json

## 输入格式

```json
{
  "action": "create|generate|replace|ab_test|polish|render_inheritance",
  "template_id": "tpl_video_001",
  "name": "视频文案模板",
  "type": "video|article|reply|product_desc|hook",
  "category": "video",
  "content": "大家好，今天是<动态配置>，今天我们来<动态配置>",
  "variables": [{"name": "date", "default": ""}, {"name": "topic", "default": ""}],
  "extends": "tpl_base_001",
  "metric": "click_rate",
  "duration": "7d"
}
```

字段说明:
- `action`: 操作类型(create创建模板/generate LLM生成内容/replace渲染/ab_test A/B测试/polish文案润色/render_inheritance继承渲染)
- `template_id`: 模板ID(tpl_{category}_{seq}格式)
- `type`: 模板类型(video视频/article图文/reply回复话术/product_desc商品描述/hook引流钩子)
- `content`: 模板内容,支持Jinja2语法(`<动态配置>`变量/`{% if %}`条件/`{% for %}`循环/`{% extends %}`继承)
- `variables`: 变量定义数组(name变量名/default默认值)
- `extends`: 父模板ID(用于模板继承)
- `metric`: A/B测试指标(click_rate点击率/conversion_rate转化率)
- `duration`: A/B测试持续时间

## 输出格式

```json
{
  "success": true,
  "data": {
    "template_id": "tpl_video_001",
    "generated_content": "大家好，今天是2026-04-07，今天我们来健身打卡",
    "engine_used": "jinja2",
    "variables_resolved": 2,
    "variables_missing": [],
    "ab_test_result": null,
    "polished_content": null
  },
  "error": null,
  "code": null
}
```

字段说明:
- `template_id`: 模板ID
- `generated_content`: 渲染后的内容(replace/render_inheritance操作返回)
- `engine_used`: 实际使用的渲染引擎(jinja2/simple_string_replace降级)
- `variables_resolved`: 成功解析的变量数
- `variables_missing`: 缺失的变量列表(降级使用默认值)
- `ab_test_result`: A/B测试结果(winner_template_id/significance/sample_size)
- `polished_content`: 润色后的内容(polish操作返回)

> 完整输入/输出JSON示例详见 scripts/content_template_reference.json

## 异常处理

| 异常类型 | 错误代码 | 处理方式 |
|:---------|:---------|:---------|
| 模板不存在 | TEMPLATE_NOT_FOUND | 返回错误提示 |
| 变量缺失 | MISSING_VARIABLES | 返回缺失变量列表 |
| 参数无效 | INVALID_PARAMS | 返回参数校验错误 |
| A/B测试样本不足 | INSUFFICIENT_SAMPLE | 返回当前数据，标注样本不足 |
| Jinja2语法错误 | CT-ERR-07 | 降级为简单字符串替换 |
| 父模板不存在 | CT-ERR-05 | 返回错误提示 |
| Jinja2不可用 | CT-ERR-06 | 降级为简单字符串替换 |

## 示例

### 旧格式模板(向后兼容)
1. 创建: `python scripts/content_template.py` (action=create, content="大家好，今天是{date}，今天我们来{topic}")
2. 使用: (action=replace, template_id="tpl_video_001", variables={date:"2026-04-07", topic:"健身打卡"})
3. 自动转换: `{date}`→`<动态配置>`→Jinja2渲染→"大家好，今天是2026-04-07，今天我们来健身打卡"

### Jinja2条件渲染模板
1. 创建: (action=create, content="{% if has_discount %}限时特惠<动态配置>元{% else %}售价<动态配置>元{% endif %}")
2. 使用: (action=replace, variables={has_discount:true, sale_price:"99", price:"199"})
3. 结果: "限时特惠99元"

### 模板继承
1. 父模板: (action=create, template_id="tpl_base_001", content="{% block title %}默认{% endblock %} - {% block content %}{% endblock %}")
2. 子模板: (action=create, template_id="tpl_child_001", extends="tpl_base_001", content='{% extends "tpl_base_001" %}{% block title %}自定义标题{% endblock %}{% block content %}自定义内容{% endblock %}')
3. 渲染: (action=render_inheritance, template_id="tpl_child_001", variables={})
4. 结果: "自定义标题 - 自定义内容"

> 更多示例(A/B测试/文案润色)详见 scripts/content_template_reference.json

## 变更历史

| 版本 | 日期 | 变更说明 |
|:-----|:-----|:---------|
| v2.1 | 2026-06-13 | Jinja2模板引擎升级: 条件渲染/循环/继承，向后兼容旧{var}格式 |
| v2.0 | 2026-05-16 | 新增hook模板类型，支持引流钩子 |
| v1.3 | 2026-05-03 | 新增文案润色场景 |
| v1.0 | 2026-04-05 | 初稿 |
