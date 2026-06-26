slug: cn-random-picker
name: 随机选择器
version: "1.0.0"
author: 千策

# 随机选择器

随机选择器。抽奖抽签神器。

## 功能

- **随机抽取**：从多个选项中随机选一个
- **多人抽取**：一次抽取多个不重复结果
- **权重模式**：每个选项可设置不同权重
- **去重保证**：已抽中的不会重复抽到
- **公平模式**：使用secrets模块确保密码学安全随机

## 安装要求

- Python 3.6+
- 无外部依赖

## 使用方法

```bash
# 基本随机选择
python3 scripts/random_picker.py "张三,李四,王五,赵六"

# 抽取多个
python3 scripts/random_picker.py "A,B,C,D,E" --count 2

# 带权重
python3 scripts/random_picker.py "一等奖:1,二等奖:3,三等奖:6"
```

## 示例

输入：`张三,李四,王五`
输出：`🎉 抽中: 李四`

## 分类

生活工具

## 关键词

随机, 抽奖, 抽签, lottery, random, picker

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
