---
name: 0
description: Zero represents the origin, the blank slate, the reset button. This skill handles initialization, zero-state operations, default values, infinite loops, and the power of nothingness. Use when starting fresh, resetting systems, or working with mathematical zero concepts.
---

# 0（Zero/Origin 简写）

这是一个哲学与技术结合的 Skill，用数字 **0** 触发。0 不只是数字，它代表：

- **原点**：一切开始的地方
- **空集**：无限可能的容器
- **重置**：清洗状态，重新开始
- **无穷**：循环的起点与终点
- **默认值**：未指定时的假设

---

## 核心理念

> "If zero were nothing, nothing would exist."  
> — 0 不是空无，而是**潜能的种子**

---

## 适用场景

当你说：
- "从零开始"
- "重置到初始状态"
- "清空所有数据"
- "初始化项目"
- "默认值是多少？"
- "无限循环怎么做？"
- "空值处理"
- "归零计数器"
- "创建空白画布"

---

## 初始化与归零

**项目初始化**
```bash
0 init                # 创建空白项目
0 new project_name    # 从零开始新项目
0 reset               # 重置所有状态到初始点
0 clean               # 清空缓存、临时文件、构建产物
0 scaffold           # 生成标准目录结构（零配置）
```

**环境重置**
```bash
0 env --fresh        # 重新创建虚拟环境
0 db --wipe          # 清空数据库（谨慎！）
0 cache --clear      # 清空所有缓存
0 config --default   # 恢复默认配置
```

---

## 空值/零值处理

**检测零值**
```bash
# Bash
if [ -z "$var" ]; then      # 空字符串
if [ "$num" -eq 0 ]; then   # 数值零
if [ -f "$file" ]; then     # 文件存在且非零大小
```

**JavaScript/TypeScript**
```javascript
// 零值合并操作符（??）
const value = input ?? defaultValue;  // null/undefined 时使用默认值

// 空值检查
if (!value || value === 0 || value === '') {
  // 处理空/零情况
}

// 逻辑零值
const result = value || fallback;  // falsy 值触发
```

**Python**
```python
# 零值判断
if not value:  # 包括 None, 0, '', [], {}
    value = default

# 空字符串
if value == "" or value is None:
    pass

# 零值合并（Python 3.8+）
value = input or default  # falsy 触发
value = input if input is not None else default
```

---

## 无限循环与零终止

**while true 但优雅退出**
```bash
# 无限循环 + 零条件退出
while true; do
  process
  [ $? -eq 0 ] || break  # 非零退出码时中断
done

# 零秒延迟（尽可能快）
while :; do task; done

# 直到零状态
until [ $(check_status) -eq 0 ]; do
  sleep 1
done
```

**for循环零迭代**
```bash
# 零次迭代（空列表）
for i in $(seq 0 -1); do echo $i; done  # 不输出

# 零索引开始
for i in $(seq 0 9); do echo $i; done   # 0-9
```

---

## 数学零操作

**shell数学**
```bash
# 零初始化
counter=0
sum=0

# 自增/自减
((counter++))
((sum+=value))

# 零除保护
if [ $divisor -ne 0 ]; then
  result=$((dividend / divisor))
else
  echo "Division by zero error!"
fi
```

**编程语言**
```python
# Python
zero = 0
result = abs(-5)  # 5
negation = -0  # 还是 0

# 科学计数法
tiny = 1e-10  # 接近零但不等于零

# 浮点零比较（谨慎！）
import math
if math.isclose(value, 0, abs_tol=1e-9):
    pass
```

```javascript
// JavaScript
0 === -0  // true
Object.is(0, -0)  // false (负零是独立的)
1 / 0  // Infinity
0 / 0  // NaN
-0.toString()  // "0" (隐式转换消除负零)
```

---

## 零宽字符与不可见

**零宽空格（ZWS）**
```bash
# 文件中隐藏数据
echo "secret" | cat -A  # 可见
echo "sec​ret" | cat -A  # U+200b 零宽空格隐藏
```

**零字节文件**
```bash
touch empty.txt        # 创建零字节文件
> zero.log            # 清空文件（保留，大小为零）
: > log.txt           # Bash空操作重定向
```

