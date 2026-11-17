---
name: pet-camera-vision
description: 桌宠摄像头感知 Skill。截图并调用多模态模型识别人脸、颜色与表情，输出结构化 JSON（在场状态+情绪+颜色），供情绪分析、长期记忆与陪伴反馈使用。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: PET_CAMERA_INDEX
        required: false
        description: 摄像头设备索引（默认 0），也支持 /dev/videoX 路径
      - name: PET_CAMERA_RESOLUTION
        required: false
        description: 截图分辨率，默认 1280x720
      - name: PET_CAMERA_OUTDIR
        required: false
        description: 截图保存目录，默认 ./captures
    emoji: "📷"
---

# pet-camera-vision — 桌宠摄像头感知 Skill

## 概述

本 Skill 是「多模态情绪陪伴桌宠系统」的**感知端**：负责拍照截图，并把"人脸的在场状态、颜色、表情"交给 OpenClaw 的多模态模型分析，最终输出**结构化 JSON**，供情绪分析、长期记忆与陪伴反馈（表情显示 / 灯光 / 动作）使用。

设计遵循项目约定：**OpenClaw 负责"思考"，Skill 负责"执行"**。
本 Skill 只负责两件事：

1. 稳定截图（多后端自动回退：libcamera-still → fswebcam → OpenCV）。
2. 生成分析提示词、并把多模态模型的回答**规范化为严格 JSON**（容错解析 + 字段校验 + 兜底默认值）。

## 架构

```
用户靠近/做表情
      │
      ▼
capture.py  ──截图──►  JPG 文件
      │
      ▼
analyze.py --local  ──►  本地辅助检测（在场状态 cv2 + 主色提取 PIL，离线可用）
      │
      ▼
多模态模型（由 OpenClaw 调用，参考 prompts 里的提示词）
      │
      ▼
analyze.py --model-output  ──►  规范化 JSON：
{
  "present": true,            # 有没有人
  "emotion": "happy",         # 表情识别结果
  "emotion_confidence": 0.9,
  "colors": [{"name": "蓝色", "hex": "#3B82F6", "ratio": 0.42}],
  "timestamp": "2026-08-31T13:47:00+08:00"
}
      │
      ▼
OpenClaw 记忆 / 反馈（表情、灯光、动作）
```

## 文件说明

| 文件 | 作用 |
| --- | --- |
| `SKILL.md` | 本说明文档 |
| `capture.py` | 截图脚本，多后端自动回退，支持离线合成测试图 |
| `analyze.py` | 本地辅助检测 + 多模态提示词生成 + 模型输出规范化 |
| `prompts/analyze_vision.md` | 给多模态模型的提示词模板（中英双语） |
| `examples/example_output.json` | 规范化输出的样例 |
| `examples/demo.md` | 演示脚本（含离线演示方式） |

## 依赖与安装

- Python 3.9+（树莓派系统自带）
- 截图后端三选一即可（按顺序自动回退）：
  - `libcamera-still`（树莓派 Camera Module，推荐）
  - `fswebcam`（USB 摄像头，`sudo apt install fswebcam`）
  - `opencv-python`（通用，`pip install opencv-python`，本机开发也能用）
- 本地辅助检测可选：`opencv-python`（人脸级联）+ `Pillow`（主色提取）

```bash
sudo apt install -y fswebcam        # USB 摄像头时
pip install opencv-python Pillow    # 通用/开发机
```

## 使用方法

### 1. 截图

```bash
python3 capture.py --outdir captures --resolution 1280x720
```

输出（stdout，JSON）：

```json
{"status": "ok", "path": "captures/20260831_134700.jpg", "backend": "libcamera-still", "timestamp": "2026-08-31T13:47:00+08:00"}
```

常用参数：`--device 0|/dev/video0`（指定摄像头）、`--filename`（自定义文件名）、`--synthetic`（无摄像头时生成合成测试图，用于离线演示）。

### 2. 本地辅助检测（离线，不调模型）

```bash
python3 analyze.py --image captures/xxx.jpg --local
```

输出在场状态（有人/无人，基于人脸级联）+ 主色 Top3（名称 + HEX + 占比），**无需联网**。

### 3. 生成多模态提示词

```bash
python3 analyze.py --image captures/xxx.jpg
```

打印可直接喂给多模态模型的提示词（见 `prompts/analyze_vision.md`），要求模型只返回 JSON。

### 4. 规范化模型输出

```bash
python3 analyze.py --image captures/xxx.jpg --model-output model_answer.txt
```

- 容错提取模型回答中的 JSON（支持代码块、前后缀杂文）
- 校验并补全字段（允许的情绪集合、置信度 0-1、颜色列表）
- 输出最终**严格 JSON**（单行，便于 OpenClaw 直接解析）

## 输出 JSON 格式

```json
{
  "present": true,
  "present_method": "multimodal",        // multimodal | cascade | unknown
  "emotion": "happy",
  "emotion_confidence": 0.92,
  "colors": [
    {"name": "蓝色", "hex": "#3B82F6", "ratio": 0.42},
    {"name": "白色", "hex": "#F8FAFC", "ratio": 0.31}
  ],
  "image_path": "captures/20260831_134700.jpg",
  "timestamp": "2026-08-31T13:47:00+08:00"
}
```

- `present`：`true`/`false`（有没有人）
- `emotion`：允许集合 `happy | sad | angry | surprised | fearful | disgusted | neutral | worried | sleepy | excited`
- `colors`：画面主色 Top3，`name` 为中文颜色名
- 模型输出缺失字段时自动补默认值，保证 JSON 永远可解析

## 与 OpenClaw 的集成（示例流程）

```text
1. OpenClaw 决定"看一眼用户"（定时轮询 / 用户靠近触发 / 对话中需要确认情绪）
2. 调用本 Skill：python3 capture.py --outdir captures
3. OpenClaw 读取截图路径，调用多模态模型（提示词见 prompts/analyze_vision.md）
4. 模型回答写入临时文件 → python3 analyze.py --image <path> --model-output <file>
5. OpenClaw 拿到结构化 JSON：
   - present=false → 进入待机，屏幕熄屏等待
   - present=true  → 更新长期记忆"用户当前情绪=happy"
   - emotion=消极 → 触发安慰反馈（冷色灯光 / 安慰表情 / 温柔语气）
   - emotion=积极 → 暖色灯光 + 开心表情联动
```

## 演示样例

见 `examples/demo.md`，含：

- **在线演示**：对着摄像头做表情 → 输出对应情绪 JSON → 触摸屏/灯光联动
- **离线演示**：无摄像头时用 `--synthetic` 生成测试图，走完整"截图→分析→JSON"链路

## 故障排查

| 现象 | 处理 |
| --- | --- |
| 提示找不到摄像头 | `--device` 指定 `/dev/video0`；检查 USB 权限；`ls /dev/video*` |
| 树莓派 libcamera 报错 | `sudo apt install -y libcamera-apps`；确认 Camera Module 已启用 |
| 分析结果总是不准 | 提高 `--resolution`；保证光线充足；让人脸占画面 1/4 以上 |
| 模型返回的不是 JSON | 使用 `prompts/analyze_vision.md` 里的严格提示词；`--model-output` 模式会自动容错提取 |

## 许可

按 ClawHub 规则，本 Skill 以 MIT-0 许可发布。
