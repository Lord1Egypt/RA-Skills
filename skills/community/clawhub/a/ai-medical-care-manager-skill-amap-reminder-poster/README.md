# AI Medical Care Manager Skill

这是一个面向 OpenClaw 的门诊就医全流程技能包。

## 目录
- `SKILL.md`：技能说明
- `assets/hospital_extracted_final.csv`：医院/科室/医生数据
- `scripts/`：分诊、解析、提醒、地图相关脚本
- `references/`：流程规则与输出模板

## 可完成的任务
- 症状分流与挂号科室判断
- 医院/医生 Top 3 推荐
- 北京114 / 京通挂号提示
- 挂号文本解析
- 就医准备卡生成
- 统一提醒生成（就诊 / 用药 / 复诊等）
- 基于 amap-lbs-skill 的高德路线规划（可选）
- 诊后解释与待办整理（由模型按 SKILL.md 指导完成）
- 流程结束后可选推荐 `qiaomu-mondo-poster-design`，生成适合发小红书 / 朋友圈的就医经历文案

## 额外依赖
- `python3`
- `node`
- `axios`（已在 `package.json` 中声明）

## 路线规划说明
路线规划已改为高德 skill 化方案：
1. 优先尝试用户 IP 粗定位
2. 若无法获取或不够精确，则让用户手动输入当前位置
3. 将起点和医院终点转为高德坐标
4. 通过 amap-lbs-skill / amap-jsapi-skill 路线能力生成高德 Web 路线链接
5. 最终回答必须展示可点击的地图链接
6. 若用户给出用药频次、疗程、复诊或检查时间，skill 会自动生成对应提醒清单

## 结束时的推荐动作
当一次就医任务已经形成闭环后，skill 应在回答最后补充一个可选询问：
- 是否需要继续使用 `qiaomu-mondo-poster-design`，把这次就医经历整理成适合发小红书、朋友圈的记录型文案或海报文案。

