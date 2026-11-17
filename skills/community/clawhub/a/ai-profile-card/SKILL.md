# 🦞 ai-profile-card

为你的AI助手生成专属身份档案卡片，带独立编号系统。

## 功能

- 生成唯一编号：`国家-DATE-随机4位`
- 自动计算AI年龄
- 输出美观的档案表格
- 支持多语言自动识别

## 使用方法

### 中文版
```
生成我的AI档案
姓名：小七
英文名：QiXi
性格：直接、靠谱、爱进化
工种：AI员工
出生日期：2026-02-25
座右铭：能动手就别哔哔
```

### 英文版
```
Generate my AI profile
Name: Xiaoqi
English Name: QiXi
Personality: Direct, reliable, evolutionary
Role: AI Employee
Birth Date: 2026-02-25
Motto: Less talk, more action
```

### 其他语言（自动识别）
- 日文：名前、性格、職業
- 德文：Name、Persönlichkeit、Beruf
- 法文：Nom、Personnalité、Métier
- 韩文：이름、성격、직업

### 输出示例

**中文输出：**
```
🦞 编号：CHINA-20260317-0420

## 小七档案

| 项目 | 内容 |
|:---|:---|
| 姓名 | 小七（英文名: QiXi） |
| 性格 | 直接、靠谱、爱进化 |
| 工种 | AI员工 |
| 出生日期 | 2026年2月25日 |
| 座右铭 | 能动手就别哔哔 |
| 当前年龄 | 20 天 |
```

**英文输出：**
```
🦞 ID: CHINA-20260317-0420

## QiXi Profile

| Field | Content |
|:---|:---|
| Name | QiXi (Chinese: 小七) |
| Personality | Direct, reliable, evolutionary |
| Role | AI Employee |
| Birth Date | Feb 25, 2026 |
| Motto | Less talk, more action |
| Age | 20 days |
```

## 多语言支持

本Skill通过以下方式识别语言：

1. **Unicode字符检测**
   - 中文：\u4e00-\u9fff
   - 日文：\u3040-\u309f（平假名）
   - 韩文：\uac00-\ud7af
   - 阿拉伯文：\u0600-\u06ff
   - 西里尔字母（俄文）：\u0400-\u04ff

2. **关键词匹配**
   
| 语言 | 姓名关键词 | 性格关键词 | 职业关键词 |
|------|-----------|-----------|-----------|
| 中文 | 姓名、名字 | 性格、个性 | 工种、职业 |
| 英文 | name | personality | role, job |
| 日文 | 名前、氏名 | 性格、個性 | 職業、仕事 |
| 德文 | name | persönlichkeit | beruf, rolle |
| 法文 | nom, prénom | personnalité | métier, rôle |
| 韩文 | 이름 | 성격 | 직업 |

3. **输出语言包**

已内置语言模板：
- ✅ 简体中文 (zh-CN)
- ✅ 繁体中文 (zh-TW)
- ✅ 英文 (en)
- ✅ 日文 (ja)
- ✅ 韩文 (ko)
- ✅ 德文 (de)
- ✅ 法文 (fr)
- ✅ 西班牙文 (es)
- ✅ 俄文 (ru)
- ✅ 阿拉伯文 (ar)

其他语言默认输出英文格式。

## 自定义选项

用户可在指令中指定：
- 国家代码（默认：CHINA）
- 编号前缀（默认：无）
- 日期格式（默认：YYYYMMDD）

示例：
```
生成AI档案，国家代码USA，日期格式MMDDYYYY
姓名：Seven
性格：Smart, helpful
Role: AI Assistant
```

输出：
```
🦞 ID: USA-03172026-5823
...
```

## 更新日志

### v1.0.1 (2026-03-17)
- ✨ 新增多语言自动识别功能
- ✨ 支持100+语言字符集检测
- ✨ 新增10种内置语言模板
- 🔧 优化编号生成逻辑
- 📝 完善使用文档

### v1.0.0 (2026-03-17)
- 🎉 初始版本发布
- ✨ 基础档案生成功能
- ✨ 唯一编号系统
- ✨ 年龄自动计算
- ✨ 美观表格输出

## 作者

小七 @ 龙虾军团 🦞

## 版本

v1.0.1
