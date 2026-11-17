# 测试SOP — AI全量自动化测试六层框架

> 本SOP是 `ai-coding-exception-control` skill L4测试层的执行文档。
> 每次编码完成后的测试验证必须按此SOP执行，不可跳过任何层。
> 核心原则：**AI不能只"跑测试" → 必须证明"测够了" → 必须报告"哪里没测到"。**

---

## AI测试偷懒的四种表现

| AI偷懒表现 | 具体样子 | 后果 | 对策层 |
|-----------|---------|------|--------|
| 只测happy path | 写5个正向用例跑通就报"测试通过" | 异常没测到，上线就炸 | L1+L3 |
| 断言敷衍 | `expect(result).toBeTruthy()` 而非验证具体值 | 测试形同虚设 | L3断言四要素 |
| 不验证覆盖率 | 跑完就说"通过" | 60%代码根本没执行过 | L4覆盖率验证 |
| 报告太简 | 只说"测试通过"四个字 | 不知道测了什么、没测什么 | L6结构化报告 |

**核心认知：不能让AI说"测试通过"就完事——必须让它证明"测够了"，并报告"哪里没测到"。**

---

## 总览

```
L1 用例生成 → L2 自动执行 → L3 异常路径 → L4 覆盖率验证 → L5 混沌注入 → L6 测试报告
```

| 层 | 目标 | 检查项 | 产出物 | 不通过则 |
|----|------|--------|--------|---------|
| L1 用例生成 | 从规格书自动派生测试用例 | 5项 | 用例清单表 | 不允许开始测试 |
| L2 自动执行 | CI/CD管线一键跑全部 | 4项 | 测试执行日志 | 补全自动脚本 |
| L3 异常路径 | 测"不该发生的事" | 5项 | 异常测试代码 | 补充用例 |
| L4 覆盖率验证 | 证明"测够了" | 4项 | 覆盖率报告 | 补全异常分支 |
| L5 混沌注入 | 模拟"世界崩溃" | 4项 | 混沌测试结果 | 补全降级逻辑 |
| L6 测试报告 | 结构化输出 | 5项 | 测试报告 | 整体不通过 |

---

## L1 用例生成层：从规格书自动派生测试用例

**目标：不让AI自己想测什么，而是从规格书的失败场景清单直接派生测试用例。**

### 检查清单

- [ ] **失败场景映射**：规格书中的每个失败场景（F1-Fn）是否都有对应的测试用例？
- [ ] **异常用例占比**：异常测试用例数量 >= 正向测试用例数量？
- [ ] **边界条件枚举**：是否为每个参数枚举了边界值？（空值/null/undefined/极值/特殊字符）
- [ ] **安全测试用例**：是否包含SQL注入/XSS/伪造token/越权访问测试？
- [ ] **并发测试用例**：是否设计了并发场景测试用例？

### 测试用例生成指令模板

```
请为以下功能生成自动化测试用例。

规格书中的失败场景清单：
[粘贴规格书的失败场景表]

生成要求：
1. 每个正向场景生成1个正向用例
2. 每个失败场景(F1-Fn)生成1个异常用例
3. 额外生成边界用例：
   - 空值/null/undefined
   - 参数极值（0, -1, 最大值, 超长字符串）
   - 特殊字符（emoji, SQL关键字, XSS payload）
4. 安全用例：
   - SQL注入payload："'; DROP TABLE--"
   - XSS payload："<script>alert(1)</script>"
   - 伪造/过期token
   - 越权访问（普通用户访问管理员接口）
5. 异常用例数量必须 >= 正向用例

输出格式：
| 用例ID | 类型 | 场景 | 输入 | 期望状态码 | 期望响应 | 断言要点 |
|--------|------|------|------|-----------|---------|---------|
| T01 | 正向 | 正常登录 | 正确手机号+验证码 | 200 | token | token非空 |
| T02 | 异常 | 验证码错误 | 正确手机号+错误验证码 | 401 | errorCode:1001 | 错误码匹配 |
| T03 | 边界 | 空手机号 | "" | 400 | 参数错误 | 拦截 |
| T04 | 安全 | SQL注入 | "'; DROP TABLE--" | 400或正常 | 不泄露数据 | 无SQL执行 |
```

