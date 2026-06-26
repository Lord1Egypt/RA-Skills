# PDF报告生成与飞书推送功能使用指南

## 功能概述

本Skill提供了完整的PDF报告生成和飞书推送功能，实现招投标信息的自动化日报生成和推送。

---

## PDF报告生成

### 功能特性

- ✅ 自动从数据库查询指定日期的数据
- ✅ 按区域分类展示（盐南高新区、经开区、区域内）
- ✅ 包含汇总统计表格
- ✅ 支持中文字体显示
- ✅ 自动保存到指定目录
- ✅ 支持单日报和日期范围报告

### 使用方法

#### 方法1：通过Python代码调用

```python
from scripts.pdf_generator import PDFGenerator
from datetime import datetime

# 创建PDF生成器
generator = PDFGenerator()

# 生成今日日报
today = datetime.now().strftime('%Y-%m-%d')
pdf_file = generator.generate_daily_report(today)

if pdf_file:
    print(f"PDF报告已生成: {pdf_file}")
else:
    print("PDF报告生成失败或无数据")
```

#### 方法2：通过命令行调用

```python
import sys
sys.path.insert(0, '/workspace/projects/bidding-crawler')
from scripts.pdf_generator import PDFGenerator

generator = PDFGenerator()
pdf_file = generator.generate_daily_report('2026-04-12')
```

### 报告内容

PDF报告包含以下内容：

1. **标题**：招投标信息日报
2. **日期**：报告日期
3. **汇总统计**：
   - 总项目数
   - 盐南高新区项目数
   - 经开区项目数
   - 区域内项目数
   - 总预算
4. **项目明细**：按区域分类展示，包含：
   - 项目名称
   - 发布日期
   - 预算
   - 采购人
   - 来源

### 文件存储

- **存储目录**：`./招投标数据/daily/`
- **文件命名**：`招投标信息日报_YYYY-MM-DD.pdf`
- **示例**：`招投标信息日报_2026-04-12.pdf`

---

## 飞书推送

### 功能特性

- ✅ 支持文本消息推送
- ✅ 支持Markdown格式消息
- ✅ 支持日报摘要推送
- ✅ 自动更新推送状态
- ✅ 支持告警消息推送

### 使用方法

#### 方式1：使用Webhook（推荐）

```python
from scripts.feishu_notifier import FeishuNotifier

# 初始化通知器
notifier = FeishuNotifier()  # 需要设置环境变量 FEISHU_WEBHOOK_URL

# 发送文本消息
notifier.send_text_message("这是一条测试消息")

# 发送日报
notifier.send_daily_report('2026-04-12', projects, pdf_file)
```

#### 方式2：使用飞书开放平台API

```python
from scripts.feishu_notifier import FeishuOpenAPI

# 初始化API客户端
api = FeishuOpenAPI(
    app_id='cli_xxxxxxxxxxxxxxxx',
    app_secret='xxxxxxxxxxxxxxxxxxxxxxxx'
)

# 上传文件
file_key = api.upload_file('./招投标数据/daily/招投标信息日报_2026-04-12.pdf')

# 发送文件消息
api.send_file_message('oc_xxxxxxxxxxxxxxxx', file_key)
```

### 配置步骤

#### 1. 创建飞书机器人（Webhook方式）

1. 在飞书群聊中，点击群设置 → 群机器人 → 添加机器人
2. 选择"自定义机器人"
3. 设置机器人名称和头像
4. 复制生成的Webhook URL
5. 设置环境变量：
   ```bash
   export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxxxxxxxxxx"
   ```

#### 2. 创建飞书应用（开放平台方式）

1. 访问 https://open.feishu.cn/
2. 创建企业自建应用
3. 获取App ID和App Secret
4. 配置应用权限：
   - 获取群聊信息
   - 发送消息
   - 上传文件
5. 设置环境变量：
   ```bash
   export FEISHU_APP_ID="cli_xxxxxxxxxxxxxxxx"
   export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxx"
   ```

---

## 定时任务调度

### 功能特性

- ✅ 支持每日定时执行
- ✅ 支持自定义Cron表达式
- ✅ 自动执行完整流程：采集 → 生成PDF → 发送通知
- ✅ 支持立即执行
- ✅ 完善的日志记录

### 使用方法

#### 命令行方式

