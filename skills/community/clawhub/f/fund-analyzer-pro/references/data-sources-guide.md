# 数据源配置指南

**用途**：配置基金数据 API，确保数据准确性

**版本**：v1.0  
**更新时间**：2026-04-16

---

## 数据源总览

| 数据源 | 类型 | 准确性 | 成本 | 推荐度 |
|--------|------|--------|------|--------|
| **天天基金 API** | 付费 API | ✅ 99%+ | 50 次/天免费 | ⭐⭐⭐⭐⭐ |
| **且慢 MCP** | 付费 API | ✅ 99%+ | 需 API Key | ⭐⭐⭐⭐⭐ |
| **东方财富** | 免费 API | ✅ 95%+ | 免费 | ⭐⭐⭐⭐ |
| **新浪财经** | 免费 API | ✅ 90%+ | 免费 | ⭐⭐⭐ |
| **基金 e 账户** | Excel 导入 | ✅ 100% | 免费 | ⭐⭐⭐⭐ |

---

## 方式 1：天天基金 API（推荐）

### 获取 API Key

**步骤**：
1. 访问 https://skills.tiantianfunds.com/
2. 注册账号
3. 登录获取 API Key
4. 复制到配置文件

**配置**：
```bash
# Linux/Mac
export TTFUND_APIKEY="ttf_sk_live_xxx"

# Windows
set TTFUND_APIKEY=ttf_sk_live_xxx

# 永久配置（推荐）
echo 'export TTFUND_APIKEY="ttf_sk_live_xxx"' >> ~/.bashrc
source ~/.bashrc
```

**验证**：
```bash
echo $TTFUND_APIKEY
# 应显示 API Key（部分隐藏）
```

### 使用限制

| 项目 | 限制 |
|------|------|
| 免费额度 | 50 次/天 |
| 超出后 | 需付费或等待次日 |
| 并发限制 | 10 次/秒 |

### 可获取数据

| 数据类型 | 是否可用 | 说明 |
|----------|----------|------|
| 基金基础信息 | ✅ | 代码、名称、类型、规模 |
| 净值数据 | ✅ | 单位净值、累计净值 |
| 收益率 | ✅ | 近 1 月/1 年/3 年等 |
| 持仓数据 | ✅ | 前十大重仓股 |
| 基金经理 | ✅ | 姓名、从业年限 |
| 费率数据 | ✅ | 管理费、托管费、申购费 |
| 夏普比率 | ✅ | 需要 API Key |
| 最大回撤 | ✅ | 需要 API Key |
| 波动率 | ✅ | 需要 API Key |

---

## 方式 2：且慢 MCP

### 获取 API Key

**步骤**：
1. 访问且慢开放平台
2. 注册开发者账号
3. 创建应用获取 API Key
4. 复制到配置文件

**配置**：
```json
{
  "url": "https://stargate.yingmi.com/mcp/v2",
  "headers": {
    "x-api-key": "your_api_key"
  }
}
```

**保存位置**：`~/.openclaw/workspace/TOOLS.md`

### 可获取数据

| 数据类型 | 是否可用 | 说明 |
|----------|----------|------|
| 投顾策略搜索 | ✅ | 全市场 500+ 策略 |
| 策略详情 | ✅ | 业绩、风险、管理人 |
| 持仓明细 | ✅ | 基金持仓穿透 |
| 收益归因 | ✅ | Campisi/Brinson 归因 |
| 风险信息 | ✅ | 最大回撤、波动率 |

---

## 方式 3：免费 API（备用）

### 东方财富 API

**接口**：
```
https://fund.eastmoney.com/{fund_code}.html
```

**示例**：
```bash
curl https://fund.eastmoney.com/000001.html
```

**可获取数据**：
- ✅ 净值数据
- ✅ 收益率
- ✅ 持仓数据
- ✅ 基金经理
- ❌ 夏普比率
- ❌ 最大回撤

### 新浪财经 API

**接口**：
```
http://hq.sinajs.cn/list=fu_{fund_code}
```

**示例**：
```bash
curl http://hq.sinajs.cn/list=fu_000001
```

**可获取数据**：
- ✅ 实时净值
- ✅ 日涨跌
- ❌ 历史数据
- ❌ 持仓数据

---

## 方式 4：Excel 导入

### 基金 e 账户导出

**步骤**：
1. 访问 https://www.chinaclear.cn/
2. 登录基金 e 账户
3. 下载持仓明细（Excel）
4. 上传到系统

