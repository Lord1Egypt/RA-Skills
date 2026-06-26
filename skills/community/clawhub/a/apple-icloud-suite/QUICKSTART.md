# 🍎 Apple iCloud Suite 快速入门

3 分钟内开始使用 iCloud 命令行工具！

## ✅ 实测验证 (2026-02-05)

| 功能 | 状态 |
|------|------|
| 📷 照片 | ✅ 可用 - 浏览、下载 |
| 💾 iCloud Drive | ✅ 可用 - 浏览文件 |
| 📱 查找设备 | ✅ 可用 - 列出设备 |
| 📅 日历 | ✅ 可用 - 读取/创建事件 |

## 第一步：安装

```bash
pip install pyicloud caldav icalendar
```

## 第二步：运行

```bash
# 设置环境变量 (可选)
export ICLOUD_USERNAME="your@email.com"
export ICLOUD_PASSWORD="your_password"
export ICLOUD_CHINA="1"  # 中国大陆用户

# 运行工具
python scripts/icloud_tool.py photos albums
```

## 第三步：双重认证

首次运行时会提示：

```
🔐 需要双重认证
请查看 iPhone/iPad/Mac 上的验证码弹窗
请输入 6 位验证码: ******
✅ 验证成功!
```

验证成功后会话会被缓存，下次无需重复验证。

## 常用命令

### 照片

```bash
# 列出相册
python scripts/icloud_tool.py photos albums

# 列出最近 20 张照片
python scripts/icloud_tool.py photos list 20

# 下载第 1 张照片
python scripts/icloud_tool.py photos download 1
```

### iCloud Drive

```bash
# 列出根目录
python scripts/icloud_tool.py drive list

# 进入文件夹
python scripts/icloud_tool.py drive cd Downloads
```

### 设备

```bash
python scripts/icloud_tool.py devices
```

### 📅 日历 (需要应用专用密码)

```bash
# 设置应用专用密码
export ICLOUD_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"

# 列出日历
python scripts/icloud_calendar.py list

# 今天的事件
python scripts/icloud_calendar.py today

# 未来 7 天
python scripts/icloud_calendar.py week 7

# 创建事件
python scripts/icloud_calendar.py new 2026-02-10 10:00 11:00 "开会"
```

## ⚠️ 重要提示

1. **照片/Drive/设备**：使用 Apple ID **主密码** + 双重认证
2. **日历**：使用 **应用专用密码**（在 appleid.apple.com 生成）
3. **中国大陆**：设置 `ICLOUD_CHINA=1` 环境变量

## 更多功能

- 批量下载照片：使用 icloudpd

详见 [SKILL.md](./SKILL.md)