```bash
# 立即执行一次
python scripts/scheduler.py --mode once

# 定时执行（每天9:00）
python scripts/scheduler.py --mode schedule --cron "0 9 * * *"

# 自定义时间（每天18:00）
python scripts/scheduler.py --mode schedule --cron "0 18 * * *"
```

#### Python代码方式

```python
from scripts.scheduler import TaskScheduler

# 创建调度器
scheduler = TaskScheduler()

# 添加每日9:00定时任务
scheduler.add_daily_job(cron_expression="0 9 * * *")

# 启动调度器
scheduler.start()

# 或者立即执行一次
scheduler.run_once()
```

### Cron表达式说明

Cron表达式格式：`分 时 日 月 周`

常用示例：
- `0 9 * * *`：每天9:00执行
- `0 18 * * *`：每天18:00执行
- `0 */6 * * *`：每6小时执行一次
- `0 9 * * 1`：每周一9:00执行

---

## 完整工作流程

### 标准流程

```
1. 采集数据
   ↓
2. 生成PDF报告
   ↓
3. 发送飞书通知
   ↓
4. 更新推送状态
```

### 代码实现

```python
from scripts.scheduler import TaskScheduler

# 创建调度器
scheduler = TaskScheduler()

# 执行完整流程
scheduler.run_daily_task()
```

### 执行步骤

1. **采集数据**
   - 调用所有采集器
   - 采集指定日期的数据
   - 存储到数据库

2. **生成PDF报告**
   - 查询数据库中的数据
   - 按区域分类
   - 生成PDF文件
   - 保存到指定目录

3. **发送飞书通知**
   - 查询数据库中的数据
   - 生成日报摘要
   - 发送到飞书群聊
   - 更新推送状态

4. **更新推送状态**
   - 将已推送的项目标记为已推送
   - 记录推送时间

---

## 测试与验证

### 测试PDF生成

```python
python scripts/test_pdf_feishu.py
```

### 测试飞书推送

```python
from scripts.feishu_notifier import FeishuNotifier

notifier = FeishuNotifier()
notifier.send_text_message("测试消息")
```

### 测试完整流程

```bash
python scripts/scheduler.py --mode once
```

---

## 常见问题

### Q1: PDF中文显示乱码？

**A**: 系统会自动查找并注册中文字体，如果仍然乱码，请检查：
- 系统是否安装了中文字体
- 字体路径是否正确

### Q2: 飞书通知发送失败？

**A**: 请检查：
- Webhook URL是否正确
- 网络连接是否正常
- 消息格式是否符合要求

### Q3: 定时任务不执行？

**A**: 请检查：
- Cron表达式是否正确
- 系统时间是否准确
- 进程是否正常运行

### Q4: 如何修改报告样式？

**A**: 编辑 `scripts/pdf_generator.py` 文件，修改表格样式和字体配置。

### Q5: 如何自定义推送消息格式？

**A**: 编辑 `scripts/feishu_notifier.py` 文件，修改 `send_daily_report` 方法中的消息模板。

---

## 配置文件

### 环境变量

```bash
# 飞书Webhook URL（推荐）
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxxxxxxxxxx"

# 飞书开放平台应用凭证（高级）
export FEISHU_APP_ID="cli_xxxxxxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxx"
```

### 配置文件示例

```bash
# .env 文件
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 监控与日志

### 日志文件

- 采集日志：`./招投标数据/logs/crawler_YYYY-MM-DD.log`
- 调度器日志：`./招投标_data/logs/scheduler.log`
- 测试报告：`./招投标_data/logs/test_report_YYYY-MM-DD_HH-MM-SS.txt`

### 监控指标

- 采集成功率
- 数据完整性
- PDF生成成功率
- 飞书推送成功率
- 推送延迟

---

## 扩展功能

### 自定义报告模板

编辑 `scripts/pdf_generator.py`，修改 `_create_region_section` 方法，自定义报告样式。

### 添加更多推送渠道

参考 `scripts/feishu_notifier.py`，实现其他推送方式（如邮件、企业微信等）。

### 多群聊推送

创建多个 `FeishuNotifier` 实例，配置不同的Webhook URL。

---

## 参考文档

- [飞书推送配置说明](references/飞书推送配置说明.md)
- [全面测试报告](references/全面测试报告.md)
- [网页结构变化检测与自修正机制](references/网页结构变化检测与自修正机制.md)

---

**文档版本**：1.0.0
**最后更新**：2026-04-12
