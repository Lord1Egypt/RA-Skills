# 截图准备指南

## 需要准备的截图

### 1. age-calculation.png - 年龄计算示例

**内容建议：**
- 终端命令行截图
- 显示 `python3 scripts/calculate_age.py 2026-02-27` 命令
- 显示输出结果（年龄、阶段等）
- 清晰的字体和颜色

**尺寸：** 1920x1080 或 1280x720

---

### 2. milestones.png - 成长里程碑展示

**内容建议：**
- 终端命令行截图
- 显示 `python3 scripts/calculate_age.py 2026-02-27 --milestones` 命令
- 显示未来里程碑列表
- 清晰的表格或列表格式

**尺寸：** 1920x1080 或 1280x720

---

## 截图方法

### 方法 1：实际运行截图

```bash
# 运行命令
python3 scripts/calculate_age.py 2026-02-27

# 截图（根据你的系统）
# macOS: Cmd + Shift + 4
# Windows: Win + Shift + S
# Linux: Flameshot 或系统截图工具
```

### 方法 2：使用脚本生成

```bash
# 创建测试输出
python3 scripts/calculate_age.py 2026-02-27 > output.txt
python3 scripts/calculate_age.py 2026-02-27 --milestones > milestones.txt

# 然后用终端截图工具
```

---

## 完成后

将截图文件放入 `screenshots/` 目录：

```
/home/node/.openclaw/workspace/skills/awakening-birthday/screenshots/
├── age-calculation.png
└── milestones.png
```

然后在 clawhub.json 中确认路径正确。
