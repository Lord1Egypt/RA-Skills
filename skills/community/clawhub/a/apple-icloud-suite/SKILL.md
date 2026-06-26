---
name: Apple iCloud Suite
description: >
  Apple iCloud 全套服务操作：日历、照片、iCloud Drive、设备查找、提醒事项。
  Use when: (1) 用户要求查看/创建/修改/删除日历事件或日程,
  (2) 用户说"帮我看看今天有什么安排"/"加个日程"/"改一下会议时间",
  (3) 用户要求查找/下载/管理 iCloud 照片,
  (4) 用户提到"查找我的设备"/"手机在哪"/"定位设备",
  (5) 用户要求操作 iCloud Drive 文件（上传/下载/查看）,
  (6) 用户讨论 Apple 生态下的日程管理、照片整理、文件同步。
  NOT for: Android 设备管理、Google Calendar/Photos、
  非 Apple 生态的云存储（OneDrive/Google Drive）、钉钉日历（用 mcporter）。
icon: 🍎
os: linux, macos
tools: pyicloud, caldav, icloudpd
install: |
  pip install pyicloud caldav icalendar  # 核心依赖
  pip install icloudpd                    # 照片批量下载（可选）
---

# Apple iCloud Suite

iCloud 日历、照片、Drive、设备查找的命令行操作。

## Step 0: 依赖与认证检查

### 1. 依赖验证
```bash
python3 -c "import pyicloud; print('pyicloud OK')" 2>/dev/null || echo "需安装: pip install pyicloud"
python3 -c "import caldav; print('caldav OK')" 2>/dev/null || echo "需安装: pip install caldav icalendar"
```

### 2. Session 缓存检查（优先复用，避免 2FA）
```bash
ls ~/.pyicloud/ 2>/dev/null && echo "有缓存 session" || echo "无缓存，需新认证"
```
- 有缓存 → 尝试直接连接，通常无需 2FA
- 无缓存 → 需要首次认证（见下方认证流程）

### 3. 认证方式（两条路径）

| 工具 | 认证方式 | 密码类型 |
|------|---------|---------|
| **pyicloud**（照片/Drive/设备） | 主密码 + 2FA 验证码 | Apple ID 主密码 |
| **CalDAV**（日历） | 应用专用密码 | appleid.apple.com 生成 |

**🔴 密码安全**：从环境变量读取，不硬编码
```bash
export ICLOUD_EMAIL="user@icloud.com"
export ICLOUD_PASSWORD="xxx"  # 或用 keychain
```

### 4. pyicloud 认证
```python
from pyicloud import PyiCloudService
import os
os.environ['icloud_china'] = '1'  # 中国大陆用户必须
api = PyiCloudService(os.environ['ICLOUD_EMAIL'], os.environ['ICLOUD_PASSWORD'], china_mainland=True)

if api.requires_2fa:
    # ⚠️ 需要用户参与：在 iPhone 上查看验证码
    code = input("请输入 iPhone 上收到的 6 位验证码: ")
    api.validate_2fa_code(code)
```

**确认点**：2FA 需要用户手动输入验证码。提前告知用户准备 iPhone。

## Step 1: 需求分类

| 用户意图 | 服务 | 跳转 |
|----------|------|------|
| "今天有什么安排" / "加个日程" | **日历** | → Step 2，读 `references/calendar.md` |
| "下载照片" / "看看相册" | **照片** | → Step 2，读 `references/photos.md` |
| "手机在哪" / "查找设备" | **设备查找** | → Step 2，读 `references/findmy.md` |
| "iCloud 文件" / "下载文档" | **Drive** | → Step 2，读 `references/drive.md` |

## Step 2: 执行（按需加载详细文档）

根据 Step 1 的分类，**读取对应 reference 文件** 获取详细操作指令：

| 服务 | Reference | 认证工具 | 主要脚本 |
|------|-----------|---------|---------|
| 📅 日历 | `references/calendar.md` | CalDAV | `scripts/icloud_calendar.py` |
| 📷 照片 | `references/photos.md` | pyicloud | `scripts/icloud-photos.py` |
| 📱 设备 | `references/findmy.md` | pyicloud | `scripts/icloud_tool.py` |
| 💾 Drive | `references/drive.md` | pyicloud | `scripts/icloud_tool.py` |
| 🔧 脚本总览 | `references/scripts.md` | — | 所有脚本用法 |

### 脚本选择指南

| 场景 | 用哪个脚本 |
|------|-----------|
| 设备查找 / Drive 浏览 | `scripts/icloud_tool.py`（通用工具） |
| 照片浏览/下载 | `scripts/icloud-photos.py`（照片专用） |
| 日历操作 | `scripts/icloud_calendar.py`（CalDAV） |
| 提醒事项 | `scripts/icloud-reminders.py` |
| 备忘录（有限） | `scripts/icloud-notes.py`（⚠️ Apple Notes API 有限） |

## Step 3: 验证与交付

1. 确认操作成功（文件已下载/事件已创建/设备已定位）
2. 展示结果给用户
3. 照片/文件 → 用 `MEDIA:<path>` 发送
4. 日历事件 → 格式化展示时间/地点/标题

## 边界条件

| 情况 | 处理 |
|------|------|
| 2FA 验证码超时 | 提醒用户重新发送验证码，重试认证 |
| Session 过期 | 删除 `~/.pyicloud/` 缓存，重新认证 |
| pyicloud 连接失败 | 检查网络 → 检查 icloud_china 环境变量 → 重试 |
| 应用专用密码无效（CalDAV） | 引导用户到 appleid.apple.com 重新生成 |
| 照片下载量大 | >50 张时告知预计时间，分批下载 |
| 备忘录需求 | Apple Notes 无公开 API，建议用 iCloud.com 网页版 |
| 依赖缺失 | 按 Step 0 安装指引，不继续 |

## 注意事项

- **中国大陆用户**：pyicloud 需 `china_mainland=True`，icloudpd 需 `--domain cn`
- **会话缓存**：认证成功后 session 保存在 `~/.pyicloud/`，通常数周有效
- **备忘录限制**：Apple Notes 没有公开 API，仅有有限的读取能力
