---
name: finoview-report-weekly
description: 调用 finoview 期货研究报告 API 获取期货周度报告数据。使用这个技能当你需要获取特定日期或期货类别的研究报告，包括报告标题、作者、摘要、PDF 链接等信息。适用于期货市场分析、研究报告汇总、市场情报收集等场景。
---

# Finoview 期货周度报告 API

一个用于获取 finoview.com.cn 期货研究报告的技能。通过调用 API 获取指定日期和期货类别的研究报告列表。

## ⚠️ 首次使用配置

**在首次使用前，您需要配置 API 凭证：**

### 步骤 1：获取 API 凭证

联系 finoview.com.cn 获取您的 API 凭证（AppKey 和 AppSecret）。

### 步骤 2：配置环境变量

设置以下两个环境变量：

- `FINOVIEW_API_KEY` - 您的 API Key
- `FINOVIEW_API_SECRET` - 您的 API Secret

**配置方法：**

#### 临时配置（当前会话）

**Linux/Mac:**
```bash
export FINOVIEW_API_KEY="your_api_key_here"
export FINOVIEW_API_SECRET="your_api_secret_here"
```

**Windows:**
```cmd
set FINOVIEW_API_KEY="your_api_key_here"
set FINOVIEW_API_SECRET="your_api_secret_here"
```

#### 永久配置

将上述命令添加到您的 shell 配置文件中：

- **Linux/Mac (Bash):** 添加到 `~/.bashrc` 或 `~/.bash_profile`
- **Linux/Mac (Zsh):** 添加到 `~/.zshrc`
- **Windows:** 通过系统环境变量设置，或在 PowerShell 配置文件（`$PROFILE`）中添加

配置完成后，需要重启终端或执行 `source ~/.bashrc`（或相应文件）使配置生效。

### 验证配置

您可以运行以下 Python 命令验证配置是否成功：

```python
import os
print("API Key:", os.environ.get("FINOVIEW_API_KEY", "未配置"))
print("API Secret:", os.environ.get("FINOVIEW_API_SECRET", "未配置"))
```

如果看到"未配置"，请重新检查环境变量设置。

## API 端点信息

- **基础 URL**: `https://www.finoview.com.cn`
- **请求路径**: `/autoApi/foreign/report_list`
- **请求方式**: POST

## 使用脚本

使用 `scripts/api_call.py` 中的函数调用 API：

```python
from scripts.api_call import get_data_from_api

# 获取 2026 年 3 月 29 日的所有周度报告
reports = get_data_from_api("2026-03-29")

# 获取黑色金属类别的报告
reports = get_data_from_api("2026-03-29", "2502")

# 获取能源化工类别的报告
reports = get_data_from_api("2026-03-29", "2505")
```

## 请求参数

| 字段 | 类型 | 是否必需 | 说明 |
|------|------|----------|------|
| time | String | 是 | 报告查询日期，格式：YYYY-MM-DD |
| indCode | String | 否 | 期货类别代码（留空获取全部类别） |
| appkey | String | 是 | 从环境变量 `FINOVIEW_API_KEY` 读取 |
| appsecret | String | 是 | 从环境变量 `FINOVIEW_API_SECRET` 读取 |

## 响应数据格式

返回 JSON 格式的报告列表，主要字段包括：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 报告 ID |
| title | String | 报告标题 |
| author | String | 报告作者 |
| type | String | 报告类型（如：周度报告） |
| typeId | Integer | 类型 ID |
| indName | String | 期货类别名称 |
| indCode | String | 期货类别代码 |
| riskRating | Integer | 风险评级 |
| time | String | 报告时间 |
| summary | String | 报告摘要 |
| url | String | PDF 附件下载链接 |
| varietyNames | String | 品种名称 |

## 期货类别代码表

| 代码 | 期货类别名称 |
|------|-------------|
| 2501 | 贵金属 |
| 2502 | 黑色金属 |
| 2503 | 有色金属 |
| 2504 | 建筑材料 |
| 2505 | 能源化工 |
| 2508 | 软商品 |
| 2509 | 股指期货 |
| 2510 | 国债期货 |
| 2511 | 外汇期货 |
| 2512 | 农产品 |
| 2514 | 商品期货 |
| 2515 | 金融期货 |

## 使用示例

### 示例 1：获取 2026 年 3 月 29 日的所有周度报告

```python
from scripts.api_call import get_data_from_api, format_reports_to_markdown

reports = get_data_from_api("2026-03-29")
print(format_reports_to_markdown(reports, "2026-03-29"))
```

### 示例 2：获取 2026 年 3 月 29 日黑色金属类别的报告

```python
from scripts.api_call import get_data_from_api

# 黑色金属（螺纹钢、铁矿石、焦炭等）
reports = get_data_from_api("2026-03-29", "2502")
for report in reports:
    print(f"标题：{report['title']}")
    print(f"作者：{report['author']}")
    print(f"摘要：{report['summary'][:100]}...")
    print(f"PDF: {report['url']}")
    print("-" * 80)
```

