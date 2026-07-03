---
name: "ebay-batch-registration"
description: "eBay 企业批量注册技能：支持20-50个法人队列管理、环境调度、进度断点续传、风控间隔控制"
---

# eBay 批量注册技能（Skill）

> **目标**：支持 20-50 个法人批量注册，解决环境资源、队列管理、进度跟踪、风控间隔等批量特有问题。
>
> **基于**：ebay-business-registration v2.0（单法人注册流程）
>
> **版本**：v1.0
>
> **适用场景**：大帅哥团队批量出海，多法人矩阵运营

---

## 一、批量注册总体架构

### 1.1 设计理念

**核心原则**：串行处理，逐个人完成，避免资源冲突和风控触发。

**不是并行！** HubStudio 资源不支持同时开 50 个环境，eBay 风控也会检测同一 IP 批量注册。

### 1.2 处理流程图

```
准备阶段
├── 批量准备资料（50套法人资料）
├── 批量注册邮箱（50个 email.cn）
├── 准备队列 JSON（记录所有法人状态）
└── 检查资源（好租码余额、HubStudio状态）

执行阶段（串行）
├── 法人1：启动环境 → 注册 → 完成 → 关闭环境
├── 等待2-4小时（风控间隔）
├── 法人2：启动环境 → 注册 → 完成 → 关闭环境
├── 等待2-4小时
├── ...
└── 法人N：启动环境 → 注册 → 完成 → 关闭环境

监控阶段
├── 每天检查队列进度
├── 处理失败案例（断点续传）
├── Payoneer审核状态跟踪
└── 销售额度查询与归档
```

---

## 二、准备阶段

### 2.1 文件夹结构（批量版）

```
C:/Users/win/Desktop/注册资料/
├── batch_queue.json              # 队列主文件（所有法人状态）
├── batch_report.xlsx             # 汇总报告（自动生成）
├── 法人1-张三/
│   ├── 注册资料.txt
│   ├── 营业执照.png
│   ├── 身份证正面.png
│   └── 身份证反面.png
├── 法人2-李四/
│   ├── 注册资料.txt
│   ├── 营业执照.png
│   ├── 身份证正面.png
│   └── 身份证反面.png
├── ...
└── 法人50-王五/
    ├── 注册资料.txt
    ├── 营业执照.png
    ├── 身份证正面.png
    └── 身份证反面.png
```

### 2.2 队列文件 batch_queue.json

```json
{
  "batch_id": "batch_20260616_001",
  "created_at": "2026-06-16",
  "total": 50,
  "completed": 12,
  "failed": 2,
  "pending": 36,
  "in_progress": 0,
  "legal_persons": [
    {
      "id": 1,
      "name": "张三",
      "hubstudio_env_id": "1662847623",
      "status": "completed",
      "current_step": "done",
      "ebay_username": "k9mNp2xQ7a",
      "ebay_account": "xxx@email.cn",
      "payoneer_account": "104651817",
      "selling_limit": "25件",
      "started_at": "2026-06-16 08:00",
      "completed_at": "2026-06-16 10:30",
      "error_log": null,
      "next_retry": null
    },
    {
      "id": 2,
      "name": "李四",
      "hubstudio_env_id": "1662847624",
      "status": "failed",
      "current_step": "hCaptcha",
      "ebay_username": null,
      "ebay_account": "yyy@email.cn",
      "payoneer_account": null,
      "selling_limit": null,
      "started_at": "2026-06-16 14:00",
      "completed_at": null,
      "error_log": "hCaptcha 连续失败3次",
      "next_retry": "2026-06-17 08:00"
    },
    {
      "id": 3,
      "name": "王五",
      "hubstudio_env_id": "1662847625",
      "status": "pending",
      "current_step": null,
      "ebay_username": null,
      "ebay_account": null,
      "payoneer_account": null,
      "selling_limit": null,
      "started_at": null,
      "completed_at": null,
      "error_log": null,
      "next_retry": null
    }
  ]
}
```

### 2.3 队列状态定义

| 状态 | 说明 | 可执行操作 |
|------|------|-----------|
| `pending` | 待处理 | 启动注册 |
| `in_progress` | 进行中 | 暂停/继续 |
| `completed` | 已完成 | 查询额度/归档 |
| `failed` | 失败 | 断点续传/重试 |
| `paused` | 手动暂停 | 恢复/跳过 |
| `skipped` | 已跳过 | 重新加入队列 |

### 2.4 注册资料批量模板

