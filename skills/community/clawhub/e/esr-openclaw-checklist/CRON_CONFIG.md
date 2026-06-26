# ESR安全检查定时任务配置指南 v3.2.1

## 🎯 定时任务概述

### 功能说明
- **自动执行**: 每天17:00自动运行安全检查
- **钉钉报告**: 自动发送格式化报告到指定钉钉群
- **完成通知**: AI代理回复完成消息
- **无需干预**: 完全自动化，无需人工操作

### 技术架构
```
OpenClaw Cron Scheduler
        ↓
触发定时任务 (0 17 * * *)
        ↓
启动AI代理会话
        ↓
执行Python脚本 (openclaw_checklist_scheduled.py)
        ↓
    ├── 执行8项安全检查
    ├── 格式化钉钉消息
    └── 发送到钉钉群
        ↓
AI代理回复完成消息
        ↓
钉钉群收到安全检查报告
```

## ⚙️ 详细配置参数

### 1. 核心定时任务配置
```bash
openclaw cron add \
  --name "ESR每日安全检查" \
  --cron "0 17 * * *" \
  --tz "Asia/Shanghai" \
  --message "执行Python脚本 ~/.openclaw/skills/ESR_openclaw-checklist-v3.2/scripts/openclaw_checklist_scheduled.py 并在完成后输出：ESR每日自动安全检查已成功执行完成。" \
  --announce \
  --channel dingtalk \
  --to "cid8NuHF/3BALK8ub6oKUf0Dw=="
```

### 2. 参数详解

#### --name "ESR每日安全检查"
- **作用**: 定时任务名称
- **要求**: 唯一标识，便于管理
- **建议**: 保持原名，便于识别

#### --cron "0 17 * * *"
- **格式**: `分 时 日 月 周`
- **解释**: 每天17:00执行
- **示例**:
  - `0 9 * * *` = 每天9:00
  - `0 17 * * 1-5` = 工作日17:00
  - `0 0,12 * * *` = 每天0点和12点

#### --tz "Asia/Shanghai"
- **作用**: 时区设置
- **支持**: IANA时区名称
- **常用**:
  - `Asia/Shanghai` = 中国标准时间
  - `Asia/Tokyo` = 日本时间
  - `America/New_York` = 美国东部时间
  - `Europe/London` = 伦敦时间

#### --message "..."
- **内容**: AI代理执行指令
- **结构**:
  1. 执行Python脚本命令
  2. 完成后输出指定文本
- **关键**: 必须包含完整路径

#### --announce
- **作用**: 启用结果通知
- **效果**: 执行完成后发送通知
- **必须**: 与 `--channel` 和 `--to` 配合使用

#### --channel dingtalk
- **作用**: 通知渠道
- **支持**: dingtalk, telegram, discord等
- **要求**: 渠道插件必须已启用

#### --to "cid8NuHF/3BALK8ub6oKUf0Dw=="
- **作用**: 钉钉群ID
- **获取**: 钉钉群设置中查看
- **注意**: 必须用双引号包裹

## 🔧 安装后配置步骤

### 步骤1: 验证技能安装
```bash
# 检查技能是否安装成功
openclaw skills list | grep -i "esr"

# 预期输出
# ESR_openclaw-checklist-v3.2
```

### 步骤2: 手动测试技能
```bash
# 测试安全检查功能
运行ESR安全检查

# 预期: 看到8项检查结果和信息安全提示
```

### 步骤3: 配置定时任务（如未自动配置）
```bash
# 获取技能安装路径
SKILL_PATH=$(openclaw skills list --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for skill in data:
    if 'ESR_openclaw-checklist' in skill.get('name', ''):
        print(skill.get('path', ''))
        break
")

# 创建定时任务
openclaw cron add \
  --name "ESR每日安全检查" \
  --cron "0 17 * * *" \
  --tz "Asia/Shanghai" \
  --message "执行Python脚本 $SKILL_PATH/scripts/openclaw_checklist_scheduled.py 并在完成后输出：ESR每日自动安全检查已成功执行完成。" \
  --announce \
  --channel dingtalk \
  --to "cid8NuHF/3BALK8ub6oKUf0Dw=="
```

### 步骤4: 验证定时任务
```bash
# 查看定时任务列表
openclaw cron list

# 预期看到
# ESR每日安全检查 (0 17 * * * Asia/Shanghai)

# 立即测试定时任务
openclaw cron list --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for job in data.get('jobs', []):
    if 'ESR每日安全检查' in job.get('name', ''):
        print('任务ID:', job['id'])
        import subprocess
        subprocess.run(['openclaw', 'cron', 'run', job['id']])
        break
"
```

## 🛠️ 自定义配置指南

### 1. 修改执行时间
```bash
# 删除原有任务
openclaw cron list --json | python3 -c "
import json, sys, subprocess
data = json.load(sys.stdin)
for job in data.get('jobs', []):
    if 'ESR每日安全检查' in job.get('name', ''):
        subprocess.run(['openclaw', 'cron', 'remove', job['id']])
"

# 创建新时间任务（例如每天9:00）
openclaw cron add \
  --name "ESR每日安全检查" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --message "执行Python脚本 ~/.openclaw/skills/ESR_openclaw-checklist-v3.2/scripts/openclaw_checklist_scheduled.py 并在完成后输出：ESR每日自动安全检查已成功执行完成。" \
  --announce \
  --channel dingtalk \
  --to "cid8NuHF/3BALK8ub6oKUf0Dw=="
```

