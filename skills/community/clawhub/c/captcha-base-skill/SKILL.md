---
name: captcha-skill
description: 免费优先的验证码基础能力 Skill。默认本地识别，复杂场景可切换低价云码兜底。适用于 OpenClaw/ClawHub、浏览器自动化与 RPA 场景。
---

# 验证码基础能力 Skill

这是一个面向公共场景的验证码基础能力 Skill，目标很直接：

- 常见验证码，优先用本地免费能力解决
- 本地不稳或题型复杂时，再切到低价云码兜底
- 让调用方尽量只关心“要识别什么”，而不是先研究一堆接口细节

它更适合被当成一个公共底层能力来用，而不是单一网站的定制脚本。

## 给 Agent 的最短说明

如果你是另一个 Skill 或 Agent，请先按下面规则使用：

1. 默认入口用 `JfbymClient.solve_auto_fallback(...)`
2. 简单文本、算术、基础滑块，默认 `prefer="free"`
3. 点选、九宫格、空间推理、旋转、ReCaptcha、hCaptcha，优先直接走付费接口
4. 输入支持三种形式：文件路径、`bytes`、base64 字符串
5. 成功结果优先读取返回值里的 `result` 或云码接口 `data`

最常用入口：

- 文本：`solve_auto_fallback(task="text", image_input=...)`
- 算术：`solve_auto_fallback(task="math", image_input=...)`
- 滑块：`solve_auto_fallback(task="slide", back_image_input=..., slide_image_input=...)`
- 复杂题型：`solve_common(...)` / `solve_slide(...)`

如果你只需要模块选择：

- 只要本地免费能力：`local_captcha.py`
- 只要云码 SDK：`jfbym_sdk.py`
- 想自动兜底、保留兼容入口、或直接用 CLI：`jfbym_api.py`

## 云端与隐私说明

这部分请在调用前明确理解：

- 本地免费能力不需要 `JFBYM_TOKEN`
- `JFBYM_TOKEN` 仅在调用云端收费接口时使用，是可选项，不是本 Skill 的必填前置条件
- 云端兜底平台为云码 JFBYM：<https://console.jfbym.com/register/TG133710>
- 一旦启用云端兜底，传入的图片数据和 `JFBYM_TOKEN` 会发送到 `https://api.jfbym.com`
- 代码中包含固定 `developer_tag`，用于渠道归因

如果你的场景对隐私更敏感：

- 只使用本地免费能力
- 不设置 `JFBYM_TOKEN`
- 不把非验证码敏感图片传给云端接口

## 调用边界摘要

- 本地模式：不上传图片，不需要 token
- 云端模式：会把调用时传入的图片发送到 `https://api.jfbym.com`
- 云端模式：会发送 `JFBYM_TOKEN`（如果已配置）
- 不读取其他系统凭据
- 不修改系统配置
- 不要求常驻运行

## 适合谁

- 需要验证码基础能力的 OpenClaw / ClawHub Skill 作者
- 做浏览器自动化、RPA、数据采集的人
- 想先免费解决大部分简单场景，再为复杂题型保留便宜兜底的人

## 核心定位

- 免费优先：文本、算术、基础滑块可先走本地能力
- 低价兜底：复杂场景可接云码 API，按量付费
- 开发友好：支持文件路径、`bytes`、base64，适合脚本和二次封装
- 场景覆盖广：文本、算术、滑块、点选、旋转、空间推理、ReCaptcha/hCaptcha

## 什么时候用哪种方式

| 场景 | 推荐策略 | 原因 |
|---|---|---|
| 4-6 位文本验证码 | 免费优先 | 本地 OCR 往往够用，零成本 |
| 简单算术验证码 | 免费优先 | 本地识别后可直接算结果 |
| 常见双图滑块 | 免费优先 | ddddocr / OpenCV 可先跑 |
| 点选、九宫格、空间推理 | 直接付费 | 本地通用能力不稳定，直接走云码省时间 |
| 旋转、轨迹验证 | 直接付费 | 题型偏复杂，云码成功率更稳 |
| ReCaptcha / hCaptcha / Turnstile | 直接付费 | 属于典型云端令牌场景 |

