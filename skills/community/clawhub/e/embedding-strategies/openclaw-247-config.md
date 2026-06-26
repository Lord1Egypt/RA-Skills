# OpenClaw 7×24 小时运行配置

_配置日期：2026-03-05_

## 电源设置（已完成）

- ✅ 电源模式：**节能模式**
- ✅ 显示器关闭：10 分钟（插电）
- ✅ 硬盘关闭：20 分钟（插电）
- ✅ 系统睡眠：**从不**（插电）

## 开机自启（已完成）

- ✅ 启动脚本：`C:\Users\Xiabi\.openclaw\workspace\openclaw-autostart.ps1`
- ✅ 快捷方式：`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw.lnk`

## 电池养护（需手动设置）

**联想笔记本：**
1. 打开 Lenovo Vantage
2. 电源 → 电池养护模式
3. 开启"节电模式"（限制充电到 55-60%）

**或其他品牌：**
- 在 BIOS 中找 Battery Health/Conservation Mode
- 或使用品牌自带的电源管理软件

## 防止 Windows 自动重启

1. `Win+R` → `gpedit.msc`
2. 计算机配置 → 管理模板 → Windows 组件 → Windows 更新
3. 启用"配置自动更新" → 设置为"通知下载和安装"

## 监控建议

**每周检查一次：**
- 风扇是否积灰
- 电脑底部温度（别超过 50°C）
- OpenClaw 是否正常运行

**命令检查：**
```powershell
# 检查 OpenClaw 状态
openclaw gateway status

# 查看系统运行时间
systeminfo | Select-String "System Boot Time"
```

## 注意事项

- ⚠️ 笔记本建议垫高或用散热架
- ⚠️ 雷雨天气建议关机
- ⚠️ 长期不用时关闭电源

---
_有问题随时找 Claw！🐾_
