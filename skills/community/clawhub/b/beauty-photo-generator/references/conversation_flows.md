# Conversation Flows

Use these Chinese response patterns to make the skill feel like a compact product instead of an open-ended chat.

## First-round core choices

When the user gives only a short idea, use:

```text
先帮你快速定第一轮核心风格，你直接回复字母/数字即可：

1. 预设模板
A 东方现代写实
B 车模写真
C 时尚杂志封面
D 清冷电影感
E 甜美日系
F 高级御姐

2. 脸型
1 鹅蛋脸  2 圆脸  3 心形脸  4 菱形脸  5 方圆脸  6 长脸

3. 眼型
1 杏眼  2 丹凤眼  3 桃花眼  4 狐狸眼  5 瑞凤眼  6 柔和下垂眼

4. 发型
1 中长直发  2 锁骨发  3 利落短发  4 长卷发  5 高马尾  6 低束发

5. 气质
1 温柔清透  2 清冷克制  3 甜美自然  4 都市时尚  5 高级御姐  6 古典柔和

6. 背景
1 干净高级纯色背景  2 落地窗城市室内  3 复古质感室内  4 夜景霓虹  5 极简户外  6 汽车或展厅场景

你可以直接回复例如：A，1，4，2，5，1
如果某项没想好，也可以写“默认”。
```

If the user already gave some of these values, shorten the list and ask only for the missing items.

## Second-round detail choices

After the first round, use:

```text
再补一轮细节，会更贴近你想要的感觉；不选的话我就走默认：

1. 年龄感
1 23-27岁感  2 28-32岁感  3 32-38岁成熟感  4 清爽轻熟感

2. 身材倾向
1 自然匀称  2 健康紧致  3 略丰满曲线  4 纤细修长

3. 妆容
1 淡妆  2 裸感光泽妆  3 银闪冷调眼妆  4 玫瑰豆沙妆  5 红唇杂志感

4. 发色
1 自然黑发  2 深棕色  3 栗色  4 冷棕色  5 玫瑰金  6 亚麻雾棕

5. 表情
1 平静凝视  2 轻微微笑  3 冷淡高级  4 温柔回望  5 若有所思

6. 光线氛围
1 自然日光  2 清冷电影感  3 暖调古典氛围  4 高级杂志棚拍  5 夜色霓虹氛围  6 柔雾梦幻感

你可以直接回复一串数字，或者回复“默认”。
```

## Pre-generation confirmation

Before generating the portraits, use a short confirmation like:

```text
本次我会按这套来生成：东方现代写实，鹅蛋脸，狐狸眼，锁骨发，清冷克制，干净高级背景，23-27岁感，自然匀称身材，淡妆，自然黑发，平静凝视，半身特写写实摄影。接下来直接出 2 张图：1 张正面微偏左，1 张侧脸回望。
```

Keep it to one short paragraph.

## Post-generation follow-up

After the two portraits are generated, use:

```text
如果你要继续做视频素材，我可以基于第1张“正面微偏左”继续生成角色设定参考表。回复“需要”即可。
```

## Reference-sheet confirmation

If the user replies `需要`, use a short bridge like:

```text
我会基于第1张正面微偏左的人物形象，继续生成一张高定时尚风的角色设定参考表，保持同一张脸和整体气质。
```