```
==== 批量注册资料模板 ====
法人ID：{id}
法人姓名：{name}
法人姓名拼音：
出生日期：
身份证号：

邮箱：{auto_generated}
邮箱密码：{auto_generated}

ebay账号：{就是邮箱}
ebay密码：{auto_generated}

ebay用户名：{脚本随机生成}
Payoneer邮箱：{同上}
Payoneer密码：{auto_generated}

ebay手机号：{接码后记录}
Payoneer手机号：{接码后记录}

ebay信用卡号：
ebay信用卡有效期：
ebay信用卡CVV：

Payoneer银行名称：
Payoneer银行卡号：
Payoneer银行地址：

公司中文名：
公司英文名：
统一社会信用代码：
公司注册日期：
公司邮编：
公司地址中文：
公司地址英文：

==== 状态记录 ====
注册状态：{pending}
当前步骤：
失败原因：
最后更新时间：
```

---

## 三、执行阶段：队列调度器

### 3.1 核心调度逻辑

```python
class BatchQueueManager:
    """批量队列管理器"""
    
    def __init__(self, queue_file):
        self.queue_file = queue_file
        self.queue = self.load_queue()
        self.current_person = None
    
    def load_queue(self):
        """加载队列文件"""
        import json
        with open(self.queue_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_queue(self):
        """保存队列状态"""
        import json
        with open(self.queue_file, 'w', encoding='utf-8') as f:
            json.dump(self.queue, f, ensure_ascii=False, indent=2)
    
    def get_next_person(self):
        """获取下一个待处理的法人"""
        for person in self.queue['legal_persons']:
            if person['status'] in ['pending', 'failed']:
                # 检查是否到重试时间
                if person['next_retry']:
                    from datetime import datetime
                    if datetime.now() < datetime.fromisoformat(person['next_retry']):
                        continue
                return person
        return None
    
    def update_person_status(self, person_id, status, step=None, error=None):
        """更新法人状态"""
        for person in self.queue['legal_persons']:
            if person['id'] == person_id:
                person['status'] = status
                if step:
                    person['current_step'] = step
                if error:
                    person['error_log'] = error
                person['last_updated'] = datetime.now().isoformat()
                break
        self.save_queue()
    
    def start_person(self, person_id):
        """开始处理一个法人"""
        self.update_person_status(person_id, 'in_progress', 'starting')
        self.current_person = person_id
    
    def complete_person(self, person_id, data):
        """完成一个法人"""
        for person in self.queue['legal_persons']:
            if person['id'] == person_id:
                person['status'] = 'completed'
                person['completed_at'] = datetime.now().isoformat()
                person['ebay_username'] = data.get('ebay_username')
                person['ebay_account'] = data.get('ebay_account')
                person['payoneer_account'] = data.get('payoneer_account')
                person['selling_limit'] = data.get('selling_limit')
                break
        self.save_queue()
    
    def fail_person(self, person_id, error, retry_after_hours=4):
        """标记失败，设置重试时间"""
        from datetime import datetime, timedelta
        for person in self.queue['legal_persons']:
            if person['id'] == person_id:
                person['status'] = 'failed'
                person['error_log'] = error
                person['next_retry'] = (datetime.now() + timedelta(hours=retry_after_hours)).isoformat()
                break
        self.save_queue()
```

### 3.2 风控间隔控制

```python
import time
import random

def wait_between_persons(min_hours=2, max_hours=4):
    """
    法人间的风控间隔
    模拟自然节奏，不是固定间隔
    """
    wait_seconds = random.uniform(min_hours * 3600, max_hours * 3600)
    
    print(f"等待 {wait_seconds/3600:.1f} 小时后继续下一个法人...")
    print(f"预计恢复时间: {datetime.now() + timedelta(seconds=wait_seconds)}")
    
    time.sleep(wait_seconds)
```

### 3.3 环境串行调度

