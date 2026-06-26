# 88查招投标搜索指南

## 功能说明

通过 CLI 调用 88查招投标搜索接口，根据关键词搜索招投标公告信息，支持分页查询。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）

## CLI 调用

```bash
python3 {baseDir}/cli.py bidding_search --keyword "搜索关键词" [--provinces "省1" "省2"] [--cities "市1"] [--regions "区1"] [--startTime <毫秒时间戳>] [--endTime <毫秒时间戳>]
```

### 参数说明

| 参数 | 缩写 | 是否必填 | 说明 |
|------|------|----------|------|
| `--keyword` | `-k` | 是 | 搜索关键词 |
| `--pageNo` | `-n` | 否（默认 1） | 页码 |
| `--pageSize` | `-s` | 否（默认 10） | 每页条数 |
| `--provinces` | - | 否 | 省份筛选，多个空格分隔。必须使用全称（如"浙江省"） |
| `--cities` | - | 否 | 城市筛选，多个空格分隔。必须使用全称（如"杭州市"） |
| `--regions` | - | 否 | 区域筛选，多个空格分隔。必须使用全称（如"西湖区"） |
| `--startTime` | - | 否 | 起始时间戳（毫秒），筛选发布日期 >= startTime 的记录 |
| `--endTime` | - | 否 | 截止时间戳（毫秒），筛选发布日期 <= endTime 的记录 |

### 区域参数格式规则

Agent 传入 provinces/cities/regions 参数时，**必须使用带行政后缀的全称**：
- 省份：浙江省、广东省、四川省（非"浙江"、"广东"）
- 城市：杭州市、深圳市、成都市（非"杭州"、"深圳"）
- 区县：西湖区、南山区（非"西湖"、"南山"）

如果用户说的是简称，Agent 应自动补全后缀再传入。

### 调用示例

```bash
# 基本搜索
python3 {baseDir}/cli.py bidding_search -k "智慧城市" -n "1" -s "10"

# 带省份筛选
python3 {baseDir}/cli.py bidding_search -k "智慧城市" --provinces "浙江省" "江苏省"

# 带省份+城市筛选
python3 {baseDir}/cli.py bidding_search -k "服务器" --provinces "广东省" --cities "深圳市"

# 多地区组合
python3 {baseDir}/cli.py bidding_search -k "办公家具" --provinces "浙江省" --cities "杭州市" "宁波市"

# 带时间范围筛选（只看最近7天）
python3 {baseDir}/cli.py bidding_search -k "智慧城市" --startTime 1716249600000 --endTime 1716854400000
```

## 输出格式

### 成功

`markdown` 字段包含格式化好的表格，Agent 直接输出即可，无需自行解析 `data`。

```json
{
  "success": true,
  "markdown": "搜索「智慧城市」的招投标信息（第 1 页，每页 10 条）：\n\n| # | 标题 | 类型 | 发布日期 | 地区 | 招标单位 | 中标单位 | 招标产品 | 中标金额 |\n|---|------|------|----------|------|----------|----------|----------|----------|\n| 1 | ... | 中标 | 2025年01月01日 | 北京市 | ... | ... | ... | 100万元 |",
  "data": {
    "data": { ... }
  }
}
```

表格列：`#` 序号 | `标题` | `类型`（subBidType / bidType）| `发布日期` | `地区`（省+市）| `招标单位` | `中标单位` | `招标产品` | `中标金额`（空值显示 `-`）

HTML 标签已自动去除，无需额外处理。

### 无结果

```json
{
  "success": true,
  "markdown": "未找到与「关键词」相关的招投标信息。",
  "data": { "data": { "data": [] } }
}
```

### 失败 — AK 未配置

```json
{
  "success": false,
  "markdown": "AK 未配置。\n\n运行: `cli.py configure YOUR_AK`"
}
```

### 失败 — 其他异常

```json
{
  "success": false,
  "markdown": "错误描述信息"
}
```

## Agent 处理流程

```
1. 从用户消息中提取：搜索关键词、区域（省/市/区）、时间范围（可选）、页码（可选）、每页条数（可选）
2. 区域参数必须使用带行政后缀的全称（浙江省、杭州市、西湖区），用户简称需自动补全
3. 执行搜索：
   python3 {baseDir}/cli.py bidding_search --keyword <关键词> [--provinces <省1> <省2>] [--cities <市1>] [--regions <区1>] [--startTime <毫秒时间戳>] [--endTime <毫秒时间戳>] [--pageNo <页码>] [--pageSize <每页条数>]
4. 检查输出：
   - success=true → 直接输出 markdown 字段
   - success=false → 直接输出 markdown 字段（错误描述）
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| 参数缺失（keyword） | 提示用户补充搜索关键词 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |
