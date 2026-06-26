# AIGC Generator

文生图生成工具。

## 文件说明

- `SKILL.md` - OpenClaw 技能说明（主要）
- `generate.py` - Python 生成脚本
- `README.md` - 本文件

## 快速测试

```bash
# 基础测试
python3 scripts/generate.py "一只可爱的小猫在阳光下打盹"

# 带参数测试
python3 scripts/generate.py "未来城市夜景" --negative "模糊,低质量" --ratio 5 --batch 2
```

## 依赖

```bash
pip3 install requests
```
