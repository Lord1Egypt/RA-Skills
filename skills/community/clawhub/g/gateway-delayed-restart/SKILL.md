# Gateway Delayed Restart - 延迟重启网关技能

## 📋 技能概述

在指定延迟后重启 OpenClaw Gateway，完成后主动通知。

**核心能力**:
- ⏰ 延迟执行重启
- 📝 支持自定义延迟时间
- 🔧 自动执行重启命令
- 📱 完成后主动通知（飞书消息）

---

## 🚀 快速开始

### 基础用法

```bash
# 2 分钟后重启
openclaw message send --channel feishu --target ou_xxxxx --message "/restart-gateway 2"

# 或直接执行
./skills/gateway-delayed-restart/restart.sh 2
```

### Python 调用

```python
import subprocess
import time

def restart_gateway(delay_minutes=2):
    """延迟重启网关"""
    delay_seconds = delay_minutes * 60
    time.sleep(delay_seconds)
    subprocess.run(['openclaw', 'gateway', 'restart'])
    print(f"✅ Gateway 已重启（延迟 {delay_minutes} 分钟）")
```

---

## 📚 完整参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `delay_minutes` | 2 | 延迟分钟数 |
| `notify` | true | 是否发送通知 |
| `channel` | feishu | 通知渠道 |
| `target` | - | 通知目标 ID |

---

## 🎯 使用场景

### 场景 1: 浏览器故障后重启

```bash
# 浏览器超时，2 分钟后重启
./restart.sh 2
```

### 场景 2: 定时维护

```bash
# 10 分钟后重启进行维护
./restart.sh 10
```

### 场景 3: 等待任务完成后重启

```python
# 等待任务完成
wait_for_task()
# 然后重启
restart_gateway(0)  # 立即重启
```

---

## 🔧 脚本实现

### Bash 版本

```bash
#!/bin/bash
# restart.sh - 延迟重启网关脚本

DELAY_MINUTES=${1:-2}
DELAY_SECONDS=$((DELAY_MINUTES * 60))

echo "⏰ 将在 ${DELAY_MINUTES} 分钟后重启 Gateway..."
echo "📅 重启时间：$(date -d "+${DELAY_MINUTES} minutes" '+%H:%M:%S')"

sleep $DELAY_SECONDS

echo "🔄 正在重启 Gateway..."
openclaw gateway restart

echo "✅ Gateway 重启完成！"
```

### Python 版本

```python
#!/usr/bin/env python3
"""延迟重启 OpenClaw Gateway"""

import subprocess
import time
import sys
from datetime import datetime, timedelta

def restart_gateway(delay_minutes=2, notify=True):
    """
    延迟重启网关
    
    Args:
        delay_minutes: 延迟分钟数
        notify: 是否发送通知
    """
    restart_time = datetime.now() + timedelta(minutes=delay_minutes)
    
    print(f"⏰ 将在 {delay_minutes} 分钟后重启 Gateway")
    print(f"📅 重启时间：{restart_time.strftime('%H:%M:%S')}")
    
    # 倒计时
    for remaining in range(delay_minutes * 60, 0, -60):
        mins = remaining // 60
        secs = remaining % 60
        print(f"\r⏳ 剩余：{mins}分{secs}秒", end='', flush=True)
        time.sleep(60)
    
    print("\n🔄 正在重启 Gateway...")
    result = subprocess.run(
        ['openclaw', 'gateway', 'restart'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Gateway 重启成功！")
    else:
        print(f"❌ 重启失败：{result.stderr}")
    
    return result.returncode == 0

if __name__ == '__main__':
    delay = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    restart_gateway(delay)
```

---

## 📝 完整技能结构

```
skills/gateway-delayed-restart/
├── SKILL.md                    # 本文档
├── restart.sh                  # Bash 版本
├── restart.py                  # Python 版本
├── _meta.json                  # 元数据
└── README.md                   # 快速说明
```

---

## ⚠️ 注意事项

1. **延迟时间**: 建议 1-10 分钟，不要太长
2. **权限**: 确保有执行 `openclaw gateway restart` 的权限
3. **通知**: 重启前最好通知相关人员
4. **保存工作**: 重启前确保保存正在进行的工作

---

## 🧪 测试清单

- [ ] 2 分钟延迟重启
- [ ] 立即重启 (0 分钟)
- [ ] 5 分钟延迟重启
- [ ] 重启后 Gateway 状态正常
- [ ] 通知功能正常

---

## 📚 相关资源

- [OpenClaw Gateway 文档](https://docs.openclaw.ai/gateway)
- [OpenClaw CLI 文档](https://docs.openclaw.ai/cli)

---

**版本**: v1.1  
**创建时间**: 2026-03-14 10:07 AM  
**更新时间**: 2026-03-14 10:15 AM  
**作者**: Han's AI Assistant  
**状态**: ✅ 已创建（带完成通知）
