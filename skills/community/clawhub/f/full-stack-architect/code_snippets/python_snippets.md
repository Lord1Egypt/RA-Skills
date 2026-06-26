# Python 代码片段

## 1. 基础语法

### 1.1 基本数据结构

```python
# 列表
fruits = ['apple', 'banana', 'cherry']
print(fruits[0])  # 访问第一个元素
fruits.append('orange')  # 添加元素

# 字典
person = {
    'name': 'John',
    'age': 30,
    'city': 'New York'
}
print(person['name'])  # 访问值
person['job'] = 'Engineer'  # 添加键值对

# 集合
numbers = {1, 2, 3, 4, 5}
numbers.add(6)  # 添加元素

# 元组
coordinates = (10.0, 20.0)
print(coordinates[0])  # 访问元素
```

### 1.2 控制流

```python
# if-elif-else
x = 10
if x > 10:
    print('x is greater than 10')
elif x == 10:
    print('x is equal to 10')
else:
    print('x is less than 10')

# for 循环
for i in range(5):
    print(i)

# while 循环
count = 0
while count < 5:
    print(count)
    count += 1

# 列表推导式
squares = [x**2 for x in range(10)]
print(squares)

# 字典推导式
square_dict = {x: x**2 for x in range(5)}
print(square_dict)
```

## 2. 函数和类

### 2.1 函数定义

```python
def greet(name):
    """问候函数"""
    return f"Hello, {name}!"

# 调用函数
print(greet('Alice'))

# 默认参数
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet('Bob'))  # 使用默认问候语
print(greet('Charlie', 'Hi'))  # 自定义问候语

# 可变参数
def sum_numbers(*args):
    return sum(args)

print(sum_numbers(1, 2, 3, 4))

# 关键字参数
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="John", age=30, city="New York")
```

### 2.2 类定义

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."
    
    def celebrate_birthday(self):
        self.age += 1
        return f"Happy birthday! I'm now {self.age} years old."

# 创建实例
person = Person("Alice", 25)
print(person.greet())
print(person.celebrate_birthday())

# 继承
class Employee(Person):
    def __init__(self, name, age, job_title):
        super().__init__(name, age)
        self.job_title = job_title
    
    def greet(self):
        return f"Hello, my name is {self.name}, I'm {self.age} years old, and I work as a {self.job_title}."

employee = Employee("Bob", 30, "Engineer")
print(employee.greet())
```

## 3. 模块和包

### 3.1 创建和使用模块

```python
# mymodule.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# 使用模块
import mymodule
print(mymodule.add(5, 3))
print(mymodule.subtract(5, 3))

# 从模块中导入特定函数
from mymodule import add
print(add(10, 5))

# 导入所有函数
from mymodule import *
print(subtract(10, 5))
```

### 3.2 创建包

```
my_package/
├── __init__.py
├── module1.py
└── module2.py
```

```python
# __init__.py
from .module1 import add
from .module2 import multiply

# module1.py
def add(a, b):
    return a + b

# module2.py
def multiply(a, b):
    return a * b

# 使用包
import my_package
print(my_package.add(5, 3))
print(my_package.multiply(5, 3))

# 从包中导入
from my_package import add, multiply
print(add(10, 5))
print(multiply(10, 5))
```

## 4. 文件操作

### 4.1 读取文件

```python
# 读取整个文件
with open('example.txt', 'r') as file:
    content = file.read()
    print(content)

# 逐行读取
with open('example.txt', 'r') as file:
    for line in file:
        print(line.strip())

# 读取所有行到列表
with open('example.txt', 'r') as file:
    lines = file.readlines()
    print(lines)
```

### 4.2 写入文件

```python
# 写入文件（覆盖）
with open('example.txt', 'w') as file:
    file.write('Hello, World!\n')
    file.write('This is a test.\n')

# 追加到文件
with open('example.txt', 'a') as file:
    file.write('This is an additional line.\n')

# 读写模式
with open('example.txt', 'r+') as file:
    content = file.read()
    file.write('\nAppended content.')
```

## 5. 异常处理

```python
try:
    # 可能引发异常的代码
    result = 10 / 0
except ZeroDivisionError:
    # 处理特定异常
    print("Cannot divide by zero!")
except Exception as e:
    # 处理其他所有异常
    print(f"An error occurred: {e}")
else:
    # 没有异常时执行
    print("No error occurred.")
finally:
    # 无论是否有异常都会执行
    print("This will always execute.")

# 自定义异常
class CustomError(Exception):
    pass

def check_positive(number):
    if number <= 0:
        raise CustomError("Number must be positive")
    return number

try:
    check_positive(-5)