### 示例 3：获取 2026 年 3 月 29 日能源化工类别的报告

```python
from scripts.api_call import get_data_from_api

# 能源化工（原油、PVC、甲醇等）
reports = get_data_from_api("2026-03-29", "2505")
for report in reports:
    print(f"标题：{report['title']}")
    print(f"作者：{report['author']}")
    print(f"摘要：{report['summary'][:100]}...")
    print(f"PDF: {report['url']}")
```

### 示例 4：生成 Markdown 表格输出

```python
from scripts.api_call import get_data_from_api, format_reports_to_table

reports = get_data_from_api("2026-03-29", "2502")  # 黑色金属
table = format_reports_to_table(reports)
print(table)
```

### 示例 5：检查凭证配置状态

```python
from scripts.api_call import check_credentials_status

# 检查 API 凭证是否已配置
if check_credentials_status():
    reports = get_data_from_api("2026-03-29")
    print(f"成功获取 {len(reports)} 篇报告")
else:
    print("请配置 API 凭证后再使用此功能")
```

## API 返回数据示例

```json
[
    {
        "id": 211501,
        "title": "通胀扰动长债，短债相对稳定",
        "author": "张粲东，国债期货",
        "typeId": 120442,
        "type": "周度报告",
        "indName": null,
        "indCode": "2510",
        "riskRating": 3,
        "time": "2026-03-29",
        "summary": "★一周复盘：国债期货震荡\n本周（03.23-03.29）国债期货震荡...",
        "url": "https://www.finoview.com.cn/group1/M00/05/41/xxx.pdf",
        "varietyNames": "国债期货"
    }
]
```

## 输出格式建议

### Markdown 表格格式

| 标题 | 作者 | 类型 | 类别 | 日期 | PDF 链接 |
|------|------|------|------|------|----------|
| 通胀扰动长债，短债相对稳定 | 张粲东，国债期货 | 周度报告 | 国债期货 | 2026-03-29 | [PDF](url) |

### Markdown 详细格式

```markdown
## Finoview 期货研究报告 - 2026-03-29

**报告数量**: 5

### 1. 通胀扰动长债，短债相对稳定
- **作者**: 张粲东，国债期货
- **类型**: 周度报告
- **类别**: 国债期货
- **日期**: 2026-03-29
- **摘要**: ★一周复盘：国债期货震荡...
- **PDF**: [下载 PDF](url)
```

## 调用注意事项

1. **日期格式**：必须使用 `YYYY-MM-DD` 格式，如 `2026-03-29`
2. **API Key 安全**：生产环境中应使用环境变量存储 appkey 和 appsecret（已实现）
3. **错误处理**：使用 `get_data_from_api_safe()` 函数处理异常情况
4. **并发限制**：注意 API 调用的频率限制，避免频繁请求
5. **凭证管理**：不要在代码中硬编码凭证，使用环境变量
6. **首次使用**：首次使用时会检查凭证配置并提供友好的配置指引

## 错误处理

```python
from scripts.api_call import get_data_from_api_safe

reports = get_data_from_api_safe("2026-03-29", "2502")
if not reports:
    print("获取报告失败，请检查日期、类别代码或 API 凭证配置")
else:
    print(f"成功获取 {len(reports)} 篇报告")
```

## 常见问题

### Q: 遇到"API 凭证未配置"错误怎么办？

A: 请按照以下步骤配置：

1. 确认您已获取 finoview 的 API 凭证
2. 在终端或系统中设置环境变量 `FINOVIEW_API_KEY` 和 `FINOVIEW_API_SECRET`
3. 确保应用重启以读取新配置的环境变量

### Q: 凭证配置后仍然报错？

A: 检查以下几点：

1. 确认环境变量已正确设置：`print(os.environ.get("FINOVIEW_API_KEY"))`
2. 确保引号正确使用（Windows 用双引号，Linux/Mac 单双引号均可）
3. 确认应用已重启以读取环境变量
4. 检查凭证是否有效（是否过期或被禁用）

### Q: 如何安全地管理 API 凭证？

A: 建议做法：

1. **使用环境变量**：不要在代码或配置文件中硬编码凭证
2. **使用密钥管理工具**：如 AWS Secrets Manager、HashiCorp Vault 等
3. **限制访问权限**：只让必要的服务/人员访问凭证
4. **定期轮换**：定期更换 API 密钥
5. **使用不同环境**：开发、测试、生产环境使用不同的凭证

## 可用函数

| 函数 | 说明 |
|------|------|
| `get_data_from_api(date, indCode)` | 调用 API 获取报告列表 |
| `get_data_from_api_safe(date, indCode)` | 带错误处理的 API 调用 |
| `format_reports_to_markdown(reports, date)` | 格式化为 Markdown 详细列表 |
| `format_reports_to_table(reports)` | 格式化为 Markdown 表格 |
| `check_credentials_status()` | 检查 API 凭证是否已配置 |
| `get_credentials()` | 从环境变量获取 API 凭证 |
