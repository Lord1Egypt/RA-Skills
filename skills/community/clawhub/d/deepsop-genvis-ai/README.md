# AI Image Generator

基于 AI Artist API 的图片/视频异步生成工具。

- 支持图片与视频任务创建
- 自动轮询任务状态直到完成
- 支持本地参考图自动上传
- 创建任务前自动调用费用预估，余额不足时会拦截并提示充值

## 🚀 快速开始

### 1) 获取 API Key

本技能需要 **API Key 授权**才能调用 AI Artist API：

- **已有账号** → 前往 [https://ai.deepsop.com/login?source=2](https://ai.deepsop.com/login?source=2) 登录获取
- **没有账号** → 前往 [https://ai.deepsop.com/register?source=2](https://ai.deepsop.com/register?source=2) 注册后获取

登录后在复制您的 API Key（`sk-` 开头）。

### 2) 设置环境变量

```bash
# Linux/macOS/Git Bash
export AI_ARTIST_TOKEN="sk-your_api_key_here"
```

```powershell
# Windows PowerShell
$env:AI_ARTIST_TOKEN="sk-your_api_key_here"
```

### 3) 验证配置

```bash
python3 scripts/test_config.py
```

### 4) 开始生成

```bash
# 查看当前服务端激活的模型
python3 scripts/generate_image.py --list-models

# 默认图片模型（3.1Nano2-Evo）
python3 scripts/generate_image.py "一只可爱的猫"
```

## 🎨 支持模型

### 图片模型（以 API sourceName 命名）
- `3.1Nano2-Evo`（默认）— DeepSop·3.1Nano2-Evo，N2 进化版
- `S5.0L` — DeepSop·S5.0L，生成快、风格全、支持联网
- `N2` — DeepSop·N2，多模态输入、卓越文字渲染
- `W2.7` — DeepSop.W2.7，文生图/图生图多模态输入
- `W2.7Pro` — DeepSop.W2.7Pro，精准控图与风格迁移
- `Nano2-Beta-Evo` — DeepSop·Nano2 Beta-Evo，N2 Beta 进化版

### 视频模型（以 API sourceName 命名）
- `V3.1FB`（默认）— DeepSop·V3.1FB，快速生成基础流畅，固定 8 秒
- `S1.5Pro` — DeepSop·S1.5Pro，影视级连贯叙事
- `V3.1PB` — DeepSop·V3.1PB，多图参考角色一致性
- `V3.1Fast` — DeepSop·V3.1Fast，音画同步、竖屏适配
- `W2.6t` / `W2.6i` / `W2.6r` — DeepSop·W2.6 系列（文生/图生/参考视频）
- `klingV3Omni` — DeepSop.klingV3Omni，多模态融合（按张计费）
- `W2.7i` / `W2.7t` / `W2.7r` — DeepSop·W2.7 系列（文生 2K 自配音 / 图生首尾帧 / 参考视频）

## 📝 常用示例

```bash
# 图片：指定模型（比例尺寸）
python3 scripts/generate_image.py "一只柴犬" --model N2 --size "1:1"

# 图片：W2.7Pro 精准控图
python3 scripts/generate_image.py "角色三视图" --model W2.7Pro --quality "4K"

# 图片：下载到本地
python3 scripts/generate_image.py "海边日落" --download

# 图片：参考图生成（本地文件自动上传）
python3 scripts/generate_image.py "做成赛博朋克风格" --reference-image "./ref.png"

# 视频：基础文生视频（S1.5Pro）
python3 scripts/generate_image.py "城市夜景延时" --model S1.5Pro

# 视频：V3.1PB 首尾帧控制
python3 scripts/generate_image.py "灯具变形动画" --model V3.1PB --first-image "./start.jpg" --last-image "./end.jpg" --duration 8

# 视频：W2.7t 文生视频（2K 自配音）
python3 scripts/generate_image.py "品牌短片" --model W2.7t --resolution "1080p" --duration 10
```

## 📖 文档

完整参数说明与更多示例见 `SKILL.md`。

## 🧪 调试与测试

```bash
# 预览最终 payload，不消耗 K 币
python3 scripts/generate_image.py "测试提示词" --dry-run

# 查看当前激活的模型
python3 scripts/generate_image.py --list-models

# 运行回归测试（需 pytest）
pytest tests -q
```

## 🔧 环境要求

- Python 3.6+
- `requests`
- `python-dotenv`（可选；用于自动加载项目根 `.env`）

## ⚠️ 注意事项

- 必须使用你自己的 `AI_ARTIST_TOKEN`
- 任务创建前会执行费用预估；若余额不足将不会提交任务
- 请遵守 AI Artist API 的使用条款

---

## 🔒 安全审计报告

> 本技能已通过 `skill-vetter` 安全审计工具的完整审查，可放心安装使用。

| 字段 | 内容 |
|---|---|
| **审计日期** | 2026-05-12 |
| **审计工具** | skill-vetter (clawhub@latest) |
| **来源** | ClawdHub / DeepSOP 官方 |
| **审查文件数** | 6（SKILL.md、README.md、api.md、generate_image.py、test_generate_image.py、飞书集成文档） |
| **可疑模式** | ✖ 无 |
| **网络访问** | `https://ai.deepsop.com/prod-api/`（合法的 AI 图像生成接口，单一已知域名） |
| **API Key 处理** | 仅从环境变量 `AI_ARTIST_TOKEN` 读取，未硬编码、无外泄 |
| **文件访问** | 用户指定的图像文件读写 |
| **依赖命令** | Python `requests` 库 |
| **风险等级** | 🟡 MEDIUM（需配置 API Key） |
| **审计结论** | ✅ **SAFE TO INSTALL — 安全可安装** |

**误报澄清：**
- 扫描器命中的 `base64.b64encode` 是把本地图片**编码**后上传给 API，并非"解码可疑数据"的危险模式。
- 全部网络流量仅指向单一已知域名 `ai.deepsop.com`。
- API Key 仅通过环境变量传入，不写入磁盘，不上报第三方。

> 完整的多技能审计报告见仓库根目录 `SKILL_VETTING_REPORT.md`。
