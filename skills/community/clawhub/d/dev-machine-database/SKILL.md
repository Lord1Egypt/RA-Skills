# 开发机数据库查询技能

## 功能
通过 SSH 连接到开发机 (datax)，查询 MySQL 数据库中的 dw 库

## 触发词
- "去草坪上 dw 库看一下"
- "开发机 MySQL 查询"
- "查询 dw 库的 [表名]"
- "草坪上的 MySQL dw 库"
- "datax 数据库查询"

## 配置信息

### 开发机配置
- **主机名**: `datax`
- **工作目录**: `/mnt/www`
- **数据库类型**: MySQL
- **数据库名**: `dw` (可能有多个：`dw`, `dw库`, `data_warehouse` 等)

### 数据库连接
```bash
# 连接方式
ssh datax "mysql -u [用户] -p[密码] [数据库名] -e 'SQL 语句'"

# 或者直接登录
ssh datax "mysql -h localhost -u [用户] -p[密码]"
```

## 使用示例

### 示例 1：查看表列表
**用户：** "去草坪上 dw 库看一下有哪些表"

**执行：**
```bash
ssh datax "mysql -h localhost -u [用户] -p[密码] dw -e 'show tables;'"
```

**回复：** 表列表

---

### 示例 2：查询用户数据
**用户：** "查看 dw 库的 tr_user 有哪些用户"

**执行：**
```bash
ssh datax "mysql -h localhost -u [用户] -p[密码] dw -e 'select * from tr_user limit 50;'"
```

**回复：** 用户列表表格

---

### 示例 3：查询表结构
**用户：** "tr_user 表结构是什么样的"

**执行：**
```bash
ssh datax "mysql -h localhost -u [用户] -p[密码] dw -e 'desc tr_user;'"
```

**回复：** 表结构详情

---

### 示例 4：统计信息
**用户：** "dw 库的 tr_user 表有多少条数据"

**执行：**
```bash
ssh datax "mysql -h localhost -u [用户] -p[密码] dw -e 'select count(*) from tr_user;'"
```

**回复：** 数据统计

---

## 数据库信息

### 可能的数据库名
| 数据库名 | 说明 |
|----------|------|
| `dw` | 数据仓库主库 |
| `dw库` | 中文别名 |
| `data_warehouse` | 英文全称 |
| `sg_alith_sync_fle_tra` | 泰国项目库 |

### 常见表
| 表名 | 说明 |
|------|------|
| `tr_user` | 用户表 |
| `tr_order` | 订单表 |
| `tr_store` | 门店表 |
| `tr_client` | 客户表 |

---

## 执行流程

1. **接收查询指令**
   - 解析用户意图
   - 提取数据库名、表名、查询条件

2. **构建 SQL 语句**
   - 根据意图生成对应 SQL
   - 添加 LIMIT 限制（默认 50 条）

3. **SSH 执行**
   - 连接到 datax 开发机
   - 执行 MySQL 查询
   - 获取结果

4. **格式化输出**
   - 表格形式展示
   - 添加统计信息
   - 发送到飞书

---

## 安全注意事项

1. **只读操作** - 只执行 SELECT 查询，不执行 INSERT/UPDATE/DELETE
2. **LIMIT 限制** - 默认 LIMIT 50，避免大数据量
3. **密码保护** - MySQL 密码不输出到日志
4. **权限控制** - 只查询授权的数据库和表

---

## 相关文件

- 技能位置：`~/.openclaw/workspace/skills/dev-machine-database/SKILL.md`
- 脚本位置：`~/.openclaw/workspace/skills/dev-machine-database/query_db.py`
- 配置位置：`~/.openclaw/workspace/TOOLS.md` (开发机配置)

---

## 更新日志

### 2026-03-04
- ✅ 创建技能
- ✅ 支持 MySQL 查询
- ✅ 集成飞书发送
- ✅ 支持多种触发词
