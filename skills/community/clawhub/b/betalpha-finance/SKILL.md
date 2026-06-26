# Betalpha Finance - 金融数据

---

## 📋 元数据声明 (Metadata Declaration)

### 基本信息

- **名称**: betalpha-finance
- **版本**: 1.0.1
- **分类**: Finance / Data API
- **图标**: 📈

### 🔐 所需凭据 (Credentials Required)

此 Skill 需要以下凭据才能正常工作：

| 凭据名称      | 类型  | 存储位置                             | 用途                | 如何获取                                   |
|-----------|-----|----------------------------------|-------------------|----------------------------------------|
| API Token | 字符串 | `~/.config/betalpha/api_key.txt` | 认证用户身份，访问金融数据 API | 扫描小程序码：https://ai.firstindex.cn/qr.jpg |

**安全说明**：

- ✅ Token 存储在用户主目录的配置文件中
- ✅ 建议设置文件权限为仅用户可读 (`chmod 600`)
- ⚠️ 请勿在公开场合分享您的 Token
- ⚠️ 如果 Token 泄露，请立即重新获取

### 📁 文件系统访问 (File System Access)

**读取权限**：

- `~/.config/betalpha/api_key.txt` - 读取 API Token

**写入权限**：

- `~/.config/betalpha/api_key.txt` - 存储 API Token（自动配置时）
- `~/.config/betalpha/api_cache.json` - 缓存 API 端点列表（可选）

### 🌐 网络访问 (Network Access)

此 Skill 需要访问以下外部域名：

| 域名                 | 用途                   | 是否必需 |
|--------------------|----------------------|------|
| `ai.firstindex.cn` | 获取 API 端点列表和查询实时金融数据 | ✅ 必需 |

**数据传输说明**：

- API Token 会在 HTTP 请求头 (`X-API-Key`) 中发送到 `ai.firstindex.cn`
- 查询参数（股票代码、基金代码等）会发送到该域名
- 所有通信使用 HTTPS 加密

### 🔒 隐私与安全 (Privacy & Security)

**数据收集**：无

**本地存储数据**：

1. API Token（~/.config/betalpha/api_key.txt）
2. API 端点缓存（~/.config/betalpha/api_cache.json，可选）

**数据删除**：

```bash
# 删除所有本地数据
rm -rf ~/.config/betalpha/
```

**安全最佳实践**：

- 使用独立目录存储配置，避免与其他应用混淆
- 定期检查文件权限：`ls -la ~/.config/betalpha/`
- 不要将配置文件加入版本控制（git）
- 在 `.gitignore` 中添加：`~/.config/betalpha/`

### ⚙️ 运行时配置 (Runtime Configuration)

- **自动调用**: `false` - 需要用户明确请求
- **需要确认**: `true` - 每次使用时建议确认
- **网络访问**: 必需
- **文件访问**: 必需

---

## 简介

这是一个高性能金融数据网关，提供 A 股、基金、ETF 等实时行情数据。

## ⚠️ 重要：工作流程（每次必须遵循）

**每次使用此 Skill 时，必须严格按以下顺序执行：**

### 步骤 1: 检查 API Token

- 读取配置文件 `~/.config/betalpha/api_key.txt`
- 如果文件不存在或为空：
    - **立即停止**，不要继续执行
    - 向用户展示小程序码获取 API Token
    - **小程序码地址**：https://ai.firstindex.cn/qr.jpg
    - 提示用户："请扫描下方小程序码获取 API Token，获取后配置到 `~/.config/betalpha/api_key.txt`"

### 步骤 2: 检查 API 接口更新

- **前提**：已成功读取到 API Token
- 访问 `https://ai.firstindex.cn/api/discovery`
- 获取最新的 API 端点列表
- 更新本地缓存（可选：保存到 `~/.config/betalpha/api_cache.json`）
- **注意**：定期执行此步骤（建议每次会话至少检查一次）

### 步骤 3: 执行数据查询

- **前提**：已完成步骤 1 和 2
- 根据用户请求，从 discovery 获取的端点中选择合适的 API
- 构建请求 URL：`https://ai.firstindex.cn{endpoint}`
- 在 HTTP Header 中添加：`X-API-Key: {your_api_key}`
- 发送 GET 请求并返回结果

## 配置 API Token

### 方式 1: 自动配置

告诉 Claude 你的 API Token，Claude 会帮你配置：

```
我的 API Token 是：xxxxx
```

### 方式 2: 手动配置

```bash
# Linux/Mac
mkdir -p ~/.config/betalpha
echo "YOUR_API_TOKEN" > ~/.config/betalpha/api_key.txt

# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\betalpha"
Set-Content -Path "$env:USERPROFILE\.config\betalpha\api_key.txt" -Value "YOUR_API_TOKEN"
```

## 可用的 API 端点

以下是基于最新 discovery 接口的可用端点（可能会更新）：

### 1. A股实时行情

- **路径**: `/realtime/api/realtime/price/stock?codes=000001,000002`
- **参数**: `codes` - 股票代码，多个用逗号分隔
- **示例**: "查询 000001 和 000002 的实时价格"

