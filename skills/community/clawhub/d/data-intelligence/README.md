# Data Intelligence 数据智能平台

综合数据智能解决方案，整合 **Apify 云端爬虫**、**PinchTab 浏览器自动化**和**内容分析**，构建完整的数据采集与分析工作流。

## 核心能力

### 🌩️ 云端爬虫 (Apify)
- 55+ 平台支持 (Instagram, Facebook, TikTok, YouTube, Google Maps)
- 无服务器架构，弹性扩展
- 按结果付费，成本可控

### 🖥️ 浏览器自动化 (PinchTab)
- 本地 Chrome 控制
- Token 高效的文本提取
- 实时交互测试

### 📊 内容分析
- 数据清洗与转换
- 竞品分析报告
- 趋势洞察

## 快速开始

### 1. 安装依赖

```bash
# Apify CLI
npm install -g @apify/mcpc

# PinchTab
curl -fsSL https://pinchtab.com/install.sh | bash

# 配置
export APIFY_TOKEN=your_token
```

### 2. 运行示例

```bash
# 采集 Google Maps 商家
/data-collect places "coffee shop" "New York"

# 分析竞品 Instagram
/data-analyze instagram "competitor_handle"

# 浏览器自动化测试
/browser-test https://example.com
```

## 使用场景

| 场景 | 工具组合 |
|------|----------|
| 线索生成 | Apify Google Maps + PinchTab 验证 |
| 竞品监测 | Apify 社媒 Actor + 内容分析 |
| 趋势研究 | Apify Trends + 内容工厂 |
| 电商情报 | Apify 电商 Actor + 价格监控 |

## 文档

- [完整技能文档](skill.md)
- [模板库](templates/)
- [示例脚本](scripts/)

---

*Data-driven decisions, intelligence-powered efficiency.*
