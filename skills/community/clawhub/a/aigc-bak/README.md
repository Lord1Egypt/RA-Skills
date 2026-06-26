# AIGC Image Generator

AI 图片生成接口 Skill，支持文生图功能。

## 文件说明

- `SKILL.md` - 技能说明文档
- `generate.py` - Python 调用脚本
- `config.env` - 配置文件（可选）
- `README.md` - 本文件

## 快速测试

```bash
# 基础测试
python3 generate.py "一只可爱的小猫在阳光下打盹"

# 带参数测试
python3 generate.py "未来城市夜景" --negative "模糊,低质量" --ratio 5 --batch 2
```

## 集成到 OpenClaw

这个 Skill 已经可以被 OpenClaw 自动识别和调用。当用户说：
- "生成一张图片..."
- "画一张..."
- "帮我生成..."

OpenClaw 会自动调用这个 Skill。

## 配置说明

如果需要修改 API 地址或其他配置，编辑 `generate.py` 中的常量：

```python
BASE_URL = "http://localhost:8082"
CLIENT_ID = "openclaw-kinggu"
PROVIDER = 4
```

## 依赖

需要安装 `requests` 库：

```bash
pip3 install requests
```

## 状态码说明

根据接口返回的 `status` 字段：
- `0` - 排队中
- `1` - 生成中
- `2` - 成功
- `<0` - 失败

脚本会自动轮询直到任务完成或超时（默认 120 秒）。