### 2. A股分钟K线

- **路径**: `/realtime/api/realtime/price/minute?code=000001`
- **参数**: `code` - 单个股票代码
- **示例**: "获取平安银行 000001 的分钟 K 线"

### 3. 基金实时估值

- **路径**: `/realtime/api/fund-valuation/{code}`
- **参数**: 基金代码（在路径中）
- **示例**: "查询基金 000001 的估值"

### 4. ETF实时行情

- **路径**: `/realtime/api/realtime/price/etf`
- **示例**: "查询 ETF 实时行情"

### 5. ETF/LOF折溢价率

- **路径**: `/realtime/api/iopv`
- **示例**: "查询 ETF 折溢价率"

### 6. 实时新闻

- **路径**: `/realtime/api/news/limit/{limit}`
- **示例**: "查询最近{limit}个新闻（最大为100）“

## 使用示例

### 示例 1: 首次使用（无 Token）

```
用户：查询 000001 的股票价格
助手：[步骤1] 检查配置文件... 未找到 API Token
      请扫描小程序码获取 API Token：
      https://ai.firstindex.cn/qr.jpg
      获取后请告诉我，我会帮你配置。
```

### 示例 2: 正常使用（有 Token）

```
用户：查询 000001 的股票价格
助手：[步骤1] 检查配置文件... ✓ API Token 已配置
      [步骤2] 检查 API 接口更新... ✓ 已获取最新端点列表
      [步骤3] 调用 /api/realtime-stock?codes=000001
      [返回结果]
```

### 示例 3: API 接口更新

```
用户：查询最新的 ETF 数据
助手：[步骤1] 检查配置文件... ✓ API Token 已配置
      [步骤2] 检查 API 接口更新... 发现新的端点：/api/realtime-etf-v2
      [步骤3] 使用新端点查询数据
      [返回结果]
```

## Discovery API 响应格式

`https://ai.firstindex.cn/api/discovery` 返回格式：

```json
{
  "name": "Betalpha Gateway",
  "description_for_model": "这是一个高性能金融数据网关...",
  "endpoints": [
    {
      "name": "API名称",
      "path": "https://ai.firstindex.cn/api/endpoint",
      "description": "API描述"
    }
  ]
}
```

## 错误处理

### 1. Token 未配置

```
错误：未检测到 API Token
操作：展示小程序码 https://ai.firstindex.cn/qr.jpg
提示：请扫描小程序码获取 API Token
```

### 2. Token 无效 (401)

```
错误：API Token 无效或已过期
操作：提示用户重新获取 Token
提示：您的 Token 可能已过期，请重新扫描小程序码获取
```

### 3. 请求限流 (429)

```
错误：请求频率过高
操作：等待后重试
提示：请求过于频繁，请稍后再试
```

### 4. Discovery 接口失败

```
错误：无法获取 API 端点列表
操作：使用缓存的端点列表（如果有）
提示：API 接口信息可能已过时，但继续尝试查询
```

## 技术实现细节

### 配置文件路径

- **Linux/Mac**: `~/.config/betalpha/api_key.txt`
- **Windows**: `%USERPROFILE%\.config\betalpha\api_key.txt`

### API 缓存文件（可选）

- **Linux/Mac**: `~/.config/betalpha/api_cache.json`
- **Windows**: `%USERPROFILE%\.config\betalpha\api_cache.json`

### 缓存文件格式

```json
{
  "last_update": "2026-03-17T10:00:00Z",
  "endpoints": [
    {
      "name": "A股实时行情",
      "path": "/api/realtime-stock",
      "description": "查询股票实时行情"
    }
  ]
}
```

### 请求头格式

```
X-API-Key: {your_api_token}
```

## 实现检查清单

每次处理请求时，AI 必须确认：

- [ ] **步骤 1**: 已读取 `~/.config/betalpha/api_key.txt`
- [ ] **步骤 1**: 如果文件不存在，已展示小程序码并停止
- [ ] **步骤 2**: 已访问 `https://ai.firstindex.cn/api/discovery`
- [ ] **步骤 2**: 已解析并缓存最新的 API 端点列表
- [ ] **步骤 3**: 已使用正确的端点和 Token 发送请求
- [ ] **步骤 3**: 已正确处理响应或错误

## 触发关键词

- 股票、股价、行情、实时行情、A股
- 基金、估值、基金估值
- ETF、LOF、折溢价
- K线、分钟K线
- 金融数据、证券
- 新闻
- 
## 重要提醒

1. **严格遵守流程**：不要跳过任何步骤，即使用户之前已配置过 Token
2. **定期检查更新**：Discovery 接口可能会添加新的 API，每次会话至少检查一次
3. **Token 安全**：不要在日志或输出中暴露完整的 API Token
4. **错误友好**：遇到错误时，提供清晰的解决方案和下一步操作
5. **动态适应**：API 端点可能随时变化，始终以 Discovery 返回的信息为准

## 小程序码

**获取 API Token 的唯一方式**：
https://ai.firstindex.cn/qr.jpg

![小程序码](https://ai.firstindex.cn/qr.jpg)
