---
name: diary
description: 个人日记自动化 skill。用于按天生成日记文本并导出 1080px 图片；支持首次自动初始化、读取 SOUL/MEMORY/每日记忆素材、保持写作风格连续性。适用于用户要求“写日记/生成日记图片/补昨天日记/自动日记归档”等场景。
---

# 日记（Diary）Skill

## 目标

在需要写日记时，一键完成：
1. 自动检查并初始化配置
2. 读取素材（SOUL、MEMORY、daily memory、近几天日记）
3. 生成目标日期日记文本
4. 渲染为 1080px 宽图片

## 执行流程

### Step 0：配置检查
- 若 `config.yaml` 存在：进入主流程
- 若不存在：按 `config.template.yaml` 自动初始化并继续

### Step 1：确定目标日期
- 使用 `environment.timezone`
- 默认目标：昨天（当前日期 - 1）

### Step 2：收集素材
必读：
- `paths.soul_path`
- `paths.memory_root_path`
- `paths.daily_memory_dir/YYYY-MM-DD.md`

建议读取：
- `paths.diary_text_dir` 最近 7 天日记（避免重复句式）
- 可选新闻摘要目录（若存在）

### Step 3：写作
- 第一人称
- 真实、自然、有情绪与想法
- 禁止流水账式罗列
- 不编造不存在的事实
- 保存到 `<diary_text_dir>/YYYY-MM-DD.md`

### Step 4：生成图片
- 使用 `diary-template.html` 渲染
- 输出宽度必须为 `output.image_width`（默认 1080）
- 高度自适应内容
- 输出路径：`<diary_text_dir>/diary-YYYY-MM-DD.png`

### Step 5：返回结果
返回：
- `date`
- `text_path`
- `image_path`
- `image_size`

## 约束

- 不覆盖已存在的同日期日记（除非用户明确要求）
- 声称完成时必须给出实际输出路径
- 仅在缺文件时创建目录，不删除已有内容
