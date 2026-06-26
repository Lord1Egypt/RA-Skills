# ernie-image-art-name

> 名字转艺术字签名 Skill —— 使用百度星河社区 ERNIE-Image API，将姓名或任意文字生成为高质量艺术字/签名图片。

## ✨ 功能亮点

- **12 种预设风格**：经典艺术字 10 种 + 可爱单线卡通签名 + 软萌彩铅风卡通签名
- **多模板随机**：卡通签名类每次从多个精选 Prompt 模板中随机选取，多次生成效果不重复
- **精准中文文字渲染**：ERNIE-Image 在中文文字渲染方面处于行业领先水平
- **零依赖**：核心脚本仅用 Python 标准库，无需安装任何第三方包
- **灵活配置**：支持命令行参数、环境变量、配置文件三种 Token 传入方式

## 🚀 快速上手

### 1. 获取 Access Token

前往 [星河社区个人中心](https://aistudio.baidu.com/account/accessToken) 获取 Token，然后保存：

```bash
python3 scripts/generate_art_name.py --set-token YOUR_TOKEN
```

### 2. 生成艺术字/签名

直接和 AI 说：

> 帮我把"张伟"生成一张中国风艺术字图片
> 帮我用"Alice"生成一张可爱单线卡通签名

或使用命令行：

```bash
# 经典中国风
python3 scripts/generate_art_name.py --name "张伟"

# 可爱单线卡通签名（适合英文名/拼音，随机模板）
python3 scripts/generate_art_name.py --name "Alice" --style 单线卡通

# 软萌彩铅风卡通签名
python3 scripts/generate_art_name.py --name "Alice" --style 彩铅卡通

# 完全自定义描述
python3 scripts/generate_art_name.py --name "张伟" --style 自定义 --prompt "蒸汽朋克风格，齿轮装饰，深棕色背景"

# 查看所有风格
python3 scripts/generate_art_name.py --list-styles
```

## 🎨 支持风格

### 经典艺术字风格

| 风格 | 描述 |
|---|---|
| 中国风 | 毛笔书法，水墨金色，古典大气 |
| 烫金 | 金属质感，浮雕效果，豪华精致 |
| 霓虹 | 霓虹灯管，赛博朋克，发光效果 |
| 卡通 | 圆润字体，彩虹渐变，活泼可爱 |
| 石刻 | 篆刻浮雕，青铜质感，古朴沧桑 |
| 玫瑰 | 花卉装饰，浪漫粉色，优雅精致 |
| 极简 | 黑白几何，现代设计，高端简洁 |
| 火焰 | 燃烧效果，橙红火焰，动感强烈 |
| 冰晶 | 霜冻效果，蓝白透明，雪花装饰 |
| 自定义 | 配合 `--prompt` 完全自定义描述 |

### 卡通签名风格（v1.1.0 新增）

| 风格 | 描述 | 模板数 |
|---|---|---|
| 单线卡通 | 极简黑色单线手绘，ins 风可爱简笔画，无填充，花体英文签名与卡通元素融合（星星/兔子/小熊/蝴蝶等），纯白背景 | 7 种 |
| 彩铅卡通 | 软萌彩铅手绘风，黑色花体字搭配迷你卡通元素，点缀低饱和马卡龙色（粉/黄/蓝），治愈系 ins 风 | 4 种 |

> 💡 **提示**：卡通签名风格每次调用从多个模板随机选取，多次生成可获得不同效果。此类风格更适合**英文名或拼音**，中文名字效果可能偏弱。

## ⚙️ 参数说明

| 参数 | 简写 | 说明 |
|---|---|---|
| `--name` | `-n` | 要生成的名字或文字（必填） |
| `--style` | `-s` | 预设风格名称，默认：中国风 |
| `--prompt` | `-p` | 自定义风格描述（`--style 自定义` 时生效） |
| `--output` | `-o` | 图片保存目录，默认 `./art_names` |
| `--token` | `-t` | 临时指定 Access Token |
| `--model` | `-m` | 模型：ERNIE-Image / ERNIE-Image-Turbo / Stable-Diffusion-XL |
| `--set-token` | — | 将 Token 永久保存到配置文件 |
| `--list-styles` | — | 列出所有可用风格 |
| `--show-config` | — | 显示当前配置 |

## 🔑 Token 配置优先级

1. 命令行 `--token YOUR_TOKEN`
2. 环境变量 `export AISTUDIO_ACCESS_TOKEN=YOUR_TOKEN`
3. 配置文件 `config.json`（skill 目录下）

## 📋 依赖说明

- Python 3.6+（仅标准库，无需 pip install）
- 百度星河社区账号（免费，100万 Tokens 免费额度）

## 📄 License

MIT
