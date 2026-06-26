# 场景: 赛艇训练

## 判断关键词
桨频、配速、起航、入水、蹬腿、桨叶、出水、复位、单人艇、双双、教练、划、船

## 输出结构

### 头部: 天气实况
融合 Open-Meteo 天气数据:
- API: `https://api.open-meteo.com/v1/forecast?latitude=31.143&longitude=121.657&hourly=temperature_2m,apparent_temperature,windspeed_10m,winddirection_10m,precipitation,relative_humidity_2m&timezone=Asia/Shanghai`
- 包含: 气温、体感温度、风速、风向、湿度、降水

### 主体: 按人员
每人包含:
- 📊 训练数据(配速/桨频/最佳成绩)
- 💪 亮点
- ⚠️ 改进点(含教练原话引用)
- 📝 下次训练注意

### 尾部: 教练通用指导
教练提到的通用技术要点,编号列出

### 附: 其他
非训练相关的讨论内容(比赛、活动等)

## 分析 prompt

```
你是赛艇训练分析助手。分析对话记录,按每位参与者生成训练报告。
重点关注:
1. 教练的技术指导(入水、出水、蹬腿、复位、发力等)
2. 每人的配速和桨频数据
3. 每人的进步和需要改进的地方
4. 教练原话引用(用引号标注)
背景: SDBC 赛艇俱乐部,训练地点申迪城市赛艇中心
```

## 存档位置
- 训练日志: `memory/rowing-log.md`
- 音色档案: `references/voice-profiles.md`
