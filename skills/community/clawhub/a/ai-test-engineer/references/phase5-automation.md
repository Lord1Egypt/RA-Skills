# Phase 5: 自动化测试 (6 Modules)

---

## M31: 自动化测试框架搭建

### 核心方法论
**选型决策 → 分层架构 → 脚手架搭建 → CI集成**

### 专家操作流程
1. **框架选型决策矩阵**：
   | 维度 | 权重 | Selenium | Playwright | Cypress | pytest+requests | RestAssured |
   |------|------|----------|------------|---------|-----------------|-------------|
   | 浏览器支持 | 15% | 全浏览器 | 全浏览器 | Chromium系 | N/A | N/A |
   | 执行速度 | 15% | 中 | 快 | 快 | 很快 | 中 |
   | 调试能力 | 10% | 一般 | 强(trace viewer) | 强(time travel) | 强(pdb) | 一般 |
   | 社区生态 | 10% | 最大 | 快速增长 | 大 | 大 | 大(Java生态) |
   | 学习曲线 | 10% | 陡 | 平缓 | 平缓 | 平缓 | 平缓 |
   | API测试 | 15% | 弱 | 中 | 弱 | 强 | 强 |
   | CI集成 | 10% | 好 | 好 | 好 | 好 | 好 |
   | 移动端 | 10% | Appium | 实验性 | 不支持 | N/A | N/A |
   | 许可 | 5% | 开源 | 开源 | 开源 | 开源 | 开源 |
2. **分层架构设计**：
   ```
   ├── tests/                    # 测试用例层
   │   ├── api/                  # API测试
   │   ├── web/                  # Web UI测试
   │   └── mobile/               # 移动端测试
   ├── pages/                    # Page Object层
   ├── apis/                     # API Client层
   ├── fixtures/                 # 测试数据层
   │   ├── data/                 # 测试数据文件(JSON/YAML/CSV)
   │   └── factories/            # 数据工厂
   ├── utils/                    # 工具层
   │   ├── db_helper.py          # 数据库操作
   │   ├── api_helper.py         # API通用方法
   │   └── report_helper.py      # 报告生成
   ├── config/                   # 配置层
   │   ├── env/                  # 环境配置(dev/staging/prod)
   │   └── global_config.yaml    # 全局配置
   ├── conftest.py               # pytest fixture定义
   ├── requirements.txt          # 依赖
   └── pytest.ini                # pytest配置
   ```
3. **脚手架搭建清单**：
   - [ ] 目录结构创建
   - [ ] 依赖安装与锁定（requirements.txt + 版本号）
   - [ ] 配置文件模板（多环境）
   - [ ] 基础Fixture定义（driver/session/数据库连接）
   - [ ] 日志配置（控制台+文件+分级）
   - [ ] 报告配置（Allure/HTML/JSON）
   - [ ] 示例用例（示范正确写法）
   - [ ] README（环境准备 + 运行命令 + 贡献规范）
   - [ ] pre-commit hook（代码格式检查）

---

## M32: UI自动化测试

### 核心方法论
**Page Object Model** + **智能等待** + **失败截图** + **自愈定位器**

### 专家操作流程
1. **Page Object设计原则**：
   - 一个页面/组件 → 一个Page Object类
   - 定位器集中在类的顶部
   - 操作方法返回Page Object（链式调用）或断言结果
   - 不在Page Object中放断言逻辑（断言在测试用例中）
2. **定位器优先级**：
   1. data-testid / data-cy（最稳定，推荐开发预埋）
   2. 语义化CSS选择器（role/aria-label/placeholder）
   3. 文本内容（getByText/getByRole）
   4. CSS选择器（class/id，注意不要依赖动态class名）
   5. XPath（最后选择，最脆弱）
3. **智能等待策略**：
   - 显式等待 > 隐式等待 > 固定sleep
   - 等待条件：元素可见/可点击/文本出现/元素消失/网络空闲
   - 超时配置：默认10s，特殊场景30s
4. **失败处理**：
   - 自动截图（失败时保存全屏截图+元素截图）
   - 自动录屏（Playwright trace viewer）
   - 自动重试（最多2次，标记retry）
   - 保留DOM snapshot用于离线分析
5. **跨浏览器/跨平台执行**：
   ```python
   # Playwright示例
   browsers = [
       {"name": "chromium", "viewport": {"width": 1920, "height": 1080}},
       {"name": "firefox", "viewport": {"width": 1366, "height": 768}},
       {"name": "webkit", "viewport": {"width": 375, "height": 812}},
   ]
   ```

---

## M33: 接口自动化测试

### 核心方法论
**契约测试** + **数据驱动** + **断言链** + **Schema校验**

### 专家操作流程
1. **API Client封装**：
   ```python
   class APIClient:
       """封装requests，提供统一接口调用能力"""
       def __init__(self, base_url, token=None):
           self.base_url = base_url
           self.session = requests.Session()
           if token:
               self.session.headers.update({"Authorization": f"Bearer {token}"})

       def get(self, path, **kwargs): ...
       def post(self, path, **kwargs): ...
       # 内置：超时、重试、日志、响应时间记录
   ```