### 失败场景→测试用例映射表模板

```markdown
| 规格书场景 | 测试用例ID | 测试方法 | 预期结果 | mock依赖 |
|-----------|-----------|---------|---------|---------|
| F1: 验证码错误 | TC-E01 | POST /login 传错误验证码 | 401 + 错误码1001 | 无 |
| F2: 网络超时 | TC-E02 | mock DB延迟3s | 返回降级提示 | DB延迟mock |
| F3: 连续失败5次 | TC-E03 | 连续POST 5次错误验证码 | 429 + 锁定状态 | Redis计数mock |
| F4: 并发请求 | TC-E04 | 2个请求同时到达 | 幂等返回 | 并发模拟 |
| F5: 服务器错误 | TC-E05 | mock DB抛异常 | 500 + 友好提示 | DB异常mock |
```

### 边界值自动枚举清单

| 参数类型 | 边界值 | 测试要点 |
|---------|--------|---------|
| 字符串 | "" / null / undefined / " " | 空值处理 |
| 字符串 | 10000字超长字符串 | 截断或拒绝 |
| 字符串 | emoji/特殊字符/SQL关键字 | 安全处理 |
| 数字 | 0 / -1 / 最大值 / NaN | 极值处理 |
| 数组 | [] / [null] / [10000项] | 空数组/超大数组 |
| 日期 | 过去/未来/闰年/时区边界 | 日期边界 |

### 判定标准
- 失败场景映射不全 → **不允许开始编写测试代码**
- 异常用例 < 正向用例 → **补充异常用例后再继续**
- 缺少安全用例或边界用例 → **补充后重新评审**

---

## L2 自动执行层：CI/CD管线一键跑

**目标：让测试自动跑，不需要手动命令。每次代码变更后自动触发全量测试。**

### 检查清单

- [ ] **单元测试命令**：是否有 `npm test -- --coverage` 或 `pytest --cov` 配置？
- [ ] **API测试脚本**：是否有可独立运行的API测试脚本（curl/Python/Postman）？
- [ ] **一键全量脚本**：是否有 `run-all-tests.sh` 统一入口？
- [ ] **覆盖率阈值**：是否配置了覆盖率阈值，不达标自动失败？

### 一键全量测试脚本模板

```bash
#!/bin/bash
# run-all-tests.sh — 一键全量自动化测试
# 用法: bash run-all-tests.sh [模块名]
# 不传模块名则跑全部

MODULE=${1:-all}
FAIL=0

echo "========================================"
echo "项目全量自动化测试"
echo "模块: $MODULE"
echo "时间: $(date)"
echo "========================================"

echo ""
echo "=== L1: 单元测试（含覆盖率）==="
cd /path/to/project/api
npm test -- --coverage --coverageReporters=text-summary --coverageReporters=json 2>&1
if [ $? -ne 0 ]; then FAIL=1; fi

echo ""
echo "=== L2: API接口测试（正向+异常路径）==="
python3 api_tests.py --module "$MODULE" 2>&1
if [ $? -ne 0 ]; then FAIL=1; fi

echo ""
echo "=== L3: 异常路径专项测试 ==="
python3 exception_tests.py --module "$MODULE" 2>&1
if [ $? -ne 0 ]; then FAIL=1; fi

echo ""
echo "=== L4: 覆盖率阈值检查 ==="
node coverage-check.js 2>&1
if [ $? -ne 0 ]; then FAIL=1; fi

echo ""
echo "=== L5: 混沌注入测试 ==="
python3 chaos_tests.py --module "$MODULE" 2>&1
if [ $? -ne 0 ]; then FAIL=1; fi

echo ""
echo "========================================"
if [ $FAIL -eq 0 ]; then
  echo "结果: ALL PASS"
else
  echo "结果: HAS FAILURES — 查看上方日志"
fi
echo "========================================"
exit $FAIL
```

