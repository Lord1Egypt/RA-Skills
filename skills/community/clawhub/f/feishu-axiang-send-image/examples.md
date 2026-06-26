# 使用示例

## 基础用法

```bash
# 发送到默认用户（配置中的目标用户）
python scripts/send.py --file-path "C:\path\to\image.png"
```

## 发送到指定用户

```bash
# 发送到个人
python scripts/send.py --file-path "image.png" --target "ou_xxxxx"

# 发送到群聊
python scripts/send.py --file-path "image.png" --target "oc_xxxxx" --target-type chat_id
```

## Python API 调用

```python
# 导入模块
import sys
sys.path.insert(0, r"C:\Users\Xiabi\.agents\skills\feishu-axiang-send-image\scripts")
from send import send_image_to_feishu

# 发送到默认用户
result = send_image_to_feishu("image.png")
print(f"Message ID: {result['message_id']}")

# 发送到指定用户
result = send_image_to_feishu(
    "image.png",
    target="ou_xxxxx",
    target_type="open_id"
)
```

## 在 OpenClaw 中使用

```bash
# 通过 exec 调用
exec: python ~/.agents/skills/feishu-axiang-send-image/scripts/send.py --file-path "image.png"
```

## 批处理示例

```bash
# 发送多张图片
for img in *.png; do
    python scripts/send.py --file-path "$img"
done
```
