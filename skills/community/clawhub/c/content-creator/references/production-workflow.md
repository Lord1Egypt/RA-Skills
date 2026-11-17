# 制作工作流与发布前检查 playbook

> 把"拍一条视频/录一期播客"变成可复现的流程。本 playbook 给视频与音频通用工作流、审核清单和常见坑。

## 1. 视频制作工作流（通用）

```
阶段 1 策划  → 选题卡（痛点/角度/平台/时长）
阶段 2 脚本  → Hook + 结构 + CTA（交 short-video-script 或自写）
阶段 3 拍摄  → 素材清单 + 环境/光线/收音检查
阶段 4 剪辑  → 粗剪 → 精剪 → 转场 → 色彩分级 → 字幕（交 video-editing）
阶段 5 包装  → 封面/缩略图 + 标题 + 标签（YouTube 交 youtube-automation）
阶段 6 发布  → 排期 + 多平台改编 + 数据回收
```

**关键纪律**：剪辑前先粗剪定节奏，再精修；色彩分级统一色调，别逐帧手调；字幕误差控制在 ±100ms。

## 2. 播客制作工作流

```
选题 → 大纲（3 个核心论点）→ 采访问题清单 → 录制（双轨收音）→
后期（降噪/切静默/电平统一）→ Shownotes → 分发（RSS/小宇宙/Apple）
```

**关键纪律**：采访类提前发提纲；后期先统一电平再降噪，顺序反了会引入底噪。

## 3. 发布前审核清单（视频）

- [ ] 节奏：前 3 秒有 Hook，无超过 5s 的拖沓
- [ ] 画质：分辨率达标、无过曝/死黑
- [ ] 音质：人声清晰、无爆音、BGM 不压人声
- [ ] 字幕：无错字、时间轴对齐
- [ ] 合规：素材授权、无平台违禁词
- [ ] 包装：封面/标题/标签就绪

## 4. 发布前审核清单（播客/音频）

- [ ] 开场 30s 说明本期价值
- [ ] 人声电平一致（-16 LUFS 左右）
- [ ] 切掉长时间静默与口误
- [ ] Shownotes 含时间戳与资源链接
- [ ] 封面与简介更新

## 5. 常见坑

- **无限重拍**：追求完美一镜，拖死进度。先完成再完美。
- **字幕遗漏**：无字幕在静音场景（地铁/办公室）完播暴跌。
- **缩略图敷衍**：YouTube CTR 直接受缩略图与标题影响，值得花时间。
- **不做数据回收**：发了就忘，下次还是盲做。固定看留存曲线与点击来源。

## 6. 相关子技能与层次边界

本 playbook 是「制作流程层」方法论（L2），覆盖视频 / 音频通用工作流与发布前检查；具体产出落地下沉到 L3 子技能：

- 视频剪辑 / 调色 / 字幕 / 多格式导出 → [skills/video-editing/SKILL.md](../skills/video-editing/SKILL.md)
- 缩略图 / SEO / 发布排期 / 数据分析 → [skills/youtube-automation/SKILL.md](../skills/youtube-automation/SKILL.md)
- 播客录制 / 后期 / 分发 → [skills/podcast-generation/SKILL.md](../skills/podcast-generation/SKILL.md)
- 短视频脚本（阶段 2 脚本） → [skills/short-video-script/SKILL.md](../skills/short-video-script/SKILL.md)
- 邮件通讯 / 简报编排 → 见 [skills/newsletter/SKILL.md](../skills/newsletter/SKILL.md)（本 playbook 不覆盖编辑类内容）

边界：本 playbook 只给"流程与检查清单"，不写具体平台软件操作或脚本内容；这些交给对应子技能。
