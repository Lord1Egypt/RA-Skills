"""演示用：包含多种代码质量问题的 mock 文件。

此文件刻意构造了 SQL 注入、性能问题、安全漏洞和不良编码实践，
用于验证 code-review-gate Skill 的扫描能力。

请勿在生产环境或任何真实项目中使用此代码。
"""

import re


# ============================================================
# 1. SQL 注入漏洞
# ============================================================

def get_user_by_id_fstring(user_id):
    """f-string SQL 注入 - 应被 SecurityChecker 检测。"""
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return execute_query(query)


def get_user_by_concat(user_id):
    """字符串拼接 SQL 注入 - 应被 SecurityChecker 检测。"""
    query = "SELECT * FROM users WHERE id = " + user_id
    return execute_query(query)


def get_user_by_format(user_id):
    """.format() SQL 注入 - 应被 SecurityChecker 检测。"""
    query = "SELECT * FROM users WHERE id = {uid}".format(uid=user_id)
    return execute_query(query)


def get_user_by_percent(user_id):
    """% 格式化 SQL 注入 - 应被 SecurityChecker 检测。"""
    query = "SELECT * FROM users WHERE id = %s" % user_id
    return execute_query(query)


# ============================================================
# 2. 硬编码敏感信息
# ============================================================

API_KEY = "sk-abcdef1234567890ghijklmn"
PASSWORD = "super_secret_password_2024"
DATABASE_URL = "postgresql://admin:secret123@localhost/production"


def send_notification(token):
    """Token 硬编码 - 应被 SecurityChecker 检测。"""
    secret = "prod-token-8a7b6c5d4e3f"
    return {"auth": secret}


# ============================================================
# 3. 命令注入
# ============================================================

import os
import subprocess


def run_user_command(user_input):
    """命令注入 - os.system 拼接 - 应被 SecurityChecker 检测。"""
    os.system("echo " + user_input)


def run_dynamic_script(script_name):
    """命令注入 - eval - 应被 SecurityChecker 检测。"""
    eval(script_name + "()")


# ============================================================
# 4. 性能问题
# ============================================================

def find_duplicates_n2(items):
    """O(n²) 嵌套循环 - 应被 PerformanceChecker 检测。"""
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                duplicates.append(items[i])
    return duplicates


def get_orders_with_customers(order_ids):
    """N+1 查询 - 应被 PerformanceChecker 检测。"""
    results = []
    for order_id in order_ids:
        customer = db.query(f"SELECT * FROM customers WHERE order_id = {order_id}")
        results.append({"order_id": order_id, "customer": customer})
    return results


def unsafe_regex(user_input):
    """灾难性回溯正则是 - 应被 PerformanceChecker 检测。"""
    pattern = re.compile(r"(a+)+b")
    return pattern.match(user_input)


def read_large_file(path):
    """读取整个大文件到内存 - 应被 PerformanceChecker 检测。"""
    content = open(path).read()
    return content


# ============================================================
# 5. 错误处理问题
# ============================================================

def risky_operation():
    """裸 except + 吞异常 - 应被 FunctionalChecker 检测。"""
    try:
        result = 100 / 0
        items = [1, 2, 3]
        value = items[10]
    except:
        pass


def validate_form(request):
    """未验证的输入 - 应被 SecurityChecker 检测。"""
    user_id = request.args["user_id"]
    return int(user_id)


# ============================================================
# 6. 可读性问题
# ============================================================

def x(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x_val, y, z):
    """超长参数列表 + 无意义变量名 - 应被 ReadabilityChecker 检测。"""
    tmp = a + b
    data = tmp * c
    thing = data / d
    stuff = thing - e
    foo = stuff + f
    bar = foo * g
    baz = bar / h
    result = baz + tmp + data + thing + stuff + foo + bar
    return result


# ============================================================
# 7. 可维护性问题
# ============================================================

def handle_task(data):
    """print 代 logging + 硬编码配置 - 应被 MaintainabilityChecker 检测。"""
    print("Starting task...")
    print(f"Processing: {data}")
    timeout = 30
    max_retry = 5
    endpoint = "https://api.example.com/v2/tasks"
    print(f"Done. Timeout was {timeout}, retries: {max_retry}")
    return {"status": "ok", "endpoint": endpoint}


# ============================================================
# 8. 文档问题
# ============================================================

def undocumented_function(x, y):
    # TODO: maybe fix this later
    z = x + y
    # HACK: this is a workaround
    return z * 2


def poorly_commented(items):
    # set result to 0
    result = 0
    # loop through items
    for item in items:
        # add item to result
        result = result + item
    # return result
    return result


# ============================================================
# 辅助函数（mock）
# ============================================================

class FakeDB:
    def query(self, sql):
        return []


class FakeRequest:
    args = {}


db = FakeDB()
request = FakeRequest()


def execute_query(query):
    return []


if __name__ == "__main__":
    print("This is a mock file for testing code-review-gate.")
