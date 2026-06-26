---
name: address2lnglat
description: 调用百度地图开放平台API，将地名批量转换为BD-09（百度）经纬度坐标，自动搜索地点 → 用户填入AK → 批量爬取坐标 → 保存CSV+JSON → 直接发送给用户。坐标保留6位小数，无需转换。
version: 1.0.0
author: ""
tags: ["地图", "百度", "地理编码", "经纬度", "坐标", "BD-09", "批量处理"]
license: MIT
homepage: ""
keywords: ["baidu", "geocoding", "address to coordinates", "BD-09", "batch", "lnglat"]
issuesUrl: ""
supports: {}
runtime: "python3"
---

# address2lnglat v4

通过百度地图开放平台 API，将地名批量转换为 **BD-09（百度）坐标**。

## 坐标系说明

| 坐标系 | 说明 | 用途 |
|--------|------|------|
| **BD-09** | 百度坐标系（本工具输出） | 直接用于百度地图相关业务 |
| GCJ-02 | 火星坐标系 | 高德/腾讯/Google地图等 |

> ⚠️ 百度地图 API 直接返回 BD-09 坐标，无需任何转换。

## 工作流程

1. **用户输入关键词**（如"天津赏花地点"）
2. **AI 搜索并总结所有相关地点名称列表**
3. **提示用户提供百度地图 AK 和限制城市**
4. **运行 Python 脚本，调用百度 Place API 获取 BD-09 坐标**
5. **保存为 CSV + JSON 文件**
6. **直接发送 CSV 文件给用户**

## 依赖

- Python 3.x
- `requests` 库（`pip install requests`）

## 使用方法

```bash
python geocoder.py 天津赏花地点
```

脚本会依次提示：
1. 输入百度地图 AK
2. 是否限制在城市内搜索

## 输出字段

| 字段 | 说明 |
|------|------|
| 序号 | 编号 |
| 名称 | 地点名称 |
| 详细地址 | 结构化地址 |
| BD-09经度 | 百度坐标经度（6位小数） |
| BD-09纬度 | 百度坐标纬度（6位小数） |
| 坐标来源 | place_api / geocoding_api |
| 类型 | 地点类型（景点/学校等） |
| 置信度 | 匹配置信度评分 |
| 状态 | 成功/失败 |

## 百度AK申请

1. 访问 [百度地图开放平台](https://lbsyun.baidu.com/)
2. 注册开发者账号 → 进入「控制台」→「我的应用」
3. 创建「浏览器端应用」→ 复制 AK
4. 确保已开通「地理编码」服务（免费6000次/天）
