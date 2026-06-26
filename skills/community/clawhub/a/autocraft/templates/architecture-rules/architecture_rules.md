# 架构规则规范

## 1. 单一职责原则（SRP）

### 1.1 文件职责定义
每个文件应只负责一个功能或一组紧密相关的功能：

| 文件类型 | 职责 | 示例 |
|----------|------|------|
| 路由文件 | HTTP请求/响应处理 | `user_router.py`, `product_router.py` |
| 服务文件 | 业务逻辑处理 | `user_service.py`, `product_service.py` |
| 数据访问文件 | 数据库操作 | `user_repository.py`, `product_repository.py` |
| 模型文件 | 数据模型定义 | `user.py`, `product.py` |
| 工具文件 | 公共函数/工具 | `utils.py`, `validators.py` |

### 1.2 违规示例
```python
# ❌ 错误：一个文件包含多个不相关功能
# data_processor.py - 包含数据上传、查询、存储、分析、报告功能
# 违反SRP原则

# ✅ 正确：拆分为多个职责单一的文件
# data_upload_router.py     - 数据上传功能
# data_query_service.py     - 数据查询功能  
# data_store_repository.py  - 数据存储功能
# data_analysis_service.py  - 数据分析功能
# report_generator.py       - 报告生成功能
```

### 1.3 文件大小限制
- **路由文件**：≤ 200行
- **服务文件**：≤ 300行
- **数据访问文件**：≤ 250行
- **模型文件**：≤ 150行
- **工具文件**：≤ 100行

**超过限制的处理**：
1. 检查是否违反SRP原则
2. 考虑拆分为多个文件
3. 提取公共功能到工具文件

## 2. 分层架构规范

### 2.1 标准分层结构
```
backend/
├── api/
│   └── routers/          # 路由层：HTTP请求/响应
│       ├── user_router.py
│       └── product_router.py
├── services/             # 服务层：业务逻辑
│   ├── user_service.py
│   └── product_service.py
├── repositories/         # 数据访问层：数据库操作
│   ├── user_repository.py
│   └── product_repository.py
├── models/               # 模型层：数据模型定义
│   ├── user.py
│   └── product.py
├── schemas/              # 模式层：Pydantic模型
│   ├── user.py
│   └── product.py
└── utils/                # 工具层：公共函数
    ├── validators.py
    └── helpers.py
```

### 2.2 各层职责

#### 路由层（routers/）
- ✅ 处理HTTP请求/响应
- ✅ 参数验证和转换
- ✅ 调用服务层方法
- ❌ 不包含业务逻辑
- ❌ 不直接操作数据库

#### 服务层（services/）
- ✅ 业务逻辑处理
- ✅ 数据验证和转换
- ✅ 事务管理
- ✅ 错误处理和日志记录
- ❌ 不处理HTTP请求
- ❌ 不直接操作数据库（通过数据访问层）

#### 数据访问层（repositories/）
- ✅ 数据库操作（CRUD）
- ✅ 查询构建
- ✅ 数据映射
- ❌ 不包含业务逻辑
- ❌ 不处理HTTP请求

#### 模型层（models/）
- ✅ SQLAlchemy模型定义
- ✅ 数据库表映射
- ✅ 关系定义
- ❌ 不包含业务逻辑

#### 模式层（schemas/）
- ✅ Pydantic模型定义
- ✅ 请求/响应数据验证
- ✅ 数据序列化/反序列化
- ❌ 不包含业务逻辑

## 3. 功能边界规范

### 3.1 模块依赖规则
```
路由层 → 服务层 → 数据访问层 → 模型层
    ↓         ↓         ↓
  模式层 ←────┴─────────┘
```

**允许的依赖方向**：
- 路由层可以依赖服务层和模式层
- 服务层可以依赖数据访问层和模式层
- 数据访问层可以依赖模型层
- 工具层可以被任何层依赖

**禁止的依赖**：
- ❌ 循环依赖
- ❌ 跨层直接调用（如路由层直接调用数据访问层）
- ❌ 服务层依赖路由层

### 3.2 耦合度控制
- **导入模块数量**：≤ 15个（单个文件）
- **函数参数数量**：≤ 5个
- **类方法数量**：≤ 20个
- **函数行数**：≤ 50行
- **嵌套深度**：≤ 3层

## 4. 代码结构检查清单

### 4.1 路由文件检查清单
- [ ] 只包含HTTP端点定义
- [ ] 不包含业务逻辑
- [ ] 使用依赖注入调用服务层
- [ ] 错误处理使用HTTPException
- [ ] 参数验证使用Pydantic模型
- [ ] 响应模型定义清晰

### 4.2 服务文件检查清单
- [ ] 业务逻辑清晰
- [ ] 错误处理完善
- [ ] 日志记录完整
- [ ] 事务管理正确
- [ ] 不包含HTTP相关代码
- [ ] 不直接操作数据库

