# 🔗 购买链接通用功能说明

**版本**: v1.7.0  
**日期**: 2026-03-15  
**功能**: 所有场景推荐的可注册域名自动生成阿里云购买链接

---

## 📋 功能说明

### 问题背景

之前购买链接功能仅在热点投资分析脚本中实现，但实际使用中，以下场景也会推荐可注册域名：

- 日常域名检查（`check_domain()`）
- 批量域名筛选
- 关键词推荐
- 吉利数字组合推荐
- 用户自定义域名检查

这些场景下推荐的域名没有购买链接，用户体验不一致。

### 解决方案

**将购买链接功能升级为通用能力**，适用于所有推荐可注册域名的场景。

---

## 🎯 适用场景

| 场景 | 说明 | 示例 |
|:---|:---|:---|
| **热点投资分析** | 热点关键词推荐的可注册域名 | `python3 domain_hotspot_analyzer.py claw` |
| **日常域名检查** | 检查某个域名是否可注册 | `check_domain("example.cn")` |
| **批量域名筛选** | 批量检查多个域名的可注册性 | 循环检查域名列表 |
| **关键词推荐** | 根据用户提供的关键词推荐域名 | "推荐几个 AI 相关的域名" |
| **吉利数字组合** | 吉利数字域名推荐 | "有哪些 168 结尾的域名可注册" |
| **自定义域名** | 用户指定的域名检查 | "帮我检查 shenyue123.cn 能否注册" |

---

## 🔧 技术实现

### 1. 核心函数（复用）

```python
def extract_suffix(domain: str) -> str:
    """从域名中提取后缀（不带点）"""
    match = re.search(r'\.([a-zA-Z]+)$', domain)
    if match:
        return match.group(1)
    return ""

def generate_buy_link(domain: str, duration: int = 12) -> str:
    """生成阿里云购买链接"""
    suffix = extract_suffix(domain)
    domain_name = re.sub(r'\.[a-zA-Z]+$', '', domain)
    
    base_url = "https://wanwang.aliyun.com/buy/commonbuy"
    params = f"?domain={domain_name}&suffix={suffix}&duration={duration}"
    
    return base_url + params
```

### 2. 使用方式

#### 方式一：在热点分析脚本中使用

```python
from domain_hotspot_analyzer import generate_buy_link

for domain in available_domains:
    buy_link = generate_buy_link(domain['domain'])
    print(f"[{domain['domain']}]({buy_link}) - ¥{domain['price']}")
```

#### 方式二：在主脚本中使用

```python
from aliyun_domain import AliyunDomainClient

client = AliyunDomainClient()

# 检查域名
result = client.check_domain("example.cn")
if result.get('available'):
    buy_link = generate_buy_link("example.cn")
    print(f"✅ {result['domain_name']} 可注册 - [点击购买]({buy_link})")
```

#### 方式三：批量检查场景

```python
domains = ["claw168.cn", "claw518.cn", "tryagent.cn"]

for domain in domains:
    result = client.check_domain(domain)
    if result.get('available'):
        buy_link = generate_buy_link(domain)
        print(f"✅ [{domain}]({buy_link}) - ¥{result['price_info'][0]['money']}")
```

---

## 📊 输出格式规范

### 单个域名推荐

```
✅ [claw168.cn](https://wanwang.aliyun.com/buy/commonbuy?domain=claw168&suffix=cn&duration=12) - ¥38 🔢 吉利数字
```

### 多个域名推荐（列表）

```
✅ 可注册域名推荐：

1. [claw168.cn](https://wanwang.aliyun.com/buy/commonbuy?domain=claw168&suffix=cn&duration=12) - ¥38 🔢 吉利数字
2. [claw518.cn](https://wanwang.aliyun.com/buy/commonbuy?domain=claw518&suffix=cn&duration=12) - ¥38 🔢 吉利数字
3. [tryagent.cn](https://wanwang.aliyun.com/buy/commonbuy?domain=tryagent&suffix=cn&duration=12) - ¥38 🤖 AI 智能体
```

### 快速链接列表（报告末尾）

```
🔗 快速购买链接:
  1. https://wanwang.aliyun.com/buy/commonbuy?domain=claw168&suffix=cn&duration=12
  2. https://wanwang.aliyun.com/buy/commonbuy?domain=claw518&suffix=cn&duration=12
  3. https://wanwang.aliyun.com/buy/commonbuy?domain=tryagent&suffix=cn&duration=12
```

---

## 🎁 用户体验提升

### Before（之前）

```
✅ claw168.cn 可注册 - ¥38

用户需要：
1. 复制域名 claw168.cn
2. 打开阿里云官网
3. 搜索域名
4. 选择购买年限
5. 加入购物车
```

### After（现在）

```
✅ [claw168.cn](https://wanwang.aliyun.com/buy/commonbuy?domain=claw168&suffix=cn&duration=12) - ¥38

用户只需：
1. 点击链接
2. 直接购买 ✅
```

**操作步骤**: 5 步 → 1 步 🎉

---

## 📝 代码示例

### 示例 1: 日常域名检查

