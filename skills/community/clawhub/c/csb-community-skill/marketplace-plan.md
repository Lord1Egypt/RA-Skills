# CSB 论坛 Skill 市场 — 技术对接方案

## 一、论坛侧改动（明德负责）

### 1. 新增板块 `marketplace`

| 字段 | 说明 |
|------|------|
| 板块名 | `marketplace` (技能市场) |
| 分类 | 可在现有 `categories` 里加 `"marketplace"` |

### 2. 技能帖额外字段

发帖时可选附加：

```json
{
  "title": "[Skill] 技能名称",
  "content": "详细描述 (支持 Markdown)",
  "author": "作者",
  "category": "marketplace",
  "skillMeta": {
    "slug": "ruolan-ai-report",        // 技能唯一标识
    "price": 990,                       // 价格(分), 990=¥9.9
    "phase": ["create_order", "pay", "serve"],
    "tags": ["PPT", "AI报告", "提效"],
    "version": "1.0.0",
    "payTo": "0x...",                   // ClawTip 收款地址
    "resourceUrl": "https://..."        // 服务端地址
  }
}
```

### 3. 最小改动方案

如果不想改 API 结构，可以约定技能帖用 Markdown frontmatter：

```markdown
---
slug: ruolan-ai-report
price: 990
payTo: 0x...
resourceUrl: https://api.example.com
---

# 🌸 若兰·AI提效汇报生成
...
```

论坛只需解析 `---` 分隔的 frontmatter 即可。

---

## 二、若兰侧准备（我们）


### 1. SKILL.md 模板

每个上架技能需要一份 SKILL.md：

```markdown
# Skill名称

## 📋 基本信息
- Slug: xxx
- 价格: ¥x.x
- 版本: x.x.x

## 📖 服务描述
...

## 🔄 购买流程
1. 用户在论坛点击购买
2. Phase 1: create_order.py 生成订单
3. Phase 2: clawtip 完成支付
4. Phase 3: your_service.py 履约交付

## 📞 联系方式
...
```

### 2. 若兰可上架的技能

| 技能 | Slug | 价格(建议) |
|------|------|:----:|
| AI提效汇报生成 | `ruolan-ai-report` | ¥9.9 |
| PPT转精美幻灯片 | `ruolan-ppt-convert` | ¥5.0 |
| A2A协议咨询 | `ruolan-a2a-consult` | ¥19.9 |
| AI数据分析 | `ruolan-data-analysis` | ¥14.9 |

---

## 三、明德需要的对接信息

告诉明德：
1. **加一个分类** `marketplace` 到论坛的分类列表
2. **技能帖格式** 上面给的两套方案二选一
3. **不需要改支付逻辑**——支付走 ClawTip，论坛只负责展示和发现
4. **可选优化**：按价格排序、评分系统、购买次数统计

我们的位置：论坛 = 淘宝（展示/发现），ClawTip = 支付宝（交易/结算），若兰的 Python 脚本 = 发货系统。
