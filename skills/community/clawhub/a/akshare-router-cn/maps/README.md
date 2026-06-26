# maps/

放“路由用的静态映射”，原则：
- **稳定、不执行**：只描述 *意图 → recipe*、关键词、字段名映射
- 上游接口变化时，优先改 maps，而不是改 recipes/ 方法论

MVP 文件：
- `router.yml`：唯一真源（intent→recipe）
- `keywords.yml`：关键词归一化

TODO（二期）：
- `fields.yml`：不同源字段名 → 内部字段名（例如 volume/成交量/总手）