```python
#!/usr/bin/env python3
"""检查指定域名是否可注册，并生成购买链接"""

from aliyun_domain import AliyunDomainClient
from domain_hotspot_analyzer import generate_buy_link

client = AliyunDomainClient()

domains = ["shenyue123.cn", "shenyue123.com", "shenyue123.xyz"]

print("🔍 域名检查:")
print("=" * 70)

for domain in domains:
    result = client.check_domain(domain)
    is_avail = result.get('available', False)
    
    if is_avail:
        price_info = result.get('price_info', [])
        price = price_info[0].get('money', 'N/A') if price_info else 'N/A'
        buy_link = generate_buy_link(domain)
        print(f"✅ [{domain}]({buy_link}) - ¥{price} 可注册")
    else:
        print(f"❌ {domain} 已注册")
```

### 示例 2: 批量域名筛选

```python
#!/usr/bin/env python3
"""批量检查域名，输出可注册域名及购买链接"""

from aliyun_domain import AliyunDomainClient
from domain_hotspot_analyzer import generate_buy_link

client = AliyunDomainClient()

# 生成候选域名
keyword = "claw"
suffixes = [".cn", ".xyz", ".io"]
candidates = [f"{keyword}{i}{s}" for i in range(100, 1000) for s in suffixes]

available = []

for domain in candidates[:50]:  # 限制检查数量
    result = client.check_domain(domain)
    if result.get('available'):
        price_info = result.get('price_info', [])
        price = price_info[0].get('money', 'N/A') if price_info else 'N/A'
        available.append({
            'domain': domain,
            'price': price,
            'buy_link': generate_buy_link(domain)
        })

# 输出结果
print(f"\n✅ 发现 {len(available)} 个可注册域名:\n")
for i, d in enumerate(available[:10], 1):
    print(f"{i}. [{d['domain']}]({d['buy_link']}) - ¥{d['price']}")
```

### 示例 3: 关键词推荐

```python
#!/usr/bin/env python3
"""根据关键词推荐可注册域名"""

from aliyun_domain import AliyunDomainClient
from domain_hotspot_analyzer import generate_buy_link

client = AliyunDomainClient()

keyword = "ai"
patterns = [
    f"get{keyword}.cn",
    f"try{keyword}.cn",
    f"{keyword}dev.cn",
    f"{keyword}lab.cn",
    f"{keyword}168.cn",
]

print(f"🔍 推荐 {keyword} 相关域名:\n")

for domain in patterns:
    result = client.check_domain(domain)
    if result.get('available'):
        buy_link = generate_buy_link(domain)
        print(f"✅ [{domain}]({buy_link})")
```

---

## ✅ 测试用例

| 测试域名 | 预期链接 |
|:---|:---|
| tryagent.cn | https://wanwang.aliyun.com/buy/commonbuy?domain=tryagent&suffix=cn&duration=12 |
| agent518.cn | https://wanwang.aliyun.com/buy/commonbuy?domain=agent518&suffix=cn&duration=12 |
| flow168.xyz | https://wanwang.aliyun.com/buy/commonbuy?domain=flow168&suffix=xyz&duration=12 |
| getauto.com | https://wanwang.aliyun.com/buy/commonbuy?domain=getauto&suffix=com&duration=12 |
| clawcode.io | https://wanwang.aliyun.com/buy/commonbuy?domain=clawcode&suffix=io&duration=12 |

---

## 🚀 最佳实践

### 1. 统一输出格式

所有推荐可注册域名的场景，统一使用以下格式：

```
✅ [域名](购买链接) - 价格 理由
```

### 2. 附带快速链接列表

在报告末尾提供完整链接列表，方便复制：

```
🔗 快速购买链接:
  1. https://...
  2. https://...
```

### 3. 标注推荐理由

为每个域名添加简短的投资理由：

| 理由 | 图标 | 适用场景 |
|:---|:---:|:---|
| AI 智能体热点 | 🤖 | agent/bot 相关 |
| 吉利数字 | 🔢 | 168/518/678 等 |
| 简短易记 | 📌 | 短域名 |
| 科技创业 | ⚡ | .io/.xyz 后缀 |
| 经济实惠 | 💰 | 低价后缀 |

### 4. 提供成本估算

```
💰 总成本估算:
  单域名：¥38
  5 个总计：¥190
  优惠口令：cn 注册多个价格更优
```

---

## 📚 相关文件

| 文件 | 说明 |
|:---|:---|
| `scripts/domain_hotspot_analyzer.py` | 热点投资分析脚本（含购买链接生成） |
| `scripts/aliyun_domain.py` | 阿里云域名 API 客户端 |
| `learnings/BUY_LINK_FEATURE.md` | 购买链接功能说明（v1.6.0） |
| `SKILL.md` | 技能说明文档（v1.7.0） |

---

## 🎯 未来优化

1. **多年限支持**: 允许用户指定购买年限（1 年/2 年/5 年）
2. **购物车批量**: 生成批量购买链接，一键加入购物车
3. **优惠口令**: 在链接中自动附带优惠口令参数（如支持）
4. **价格监控**: 链接附带价格监控，降价时提醒
5. **API 集成**: 将购买链接生成函数集成到主 API 客户端

---

**维护者**: 神月 🦐  
**最后更新**: 2026-03-15  
**技能版本**: v1.7.0