---

## 默认值模式

**shell默认**
```bash
# 参数默认值
: "${VAR:=default}"    # 如果VAR为空，设为default（并导出）
: "${VAR:-default}"    # 使用default但不修改VAR

# 函数参数默认
func() {
  local arg1=${1:-value1}
  local arg2=${2:-value2}
}
```

**其他语言**
```python
# Python
value = user_input or "default"
value = user_input if user_input is not None else "default"

# JavaScript
const value = input ?? "default";
const legacy = input || "default";
```

---

## 零信任与安全

**零信任模型**
```bash
# 默认拒绝，显式允许
# 无配置时，零权限
chmod 000 secret.txt   # 完全禁止
chmod 644 file.txt     # 最小权限原则

# 零知识证明（概念）
# 不传递秘密，只证明知道
```

**零日漏洞（Zero-day）**
```bash
# 零日响应：立即修补
# 零日防御：多层安全，最小权限
```

---

## 哲学隐喻

**归零心态**
```bash
# 每日清零任务
0 dayplan --clear      # 清除昨日计划
0 journal --new        # 新日记本
0 habits --reset       # 重新开始习惯追踪

# 代码库归零（危险操作！）
0 repo --fresh-start   # 重新初始化Git（保留代码）
0 deps --reinstall     # 重新安装所有依赖
```

**空杯心态**
```bash
# 学习模式：清空预设
0 learn --beginner-mode
0 docs --from-scratch
```

---

## 特殊零概念

**零成本抽象**
```rust
// Rust理念：零成本抽象
// 高级语法不增加运行时开销
// "You don't pay for what you don't use"
```

**零拷贝**
```bash
# 数据传输不复制
sendfile()  # Linux零拷贝系统调用
splice()    # 管道间零拷贝
```

**零时区（UTC）**
```bash
date -u      # UTC时间
TZ=UTC date  # 明确指定
```

---

## 实用单行

```bash
# 零行数文件（创建）
> empty.txt

# 零宽度分隔符处理（awk）
awk -v RS='\0' '{print}' file  # NUL分隔

# 零文件大小检查
if [ ! -s file.txt ]; then echo "File is zero or empty"; fi

# 零退出码（成功）
true  # 返回0
echo $?  # 0

# 零延迟（立即）
sleep 0  # 瞬时完成
```

---

## 禁忌与警告

⚠️ **除以零** = 崩溃（数学与程序）
```bash
expr 10 / 0  # 错误
echo $((10/0))  # Bash: floating exception
```

⚠️ **零指针** = Segmentation Fault
```c
int *p = NULL;
*p = 5;  // 崩溃！
```

⚠️ **零长度数组** = 未定义行为
```c
int arr[0];  // GCC扩展，标准不允许
```

---

## 文化Zero

**《从零开始的xxx》**
```bash
0 learn python --from-scratch    # 从零学Python
0 build app --zero-dependency    # 零依赖构建
0 deploy --bare-metal           # 裸金属部署（从零）
```

**零的象征意义**
- 道生一，一生二，二生三，三生万物 → **道 = 0**
- 空杯才能满 → **清空 = 0**
- 无限循环 → **∞ = 0 + ∞**
- 二进制基础 → **0和1构成万物**

---

## 彩蛋：零的其他读法

| 场景 | 读法 | 示例 |
|------|------|------|
| 数字 | zero | 0.5 (zero point five) |
| 电话 | oh | 555-0xxx (five five five oh xxx) |
| 温度 | nothing | 0°C (nothing degrees) |
| 代码 | null | null/None/undefined |
| 金融 | nought | £0 (nought pounds) |
| 体育 | love | 0-0 (love-love, 网球) |

---

> **0 是数字世界的奇点**。它既是最小，也是无限；既是虚无，也是全部。当你从零开始，你拥有所有的可能。

---

## 快速参考

```
0 init       # 初始化
0 reset      # 重置
0 clean      # 清空
0 default    # 恢复默认
0 check      # 零值检查
0 cycle      # 循环直到零
```

---

**最后一句**：  
> 最伟大的系统，往往从最简单的 **0** 开始。  
> 学会归零，才能超越零。
