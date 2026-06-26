# DataWorks Diagnoser 🔍

DataWorks 任务实例智能诊断工具 - 自动获取日志、分析错误、提供解决方案

## 功能特性

- ✅ **自动获取日志** - 通过阿里云 API 获取任务实例日志
- ✅ **智能错误识别** - 自动提取 ODPS、DataX、Java 异常等错误代码
- ✅ **AI 智能分析** - 分析错误原因，提供解决方案
- ✅ **明确的行动指引** - 每个错误都有"下一步"操作建议
- ✅ **简洁清晰的报告** - 无冗余信息，直击问题核心

## 支持的错误类型

| 类型 | 错误代码示例 | 自动识别 |
|------|----------|----------|
| ODPS SQL | `ODPS-0130071` 函数不存在 | ✅ |
| ODPS SQL | `ODPS-0130141` 类型转换错误 | ✅ |
| DataX | `MYSQLErrCode-02` 连接失败 | ✅ |
| Java | `NullPointerException` | ✅ |
| 通用错误 | `ERROR`, `FAILED` | ✅ |

## 安装方法

### 方法 1: OpenClaw Skill（推荐）

```bash
# 1. 下载 skill 包
# 将 dataworks-diagnoser.skill 放到 skills 目录
unzip dataworks-diagnoser.skill -d ~/.openclaw/skills/

# 2. 重启 OpenClaw 或重新加载 skills
openclaw gateway restart
```

### 方法 2: 直接使用脚本

```bash
# 1. 克隆或下载源码
git clone <repo-url>
cd dataworks-diagnoser

# 2. 安装依赖
pip3 install alibabacloud_dataworks_public20240518 alibabacloud_credentials

# 3. 配置阿里云 AK
export ALIBABA_CLOUD_ACCESS_KEY_ID=LTAI5t...
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=xxxxxx

# 4. 运行诊断
python3 scripts/dataworks_diagnose.py <实例 ID>
```

## 使用方法

### 基础用法

```bash
# 配置阿里云 AccessKey
export ALIBABA_CLOUD_ACCESS_KEY_ID=你的 AK
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=你的密钥

# 诊断任务实例
python3 scripts/dataworks_diagnose.py 1004057140616
```

### 输出示例

```
🔍 开始诊断 DataWorks 任务实例：1004057140616
📍 区域：cn-hangzhou
------------------------------------------------------------

📥 步骤 1/2: 获取任务日志...
✅ 日志获取成功
📋 RequestId: B7719DED-6DD1-5ACA-B3EC-A7CE943131DB

📊 任务摘要:
   ❌ FAILED: ODPS-0130071:[11,10] Semantic analysis exception

🔬 步骤 2/2: AI 智能分析中...
✅ 诊断完成

======================================================================
DataWorks 任务诊断报告
======================================================================
实例 ID: 1004057140616
发现错误：2 个

错误 1: ODPS - ODPS-0130071
错误信息:
  Semantic analysis exception - function or view 'bound_index' cannot be resolved
  位置：line 11, col 10

可能原因:
  • SQL 中使用了不存在的函数或视图

解决方案:
  1. 检查 SQL 第 line 11, col 10 处的函数
  2. 确认函数名称拼写正确
  3. 在 DataWorks 数据开发中测试该函数

下一步：在 DataWorks 数据开发面板试运行 SQL
======================================================================
```

### 高级用法

```bash
# 指定区域
python3 scripts/dataworks_diagnose.py 1004057140616 --region cn-shanghai

# 输出 JSON 格式
python3 scripts/dataworks_diagnose.py 1004057140616 --json

# 只分析日志文件（不需要 AK）
python3 scripts/analyze_error.py error.log

# 从管道读取日志
cat task.log | python3 scripts/analyze_error.py
```

## 前置要求

### 1. 阿里云 AccessKey

需要配置阿里云 AccessKey 才能获取任务日志：