except CustomError as e:
    print(f"Custom error: {e}")
```

## 6. 数据科学和机器学习

### 6.1 NumPy 基础

```python
import numpy as np

# 创建数组
arr = np.array([1, 2, 3, 4, 5])
print(arr)

# 二维数组
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix)

# 数组操作
print(arr + 1)  # 加法
print(arr * 2)  # 乘法
print(np.mean(arr))  # 平均值
print(np.max(arr))  # 最大值
print(np.min(arr))  # 最小值

# 矩阵操作
print(matrix.shape)  # 形状
print(matrix.T)  # 转置
print(np.dot(matrix, matrix))  # 矩阵乘法
```

### 6.2 Pandas 基础

```python
import pandas as pd

# 创建数据框
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['New York', 'London', 'Paris']
}
df = pd.DataFrame(data)
print(df)

# 基本操作
print(df.head())  # 前几行
print(df.tail())  # 后几行
print(df.info())  # 信息
print(df.describe())  # 统计描述

# 选择数据
print(df['name'])  # 选择列
print(df.loc[0])  # 按标签选择行
print(df.iloc[0])  # 按位置选择行

# 过滤数据
filtered = df[df['age'] > 28]
print(filtered)

# 分组
grouped = df.groupby('city').mean()
print(grouped)

# 读取和写入文件
df.to_csv('data.csv', index=False)
df_read = pd.read_csv('data.csv')
print(df_read)
```

### 6.3 Scikit-learn 基础

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

# 创建示例数据
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# 分割数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建模型
model = LinearRegression()

# 训练模型
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)
print(f"Predictions: {y_pred}")
print(f"Actual: {y_test}")

# 评估
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# 模型参数
print(f"Coefficient: {model.coef_}")
print(f"Intercept: {model.intercept_}")
```

## 7. Web 开发

### 7.1 Flask 基础

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from API", "data": [1, 2, 3]})

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json()
    return jsonify({"message": "Data received", "data": data})

if __name__ == '__main__':
    app.run(debug=True)
```

### 7.2 FastAPI 基础

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/items/{item_id}')
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post('/items/')
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}

# 运行: uvicorn main:app --reload
```

### 7.3 Django 基础

```python
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def hello(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Hello, World!"})
    elif request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse({"message": "Data received", "data": data})

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello),
]
```

## 8. 数据库操作

### 8.1 SQLite

```python
import sqlite3

# 连接到数据库
conn = sqlite3.connect('example.db')
c = conn.cursor()

# 创建表
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# 插入数据
c.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
c.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 30))

# 提交更改
conn.commit()

# 查询数据
c.execute("SELECT * FROM users")
rows = c.fetchall()
for row in rows:
    print(row)

# 更新数据
c.execute("UPDATE users SET age = ? WHERE name = ?", (26, "Alice"))
conn.commit()

# 删除数据
c.execute("DELETE FROM users WHERE name = ?", ("Bob",))
conn.commit()

# 关闭连接
conn.close()
```

### 8.2 PostgreSQL

```python
import psycopg2

# 连接到数据库
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="myuser",
    password="mypassword"
)
c = conn.cursor()

# 创建表
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (id SERIAL PRIMARY KEY, name VARCHAR(255), age INTEGER)''')

# 插入数据
c.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Alice", 25))
c.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Bob", 30))

# 提交更改
conn.commit()

# 查询数据
c.execute("SELECT * FROM users")
rows = c.fetchall()
for row in rows:
    print(row)

# 关闭连接
conn.close()
```

### 8.3 MongoDB

```python
from pymongo import MongoClient

# 连接到 MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["users"]

# 插入文档
user1 = {"name": "Alice", "age": 25, "city": "New York"}
user2 = {"name": "Bob", "age": 30, "city": "London"}

# 插入单个文档
collection.insert_one(user1)

# 插入多个文档
collection.insert_many([user2])

# 查询所有文档
for user in collection.find():
    print(user)

# 查询特定文档
for user in collection.find({"age": {"$gt": 25}}):
    print(user)

# 更新文档
collection.update_one({"name": "Alice"}, {"$set": {"age": 26}})

# 删除文档
collection.delete_one({"name": "Bob"})

# 关闭连接
client.close()
```

## 9. 并发和异步

### 9.1 多线程

```python
import threading
import time

def print_numbers():
    for i in range(5):
        print(f"Number: {i}")
        time.sleep(1)

def print_letters():
    for letter in 'ABCDE':
        print(f"Letter: {letter}")
        time.sleep(1)

# 创建线程
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# 启动线程
thread1.start()
thread2.start()

# 等待线程完成
thread1.join()
thread2.join()

print("All threads completed")
```