2. **数据驱动测试**：
   ```python
   @pytest.mark.parametrize("test_case", load_test_data("user_api.yaml"))
   def test_user_api(test_case):
       response = client.request(
           method=test_case["method"],
           path=test_case["path"],
           params=test_case.get("params"),
           json=test_case.get("body"),
       )
       # 1. 状态码断言
       assert response.status_code == test_case["expected_status"]
       # 2. Schema断言
       validate(instance=response.json(), schema=test_case["expected_schema"])
       # 3. 业务断言
       for key, value in test_case["expected_values"].items():
           assert get_nested_value(response.json(), key) == value
   ```
3. **断言链设计**：
   - L1 - 状态码断言（最快失败）
   - L2 - 响应头断言（Content-Type/CORS头）
   - L3 - Schema断言（JSON Schema/OpenAPI校验）
   - L4 - 业务数据断言（字段值/计算正确性）
   - L5 - 副作用断言（数据库变更/消息队列/缓存）
4. **契约测试**：
   - Consumer端：定义期望的请求和响应格式
   - Provider端：验证实际接口是否符合契约
   - Pact工具链：Consumer → Pact Broker → Provider

---

## M34: CI/CD测试集成

### 核心方法论
**Pipeline设计** + **质量门禁** + **并行策略** + **环境管理**

### 专家操作流程
1. **Pipeline阶段设计**：
   ```
   Commit Push → Lint & Format → Unit Test → Build → 
   API Test → UI Test → Performance Smoke → Security Scan → Quality Gate
   ```
2. **测试分层与执行策略**：
   | 阶段 | 触发条件 | 超时 | 失败策略 |
   |------|---------|------|---------|
   | Lint | 每次Push | 2min | 阻塞 |
   | Unit Test | 每次Push | 5min | 阻塞 |
   | API Test | Push/PR | 15min | 阻塞 |
   | UI Smoke | PR | 15min | 阻塞 |
   | UI Full | Nightly | 2h | 告警 |
   | Performance | Nightly/Release | 30min | 告警（阈值） |
   | Security | Release | 15min | 阻塞（高危） |
3. **质量门禁（Quality Gate）**：
   - [ ] 代码覆盖率不低于XX%（新代码覆盖率不低于YY%）
   - [ ] 无P0/P1未解决缺陷
   - [ ] API测试通过率100%
   - [ ] UI关键路径100%通过
   - [ ] 性能指标未退化>10%
   - [ ] 安全扫描无High/Critical漏洞
4. **并行执行策略**：
   - 按模块分组并行（user测试组 + order测试组）
   - 按浏览器分组并行（Chrome组 + Firefox组）
   - 按数据分片（1/N数据量给每个并行worker）
   - 注意：确保测试间完全独立，无共享状态

---

## M35: 自动化脚本维护

### 核心方法论
**自愈机制** + **参数化** + **模块化** + **定期清理**

### 专家操作流程
1. **脚本腐烂原因与对策**：
   | 腐烂原因 | 频次 | 对策 |
   |---------|------|------|
   | UI元素定位器变化 | 最高 | data-testid + 自愈定位器策略 |
   | 测试数据过期 | 高 | 用例前置中动态创建数据 |
   | 环境变化 | 中 | 配置外部化 + 环境健康检查 |
   | 业务逻辑变更 | 中 | 需求变更联动脚本更新 |
   | 第三方服务不稳定 | 中 | Mock/Stub + 超时重试 |
2. **定位器自愈策略**：
   - 主定位器失败 → 依次尝试备选定位器
   - 实时记录定位器失败率，高失败率定位器标记待修复
   - AI辅助：根据当前DOM结构推断新定位器
3. **定期维护清单**（每迭代/每版本）：
   - [ ] 删除废弃的用例（不再需要的功能）
   - [ ] 更新过期的测试数据
   - [ ] 检查并修复Flaky测试（失败率>5%）
   - [ ] 更新框架/依赖库版本
   - [ ] 优化执行速度（移除不必要的等待/断言）

---

## M36: 自动化执行与调度

### 核心方法论
**分布式执行** + **重试机制** + **资源管理** + **结果汇聚**

### 专家操作流程
1. **执行触发策略**：
   - 事件触发：代码Push → 运行冒烟套件
   - 定时触发：每日凌晨 → 全量回归
   - 手动触发：发布前 → 全量验证
   - 条件触发：依赖服务就绪 → 集成测试
2. **Flaky测试管理**：
   - 自动识别：连续3次执行中至少1次失败的用例
   - 自动隔离：移入Quarantine套件，不影响主流水线
   - 自动重试：Flaky用例最多重试2次
   - 人工修复：每周审查Quarantine套件，修复或删除
3. **资源管理**：
   - Selenium Grid / Playwright Service / BrowserStack 管理浏览器实例
   - 并发数 = min(可用实例数, CPU核数×2)
   - 用例排队 + 动态扩容
4. **结果汇聚与通知**：
   - 测试报告：Allure Report 自动发布
   - 通知渠道：企业微信/钉钉/飞书/Slack → 推送关键摘要
   - 通知内容：通过率 + 失败用例Top3 + 执行时间趋势
