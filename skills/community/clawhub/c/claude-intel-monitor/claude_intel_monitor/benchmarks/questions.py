"""Benchmark questions for intelligence degradation detection.

Three categories, 10 questions each. Designed to detect known Claude
degradation patterns: truncated reasoning, shallow analysis, code quality drop.

中文社区发现的降智特征:
- 多步推理跳步（应该说5步只说2步）
- 代码简化（应该写完整却只给骨架）
- 数学幻觉（简单计算也能算错）
- 过度安全拒绝（正常问题也拒答）
"""

MATH_QUESTIONS = [
    {
        "id": "math-01",
        "prompt": "一个水池有进水管和出水管。进水管单独注满需要3小时，出水管单独排空需要5小时。如果两管同时打开，池内有1/3的水，注满需要多少小时？请逐步推导。",
        "expected_concepts": ["工作效率", "代数方程", "单位换算"],
        "check": lambda response: "2" in response and ("小时" in response or "hour" in response) and len(response) > 100,
        "weight": 1.0
    },
    {
        "id": "math-02",
        "prompt": "计算 sum_{k=1}^{n} k*C(n,k) 的闭式表达式，其中 C(n,k) 是二项式系数。请给出推导过程。",
        "expected_concepts": ["组合恒等式", "二项式定理", "n*2^(n-1)"],
        "check": lambda response: "2^(n-1)" in response.replace(" ", "") or "2^{n-1}" in response.replace(" ", "") and len(response) > 150,
        "weight": 1.5
    },
    {
        "id": "math-03",
        "prompt": "证明：sqrt(2) + sqrt(3) 是无理数。",
        "expected_concepts": ["反证法", "有理数定义", "平方展开"],
        "check": lambda response: ("无理" in response or "irrational" in response.lower()) and len(response) > 120,
        "weight": 1.5
    },
    {
        "id": "math-04",
        "prompt": "一个100人的村庄爆发传染病。每天每个感染者会感染2个健康人，同时10%的感染者康复。第0天有1个感染者，第几天全村感染超过90人？请建立数学模型并求解。",
        "expected_concepts": ["递推关系", "SIR模型", "day 6-8"],
        "check": lambda response: any(str(d) in response for d in ["6", "7", "8"]) and len(response) > 200,
        "weight": 1.5
    },
    {
        "id": "math-05",
        "prompt": "一个正方体棱长为1，随机取两个顶点，求它们之间距离的期望值。",
        "expected_concepts": ["概率", "距离公式", "期望值"],
        "check": lambda response: any(x in response for x in ["0.9", "0.90", "0.905", "0.91"]) and len(response) > 100,
        "weight": 1.0
    },
    {
        "id": "math-06",
        "prompt": "矩阵A = [[2,1],[1,2]]，求A的特征值和特征向量，并解释其几何意义。",
        "expected_concepts": ["特征值3,1", "特征向量正交", "几何意义"],
        "check": lambda response: ("3" in response and "1" in response) and len(response) > 150,
        "weight": 1.0
    },
    {
        "id": "math-07",
        "prompt": "一个骰子连续投掷直到出现6为止。求投掷次数的期望值和方差。",
        "expected_concepts": ["几何分布", "期望=6", "方差=30"],
        "check": lambda response: "6" in response and len(response) > 80,
        "weight": 1.0
    },
    {
        "id": "math-08",
        "prompt": "求解：x^4 - 10x^2 + 9 = 0 的所有实根和复根。",
        "expected_concepts": ["换元法", "二次方程", "±1,±3"],
        "check": lambda response: all(r in response for r in ["1", "3"]) and len(response) > 100,
        "weight": 1.0
    },
    {
        "id": "math-09",
        "prompt": "计算极限 lim_{x→0} (sin(x) - x) / x^3。请用泰勒展开推导。",
        "expected_concepts": ["泰勒展开", "-1/6", "sin x ≈ x - x³/6"],
        "check": lambda response: ("-1/6" in response or "-1 / 6" in response.replace(" ","") or "1/6" in response) and len(response) > 150,
        "weight": 1.5
    },
    {
        "id": "math-10",
        "prompt": "在等边三角形ABC内任取一点P，求P到三边距离之和与三角形高的关系。请严格证明。",
        "expected_concepts": ["维维亚尼定理", "面积法", "等于高"],
        "check": lambda response: ("等于" in response or "equal" in response.lower()) and len(response) > 120,
        "weight": 1.0
    },
]