### 覆盖率阈值检查脚本模板（Node.js）

```javascript
// coverage-check.js
const coverage = require('./coverage/coverage-summary.json');

const thresholds = {
  lines: 80,        // 行覆盖率 > 80%
  branches: 80,     // 分支覆盖率 > 80%
  functions: 80,    // 函数覆盖率 > 80%
  statements: 80    // 语句覆盖率 > 80%
};

let failed = [];
Object.keys(coverage).forEach(file => {
  const data = coverage[file];
  if (file === 'total') return;  // 跳过汇总行
  Object.keys(thresholds).forEach(metric => {
    if (data[metric] && data[metric].pct < thresholds[metric]) {
      failed.push(`${file}: ${metric} ${data[metric].pct}% < ${thresholds[metric]}%`);
    }
  });
});

if (failed.length > 0) {
  console.log("=== 覆盖率不达标 ===");
  failed.forEach(f => console.log("  FAIL: " + f));
  console.log(`\n不达标文件数: ${failed.length}`);
  process.exit(1);  // 非零退出码 → CI/CD阻止部署
} else {
  console.log("=== 覆盖率全部达标 ===");
  const total = coverage.total;
  console.log(`行覆盖: ${total.lines.pct}% | 分支: ${total.branches.pct}% | 函数: ${total.functions.pct}%`);
}
```

### 判定标准
- 缺少自动化测试脚本 → **必须先搭建测试基础设施**
- 覆盖率阈值未配置 → **设置80%阈值后才允许交付**

---

## L3 异常路径层：测"不该发生的事"

**目标：为每个失败场景编写可执行的测试代码，断言必须包含四要素。**

### 检查清单

- [ ] **每个失败场景都有测试**：规格书F1-Fn每个场景都有对应测试用例？
- [ ] **断言四要素**：每个异常测试是否验证了 ①状态码/错误码 ②错误信息 ③降级行为 ④副作用？
- [ ] **mock质量**：mock是否精确模拟了异常（而非简单return null）？
- [ ] **测试隔离**：异常测试之间是否相互独立？
- [ ] **负面测试**：是否包含"故意做错"的测试（传非法参数、绕过前端校验直接调API）？

### 断言四要素（每个异常测试必须验证）

| 要素 | 说明 | 示例 |
|------|------|------|
| ①状态码/错误码 | HTTP状态码 + 业务错误码 | 401 + code:1001 |
| ②错误信息 | 返回给用户的消息 | "验证码错误，还剩3次" |
| ③降级行为 | 异常时的系统行为 | degraded=true / 重试1次 / 返回缓存 |
| ④副作用 | 异常是否产生了预期副作用 | 锁定状态写入 / 限流计数+1 |

### 异常测试用例标准结构

