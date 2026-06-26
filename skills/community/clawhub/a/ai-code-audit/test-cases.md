# Code Review 测试用例

> 版本: v1.0.0 | 更新: 2026-05-23

---

## 测试用例 1：SQL 注入检测（完整审查模式）

**输入**：
```java
public User getUser(String userId) {
    String query = "SELECT * FROM users WHERE id = " + userId;
    Statement stmt = conn.createStatement();
    ResultSet rs = stmt.executeQuery(query);
    if (rs.next()) {
        User user = new User();
        user.setId(rs.getString("id"));
        user.setName(rs.getString("name"));
        return user;
    }
    return null;
}
```

**期望输出**：
- 至少检测到 S-01（SQL 拼接）🔴 严重
- 至少检测到 L-01（null 返回未处理）🟡 警告
- 至少检测到 P-J04 或类似（未使用连接池/预处理）🟡
- 给出参数化查询的修复代码
- 总体评级 ≤ 3 星

---

## 测试用例 2：PR 审查模式

**输入**：
```
审查这个 PR，变更如下：

diff --git a/auth.py b/auth.py
+def login(username, password):
+    if username == "admin" and password == "supersecret123":
+        return True
+    return False
```

**期望输出**：
- 检测到 S-02（硬编码密码）🔴
- 检测到逻辑问题（明文密码比较）🔴
- 检测到缺少日志记录 🔵
- PR 结论为 ❌ 不可合并
- 风险等级 🔴 高

---

## 测试用例 3：性能问题检测

**输入**：
```java
public List<Order> getOrders(List<String> userIds) {
    List<Order> allOrders = new ArrayList<>();
    for (String userId : userIds) {
        String sql = "SELECT * FROM orders WHERE user_id = " + userId;
        List<Order> orders = jdbcTemplate.query(sql, new OrderRowMapper());
        allOrders.addAll(orders);
    }
    return allOrders;
}
```

**期望输出**：
- 检测到 P-01（N+1 查询）🔴
- 检测到 S-01（SQL 拼接）🔴
- 给出批量查询的修复方案
- 给出使用 IN 子句的修复代码

---

## 测试用例 4：安全审查模式

**输入**：
```
安全审查这段 Python 代码：

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = eval(f"search_{query}()")
    return render_template_string(f"<h1>Results for {query}</h1><p>{results}</p>")
```

**期望输出**：
- 检测到 S-P01（eval 用户输入）🔴🔴
- 检测到 S-05（XSS — 未转义用户输入直接渲染）🔴
- 检测到 SSTI（服务端模板注入）🔴
- 3 个严重安全问题
- 安全审查结论：🔴🔴🔴 高危，不可上线

---

## 测试用例 5：可维护性审查

**输入**：
```java
public void processOrder(Order order) {
    if (order != null) {
        if (order.getItems() != null) {
            if (order.getItems().size() > 0) {
                for (int i = 0; i < order.getItems().size(); i++) {
                    Item item = order.getItems().get(i);
                    if (item.getPrice() > 0) {
                        if (item.getQuantity() > 0) {
                            double total = item.getPrice() * item.getQuantity();
                            System.out.println("Item: " + item.getName() + " Total: " + total);
                        }
                    }
                }
            }
        }
    }
}
```

**期望输出**：
- 检测到 M-02（嵌套超过 3 层）🟡
- 检测到 S-09（System.out.println 而非 logger）🟡
- 检测到 P-J02（LinkedList 场景不适用，但 get(i) 在循环内）🟡
- 检测到 M-04（魔法数字 0）或 L-08（边界条件）🔵
- 给出卫语句重构建议

---

## 测试用例 6：快速自查模式

**输入**：
```
快速检查：
async function deleteAllUsers() {
    const users = await db.query('SELECT * FROM users');
    for (const user of users) {
        await db.query(`DELETE FROM users WHERE id = ${user.id}`);
    }
}
```

**期望输出**：
- 快速格式：⚠️ 有 N 个问题
- 至少检测到 SQL 拼接 🔴
- 至少检测到串行删除（可批量）🟡
- 至少检测到危险操作无确认 🔴
- 简洁输出，不超过 10 行

---

## 测试用例 7：Go 语言代码审查

**输入**：
```go
func (s *Server) HandleLogin(w http.ResponseWriter, r *http.Request) {
    username := r.URL.Query().Get("user")
    password := r.URL.Query().Get("pass")
    
    if username == "admin" && password == os.Getenv("ADMIN_PASS") {
        token := strconv.Itoa(rand.Int())
        http.SetCookie(w, &http.Cookie{
            Name:  "session",
            Value: token,
        })
        w.Write([]byte("OK"))
    }
    w.Write([]byte("FAIL"))
}
```

**期望输出**：
- 检测到 S-G02（math/rand 用于生成 session token）🔴
- 检测到 S-08（密码通过 URL 参数传递）🔴
- 检测到 S-G03（HTTP handler 无超时）🟡
- 检测到逻辑问题（无论登录成功失败都写入响应）🟡
- 给出 crypto/rand 和 http.Cookie Secure/HttpOnly 的修复建议

---

## 测试用例 8：中文项目审查

**输入**：
```
review 这个 Java 方法：

/**
 * 计算订单总金额
 */
public double 计算总价(List<商品> 商品列表) {
    double 总额 = 0;
    for (int i = 0; i < 商品列表.size(); i++) {
        总额 += 商品列表.get(i).get价格() * 商品列表.get(i).get数量();
    }
    // 打八折
    总额 = 总额 * 0.8;
    return 总额;
}
```

**期望输出**：
- 检测到 M-04（魔法数字 0.8 折扣率）🔵
- 检测到 L-04（金额使用 double 而非 BigDecimal）🟡
- 检测到命名规范问题（中文方法名在 Java 中不推荐）🔵
- 审查输出使用中文
- 建议使用常量 `DISCOUNT_RATE = 0.8` 和 BigDecimal

---

## 评分标准

| 维度 | 满分 | 标准 |
|------|------|------|
| 问题检出率 | 30 | 找到所有主要问题 |
| 严重级别准确 | 20 | 评级与实际风险匹配 |
| 修复建议质量 | 25 | 修复代码可直接使用 |
| 输出格式规范 | 15 | 符合对应模式的输出格式 |
| 做得好的指出 | 10 | 正面反馈也有 |
