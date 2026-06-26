# SKILL.md - 公司情报侦察

> **名称：** 公司情报侦察
> **触发：** 用户提供公司 URL 或公司名，要求建档/背调/找联系人/查邮箱
> **执行：** SHADOW Agent 直接调用工具完成全流程
> **输出：** 本地档案 + OKKI 建档 + 有效邮箱列表

---

## 📋 完整工作流（SHADOW 亲自执行）

```
Phase 1: 网站背调 → Phase 2: 联系人挖掘 → Phase 3: 邮箱验证 → Phase 4: 写入 OKKI
```

### Phase 1: 网站背调

**工具：** `web_fetch` + `web_search`

```
1. web_fetch 目标 URL（contact-us / about / 首页）
2. web_fetch 补充页面（/about/, /career/, /services/）
3. web_search 公司名（获取 LinkedIn / ZoomInfo / Moneyhouse 等外部来源）
4. 交叉验证：至少 2 个独立来源确认同一信息
```

**提取字段：**
- 公司全称、简称、国家、地址
- 电话、邮箱、网站
- 成立时间、营业额、员工规模
- 业务类型、产品线、代理品牌
- 核心团队（官网列出的）

### Phase 2: 联系人挖掘

**工具：** `web_search`

```
1. site:linkedin.com/in "{公司名}" — 找员工 LinkedIn
2. "{公司名}" "CEO" OR "buyer" OR "purchasing" OR "category manager"
3. "{公司名}" "{人名}" email — 找已知人名的邮箱
4. 从 RocketReach / Hunter.io snippet 推导邮箱格式
5. 基于已知格式（first@domain.com 等）推导更多邮箱
```

**关键角色优先级：**
1. CEO/Founder — 最高决策人
2. Head of Distribution/Purchasing — 采购负责人
3. Category Manager — 品类采购
4. Key Account Manager — 可反向利用
5. Finance Head — 价格谈判

### Phase 3: SMTP 邮箱验证（零风险）

**工具：** `exec` 运行 Python 脚本

SHADOW 执行以下 Python 代码，逐个验证邮箱：

```python
import socket
import time

emails = ['artur@domain.com', 'info@domain.com', ...]
mx = 'mail.domain.com'  # 从 dig MX 获取

for email in emails:
    s = socket.create_connection((mx, 25), timeout=15)
    s.settimeout(15)
    s.recv(1024)
    s.send(b"EHLO gmail.com\r\n")
    time.sleep(2)
    s.recv(4096)
    s.send(b"MAIL FROM:<test@gmail.com>\r\n")
    time.sleep(2)
    s.recv(512)
    s.send(f"RCPT TO:<{email}>\r\n".encode())
    time.sleep(2)
    resp = s.recv(512).decode()
    code = resp[:3]  # 250 = 有效，550 = 不存在
    s.send(b"QUIT\r\n")
    s.close()
    time.sleep(3)  # 每个邮箱间隔 3 秒
```

**⚠️ 关键：**
- 必须 `time.sleep(2~3)`，否则超时
- 只到 RCPT TO，绝不发 DATA
- 每个邮箱之间间隔 3 秒

### Phase 4: 写入 OKKI

**工具：** `exec` 调 OKKI CLI

**4a. 本地存档：**
```
intelligence/clients/{Company_Name}.md
```

**4b. OKKI 新建客户：**
```python
data = {
    'name': '公司全称',
    'short_name': '简称',
    'country': 'ISO两位码',
    'address': '详细地址',
    'homepage': 'https://...',
    'user_id': 56785529,  # Jordan
    'group_id': 0,
    'pool_id': 0,
    'is_public': 0,
    'remark': '关键信息摘要',
    'customers': [
        {'first_name': '名', 'last_name': '姓', 'position': '职位', 'email': '已验证邮箱'}
    ]
}
```

注意：`group_id` 和 `pool_id` 必填，不能省略。

---

## 📝 交付模板

### 本地档案
```markdown
# {Company Name}

> 建档日期：YYYY-MM-DD | 跟进人：XXX

## 基本信息
| 项目 | 内容 |
|------|------|

## 核心联系人（已验证邮箱）
| 姓名 | 职位 | 邮箱 | 状态 |
|------|------|------|------|

## 关键点
- ...
```

---

## ⚠️ 安全红线

1. **邮箱验证绝不发 DATA** — 只到 RCPT TO 阶段
2. **公司背调三步法则** — 域名可访问 → 内容匹配 → 交叉验证
3. **不捏造信息** — 不确定时说"不确定"
4. **OKKI 建档必填 group_id/pool_id**
