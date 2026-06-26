# Amazon Review Advisor

> 🔰 亚马逊卖家的「情绪免疫系统」与「品牌护盾」

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Coze-blue.svg)](https://coze.com)

## 🎯 核心定位

**不是删评工具**，而是帮助卖家**合规应对差评**、**分析反馈**、**提炼改进方向**的情绪免疫系统。

## ✨ 功能概览

### 1. 评论情绪分类
- 🟢正面 / 🔴负面 / 🟡中性 自动识别
- 投诉焦点分类：物流/质量/尺寸/包装/客服
- 异常模式标注

### 2. 分类应对方案

| 类型 | 处理策略 |
|------|----------|
| **真实体验差评** | → 内部改进建议 + 公开回复模板 |
| **异常评论** | → 违规要素梳理 + 合规申诉路径 |

### 3. 评价邀请指导
- ⏰ 最佳时机：送达后 **3-7 天**
- 📝 话术模板（英文/中文）
- ✅ 仅使用官方渠道，对所有买家一视同仁

### 4. 评论趋势梳理
- 问题频率统计
- 产品迭代建议
- 运营优化方向

## 🚀 快速开始

### 输入格式
```
产品信息：[ASIN / 产品名称 / 产品描述]

待分析评论：[粘贴评论内容]

关注点（可选）：[具体想解决的问题]
```

### 示例
```
产品信息：无线蓝牙耳机，型号X1

待分析评论：
1. "Sound quality is amazing but the earbuds fell out easily." - 3 stars
2. "Battery lasted only 2 hours, not 8 as advertised." - 1 star

关注点：了解产品质量问题类型
```

## ⚠️ 合规声明

1. 本技能**不提供删评服务**，只提供合规应对指导
2. 严禁虚假评论、刷单等违规行为
3. 评价邀请**仅使用官方 "Request a Review" 功能**，对所有买家一视同仁
4. **禁止以补偿、退款等利益交换诱导买家修改评价**
5. 平台政策请以 Amazon 官方最新指南为准

## 📁 文件结构

```
amazon-review-advisor/
├── SKILL.md                        # 技能主文件
├── clawhub.yaml                    # ClawHub 元数据
├── README.md                       # 本说明文档
└── references/
    └── response-templates.md       # 回复模板库
```

## 🔗 相关资源

- [Amazon Seller Central](https://sellercentral.amazon.com)
- [Review Reporting Guidelines](https://www.amazon.com/gp/help/customer/html.html?plattr=FOOT)
- [Request a Review Feature](https://sellercentral.amazon.com/learn/courses?moduleId=8eb9f36c&quizId=34b&readId=a5e5c43a)

## 📄 License

MIT License - feel free to use and modify.