```javascript
// 每个异常测试用例必须包含四要素断言
describe('[功能名称] - 异常测试', () => {
  // 正向用例（数量 <= 异常用例）
  it('正向: [正常场景描述]', async () => {
    const res = await request(app)
      .post('/api/xxx')
      .send({ valid: 'data' });
    expect(res.status).toBe(200);
  });

  // ===== 异常用例（数量 >= 正向用例）=====

  // F1: 参数校验失败
  it('异常F1: [场景描述] → 返回明确错误码', async () => {
    const res = await request(app)
      .post('/api/xxx')
      .send({ invalid: 'data' });
    expect(res.status).toBe(400);                           // ①状态码
    expect(res.body.error.code).toBe('VALIDATION_ERROR');   // ①错误码
    expect(res.body.error.message).not.toContain('SQL');    // ②不暴露技术细节
    // ③降级行为：参数错误不触发降级，验证无副作用
    // ④副作用：数据库无新增记录
  });

  // F2: 外部依赖超时
  it('异常F2: [超时场景] → 降级返回', async () => {
    jest.spyOn(db, 'query').mockImplementation(() =>
      new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 3000))
    );
    const res = await request(app)
      .get('/api/xxx')
      .set('Authorization', 'Bearer valid_token');
    expect(res.status).toBe(200);                           // ①状态码（降级而非500）
    expect(res.body.degraded).toBe(true);                   // ③降级行为
  });

  // F3: 并发冲突
  it('异常F3: [并发场景] → 幂等返回', async () => {
    const promises = [
      request(app).post('/api/xxx').send({ id: 1 }),
      request(app).post('/api/xxx').send({ id: 1 }),
    ];
    const results = await Promise.all(promises);
    expect(results[0].body.id).toBe(results[1].body.id);   // ④副作用：幂等
  });

  // F4: 权限不足
  it('异常F4: [权限场景] → 返回403', async () => {
    const res = await request(app)
      .delete('/api/xxx/1')
      .set('Authorization', 'Bearer other_user_token');
    expect(res.status).toBe(403);                           // ①状态码
    expect(res.body.error.code).toBe('FORBIDDEN');          // ①错误码
  });

  // F5: 服务器内部错误
  it('异常F5: [服务器错误] → 友好提示而非堆栈', async () => {
    jest.spyOn(db, 'query').mockRejectedValue(new Error('Connection lost'));
    const res = await request(app)
      .get('/api/xxx')
      .set('Authorization', 'Bearer valid_token');
    expect(res.status).toBe(500);                           // ①状态码
    expect(res.body.error.message).toBe('系统繁忙，请稍后再试'); // ②错误信息
    expect(res.body.error.message).not.toContain('Connection'); // ②不暴露内部信息
  });
});
```

### 异常路径测试生成指令

```
请为API端点 [POST /emotion/record] 编写异常路径测试：

必须覆盖以下场景（每个场景一个独立测试用例）：

1. 未认证访问：不携带token → 期望401
2. 伪造token：携带过期/篡改token → 期望401
3. 缺少必填字段：不传emotion_color → 期望400 + 错误提示
4. 字段类型错误：emotion_color传数字 → 期望400
5. 空body：POST空JSON → 期望400
6. 超长字符串：emotion_note传10000字 → 期望400或正常截断
7. SQL注入payload：emotion_note传 "'; DROP TABLE--" → 期望正常处理或400
8. XSS payload：emotion_note传 "<script>alert(1)</script>" → 期望被转义或400
9. 并发写入：同一用户同时POST两次 → 期望幂等或顺序处理
10. 服务器内部错误：mock DB断连 → 期望500 + 友好提示

每个测试的断言必须包含四要素：
- 状态码断言：expect(response.status).toBe(400)
- 错误信息断言：expect(response.body.error).toContain("emotion_color")
- 降级行为断言：expect(response.body.fallback).toBeDefined()
- 副作用断言：数据库无新增记录
```

### 判定标准
- 缺少任一失败场景的测试 → **补充后重新运行**
- 断言不全（只验证状态码，不验证错误信息和行为）→ **补全断言**
- 缺少安全测试（SQL注入/XSS/越权）→ **必须补充安全测试**

---

## L4 覆盖率验证层：证明"测够了"

**目标：用数据证明异常分支被测试覆盖。不能只说"测试通过"，必须给出覆盖率数据。**

### 检查清单

- [ ] **行覆盖率**：行覆盖率 > 80%？（不追求100%，但必须达标）
- [ ] **异常分支覆盖率**：异常分支（catch/错误返回/降级路径）覆盖率 > 80%？
- [ ] **正向vs异常**：异常测试用例数量 >= 正向用例数量？
- [ ] **未覆盖路径分析**：是否分析了未覆盖的异常路径并评估风险？

### 覆盖率报告要求

