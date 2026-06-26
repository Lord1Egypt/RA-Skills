---
name: biglead
description: "🎯 BigLead 精准客户线索挖掘 — 按行业/产品/地区搜索目标公司，多渠道交叉验证，提取联系方式（如有），管理客户线索库。B2B销售、市场调研、竞品分析。"
---

# 🎯 BigLead · 精准客户线索挖掘

按行业/产品/地区搜索目标公司，多渠道交叉验证，提取联系方式，构建客户线索库。

## 📋 功能概览

BigLead 是一款 **精准 B2B 客户线索挖掘工具**，按行业/产品/地区搜索目标公司，多渠道验证，提取联系方式。

**核心功能：**
- **🔍 智能搜索** — 按行业、产品、地区、规模等多维度搜索目标公司
- **✅ 多渠道验证** — 官网、招聘、新闻、社交等多源交叉验证公司信息
- **📞 联系方式提取** — 从公开渠道提取电话、邮箱等联系信息
- **📂 客户库管理** — 线索分类保存，跟进状态追踪
- **📊 竞品分析** — 自动识别竞品动态，生成行业洞察
## 触发词

`找客户` `搜公司` `客户线索` `找做XX的公司` `行业XX的公司` `潜在客户` `leads` `list` `搜索客户` `客户挖掘`

## ⚠️ 数据存储规范

所有线索数据 **必须** 存到 `memory/lead-data/` 目录：

```
memory/lead-data/
├── leads.json         ← 所有客户线索
├── search-history.json  ← 搜索记录（避免重复搜索）
└── export/            ← 导出的 CSV
```

**读写方式：**
- 新增线索 → `python3 skills/biglead/scripts/biglead.py add ...`
- 查询线索 → `python3 skills/biglead/scripts/biglead.py query ...`
- 导出 → `python3 skills/biglead/scripts/biglead.py export`
- 统计 → `python3 skills/biglead/scripts/biglead.py stats`

不要手动读写 JSON 文件。

## 线索数据格式

```json
{
  "leads": [
    {
      "id": "uuid",
      "company": "深圳市XX科技有限公司",
      "business": "主营业务描述",
      "region": "深圳",
      "industry": "智能家居",
      "website": "xxx.com",
      "phone": "",              // 公开联系方式，没有留空
      "email": "",              // 公开联系方式，没有留空
      "address": "",
      "sources": [              // 信息来源
        {"name": "企查查", "url": "...", "trusted": true},
        {"name": "官网", "url": "...", "trusted": true}
      ],
      "credibility": 2,         // 可信度分数（0-3）
      "status": "new",          // new / contacted / qualified / disqualified
      "created_at": "2026-05-30T17:00:00+08:00",
      "updated_at": "2026-05-30T17:00:00+08:00",
      "notes": ""
    }
  ]
}
```

## 工作流程

### 1️⃣ 客户搜索（核心）

用户指定：**做什么**（行业/产品）+ **在哪**（地区），可选：**公司规模**。

**搜索策略（自动构建多角度查询）：**

```python
# 示例：用户说"找深圳做智能家居的公司"
queries = [
    "深圳 智能家居 公司 企业名录",            # 通用名录
    "深圳 智能家居 企业列表 site:zhihu.com",   # 知乎推荐
    "智能家居 深圳 厂家 供应商",               # 供应链
    "2025 深圳 智能家居 企业 排名",            # 排名/榜单
    "深圳 智能家居 公司 官网 招聘",            # 招聘渠道
]
```

**执行流程：**

```
请求解析 → 构建搜索策略
   ↓
① 查已有名单 → python3 scripts/biglead.py existing --industry 行业 --region 地区
   ↓   输出该行业/地区已收录的公司名（供搜索时过滤）
   ↓
② web_search × 3-5 次（不同关键词/渠道）
   ↓   跳过已有名单里的公司
   ↓
③ 结果归并 + 去重（同一公司合并）
   ↓   再次过滤已收录的公司
   ↓
④ 只对新增公司 → web_fetch 官网/来源页
   ↓
⑤ 提取：业务描述 / 联系方式（有则记，无则空） / 地址
   ↓
⑥ 交叉验证：出现在 N 个来源 → 可信度 +N
   ↓
⑦ 保存到 leads.json + 输出报告
```

> 💡 **去重关键：** 每次搜索前先查已有名单，web_fetch 只花在新公司上，不浪费时间去爬已经找到的。

> 📋 **输出限制：** 每次搜索默认输出 **最多 10 家客户**，避免结果过长。如果需要查询更多公司，请告诉用户再找一批。

### 2️⃣ 联系方式提取规则

