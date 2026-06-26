# B站个性装扮标准操作流程 (SOP)

## 目录

1. [日常查询流程](#日常查询流程)
2. [Benefit扫描流程](#benefit扫描流程)
3. [绝版装扮数据恢复](#绝版装扮数据恢复)
4. [收藏集卡片查询](#收藏集卡片查询)
5. [品级判别流程](#品级判别流程)
6. [凭证更新](#凭证更新)

---

## 日常查询流程

### 搜索装扮

```bash
bash scripts/bilibili-garb-search.sh "关键词"
```

输出分为三类：
1. **`[官方]`** — B站搜索API返回的在售商品
2. **`[藏馆-绝版]`** — 本地数据库中的下架商品（官方API已查不到）

搜索结果中：
- 收藏集使用 `biz_id`（≤6位数字）
- 套装使用 `item_id`（>6位数字）

### 查看详情

```bash
bash scripts/bilibili-garb-collection.sh -i <ID>
```

脚本自动判断类型：
- ID ≤ 6位 → 收藏集模式
- ID > 6位 → 套装模式

查询策略（按优先级）：
1. 官方搜索API
2. `act/basic` API（即使下架也能获取基础信息）
3. 本地藏馆数据库回退

---

## Benefit扫描流程

### 前置准备

1. 确认 `data/decorations-database.json` 存在（用户装扮资产数据库）
2. 确认凭证有效（`configs/bili-api-creds.json` 或环境变量）

### 执行扫描

```bash
# 全量扫描
python3 scripts/garb-benefit-scan.py

# 限制数量（测试用）
python3 scripts/garb-benefit-scan.py --limit 5

# 预览模式（不实际请求）
python3 scripts/garb-benefit-scan.py --dry-run

# 强制重扫已有数据
python3 scripts/garb-benefit-scan.py --force

# 调试模式
python3 scripts/garb-benefit-scan.py --debug --limit 3
```

### 扫描逻辑

1. 读取 `decorations-database.json`
2. 过滤：只保留 `biz_type=1`（装扮套装）且 `owned>=1` 的记录
3. 去重：跳过已有 benefit 数据的记录（除非 `--force`）
4. DIY检测：`item_id` 含横杠或非纯数字 → `is_diy=1`
5. 调用 benefit API（DIY套装用 `biz_id` 作为 `item_id` 参数）
6. 完整提取 `properties` 所有非空字段
7. 追加写入 `data/garb-benefit-results.ndjson`

### 中断恢复

- `Ctrl+C` 安全退出，进度自动保存
- 重新运行自动从断点续传
- 进度文件：`data/garb-benefit-scan.progress.json`

### 结果解读

```json
{
  "biz_id": 59673,
  "item_id": 59672,
  "is_diy": false,
  "benefit_items": {
    "card": [{"item_id": 123, "name": "...", "image": "..."}],
    "space_bg": [{"item_id": 456, "image": "...", "image_vertical": "..."}],
    "emoji_package": [{"item_id": 789, "emoji_list": [...]}]
  }
}
```

---

## 绝版装扮数据恢复

绝版（已下架）装扮无法通过 `suit/detail` 获取数据。恢复流程：

1. **确认拥有**：从 `decorations-database.json` 确认 `owned=1`
2. **调用 benefit**：使用 `part=space_bg`，DIY套装传 `biz_id`
3. **提取子项**：从 `suit_items` 获取9种子项的 `item_id` + `properties`
4. **如需详情**：用子项 `item_id` 调 `suit/detail?item_id=X&part=对应类型`

---

## 收藏集卡片查询

### 步骤

1. 获取收藏集基础信息：
   ```
   GET /x/vas/dlc_act/act/basic?act_id=<ID>
   → 获取 lottery_id
   ```

2. 获取卡池配置和头像框：
   ```
   GET /x/vas/dlc_act/lottery_home_detail?act_id=<ID>&lottery_id=<LOTTERY_ID>
   → item_list: 卡片名称、稀缺度
   → collect_list.collect_infos: 收集奖励（含头像框）
   ```

3. 获取持有卡片编号（需Cookie认证）：
   ```
   GET /x/vas/user/dlc/card/list?vmid=<UID>&act_id=<ID>
   → card_list: card_no 编号
   ```

---

## 品级判别流程

### 判别优先级

1. **公开API `item_list` 的 `scarcity`** — 最可靠
   - `10` = 普通(N)
   - `20` = 稀有(R)
   - `30` = 小隐藏(SR)
   - `40` = 大隐藏(SSR)

2. **本地NDJSON数据库** — 次之

3. **保守兜底** — 当 `scarcity_rate=2` 且 `rate2_count==1` 时：
   - **默认小隐藏(30)**
   - **不自动升大隐藏(SSR)**
   - 需用户确认后方可调整

### ⚠️ 易错点

- DLC头像框 ≠ 常驻头像框：播报DLC时头像框必须从 `lottery_home_detail` 取
- 收藏集自带的 `frame`/`frame_image` 不是DLC头像框

---

## 凭证更新

### 何时更新

- `access_key` 过期（API返回错误码）
- Cookie失效（接口返回未登录）

### 更新方法

1. 使用抓包工具（mitmproxy/Charles）捕获B站移动端HTTPS流量
2. 找到任意API请求中的 `access_key` 参数
3. 找到Cookie中的 `SESSDATA`、`bili_jct`、`DedeUserID`
4. 更新 `configs/bili-api-creds.json`：

```json
{
  "appkey": "27eb53fc9058f8c3",
  "appsecret": "<from mobile client>",
  "access_key": "<new access_key>",
  "csrf": "<new bili_jct>",
  "DedeUserID": "<uid>",
  "SESSDATA": "<new SESSDATA>"
}
```

### 验证

```bash
# 测试benefit API是否可用
curl -s "https://api.bilibili.com/x/garb/v2/user/suit/benefit?item_id=59672&part=space_bg&is_diy=0&vmid=<UID>&access_key=<ACCESS_KEY>&appkey=27eb53fc9058f8c3&csrf=<CSRF>&mobi_app=iphone&platform=ios&ts=<TIMESTAMP>&sign=<SIGN>" \
  -H "Cookie: SESSDATA=<SESSDATA>; bili_jct=<CSRF>; DedeUserID=<UID>"
```
