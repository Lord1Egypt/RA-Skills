---
name: asin-video-pipeline
description: ASIN营销视频全自动流水线 - 基于n8n+Topview AI+Apify+Google Sheets的自动化方案。当用户需要创建Amazon产品营销视频、批量生成ASIN视频内容、搭建视频自动化工作流、集成Topview AI视频生成、使用n8n自动化亚马逊视频营销时触发。支持从ASIN列表到成品视频的完整自动化流程，包括产品信息提取、视频生成、审核管理和导出发布。
---

# ASIN营销视频全自动流水线

基于n8n + Topview AI + Apify + Google Sheets 构建的ASIN营销视频自动化解决方案。

## 核心工作流

```
ASIN列表 → 产品信息提取 → 图片上传 → 视频生成 → 审核 → 导出成品
```

### 工作流1：主流程（生成预览视频）
1. **读取 & 筛选** - 从Google Sheets读取ASIN列表，跳过已有视频的行
2. **提取产品信息** - 通过Apify抓取Amazon产品详情
3. **上传图片到Topview** - 将产品图上传至Topview AI
4. **提交视频生成任务** - 调用Topview API创建视频任务
5. **等待 & 查询** - 等待5分钟后查询任务状态
6. **回填链接** - 将预览视频URL写回Google Sheets

### 工作流2：导出流程（生成正式版）
1. **读取审核通过项** - 从Sheets读取标记为"审核通过"的行
2. **获取scriptId** - 用taskId查询任务详情
3. **调用导出接口** - 调用 `/v1/m2v/task/export` 导出无水印版
4. **等待导出完成** - 等待3分钟查询导出结果
5. **回填最终URL** - 将成品视频URL写回Sheets

## 快速开始

### 前置要求
- n8n 实例（本地或云）
- Topview AI API Key
- Apify API Key
- Google Cloud 项目 + Service Account

### 1. 配置Google Sheets

创建表格，包含以下列：
| 列名 | 说明 |
|------|------|
| ASIN | 亚马逊产品ID |
| 产品名称 | 自动填充 |
| 产品图片URL | 自动填充 |
| 视频链接 | 自动填充 |
| 审核状态 | 手动填写：待审核/通过/拒绝 |
| 任务ID | 自动填充 |

### 2. 导入n8n工作流

使用提供的JSON工作流文件：
```bash
# 工作流1：生成预览视频
n8n import:workflow --input=./references/n8n-workflow-preview.json

# 工作流2：导出正式版
n8n import:workflow --input=./references/n8n-workflow-export.json
```

### 3. 配置Credentials

在n8n中配置以下凭证：
- `topviewApiKey` - Topview AI API Key
- `apifyApiKey` - Apify API Key  
- `googleSheetsOAuth2` - Google Sheets API

## Topview AI API 参考

### 上传图片
```
POST /v1/m2v/image/upload
Content-Type: multipart/form-data
Authorization: Bearer {API_KEY}

Body:
- image: 图片文件
```

### 创建视频任务
```
POST /v1/m2v/task
Authorization: Bearer {API_KEY}
Content-Type: application/json

{
  "script_id": "your_script_id",
  "images": ["image_url_1", "image_url_2"],
  "texts": ["产品卖点文案"],
  "callback_url": "https://your-webhook.com"
}
```

### 查询任务状态
```
GET /v1/m2v/task/{task_id}
Authorization: Bearer {API_KEY}
```

### 导出无水印版
```
POST /v1/m2v/task/export
Authorization: Bearer {API_KEY}
Content-Type: application/json

{
  "task_id": "task_id_to_export",
  "script_id": "script_id"
}
```

## 工具清单

| 工具 | 用途 |
|------|------|
| **n8n** | 自动化平台，串联所有步骤 |
| **Apify** | 抓取Amazon产品信息 |
| **Topview AI** | AI视频生成，图片+文案合成营销视频 |
| **Google Sheets** | ASIN列表管理和状态追踪 |

## 详细配置指南

完整配置步骤和节点说明：[WORKFLOW_SETUP.md](references/WORKFLOW_SETUP.md)

## 自动化脚本

- `scripts/init_pipeline.py` - 初始化流水线配置
- `scripts/validate_setup.py` - 验证配置完整性

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| 视频生成失败 | 检查Topview API额度、图片格式是否符合要求 |
| Google Sheets连接失败 | 确认Service Account有表格编辑权限 |
| 产品信息提取失败 | 检查Apify Actor运行状态、ASIN是否有效 |
| 导出超时 | 无水印导出耗时较长，可适当增加等待时间 |

## 进阶用法

- **批量处理** - 修改n8n Batch节点参数调整并发数
- **自定义模板** - 在Topview后台创建品牌专属视频模板
- **多语言支持** - 通过Apify提取多语言产品描述
- **定时触发** - 使用n8n Schedule节点实现定时批量处理
