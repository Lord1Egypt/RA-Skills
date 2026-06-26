# ASIN营销视频流水线 - 详细配置指南

## 目录
1. [环境准备](#环境准备)
2. [Google Sheets 配置](#google-sheets-配置)
3. [Topview AI 配置](#topview-ai-配置)
4. [Apify 配置](#apify-配置)
5. [n8n 工作流导入](#n8n-工作流导入)
6. [凭证配置](#凭证配置)
7. [运行测试](#运行测试)

---

## 环境准备

### 1. 安装n8n

**Docker方式（推荐）**
```bash
docker run -it --rm \n  --name n8n \n  -p 5678:5678 \n  -v ~/.n8n:/home/node/.n8n \n  n8nio/n8n
```

**npm方式**
```bash
npm install n8n -g
n8n start
```

访问 http://localhost:5678 进入n8n编辑器

### 2. 注册必要服务

| 服务 | 注册地址 | 需要获取 |
|------|---------|---------|
| Topview AI | https://www.topview.ai | API Key |
| Apify | https://apify.com | API Token |
| Google Cloud | https://console.cloud.google.com | Service Account JSON |

---

## Google Sheets 配置

### 1. 创建表格

1. 访问 https://sheets.new 创建新表格
2. 重命名为 "ASIN视频管理"
3. 按以下格式设置表头：

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| ASIN | 产品名称 | 产品图片URL | 视频链接 | 审核状态 | 任务ID |

### 2. 获取表格ID

表格URL格式：`https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`

复制 `{SPREADSHEET_ID}` 部分，这是你的 `GOOGLE_SHEETS_ID`

### 3. 设置Google Cloud项目

1. 访问 https://console.cloud.google.com
2. 创建新项目或选择现有项目
3. 启用 Google Sheets API：
   - 进入 "API和服务" > "库"
   - 搜索 "Google Sheets API"
   - 点击 "启用"

### 4. 创建Service Account

1. 进入 "IAM和管理" > "服务账号"
2. 点击 "创建服务账号"
3. 填写名称（如：n8n-sheets-access）
4. 创建密钥：
   - 选择JSON格式
   - 下载保存密钥文件

### 5. 分享表格权限

1. 打开表格，点击右上角 "分享"
2. 添加Service Account邮箱（格式：`xxx@project-id.iam.gserviceaccount.com`）
3. 权限设为 "编辑者"

---

## Topview AI 配置

### 1. 获取API Key

1. 登录 https://www.topview.ai
2. 进入 "API" 或 "开发者" 页面
3. 创建新的API Key
4. 复制保存API Key

### 2. 创建视频模板（可选）

如需使用自定义模板：
1. 在Topview后台创建营销视频模板
2. 记录模板ID（如 `marketing_template_01`）
3. 在n8n工作流中替换默认模板ID

### 3. API接口说明

**Base URL**: `https://api.topview.ai`

主要接口：
- `POST /v1/m2v/image/upload` - 上传图片
- `POST /v1/m2v/task` - 创建视频任务
- `GET /v1/m2v/task/{task_id}` - 查询任务状态
- `POST /v1/m2v/task/export` - 导出无水印版

---

## Apify 配置

### 1. 获取API Token

1. 登录 https://console.apify.com
2. 进入 "Settings" > "Integrations"
3. 复制 Personal API Token

### 2. 配置Amazon Scraper

工作流使用的是 `epctex~amazon-product-scraper` Actor：

- **免费额度**：每月有免费计算单元
- **付费方案**：超出后按使用量计费
- **输入参数**：
  - `asin`: Amazon产品ID
  - `country`: 国家代码（如 US, UK, DE）

### 3. 测试Scraper

在Apify控制台测试：
```json
{
  "asin": "B08N5WRWNW",
  "country": "US"
}
```

---

## n8n 工作流导入

### 1. 导入预览版工作流

1. 在n8n编辑器中，点击左侧菜单 "Workflows"
2. 点击右上角 "Import from File"
3. 选择 `n8n-workflow-preview.json`
4. 重命名工作流为 "ASIN视频生成-预览版"

### 2. 导入导出版工作流

重复上述步骤，导入 `n8n-workflow-export.json`
重命名为 "ASIN视频导出-正式版"

### 3. 设置环境变量

在n8n Settings 或 .env 文件中设置：
```bash
GOOGLE_SHEETS_ID=your_spreadsheet_id_here
```

---

## 凭证配置

### 1. 配置Google Sheets凭证

1. 在n8n编辑器，点击右上角 "Settings" 图标
2. 进入 "Credentials" 标签
3. 点击 "Add Credential"
4. 选择 "Google Sheets OAuth2 API"
5. 导入Service Account JSON文件
6. 保存凭证，命名为 `googleSheetsOAuth2`

### 2. 配置Topview API凭证

1. 添加新凭证，选择 "HTTP Header Auth"
2. 配置：
   - Name: `topviewApiKey`
   - Value: `Bearer your_topview_api_key`
3. 保存

### 3. 配置Apify API凭证

1. 添加新凭证，选择 "HTTP Header Auth"
2. 配置：
   - Name: `apifyApiKey`
   - Value: `your_apify_api_token`
3. 保存

---

## 运行测试

### 1. 添加测试数据

在Google Sheets添加一行测试数据：
| ASIN | 产品名称 | 产品图片URL | 视频链接 | 审核状态 | 任务ID |
|------|---------|------------|---------|---------|--------|
| B08N5WRWNW | | | | | |

### 2. 运行预览版工作流

1. 打开 "ASIN视频生成-预览版" 工作流
2. 点击 "Execute Workflow"
3. 观察节点执行情况（绿色=成功，红色=失败）
4. 检查Google Sheets是否更新了视频链接

### 3. 运行导出版工作流

1. 在Sheets中将审核状态改为 "通过"
2. 打开 "ASIN视频导出-正式版" 工作流
3. 点击 "Execute Workflow"
4. 等待完成后检查最终视频链接

---

## 常见问题

### Q: 视频生成超时怎么办？
A: 增加等待节点的等待时间，或在Topview后台查看任务队列状态。

### Q: Google Sheets连接失败？
A: 检查：
- Service Account是否有表格编辑权限
- Google Sheets API是否已启用
- 表格ID是否正确

### Q: Apify返回空数据？
A: 检查：
- ASIN是否有效
- 国家代码是否正确
- 计算单元是否充足

### Q: 如何批量处理多个ASIN？
A: 在n8n中使用 "Split in Batches" 节点，或使用Schedule触发器定时执行。

---

## 进阶配置

### 启用定时执行

1. 将触发器从 Manual Trigger 改为 Schedule Trigger
2. 设置Cron表达式，如每小时执行一次：
   ```
   0 * * * *
   ```

### 添加邮件通知

在流程末尾添加 "Send Email" 节点，配置SMTP服务器，实现完成后自动通知。

### 多语言支持

修改Apify节点参数：
```json
{
  "asin": "={{ $json['ASIN'] }}",
  "country": "={{ $