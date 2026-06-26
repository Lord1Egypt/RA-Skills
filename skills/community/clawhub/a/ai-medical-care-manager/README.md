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
- 三次提醒生成
- 高德地图路线规划（可选）
- 诊后解释与待办整理（由模型按 SKILL.md 指导完成）

## 额外依赖
- `python3`
- `node`
- `axios`（已在 `package.json` 中声明）

## 路线规划说明
路线规划已改为高德方案：
1. 优先尝试用户 IP 粗定位
2. 若无法获取或不够精确，则让用户手动输入当前位置
3. 将起点和医院终点转为高德坐标
4. 生成高德 Web 路线链接