### 2. 修改钉钉群ID
```bash
# 编辑配置文件
nano ~/.openclaw/skills/ESR_openclaw-checklist-v3.2/config.json

# 修改 dingtalk_group_id 字段
# "dingtalk_group_id": "新的钉钉群ID"

# 重启OpenClaw服务
openclaw gateway restart

# 重新创建定时任务（使用新群ID）
openclaw cron add \
  --name "ESR每日安全检查" \
  --cron "0 17 * * *" \
  --tz "Asia/Shanghai" \
  --message "执行Python脚本 ~/.openclaw/skills/ESR_openclaw-checklist-v3.2/scripts/openclaw_checklist_scheduled.py 并在完成后输出：ESR每日自动安全检查已成功执行完成。" \
  --announce \
  --channel dingtalk \
  --to "新的钉钉群ID"
```

### 3. 多时段执行
```bash
# 上午9:00执行
openclaw cron add \
  --name "ESR上午安全检查" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --message "执行Python脚本 ~/.openclaw/skills/ESR_openclaw-checklist-v3.2/scripts/openclaw_checklist_scheduled.py 并在完成后输出：ESR上午自动安全检查已成功执行完成。" \
  --announce \
  --channel dingtalk \
  --to "cid8NuHF/3BALK8ub6oKUf0Dw=="

# 下午17:00执行
openclaw cron add \
  --name "ESR下午安全检查" \
  --cron "0 17 * * *" \
  --tz "Asia/Shanghai" \
  --message "执行Python脚本 ~/.openclaw/skills/ESR_openclaw-checklist-v3.2/scripts/openclaw_checklist_scheduled.py 并在完成后输出：ESR下午自动安全检查已成功执行完成。" \
  --announce \
  --channel dingtalk \
  --to "cid8NuHF/3BALK8ub6oKUf0Dw=="
```

## 🔍 故障诊断

### 1. 定时任务未执行
```bash
# 检查Cron服务状态
openclaw cron status

# 检查任务列表
openclaw cron list --json

# 检查任务详情
openclaw cron list --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for job in data.get('jobs', []):
    if 'ESR' in job.get('name', ''):
        print(json.dumps(job, indent=2, ensure_ascii=False))
"

# 手动触发测试
openclaw cron run [任务ID]
```

### 2. 钉钉消息未发送
```bash
# 检查钉钉插件状态
openclaw config get channels.dingtalk

# 测试钉钉连接
openclaw message send --channel dingtalk --to "测试ID" --message "定时任务测试"

# 检查Python脚本中的钉钉发送逻辑
grep -n "send_to_dingtalk" ~/.openclaw/skills/ESR_openclaw-checklist-v3.2/scripts/openclaw_checklist_scheduled.py
```

### 3. AI代理执行失败
```bash
# 测试AI代理命令执行
运行ESR安全检查

# 检查Python脚本权限
ls -la ~/.openclaw/skills/ESR_openclaw-checklist-v3.2/scripts/

# 检查Python环境
python3 --version
cd ~/.openclaw/skills/ESR_openclaw-checklist-v3.2 && python3 scripts/openclaw_checklist_scheduled.py
```

### 4. 时区问题
```bash
# 检查系统时区
date
timedatectl

# 检查OpenClaw时区配置
openclaw config get gateway.timezone

# 验证Cron时区
openclaw cron list --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for job in data.get('jobs', []):
    if 'ESR' in job.get('name', ''):
        print('任务:', job['name'])
        print('时区:', job.get('schedule', {}).get('tz', '未设置'))
"
```

## 📊 监控和维护

### 1. 查看执行历史
```bash
# 获取任务ID
TASK_ID=$(openclaw cron list --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for job in data.get('jobs', []):
    if 'ESR每日安全检查' in job.get('name', ''):
        print(job['id'])
        break
")

# 查看运行历史
openclaw cron runs --id $TASK_ID
```

### 2. 检查日志
```bash
# OpenClaw服务日志
openclaw logs --limit 100 | grep -i "cron\|ESR"

# 定时任务专用日志
openclaw cron runs --id $TASK_ID --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for entry in data.get('entries', []):
    print('时间:', entry.get('startedAt'))
    print('状态:', entry.get('status'))
    print('输出:', entry.get('output', '')[:200])
    print('---')
"
```

### 3. 定期维护
```bash
# 每月清理旧的历史记录
openclaw cron runs --id $TASK_ID --json | python3 -c "
import json, sys, time
data = json.load(sys.stdin)
month_ago = time.time() * 1000 - 30 * 24 * 60 * 60 * 1000
old_runs = [e for e in data.get('entries', []) if e.get('startedAt', 0) < month_ago]
print(f'找到 {len(old_runs)} 个30天前的历史记录')
"

# 检查技能更新
openclaw skills list --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for skill in data:
    if 'ESR' in skill.get('name', ''):
        print('技能:', skill.get('name'))
        print('路径:', skill.get('path'))
        print('---')
"
```

## ✅ 验证清单

安装完成后，请验证：

1. [ ] 技能安装成功：`openclaw skills list | grep ESR`
2. [ ] 手动执行正常：`运行ESR安全检查`
3. [ ] 定时任务创建：`openclaw cron list | grep ESR`
4. [ ] 定时任务测试：立即执行一次验证
5. [ ] 钉钉消息接收：检查钉钉群是否收到报告
6. [ ] 输出格式正确：包含8项检查+信息安全提示

## 📞 技术支持

### 问题反馈
- 定时任务配置失败
- 钉钉消息未发送
- 执行时间不正确
- 输出格式异常

### 联系信息
- **部门**: ESR信息安全部
- **文档版本**: v3.2.1
- **更新日期**: 2026-03-16
- **适用技能**: ESR_openclaw-checklist-v3.2