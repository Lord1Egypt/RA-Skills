---
name: current-akshare-list
description: 通过akshare下载所有A股、创业板、B股股票简况并用实时行情列表校对，获得当前正在交易的所有AB和创业板股票清单，以及不在交易的股票清单（代码、简称、上市时间），保存为csv。触发词："A股股票列表"、"更新股票列表"、"股票列表下载"、"akshare股票"、"获取全部A股"、"沪深京A股"、"不在交易股票"、"停牌股票"。若遇东方财富接口封禁，提示用户开VPN再试或自动建立定时任务重试直到接通。
---

# current-akshare-list

获取A股全量股票基础信息列表，并用实时行情接口交叉验证，输出「在交易」和「不在交易」两份清单。

## 环境要求

- Python 3.11+
- akshare SDK：`pip install akshare`
- 若接口封禁，需开启VPN或建立定时任务等待

## 工作流程

### 第一步：下载股票基础信息（可选，若已有可跳过）

从六个市场来源获取股票列表，合并去重：

```python
import akshare as ak
import pandas as pd

sources = [
    ("沪A", lambda: ak.stock_info_sh_name_code(symbol="主板A股")),
    ("沪B", lambda: ak.stock_info_sh_name_code(symbol="主板B股")),
    ("沪创", lambda: ak.stock_zh_index_cons_ci(symbol="000688")),
    ("深A", lambda: ak.stock_info_sz_name_code(symbol="A股列表")),
    ("深B", lambda: ak.stock_info_sz_name_code(symbol="B股列表")),
    ("京A", lambda: ak.stock_info_bj_a_code_name()),
]

results = []
for name, fn in sources:
    try:
        df = fn()
        df["source"] = name
        results.append(df)
    except Exception as e:
        print(f"{name} 获取失败: {e}")

stocklist = pd.concat(results).drop_duplicates(subset=["code"])
stocklist.columns = ["Symbol", "ShortName", "ListedDate", "Source"]
stocklist.to_csv("stocklist.csv", index=False)
```

### 第二步：实时行情接口验证（核心）

依次尝试三个接口，遇到封堵则处理：

```python
import akshare as ak
import json

def fetch_spot_data():
    """获取三接口实时行情数据"""
    data = {}
    
    # 1. A股实时行情
    try:
        df = ak.stock_zh_a_spot_em()
        codes = df[['代码','名称']].to_dict('records')
        with open('/tmp/akshare_a_codes.json', 'w') as f:
            json.dump(codes, f, ensure_ascii=False)
        data['a'] = len(codes)
        print(f"✅ A股成功: {len(codes)} 条")
    except Exception as e:
        print(f"❌ A股失败: {type(e).__name__}: {e}")
        raise ConnectionError(f"A股接口封禁: {e}")
    
    # 2. B股实时行情
    try:
        df = ak.stock_zh_b_spot_em()
        codes = df[['代码','名称']].to_dict('records')
        with open('/tmp/akshare_b_codes.json', 'w') as f:
            json.dump(codes, f, ensure_ascii=False)
        data['b'] = len(codes)
        print(f"✅ B股成功: {len(codes)} 条")
    except Exception as e:
        print(f"❌ B股失败: {e}")
    
    # 3. 科创板实时行情
    try:
        df = ak.stock_zh_kcb_spot()
        codes = df[['代码','名称']].to_dict('records')
        with open('/tmp/akshare_kcb_codes.json', 'w') as f:
            json.dump(codes, f, ensure_ascii=False)
        data['kcb'] = len(codes)
        print(f"✅ 科创板成功: {len(codes)} 条")
    except Exception as e:
        print(f"❌ 科创板失败: {e}")
    
    return data

# 执行获取
try:
    data = fetch_spot_data()
    print(f"完成: {data}")
except ConnectionError as e:
    print(f"接口封禁，需要处理...")
    raise
```

### 第三步：对比分析

```python
import json, csv

# 读取三个接口数据
with open('/tmp/akshare_a_codes.json', 'r') as f:
    a_codes = set(item['代码'] for item in json.load(f))
with open('/tmp/akshare_b_codes.json', 'r') as f:
    b_codes = set(item['代码'] for item in json.load(f))
with open('/tmp/akshare_kcb_codes.json', 'r') as f:
    kcb_codes = set(item['代码'] for item in json.load(f))

# 读取 stocklist
stocklist_codes = set()
stocklist_info = {}
with open('stocklist.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        code = row['Symbol'].strip()
        stocklist_codes.add(code)
        stocklist_info[code] = {'name': row.get('ShortName', ''), 'date': row.get('ListedDate', '')}

# 三接口合并（去重）
all_spot_codes = a_codes | b_codes | kcb_codes

# 对比分析
in_spot_not_stocklist = all_spot_codes - stocklist_codes  # 需补充
in_stocklist_not_spot = stocklist_codes - all_spot_codes  # notspot

print(f"需补充: {len(in_spot_not_stocklist)}")
print(f"notspot: {len(in_stocklist_not_spot)}")
```

### 第四步：接口封禁处理

当东财接口被封（ConnectionError、RemoteDisconnected）时：

**方案A：用户手动处理**
```
告知用户："东方财富接口被封，请开启VPN后重新执行，或选择建立定时任务自动重试"
```

**方案B：自动建立定时任务**
```
1. 创建 cron 任务，每30分钟重试东财接口
2. 若成功：执行全量对比 → 输出结果 → 删除自身任务
3. 若失败：输出"仍被封，等待下次尝试" → 保留任务继续重试
4. 最大重试次数：24次（12小时），超时后通知用户
```

```python
# 定时任务 payload 示例
{
    "kind": "agentTurn",
    "message": "重试东财接口，若成功则完成全量对比并输出结果到指定路径",
    "sessionTarget": "isolated"
}
```

### 第五步：输出结果文件

| 文件 | 说明 | 字段 |
|------|------|------|
| `stocklist.csv` | 全量股票基础信息 | 代码、简称、上市日期、来源 |
| `stocklist_intrading.csv` | 当前在交易股票 | 代码、简称、上市日期 |
| `notspot.csv` | 不在交易股票清单 | 代码、简称、上市日期 |

## VPN 环境说明

东方财富接口（`stock_zh_a_spot_em`）在大陆IP下经常被封：
- **开启VPN后**：通常可稳定获取数据
- **无VPN**：接口返回 ConnectionError 或 RemoteDisconnected

若遇封禁，建议：
1. 开启VPN后重试
2. 建立定时任务自动重试（适合夜间执行）

## 已知限制

- B股不在部分实时行情覆盖范围内，预期出现在 notspot 中
- 科创板全量通过指数成分股接口获取（非直接全量列表）