### 4.3 数据访问文件检查清单
- [ ] 只包含数据库操作
- [ ] 查询构建正确
- [ ] 使用SQLAlchemy ORM
- [ ] 不包含业务逻辑
- [ ] 错误处理完善

## 5. 架构合理性验证标准

### 5.1 验证维度
| 维度 | 检查项 | 通过标准 |
|------|--------|----------|
| **文件职责单一性** | 文件是否只负责一个功能 | 无SRP违规 |
| **代码结构合理性** | 分层架构是否清晰 | 路由/服务/数据访问分离 |
| **功能边界分明性** | 模块依赖是否合理 | 无循环依赖，耦合度低 |
| **代码复杂度控制** | 文件大小/函数复杂度 | 符合限制标准 |

### 5.2 自动检查脚本
使用架构检查脚本：
```bash
python3 architecture_check.py --path /path/to/code --verbose
```

### 5.3 手动检查清单
1. **文件职责**：检查每个文件的功能是否单一
2. **分层结构**：检查代码是否在正确层级
3. **依赖关系**：检查模块依赖是否合理
4. **代码复杂度**：检查文件大小和函数复杂度

## 6. 重构指南

### 6.1 何时需要重构
- ✅ 文件超过行数限制
- ✅ 违反SRP原则（一个文件多个功能）
- ✅ 业务逻辑在路由文件中
- ✅ 循环依赖
- ✅ 高耦合度（导入过多模块）

### 6.2 重构步骤
1. **分析问题**：使用架构检查脚本识别问题
2. **设计新结构**：按照分层架构设计新结构
3. **逐步迁移**：逐步迁移代码，保持功能可用
4. **测试验证**：确保重构后功能正常
5. **清理旧代码**：删除旧文件，更新导入

### 6.3 重构示例
**重构前**：
```python
# data_processor.py（违反SRP）
class DataProcessor:
    def upload_data(): ...
    def query_data(): ...
    def store_data(): ...
    def analyze_data(): ...
    def generate_report(): ...
```

**重构后**：
```python
# data_upload_router.py
class DataUploadRouter:
    def upload_data(): ...

# data_query_service.py  
class DataQueryService:
    def query_data(): ...

# data_store_repository.py
class DataStoreRepository:
    def store_data(): ...

# data_analysis_service.py
class DataAnalysisService:
    def analyze_data(): ...

# report_generator.py
class ReportGenerator:
    def generate_report(): ...
```

## 7. 最佳实践

### 7.1 新模块创建流程
1. **确定职责**：明确模块的单一职责
2. **选择层级**：确定属于路由层/服务层/数据访问层
3. **创建文件**：使用模板创建文件
4. **编写代码**：遵循分层架构规范
5. **注册路由**：在main.py中注册路由
6. **编写测试**：编写单元测试和集成测试
7. **架构检查**：运行架构检查脚本

### 7.2 代码审查要点
- ✅ 文件职责是否单一
- ✅ 代码是否在正确层级
- ✅ 依赖关系是否合理
- ✅ 代码复杂度是否可控
- ✅ 错误处理是否完善
- ✅ 测试覆盖是否充分

### 7.3 持续维护
- **定期检查**：每月运行架构检查脚本
- **及时重构**：发现问题及时重构
- **团队培训**：确保团队成员理解架构规范
- **文档更新**：保持架构文档最新

## 8. 工具支持

### 8.1 架构检查脚本
```bash
# 基本检查
python3 architecture_check.py --path ./backend

# 生成详细报告
python3 architecture_check.py --path ./backend --report architecture_report.json

# 集成到CI/CD
python3 architecture_check.py --path ./backend --verbose
```

### 8.2 代码质量工具
- **pylint**：代码风格检查
- **flake8**：代码规范检查
- **mypy**：类型检查
- **bandit**：安全漏洞检查

### 8.3 模板文件
- `router_template.py`：路由文件模板
- `service_template.py`：服务文件模板
- `test_template.py`：测试文件模板
- `pytest.ini`：测试配置模板

## 9. 附录

### 9.1 常见问题

**Q：一个文件可以包含多个相关功能吗？**
A：可以，但必须是紧密相关的功能。例如，`user_service.py`可以包含用户相关的所有业务逻辑，但不能包含订单或产品逻辑。

**Q：工具函数应该放在哪里？**
A：公共工具函数放在`utils/`目录，模块特定的工具函数可以放在模块内部。

**Q：如何判断是否需要拆分文件？**
A：如果文件超过行数限制，或者包含多个不相关的功能，或者难以维护，就应该考虑拆分。

### 9.2 参考资源
- [单一职责原则（SRP）](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- [分层架构模式](https://en.wikipedia.org/wiki/Multitier_architecture)
- [FastAPI最佳实践](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [SQLAlchemy ORM指南](https://docs.sqlalchemy.org/en/14/orm/)

---

**版本**：v1.0  
**更新日期**：2026-05-08  
**维护者**：皮皮虾 🦐