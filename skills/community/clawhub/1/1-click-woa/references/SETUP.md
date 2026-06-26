# 1-Click WOA 安装配置指南

## 前置要求

- OpenClaw 已安装并正常运行
- 微信公众号账号（已认证服务号最佳，订阅号功能受限）
- Node.js 16+ / Python 3.8+

---

## Step 1：获取微信 AppID 和 AppSecret

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入 **设置与开发 → 基本配置**
3. 找到 **AppID** 和 **AppSecret**
4. 若 AppSecret 未生成，点击"重置"获取

> ⚠️ AppSecret 是重要凭证，请勿泄露给他人

---

## Step 2：创建配置文件

```bash
mkdir -p ~/.openclaw/agents/gzh-assistant/wechat
```

创建文件 `~/.openclaw/agents/gzh-assistant/wechat/credentials.json`：

```json
{
  "app_id": "wx1234567890abcdef",
  "app_secret": "abcdef1234567890abcdef1234567890",
  "image_dir": "/root/wechat_images"
}
```

| 字段 | 说明 |
|------|------|
| `app_id` | 微信 AppID |
| `app_secret` | 微信 AppSecret |
| `image_dir` | 图片存放目录（绝对路径） |

---

## Step 3：准备图片目录

```bash
mkdir -p ~/wechat_images
```

将以下图片放入目录：

| 文件名 | 说明 | 必须 |
|--------|------|------|
| `cover.png` / `cover.jpg` | 封面图 | ✅ 必须 |
| `layer1.png` / `layer1.jpg` | 内容图1 | 可选 |
| `layer2.png` / `layer2.jpg` | 内容图2 | 可选 |
| `layer3.png` / `layer3.jpg` | 内容图3 | 可选 |
| `layer4.png` / `layer4.jpg` | 内容图4 | 可选 |

**图片要求：**
- 封面图尺寸：900×383 px
- 内容图宽度：≤1080px
- 格式：PNG 或 JPG

---

## Step 4：测试配置

```bash
cd ~/.openclaw/agents/gzh-assistant/skills/1-click-woa/scripts
python3 test_config.py
```

成功输出：
```
✅ credentials.json 存在
✅ AppID 格式正确
✅ AppSecret 格式正确
✅ image_dir 目录存在
✅ cover.png 存在
```

---

## 目录结构

```
~/.openclaw/agents/gzh-assistant/
├── wechat/
│   └── credentials.json    ← 用户的配置文件（不提交到 clawhub）
├── skills/
│   └── 1-click-woa/
│       ├── SKILL.md
│       ├── scripts/
│       │   └── publish.py
│       └── references/
│           ├── SETUP.md
│           └── TROUBLESHOOTING.md
└── wechat_images/         ← 图片目录
    ├── cover.png
    └── layer1-4.png
```

---

## 凭证安全说明

- `credentials.json` 包含敏感信息，**不要提交到代码仓库**
- clawhub 发布时会自动忽略 `credentials.json`
- 建议定期更换 AppSecret