### 9.2 异步编程

```python
import asyncio

async def print_numbers():
    for i in range(5):
        print(f"Number: {i}")
        await asyncio.sleep(1)

async def print_letters():
    for letter in 'ABCDE':
        print(f"Letter: {letter}")
        await asyncio.sleep(1)

async def main():
    # 并发执行两个协程
    await asyncio.gather(
        print_numbers(),
        print_letters()
    )

# 运行事件循环
asyncio.run(main())
print("All tasks completed")
```

## 10. 测试

### 10.1 使用 unittest

```python
import unittest

class TestMathFunctions(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)
        self.assertEqual(5 + 3, 8)
    
    def test_subtract(self):
        self.assertEqual(5 - 3, 2)
        self.assertEqual(10 - 5, 5)
    
    def test_multiply(self):
        self.assertEqual(2 * 3, 6)
        self.assertEqual(5 * 5, 25)

if __name__ == '__main__':
    unittest.main()
```

### 10.2 使用 pytest

```python
# test_math.py
def test_add():
    assert 1 + 1 == 2
    assert 5 + 3 == 8

def test_subtract():
    assert 5 - 3 == 2
    assert 10 - 5 == 5

def test_multiply():
    assert 2 * 3 == 6
    assert 5 * 5 == 25

# 运行: pytest test_math.py -v
```

## 11. 部署

### 11.1 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
```

### 11.2 云部署

```python
# AWS Lambda 函数
def lambda_handler(event, context):
    """Lambda function handler"""
    name = event.get('name', 'World')
    return {
        'statusCode': 200,
        'body': f'Hello, {name}!'
    }
```

## 12. 工具和库

### 12.1 常用库

```python
# 网络请求
import requests
response = requests.get('https://api.example.com')
print(response.json())

# 日期时间
from datetime import datetime, timedelta
now = datetime.now()
tomorrow = now + timedelta(days=1)
print(now.strftime('%Y-%m-%d %H:%M:%S'))

# 正则表达式
import re
pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
email = 'test@example.com'
if re.match(pattern, email):
    print('Valid email')

# 密码哈希
from passlib.hash import bcrypt
hashed_password = bcrypt.hash('mysecretpassword')
print(bcrypt.verify('mysecretpassword', hashed_password))

# JWT
import jwt
from datetime import datetime, timedelta

payload = {
    'user_id': 123,
    'exp': datetime.utcnow() + timedelta(hours=1)
}
token = jwt.encode(payload, 'secret_key', algorithm='HS256')
decoded = jwt.decode(token, 'secret_key', algorithms=['HS256'])
print(decoded)
```

## 13. 性能优化

### 13.1 列表操作优化

```python
# 避免频繁列表连接
# 不好的做法
result = []
for i in range(1000):
    result = result + [i]  # 每次都创建新列表

# 好的做法
result = []
for i in range(1000):
    result.append(i)  # 原地修改

# 列表推导式更高效
a = [i for i in range(1000)]

# 使用生成器节省内存
def generate_numbers(n):
    for i in range(n):
        yield i

for num in generate_numbers(1000):
    print(num)
```

### 13.2 字典操作优化

```python
# 避免重复键查找
# 不好的做法
if 'key' in my_dict:
    value = my_dict['key']
else:
    value = default_value

# 好的做法
value = my_dict.get('key', default_value)

# 使用 collections.defaultdict
from collections import defaultdict

# 自动处理不存在的键
counts = defaultdict(int)
for item in items:
    counts[item] += 1

# 使用 collections.Counter
from collections import Counter
counts = Counter(items)
```

## 14. 最佳实践

### 14.1 代码风格

```python
# PEP 8 风格

# 缩进：4个空格
def function_name(parameter1, parameter2):
    """函数文档字符串"""
    if parameter1 > parameter2:
        return parameter1
    else:
        return parameter2

# 命名规范
# 函数和变量：snake_case
user_name = "John"
def calculate_total():
    pass

# 类：CamelCase
class UserProfile:
    pass

# 常量：UPPER_CASE
MAX_RETRY = 3
```

### 14.2 错误处理

```python
# 具体异常处理
try:
    result = do_something()
except SpecificError as e:
    # 处理特定异常
    logger.error(f"Specific error: {e}")
except Exception as e:
    # 处理其他异常
    logger.error(f"Unexpected error: {e}")
else:
    # 无异常时执行
    process_result(result)
finally:
    # 清理资源
    cleanup()
```

### 14.3 日志记录

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

logger = logging.getLogger(__name__)

# 使用日志
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
```

*本代码片段库将持续更新，以反映 Python 的最新最佳实践和特性。*