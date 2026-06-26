# 高德 POI 搜索（替代 WebSearch 查地点）

用高德 Web 服务 API 精准查找酒店、小区、商铺等 POI，一次拿到 **名称、地址、GCJ-02 坐标**，不再依赖 WebSearch 猜地点。

## API Key 配置

Key 存放在 Skill 同目录 `config/amap-api-key.md` 文件中（最后一行非注释行即为 Key）。

**首次使用时**：读取该文件，如果是 `YOUR_KEY_HERE` 或为空，告诉用户：

> 需要一个高德 Web 服务 API Key 才能精准查地点。申请很快：
> 1. 打开 https://console.amap.com/
> 2. 注册/登录 → 创建应用 → 添加 Key（服务平台选「Web 服务」）
> 3. 把 Key 粘贴到 `config/amap-api-key.md` 文件最后一行，保存即可。

用户配好后重新读取文件获取 Key。

**读取方式**：

```bash
AMAP_KEY=$(grep -v '^#' "$SKILL_DIR/config/amap-api-key.md" | grep -v '^$' | tail -1)
```

---

## 搜索流程

### 场景 1：查用户提到的地点（酒店、小区、地标）

用户说「我在北秀观云」「我在美豪五一广场店」时，**优先用 POI 搜索**，不要先 WebSearch。

```bash
curl -s "https://restapi.amap.com/v3/place/text?key=${AMAP_KEY}&keywords=北秀观云&city=杭州&citylimit=true&extensions=all&offset=5"
```

**关键参数**：

| 参数 | 值 | 说明 |
|------|----|------|
| `keywords` | 用户说的地点名 | 如 `北秀观云`、`美豪酒店五一广场` |
| `city` | 用户所在城市 | 如 `杭州`、`长沙`。从用户话里提取，或从 `standups.md` 推断 |
| `citylimit` | `true` | 只搜这个城市，避免跨城干扰 |
| `extensions` | `all` | 拿到完整地址、区域名等 |
| `offset` | `5` | 取前 5 条就够 |

### 场景 2：查推荐目的地的坐标（用于拼高德导航链接）

确定推荐地点后（如「太平老街」「杭钢遗址公园」），用同样的接口拿坐标：

```bash
curl -s "https://restapi.amap.com/v3/place/text?key=${AMAP_KEY}&keywords=杭钢遗址公园&city=杭州&citylimit=true&offset=3"
```

从返回的 `pois[0].location` 拿到 GCJ-02 坐标（格式 `经度,纬度`），直接用于拼 `amap-navigation-uri.md` 的导航链接。

---

## 返回结果解析

API 返回 JSON，核心结构：

```json
{
  "status": "1",
  "count": "2",
  "pois": [
    {
      "name": "联发北秀观云",
      "address": "金昌路与北秀街交叉口",
      "location": "120.123456,30.345678",
      "cityname": "杭州市",
      "adname": "拱墅区",
      "type": "商务住宅;住宅区;住宅小区"
    }
  ]
}
```

**提取要点**：

| 字段 | 用途 |
|------|------|
| `name` | POI 正式名称，可能和用户口语不完全一致（如用户说「北秀观云」，返回「联发北秀观云」） |
| `location` | **GCJ-02 坐标**，格式 `经度,纬度`，可直接用于高德导航链接 |
| `address` | 街道地址，用于输出中描述位置 |
| `adname` | 所在区，辅助判断位置 |

**多条结果处理**：

- 取 **第一条**（高德默认按相关度排序）。
- 如果第一条的 `adname`/`cityname` 与用户上下文不符，看第二三条。
- 如果 `count` 为 0（没搜到），**回退到 WebSearch**，不要报错。

---

## 与工作流的集成

### 替代 WebSearch 查地点的优先级

1. **有 Key → 优先用高德 POI 搜索**：查用户位置、查推荐目的地坐标。
2. **POI 搜索无结果 → 回退 WebSearch**：冷门地点高德可能没收录。
3. **无 Key → 全程用 WebSearch**：和之前一样，不阻断流程。

### 坐标直通导航链接

POI 搜索拿到的 `location` 是 **GCJ-02**，可以 **直接** 填入高德导航 URI 的 `from`/`to`，不需要再额外验证坐标系。在输出中声明：

```markdown
**坐标来源：** 高德 POI 搜索「联发北秀观云」返回 GCJ-02（120.1234, 30.3456）
```

### 起点 + 终点一次搞定

用户说出位置后，**一次请求查起点**（用户酒店/小区），推荐确定后 **一次请求查终点**（推荐地点）。两个坐标直接拼进导航链接，起点终点都精准。

---

## 回退策略

| 情况 | 处理 |
|------|------|
| Key 未配置（`YOUR_KEY_HERE`） | 提示用户配置，本次用 WebSearch 兜底 |
| API 返回 `status: 0`（Key 无效/过期/超限） | 提示用户检查 Key，本次用 WebSearch 兜底 |
| `count: 0`（没搜到） | 回退 WebSearch |
| 网络超时 | 回退 WebSearch |

**无论何种回退，都不阻断推荐流程。**

---

## 注意事项

- 高德 Web 服务 API **免费额度**：每日 5000 次（个人开发者），对微度假场景绰绰有余。
- `config/amap-api-key.md` 文件 **不要** 提交到 Git（如有 `.gitignore` 应加入）。
- 同一个 Key 可以同时用于 POI 搜索和其他高德 Web 服务（如逆地理编码），无需重复申请。