REASONING_QUESTIONS = [
    {
        "id": "reason-01",
        "prompt": "小明说：'如果下雨，我就不出门。' 结果小明出门了。请问：可以得出什么结论？有哪些可能的情况？请用逻辑形式化分析。",
        "expected_concepts": ["逆否命题", "没有下雨", "逻辑蕴涵"],
        "check": lambda response: (("没有" in response and "下雨" in response) or "没下雨" in response) and len(response) > 120,
        "weight": 1.5
    },
    {
        "id": "reason-02",
        "prompt": "A和B两个人，每个说真话或假话。A说：'B说真话。' B说：'A和B不都说真话。' 判断谁说真话。请给出完整推导。",
        "expected_concepts": ["真值表", "矛盾法", "A假B真"],
        "check": lambda response: ("A" in response and "B" in response) and len(response) > 200,
        "weight": 1.5
    },
    {
        "id": "reason-03",
        "prompt": "你有一个8升的水壶和一个5升的水壶，无限量自来水。如何量出4升水？请给出最少步数的解法。",
        "expected_concepts": ["状态转移", "BFS", "最少步骤"],
        "check": lambda response: "4" in response and ("4升" in response or "4L" in response.upper()) and len(response) > 100,
        "weight": 1.0
    },
    {
        "id": "reason-04",
        "prompt": "有12个球，其中11个重量相同，1个重量不同（不知道是轻是重）。用一架天平，最少称几次可以找出这个球并知道它是轻是重？请详细描述策略。",
        "expected_concepts": ["三分法", "信息论", "3次"],
        "check": lambda response: "3" in response and ("次" in response or "times" in response) and len(response) > 300,
        "weight": 2.0
    },
    {
        "id": "reason-05",
        "prompt": "一个岛上住着100个蓝眼睛的人和1个绿眼睛的人。他们不能交流眼睛颜色，但知道至少有1个蓝眼睛。每个午夜，如果某人确定自己眼睛颜色，就离开。问：岛上的人需要多少天全部离开？请用归纳法证明。",
        "expected_concepts": ["公共知识", "数学归纳法", "同步推理"],
        "check": lambda response: ("100" in response or "101" in response) and ("天" in response or "day" in response) and len(response) > 250,
        "weight": 2.0
    },
    {
        "id": "reason-06",
        "prompt": "解释以下悖论：'这句话是假的。' 这句话到底是真的还是假的？请从自指、层次理论、和实际计算的角度分析。",
        "expected_concepts": ["自指", "类型论", "哥德尔不完全"],
        "check": lambda response: ("自指" in response or "递归" in response or "悖论" in response) and len(response) > 200,
        "weight": 1.5
    },
    {
        "id": "reason-07",
        "prompt": "三个盒子，分别标着'苹果'、'橙子'、'苹果和橙子'，但所有标签都贴错了。只从一个盒子里拿出一个水果看，你能确定所有盒子里装的是什么吗？如果可以，从哪个盒子里拿？",
        "expected_concepts": ["标签错误约束", "信息推理", "混合盒子"],
        "check": lambda response: ("混合" in response or "苹果和橙子" in response or "both" in response.lower()) and len(response) > 120,
        "weight": 1.0
    },
    {
        "id": "reason-08",
        "prompt": "一个人从A地出发去B地，前半程速度30km/h，后半程速度50km/h，求平均速度。注意：是路程的一半，不是时间的一半。",
        "expected_concepts": ["调和平均", "37.5", "不是算术平均"],
        "check": lambda response: ("37.5" in response or "37. 5" in response.replace(" ","")) and len(response) > 80,
        "weight": 1.0
    },
    {
        "id": "reason-09",
        "prompt": "某公司老板说：'表现最好的员工不会加薪。'人力资源部门调查后发现，加薪的员工都不是表现最好的。请问老板的话可以被推翻吗？请用文氏图推理。",
        "expected_concepts": ["集合论", "原命题vs逆否命题", "逻辑等价"],
        "check": lambda response: ("不能" in response or "没有矛盾" in response or "一致" in response) and len(response) > 120,
        "weight": 1.5
    },
    {
        "id": "reason-10",
        "prompt": "一个国王想要处决你，给你一个机会：在两个相同的门中选一个，一个后面是老虎，一个后面是美女。你选了1号门。国王说：'剩下的2号门后面是美女。' 你应该换门吗？还是无所谓？请用条件概率严格分析。",
        "expected_concepts": ["蒙提霍尔", "条件概率", "换门/不换"],
        "check": lambda response: ("换" in response or "switch" in response.lower() or "2/3" in response) and len(response) > 180,
        "weight": 1.5
    },
]

