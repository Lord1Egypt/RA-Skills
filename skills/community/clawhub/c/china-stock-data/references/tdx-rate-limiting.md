# TDX 通达信限速策略与反封指南

## 背景

通达信（TDX）使用 pytdx 库通过私有 TCP 协议直连通达信行情服务器。
该协议无需 API Key，但过快或过多请求可能导致 IP 被封。

## 限速架构（两层独立保护）

### 第一层：china_stock.py（核心模块限速）

所有 `china_stock.tdx_connect()` 调用自动触发限速：

```python
# 全局时间戳
_LAST_TDX_TIME = 0

def tdx_throttle():
    """每次调用至少间隔0.5秒 + 随机抖动0~0.2秒"""
    global _LAST_TDX_TIME
    elapsed = time.time() - _LAST_TDX_TIME
    if elapsed < 0.5:
        time.sleep(round(0.5 - elapsed + random.random() * 0.2, 3))
    _LAST_TDX_TIME = time.time()
```

### 第二层：news_aggregator.py（日报模块限速）

独立限速器（与 china_stock 不共享全局状态，但日报场景只走这一个入口）：

```python
_TDX_LAST_CALL = 0

def _tdx_rate_limit():
    global _TDX_LAST_CALL
    elapsed = time.time() - _TDX_LAST_CALL
    if elapsed < 0.5:
        time.sleep(0.5 - elapsed)
    _TDX_LAST_CALL = time.time()
```

## 服务器轮询策略

4台服务器轮流使用，每次连接从不同的起点开始尝试：

| # | 名称 | IP | 端口 |
|---|------|:--:|:----:|
| 1 | 上证云成都电信一 | 218.6.170.47 | 7709 |
| 2 | 上证云北京联通一 | 123.125.108.14 | 7709 |
| 3 | 上海电信主站Z1 | 180.153.18.170 | 7709 |
| 4 | 杭州电信主站J1 | 60.191.117.167 | 7709 |

轮询实现：全局 `_TDX_HOST_IDX` 自增后取模，每个连接尝试最多遍历全部4台服务器。

## 批量查询优化（关键）

### ❌ 旧方案（每次查询独立连接）

```python
for name, mkt, code in indices_config:
    d = get_index_close(code, mkt)   # 每次独立 connect→query→disconnect
    time.sleep(0.2)
# → 6次连接，对同一台服务器
```

### ✅ 新方案（一次连接批量查询）

```python
def _get_index_closes_batch(indices):
    """一次 get_security_queries() 传所有codes"""
    api.get_security_queries([(mkt, code) for _, mkt, code in indices])
    # → 1次连接，查6个指数
```

pytdx 的 `get_security_quotes()` 原生支持批量——传入 `[(market, code), ...]` 列表即可。

## 速率对比

| 场景 | 改造前 | 改造后 |
|:----|:------|:------|
| 每日早报（6指数） | 6次连接 × 0.2s间隔 = ~1.2秒 | 1次连接 × 0.5s限速 = ~0.5秒 |
| 自选异动扫描（8股） | 8次连接 × 0.3s间隔 = ~2.4秒 | 8次连接 × 0.5s限速 + 0.3s = ~6.4秒 |

注意：自选异动扫描虽然变慢了，但这是为了安全——宁可慢不要被封。

## 被封后的恢复

如果 IP 已被通达信临时封禁：
1. 停止所有 TDX 请求至少 5-10 分钟
2. 切换使用腾讯财经作为替代数据源（`tencent_quote()`）
3. 恢复后检查限速策略是否严格执行

## 与其他数据源的关系

| 数据源 | 是否受限 | 容量 |
|:------|:--------:|:----:|
| 通达信(TDX) | 需限速，否则封IP | ~1次/0.5秒 |
| 腾讯财经 | 公开API，无限制 | ~10次/秒 |
| 同花顺iFinD | 每周1万条API配额 | 用完需等下周 |
| 东方财富(EastMoney) | IP已被封禁 | — |