一句话：

- 简单题，先免费
- 复杂题，直接低价兜底
- 不确定时，就用 `solve_auto_fallback`

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 最推荐的用法：自动策略

```python
from jfbym_api import JfbymClient

client = JfbymClient()  # 不配 token 也能先跑免费分支

ret = client.solve_auto_fallback(
    task="text",
    image_input="captcha.png",
    charset_range="0123456789",
)

print(ret)
```

默认 `prefer="free"`，也就是：

- 先走本地免费能力
- 免费失败时，若已配置 `JFBYM_TOKEN`，再自动走付费兜底

返回结构固定优先看这几个字段：

```python
{
  "task": "text|math|slide",
  "mode": "free|paid",
  "result": ...,
  "fallback_reason": "..."  # 仅在发生兜底时存在
}
```

### 3. 命令行直接跑

文本验证码：

```bash
python jfbym_api.py text --image captcha.png --charset 0123456789
```

算术验证码：

```bash
python jfbym_api.py math --image math.png
```

双图滑块：

```bash
python jfbym_api.py slide --background back.png --slide slide.png
```

如需优先走付费兜底：

```bash
python jfbym_api.py text --image captcha.png --prefer paid
```

输出默认为 JSON，方便给其他 Skill 或 Agent 继续处理。

猜你该用哪个 `captcha_type`：

```bash
python jfbym_api.py guess --description "九宫格点选"
```

查余额：

```bash
python jfbym_api.py balance
```

返分：

```bash
python jfbym_api.py report-error --unique-code 打码返回的uniqueCode
```

## 输入与输出约定

### 输入约定

- `image_input`：文件路径、`bytes`、base64
- `back_image_input` / `slide_image_input`：文件路径、`bytes`、base64
- `extra`：复杂点选/推理类场景的文字提示
- `paid_captcha_type`：覆盖默认云码类型

### 输出约定

- 自动策略接口：统一返回外层结构 `task/mode/result/fallback_reason`
- 本地文本识别：返回 `str`
- 本地算术识别：返回 `dict`
- 本地滑块识别：返回 `dict` 或 `int`
- 云码接口：返回云码原始 `data`

Agent 调用建议：

- 自动策略返回时，优先读 `ret["result"]`
- 云码接口返回时，优先读 `ret.get("data")` 或按题型字段读取
- 不要假定所有付费题型返回结构完全一致

## 免费能力（本地）

> 适合优先降本，覆盖常见简单验证码。无需 `token`。

### 支持能力

- 通用文本识别：`solve_local_text_captcha(image_input)`
- 字符集约束识别：`solve_local_text_captcha_with_range(image_input, charset_range=...)`
- 算术验证码识别：`solve_local_math_captcha(image_input)`
- 文本框检测：`detect_local_text_boxes(image_input)`
- 滑块匹配（ddddocr）：`solve_local_slide_distance_ddddocr(back, slide)`
- 滑块匹配（OpenCV）：`solve_local_slide_distance(back_base64, slide_base64)`

### 适用建议

- 纯数字、纯字母、简单字母数字混合：优先免费
- 简单算术题：优先免费
- 常见双图滑块：优先免费
- 干扰严重、点选、旋转、空间推理：通常直接走云码更省时间

### 免费本地示例

```python
from jfbym_api import JfbymClient

text = JfbymClient.solve_local_text_captcha("captcha.png")
math_ret = JfbymClient.solve_local_math_captcha("math.png")
slide_ret = JfbymClient.solve_local_slide_distance_ddddocr("back.png", "slide.png")
```

## 低价兜底能力（云码 API / JFBYM）

> 适合复杂验证码或高成功率场景。仅在调用云端接口时需要 `token`。

平台主页：

- <https://console.jfbym.com/register/TG133710>

### 透明说明

- 这是我推荐的低价兜底渠道，不影响免费功能使用
- 你完全可以只用本地免费能力，不注册、不充值也没问题

