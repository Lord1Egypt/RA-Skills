# C22 - 通达信

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C22 |
| 连接器名 | tdx-connector |
| 显示名 | 通达信 |
| 层级 | L3 纯 API 查询型 |
| 可替代 | ✅ 完全可替代（Skill） |
| 分类 | 金融数据 |
| 替代难度 | 简单（已有 skill） |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 实时行情 | 股票/期货/外汇实时报价 |
| K线数据 | 日K/周K/月K/分钟K |
| 财务数据 | 财务报表/财务指标 |
| 指数数据 | 上证/深证/创业板指数 |
| 历史数据 | 历史行情回测 |

## 已有 Skill 替代

**financial-report-minesweeper**（财报排雷）已覆盖：
- 下载财务报表
- 计算 50 项核心指标
- 生成排雷报告（MD+HTML）

## 扩展 Skill 方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L3-api-finance-C22-tdx-realtime-quote.py  # 实时行情
└── L3-api-finance-C22-tdx-kline-data.py      # K线数据
```

### 鉴权方式

**无需鉴权**：
- 通达信行情服务器公开可访问
- 直接 TCP 连接请求数据

### 核心脚本示例

**L3-api-finance-C22-tdx-realtime-quote.py**：
```python
#!/usr/bin/env python3
"""获取实时行情"""

import struct
import socket
import argparse
from pathlib import Path

# 通达信行情服务器
SERVERS = [
    ("119.147.212.81", 7709),
    ("112.74.214.43", 7727),
    ("221.231.141.60", 7709),
]

def connect_server(host: str, port: int) -> socket.socket:
    """连接行情服务器"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((host, port))
    return sock

def get_realtime_quote(code: str) -> dict:
    """获取实时行情"""
    # 解析股票代码
    if code.startswith("6"):
        market = 1  # 上海
    else:
        market = 0  # 深圳
    
    # 构建请求包
    # ... 协议实现 ...
    
    return {
        "code": code,
        "name": "示例股票",
        "price": 10.50,
        "change": 0.25,
        "change_percent": 2.44,
        "volume": 1234567,
        "amount": 12962953.50,
        "open": 10.25,
        "high": 10.60,
        "low": 10.20,
        "close": 10.50,
        "pre_close": 10.25,
    }

def format_output(data: dict) -> str:
    """格式化输出"""
    return f"""
## {data['name']} ({data['code']})

| 指标 | 值 |
|------|-----|
| 最新价 | ¥{data['price']:.2f} |
| 涨跌额 | {data['change']:+.2f} |
| 涨跌幅 | {data['change_percent']:+.2f}% |
| 成交量 | {data['volume']:,} |
| 成交额 | ¥{data['amount']:,.2f} |
| 今开 | ¥{data['open']:.2f} |
| 最高 | ¥{data['high']:.2f} |
| 最低 | ¥{data['low']:.2f} |
| 昨收 | ¥{data['pre_close']:.2f} |
"""

def main():
    parser = argparse.ArgumentParser(description="获取实时行情")
    parser.add_argument("code", help="股票代码（如 600000）")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = get_realtime_quote(args.code)
        
        if args.json:
            import json
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"获取失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 迁移成本

| 项目 | 说明 |
|------|------|
| 服务器 | 改服务器地址即可 |
| 协议 | 通达信协议通用 |
| 数据格式 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 无需 | 无需 |
| 数据源 | 绑定通达信 | 可切换多源 |
| 数据处理 | 原样返回 | 可计算指标 |
| 输出格式 | 固定 | 模板化可定制 |
| 离线能力 | 无 | 可缓存数据 |
