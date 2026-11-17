---
name: "Baidumap"
version: "1.1.0"
description: "百度地图快速入口：本 skill 是 baidu-map 主技能的别名入口，附百度地图开放平台速查（BD-09坐标系、Web API 域名、Key申请路径）。Alias entry for the baidu-map skill, with a quick reference for Baidu Maps Open Platform (BD-09 coordinates, API domains, key application)."
tags: ["baidu", "map", "navigation", "lbs", "alias"]
author: "ClawSkills Team"
category: "navigation"
---

# 百度地图（别名入口）

完整的百度地图开发指引在本团队的 **`baidu-map`** 主技能中，
本入口保留一份最常用的速查信息，避免多维护一份重复文档。

## 速查卡

| 项目 | 值 |
|------|-----|
| 开放平台 | https://lbsyun.baidu.com |
| 坐标系 | **BD-09**（百度自有，GCJ-02 基础上二次加密） |
| Key 申请 | 开放平台控制台 → 创建应用 → 获取 AK |
| 主要产品线 | JavaScript API、Web 服务 API、Android/iOS SDK、静态图 |

## 最容易踩的坑：坐标系

百度地图全系使用 BD-09 坐标。把 GPS（WGS-84）或高德/腾讯（GCJ-02）
坐标直接传给百度接口，位置会偏移几百米：

- 外部坐标 → 百度：用官方"坐标转换服务"（Web 服务 API 提供）
- 百度坐标 → 外部：官方不提供反向接口，社区有近似算法（有精度损失）

## Agent 典型用法

1. 用户要做地图选型/接入百度地图 → 安装并使用 `baidu-map` 主技能
2. 用户的坐标显示偏移 → 优先排查坐标系是否混用（见上节）
3. 对比三大地图平台 → 高德见 `gaode`、腾讯见 `tencent-map`