注册链接：

- <https://console.jfbym.com/register/TG133710>

### 为什么我愿意推荐它

- 价格低，适合作为“偶尔才用一次”的兜底渠道
- 很多验证码场景本来就不高频，通常不需要高额充值
- 文本、算术、基础滑块本来就可以先走本地免费，只有复杂题型才建议付费

### token 配置

```bash
export JFBYM_TOKEN="你的云码token"
```

Windows PowerShell:

```powershell
$env:JFBYM_TOKEN="你的云码token"
```

### 常见复杂题型

价格来源：<https://www.jfbym.com/price.html>（日期：2026-03-12）

| 场景 | 推荐 type | 低至价格 | 推荐接口 | 关键说明 |
|---|---|---|---|---|
| 空间推理点选（无确定按钮） | `50009` | `0.012元` | `solve_common` | 如：点击侧对着你的字母 |
| 空间推理点选（有确定按钮） | `30340` | `0.01元` | `solve_common` | 如：点击正方体上面字母的小写字母 |
| 文字点选（通用） | `30100` | `0.01元` | `solve_common` | 按顺序点击需求文字 |
| 推理拼图 | `30108` | `0.008元` | `solve_common` | 交换 2 个图块 |
| 九宫格点选 | `30008` | `0.01元` | `solve_common` | 9 宫格图片验证 |
| 双图滑块（收费兜底） | `20111` | `0.01元` | `solve_slide` | 2 个或多个缺口的滑块场景 |
| 轨迹验证/单图滑块优化 | `22222` | `0.008元` | `solve_common` | 返回坐标或偏移相关结果 |
| 单图旋转 | `90007` | `按官网/定制` | `solve_common` | 通用旋转验证码 |
| 双图旋转 | `90004` | `0.01元` | `solve_common` | 内圈、外圈图片旋转验证 |
| 双图旋转（高频场景） | `90015` | `按官网/定制` | `solve_common` | 返回 `rotate_angle` 和 `slide_px` |
| 问答题 | `50103` | `0.016元` | `solve_common` | 看图问答 |

说明：价格与活动可能随时间变化，最终请以官网实时页面为准。

## 推荐调用策略

### 方案 A：大多数人最适合

- 文本：先 `solve_auto_fallback(task="text", ...)`
- 算术：先 `solve_auto_fallback(task="math", ...)`
- 滑块：先 `solve_auto_fallback(task="slide", ...)`

### 方案 B：你已经明确知道是复杂题型

- 点选、空间推理、旋转、ReCaptcha、hCaptcha
- 直接走云码接口，减少本地重试

## 典型场景

### 场景 1：登录页数字验证码

```python
from jfbym_api import JfbymClient

client = JfbymClient()
ret = client.solve_auto_fallback(
    task="text",
    image_input="captcha.png",
    charset_range="0123456789",
)
```

### 场景 2：算术验证码

```python
from jfbym_api import JfbymClient

ret = JfbymClient.solve_local_math_captcha("math.png")
print(ret["result"])
```

### 场景 3：双图滑块

```python
from jfbym_api import JfbymClient

client = JfbymClient()
ret = client.solve_auto_fallback(
    task="slide",
    back_image_input="back.png",
    slide_image_input="slide.png",
)
```

### 场景 4：九宫格 / 空间推理 / 点选

```python
from jfbym_api import JfbymClient

client = JfbymClient()
ret = client.solve_common(
    image_input=image_b64,
    captcha_type="30008",
    label_image=label_image_b64,
)
```

### 场景 5：不确定该走哪个付费 type

```bash
python jfbym_api.py guess --description "点击所有朝向左边的字母"
```

## 自动策略接口

统一入口：

- `solve_auto_fallback(task, image_input=None, back_image_input=None, slide_image_input=None, charset_range=None, paid_captcha_type=None, extra=None, prefer="free")`

### 参数说明

