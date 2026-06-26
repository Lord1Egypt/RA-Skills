# Yijia Test Workflow Reference

## 用途

把脚本类 skill 产出的内容，压缩成可以直接用于 Yijia 文生视频测试的一段 prompt。

## 推荐测试规则

- 先从 `temp-workflow` 做测试，不污染正式 workflow
- 时长优先 8 秒
- 分辨率优先 竖屏
- 模型优先：`grok-imagine-1.0-video` 或 `grok-video`
- 类别可先用测试分类，例如：`测试视频`
- prompt 只保留单主体、单场景、单情绪、单动作主线

## Prompt 压缩法

把原脚本压成一段：

```text
主体 + 核心动作 + 场景 + 镜头运动 + 光线 + 风格 + 画质
```

### 示例 1：萌宠

```text
一只柯基在客厅地毯上摇着屁股小跑向镜头，嘴里叼着一只红色拖鞋，镜头低机位轻微跟拍，午后暖阳从窗边照进来，轻松搞笑，生活感，竖屏，高清
```

### 示例 2：解压

```text
透明玻璃珠缓慢落入浅水盘中激起细小波纹，微距特写，镜头轻微推进，柔和棚拍光线，安静、治愈、沉浸感，竖屏，高清
```

## Creator 测试命令

```bash
python3 /Users/shift/.openclaw/workspace-video-creator/scripts/workflow_guard.py
python3 /Users/shift/.openclaw/workspace-video-creator/scripts/enforce_project_layout.py
bash /Users/shift/.openclaw/workspace-video-creator/scripts/yijia_generate.sh \
  --project "temp-workflow" \
  --category "测试视频" \
  --language zh \
  --target "tiktok/shiftshen" \
  --prompt "一只柯基在客厅地毯上摇着屁股小跑向镜头，嘴里叼着一只红色拖鞋，镜头低机位轻微跟拍，午后暖阳从窗边照进来，轻松搞笑，生活感，竖屏，高清" \
  --duration "8秒" \
  --resolution "竖屏" \
  --mode text2video \
  --channel "yijia" \
  --model "grok-video"
```

## 预期产物

- `projects/temp-workflow/outputs/*.mp4`
- `projects/temp-workflow/outputs/*.txt`
- `projects/temp-workflow/progress/yijia_create_*.json`

## 注意

- 若环境未配置 Yijia 可执行文件或 API Key，测试会卡在生成阶段
- 若要正式 workflow 使用，需把测试 prompt 改成该 workflow 的 category/language 约束版本
