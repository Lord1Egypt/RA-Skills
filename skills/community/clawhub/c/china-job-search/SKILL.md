---
name: china-job-search
description: 中国招聘平台搜索技能。支持BOSS直聘、智联招聘、前程无忧三大平台，提供关键词搜索、地点筛选、薪资范围过滤等功能。专门针对中国本土招聘市场设计。
metadata: { "openclaw": { "emoji": "🔍", "requires": { "python": true }, "category": "productivity", "language": "zh-CN" } }
version: 1.0.0
author: 鱼头
license: MIT
---

# 招聘搜索技能

## 功能概述

专门用于在中国主流招聘平台（BOSS直聘、智联招聘、前程无忧）搜索岗位信息的技能。支持多条件筛选和结构化结果展示。

## 🚀 快速开始

### 基础搜索
```
搜索 [关键词] [地点]
示例：搜索 Python开发 北京
```

### 高级搜索
```
搜索 [关键词] [地点] [薪资下限]-[薪资上限]K [经验要求]
示例：搜索 Java开发 上海 15-30K 3-5年
```

### 平台指定搜索
```
搜索 [平台] [关键词] [地点]
示例：搜索 boss Python 北京
示例：搜索 智联 前端 上海
示例：搜索 前程无忧 测试 广州
```

## 📋 使用说明

### 搜索参数
- **关键词**: 职位名称或技能关键词
- **地点**: 城市名称（如：北京、上海、广州、深圳）
- **薪资范围**: 格式为"下限-上限K"（如：15-30K）
- **经验要求**: 格式为"下限-上限年"（如：3-5年）

### 支持平台
1. **BOSS直聘** (boss/zhipin) - 最活跃的互联网招聘平台
2. **智联招聘** (zhilian/zhaopin) - 传统综合性招聘平台
3. **前程无忧** (qiancheng/51job) - 大型综合招聘平台

## 🔧 技术实现

### 核心文件
- `scripts/job_searcher.py` - 主搜索逻辑
- `scripts/boss_parser.py` - BOSS直聘解析器
- `scripts/zhilian_parser.py` - 智联招聘解析器
- `scripts/qiancheng_parser.py` - 前程无忧解析器

### 依赖库
```txt
requests>=2.28.0
beautifulsoup4>=4.11.0
fake-useragent>=1.4.0
```

### 安装依赖
```bash
pip install -r scripts/requirements.txt
```

## 📊 输出格式

搜索结果以结构化表格形式展示，包含以下字段：
- 平台
- 职位标题
- 公司名称
- 薪资范围
- 工作地点
- 经验要求
- 学历要求
- 关键技能
- 发布时间
- 详情链接

## ⚠️ 注意事项

1. **遵守平台规则**: 尊重各平台的robots.txt，避免频繁请求
2. **合理使用**: 搜索结果仅供参考，请以官方信息为准
3. **隐私保护**: 不存储用户个人信息
4. **延迟设置**: 自动添加请求延迟，避免被封IP

## 🔄 更新日志

### v1.0.0 (初始版本)
- 支持三大主流招聘平台
- 实现基础搜索和高级搜索
- 结构化结果展示
- 多条件筛选功能

## 📁 文件结构

```
job-search/
├── SKILL.md              # 技能说明文档
├── scripts/              # Python脚本目录
│   ├── job_searcher.py   # 主搜索逻辑
│   ├── boss_parser.py    # BOSS直聘解析器
│   ├── zhilian_parser.py # 智联招聘解析器
│   ├── qiancheng_parser.py # 前程无忧解析器
│   ├── config.json       # 配置文件
│   └── requirements.txt  # 依赖库列表
└── references/           # 参考文档
    └── API_REFERENCE.md  # API接口说明
```

## 💡 使用示例

### 示例1：简单搜索
```
用户：搜索 Python开发 北京
技能：正在搜索BOSS直聘、智联招聘、前程无忧的Python开发岗位（北京）...
```

### 示例2：高级搜索
```
用户：搜索 Java开发 上海 20-40K 5-8年
技能：正在搜索Java开发岗位（上海），薪资20-40K，经验5-8年...
```

### 示例3：指定平台
```
用户：搜索 boss 前端 杭州
技能：正在搜索BOSS直聘的前端开发岗位（杭州）...
```

## 🛠️ 开发指南

如需扩展功能或添加新平台，请参考：
1. 在`scripts/`目录下创建新的解析器
2. 在`job_searcher.py`中注册新平台
3. 更新`config.json`配置文件
4. 测试新功能并更新文档