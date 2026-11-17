# Boiler Water Treatment Expert

锅炉水处理专家，提供系统设计、工艺优化与运行维护全流程咨询

## 类型

Agent 型（单个 AI 专家）

## 功能

- 系统整体方案设计（补给水预处理、软化、除盐、除氧、加药）
- 关键工艺参数计算与成本估算
- 运行监控方案与故障诊断建议
- 设备清单与维护手册编制

## 使用示例

- 请问我的锅炉系统补给水预处理方案如何优化？
- 如何在锅炉水系统中有效防止结垢和腐蚀？
- 我需要一份锅炉水处理设备清单及维护手册。

## 头像

头像已自动生成在 `avatars/` 目录下。如需替换为自定义头像，要求：
- 格式：PNG（推荐）或 JPG
- 尺寸：512×512 px
- 大小：单张不超过 500KB

## 安装

将专家包目录放到专家目录下：

```
C:\Users\36977\.workbuddy\plugins\marketplaces\my-experts\plugins/boiler-water-treatment-expert/
```

然后运行注册命令使其可见：

```bash
python3 scripts/register_expert.py <expert-dir>
```

## 打包分享

```bash
zip -r boiler-water-treatment-expert.zip boiler-water-treatment-expert/
```
