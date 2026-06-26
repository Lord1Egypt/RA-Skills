# 洞察任务管理集成指南（v3.0 - MD5鉴权）

本技能集成了明日DMP 人群洞察服务的两个核心接口，支持查询任务状态和获取分析结果。

**【版本信息】**
- v3.0（当前）：MD5签名 + 4位随机数 + dmp-dev.mingdata.com
- v2.0（已弃用）：SHA1签名 + 32位随机字符串 + open.mingdata.com

---

## 功能说明

### 1️⃣ 查询洞察任务状态

**用途：** 检查已提交的洞察任务是否完成

**接口：** POST `/audience/insight/list`

**输入：** 任务ID列表

**输出：** 任务信息（ID、名称、人群、状态、创建时间）

**状态码：**
- `0` - 失败 ❌
- `1` - 成功 ✅
- `2` - 等待中 ⏳
- `3` - 计算中 🔄

### 2️⃣ 获取洞察任务结果

**用途：** 拉取已完成任务的分析结果（特征、占比、TGI）

**接口：** GET `/audience/insight/result`

**输入：** 任务ID

**输出：** 多维度特征数据（层级树结构）
```json
{
  "code": "0",
  "msg": "success",
  "data": {
    "id": "basic",
    "name": "基础标签",
    "parentId": null,
    "type": 1,
    "coverageRate": null,
    "tgi": null,
    "children": [
      {
        "id": "职业属性",
        "name": "职业属性",
        "parentId": "basic",
        "type": 0,
        "coverageRate": 0.45,
        "tgi": 1.8,
        "children": [...]
      }
    ]
  }
}
```

---

## 正确的鉴权方式（v3.0）

### 核心算法

```python
import hashlib
import time
import random

def generate_auth_params(ak, sk):
    """生成认证参数"""
    ts = str(int(time.time()))              # 10位秒级时间戳
    rand_str = str(random.randint(1000, 9999))  # 4位数字
    
    # 签名 = MD5(ts + randStr + SK).upper()
    sign_str = f'{ts}{rand_str}{sk}'
    sign = hashlib.md5(sign_str.encode()).hexdigest().upper()
    
    return {
        'ts': ts,
        'randStr': rand_str,
        'accessKey': ak,
        'sign': sign
    }
```

### 关键参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `ts` | 10位秒级时间戳 | `1774580142` |
| `randStr` | 4位纯数字随机数 | `8165` |
| `accessKey` | 明日DMP的 Access Key | `wArzwWvT` |
| `sign` | MD5签名（大写） | `5A4E951BCCF371F48FDFA39BF2D53A25` |

### 签名生成规则

```
签名字符串 = ts + randStr + SK
MD5哈希 = md5(签名字符串)
签名 = MD5哈希.upper()
```

**示例**：
```
ts = "1774580142"
randStr = "8165"
SK = "zZYeW35ndoQVmUv5S2Kuq1PipMYC8mN0"

签名字符串 = "17745801428165zZYeW35ndoQVmUv5S2Kuq1PipMYC8mN0"
MD5 = "5a4e951bccf371f48fdfa39bf2d53a25"
sign = "5A4E951BCCF371F48FDFA39BF2D53A25"
```

---

## 集成方式

### 方式一：Python API 调用（推荐）

```python
from scripts.insight_api import InsightAPI
import warnings
warnings.filterwarnings('ignore')

# 初始化客户端（使用AK/SK）
api = InsightAPI(ak='wArzwWvT', sk='zZYeW35ndoQVmUv5S2Kuq1PipMYC8mN0')

# 查询任务状态
status = api.query_insight_status([100262, 100264])
print(status)

# 获取任务结果
result = api.get_insight_result(100262)
print(result)
```

### 方式二：环境变量配置

```bash
# 设置环境变量
export DMP_AK='wArzwWvT'
export DMP_SK='zZYeW35ndoQVmUv5S2Kuq1PipMYC8mN0'

# Python中自动读取
from scripts.insight_api import InsightAPI
api = InsightAPI()  # 自动从环境变量读取 AK/SK
result = api.get_insight_result(100262)
```

### 方式三：直接 HTTP 请求

```bash
# 获取洞察结果
curl -s "https://dmp-dev.mingdata.com/api/open-api/audience/insight/result?ts=1774580142&randStr=8165&accessKey=wArzwWvT&sign=5A4E951BCCF371F48FDFA39BF2D53A25&taskId=100262" \
  -k | jq .

# 或使用 Python requests
import requests
import warnings
warnings.filterwarnings('ignore')

url = "https://dmp-dev.mingdata.com/api/open-api/audience/insight/result"
params = {
    'ts': '1774580142',
    'randStr': '8165',
    'accessKey': 'wArzwWvT',
    'sign': '5A4E951BCCF371F48FDFA39BF2D53A25',
    'taskId': '100262'
}

response = requests.get(url, params=params, verify=False)
print(response.json())
```

---

## 凭证配置

### ✅ 推荐方式：环境变量

```bash
# 开发环境
export DMP_AK='your_access_key'
export DMP_SK='your_secret_key'

# Python代码自动读取
from scripts.insight_api import InsightAPI
api = InsightAPI()
```

### ✅ OpenClaw Dashboard 配置

