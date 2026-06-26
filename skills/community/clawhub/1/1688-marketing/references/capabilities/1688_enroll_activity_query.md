# 1688招商活动查询指南

## 功能说明

查询1688招商活动列表，支持按活动ID或名称关键词搜索，支持分页。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）

## CLI 调用

```bash
python3 {baseDir}/cli.py 1688_enroll_activity_query --pageNo 1 --pageSize 10 --keyword "活动名称"
```

### 参数说明

| 参数 | 缩写 | 是否必填 | 类型 | 说明 |
|------|------|----------|------|------|
| `--pageNo` | `-p` | 否 | Integer | 当前分页，默认1 |
| `--pageSize` | `-s` | 否 | Integer | 分页大小，默认10 |
| `--keyword` | `-k` | 否 | String | 活动Id或名称关键词 |

### 调用示例

```bash
# 查询第一页活动
python3 {baseDir}/cli.py 1688_enroll_activity_query

# 按关键词搜索
python3 {baseDir}/cli.py 1688_enroll_activity_query -k "618"

# 指定分页
python3 {baseDir}/cli.py 1688_enroll_activity_query -p 2 -s 20
```

## 输出格式

### 成功

```json
{
  "success": true,
  "markdown": "",
  "data": {
    "total": 5,
    "pageNo": 1,
    "pageSize": 10,
    "data": [...]
  }
}
```

## Agent 处理流程

```
1. 用户表达查询活动意图时，提取关键词（如有）
2. 执行 python3 {baseDir}/cli.py 1688_enroll_activity_query [--keyword <关键词>]
3. 检查输出：
   - success=true → 展示活动列表，引导用户选择感兴趣的活动
   - success=false → 原样输出错误信息
4. 用户选择活动后，可继续调用商品查询和报名流程
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| 无匹配活动 | 提示用户更换关键词或查看全部活动 |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 SKILL.md 异常处理章节。