- `task`: 必填。支持 `text` / `math` / `slide`
- `image_input`: `text`、`math` 任务必填。支持文件路径、`bytes`、base64
- `back_image_input`、`slide_image_input`: `slide` 任务必填
- `charset_range`: 文本任务可选。可限制字符集
- `paid_captcha_type`: 可选。覆盖默认云码 type
- `extra`: 可选。透传给收费 `solve_common`
- `prefer`: `free` 或 `paid`，默认 `free`

### 返回结构

```python
{
  "task": "text|math|slide",
  "mode": "free|paid",
  "result": ...,
  "fallback_reason": "..."  # 仅在发生兜底时存在
}
```

### 示例

```python
from jfbym_api import JfbymClient

client = JfbymClient()

text_ret = client.solve_auto_fallback(
    task="text",
    image_input="captcha.png",
    charset_range="0123456789",
)

math_ret = client.solve_auto_fallback(
    task="math",
    image_input="math.png",
)

slide_ret = client.solve_auto_fallback(
    task="slide",
    back_image_input="back.png",
    slide_image_input="slide.png",
)
```

## 进阶：直接调用云码接口

### 通用单图接口

```python
ret = client.solve_common(
    image_input=image_b64,
    captcha_type="30100",
    extra="猫,狗,车",
)
```

### 双图滑块接口

```python
ret = client.solve_slide(
    slide_image="slide.png",
    bg_image="back.png",
    captcha_type="20111",
)
```

### 双图旋转（90015）

```python
ret = client.solve_common(
    image_input=None,
    out_ring_image=out_ring_b64,
    inner_circle_image=inner_circle_b64,
    captcha_type="90015",
)

rotate_angle = ret.get("data", {}).get("rotate_angle")
slide_px = ret.get("data", {}).get("slide_px")
```

## 识别结果说明

### 免费本地接口返回

- `solve_local_text_captcha(...)`：返回 `str`
- `solve_local_text_captcha_with_range(...)`：返回 `str`
- `solve_local_math_captcha(...)`：返回 `dict`
- `detect_local_text_boxes(...)`：返回 `list`
- `solve_local_slide_distance_ddddocr(...)`：返回 `dict`
- `solve_local_slide_distance(...)`：返回 `int`

### 收费云码接口返回

- `solve_common(...)`：返回云码接口 `data`
- `solve_slide(...)`：返回云码接口 `data`
- `solve_recaptcha(...)`：返回可提交 token
- `get_balance()`：返回积分余额
- `report_error(unique_code)`：返回是否退款成功
- `guess_captcha_type(description)`：返回推荐 type

## 安全与边界

- 本地免费能力不会上传图片到第三方 API
- 使用云码兜底时，图片会提交到第三方服务，请自行评估场景敏感度
- 建议不要把它用于含有敏感隐私信息的整页截图上传场景
- 调用方最好自己控制失败重试次数，避免无意义消耗

## 依赖建议

- 建议在虚拟环境或隔离环境中安装依赖
- ddddocr、OpenCV、Pillow、numpy 这类图像处理依赖体积可能较大
- 如果你只打算使用本地免费能力，先完成依赖安装再测试
- 如果你只打算接入云码 SDK，仍建议先在受控环境中验证网络调用与返回结构

## 开源致谢

本 Skill 的本地免费能力基于开源项目 [ddddocr](https://github.com/sml2h3/ddddocr) 构建，感谢作者与社区贡献。

## 支持与反馈

如果这个 Skill 对你有帮助，欢迎：

- 在 ClawHub 给它点个星标，能帮助更多人看到它
- 遇到问题时提交 issue 或直接反馈复现信息、错误样例、题型截图
- 分享你的使用场景，方便我继续优化免费能力和兜底策略

说明：

- 星标、反馈和真实案例都很重要，公共基础能力只有在被持续使用时才有维护价值
- 如果后续你有 GitHub 仓库，建议把这里补成正式的 Issues 链接

## 项目结构

```text
captcha-base-skill/
├── SKILL.md
├── requirements.txt
├── local_captcha.py   # 本地免费能力
├── jfbym_sdk.py       # 云码 SDK
└── jfbym_api.py       # 统一门面 + 自动兜底 + CLI
```