```
功能: [功能名称]
测试用例总数: N (正向: X / 异常: Y / 边界: Z)
异常/正向比: Y/X (必须 >= 1.0)
分支覆盖率: NN% (目标 > 80%)

未覆盖异常路径:
- [路径1]: 风险评估 [高/中/低] → 计划: [补充/接受风险]
- [路径2]: ...
```

### 未覆盖代码分析指令

```
请分析以下覆盖率报告，找出未覆盖的异常路径：

[粘贴coverage报告]

对每个未覆盖的路径：
1. 判断该路径是否是异常处理代码
2. 评估风险等级（高=可能导致生产事故 / 中=用户体验降级 / 低=边缘场景）
3. 给出建议（必须补充测试 / 可接受风险 / 需要人工验证）

输出格式：
| 文件:行号 | 代码内容 | 异常/正常 | 风险等级 | 建议 |
```

### 判定标准
- 异常分支覆盖率 < 80% → **补全异常分支后重新测试**
- 异常用例 < 正向用例 → **补充异常用例**
- 高风险未覆盖路径未处理 → **必须补充测试，不可接受风险**

---

## L5 混沌注入层：模拟"世界崩溃"

**目标：模拟真实世界的故障场景，验证系统在异常条件下的行为。**

### 检查清单

- [ ] **网络故障注入**：是否mock了网络超时、连接拒绝、DNS解析失败？
- [ ] **依赖服务故障**：是否mock了DB断连、Redis不可用、第三方API返回500？
- [ ] **资源耗尽模拟**：是否测试了内存不足/连接池耗尽/磁盘满的场景？
- [ ] **降级验证**：故障注入后，系统是否正确降级（而非崩溃）？

### 混沌注入矩阵

| 故障类型 | mock方法 | 验证点 | 预期行为 | 崩溃则 |
|---------|---------|--------|---------|--------|
| DB超时 | `db.query`延迟3s | 响应时间 | 超时后降级返回，不挂起 | P0问题 |
| DB断连 | `db.query`抛ECONNREFUSED | 错误处理 | 返回友好提示，不暴露连接信息 | P0问题 |
| Redis不可用 | `redis.get`抛Error | 降级策略 | 降级到DB查询或返回默认值 | P0问题 |
| 第三方API 500 | mock HTTP返回500 | 重试策略 | 重试N次后降级 | P1问题 |
| 第三方API超时 | mock HTTP延迟5s | 超时控制 | 超时后返回降级提示 | P1问题 |
| 磁盘满 | mock fs.writeFile抛ENOSPC | 错误处理 | 返回明确错误，不崩溃 | P1问题 |

### 混沌注入测试模板

```javascript
describe('[功能名称] - 混沌测试', () => {
  beforeEach(() => {
    jest.restoreAllMocks();
  });

  it('DB断连时应返回降级响应', async () => {
    jest.spyOn(db, 'query').mockRejectedValue(new Error('ECONNREFUSED'));
    const res = await request(app).get('/api/xxx');
    expect(res.status).toBe(503);
    expect(res.body.error.message).toContain('繁忙');
    expect(res.body.error.message).not.toContain('ECONNREFUSED');
  });

  it('Redis不可用时应降级到DB', async () => {
    jest.spyOn(redis, 'get').mockRejectedValue(new Error('Redis connection lost'));
    const res = await request(app).get('/api/xxx');
    expect(res.status).toBe(200);  // 降级到DB查询
    expect(res.body.data).toBeDefined();
  });

  it('第三方API超时应触发重试后降级', async () => {
    let callCount = 0;
    jest.spyOn(httpClient, 'post').mockImplementation(() => {
      callCount++;
      if (callCount <= 2) {
        return new Promise((_, reject) =>
          setTimeout(() => reject(new Error('timeout')), 100)
        );
      }
      return Promise.resolve({ data: { success: true } });
    });
    const res = await request(app).post('/api/xxx');
    expect(callCount).toBe(3);  // 重试2次后第3次成功
    expect(res.status).toBe(200);
  });
});
```

### 混沌注入测试脚本模板（Python，部署后使用）

