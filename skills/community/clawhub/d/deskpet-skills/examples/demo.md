# 演示脚本（demo.md）— pet-camera-vision

## 场景

对着摄像头做表情 → 桌宠识别出"在场状态 + 情绪 + 颜色" → 结构化 JSON
→ OpenClaw 更新记忆 → 反馈 Skill 显示对应表情/灯光。

## 演示一：在线演示（有摄像头）

```bash
# 1. 截图
python3 capture.py --outdir captures

# 2. 本地辅助检测（可选，展示"离线也能感知"）
python3 analyze.py --image captures/<最新图片>.jpg --local
# 期望输出：{"present": true, "colors": [...], ...}

# 3. 生成提示词并交给多模态模型（OpenClaw 自动完成这一步）
python3 analyze.py --image captures/<最新图片>.jpg

# 4. 把模型回答存成文件，规范化输出
python3 analyze.py --image captures/<最新图片>.jpg --model-output model_answer.txt
# 期望输出：{"present": true, "emotion": "happy", "emotion_confidence": 0.9, "colors": [...], ...}
```

**演示话术**：先对镜头笑（识别出 happy），再皱眉（识别出 sad/worried），
最后离开画面（present=false）——桌宠进入待机。

## 演示二：离线演示（无摄像头，备选方案）

```bash
# 生成合成测试图（渐变背景 + 笑脸"人脸"）
python3 capture.py --synthetic --outdir captures

# 与在线演示相同的分析链路
python3 analyze.py --image captures/<合成图>.jpg --local
python3 analyze.py --image captures/<合成图>.jpg
```

## 演示三：端到端（与 pet-feedback 联动，完整闭环）

```bash
# 终端 A：启动反馈 Skill 守护进程
python3 ../pet-feedback/daemon.py --state-file /tmp/pet_state.json --fullscreen

# 终端 B：感知 → 分析 → 写状态 → 反馈
python3 capture.py --outdir captures
# ... OpenClaw 分析情绪 ...
echo '{"emotion":"happy","phase":"talk","message":"看到你笑我也开心！"}' > /tmp/pet_state.json
# → 屏幕显示开心表情；语音播放"看到你笑我也开心！"
```

## 常见问题

| 问题 | 处理 |
| --- | --- |
| 摄像头打不开 | `--device` 指定索引；检查权限；`v4l2-ctl --list-devices` |
| 识别不准 | 提高分辨率、保证光线、人脸靠近镜头 |
| 模型输出非 JSON | 用本 Skill 的 `--model-output` 模式，自带容错提取 |