**字段要求**：
| 字段 | 必填 | 说明 |
|------|------|------|
| 基金代码 | ✅ | 6 位数字 |
| 基金名称 | ❌ | 可选 |
| 持仓金额 | ✅ | 元 |
| 成本价 | ✅ | 元 |
| 当前净值 | ❌ | 自动获取 |

### 天天基金导出

**步骤**：
1. 登录天天基金 APP
2. 进入"我的持仓"
3. 导出持仓（截图/Excel）
4. 上传到系统

---

## 数据验证

### 验证脚本

```bash
# 测试天天基金 API
cd ~/.openclaw/workspace/skills/fund-analyzer-pro
python3 scripts/ttfund-query.py

# 测试且慢 MCP
python3 scripts/qieman-mcp-query.py
```

### 验证清单

**每次配置后检查**：

- [ ] API Key 已保存
- [ ] 环境变量已配置
- [ ] 测试脚本运行成功
- [ ] 数据获取正常
- [ ] 无错误提示

---

## 故障排查

### 问题 1：API Key 未配置

**错误信息**：
```
❌ 获取失败：未配置 TTFUND_APIKEY 环境变量
```

**解决方案**：
```bash
export TTFUND_APIKEY="your_api_key"
# 或添加到 ~/.bashrc
```

### 问题 2：API Key 无效

**错误信息**：
```
❌ 获取失败：API Key 无效
```

**解决方案**：
1. 检查 API Key 是否正确（复制完整）
2. 重新获取 API Key
3. 联系 API 提供方

### 问题 3：API 限流

**错误信息**：
```
❌ 获取失败：请求过于频繁
```

**解决方案**：
1. 等待 1 分钟后重试
2. 降低请求频率
3. 升级到付费版本

### 问题 4：基金代码不存在

**错误信息**：
```
❌ 获取失败：基金代码不存在
```

**解决方案**：
1. 检查基金代码（6 位数字）
2. 在天天基金网查询确认
3. 基金可能已清盘

---

## 数据准确性保障

### 数据源优先级

```
1. 天天基金 API（有 API Key）→ 最完整
2. 且慢 MCP（有 API Key）→ 投顾策略专用
3. 东方财富免费 API → 基础数据
4. 新浪财经免费 API → 实时净值
5. 用户手动输入 → 补充数据
```

### 数据验证规则

| 数据类型 | 验证规则 |
|----------|----------|
| 基金代码 | 6 位数字正则校验 |
| 净值 | > 0 且 < 100 |
| 收益率 | -100% 到 +1000% |
| 持仓占比 | 0% 到 100% |
| 费率 | 0% 到 10% |

### 数据过期处理

**规则**：
- 净值数据：T+1 更新（次日）
- 持仓数据：季度更新
- 基金经理：变更时更新

**过期提示**：
```
⚠️ 数据可能已过期（最后更新：YYYY-MM-DD）

**建议**：
- 刷新数据：重新调用 API
- 或访问天天基金网获取最新数据
```

---

## 最佳实践

### 1. 配置备份

**保存 API Key 到多个位置**：
```bash
# 环境变量
export TTFUND_APIKEY="xxx"

# 配置文件
~/.openclaw/workspace/TOOLS.md

# 密码管理器
1Password / Bitwarden
```

### 2. 缓存机制

**避免重复调用 API**：
```python
# 缓存 TTL：1 小时
cache_key = get_cache_key(fund_code)
data = get_from_cache(cache_key, ttl=3600)
if not data:
    data = fetch_from_api(fund_code)
    save_to_cache(cache_key, data)
```

### 3. 降级策略

```
天天基金 API → 且慢 MCP → 免费 API → 手动输入
```

**实现**：
```python
try:
    data = ttfund_api.query(fund_code)
except:
    try:
        data = qieman_mcp.query(fund_code)
    except:
        data = free_api.query(fund_code)
```

### 4. 数据校验

**每次获取后校验**：
```python
if not validate_fund_code(fund_code):
    return {"error": "基金代码格式错误"}

if data['nav'] <= 0:
    return {"error": "净值数据异常"}
```

---

## 相关文档

- `examples/test-cases.md` - 测试案例集
- `SKILL.md` - 主技能文档
- `templates/fund-report-template.md` - 报告模板

---

**维护者**：燃冰 & ant  
**最后更新**：2026-04-16  
**下次审查**：2026-05-16