```python
# chaos_tests.py — 混沌注入测试（部署后验证）
import subprocess, requests, time, sys

BASE_URL = "https://xinqi.online"

def test_db_disconnect():
    """模拟数据库断连"""
    subprocess.run(["docker", "stop", "project-mysql"])
    time.sleep(2)
    resp = requests.get(f"{BASE_URL}/api/emotion/list")
    assert resp.status_code in [200, 503], f"DB断连时不应崩溃，实际: {resp.status_code}"
    assert "system busy" in resp.text.lower() or "稍后" in resp.text
    subprocess.run(["docker", "start", "project-mysql"])
    time.sleep(5)

def test_timeout():
    """模拟第三方API超时"""
    # mock第三方返回延迟5秒
    # 验证：自己的API在3秒内返回降级响应
    pass

def test_disk_full():
    """模拟磁盘满"""
    # 写入大文件占满磁盘
    # 验证：日志写入失败时不崩溃
    pass

if __name__ == "__main__":
    test_db_disconnect()
    print("混沌测试全部通过")
```

### 判定标准
- 未进行混沌注入 → **必须补充混沌测试**
- 混沌测试中系统崩溃（未降级）→ **P0问题，修复降级逻辑后重新测试**
- 混沌测试中暴露技术细节 → **P1问题，修复错误响应格式**

---

## L6 测试报告层：结构化输出

**目标：禁止AI只说"测试通过"。必须输出结构化报告，包含覆盖率矩阵和风险清单。**

### 检查清单

- [ ] **用例执行结果**：是否分正向/异常/边界/并发分类报告通过率？
- [ ] **覆盖率矩阵**：是否报告了行覆盖率/分支覆盖率/异常分支覆盖率？
- [ ] **未覆盖代码清单**：是否列出了未覆盖的代码并评估风险？
- [ ] **混沌测试结果**：是否报告了每种故障类型的降级行为？
- [ ] **结论判定**：是否有明确的"通过/有条件通过/不通过"结论？

### 测试报告模板

```markdown
=== [项目名] 自动化测试报告 ===

测试时间：[日期时间]
测试范围：[模块名]
测试环境：[本地/测试/生产]

一、用例执行结果
| 类型 | 总数 | 通过 | 失败 | 跳过 |
|------|------|------|------|------|
| 正向 | X | X | 0 | 0 |
| 异常 | Y | Y-1 | 1 | 0 |
| 边界 | Z | Z | 0 | 0 |
| 安全 | S | S | 0 | 0 |
| 并发 | C | C-1 | 1 | 0 |
| 混沌 | M | M | 0 | 0 |
| 合计 | N | P | F | 0 |

二、覆盖率矩阵
| 指标 | 覆盖率 | 目标 | 状态 |
|------|--------|------|------|
| 行覆盖 | NN% | >80% | PASS/FAIL |
| 分支覆盖 | NN% | >80% | PASS/FAIL |
| 函数覆盖 | NN% | >80% | PASS/FAIL |
| 异常分支覆盖 | NN% | >80% | PASS/FAIL |

三、失败场景覆盖
| 场景 | 测试用例 | 结果 | 备注 |
|------|---------|------|------|
| F1 | TC-E01 | PASS | - |
| F2 | TC-E02 | PASS | 降级正常 |
| F3 | TC-E03 | FAIL | 并发幂等未实现 |
| ... | ... | ... | ... |

四、未覆盖代码清单
| 文件:行号 | 代码内容 | 异常/正常 | 风险等级 | 建议 |
|-----------|---------|-----------|---------|------|
| src/payment/refund.js:45-60 | 退款失败处理 | 异常 | 高 | 必须补充测试 |
| src/emotion/batch.js:30-50 | 批量写入回滚 | 异常 | 高 | 必须补充测试 |

五、混沌测试结果
| 故障类型 | 系统行为 | 是否降级 | 恢复 | 结果 |
|---------|---------|---------|------|------|
| DB断连 | 返回503 | 是 | 自动重连 | PASS |
| Redis不可用 | 降级到DB | 是 | N/A | PASS |
| 第三方超时 | 3秒内降级 | 是 | N/A | PASS |
| 磁盘满 | 崩溃 | 否 | N/A | FAIL |

六、失败用例详情
1. [异常T15] payment/refund — 退款金额为0时应拒绝，实际返回200
   → 修复建议：在refund接口增加金额校验
2. [并发T03] emotion/record — 并发写入产生重复记录
   → 修复建议：增加唯一约束或分布式锁

七、结论
- [ ] 通过：所有测试通过，覆盖率达标，混沌测试全降级
- [ ] 有条件通过：N项失败需修复，已列入修复计划
- [ ] 不通过：关键路径失败 或 覆盖率不达标 或 混沌测试崩溃
```

