## 授权码协议确认

用户购买、领取、发送、输入、提交、激活或使用 BossSkill 授权码，即表示已阅读、理解并同意 `USER_AGREEMENT.md`、`PRIVACY.md` 和 `LICENSE_NOTICE.md`。

# BossSkill 商业版授权说明

当前商业版只区分两种状态：

- 免费版：没有授权码或授权无效。
- 授权版：授权码有效，开放商业能力。

授权时长由授权中心创建：

- `1_month`：1个月
- `1_quarter`：1季度
- `1_year`：1年

## 免费版保留

- 基础客户记录
- 基础团队记录
- 基础任务记录
- 简单 Web 控制台
- 基础训练手册
- 少量本地规则

## 授权版开放

- 老板秘书智能判断
- 行业深度包
- 持续学习知识库
- 自动测试样例库
- 高级经营诊断
- 老板偏好学习
- 误判纠错记忆
- SOP 和话术沉淀
- 后续私有模型/agent 接入

## 激活授权

```powershell
python scripts\startup_os_db.py activate-license --db startup_os.sqlite3 --license-key YOUR_LICENSE_KEY
```

查看授权状态：

```powershell
python scripts\startup_os_db.py license-status --db startup_os.sqlite3
```

也可以使用环境变量：

```powershell
$env:BOOSKILL_LICENSE_KEY="YOUR_LICENSE_KEY"
```

## 授权中心

默认授权中心：

```text
https://bt.fanfan.la
```

授权缓存默认保留 72 小时。短时间断网时，授权版能力可以继续使用；超过缓存时间后需要重新联网校验。
## 隐私与数据传输

授权校验只发送授权码、设备标识和功能名，不要求客户上传本地数据库。

授权版云端能力默认只接收当次命令参数，例如用户本次输入的问题、命令名和授权信息；不会自动上传完整客户库、团队库、任务库、人脉库或本地 SQLite 文件。

如果用户需要生成公网 Word/PDF 下载链接，系统只上传用户明确指定的文档文件，链接默认短期有效。

## 授权版新增：对话经营情报

授权版支持从老板的日常描述里识别经营信号，例如客户异议、成交、流失、客户沉默、员工风险、员工训练、人脉资源、合作机会和任务延期。

示例：

```powershell
python scripts\startup_os_db.py conversation-intelligence --db startup_os.sqlite3 --text "李总今天说预算有点高，想再看看案例，下周三再聊"
```

该能力由官方云端商业核心提供，公开客户端只保留授权、基础记录和云端调用入口。

