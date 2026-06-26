# FastAPI 开发最佳实践规范

## 1. 类型注解 (Type Hints)
- **Rule 1.1**: 所有函数签名必须添加完整的类型注解。
- **Rule 1.2**: Pydantic 模型字段必须显式声明类型。

## 2. 依赖注入 (Dependency Injection)
- **Rule 2.1**: 统一使用 `Annotated` 风格进行依赖注入。
  *Bad*: `def func(db: Session = Depends(get_db))`
  *Good*: `def func(db: Annotated[Session, Depends(get_db)])`

## 3. HTTP 接口规范
- **Rule 3.1**: 必须明确指定 `status_code` (默认 200 除外)。
- **Rule 3.2**: 必须包含 `summary`，建议包含 `description`。
- **Rule 3.3**: 错误响应使用 `HTTPException`，并指定合适的 4xx/5xx 状态码。

## 4. Pydantic 模型规范
- **Rule 4.1**: 模型字段需添加 `Field(..., description="...")` 说明。
- **Rule 4.2**: 合理使用 `Config` 类配置 schema 示例。

## 5. 项目结构建议
- 路由分离 (`routers/`)
- 模型分离 (`schemas/`, `models/`)
- 依赖分离 (`dependencies/`)