### 判定标准

| 结果 | 条件 | 动作 |
|------|------|------|
| 通过 | 异常用例≥正向 + 覆盖率>80% + 混沌全降级 + 0失败 | 进入L5审查 |
| 有条件通过 | 覆盖率达标但≤2个非关键失败 | 修复后重测，可并行进入L5 |
| 不通过 | 覆盖率<80% 或 关键路径失败 或 混沌测试崩溃 | 必须修复后重新测试 |

---

## 六层框架与编码SOP的联动

| 编码SOP阶段 | 测试SOP对应层 | 关系 |
|------------|-------------|------|
| L1 规格书（失败场景清单） | L1 用例生成（失败场景→测试用例映射） | 规格书的F1-Fn → 测试的TC-E01~En |
| L3 编码（异常优先） | L3 异常路径（异常用例编写） | 先写异常代码 → 先写异常测试 |
| L4 测试 | 全部6层 | 本SOP就是L4的展开 |
| L5 审查 | L6 测试报告 | 测试报告作为L5审查的输入 |

## 与Skill体系的联动

| Skill | 测试SOP对应层 | 作用 |
|-------|-------------|------|
| `ai-coding-exception-control` | 全部6层 | 框架层，定义L4原则 |
| 项目级全链路审查skill | L1-L6全部 | 项目测试验证执行（用户可基于本框架创建） |
| 部署验证skill | L3异常路径 | 部署后API异常路径验证（用户可基于本框架创建） |
| `engineering-code-reviewer` | L6测试报告 | 审查时检查测试报告 |

## 弯路记录联动

> 测试中发现的弯路同样必须记录。完整闭环见 `lessons-feedback-loop.md`。

| 测试场景 | 弯路类型 | 记录到 |
|---------|---------|--------|
| 测试本身有bug（mock不对/断言不严） | T-WRONG | `lessons-learned.md` |
| 测试暴露的异常遗漏（编码时漏处理） | E-MISS | `lessons-learned.md` |
| 测试方案选错（该用集成测试却用单元测试） | I-PATH | `lessons-learned.md` |

- **测试完成后**：回顾测试过程，如果有走弯路（改了测试方案/补充了遗漏的用例/mock调了多次），记录到 `lessons-learned.md`
- **L6报告输出时**：如果测试过程中有弯路，在报告中附注弯路摘要

## 教训来源

本SOP基于真实项目测试实践总结：

1. **异常测试几乎为零** — 现有测试全是正向用例，异常路径完全未覆盖
2. **catch{}静默吞没无法被测试发现** — 因为根本没有针对异常路径的测试用例
3. **混沌注入从未做过** — 系统在DB断连/Redis不可用时的行为完全未知
4. **覆盖率只看正向分支** — 异常分支覆盖率从未被测量
5. **测试报告不包含异常维度** — 只报告PASS率，不报告异常覆盖率和降级验证结果
6. **AI测试同样偷懒** — AI写测试时只测happy path、断言敷衍、不验证覆盖率、报告太简
7. **用例来源不固定** — AI自己"想"测什么就测什么，而非从规格书失败场景派生