CODE_QUESTIONS = [
    {
        "id": "code-01",
        "prompt": """用 Python 实现一个线程安全的 LRU 缓存，支持并发读写。要求：
1. 使用 threading.Lock
2. 实现 get(key) 和 put(key, value) 
3. 达到容量上限时淘汰最久未使用的
4. 时间复杂度 O(1)

请写出完整可运行代码并解释关键设计。""",
        "expected_concepts": ["双向链表", "dict", "Lock", "O(1)"],
        "check": lambda response: ("OrderedDict" in response or "双向" in response or "doubly" in response.lower()) and "lock" in response.lower() and len(response) > 300,
        "weight": 1.5
    },
    {
        "id": "code-02",
        "prompt": """写一个 Python 函数，输入一个整数 n，输出所有有效的 n 对括号组合。
例如 n=3，输出: ["((()))","(()())","(())()","()(())","()()()"]

请用回溯法实现，并分析时间复杂度和卡特兰数公式。""",
        "expected_concepts": ["回溯", "卡特兰数", "O(4^n/sqrt(n))"],
        "check": lambda response: "backtrack" in response.lower() or "回溯" in response and len(response) > 200,
        "weight": 1.5
    },
    {
        "id": "code-03",
        "prompt": """以下 Python 代码有什么问题？请找出至少 3 个 bug 并解释修复方案：

```python
class DataProcessor:
    def __init__(self, data=[]):
        self.data = data
    
    def add(self, item):
        self.data.append(item)
    
    def process(self):
        return [x/len(self.data) for x in self.data]
```""",
        "expected_concepts": ["可变默认参数", "除零", "类型安全"],
        "check": lambda response: ("默认参数" in response or "mutable" in response.lower()) and "0" in response and len(response) > 150,
        "weight": 1.0
    },
    {
        "id": "code-04",
        "prompt": """实现一个异步批量请求处理器，要求：
1. 最多同时发送 N 个并发请求
2. 如果某个请求失败，最多重试 2 次
3. 所有请求完成后返回结果列表
4. 使用 asyncio.Semaphore

请写出完整代码。""",
        "expected_concepts": ["asyncio", "Semaphore", "gather", "retry"],
        "check": lambda response: "semaphore" in response.lower() and "asyncio" in response.lower() and len(response) > 250,
        "weight": 1.5
    },
    {
        "id": "code-05",
        "prompt": """解释 Python 中 __new__ 和 __init__ 的区别。在什么场景下需要重写 __new__？请用单例模式的实现举例说明。""",
        "expected_concepts": ["__new__创建对象", "__init__初始化", "单例", "元类"],
        "check": lambda response: "__new__" in response and "单例" in response and len(response) > 150,
        "weight": 1.0
    },
    {
        "id": "code-06",
        "prompt": """写一个 SQL 查询：有一个 orders 表（id, user_id, amount, created_at），
找出连续 3 天及以上每天都有订单的用户，输出 user_id 和最长连续天数。
请用窗口函数实现。""",
        "expected_concepts": ["窗口函数", "LAG/LEAD", "连续天数", "ROW_NUMBER"],
        "check": lambda response: ("row_number" in response.lower() or "lag" in response.lower()) and "group" in response.lower() and len(response) > 200,
        "weight": 1.5
    },
    {
        "id": "code-07",
        "prompt": """写一个 Python 装饰器 @retry_with_backoff，功能：
1. 重试指定次数
2. 每次重试间隔指数增长（1s, 2s, 4s, 8s...）
3. 可以指定仅在特定异常时重试
4. 重试耗尽后抛出原异常

请实现并给出使用示例。""",
        "expected_concepts": ["装饰器", "functools.wraps", "exponential backoff", "time.sleep"],
        "check": lambda response: "@wraps" in response and "exp" in response.lower() and len(response) > 200,
        "weight": 1.0
    },
    {
        "id": "code-08",
        "prompt": """用 Rust 或 Python 实现一个简单的内存池分配器（memory pool），
支持 allocate(size: usize) -> Option<*mut u8> 和 deallocate(ptr: *mut u8)。
解释你的设计如何减少内存碎片。

注：用Python实现则模拟底层分配逻辑即可。""",
        "expected_concepts": ["free list", "块大小", "碎片", "bump allocator"],
        "check": lambda response: ("free" in response.lower() or "碎片" in response or "block" in response.lower()) and len(response) > 200,
        "weight": 1.5
    },
    {
        "id": "code-09",
        "prompt": """写一个 Python 脚本，把一个目录下所有文件的编码从 GBK 批量转换为 UTF-8。
要求：
1. 递归处理子目录
2. 自动检测原编码（尝试常见的几种）
3. 备份原文件
4. 打印转换日志""",
        "expected_concepts": ["chardet", "os.walk", "编码转换", "备份"],
        "check": lambda response: ("chardet" in response.lower() or "detect" in response.lower()) and "编码" in response and len(response) > 200,
        "weight": 1.0
    },
    {
        "id": "code-10",
        "prompt": """设计一个简单的分布式限流器（rate limiter）使用 Redis：
1. 支持固定时间窗口（如每分钟100次）
2. 支持滑动窗口（更精确）
3. 用 Lua 脚本保证原子性
4. 给出 Python 客户端代码

请解释两种窗口的优缺点。""",
        "expected_concepts": ["Redis", "Lua", "ZSET", "滑动窗口", "INCR"],
        "check": lambda response: ("lua" in response.lower() or "redis" in response.lower()) and "窗口" in response and len(response) > 250,
        "weight": 1.5
    },
]

# All questions combined
ALL_QUESTIONS = [
    {"category": "math", "questions": MATH_QUESTIONS},
    {"category": "reasoning", "questions": REASONING_QUESTIONS},
    {"category": "code", "questions": CODE_QUESTIONS},
]
