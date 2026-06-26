---
name: baby-record
version: 1.0.0
description: 宝宝每日护理记录技能。支持通过拍照纸质表单或口语描述快速录入宝宝每日数据（体温、黄疸、沐浴、体重、睡眠、喂养、排泄等），数据存储为 JSON 文件。当用户提到以下内容时触发：记录宝宝今天数据、宝宝每日汇总、今天体温多少、今天喝了多少奶、宝宝最近数据、帮我看看这张表（图片）、宝宝日记、baby record、每日情况汇总。
license: MIT
---

# 宝宝每日护理记录

通过对话或图片快速记录宝宝每日护理数据，存储为结构化 JSON 文件。

数据目录：`{baseDir}/data/`（每天一个 JSON 文件，如 `2026-03-09.json`）

脚本：`{baseDir}/scripts/daily_tracker.py`（纯 Python，无外部依赖）

字段参考：`{baseDir}/references/schema.md`

## 数据录入

### 从图片录入

用户发送纸质「宝宝每日基本情况汇总」表单照片时：

1. 用视觉能力识别照片中的所有字段
2. 参考 `references/schema.md` 将数据映射到标准字段
3. 向用户确认提取结果（用简洁表格展示）
4. 确认后调用脚本保存：
```bash
python {baseDir}/scripts/daily_tracker.py save --date YYYY-MM-DD --data '{"temperature":{"morning":36.9},...}'
```

### 从口语录入

用户用自然语言描述时（如"今天体温36.5，奶粉560ml喝了7次，便便2次"）：

1. 提取所有能识别的字段
2. 未提及的字段不填（保留为 null）
3. 日期未指定默认今天
4. 直接调用脚本保存，保存后用友好中文确认

### 增量更新

同一天可多次录入。脚本会自动合并：新数据覆盖已有字段，未提及字段保持原值。

## 数据查询

用户问"最近几天数据"、"昨天记录"、"上周汇总"等：

```bash
# 查看单日
python {baseDir}/scripts/daily_tracker.py get --date 2026-03-09

# 最近 N 天列表
python {baseDir}/scripts/daily_tracker.py list --last 7

# 日期范围查询
python {baseDir}/scripts/daily_tracker.py query --start 2026-03-01 --end 2026-03-09

# 趋势汇总
python {baseDir}/scripts/daily_tracker.py summary --last 7
```

查询结果为 JSON，用友好的中文表格或列表展示给用户。

## 展示规范

- 体温：显示 °C，异常值（>37.5）标注提醒
- 黄疸：显示 mg/dL，按早/晚 × 额头/脸/胸 表格展示
- 喂养：分奶粉和母乳展示 ml 和次数
- 趋势汇总：包含体温变化、体重增长、喂养量趋势、排泄频率

## 注意事项

- 所有交互使用中文
- 日期格式统一 YYYY-MM-DD
- 体温单位 °C，体重单位 kg，黄疸单位 mg/dL，奶量单位 ml
- 数据文件不存在时自动创建，无需初始化步骤
- 从图片提取数据时务必让用户确认后再保存
