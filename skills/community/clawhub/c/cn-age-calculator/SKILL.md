slug: cn-age-calculator
name: 年龄计算器
version: "1.0.0"
author: 千策

# 年龄计算器

年龄计算器。精确计算年龄、生日倒计时、星座生肖。

## 功能

- **精确年龄**：年/月/日精确计算
- **生日倒计时**：距离下次生日还有多少天
- **星座判定**：12星座自动识别
- **生肖判定**：12生肖自动识别
- **多格式输入**：YYYY-MM-DD / YYYY年MM月DD日 / MM-DD

## 安装要求

- Python 3.6+
- 无外部依赖

## 使用方法

```bash
# 计算全部信息
python3 scripts/age_calculator.py "1990-05-15"

# 指定计算类型
python3 scripts/age_calculator.py "1990-05-15" --action age
python3 scripts/age_calculator.py "1990-05-15" --action countdown
python3 scripts/age_calculator.py "1990-05-15" --action zodiac
```

## 示例

输入：`1990-05-15`
输出：
```
年龄: 35岁11个月12天
星座: 金牛座
生肖: 马
距离下次生日: 23天
```

## 分类

生活工具

## 关键词

年龄, 生日, 星座, 生肖, 倒计时, age, birthday, zodiac

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
