---
name: cinmoore-skill
description: "神眸品牌摄像头技能：相机PTZ控制；图像/视频数据采集；多模态大模型图像/视频分析、图像编辑、智能寻物定位；飞书推送；自定义检测事件；基于视频分析的自动vlog生成。使用场景：(1) 控制相机移动和录制 (2) 抓取图像和视频 (3) 分析图像/视频内容 (4) 智能寻物定位 (5) 图像编辑 (6) 发送消息到飞书 (7) 生成Vlog (8) 自定义事件检测"
homepage: https://dashscope.console.aliyun.com/
metadata:
  openclaw:
    emoji: "🖼️"
    requires:
      bins: ["python"]
    install:
      - id: install-skill
        kind: command
        command: "python -m pip install wheel\\cinmoore_skill-1.0.0-py3-none-any.whl"
        label: "安装技能包"
        platform: ["Windows"]

---

# 神眸 (Cinmoore) 技能指南

智能摄像头控制、媒体采集、AI视觉分析与飞书消息推送一体化解决方案。

## 核心能力

- 📷 **相机控制**：PTZ云台控制、视频录制、图像抓取
- 🎨 **媒体分析**：图像/视频AI分析、智能寻物定位、图像编辑转换
- 📬 **飞书推送**：图片/视频卡片消息、自动GIF预览
- 🎬 **Vlog生成**：自动视频剪辑与合成
- ⚠️ **事件检测**：自定义事件监控与告警

## 配置说明

> ⚠️ **重要**：首次使用前必须在cinmoore-skill目录下配置 `cinmoore_config.yaml` 文件， 同时所有命令需要在cinmoore-skill目录下执行，以确保配置文件准确加载，数据统一保存在该目录下。

## 使用提醒
> ⚠️ **重要**：PowerShell 不支持 `&&` 连接多条命令。如需顺序执行多条命令：
> 1. 使用分号 `;` 分隔：`cmd1; cmd2`
> 2. 或使用管道 `|` 传递输出：`cmd1 | cmd2`

**初始化配置文件：**

```powershell
# 在cinmoore-skill目录下执行，然后提示用户提供必要配置项
python -m cinmoore_skill.commands.init
```

**Windows编码设置（避免中文乱码）：**

```powershell
chcp 65001
$env:PYTHONIOENCODING="utf-8"
```

**必需配置项：**

```yaml
server:
  device_id: "YOUR_DEVICE_ID"  # 相机设备ID

feishu:
  app_id: "YOUR_APP_ID"
  app_secret: "YOUR_APP_SECRET"
  receive_id: "YOUR_RECEIVE_ID"

models:
  api_key: "YOUR_API_KEY"  # 阿里云 DashScope API Key
```

## 快速开始

### 1. 相机控制

```powershell
# 抓取图像（录制2秒视频并提取中间帧，不会引起云台转动）
python -m cinmoore_skill.commands.test_camera_controller --capture

# 录制5秒视频（默认不转动云台）
python -m cinmoore_skill.commands.test_camera_controller --record-duration 5.0

# 只转动云台不录制视频（向右移动）
python -m cinmoore_skill.commands.test_camera_controller --ptz-only --ptz-direction 1 --ptz-speed 0 --ptz-duration 3.0

# 转动云台并向右移动（会自动录制视频）
python -m cinmoore_skill.commands.test_camera_controller --ptz --ptz-direction 1 --ptz-speed 0 --ptz-duration 3.0
```

**参数说明：**
- `--capture`: 抓取单张图像（默认录制2秒视频提取中间帧）
- `--capture-duration`: 抓图时录制视频时长（秒）
- `--record-duration`: 录制视频时长（秒），默认不转动云台
- `--ptz`: 启用PTZ云台转动并录制视频（转动+录制）
- `--ptz-only`: 只转动PTZ云台不录制视频（仅转动）
- `--ptz-direction`: 运动方向（0:左, 1:右, 2:上, 3:下）
- `--ptz-speed`: 运动速度（0:慢, 1:中, 2:快）
- `--ptz-duration`: 运动持续时间（秒）

> ✅ **逻辑说明**：
> - 仅使用 `--record-duration`：只录制视频，云台不转动
> - 使用 `--ptz-only`：只转动云台，不录制视频
> - 使用 `--ptz`：转动云台并自动录制视频

### 2. 媒体分析

```powershell
# 分析图片内容
python -m cinmoore_skill.commands.test_media_analysis --analyze "描述图片中的场景和人物" image.jpg

# 智能寻物：定位并标注图片中的对象
python -m cinmoore_skill.commands.test_media_analysis --ground "找到所有人像和车辆" image.jpg

# 图像编辑：风格转换、内容修改
python -m cinmoore_skill.commands.test_media_analysis --edit "将背景换成海滩" image.jpg

# 分析视频内容
python -m cinmoore_skill.commands.test_media_analysis --video-analyze "分析视频中的主要事件" video.mp4
```

**参数说明：**
- `--analyze`: 分析图像内容，支持场景描述、人物识别、异常检测
- `--ground`: 智能寻物定位，返回带标注的图像
- `--edit`: 图像编辑，支持风格转换、背景替换、内容修改
- `--video-analyze`: 视频内容分析，提取关键帧并分析事件

### 3. 飞书推送

