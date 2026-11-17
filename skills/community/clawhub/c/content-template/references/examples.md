# 示例 - content-template

> 来源: skills/content-template/SKILL.md 示例章节

## 示例1: 旧格式模板 (向后兼容)

### 输入

```json
{
  "action": "create",
  "name": "视频文案模板",
  "type": "video",
  "category": "video",
  "content": "大家好，今天是{date}，今天我们来{topic}"
}
```

使用渲染:

```json
{
  "action": "replace",
  "template_id": "tpl_video_001",
  "variables": {"date": "2026-04-07", "topic": "健身打卡"}
}
```

### 输出

```json
{
  "success": true,
  "data": {
    "template_id": "tpl_video_001",
    "generated_content": "大家好，今天是2026-04-07，今天我们来健身打卡",
    "engine_used": "jinja2",
    "variables_resolved": 2,
    "variables_missing": []
  },
  "error": null,
  "code": null
}
```

> 自动转换: `{date}` → `{{ date }}` → Jinja2 渲染

## 示例2: Jinja2 条件渲染

### 输入

```json
{
  "action": "create",
  "name": "促销模板",
  "type": "article",
  "category": "article",
  "content": "{% if has_discount %}限时特惠{{ sale_price }}元{% else %}售价{{ price }}元{% endif %}"
}
```

使用渲染:

```json
{
  "action": "replace",
  "template_id": "tpl_article_001",
  "variables": {"has_discount": true, "sale_price": "99", "price": "199"}
}
```

### 输出

```json
{
  "success": true,
  "data": {
    "template_id": "tpl_article_001",
    "generated_content": "限时特惠99元",
    "engine_used": "jinja2",
    "variables_resolved": 3,
    "variables_missing": []
  },
  "error": null,
  "code": null
}
```

## 示例3: 模板继承

### 输入

父模板创建:

```json
{
  "action": "create",
  "template_id": "tpl_base_001",
  "content": "{% block title %}默认{% endblock %} - {% block content %}{% endblock %}"
}
```

子模板创建:

```json
{
  "action": "create",
  "template_id": "tpl_child_001",
  "extends": "tpl_base_001",
  "content": "{% extends \"tpl_base_001\" %}{% block title %}自定义标题{% endblock %}{% block content %}自定义内容{% endblock %}"
}
```

继承渲染:

```json
{
  "action": "render_inheritance",
  "template_id": "tpl_child_001",
  "variables": {}
}
```

### 输出

```json
{
  "success": true,
  "data": {
    "template_id": "tpl_child_001",
    "generated_content": "自定义标题 - 自定义内容",
    "engine_used": "jinja2",
    "parent_id": "tpl_base_001"
  },
  "error": null,
  "code": null
}
```
