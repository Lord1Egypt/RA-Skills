---
title: "生成质量修复策略"
summary: "当生成的图片或视频不满足预期时，判断是改 script.json 还是直接改 prompt 文件"
---

# 生成质量修复策略

## 核心原则

| 层面 | 修改对象 | 影响范围 | 重建成本 |
|------|---------|---------|---------|
| **脚本层** | `script.json`（description/characters/shot_type/duration） | 全局一致，所有 shot 都受影响 | 高（需 rebuild-first-frames → regen → submit） |
| **提示词层** | `prompts/storyboard/shotXX_image.md` / `prompts/videos/video_shotXX.md` | 单张图片或单个视频 | 低（直接 regen/submit） |

## 管道自动修复（optimize 阶段执行）

脚本优化阶段（`optimize` / `auto` Stage 0）自动执行以下修复，无需人工干预：

### 脚本层自动修复

| 问题 | 检测规则 | 自动修复策略 |
|------|---------|-------------|
| **角色字段缺失/不完整** | description 提到角色名但 `characters` 字段为空或不全 | 从 description 匹配角色名自动补全；同组内前序 shot 角色可继承 |
| **角色不合理消失** | 同场景组内中景/远景中角色数无故减少 | 新角色入场→合并新旧角色集；旧角色缺失→补全 |
| **计数词代替角色名** | description 有"三人""两人"等模糊计数词 | 替换为实际角色名（如"阿巴斯、周戎和司南"） |
| **场景引用错误** | `reference_images.kf1` 指向错误的场景资产 | 根据 shot scene 修正为正确的场景资产路径 |
| **场景名缺失** | description 未命中任何 scene_cards 名称 | 补场景名到 description 尾部 |
| **场景组过渡缺失** | 两个场景组之间无过渡描述 | 首镜补「画面切换至X场景」 |
| **开头爆点缺失** | 前3镜头无爆点元素 | 补"突然"等爆点词（检查是否已含"突然"，避免重复） |
| **连续"突然"** | 相邻两个 shot 都以"突然"开头 | 第二个改为"意外"/"骤然"等其他爆点词 |
| **运镜多样性不足** | 连续3+镜头相同运镜 | 改中间 shot 的 camera_movement |
| **时长节奏差** | 各 shot 时长标准差 < 1.5s | 缩短最长 shot、加长最短 shot |
| **动作接续断裂** | 相邻 shot 动作动词不连贯（跑→坐无过渡） | 补过渡描述 |
| **视角跳跃** | 特写→远景无中景过渡 | 补推近/拉远描述 |
| **情绪弧线跳变** | 悲伤→欢快等不合理跳变 | 补过渡描述（"气氛突然沉重"等） |
| **空间一致性** | 角色在连续 shot 中位置未指定 | 从同组前序继承位置关键词 |
| **开头"突然"重复** | 描述中已含"突然"但又被前缀补 | 检查已有后跳过 |

### 提示词层自动修复（fix_prompts 开启）

| 问题 | 检测规则 | 自动修复策略 |
|------|---------|-------------|
| **角色 prompt 缺段** | 缺少光照/风格/质量要求等段 | 追加缺段的模板内容 |
| **首帧图 prompt 缺段** | 图生图缺少保留元素/新风格描述 | 追加缺段 |
| **场景 prompt 缺段** | 缺少画质要求 | 追加 quality 模板 |

### 验证后自动修复（_poll_shots 阶段执行）

视频内容验证不通过时，根据失败类型自动修复并重试：

| 失败原因 | 自动修复 |
|---------|---------|
| 人脸数不对 | 从同组前序继承或从 description 匹配补全 characters 字段 |
| 动作未检测 | 改 video_shotXX.md [动画内容] 段补动作指令 + 改 motion_type |
| 运镜不匹配 | 改 script.json shot_type |
| 场景直方图不匹配 | 从 description 匹配正确场景卡 → 更新 reference_images |

## 手动修复决策树

上述自动修复未覆盖或自动修复失败时，按以下决策树手动修复：

```
生成的图/视频有问题
│
├─ 角色不对（少人、多人、角色错误）
│  └─ 改 script.json: characters 字段 或 description 指名
│
├─ 场景不对（废墟变丛林、白天变黑夜）
│  └─ 改 script.json: description 或 scene 引用
│
├─ 动作不对（应转头没转、应跳没跳、幅度不对）
│  ├─ 动作类型/motion_type 错 → 改 script.json description
│  └─ 动作幅度/细节错 → 改 prompts/videos/video_shotXX.md [动画内容]
│
├─ 运镜不对（中景给了特写、推拉镜头方向反）
│  └─ 改 script.json: shot_type / camera_movement
│
├─ 情绪/氛围不对（紧张变温馨）
│  └─ 改 script.json: description 加入情绪关键词
│
├─ 时长/节奏不对（镜头太短或太长）
│  └─ 改 script.json: duration
│
├─ 构图不满意（角色偏左想居右、人太小）
│  └─ 改 prompts/storyboard/shotXX_image.md [构图] 段
│
├─ 画质不够（细节粗糙、模糊）
│  └─ 改 prompts/storyboard/shotXX_image.md [画质要求] 段
│
├─ 光影不匹配（太暗/太亮、色温不对）
│  └─ 改 prompts/storyboard/shotXX_image.md [光照] 段
│
├─ 角色特征丢失（耳钉、纹身、项链没显示）
│  └─ 改 prompts/storyboard/shotXX_image.md [目标风格/场景] 段
│
├─ 文字/UI元素干扰（不该出现字幕、标签）
│  └─ 检查 negative_prompt 是否有文字相关词
│
└─ 画面穿模/形变（人物扭曲、背景拉伸）
   └─ 改 prompts/storyboard/shotXX_image.md 降低复杂度，或缩小多角色参考图
```

## 提示词文件的手动保护

手工修改 prompt 文件后，在文件顶部添加：

```markdown
> ⚠️ 手动精修，勿自动覆盖
```

`build-first-frames --force` 检测到此标记时**跳过该文件**。不添加此标记的 prompt 文件在下次重建时会被覆盖。

## 批量修复流程

```bash
# 改 script.json 后的全量重建
build-first-frames --force      # 重新生成所有 prompt 文件
gi --shot-ids <id>              # 重新生成首帧图
submit --force <id>             # 重新提交视频

# 单改 prompt 文件后的局部重建
gi --shot-ids <id>              # 只重新生成指定 shot 的首帧图
submit --force <id>             # 指定 shot 重新提交
```