**获取 AK：**
1. 登录 [阿里云 RAM 控制台](https://ram.console.aliyun.com/manage/ak)
2. 创建 AccessKey 或使用现有的
3. 记录 `AccessKey ID` 和 `AccessKey Secret`

**配置 AK（3 选 1）：**

```bash
# 方式 1: 环境变量（推荐）
export ALIBABA_CLOUD_ACCESS_KEY_ID=LTAI5t...
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=xxxxxx

# 方式 2: 配置文件
cat > ~/.alibabacloud/credentials << EOF
{
  "access_key_id": "LTAI5t...",
  "access_key_secret": "xxxxxx"
}
EOF

# 方式 3: 命令行参数
python3 scripts/dataworks_diagnose.py <实例 ID> \
  --access-key LTAI5t... \
  --access-secret xxxxxx
```

### 2. RAM 权限

AccessKey 需要以下权限：

```json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dataworks:GetTaskInstanceLog",
        "dataworks:QueryTask"
      ],
      "Resource": "*"
    }
  ]
}
```

### 3. Python 依赖

```bash
pip3 install alibabacloud_dataworks_public20240518 alibabacloud_credentials
```

## 文件结构

```
dataworks-diagnoser/
├── scripts/
│   ├── dataworks_diagnose.py      # 主程序：获取日志 + 分析
│   ├── fetch_instance_log.py      # 日志获取（官方 SDK）
│   ├── analyze_error.py           # 错误分析
│   └── diagnose_log.py            # 旧版诊断（兼容）
├── test_logs/                     # 测试日志样本
├── references/
│   └── error_codes.md             # 错误代码参考
├── AK_SETUP.md                    # AK 配置指南
├── QUICK_START.md                 # 快速开始
└── README.md                      # 本文档
```

## 故障排查

### "Credentials not found"

**原因：** 未配置 AK

**解决：**
```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID=你的 AK
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=你的密钥
```

### "InvalidAccessKeyId"

**原因：** AK ID 错误或已禁用

**解决：**
- 检查 AK ID 是否正确
- 在 RAM 控制台确认 AK 状态为"启用"

### "Forbidden"

**原因：** 权限不足

**解决：**
- 在 RAM 控制台授予 `dataworks:GetTaskInstanceLog` 权限

### "Instance not found"

**原因：** 实例 ID 错误或区域不匹配

**解决：**
- 确认实例 ID 正确
- 使用 `--region` 指定正确区域

## 安全提醒

⚠️ **重要安全事项：**

1. **不要使用主账号 AK** - 创建 RAM 子账号
2. **不要提交 AK 到 Git** - 使用 `.gitignore`
3. **定期轮换 AK** - 建议 90 天更换
4. **最小权限原则** - 只授予必要的 API 权限

## 常见问题

### Q: 支持哪些区域？

A: 支持所有阿里云区域，默认 `cn-hangzhou`。使用 `--region` 指定：
```bash
python3 scripts/dataworks_diagnose.py <实例 ID> --region cn-shanghai
```

### Q: 可以诊断历史任务吗？

A: 可以，只要任务日志还在阿里云保留期内（通常 30 天）。

### Q: 支持批量诊断吗？

A: 当前版本支持单个实例诊断。批量诊断可以写脚本循环调用：
```bash
for id in 1004057140616 1004057140617 1004057140618; do
  python3 scripts/dataworks_diagnose.py $id
done
```

### Q: 如何反馈问题？

A: 请提供：
- 实例 ID
- 完整错误信息
- 期望的行为

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0 | 2024-01-15 | 初始版本 |
| 1.1 | 2024-01-15 | 添加 ODPS 错误识别 |
| 1.2 | 2024-01-15 | 简化输出，移除假链接 |
| 1.3 | 2024-01-15 | 添加下一步行动指引 |

## 许可证

MIT License

## 联系方式

- GitHub: [你的 GitHub 链接]
- 邮箱：[你的邮箱]
- 阿里云市场：[产品链接]

---

**让 DataWorks 故障排查更简单！** 🚀
