# Beauty Image 使用示例

## 基础示例

### 智能模式 (自动识别)

```bash
# 名片生成
uv run scripts/generate_image_v3.py --prompt "帮我做一张赛博朋克风格的个人名片，名字叫圆规"

# 水晶质感
uv run scripts/generate_image_v3.py --prompt "画一只猫的水晶质感手办"

# 天气卡片
uv run scripts/generate_image_v3.py --prompt "上海天气卡片"

# 毛绒玩具
uv run scripts/generate_image_v3.py --prompt "做个毛绒版的苹果logo"
```

### 指定场景 + 风格

```bash
# 浮世绘闪卡
uv run scripts/generate_image_v3.py --prompt "日本武士" --scene art_ukiyoe_card --style 浮世绘

# 微缩场景
uv run scripts/generate_image_v3.py --prompt "咖啡店" --scene 3d_miniature

# 带字段的名片
uv run scripts/generate_image_v3.py --prompt "名片" --scene biz_card \
  --fields '{"name":"圆规","title":"CEO","company":"XyvaClaw"}'
```

### 指定引擎

```bash
# 强制使用 seedream5 (最高画质)
uv run scripts/generate_image_v3.py --prompt "一幅油画风格的日落" --engine seedream5

# 强制使用 wanx (文字渲染佳)
uv run scripts/generate_image_v3.py --prompt "金句卡片" --engine wanx
```

## 配置说明

### 必需配置

至少配置以下 API Key 之一:

1. `DASHSCOPE_API_KEY` — 通义万相引擎 (推荐, 免费额度多)
   - 获取: https://dashscope.console.aliyun.com/apiKey
2. `ARK_API_KEY` — Seedream 引擎 (画质更高)
   - 获取: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey

### 可选配置

1. `DEEPSEEK_API_KEY` — 用于 `--use-llm` 深度意图解析
   - 获取: https://platform.deepseek.com/api_keys

## 故障排除

### 常见问题

1. **"缺少 API Key" 错误**
   - 原因: 未配置任何 API Key
   - 解决: 设置 `DASHSCOPE_API_KEY` 环境变量，或在 `~/.openclaw/openclaw.json` 中配置

2. **"wan2.6 失败, 降级到 wan2.5" 警告**
   - 原因: wan2.6 模型暂时不可用或尺寸参数不合法
   - 解决: 正常现象，脚本会自动降级到 wan2.5。如持续失败，检查 API Key 是否有效

3. **"HTTP 401" 错误**
   - 原因: API Key 无效或已过期
   - 解决: 重新获取 API Key 并配置

4. **Seedream 不可用**
   - 原因: 未配置 `ARK_API_KEY`
   - 解决: 前往火山引擎控制台获取 API Key

### 健康检查

```bash
uv run scripts/check.py
```
