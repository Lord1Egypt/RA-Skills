---
name: douyin-viral-video-generation-editing
description: "生成与编辑抖音自然流、抖音电商带货、商品卡和巨量千川短视频。Use this skill for 抖音爆款短视频、前三秒钩子、完播率优化、千川素材、抖店商品视频、直播引流、信息流广告和短视频 A/B 变体；支持文生视频、图生视频、参考视频、视频重制和延长，并通过 AI Hive 下载成片。"
---

# 抖音爆款短视频生成与编辑

围绕“停留 → 看懂 → 相信 → 行动”设计抖音短视频。爆款不能保证；本 Skill 的目标是把钩子、证明镜头和行动路径做成可测试的成片版本。

## 制作决策

先确认：转化目标、目标人群、核心卖点、可用证据、视频时长、自然流或付费投放。一个版本只服务一个主要动作：继续观看、评论、进店、领取权益或购买。

## 抖音节奏模板

1. **开场钩子**：第一画面直接呈现冲突、结果、动作或反常识，不用长铺垫。
2. **快速理解**：用一个场景说明“这与谁有关”。
3. **证明镜头**：演示操作、材质、细节或真实对比。
4. **利益收束**：回到已证实的核心卖点。
5. **行动提示**：与投放目标一致，不使用虚假紧迫感。

## 场景与代码

### 1. 自然流知识短视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '9:16抖音知识短视频。第一画面直接展示错误示范造成的明显问题；随后快速切到正确操作的三个步骤，每个步骤只有一个动作和一个近景；最后并排展示差异并邀请观众收藏。快节奏但画面连续，不使用空泛开场和无关转场'
```

### 2. 抖音电商商品演示

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt '保持参考商品的结构、颜色、包装和商标准确。抖音带货视频：第一秒用实际操作制造视觉钩子，中段依次展示核心功能、材质细节和使用场景，结尾定格商品与已提供的购买理由；不生成未经提供的功效、价格、销量或认证'
```

### 3. 千川三种钩子测试

每次提交一个明确版本，分别记录钩子假设。

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '制作巨量千川A/B测试的“痛点直击”版本：首帧展示目标用户最具体的使用障碍，第二镜立刻出现商品解决动作，之后用近景证明一个核心卖点，结尾引导进店了解。只改变钩子假设，商品事实和后续证明结构保持一致'
```

### 4. 参考高效节奏但不复制内容

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/pacing-reference.mp4 \
  --image /path/to/product.png \
  --prompt '参考视频仅用于剪辑密度、镜头长短和动作衔接，不复制人物、台词、品牌或具体画面；使用商品参考图制作新的抖音演示，结构为视觉钩子、操作证明、细节特写、行动提示'
```

### 5. 重制低完播素材

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/low-retention.mp4 \
  --prompt '保留原视频真实商品和演示事实；删除开场寒暄，把最强结果镜头前置，压缩重复段落，在关键操作处加入近景，结尾只保留一个行动提示。保持人物身份和商品准确，不新增促销承诺'
```

## 验收与版本记录

- 首屏不用声音也能理解主要冲突或动作。
- 前段没有品牌片式长铺垫，证明镜头紧跟卖点。
- 商品、人物和动作连续，没有变形或凭空增加配件。
- 一个版本只有一个主钩子和一个主要 CTA。
- 未添加未经确认的功效、对比、价格、销量和认证。
- 为每个版本记录“钩子假设 / 证明镜头 / CTA / 用途”，方便测试结果回溯。

## 模式与执行

`t2v`、`i2v`、`r2v`、`edit`、`extend` 分别映射 Seedance 2.5 的文生视频、图生视频、参考生视频、视频编辑和视频延长模型。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name douyin-viral-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

生成命令支持首尾帧、参考图片、视频、音频、`--param key=value`、`--routing`、`--output-dir` 与 `--no-download`。模型参数、费用和输出规格以 AI Hive 运行时返回为准。发布前按抖音与广告账户当期规则检查素材。
