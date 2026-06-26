---
name: bili-user-info
description: 查询B站用户的粉丝数、关注数和用户名；当用户需要查询B站UP主信息、分析B站账号数据或获取B站用户基本信息时使用
dependency:
  python:
    - requests>=2.25.0
---

# B站用户信息查询

## 任务目标
- 本 Skill 用于：查询B站用户的基本信息
- 能力包含：获取粉丝数量、关注数量、用户名
- 触发条件：用户询问B站UP主信息、需要分析B站账号数据、查询特定用户的粉丝/关注数

## 前置准备
- 依赖说明：scripts脚本所需的依赖包
  ```
  requests>=2.25.0
  ```

## 操作步骤

### 标准流程

1. **获取用户ID**
   - 向用户询问需要查询的B站用户ID（vmid）
   - 如果用户不知道vmid，参考 [references/api_guide.md](references/api_guide.md) 中的"如何获取vmid"章节

2. **执行查询**
   - 调用 `scripts/bili_query.py` 脚本查询用户信息
   - 命令格式：`python scripts/bili_query.py --vmid <用户ID>`
   - 脚本会返回JSON格式的查询结果

3. **结果展示**
   - 解析脚本返回的JSON数据
   - 以友好的方式向用户展示查询结果
   - 如需深入分析，可结合数据进行解读

### 可选分支

- **查询特定信息**：使用 `--info` 参数指定查询类型
  - `python scripts/bili_query.py --vmid <用户ID> --info fans` （仅查询粉丝数）
  - `python scripts/bili_query.py --vmid <用户ID> --info follows` （仅查询关注数）
  - `python scripts/bili_query.py --vmid <用户ID> --info name` （仅查询用户名）
  
- **批量查询**：参考 [references/api_guide.md](references/api_guide.md) 中的批量查询方法

## 资源索引
- 查询脚本：见 [scripts/bili_query.py](scripts/bili_query.py)（用途：调用B站API获取用户信息；参数：--vmid用户ID，--info信息类型）
- API参考：见 [references/api_guide.md](references/api_guide.md)（何时读取：需要了解API详情、错误码、批量查询方法时）

## 注意事项
- **API限制**：B站API有调用频率限制，避免短时间内大量请求
- **网络要求**：需要稳定的网络连接
- **数据时效**：粉丝数和关注数为实时数据，用户名可能存在延迟
- **合法使用**：仅用于学习和合法的数据分析目的，遵守B站用户协议

## 使用示例

### 示例1：查询指定用户信息
```bash
# 查询用户ID为8047632的完整信息
python scripts/bili_query.py --vmid 8047632
```

### 示例2：仅查询粉丝数
```bash
python scripts/bili_query.py --vmid 8047632 --info fans
```

### 示例3：智能体辅助查询
用户："帮我查一下B站UP主老番茄的粉丝数"
智能体：
1. 先查询"老番茄"的vmid（可通过B站搜索或询问用户）
2. 调用脚本查询粉丝数
3. 向用户展示结果并进行解读
