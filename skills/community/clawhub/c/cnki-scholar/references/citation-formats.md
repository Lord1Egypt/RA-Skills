# 引用格式模板

## APA 7th 格式

### 期刊论文
```
作者1, 作者2, & 作者3. (年份). 论文标题. 期刊名, 卷(期), 页码. DOI
```

示例：
```
Ge, X., & Han, Q.-L. (2017). Distributed formation control of networked 
multi-agent systems using a dynamic event-triggered communication mechanism. 
IEEE Transactions on Industrial Electronics, 64(9), 7731-7740. 
https://doi.org/10.1109/tie.2017.2701778
```

### 作者规则
- 1-20位作者：全部列出
- 21位以上：前19位 + ... + 最后一位
- 中国作者：姓在前，名缩写
  - 正确：Li, X., & Wang, Y.
  - 错误：Xiaoduo Li, Yi Wang

### 多作者格式
- 2位：Author1, & Author2.
- 3位以上：Author1, Author2, & Author3.

## GB/T 7714 格式（中国标准）

### 期刊论文 [J]
```
[序号] 作者. 题名[J]. 刊名, 年, 卷(期): 起止页码.
```

示例：
```
[1] GE X, HAN Q L. Distributed formation control of networked multi-agent 
systems using a dynamic event-triggered communication mechanism[J]. IEEE 
Transactions on Industrial Electronics, 2017, 64(9): 7731-7740.
```

### 学位论文 [D]
```
[序号] 作者. 题名[D]. 保存地点: 保存单位, 年份.
```

### 会议论文 [C]
```
[序号] 作者. 题名[C]//会议名称. 出版地: 出版者, 年: 页码.
```

## BibTeX 格式

```bibtex
@article{ge2017distributed,
  author  = {Ge, Xiaohua and Han, Qing-Long},
  title   = {Distributed Formation Control of Networked Multi-Agent Systems 
             Using a Dynamic Event-Triggered Communication Mechanism},
  journal = {IEEE Transactions on Industrial Electronics},
  year    = {2017},
  volume  = {64},
  number  = {9},
  pages   = {7731--7740},
  doi     = {10.1109/tie.2017.2701778}
}
```

### BibTeX Key 命名规则
```
姓氏年份关键词
ge2017distributed
li2018event
```

## RIS 格式（EndNote/Zotero）

```
TY  - JOUR
AU  - Ge, Xiaohua
AU  - Han, Qing-Long
TI  - Distributed Formation Control of Networked Multi-Agent Systems
JO  - IEEE Transactions on Industrial Electronics
VL  - 64
IS  - 9
SP  - 7731
EP  - 7740
PY  - 2017
DO  - 10.1109/tie.2017.2701778
ER  - 
```

## 格式选择指南

| 场景 | 推荐格式 |
|------|----------|
| 英文论文 | APA 7th |
| 中文论文 | GB/T 7714 |
| LaTeX写作 | BibTeX |
| EndNote/Zotero | RIS |
| Word写作 | APA 或 GB/T |
