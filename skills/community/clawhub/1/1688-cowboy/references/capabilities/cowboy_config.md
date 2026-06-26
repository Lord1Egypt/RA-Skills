# cowboy_config（牛仔配置服务）

## 功能说明

牛仔（AI 客服）生命周期管理，提供创建、更新配置、暂停接待、恢复接待、加载配置五个操作。

## 网关接口

| 操作 | TPP 路径 | 说明 |
|------|----------|------|
| create | `api/create_cow_boy/1.0.0` | 创建牛仔（初始化卖家 AI 客服） |
| update | `api/update_cow_boy/1.0.0` | 更新牛仔配置信息 |
| pause | `api/pause_cow_boy/1.0.0` | 暂停牛仔接待，AI 客服停止自动回复 |
| resume | `api/resume_cow_boy/1.0.0` | 恢复牛仔接待，AI 客服重新开始自动回复 |
| load | `api/load_cow_boy/1.0.0` | 加载牛仔配置（读取 `agent_status` + 接待买家等级） |

### 请求体

`sellerUserId` 由网关从上下文自动注入，**不需要**业务代码显式传入。

#### create / update —— 必传 `allowBuyerLevelList`

```json
{
  "allowBuyerLevelList": "L0,L1,L2"
}
```

- `allowBuyerLevelList` ：**逗号分隔的字符串**，合法元素 `L0` ~ `L6`；service 层接受 `Iterable[str]` 业务参数，内部会去重 / 验证合法性后再 join。
- create 会把它存在服务端 `config` 字段的 JSON 中；update **仅更新**该部分，不影响 `enable` / pause 状态。
- create 在同一商家重复调用会报错（每商家只能创建一次）；update 需商家已有配置，否则报错。

#### pause / resume / load —— 空请求体

```json
{}
```

### 响应结构

#### create / update / pause / resume —— 双层 Result 包装

```json
{
  "success": true,
  "data": "success"
}
```

失败时：

```json
{
  "success": true,
  "data": {
    "success": false,
    "errorMsg": "具体错误信息",
    "code": "BIZ_ERROR"
  }
}
```

#### load —— 单层 Result + DTO

```json
{
  "success": true,
  "data": {
    "sellerUserId": "xxx",
    "status": "active",
    "allowBuyerLevelList": ["v1", "v2"]
  }
}
```

`status` 枚举值：

| status | 含义 |
|--------|------|
| `not_hired` | 未招聘（未安装牛仔） |
| `active` | 正常运行 |
| `paused` | 已暂停 |

未招聘场景下，`data` 可能为 `null` 或 `{}`，service 层兜底为 `status=not_hired`。

> ⚠️ service 层对 load 做启发式响应结构识别（兼容潜在的双层包装）：若 `data` 内层含 `success`/`errorMsg`/`errorCode` 但不含 `status`/`sellerUserId`，则按双层 Result 解包；否则视为 DTO 本体。

## CLI 调用

```bash
python3 cli.py cowboy_config create --levels L0,L1,L2   # 创建牛仔（必传）
python3 cli.py cowboy_config update --levels L0,L1      # 更新买家等级（必传）
python3 cli.py cowboy_config pause                       # 暂停接待
python3 cli.py cowboy_config resume                      # 恢复接待
python3 cli.py cowboy_config load                        # 加载配置（读取状态）
```

- `--levels` 取值范围 `L0` ~ `L6`，逗号分隔；service 层会 `upper()` + 去重 + 拒绝非法值。
- create / update **必传** `--levels`，未传时 CLI 直接返回 `success: false` 提示，不会发请求。
- argparse 已关闭前缀缩写匹配（`allow_abbrev=False`）：写 `--level`（少 s）会被拒绝为 `unrecognized arguments`，避免静默参数误匹配。

## 输出格式

### 成功

```json
{
  "success": true,
  "markdown": "✅ 创建牛仔成功",
  "data": { "success": true }
}
```

### 失败

```json
{
  "success": false,
  "markdown": "创建牛仔失败：具体错误信息\n\n**建议**: ...",
  "data": {}
}
```

### load 成功

```json
{
  "success": true,
  "markdown": "**牛仔配置**\n\n- 状态：正常运行\n- 接待买家等级：v1, v2",
  "data": {
    "status": "active",
    "allow_buyer_level_list": ["v1", "v2"]
  }
}
```

> load 输出**不透出 `sellerUserId`**（避免身份信息外泄，由网关上下文承载即可）。

## 注意事项

1. `sellerUserId` 由网关上下文自动注入，CLI 层和 service 层均不传递此参数；load 输出也不回传该字段
2. 五个接口共享相同的鉴权机制（HMAC-SHA256 签名，走 `_auth.py`）
3. 写操作（create/update/pause/resume）为双层 Result 包装；读操作（load）为单层 Result + DTO，service 层做启发式识别兼容
4. 本命令为底层 API 调用，`hire-reception` 5 步剧情对话流在 Agent 编排层实现，与本命令职责分离
5. `load` 是路由判断的底层依赖：主 Agent 在每轮商家会话开始前调用 `load` 拿到 `agent_status`，据此决定走 `hire-reception` 剧情流（`not_hired`）还是正常路由（`active`/`paused`）
6. **招聘场景**：hire-reception Step 4 商家提交接待范围卡后（Q3「哪些买家不让我接」反推 L 等级），主 Agent **仅将推导出的 L 等级写入会话上下文暂存**（建议 key：`hire.reception_levels`），**不调本接口**、不激活接待助手，直接推进至 Step 5 模拟对话；Step 5 商家点「确认模拟效果」后，主 Agent **此时才立即调** `cowboy_config create --levels {Step 4 暂存值}`，一步完成子账号创建 + 买家等级写入，接口成功后接待助手 status 写为 `active`、正式上岗；**后续**调为 `update --levels` 在管理页面同步买家等级，不在主对话框发起
