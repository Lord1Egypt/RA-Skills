---
name: jisu-character
description: MBTI 完整版或简版逐题作答，提交后获取性格类型结果。当用户说：我想测个 MBTI、给我性格测试题，或类似 MBTI 测评时，使用本技能。
metadata: { "openclaw": { "emoji": "🧠", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据 MBTI 性格测试（Jisu Character / MBTI）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **获取题目**（`/character/questions`），支持 `full`（93 题）与 `simple`（28 题）
- **提交答案获取结果**（`/character/answer`）
- **逐题推进模式**：每次返回 1 道题，用户选择 A/B 后继续下一题，最后自动提交并返回 MBTI 结果

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [MBTI 性格测试 API](https://www.jisuapi.com/api/character/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/character/character.py`

## 使用方式与请求参数

### 1. 获取题目列表（/character/questions）

```bash
# full（默认）
python3 skills/character/character.py questions

# simple
python3 skills/character/character.py questions '{"version":"simple"}'
```

请求 JSON：

```json
{
  "version": "full"
}
```

| 字段名   | 类型   | 必填 | 说明                 |
|----------|--------|------|----------------------|
| version  | string | 否   | `full` / `simple`，默认 `full` |

### 2. 逐题返回题目并作答（推荐）

这个模式用于「拿到题目以后，一个个返回题目让用户做；用户完成以后，再拼接选项拿到结果」。

#### 2.1 获取第一题

```bash
python3 skills/character/character.py next '{"version":"full"}'
```

返回里会包含：

- `cursor`：当前题索引（0 开始）
- `total`：题目总数
- `picked`：已选择的选项编码数组（用于下一次调用原样带回）
- `question`：当前题（包含 `answer1/answer2` 文案）

#### 2.2 用户选择 A/B 后拿下一题

把上一轮返回的 `cursor` 与 `picked` 带上，再附加 `choice`（A 或 B）：

```bash
python3 skills/character/character.py next '{"version":"full","cursor":0,"picked":[],"choice":"A"}'
```

当最后一题完成后，返回将包含：

- `done: true`
- `answer`：拼接后的答案字符串（逗号分隔）
- `result`：MBTI 结果（type/name/summary/characteristic/field/job 等）

请求 JSON（逐题模式）：

```json
{
  "version": "full",
  "cursor": 0,
  "picked": ["x1", "y2"],
  "choice": "A"
}
```

| 字段名  | 类型          | 必填 | 说明 |
|--------|---------------|------|------|
| version | string       | 否   | `full` / `simple`，默认 `full` |
| cursor  | int          | 否   | 当前题索引（0 开始），默认 0 |
| picked  | array<string>| 否   | 已选编码数组（原样回传） |
| choice  | string       | 否   | 当前题选择：`A` 或 `B`（不传则仅返回当前题） |

### 3. 直接提交答案拿结果（/character/answer）

如果你已经在对话里收集到所有编码（例如 `x1,y1,x2,...`），可直接提交：

```bash
python3 skills/character/character.py answer '{"version":"simple","answer":"x1,y1,x2,y2"}'
```

也支持传数组：

```bash
python3 skills/character/character.py answer '{"version":"simple","answers":["x1","y1","x2","y2"]}'
```

### 4. 本地交互模式（终端逐题输入）

适合你自己在命令行里跑一遍测试（会逐题提示输入 A/B）：

```bash
python3 skills/character/character.py quiz '{"version":"full"}'
```

## 常见错误码

来自 [极速数据性格测试文档](https://www.jisuapi.com/api/character/) 的业务错误码：

| 代号 | 说明     |
|------|----------|
| 201  | 答案不足 |
| 210  | 没有信息 |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |
| 106  | IP 请求超过限制      |
| 107  | 接口维护中           |
| 108  | 接口已停用           |

## 推荐用法

1. 用户提问：「给我做一个 MBTI 测试（简单版）。」  
2. 代理调用：`python3 skills/character/character.py next '{"version":"simple"}'`，把返回的 `question` 展示给用户，只让用户回答 A 或 B。  
3. 用户每回答一次，代理把上一轮的 `cursor/picked` 带回，再加上 `choice` 调用 `next`，继续拿下一题。  
4. 当返回 `done: true` 时，把 `result` 里的 `type/name/summary/characteristic` 等字段整理成自然语言结果，并给出适合的职业建议（`field/job`）。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

