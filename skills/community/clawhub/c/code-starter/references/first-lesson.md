# 第一课：猜数字游戏

最经典的编程入门项目，适合所有零基础学生。

---

## 项目介绍

**对学生说：**
```
我们来做一个猜数字游戏。

电脑想一个1到100的数字，你来猜。
猜大了，电脑说"大了"。
猜小了，电脑说"小了"。
猜对了，电脑说"恭喜你！"

这个游戏包含很多编程的核心思想：
- 存数据（变量）
- 判断（条件）
- 重复（循环）
- 随机性

准备好了吗？
```

---

## 完整代码

```python
import random

# 电脑想一个数字
number = random.randint(1, 100)

print("我想了一个1到100的数字，猜猜看！")

# 猜测次数
guesses = 0

while True:
    # 玩家猜
    guess = int(input("你猜几？"))
    guesses = guesses + 1
    
    # 判断
    if guess == number:
        print(f"对了！你用了{guesses}次猜中！")
        break
    elif guess > number:
        print("大了，再试试")
    else:
        print("小了，再试试")
```

---

## 分步教学

### Part 1: 让电脑想数字（5分钟）

**目标：** 理解变量和随机数

```python
import random
number = random.randint(1, 100)
print(number)
```

**讲解要点：**
- `import random` = 打开随机数工具箱
- `random.randint(1, 100)` = 随机选一个1到100的数
- `number = ...` = 把选中的数存进变量
- `print(number)` = 显示出来看看

**互动：**
```
运行几次看看，每次是不是不一样的数字？

这就是"随机"——电脑也不知道会选哪个。
```

---

### Part 2: 让玩家猜（5分钟）

**目标：** 理解输入和类型转换

```python
import random
number = random.randint(1, 100)

guess = int(input("你猜几？"))
print("你猜的是", guess)
```

**讲解要点：**
- `input("你猜几？")` = 显示问题，等待输入
- `int(...)` = 把输入的文字变成数字
- `guess = ...` = 把你猜的存进变量

**常见问题：**
```
Q: 为什么要用 int()？
A: input 得到的是文字，"5" 和 5 不一样。
   文字不能比较大小，所以要变成数字。
```

---

### Part 3: 判断对错（10分钟）

**目标：** 理解条件判断

```python
import random
number = random.randint(1, 100)

guess = int(input("你猜几？"))

if guess == number:
    print("对了！")
elif guess > number:
    print("大了")
else:
    print("小了")
```

**讲解要点：**
- `if` = 如果
- `==` = 等于（两个等号！）
- `elif` = 否则如果
- `else` = 否则
- 缩进很重要！

**互动：**
```
试着改成：
- 猜对显示"你真厉害"
- 猜错显示具体差多少

提示：abs(guess - number) 可以算差多少
```

---

### Part 4: 可以一直猜（10分钟）

**目标：** 理解循环

```python
import random
number = random.randint(1, 100)

while True:
    guess = int(input("你猜几？"))
    
    if guess == number:
        print("对了！")
        break
    elif guess > number:
        print("大了")
    else:
        print("小了")
```

**讲解要点：**
- `while True:` = 一直重复
- `break` = 跳出循环（猜对时停止）
- 注意缩进！

**互动：**
```
试玩一下。能猜对吗？

挑战：能在10次内猜对吗？
提示：每次猜中间的数字效率最高。
```

---

### Part 5: 记录猜测次数（5分钟）

**目标：** 理解变量更新

```python
import random
number = random.randint(1, 100)

guesses = 0  # 记录猜了几次

while True:
    guess = int(input("你猜几？"))
    guesses = guesses + 1
    
    if guess == number:
        print(f"对了！你用了{guesses}次")
        break
    elif guess > number:
        print("大了")
    else:
        print("小了")
```

**讲解要点：**
- `guesses = 0` = 初始化计数器
- `guesses = guesses + 1` = 每次加1
- `f"..."` = 格式化字符串，可以插入变量

---

## 挑战任务

### 初级
- [ ] 修改数字范围（1-1000？）
- [ ] 猜对后显示"太棒了！"而不是"对了！"
- [ ] 限制最多猜10次

### 中级
- [ ] 显示剩余次数
- [ ] 游戏结束后可以再玩一次
- [ ] 记录最好成绩（最少次数）

### 高级
- [ ] 选择难度（简单/中等/困难）
- [ ] 多人模式（轮流猜）
- [ ] 计时模式

---

## 常见错误处理

### 错误1：输入的不是数字
```
ValueError: invalid literal for int()
```

**解决：**
```python
try:
    guess = int(input("你猜几？"))
except:
    print("请输入数字！")
    continue
```

### 错误2：缩进不对
```
IndentationError: expected an indented block
```

**解决：**
```
检查 if/elif/else/while 下面的代码有没有缩进。
用4个空格或者Tab键。
```

---

## 课后思考

1. 电脑是怎么"想"数字的？
2. 为什么最多7次就能猜对？（二分法）
3. 如果要让游戏更难/更简单，可以怎么改？

---

## 扩展项目

完成猜数字后，可以尝试：

- **反向猜数字**：玩家想数字，电脑猜
- **猜词游戏**：猜单词而不是数字
- **21点游戏**：累计得分，不能超过21
- **文字冒险**：多分支的故事选择