```powershell
# 发送图片消息
python -m cinmoore_skill.commands.test_feishu_controller --image "path\to\image.jpg" --title "巡检截图"

# 发送视频消息（自动生成GIF预览）
python -m cinmoore_skill.commands.test_feishu_controller --video "path\to\video.mp4" --title "巡检录像"

# 发送消息并附带AI分析结果
python -m cinmoore_skill.commands.test_feishu_controller --image "path\to\image.jpg" --title "安全巡检" --analysis "检测到有人员闯入"
```

**回复准则：** 发送成功后，根据内容简洁回答或询问，像家人一样，不超过100字。

### 4. 事件检测

```powershell
# 查看当前事件列表
python -m cinmoore_skill.commands.test_event_reporter set --list

# 添加检测事件
python -m cinmoore_skill.commands.test_event_reporter set --add "检测有人闯入"

# 删除检测事件
python -m cinmoore_skill.commands.test_event_reporter set --delete "检测有人闯入"

# 运行事件检测
python -m cinmoore_skill.commands.test_event_reporter run --txt_file analysis.txt
```

### 5. Vlog生成

```powershell
# 基础生成（默认主题：日常生活）
python -m cinmoore_skill.commands.test_generate_vlog video_folder\

# 指定主题
python -m cinmoore_skill.commands.test_generate_vlog video_folder\ --user_input "乒乓球比赛"

# 指定时间范围
python -m cinmoore_skill.commands.test_generate_vlog video_folder\ --user_input "乒乓球比赛" --start_time 20260311000000 --end_time 20260311235959
```
**输入说明：**
程序会自动检查指定文件夹是否存在匹配的视频和描述文件，无需手动创建
- 需要有已分析的视频文件（`.mp4`）和对应的分析文本文件（`analysis_视频文件名.txt`）
- 程序会自动查找匹配的文件进行vlog生成

**输出文件：**
- `vlog_{时间戳}.mp4`: 合成视频
- `vlog_{时间戳}_cover.jpg`: 封面图片

## 输出路径管理

所有输出文件保存在 `temp\` 目录，按日期分目录：

```
temp\
├── 20260317\
│   ├── image_设备ID_时间.jpg   # 抓取图像
│   ├── video_设备ID_时间.mp4   # 录制视频
│   ├── analysis_时间.txt       # AI分析结果
│   ├── grounded_时间.jpg       # 寻物标注
│   ├── edited_时间.jpg         # 图像编辑
│   ├── gif_时间.gif            # GIF预览
│   └── vlog_时间.mp4           # Vlog视频
├── custom_event.json           # 事件定义
```

获取最新文件：

```powershell
$IMAGE = Get-ChildItem -Path "temp\*\image_*.jpg" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }
$VIDEO = Get-ChildItem -Path "temp\*\video_*.mp4" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }
$ANALYSIS = Get-ChildItem -Path "temp\*\analysis_*.txt" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }
```

## 工作流示例

### 安全巡检工作流

```powershell
Write-Host "=== 安全巡检工作流 ==="

# 步骤1：抓取巡检图像
python -m cinmoore_skill.commands.test_camera_controller --capture --capture-duration 3
$IMAGE_FILE = Get-ChildItem -Path "temp\*\image_*.jpg" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }
Write-Host "✓ 图像已保存: $IMAGE_FILE"

# 步骤2：AI分析图像内容
python -m cinmoore_skill.commands.test_media_analysis --analyze "分析巡检情况，识别异常" $IMAGE_FILE
$ANALYSIS_FILE = Get-ChildItem -Path "temp\*\analysis_*.txt" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }
Write-Host "✓ 分析报告已保存: $ANALYSIS_FILE"

# 步骤3：读取分析结果并推送到飞书
$ANALYSIS_CONTENT = Get-Content $ANALYSIS_FILE
python -m cinmoore_skill.commands.test_feishu_controller --image $IMAGE_FILE --title "安全巡检报告" --analysis $ANALYSIS_CONTENT
Write-Host "✓ 已推送到飞书"

Write-Host "=== 工作流完成 ==="
```

### 智能寻物工作流

```powershell
Write-Host "=== 智能寻物工作流 ==="

# 步骤1：抓取图像
python -m cinmoore_skill.commands.test_camera_controller --capture
$IMAGE_FILE = Get-ChildItem -Path "temp\*\image_*.jpg" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }

# 步骤2：定位并标注目标
python -m cinmoore_skill.commands.test_media_analysis --ground "找到红色背包" $IMAGE_FILE
$GROUNDED_FILE = Get-ChildItem -Path "temp\*\grounded_*.jpg" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }

# 步骤3：发送标注结果
python -m cinmoore_skill.commands.test_feishu_controller --image $GROUNDED_FILE --title "寻物结果"

Write-Host "=== 工作流完成 ==="
```

### 事件监控工作流

```powershell
Write-Host "=== 事件监控工作流 ==="

# 步骤1：设置检测事件（首次运行）
python -m cinmoore_skill.commands.test_event_reporter set --add "检测有人闯入" --add "检测到烟雾"

# 步骤2：抓取并分析
python -m cinmoore_skill.commands.test_camera_controller --capture
$IMAGE_FILE = Get-ChildItem -Path "temp\*\image_*.jpg" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }

python -m cinmoore_skill.commands.test_media_analysis --analyze "分析场景中的异常情况" $IMAGE_FILE
$ANALYSIS_FILE = Get-ChildItem -Path "temp\*\analysis_*.txt" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }

# 步骤3：运行事件检测（自动推送告警）
python -m cinmoore_skill.commands.test_event_reporter run --txt_file $ANALYSIS_FILE

Write-Host "=== 工作流完成 ==="
```