| 位置 | 提取方式 | 备注 |
|------|---------|------|
| 官网 | web_fetch 首页 + 联系页面 | 找 "contact" "关于我们" 链接 |
| 企业名录 | 搜索结果摘要/详情页 | 部分名录页带电话 |
| 招聘网站 | 招聘信息中的公司地址、邮箱 | 不同角度看公司规模 |
| 行业黄页 | 供应商/厂家页面 | 通常带电话 |

> ⚠️ 只提取**公开可见**的联系方式。没有就不填，不会自动推断。

### 3️⃣ 可信度评分

| 分数 | 条件 | 示例 |
|:---:|------|------|
| 3 🟢 | 3+ 独立来源验证 | 企查查 + 官网 + 招聘 |
| 2 🟢 | 2 个来源 | 官网 + 名录 |
| 1 🟡 | 1 个来源 | 仅出现在某个名单 |
| 0 ⚪ | 来源不可靠 | 论坛帖子提到 |

### 4️⃣ 线索管理

- 查询已有线索 → `python3 scripts/biglead.py query --industry 智能家居 --region 深圳`
- 更新线索状态 → `python3 scripts/biglead.py update --id <uuid> --status contacted`
- 导出 CSV → `python3 scripts/biglead.py export`
- 统计 → `python3 scripts/biglead.py stats`

## 输出格式

```
🎯 BigLead 客户线索报告

📋 搜索条件：深圳 智能家居
🔍 搜索策略：企业名录 ×1 / 知乎推荐 ×1 / 供应商 ×1 / 行业榜单 ×1
📊 共发现：12 家（去重后 8 家） | 新线索 8 条

🟢 高可信度（3 分）
1. 深圳市XX智能科技有限公司
   → 官网：xxx.com
   → 业务：智能灯控系统 · 成立于2015 · 50-200人
   → 📞 0755-XXXXXXXX
   → ✉️ info@xxx.com
   → 📍 深圳市南山区科技园
   → 来源：企查查✅ 官网✅ 招聘✅

2. 深圳XX物联网技术有限公司
   → 官网：xxx.com
   → 业务：智能家居解决方案 · 2018成立
   → 📞 （未公开）
   → 来源：官网✅ 行业黄页✅

🟡 中等可信度（1-2 分）
3. ...

💡 建议：优先联系高可信度线索。联系方式为空的可通过官网联系表单触达。
📋 以上是前 10 家客户，如需查询更多公司请告知。
---
```

## 常见搜索场景

| 你说 | 搜索策略 |
|------|---------|
| "找深圳做跨境电商的公司" | 跨境电商 深圳 企业 + 深圳 跨境电商 协会 成员 + 深圳 Amazon 卖家 名单 |
| "搜索做AI客服的公司" | AI 客服 公司 + 智能客服 企业 排名 + AI 客服 SaaS 厂商 |
| "广州的电子元器件供应商" | 广州 电子元器件 供应商 + 广州 电子元器件 厂家 + 广州 元器件 代理商 |
| "找上海做SaaS的公司" | 上海 SaaS 企业 名单 + 上海 SaaS 公司 2025 + 上海 企业服务 SaaS |


## ⚠️ 使用注意

1. **公开数据原则** — 只搜公开信息，不爬付费墙、不搞暴力破解
2. **联系方式有限** — 大部分公司不公开个人手机，有官网联系表单就不错了
3. **不要过度搜索** — 同一家公司不要反复搜，避免被封
4. **数据时效** — 公开信息可能过时，建议先通过官网验证

## 脚本工具

```bash
# 新增线索
python3 skills/biglead/scripts/biglead.py add \
  --company "公司名" \
  --business "业务描述" \
  --region "深圳" \
  --industry "智能家居" \
  --website "xxx.com" \
  --phone "0755-XXXX" \     # 可选，没有不传
  --email "info@xxx.com"    # 可选，没有不传
  --source "企查查"

# 批量新增（从 JSON 文件）
python3 skills/biglead/scripts/biglead.py import --file companies.json

# 查询线索
python3 skills/biglead/scripts/biglead.py query [--industry 行业] [--region 地区] [--status new]

# 更新线索
python3 skills/biglead/scripts/biglead.py update --id <uuid> --status contacted --notes "已发邮件"

# 导出 CSV
python3 skills/biglead/scripts/biglead.py export [--output leads.csv]

# 统计
python3 skills/biglead/scripts/biglead.py stats

# 查看已有公司（搜索前过滤用）
python3 skills/biglead/scripts/biglead.py existing --industry 跨境电商 --region 深圳
# 输出：已收录公司名列表，搜索时自动跳过

# 记录搜索历史
python3 skills/biglead/scripts/biglead.py log-search --query "深圳 智能家居 公司" --results 12 --new 8
```
