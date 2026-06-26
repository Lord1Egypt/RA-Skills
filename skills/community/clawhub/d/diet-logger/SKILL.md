---
name: diet-logger
version: 1.0.0
description: 记录日常饮食并保存到 Obsidian 库。当用户要求记录早饭、午饭、晚饭、加餐、饮食日记或类似的饮食追踪任务时使用。使用 scripts/log_diet.py 脚本确保格式固定一致。
---

# 饮食记录

用于记录日常饮食，保存到 Obsidian 库中，格式完全固定。

## 使用方法

使用 Python 脚本记录饮食：

```bash
python3 ~/.openclaw/workspace/skills/diet-logger/scripts/log_diet.py \
  --date 2026-03-27 \
  --meal 晚饭 \
  --items "红烧肉,米饭"
```

### 参数说明

- `--date`: 日期 (YYYY-MM-DD)，默认为今天
- `--meal`: 餐段，可选值：早饭、中饭、晚饭、加餐
- `--items`: 食物列表，逗号分隔

### 示例

```bash
# 记录早饭
python3 ~/.openclaw/workspace/skills/diet-logger/scripts/log_diet.py \
  --meal 早饭 --items "鸡蛋,牛奶"

# 记录中饭
python3 ~/.openclaw/workspace/skills/diet-logger/scripts/log_diet.py \
  --meal 中饭 --items "清蒸鲈鱼,炒花菜,米饭"

# 指定日期
python3 ~/.openclaw/workspace/skills/diet-logger/scripts/log_diet.py \
  --date 2026-03-26 --meal 晚饭 --items "面条"
```

## 文件格式

生成的文件格式固定如下：

```markdown
# YYYY-MM-DD 饮食记录

## 早饭
- 鸡蛋
- 牛奶

## 中饭
- 清蒸鲈鱼
- 炒花菜
- 米饭

## 晚饭

## 加餐

---
*记录时间: YYYY-MM-DD HH:MM*
```

## 配置信息

**保存路径**: `/mnt/c/Users/loong/iCloudDrive/iCloud~md~obsidian/HomeMo.Art/05-Daily/`

**文件名格式**: `饮食记录-YYYY-MM-DD.md`

**脚本位置**: `scripts/log_diet.py`
