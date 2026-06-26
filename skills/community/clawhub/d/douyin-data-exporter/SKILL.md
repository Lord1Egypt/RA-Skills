---
name: douyin-data-exporter
description: 抖音数据导出技能 - 获取用户主页视频数据
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python"] },
        "install":
          [
            {
              "id": "python",
              "kind": "python",
              "label": "Install Python",
            },
          ],
      },
  }
---

## 抖音数据导出技能（含投流数据）

### 功能

本技能通过 TikHub API 获取指定抖音用户的主页视频列表，支持分页和自动翻页；同时可选通过 BOSS 平台接口获取该账号的投流订单导出数据（需提供独立 Token）。所有数据将保存为 JSON 和/或 CSV/Excel 格式到工作区。

### 使用方法

基于真实的 Python 路径，以下为参考命令：

powershell
```
& "F:\\python 3.10\\python.exe" C:\\Users\\EDY\\.openclaw\\skills\\douyin-data-exporter\\export.py `
    --sec-user-id "用户的 sec_user_id" `
    --account-name "账号名称" `
    [--max-videos 100] `
    [--export-format both] `
    [--douplus-token "投流API Token"] `
    [--douplus-customer-id "336"]
```



### 参数说明

| 参数                    | 必填 | 说明                                               |
| :---------------------- | :--- | :------------------------------------------------- |
| `--sec-user-id`         | 是   | 抖音用户的 sec_user_id（从浏览器或开发者工具获取） |
| `--account-name`        | 是   | 账号名称，用于命名输出文件                         |
| `--max-videos`          | 否   | 最大获取视频数量，默认 100                         |
| `--export-format`       | 否   | 视频导出格式：`json`、`csv` 或 `both`，默认 `both` |
| `--douplus-token`       | 否   | 投流 API 的 Bearer Token（从浏览器获取）           |
| `--douplus-customer-id` | 否   | 投流 API 的 customerId（如 `336`，可从浏览器获取） |

> 注：若同时提供命令行参数和环境变量，命令行参数优先。

### 输出

所有输出文件保存在 `C:\Users\EDY\.openclaw\workspace\data` 目录。

| 数据类型     | 文件格式            | 文件名示例                                                   |
| :----------- | :------------------ | :----------------------------------------------------------- |
| 视频列表     | JSON / CSV          | `{account_name}_videos_{timestamp}.json` / `.csv`            |
| 投流订单数据 | Excel (xlsx) / JSON | `{account_name}_投流数据_{timestamp}.xlsx`（若 API 返回 Excel） `{account_name}_投流数据_{timestamp}.json`（若返回 JSON） |
| 汇总报告     | JSON                | `{account_name}_导出汇总报告_{timestamp}.json`               |

### 配置要求

#### 1. 获取 TikHub Token（用于视频数据）

1. 访问 [TikHub 官网](https://user.tikhub.io/register) 注册并登录。
2. 在个人中心获取您的 API Token。
3. 设置环境变量 `TIKHUB_TOKEN`，或直接在脚本中修改 `TIKHUB_TOKEN` 变量（不推荐硬编码）。

> ⚠️ 官网链接可能需登录，若无法访问请确认网络或账号状态。

#### 2. 获取投流 API Token 和 Customer ID（用于投流数据）

- **Token**：联系平台管理员或从 BOSS 系统后台获取有效的 Bearer Token。
- **Customer ID**：通常为数字标识（如 `336`），需向平台方确认。