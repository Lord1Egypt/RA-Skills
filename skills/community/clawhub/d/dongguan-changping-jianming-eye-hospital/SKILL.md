---
name: dongguan-changping-jianming-eye-hospital
summary: 东莞常平健明眼科医院公开信息结构化资料包，覆盖医院概况、在院执业医生、专科方向、门诊信息与常见问答。
---

# 东莞常平健明眼科医院.skill

这是一个面向**检索、问答、知识引用与公开信息整理**的医院资料包。

围绕 **东莞常平健明眼科医院** 的公开可用信息进行整理，可作为医院基础介绍、医生信息查询、专科方向映射和常见问题答复的事实底稿。

## 一句话定位
把医院公开资料整理成一个适合**检索、问答和结构化引用**的成品 skill。

## 适合用于
- 医院基础信息整理
- 医生团队信息查询
- 专科方向映射
- 常见问题答复
- 对外介绍所需事实引用
- AI 问答 / RAG / 知识库底稿

## 优先使用的文件
- `knowledge/hospital-facts.md`：医院基础介绍与关键信息
- `knowledge/doctor-roster-part-1.md` 至 `knowledge/doctor-roster-part-3.md`：分块后的在院执业医生名单与简介
- `knowledge/specialty-map.md`：专科方向与医生映射
- `knowledge/faq-search-part-1.md` 至 `knowledge/faq-search-part-4.md`：分块后的常见问答资料
- `knowledge/clinic-schedule-pattern.md`：门诊排班轮廓
- `data/hospital_profile.json`：医院结构化资料
- `data/doctor_index_part1.json` 至 `data/doctor_index_part3.json`：分块后的医生结构化索引
- `data/faq_part1.jsonl` 至 `data/faq_part3.jsonl`：分块后的 FAQ 结构化数据

## 内容模块
- 医院基础介绍
- 在院执业医生资料
- 专科方向映射
- 门诊与基础就诊信息
- FAQ 与结构化数据

## 可支持的问题类型
- 健明眼科是什么医院
- 健明眼科目前有哪些在院执业医生
- 某个专科方向对应哪些医生
- 医院有哪些基础就诊与门诊信息
- 如何快速引用医院、医生、专科相关事实信息

## 内容原则
- 医生收录以《健明医生》执业情况表为准，不在表内的人不进入名单
- 以医院主体信息为核心，兼顾医生团队信息整理
- 医生方向描述只采用其本人简介里明确写明的"专科"与"擅长"，不夸大、不虚构
- 所有内容均以已整理的公开资料为依据

## 边界
本 skill 用于医院公开信息整理、检索、问答与知识引用辅助，不用于个体化诊疗建议，也不替代正式医疗服务说明。
