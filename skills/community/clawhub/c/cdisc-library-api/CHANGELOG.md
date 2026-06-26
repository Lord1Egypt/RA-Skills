# CDISC Library API Skill 更新日志

## [1.0] 2026-03-08

### 新增
- ✅ 完整 CDISC Library API 客户端封装
- ✅ 认证管理（支持 TOOLS.md 和环境变量）
- ✅ 自动缓存（1 小时 TTL）
- ✅ 速率限制（100ms/请求）
- ✅ 错误处理和重试逻辑

### 命令（16 个）
- `products` - 产品列表
- `qrs` - QRS 量表查询（支持自动获取最新版）
- `items` - 量表项目查询
- `adam` - ADaM 查询
- `sdtm` - SDTM 查询
- `cdash` - CDASH 查询
- `ct-packages` - 受控术语包列表
- `root` - 根资源查询
- `docs` - 文档查询
- `rules` - 规则查询
- `search` - 跨类别搜索
- `compare` - 版本比较
- `export` - 导出 JSON/CSV
- `batch` - 批量查询
- `cache` - 缓存管理

### 资源
- SKILL.md - 完整使用说明
- README.md - 快速开始指南
- assets/quickref.md - 速查表
- queries.example.txt - 批量查询示例

### 测试状态
- ✅ API 连接测试通过
- ✅ QRS 量表查询测试通过（AIMS01 v2-0）
- ✅ 产品列表测试通过（6 个类别）
- ✅ 术语包列表测试通过（200 项）

### 已知问题
- 部分 API 端点结构与文档描述不同（已适配实际 API）
- CT 术语查询需要指定术语包（待完善）

---

## 待办事项
- [ ] 完善 CT 术语查询（支持按包查询代码表）
- [ ] 添加更多搜索功能（支持变量名搜索）
- [ ] 优化导出格式（支持 Excel）
- [ ] 添加单元测试