```python
def process_single_person(person):
    """
    处理单个法人（调用原有单法人技能）
    """
    env_id = person['hubstudio_env_id']
    
    # 1. 启动 HubStudio 环境
    start_hubstudio(env_id)
    
    # 2. 获取 debug port
    port = get_debug_port(env_id)
    
    # 3. 连接浏览器
    connect_browser(port)
    
    # 4. 调用单法人注册流程（复用原有技能）
    from ebay_business_registration import register_single_person
    result = register_single_person(person)
    
    # 5. 关闭环境
    stop_hubstudio(env_id)
    
    return result

def batch_process(queue_file, max_per_day=5):
    """
    批量处理主循环
    """
    manager = BatchQueueManager(queue_file)
    processed_today = 0
    
    while True:
        # 检查今日处理数量
        if processed_today >= max_per_day:
            print(f"今日已处理 {max_per_day} 个法人，暂停到明天...")
            # 等待到第二天
            wait_until_next_day()
            processed_today = 0
        
        # 获取下一个法人
        person = manager.get_next_person()
        if not person:
            print("所有法人处理完成！")
            break
        
        # 处理法人
        try:
            manager.start_person(person['id'])
            result = process_single_person(person)
            
            if result['success']:
                manager.complete_person(person['id'], result)
                processed_today += 1
                print(f"✅ 法人 {person['name']} 完成！")
            else:
                manager.fail_person(person['id'], result['error'])
                print(f"❌ 法人 {person['name']} 失败：{result['error']}")
        
        except Exception as e:
            manager.fail_person(person['id'], str(e))
            print(f"💥 法人 {person['name']} 异常：{e}")
        
        # 风控间隔
        if manager.get_next_person():
            wait_between_persons(2, 4)
```

---

## 四、断点续传机制

### 4.1 断点定义

每个法人注册有 7 个 Phase，每个 Phase 完成后记录断点：

```python
BREAKPOINTS = [
    'phase_1_env_ready',        # 环境启动完成
    'phase_2_ebay_form_filled', # eBay表单填写完成
    'phase_3_email_verified',   # 邮箱验证完成
    'phase_4_phone_verified',   # 手机验证完成
    'phase_5_company_done',     # 企业认证完成
    'phase_6_payoneer_linked',  # Payoneer绑定完成
    'phase_7_card_done',        # 信用卡绑定完成
    'phase_8_limit_checked',    # 额度查询完成
    'done'                      # 全部完成
]
```

### 4.2 断点续传逻辑

```python
def resume_person(person):
    """
    从断点恢复注册
    """
    current_step = person['current_step'] or 'phase_1_env_ready'
    
    # 找到对应的 Phase 继续
    phase_map = {
        'phase_1_env_ready': start_env,
        'phase_2_ebay_form_filled': do_email_verification,
        'phase_3_email_verified': do_phone_verification,
        'phase_4_phone_verified': do_company_verification,
        'phase_5_company_done': do_payoneer_binding,
        'phase_6_payoneer_linked': do_credit_card,
        'phase_7_card_done': check_selling_limit,
    }
    
    # 从当前步骤继续
    for phase in BREAKPOINTS:
        if phase == current_step:
            # 继续执行
            func = phase_map.get(phase)
            if func:
                result = func(person)
                if not result['success']:
                    return result
    
    return {'success': True}
```

### 4.3 常见失败场景与恢复策略

| 失败步骤 | 原因 | 恢复策略 |
|---------|------|---------|
| hCaptcha | 人工未点击 | 重新启动环境，从头开始 |
| 邮箱验证超时 | 验证码过期 | 重新获取验证码，继续 |
| 手机验证失败 | 接码失败 | 换手机号重新接码，继续 |
| Payoneer 跳转失败 | Token过期 | 返回 eBay 重新跳转，继续 |
| 信用卡姓名重复 | React 问题 | 手动修复后，从信用卡步骤继续 |
| 环境崩溃 | 浏览器卡死 | 关闭重启环境，从当前步骤继续 |

---

## 五、批量特有问题与解决方案

### 5.1 问题1：资源耗尽（内存/CPU）

**现象**：处理 10 个法人后，电脑卡死，HubStudio 无法启动新环境。

**解决**：
- 每处理完一个法人，**彻底关闭环境并清理缓存**
- 定期重启电脑（每 5 个法人）
- 监控资源使用，超过 80% 时暂停

```python
def cleanup_after_person(env_id):
    """处理完一个法人后清理资源"""
    stop_hubstudio(env_id)
    clear_browser_cache(env_id)
    # 强制垃圾回收
    import gc
    gc.collect()
    
    # 检查内存使用
    import psutil
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        print("⚠️ 内存使用率过高，建议重启电脑后再继续")
        return False
    return True
```

### 5.2 问题2：IP 被封

**现象**：处理到第 15 个法人时，eBay 提示「无法注册」或「账户限制」。

**解决**：
- 每个法人使用 **不同代理 IP**（如果 HubStudio 支持）
- 延长间隔到 4-6 小时
- 分散到多天（每天 3-5 个）
- 如果被封，暂停 24-48 小时再试

