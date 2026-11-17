# 详细参考 - diagram-master-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (json)

```json
{
  "diagramMaster": {
    "batch": {
      "enabled": true,
      "parallel": 4,
      "checkpoint": true
    },
    "color": {
      "custom_enabled": true,
      "theme": "brand-corporate",
      "themes": ["dark", "light", "brand-corporate"]
    },
    "template": {
      "library_path": "~/.diagram-templates/",
      "auto_save": true
    },
    "export": {
      "formats": ["svg", "png@2x", "png@4x"],
      "default": "png@2x"
    },
    "version": {
      "enabled": true,
      "history_path": "~/.diagram-versions/"
    },
    "interactive": {
      "clickable_nodes": true,
      "dynamic_highlight": true
    }
  }
}
```

## 代码示例 (text)

```text
┌──────────────────────────────────────────────────────────────┐
│        图表制作大师专业版 (DIAGRAM MASTER PRO)                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  批量生成     │  │  自定义配色   │  │  模板库       │        │
│  │  Batch Gen   │  │  Custom Color│  │  Template    │        │
│  │              │  │              │  │              │        │
│  │ 多图表并行   │  │ 品牌色定制   │  │ 预设模板     │        │
│  │ 自动化流水线 │  │ 多主题切换   │  │ 快速套用     │        │
│  │              │  │              │  │              │        │
│  │ ✅ 专业版    │  │ ✅ 专业版    │  │ ✅ 专业版    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│          │                │                │                  │
│          └────────────────┼────────────────┘                  │
│                           ▼                                   │
│                   ┌──────────────┐                            │
│                   │  高清导出     │  ← @2x/@4x PNG             │
│                   │  HD Export   │    ✅ 专业版               │
│                   └──────────────┘                            │
│                           │                                   │
│                           ▼                                   │
│                   ┌──────────────┐  ┌──────────────┐          │
│                   │  版本管理     │  │  交互式图表   │          │
│                   │  Version     │  │  Interactive │          │
│                   │  ✅ 专业版   │  │  ✅ 专业版   │          │
│                   └──────────────┘  └──────────────┘          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 完整搭建（<300秒）
配置全部高级功能：

```json
{
  "diagramMaster": {
    "batch": {
      "enabled": true,
      "parallel": 4,
      "checkpoint": true
    },
    "color": {
      "custom_enabled": true,
      "theme": "brand-corporate",
      "themes": ["dark", "light", "brand-corporate"]
    },
    "template": {
      "library_path": "~/.diagram-templates/",
      "auto_save": true
    },
    "export": {
      "formats": ["svg", "png@2x", "png@4x"],
      "default": "png@2x"
    },
    "version": {
      "enabled": true,
      "history_path": "~/.diagram-versions/"
    },
    "interactive": {
      "clickable_nodes": true,
      "dynamic_highlight": true
    }
  }
}
```



## 架构总览
```text
┌──────────────────────────────────────────────────────────────┐
│        图表制作大师专业版 (DIAGRAM MASTER PRO)                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  批量生成     │  │  自定义配色   │  │  模板库       │        │
│  │  Batch Gen   │  │  Custom Color│  │  Template    │        │
│  │              │  │              │  │              │        │
│  │ 多图表并行   │  │ 品牌色定制   │  │ 预设模板     │        │
│  │ 自动化流水线 │  │ 多主题切换   │  │ 快速套用     │        │
│  │              │  │              │  │              │        │
│  │ ✅ 专业版    │  │ ✅ 专业版    │  │ ✅ 专业版    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│          │                │                │                  │
│          └────────────────┼────────────────┘                  │
│                           ▼                                   │
│                   ┌──────────────┐                            │
│                   │  高清导出     │  ← @2x/@4x PNG             │
│                   │  HD Export   │    ✅ 专业版               │
│                   └──────────────┘                            │
│                           │                                   │
│                           ▼                                   │
│                   ┌──────────────┐  ┌──────────────┐          │
│                   │  版本管理     │  │  交互式图表   │          │
│                   │  Version     │  │  Interactive │          │
│                   │  ✅ 专业版   │  │  ✅ 专业版   │          │
│                   └──────────────┘  └──────────────┘          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```



### 场景二：大规模API文档批量生图（API文档工程师角色）
**场景描述**：API文档网站需要为每个API生成时序图，50+API手工绘制不现实。

**操作流程**：
```bash
diagram-master --batch --from-api openapi.yaml \
  --template api-interaction \
  --parallel 8 \
  --output docs/api/diagrams/

diagram-master --export --batch docs/api/diagrams/ \
  --format png@2x
```

**效果**：50+API时序图一键生成，API更新后图表自动更新，文档维护成本降低90%。



