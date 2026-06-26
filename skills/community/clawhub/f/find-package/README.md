# 找快递 (find-package)

一个 [OpenClaw](https://openclaw.com) 技能，通过 Telegram Bot 帮你在驿站货架上找到自己的快递。

## 工作流程

1. **发送取件码** — 直接输入文字（如 `5-2-1234`），或者截图发过来（短信通知、菜鸟裹裹等 App 截图都行）
2. **拍货架照片** — 对着货架拍照发给 Bot，一次可以发多张
3. **自动识别匹配** — Bot 识别照片上的取件码，找到匹配的快递后用红框标出来
4. **结果反馈** — 找到的快递会标注在照片上发回给你，多个快递会逐个追踪，全部找到后提示完成

## 安装

将 `find-package/` 目录复制到 OpenClaw 的 skills 目录下即可。

### 依赖

- Python 3
- [Pillow](https://pillow.readthedocs.io/)（图片标注用）

```bash
pip3 install Pillow
```

## 文件结构

```
find-package/
├── SKILL.md              # 技能定义与工作流指令
└── scripts/
    └── annotate.py       # 图片红框标注脚本
```

## annotate.py 用法

独立使用标注脚本：

```bash
# 单个标注
python3 find-package/scripts/annotate.py \
  --input photo.jpg \
  --output result.jpg \
  --box "100,200,300,400" \
  --label "取件码: 5-2-1234"

# 多个标注
python3 find-package/scripts/annotate.py \
  --input photo.jpg \
  --output result.jpg \
  --box "100,200,300,400" --label "5-2-1234" \
  --box "500,200,700,400" --label "3-1-5678"
```

## 触发方式

在 Telegram 中对 OpenClaw Bot 说：

- "帮我找快递"
- "我要取件"
- "取件码是 5-2-1234"
- "快递在哪"

等类似的话即可触发。