### 5.3 问题3：好租码余额不足

**现象**：处理到一半，接码平台余额用完。

**解决**：
- 批量处理前检查余额
- 设置余额预警（低于 ¥50 时暂停）
- 准备备用接码平台（super5.com）

```python
def check_resources():
    """检查资源是否充足"""
    # 检查好租码余额
    balance = get_haozuma_balance()
    if balance < 50:
        print("⚠️ 好租码余额不足，请充值后再继续")
        return False
    
    # 检查邮箱数量
    remaining = count_remaining_persons()
    if remaining > 0 and not enough_emails(remaining):
        print("⚠️ 邮箱数量不足，请先注册更多邮箱")
        return False
    
    # 检查信用卡数量
    if remaining > 0 and not enough_credit_cards(remaining):
        print("⚠️ 信用卡数量不足")
        return False
    
    return True
```

### 5.4 问题4：用户无法持续在线

**现象**：用户需要工作/睡觉，不能 24 小时盯着 hCaptcha。

**解决**：
- 设置每日处理上限（如 5 个/天）
- 处理完当日配额后自动暂停
- 设置 cron 定时任务，每天早上自动恢复
- 失败时发送通知（钉钉/微信）

```python
def set_daily_limit(limit=5):
    """设置每日处理上限"""
    processed = get_today_processed_count()
    if processed >= limit:
        print(f"今日已处理 {processed} 个，达到上限 {limit}")
        schedule_next_day()
        return False
    return True
```

---

## 六、批量监控与报告

### 6.1 实时进度面板

```python
def show_progress(queue):
    """显示实时进度"""
    total = queue['total']
    completed = queue['completed']
    failed = queue['failed']
    pending = queue['pending']
    
    progress = (completed / total) * 100
    
    print(f"\n{'='*60}")
    print(f"📊 批量注册进度面板")
    print(f"{'='*60}")
    print(f"总数量: {total}")
    print(f"已完成: {completed} ({progress:.1f}%)")
    print(f"失败: {failed}")
    print(f"待处理: {pending}")
    print(f"当前处理: {queue['in_progress']}")
    print(f"\n[{'█' * int(progress/2)}{'░' * (50-int(progress/2))}] {progress:.1f}%")
    print(f"{'='*60}\n")
```

### 6.2 批量报告生成

```python
def generate_report(queue_file, output_file):
    """
    生成 Excel 汇总报告
    """
    import pandas as pd
    import json
    
    with open(queue_file, 'r', encoding='utf-8') as f:
        queue = json.load(f)
    
    data = []
    for person in queue['legal_persons']:
        data.append({
            'ID': person['id'],
            '姓名': person['name'],
            '状态': person['status'],
            'eBay用户名': person.get('ebay_username', ''),
            'eBay账号': person.get('ebay_account', ''),
            'Payoneer账号': person.get('payoneer_account', ''),
            '销售额度': person.get('selling_limit', ''),
            '开始时间': person.get('started_at', ''),
            '完成时间': person.get('completed_at', ''),
            '失败原因': person.get('error_log', '')
        })
    
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"报告已生成：{output_file}")
```

### 6.3 失败案例分析

```python
def analyze_failures(queue_file):
    """
    分析失败案例，找出共性问题
    """
    with open(queue_file, 'r', encoding='utf-8') as f:
        queue = json.load(f)
    
    failures = {}
    for person in queue['legal_persons']:
        if person['status'] == 'failed':
            error = person.get('error_log', 'Unknown')
            failures[error] = failures.get(error, 0) + 1
    
    print("\n失败原因分析：")
    for error, count in sorted(failures.items(), key=lambda x: x[1], reverse=True):
        print(f"  {error}: {count} 次")
    
    return failures
```

---

## 七、使用方式

### 7.1 初始化批量任务

```bash
# 1. 准备 50 套法人资料，放入 C:/Users/win/Desktop/注册资料/法人1~50/

# 2. 初始化队列
python batch_init.py --folder "C:/Users/win/Desktop/注册资料" --output batch_queue.json

# 3. 检查资源
python batch_check.py --queue batch_queue.json

# 4. 开始批量处理（每天5个）
python batch_run.py --queue batch_queue.json --daily-limit 5
```

### 7.2 日常监控

```bash
# 查看进度
python batch_progress.py --queue batch_queue.json

# 查看失败案例
python batch_analyze.py --queue batch_queue.json

# 生成报告
python batch_report.py --queue batch_queue.json --output report.xlsx

# 重新处理失败的案例
python batch_retry.py --queue batch_queue.json --retry-failed
```

