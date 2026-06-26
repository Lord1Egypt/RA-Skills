# feishu-bitable-plus

企业级飞书多维表格智能操作技能 - 自然语言驱动，纯本地安全部署

## 描述

用自然语言操作飞书多维表格，告别复杂API。

支持批量处理、数据同步、质量分析，纯本地部署保障数据安全。

## 安装

```bash
npx clawhub@latest install feishu-bitable-plus
```

## 使用

```bash
# 配置飞书凭证
fbt config

# 自然语言查询
fbt query "列出客户表的所有记录"

# 交互模式
fbt interactive
```

## 功能

- 自然语言操作表格
- 完整CRUD（增删改查）
- 批量导入导出
- 跨表数据同步
- 数据质量分析

## 权限

- bitable:app
- bitable:record
- bitable:table

## 作者

wenyuan

## 许可证

MIT