1. 打开 OpenClaw Dashboard
2. 进入 **Skills** 页面
3. 找到 **dmp-persona-insight**
4. 点击 **配置** 按钮
5. 填入：
   - `DMP_AK` - 明日DMP Access Key
   - `DMP_SK` - 明日DMP Secret Key
6. 保存

### ✅ 代码中直接传入

```python
from scripts.insight_api import InsightAPI

api = InsightAPI(
    ak='wArzwWvT',
    sk='zZYeW35ndoQVmUv5S2Kuq1PipMYC8mN0'
)
result = api.get_insight_result(100262)
```

---

## 工作流示例

### 场景：自动拉取洞察结果并生成报告

```python
from scripts.insight_api import InsightAPI
from scripts.analyze_persona import parse_insight_to_persona
import json
import warnings
warnings.filterwarnings('ignore')

# 1. 初始化API
api = InsightAPI(ak='your_ak', sk='your_sk')

# 2. 查询任务状态
print("📋 查询任务状态...")
status_list = api.query_insight_status([100262])

task = status_list[0]
if task.get('status') == 1:  # 成功
    print(f"✅ 任务完成：{task.get('name')}")
    
    # 3. 获取结果
    print("📥 拉取分析结果...")
    result = api.get_insight_result(100262)
    
    # 4. 输出数据
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
elif task.get('status') == 3:  # 计算中
    print(f"⏳ 任务仍在计算中，请稍后查询...")
    
elif task.get('status') == 0:  # 失败
    print(f"❌ 任务失败")
```

---

## 常见问题

### Q: 签名一直生成失败，提示 "找不到该accessKey信息"？

**A:** 检查以下几点：
1. ✅ AK/SK 是否正确（无多余空格）
2. ✅ 签名算法是否是 MD5（不是 SHA1）
3. ✅ 签名字符串顺序是否正确：`ts + randStr + SK`
4. ✅ 签名是否大写（.upper()）
5. ✅ 时间戳是否是 10 位秒级（不是毫秒）
6. ✅ 随机数是否是 4 位数字（1000-9999）

### Q: 为什么API域名是 dmp-dev.mingdata.com 而不是 open.mingdata.com？

**A:** 明日DMP 的洞察 API 部署在开发环境域名上，这是正常的。v2.0版本使用了错误的域名（open.mingdata.com），已在 v3.0 中修正。

### Q: 任务一直显示"等待中"或"计算中"？

**A:** 这是正常的。明日DMP 的洞察任务通常需要 5-30 分钟完成：
- 任务提交后，建议 5 分钟后再查询
- 任务计算期间，每 2-5 分钟查询一次
- 避免频繁查询（建议不要在 30 秒内重复查询同一任务）

### Q: 获取结果返回空数据或错误？

**A:** 可能原因：
1. 人群量级过小（< 1万），洞察分析无法进行
2. 任务仍在计算中，还未完成
3. 任务失败（请检查任务状态）
4. 任务ID 错误或不存在

### Q: 如何重新生成洞察任务？

**A:** 使用 mingdata-dmp skill 中的"创建洞察任务"功能：
1. 需要指定新的人群 ID
2. 需要选择洞察维度（basic、region、interest 等）
3. 系统会返回新的 taskId
4. 使用新的 taskId 查询结果

### Q: 能否批量查询多个任务？

**A:** 可以。调用 `query_insight_status([task_id_1, task_id_2, ...])` 一次查询多个任务。

---

## API 参考

### InsightAPI 类

#### 初始化
```python
# 方式1：直接传入凭证
api = InsightAPI(ak="wArzwWvT", sk="zZYeW35ndoQVmUv5S2Kuq1PipMYC8mN0")

# 方式2：从环境变量读取
api = InsightAPI()
```

#### 查询任务状态
```python
status = api.query_insight_status([100262])
# 返回列表，每项包含：
# - id: 任务ID
# - name: 任务名称
# - status: 状态码 (0/1/2/3)
# - createdAt: 创建时间
```

#### 获取任务结果
```python
result = api.get_insight_result(100262)
# 返回特征树结构数据，包含：
# - id: 特征ID
# - name: 特征名称
# - coverageRate: 覆盖率 (小数)
# - tgi: TGI指标
# - children: 子特征列表
```

---

## 版本历史

| 版本 | 日期 | 改动 |
|------|------|------|
| 3.0 | 2026-03-27 | ✅ 修正鉴权算法：SHA1 → MD5；修正域名：open → dmp-dev；修正随机数：32位 → 4位 |
| 2.0 | 2026-03-27 | ❌ 初始版本，使用了错误的鉴权方式 |

---

## 更新日志

### v3.0 更新内容（2026-03-27）

🔧 **鉴权方式优化**
- ✅ 算法：SHA1 → **MD5**
- ✅ 签名格式：`MD5(ts + randStr + SK).upper()`
- ✅ 随机数：32位字母数字 → **4位纯数字**
- ✅ 时间戳：毫秒级 → **秒级**
- ✅ 域名：open.mingdata.com → **dmp-dev.mingdata.com**

📚 **文档更新**
- ✅ 补充详细的鉴权步骤
- ✅ 添加常见问题解答
- ✅ 完善 API 参考

🚀 **脚本更新**
- ✅ `insight_api.py` 升级至 v3.0
- ✅ 自动处理 SSL 证书警告
- ✅ 改进错误提示信息

