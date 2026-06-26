# GEO Master - 品牌AI可见性监控

自动搜索Kimi、讯飞星火、文心一言、智谱等AI平台，检测品牌关键词的AI搜索可见性，生成0-100 GEM评分，AI分析"为什么没被推荐"，支持飞书推送。

## 版本与定价

| 版本 | 价格 | 品牌限制 | 平台数量 | 技术方案 |
|------|------|:--------:|:--------:|----------|
| **免费版** | ¥0/月 | 1个/月 | 3个平台 | 本地Playwright |
| **专业版** | ¥99/月 | 无限 | 全部9个平台 | 🌐 Tavily API（实时搜索） |
| **企业版** | ¥399/月 | 无限 | 全部9个+深度分析 | 专属客服 |

### 专业版核心优势

- ✅ 全部9个AI平台（DeepSeek/千问/豆包/秘塔/混元等）
- ✅ 覆盖AI的**实时搜索推荐**（非训练数据）
- ✅ 我们服务器中转，无需本地环境
- ✅ 稳定高效，不封IP

> 申请专业版：[https://yk-global.com](https://yk-global.com)

### 免费版限制

- 每月最多检测 **1个品牌**
- 每月最多使用 **3个AI平台**（Kimi、讯飞星火、文心一言）
- 每月1日自动重置配额

### 升级方法

访问 [https://yk-global.com](https://yk-global.com) 购买专业版/企业版，获取升级码后运行：

```bash
# 升级到专业版
python3 scripts/geo_report.py --upgrade-pro

# 升级到企业版
python3 scripts/geo_report.py --upgrade-ent
```

## 快速使用

```bash
# 检测单个品牌
python3 scripts/geo_report.py "品牌名"

# 检测多个品牌
python3 scripts/geo_report.py "品牌A" "品牌B"

# 不推送飞书（调试用）
python3 scripts/geo_report.py "品牌名" --no-push

# 查看当前配额状态
python3 scripts/geo_report.py --status
```

## 支持的平台

| 平台 | 免费版 | 专业版 |
|------|:------:|:------:|
| Kimi | ✅ | ✅ |
| 讯飞星火 | ✅ | ✅ |
| 文心一言 | ✅ | ✅ |
| 智谱 | ❌ | ✅ |
| DeepSeek | ❌ | ✅ |
| 通义千问 | ❌ | ✅ |
| 豆包 | ❌ | ✅ |
| 秘塔 | ❌ | ✅ |
| 混元 | ❌ | ✅ |

## 评分说明

| 评分 | 等级 | 说明 |
|-----:|:----:|------|
| 80-100 | 🟢 优秀 | AI主动推荐，品牌强曝光 |
| 60-79 | 🟡 良好 | 被部分AI平台提及 |
| 30-59 | 🟠 一般 | 零星提及，需优化 |
| 0-29 | 🔴 薄弱 | 完全不可见 |

## 配置文件

编辑 `config.json`：

```json
{
  "report": {
    "push_to_feishu": true,
    "feishu_webhook": "填入您的飞书群机器人地址"
  }
}
```

**如何获取飞书Webhook？**
在飞书群设置中添加"自定义机器人"，复制Webhook地址填入上方。

## 依赖

- Python 3.10+
- playwright (`pip install playwright && playwright install chromium`)

## 官网

[https://yk-global.com](https://yk-global.com)