### 7.3 与单法人技能的关系

```
ebay-batch-registration（批量）
    ├── 调用 ebay-business-registration（单法人）
    │   ├── 养会话
    │   ├── 填写表单
    │   ├── 验证
    │   └── 绑定
    ├── 队列管理
    ├── 断点续传
    ├── 风控间隔
    └── 监控报告
```

---

## 八、预估时间表（50个法人）

### 方案 A：保守（每天3个，风控间隔4小时）

| 天数 | 处理数量 | 累计完成 | 备注 |
|------|---------|---------|------|
| 第1天 | 3个 | 3 | 测试阶段，观察风控 |
| 第2天 | 3个 | 6 | 确认无风控后稳定执行 |
| ... | ... | ... | |
| 第17天 | 3个 | 50 | 全部完成 |

**总时间：17天**（约2.5周）
**每日投入：3-4小时**（含hCaptcha人工点击）

### 方案 B：激进（每天5个，风控间隔2小时）

| 天数 | 处理数量 | 累计完成 | 备注 |
|------|---------|---------|------|
| 第1天 | 5个 | 5 | |
| 第2天 | 5个 | 10 | |
| ... | ... | ... | |
| 第10天 | 5个 | 50 | |

**总时间：10天**（约1.5周）
**风险**：可能触发 eBay 风控，导致批量失败

### 方案 C：混合（工作日3个，周末5个）

| 天数 | 处理数量 | 累计完成 |
|------|---------|---------|
| 第1-5天（工作日） | 3×5=15 | 15 |
| 第6-7天（周末） | 5×2=10 | 25 |
| 第8-12天（工作日） | 3×5=15 | 40 |
| 第13-14天（周末） | 5×2=10 | 50 |

**总时间：14天**（约2周）
**优点**：兼顾效率与安全

---

## 九、风险控制清单

### 批量前必须确认

- [ ] 50 套法人资料齐全（营业执照、身份证、照片）
- [ ] 50 个邮箱已注册（可用脚本批量）
- [ ] 50 个 HubStudio 环境已创建（每个法人一个）
- [ ] 好租码余额 ≥ ¥200（50 人 × 3 次 × ¥1-3）
- [ ] 信用卡：50 张（或虚拟卡服务已开通）
- [ ] 用户确认每日可投入时间（3-5 小时）
- [ ] 确认风控间隔策略（2-4 小时）
- [ ] 备份重要数据（防止意外丢失）

### 运行中监控

- [ ] 每处理 5 个法人检查 eBay 是否有限制提示
- [ ] 每处理 10 个法人重启电脑清理资源
- [ ] 每天生成进度报告
- [ ] 失败案例超过 3 个时暂停分析原因

---

## 十、技术依赖

| 依赖 | 用途 | 状态 |
|------|------|------|
| ebay-business-registration | 单法人注册流程 | 已固化 ✅ |
| HubStudio API | 环境启动/关闭 | 已有 |
| Selenium + ChromeDriver | 浏览器自动化 | 已有 |
| 好租码 API | 接码服务 | 已有 |
| email.cn IMAP | 邮箱验证码读取 | 已有 |
| pandas + openpyxl | Excel 报告生成 | 需安装 |
| psutil | 系统资源监控 | 需安装 |
| cron / 任务计划 | 定时恢复处理 | 需配置 |

---

## 十一、待办事项

### 已完成
- [x] 单法人注册流程固化（ebay-business-registration v2.0）
- [x] 批量队列架构设计
- [x] 断点续传机制设计
- [x] 风控间隔策略设计

### 待开发
- [ ] `batch_init.py`：批量初始化队列
- [ ] `batch_check.py`：资源检查工具
- [ ] `batch_run.py`：批量处理主脚本
- [ ] `batch_progress.py`：进度监控工具
- [ ] `batch_analyze.py`：失败分析工具
- [ ] `batch_report.py`：Excel 报告生成
- [ ] `batch_retry.py`：失败重试工具
- [ ] 定时任务配置（每天早上自动恢复）

### 待测试
- [ ] 5 个法人测试（验证批量流程）
- [ ] 10 个法人测试（验证资源管理）
- [ ] 观察 eBay 风控触发阈值
- [ ] 测试断点续传功能

---

*批量技能设计时间：2026-06-16 10:16*
*版本：v1.0*
*依赖：ebay-business-registration v2.0*
*适用场景：20-50 法人批量注册*
